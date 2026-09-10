from collections.abc import Iterable

import polars as polas

from workeanly.database.connection import create_sql_server_connection
from workeanly.validation.data_quality import validate_raw_data


TABLE_COLUMNS = {
    "dim_company": ["company"],
    "dim_country": ["country", "region"],
    "dim_platform": ["platform"],
    "dim_skill": ["skill"],
    "fact_job_postings": [
        "job_id", "job_title", "company", "country", "region", "platform",
        "experience_level", "employment_type", "salary_min_usd", "salary_max_usd",
        "remote_option", "posting_date", "posting_date_parsed", "applicants_estimate",
    ],
    "bridge_job_skills": ["job_id", "skill"],
}

TARGET_COLUMNS = {
    **TABLE_COLUMNS,
    "fact_job_postings": [
        "job_id", "job_title", "company", "country", "region", "platform",
        "experience_level", "employment_type", "salary_min_usd", "salary_max_usd",
        "remote_option", "posting_date_raw", "posting_date", "applicants_estimate",
    ],
}

LOAD_ORDER = [
    "dim_company",
    "dim_country",
    "dim_platform",
    "dim_skill",
    "fact_job_postings",
    "bridge_job_skills",
]


def assert_sql_ready(tables: dict[str, polas.DataFrame]) -> None:
    report = validate_raw_data(tables)
    invalid_keys = [
        name for name, result in report["key_checks"].items() if not result["is_unique"]
    ]
    problems = {
        "invalid keys": invalid_keys,
        "duplicate bridge pairs": report["bridge_duplicates"].height,
        "orphan skills": report["orphan_skills"].height,
        "orphan jobs": report["orphan_jobs"].height,
    }
    if invalid_keys or any(value for key, value in problems.items() if key != "invalid keys"):
        raise ValueError(f"SQL load stopped because validation failed: {problems}")


def load_to_sql_server(
    tables: dict[str, polas.DataFrame],
    cleaned_tables: dict[str, polas.DataFrame],
    connection_string: str,
    schema: str = "workeanly",
) -> None:
    assert_sql_ready(tables)
    connection = create_sql_server_connection(connection_string)
    try:
        cursor = connection.cursor()
        _assert_target_tables_empty(cursor, schema)
        for table_name in LOAD_ORDER:
            _insert_dataframe(
                cursor,
                schema,
                table_name,
                cleaned_tables[table_name],
                TABLE_COLUMNS[table_name],
                TARGET_COLUMNS[table_name],
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _assert_target_tables_empty(cursor, schema: str) -> None:
    for table_name in LOAD_ORDER:
        cursor.execute(f"SELECT COUNT(*) FROM [{schema}].[{table_name}]")
        if cursor.fetchone()[0] > 0:
            raise ValueError(
                f"Target table [{schema}].[{table_name}] is not empty. "
                "Load was cancelled to prevent duplicates."
            )


def _insert_dataframe(
    cursor,
    schema: str,
    table_name: str,
    data: polas.DataFrame,
    source_columns: list[str],
    target_columns: list[str],
) -> None:
    placeholders = ", ".join("?" for _ in target_columns)
    column_list = ", ".join(f"[{column}]" for column in target_columns)
    statement = f"INSERT INTO [{schema}].[{table_name}] ({column_list}) VALUES ({placeholders})"
    rows = _database_rows(data.select(source_columns).iter_rows())
    cursor.fast_executemany = True
    cursor.executemany(statement, rows)


def _database_rows(rows: Iterable[tuple]) -> list[tuple]:
    return [tuple(None if value is None else value for value in row) for row in rows]
