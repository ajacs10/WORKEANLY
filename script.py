import argparse
import os

from workeanly.analysis.jobs import jobs_by_title, salary_by_experience
from workeanly.analysis.skills import create_job_skills, skills_by_demand
from workeanly.cleaning.transformations import clean_tables
from workeanly.database.sql_server_loader import load_to_sql_server
from workeanly.ingestion.loader import load_raw_data
from workeanly.validation.data_quality import validate_raw_data


def build_connection_string() -> str:
    required_variables = [
        "WORKEANLY_SQL_SERVER",
        "WORKEANLY_SQL_DATABASE",
        "WORKEANLY_SQL_USERNAME",
        "WORKEANLY_SQL_PASSWORD",
    ]
    missing_variables = [name for name in required_variables if not os.getenv(name)]
    if missing_variables:
        raise ValueError(
            "Missing SQL configuration: " + ", ".join(missing_variables)
        )
    driver = os.getenv("WORKEANLY_SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    return (
        f"DRIVER={{{driver}}};SERVER={os.environ['WORKEANLY_SQL_SERVER']};"
        f"DATABASE={os.environ['WORKEANLY_SQL_DATABASE']};"
        f"UID={os.environ['WORKEANLY_SQL_USERNAME']};"
        f"PWD={os.environ['WORKEANLY_SQL_PASSWORD']};TrustServerCertificate=yes;"
    )


def main(load_sql: bool = False) -> None:
    tables = load_raw_data()
    validation_report = validate_raw_data(tables)
    cleaned_tables = clean_tables(tables)
    job_skills = create_job_skills(
        cleaned_tables["fact_job_postings"], cleaned_tables["bridge_job_skills"]
    )

    print("Loaded tables:", ", ".join(tables))
    print("Rows in fact_job_postings:", tables["fact_job_postings"].height)
    print("Bridge duplicate pairs:", validation_report["bridge_duplicates"].height)
    print("Orphan skills:", validation_report["orphan_skills"].height)
    print("Orphan jobs:", validation_report["orphan_jobs"].height)
    print("\nMost requested job titles:")
    print(jobs_by_title(cleaned_tables["fact_job_postings"]).head(10))
    print("\nMost requested skills:")
    print(skills_by_demand(job_skills).head(10))
    print("\nSalary by experience:")
    print(salary_by_experience(cleaned_tables["fact_job_postings"]))

    if load_sql:
        load_to_sql_server(tables, cleaned_tables, build_connection_string())
        print("\nSQL Server load completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the WORKEANLY pipeline.")
    parser.add_argument(
        "--load-sql",
        action="store_true",
        help="Load validated data into empty SQL Server tables.",
    )
    arguments = parser.parse_args()
    main(load_sql=arguments.load_sql)
