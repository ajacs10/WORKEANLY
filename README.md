# WORKEANLY

### Labour Market Intelligence & Skills Analytics

WORKEANLY is an end-to-end data analytics project that turns global job-posting data into reliable insights about hiring demand, skills, compensation, experience requirements, employment types, remote work, companies and geography.

The project is designed as a professional Data Analyst portfolio case study. It demonstrates a complete analytical workflow: raw-data ingestion, quality validation, transformation, relational modelling, SQL analysis and business intelligence reporting.

## Project status

| Area | Status |
| --- | --- |
| Dataset definition | Ready |
| Python and Polars pipeline | Implemented and tested locally |
| Data-quality validation | Implemented and tested locally |
| SQL Server data model | Implemented; awaiting a configured SQL Server instance |
| Analytical SQL views | Implemented; awaiting database execution |
| Power BI dashboard | Planned |

## Business objective

Labour-market data is valuable only when it can answer useful questions. WORKEANLY focuses on the following areas:

- Which job titles have the highest hiring demand?
- Which companies publish the most opportunities?
- Which countries and regions have the greatest job-posting volume?
- Which skills are requested most often?
- Which skills are associated with specific roles and experience levels?
- How do salary ranges vary by role, location and seniority?
- How common are remote opportunities?
- What skills may represent potential market gaps?

The objective is not only to calculate metrics. It is to produce a documented, reproducible analytical model that supports clear business interpretation.

## Dataset

WORKEANLY uses the **Job Market Intelligence 2024 – Skills Global Dataset**. The source data is organised into a fact table, four dimensions and one bridge table.

| Dataset | Grain | Purpose |
| --- | --- | --- |
| `fact_job_postings` | One row per job posting | Stores the core attributes of each advertised job. |
| `dim_company` | One row per company | Provides company reference data. |
| `dim_country` | One row per country | Provides country and region reference data. |
| `dim_platform` | One row per job platform | Identifies the source platform of a posting. |
| `dim_skill` | One row per skill | Provides the controlled skill list. |
| `bridge_job_skills` | One row per job–skill pair | Resolves the many-to-many relationship between jobs and skills. |

### Source files

```text
data/raw/
├── fact_job_postings.csv
├── bridge_job_skills.csv
├── dim_company.csv
├── dim_country.csv
├── dim_platform.csv
└── dim_skill.csv
```

`job_skills` is not a source CSV. It is an analytical DataFrame created when needed by joining `fact_job_postings` with `bridge_job_skills` on `job_id`.

## Data model

```text
dim_company                 dim_country                 dim_platform
    │                            │                            │
    └────────────────────────────┴───────────────┬────────────┘
                                                   ▼
                                         fact_job_postings
                                                   │
                                                   ▼
                                         bridge_job_skills
                                                   │
                                                   ▼
                                               dim_skill
```

### Fact table: `fact_job_postings`

The fact table represents the central business event: a job posting. Its expected fields are:

```text
job_id
job_title
company
country
region
platform
experience_level
employment_type
salary_min_usd
salary_max_usd
remote_option
posting_date
applicants_estimate
```

`job_id` is expected to become the primary key only after uniqueness and null checks have passed.

### Dimension tables

| Table | Candidate key | Attributes |
| --- | --- | --- |
| `dim_company` | `company` | Company name |
| `dim_country` | `country` | Country, region |
| `dim_platform` | `platform` | Platform name |
| `dim_skill` | `skill` | Skill name |

### Bridge table: `bridge_job_skills`

One job can require several skills, and one skill can occur in several jobs. This is a many-to-many relationship, represented by the bridge table.

```text
job_id + skill
```

The composite pair `(job_id, skill)` must be unique. Once validated, it becomes the bridge table primary key. `job_id` and `skill` then become foreign keys to `fact_job_postings` and `dim_skill` respectively.

## Architecture and data flow

```text
Raw CSV files
    ↓
Python + Polars ingestion
    ↓
Data-quality validation
    ↓
Cleaning and transformation
    ↓
Reusable analytical DataFrames
    ↓
Microsoft SQL Server
    ↓
Analytical SQL and views
    ↓
Power BI dashboard
```

Each layer has one responsibility:

| Layer | Responsibility |
| --- | --- |
| `data/raw` | Immutable source CSV files. |
| `ingestion` | Reads CSV files into Polars DataFrames. |
| `validation` | Tests quality, uniqueness and referential integrity. |
| `cleaning` | Standardises valid values and creates analysis-ready fields. |
| `analysis` | Provides reusable business calculations. |
| SQL Server | Stores validated relational data and serves analytical queries. |
| Power BI | Delivers interactive visual analysis; it does not replace the transformation layer. |

## Data-quality strategy

No primary key or foreign key is assumed before validation. The pipeline must verify the following controls before loading data into SQL Server:

| Control | Purpose | Expected result |
| --- | --- | --- |
| Null check | Identifies missing values by column. | Reviewed and documented. |
| Duplicate-row check | Detects repeated full records. | Zero unexpected duplicates. |
| Unique-key check | Validates primary-key candidates. | One distinct, non-null value per row. |
| Bridge duplicate check | Detects repeated `(job_id, skill)` relationships. | Zero duplicate pairs. |
| Orphan-skill check | Finds bridge skills missing from `dim_skill`. | Zero rows. |
| Orphan-job check | Finds bridge jobs missing from `fact_job_postings`. | Zero rows. |

