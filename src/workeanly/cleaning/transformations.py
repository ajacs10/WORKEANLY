import polars as polas


def clean_fact_job_postings(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    text_columns = [
        "job_title", "company", "country", "region", "platform",
        "experience_level", "employment_type", "remote_option",
    ]
    return (
        fact_job_postings.with_columns(
            [polas.col(column).str.strip_chars().alias(column) for column in text_columns]
        )
        .with_columns(
            polas.col("posting_date")
            .str.to_date(format="%Y-%m-%d", strict=False)
            .alias("posting_date_parsed"),
            ((polas.col("salary_min_usd") + polas.col("salary_max_usd")) / 2).alias(
                "salary_avg_usd"
            ),
        )
    )


def clean_dimensions(tables: dict[str, polas.DataFrame]) -> dict[str, polas.DataFrame]:
    cleaned_tables = tables.copy()
    for table_name, column in {
        "dim_company": "company",
        "dim_country": "country",
        "dim_platform": "platform",
        "dim_skill": "skill",
        "bridge_job_skills": "skill",
    }.items():
        cleaned_tables[table_name] = cleaned_tables[table_name].with_columns(
            polas.col(column).str.strip_chars().alias(column)
        )
    return cleaned_tables


def clean_tables(tables: dict[str, polas.DataFrame]) -> dict[str, polas.DataFrame]:
    cleaned_tables = clean_dimensions(tables)
    cleaned_tables["fact_job_postings"] = clean_fact_job_postings(
        tables["fact_job_postings"]
    )
    return cleaned_tables
