import polars as polas


def create_job_skills(
    fact_job_postings: polas.DataFrame, bridge_job_skills: polas.DataFrame
) -> polas.DataFrame:
    return bridge_job_skills.join(fact_job_postings, on="job_id", how="inner")


def skills_by_demand(job_skills: polas.DataFrame) -> polas.DataFrame:
    return (
        job_skills.group_by("skill")
        .agg(polas.col("job_id").n_unique().alias("job_count"))
        .sort("job_count", descending=True)
    )


def skills_by_job_title(job_skills: polas.DataFrame) -> polas.DataFrame:
    return (
        job_skills.group_by("job_title", "skill")
        .agg(polas.col("job_id").n_unique().alias("job_count"))
        .sort(["job_title", "job_count"], descending=[False, True])
    )


def skills_by_experience(job_skills: polas.DataFrame) -> polas.DataFrame:
    return (
        job_skills.group_by("experience_level", "skill")
        .agg(polas.col("job_id").n_unique().alias("job_count"))
        .sort(["experience_level", "job_count"], descending=[False, True])
    )


def skills_salary_summary(job_skills: polas.DataFrame) -> polas.DataFrame:
    return (
        job_skills.group_by("skill")
        .agg(
            polas.col("job_id").n_unique().alias("job_count"),
            polas.col("salary_avg_usd").mean().round(2).alias("avg_salary_usd"),
        )
        .sort("avg_salary_usd", descending=True, nulls_last=True)
    )
