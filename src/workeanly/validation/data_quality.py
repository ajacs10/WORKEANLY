import polars as polas


def check_nulls(data: polas.DataFrame) -> polas.DataFrame:
    null_counts = data.null_count().transpose(
        include_header=True, header_name="column", column_names=["null_count"]
    )
    return null_counts.filter(polas.col("null_count") > 0)


def check_duplicates(data: polas.DataFrame) -> int:
    return data.filter(data.is_duplicated()).height


def check_unique_column(data: polas.DataFrame, column: str) -> dict[str, int | bool]:
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist.")

    values = data.get_column(column)
    total_rows = data.height
    null_count = values.null_count()
    unique_count = values.n_unique()
    return {
        "total_rows": total_rows,
        "unique_values": unique_count,
        "null_values": null_count,
        "duplicate_values": total_rows - unique_count,
        "is_unique": null_count == 0 and unique_count == total_rows,
    }


def check_bridge_duplicates(bridge_job_skills: polas.DataFrame) -> polas.DataFrame:
    return (
        bridge_job_skills.group_by("job_id", "skill")
        .len()
        .filter(polas.col("len") > 1)
        .sort("len", descending=True)
    )


def check_orphan_skills(
    bridge_job_skills: polas.DataFrame, dim_skill: polas.DataFrame
) -> polas.DataFrame:
    return bridge_job_skills.join(dim_skill, on="skill", how="anti")


def check_orphan_jobs(
    bridge_job_skills: polas.DataFrame, fact_job_postings: polas.DataFrame
) -> polas.DataFrame:
    return bridge_job_skills.join(
        fact_job_postings.select("job_id"), on="job_id", how="anti"
    )


def validate_raw_data(tables: dict[str, polas.DataFrame]) -> dict[str, object]:
    return {
        "nulls": {name: check_nulls(data) for name, data in tables.items()},
        "row_duplicates": {name: check_duplicates(data) for name, data in tables.items()},
        "key_checks": {
            "fact_job_postings.job_id": check_unique_column(tables["fact_job_postings"], "job_id"),
            "dim_company.company": check_unique_column(tables["dim_company"], "company"),
            "dim_country.country": check_unique_column(tables["dim_country"], "country"),
            "dim_platform.platform": check_unique_column(tables["dim_platform"], "platform"),
            "dim_skill.skill": check_unique_column(tables["dim_skill"], "skill"),
        },
        "bridge_duplicates": check_bridge_duplicates(tables["bridge_job_skills"]),
        "orphan_skills": check_orphan_skills(tables["bridge_job_skills"], tables["dim_skill"]),
        "orphan_jobs": check_orphan_jobs(tables["bridge_job_skills"], tables["fact_job_postings"]),
    }
