CREATE VIEW workeanly.vw_skill_demand AS
SELECT
    skill,
    COUNT(DISTINCT job_id) AS job_count
FROM workeanly.bridge_job_skills
GROUP BY skill;
GO

CREATE VIEW workeanly.vw_salary_by_experience AS
SELECT
    experience_level,
    COUNT(*) AS job_count,
    AVG((salary_min_usd + salary_max_usd) / 2.0) AS avg_salary_usd
FROM workeanly.fact_job_postings
GROUP BY experience_level;
GO
