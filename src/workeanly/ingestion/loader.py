from pathlib import Path

import polars as polas


RAW_DATA_DIR = Path("data/raw")


def load_raw_data(raw_data_dir: Path = RAW_DATA_DIR) -> dict[str, polas.DataFrame]:
    file_names = {
        "fact_job_postings": "fact_job_postings.csv",
        "bridge_job_skills": "bridge_job_skills.csv",
        "dim_company": "dim_company.csv",
        "dim_country": "dim_country.csv",
        "dim_platform": "dim_platform.csv",
        "dim_skill": "dim_skill.csv",
    }
    missing_files = [
        name for name in file_names.values() if not (raw_data_dir / name).is_file()
    ]
    if missing_files:
        raise FileNotFoundError(
            f"Raw data files not found in '{raw_data_dir}': {', '.join(missing_files)}"
        )
    return {
        table_name: polas.read_csv(raw_data_dir / file_name)
        for table_name, file_name in file_names.items()
    }
