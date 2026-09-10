IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'workeanly')
    EXEC('CREATE SCHEMA workeanly');
GO

CREATE TABLE workeanly.dim_company (
    company NVARCHAR(200) NOT NULL,
    CONSTRAINT PK_dim_company PRIMARY KEY (company)
);

CREATE TABLE workeanly.dim_country (
    country NVARCHAR(100) NOT NULL,
    region NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_dim_country PRIMARY KEY (country)
);

CREATE TABLE workeanly.dim_platform (
    platform NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_dim_platform PRIMARY KEY (platform)
);

CREATE TABLE workeanly.dim_skill (
    skill NVARCHAR(150) NOT NULL,
    CONSTRAINT PK_dim_skill PRIMARY KEY (skill)
);

CREATE TABLE workeanly.fact_job_postings (
    job_id INT NOT NULL,
    job_title NVARCHAR(250) NOT NULL,
    company NVARCHAR(200) NOT NULL,
    country NVARCHAR(100) NOT NULL,
    region NVARCHAR(100) NOT NULL,
    platform NVARCHAR(100) NOT NULL,
    experience_level NVARCHAR(100) NOT NULL,
    employment_type NVARCHAR(100) NOT NULL,
    salary_min_usd DECIMAL(12, 2) NULL,
    salary_max_usd DECIMAL(12, 2) NULL,
    remote_option NVARCHAR(100) NOT NULL,
    posting_date_raw NVARCHAR(30) NOT NULL,
    posting_date DATE NULL,
    applicants_estimate INT NULL,
    CONSTRAINT PK_fact_job_postings PRIMARY KEY (job_id),
    CONSTRAINT FK_jobs_company FOREIGN KEY (company) REFERENCES workeanly.dim_company(company),
    CONSTRAINT FK_jobs_country FOREIGN KEY (country) REFERENCES workeanly.dim_country(country),
    CONSTRAINT FK_jobs_platform FOREIGN KEY (platform) REFERENCES workeanly.dim_platform(platform)
);

CREATE TABLE workeanly.bridge_job_skills (
    job_id INT NOT NULL,
    skill NVARCHAR(150) NOT NULL,
    CONSTRAINT PK_bridge_job_skills PRIMARY KEY (job_id, skill),
    CONSTRAINT FK_bridge_job FOREIGN KEY (job_id) REFERENCES workeanly.fact_job_postings(job_id),
    CONSTRAINT FK_bridge_skill FOREIGN KEY (skill) REFERENCES workeanly.dim_skill(skill)
);
GO