An orphan is a record whose reference does not exist in its parent table. For example, a skill in `bridge_job_skills` is orphaned if that skill is absent from `dim_skill`. In Polars, an anti join returns exactly these unmatched rows. Zero rows means the relationship is valid for a SQL Server foreign key.

## Planned analytics

### Job demand

- Posting volume by job title
- Hiring volume by company
- Posting volume by country and region
- Employment-type distribution
- Remote versus non-remote opportunities
- Job-posting volume by experience level

### Skills intelligence

- Most demanded skills, measured by distinct `job_id`
- Skills by job title
- Skills by experience level
- Skills associated with higher salary ranges
- Potential skills gaps based on demand patterns

### Compensation and experience

- Average, minimum and maximum salary by role
- Salary distribution by experience level
- Relationship between experience and salary
- Salary comparison by geography and employment type

### Market trends

- Job-posting volume over time, when valid dates are available
- Growth or decline by role, skill, country and platform
- Remote-work patterns over time

## Technology stack

| Technology | Role in WORKEANLY |
| --- | --- |
| Python | Main language for data processing and automation. |
| Polars | Fast, expressive DataFrame operations for ingestion, validation, joins and aggregation. |
| Jupyter Notebook | Exploration, learning, experiments and visual investigation. |
| Microsoft SQL Server | Relational storage, integrity constraints, joins, aggregations and views. |
| Power BI | KPI reporting, interactive filtering and dashboard presentation. |

The stack intentionally avoids unnecessary infrastructure. The project prioritises strong data fundamentals over operational complexity.

## Local setup and execution

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Run the local pipeline

Run this command from the repository root:

```bash
PYTHONPATH=src python script.py
```

The command loads the raw CSV files, runs validation checks, prepares cleaned tables, creates the `job_skills` analytical DataFrame and prints selected business outputs.

### 4. Run automated tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

### 5. Load validated data into SQL Server

Execute the schema script in the target database, configure credentials as local environment variables, then run the optional load command:

```bash
PYTHONPATH=src python script.py --load-sql
```

The SQL loader refuses to insert data into non-empty destination tables. This avoids accidental duplicate loads and preserves the integrity of the database model.

## Project structure

```text
WORKEANLY/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_data_exploration.ipynb
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load.sql
│   └── 03_analytics_views.sql
├── src/
│   └── workeanly/
│       ├── analysis/
│       │   ├── jobs.py
│       │   └── skills.py
│       ├── cleaning/
│       │   └── transformations.py
│       ├── database/
│       │   └── connection.py
│       ├── ingestion/
│       │   └── loader.py
│       └── validation/
│           └── data_quality.py
├── README.md
├── SECURITY.md
├── pyproject.toml
├── requirements.txt
├── tests/
│   └── test_pipeline.py
└── .github/
    └── workflows/ci.yml
```

The repository also contains `.github/workflows/ci.yml`, which compiles the code and runs the pipeline tests on every push and pull request to `main`.

## Implementation roadmap

1. Load each raw CSV with Polars.
2. Profile schema, row counts, nulls, duplicates and value distributions.
3. Validate candidate keys and bridge-table integrity.
4. Apply documented cleaning transformations without modifying source files.
5. Build reusable job and skill analysis functions.
6. Create and populate the validated SQL Server model.
7. Develop analytical SQL queries and views.
8. Connect Power BI to SQL Server.
9. Design a minimal, accessible dashboard with clear KPIs and filters.
10. Document insights, assumptions, limitations and recommendations.

## Power BI dashboard plan

The final dashboard will use a restrained, enterprise-style visual language: white and neutral grey surfaces, dark text and one discrete accent colour. It will prioritise readability, comparison and meaningful interaction.

Proposed pages:

| Page | Main content |
| --- | --- |
| Market overview | Total postings, top roles, top companies, top countries and remote share. |
| Skills demand | Most requested skills, skills by role and skills by experience level. |
| Compensation | Salary distributions and salary by role, level and location. |
| Geography and work model | Country and region analysis, employment type and remote patterns. |

Recommended filters include country, region, job title, company, platform, experience level, employment type and remote option.

## How this project can be explained in an interview

WORKEANLY demonstrates an analytical workflow rather than a single dashboard. The explanation should follow the data flow:

1. Raw CSV files are loaded into Polars DataFrames.
2. Quality checks identify nulls, duplicates, invalid key candidates and broken relationships.
3. Cleaning creates consistent, analysis-ready fields while preserving raw source data.
4. Jobs and skills are connected through a bridge table because their relationship is many-to-many.
5. Validated data is loaded into SQL Server, where PK/FK constraints enforce relational integrity.
6. SQL views provide stable datasets for Power BI.
7. Power BI focuses on communicating KPIs and interactive business insights.

## License

This project is intended for educational and portfolio purposes. Dataset usage remains subject to the source dataset licence.
