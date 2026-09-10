import unittest

from workeanly.analysis.skills import create_job_skills, skills_by_demand
from workeanly.cleaning.transformations import clean_tables
from workeanly.ingestion.loader import load_raw_data
from workeanly.validation.data_quality import validate_raw_data


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = load_raw_data()
        cls.cleaned_tables = clean_tables(cls.tables)
        cls.validation_report = validate_raw_data(cls.tables)

    def test_expected_tables_are_loaded(self):
        self.assertEqual(
            set(self.tables),
            {
                "fact_job_postings",
                "bridge_job_skills",
                "dim_company",
                "dim_country",
                "dim_platform",
                "dim_skill",
            },
        )

    def test_bridge_references_are_valid(self):
        self.assertEqual(self.validation_report["bridge_duplicates"].height, 0)
        self.assertEqual(self.validation_report["orphan_skills"].height, 0)
        self.assertEqual(self.validation_report["orphan_jobs"].height, 0)

    def test_job_skills_preserves_valid_bridge_rows(self):
        job_skills = create_job_skills(
            self.cleaned_tables["fact_job_postings"],
            self.cleaned_tables["bridge_job_skills"],
        )
        self.assertEqual(job_skills.height, self.tables["bridge_job_skills"].height)
        self.assertEqual(
            skills_by_demand(job_skills).height,
            self.tables["dim_skill"].height,
        )
