import polars as polas


def jobs_by_title(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return _count_jobs(fact_job_postings, "job_title")


def jobs_by_company(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return _count_jobs(fact_job_postings, "company")


def jobs_by_country(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return _count_jobs(fact_job_postings, "country")


def jobs_by_experience(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return _count_jobs(fact_job_postings, "experience_level")


def jobs_by_employment_type(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return _count_jobs(fact_job_postings, "employment_type")


def remote_job_summary(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return _count_jobs(fact_job_postings, "remote_option")


def salary_by_experience(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    return (
        fact_job_postings.group_by("experience_level")
        .agg(
            polas.len().alias("job_count"),
            polas.col("salary_avg_usd").mean().round(2).alias("avg_salary_usd"),
            polas.col("salary_min_usd").mean().round(2).alias("avg_min_salary_usd"),
            polas.col("salary_max_usd").mean().round(2).alias("avg_max_salary_usd"),
        )
        .sort("avg_salary_usd", descending=True, nulls_last=True)
    )


def job_posting_trend(fact_job_postings: polas.DataFrame) -> polas.DataFrame:
    if "posting_date_parsed" not in fact_job_postings.columns:
        raise ValueError("Run clean_fact_job_postings before calculating trends.")
    return (
        fact_job_postings.with_columns(
            polas.col("posting_date_parsed").dt.truncate("1mo").alias("posting_month")
        )
        .filter(polas.col("posting_month").is_not_null())
        .group_by("posting_month")
        .len()
        .rename({"len": "job_count"})
        .sort("posting_month")
    )


def _count_jobs(fact_job_postings: polas.DataFrame, column: str) -> polas.DataFrame:
    return (
        fact_job_postings.group_by(column)
        .len()
        .rename({"len": "job_count"})
        .sort("job_count", descending=True)
    )
