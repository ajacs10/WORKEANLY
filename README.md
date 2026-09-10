# WORKEANLY

### Labour Market Intelligence & Skills Analytics

WORKEANLY is an end-to-end labour market analytics project designed to transform job-posting data into structured, reliable and actionable insights about hiring demand, skills, salaries, experience levels, employment types and geographic patterns.

The project combines **Python and Polars** for data ingestion, exploration, cleaning, transformation and validation, **Microsoft SQL Server** for relational data modelling and analytical SQL, and **Power BI** for business intelligence and interactive data visualisation.

> **Project status:** In development

---

## Overview

The labour market generates large amounts of job-posting data containing information about roles, companies, skills, locations, salaries and candidate requirements.

WORKEANLY explores this data from an analytical and business perspective, with the goal of answering questions such as:

* Which job roles have the highest hiring demand?
* Which technical skills are most frequently requested?
* Which companies are hiring for specific roles?
* How does skill demand vary across experience levels?
* Which countries and regions have the highest job-posting volume?
* How are salaries distributed across roles and experience levels?
* What is the relationship between salary and experience level?
* Which skills are associated with specific job roles?
* How common are remote opportunities?
* What patterns can be identified in the labour market?

The project is structured as a complete analytical workflow rather than a collection of isolated notebooks.

---

## Objectives

The main objectives of WORKEANLY are to:

1. Build a reproducible data ingestion workflow.
2. Understand and profile raw labour-market data.
3. Identify data-quality issues before analysis.
4. Clean and transform data using Python and Polars.
5. Validate relationships between datasets.
6. Model the data using a relational structure.
7. Store and analyse structured data in Microsoft SQL Server.
8. Answer business questions using analytical SQL.
9. Prepare analytical datasets for Business Intelligence.
10. Build Power BI dashboards to communicate the resulting insights.

---

## Data Source

The project uses the **Job Market Intelligence 2024 – Skills Global Dataset**.

The dataset contains job-posting information and supporting dimension tables covering areas such as:

* Job postings
* Companies
* Countries and regions
* Platforms
* Skills
* Job-to-skill relationships

The raw data is organised into fact, dimension and bridge datasets to support relational analysis.

### Dataset tables

| Table               | Purpose                                           |
| ------------------- | ------------------------------------------------- |
| `fact_job_postings` | Core job-posting information                      |
| `dim_company`       | Company reference data                            |
| `dim_country`       | Country and regional information                  |
| `dim_platform`      | Job-platform information                          |
| `dim_skill`         | Skill reference data                              |
| `bridge_job_skills` | Many-to-many relationship between jobs and skills |

---

## Data Model

WORKEANLY uses a relational model based on **fact, dimension and bridge tables**.

```text
                         dim_company
                              │
                              │
                              ▼
dim_country ─────────► fact_job_postings ◄───────── dim_platform
                              │
                              │
                              │
                              ▼
                       bridge_job_skills
                              │
                              │
                              ▼
                         dim_skill
```

### Fact table

`fact_job_postings` represents individual job postings.

Main attributes include:

* `job_id`
* `job_title`
* `company`
* `country`
* `region`
* `platform`
* `experience_level`
* `employment_type`
* `salary_min_usd`
* `salary_max_usd`
* `remote_option`
* `posting_date`
* `applicants_estimate`

### Dimension tables

The dimension tables provide descriptive information used to analyse the fact data.

#### `dim_company`

Contains unique companies.

```text
company
```

#### `dim_country`

Contains countries and their corresponding regions.

```text
country
region
```

#### `dim_platform`

Contains the platforms where job postings were published.

```text
platform
```

#### `dim_skill`

Contains the available skills associated with job postings.

```text
skill
```

### Bridge table

`bridge_job_skills` represents the many-to-many relationship between job postings and skills.

```text
job_id
skill
```

A single job can require multiple skills, while the same skill can be required by many jobs.

The logical composite key is:

```text
(job_id, skill)
```

---

## Analytical Workflow

The project follows a structured data-analysis pipeline:

```text
Raw CSV Data
     │
     ▼
Data Ingestion
     │
     ▼
Data Profiling
     │
     ▼
Data Quality Validation
     │
     ▼
Cleaning & Transformation
     │
     ▼
Exploratory Data Analysis
     │
     ▼
Relational Data Model
     │
     ▼
Microsoft SQL Server
     │
     ▼
Analytical SQL
     │
     ▼
Power BI
     │
     ▼
Business Insights
```

Each stage has a specific responsibility and is kept separate to make the project easier to maintain, test and extend.

---

# Technology Stack

## Python

Python is used as the main programming language for the data-processing layer.

Responsibilities include:

* Data ingestion
* Data profiling
* Data cleaning
* Data transformation
* Data validation
* Exploratory analysis
* Reusable analytical functions

## Polars

Polars is used as the primary DataFrame library.

It is used for:

* Reading CSV files
* Inspecting schemas
* Handling missing values
* Grouping and aggregation
* Joining datasets
* Filtering
* Transformation
* Statistical calculations
* Data validation

The project intentionally uses Polars instead of relying on a large number of data-processing libraries.

## Microsoft SQL Server

Microsoft SQL Server is used as the relational database and analytical SQL layer.

Responsibilities include:

* Relational data storage
* Table modelling
* Primary and foreign keys
* Referential integrity
* SQL querying
* Aggregations
* Joins
* Analytical views and queries
* Preparing data for Business Intelligence

## Power BI

Power BI is used as the visualisation and Business Intelligence layer.

The dashboard layer is designed to communicate analytical results rather than perform the core data-processing work.

Potential dashboard areas include:

* Labour market overview
* Job demand
* Skill demand
* Salary analysis
* Experience analysis
* Geographic analysis
* Remote work
* Company hiring activity

---

# Project Structure

```text
WORKEANLY/
│
├── data/
│   ├── raw/
│   │   ├── fact_job_postings.csv
│   │   ├── dim_company.csv
│   │   ├── dim_country.csv
│   │   ├── dim_platform.csv
│   │   ├── dim_skill.csv
│   │   └── bridge_job_skills.csv
│   │
│   └── processed/
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── src/
│   └── workeanly/
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── jobs.py
│       │   └── skills.py
│       │
│       ├── cleaning/
│       │   └── __init__.py
│       │
│       ├── database/
│       │   ├── __init__.py
│       │   └── connection.py
│       │
│       ├── ingestion/
│       │   ├── __init__.py
│       │   └── loader.py
│       │
│       └── validation/
│           ├── __init__.py
│           └── data_quality.py
│
├── script.py
├── README.md
└── LICENSE
```

---

# Data Ingestion

The ingestion layer is responsible only for loading the raw datasets.

The main loader is:

```text
src/workeanly/ingestion/loader.py
```

It reads the CSV files from:

```text
data/raw/
```

and returns them as a dictionary of Polars DataFrames.

Conceptually:

```python
tables = load_raw_data()
```

The resulting structure is:

```text
tables
│
├── fact_job_postings
├── dim_company
├── dim_country
├── dim_platform
├── dim_skill
└── bridge_job_skills
```

This separation keeps file loading independent from validation and analysis.

---

# Data Quality

Before performing analytical calculations, WORKEANLY validates the structure and relationships of the data.

The validation layer checks:

### Missing values

Identify columns containing null values.

```text
check_nulls()
```

### Duplicate records

Check whether rows are duplicated.

```text
check_duplicates()
```

### Unique values

Evaluate candidate keys and reference columns.

```text
check_unique_column()
```

### Duplicate job-skill relationships

Validate that the same job-skill pair does not appear multiple times.

```text
(job_id, skill)
```

### Orphan skills

Verify that every skill referenced by `bridge_job_skills` exists in `dim_skill`.

### Orphan jobs

Verify that every `job_id` referenced by `bridge_job_skills` exists in `fact_job_postings`.

These checks help ensure that analytical results are based on structurally consistent data.

---

# Exploratory Data Analysis

The exploratory analysis layer is used to understand the dataset before building the final analytical model.

Examples of analyses include:

## Job demand

Determine the number of postings by job title.

```text
job_title
job_count
```

This makes it possible to identify roles with the highest representation in the dataset.

## Salary analysis

Calculate metrics such as:

* Average salary
* Median salary
* Minimum salary
* Maximum salary
* Salary by role
* Salary by experience level

For postings containing minimum and maximum salary values, an average salary estimate can be calculated as:

```text
average salary = (salary_min + salary_max) / 2
```

## Applicant analysis

Analyse:

* Average estimated applicants
* Applicants by job title
* Applicants relative to job-posting volume

## Skill demand

Measure how many different job postings require each skill.

A job may contain the same skill only once in the logical relationship:

```text
job_id + skill
```

Therefore, skill demand is analysed using the number of distinct jobs requiring each skill.

## Skill and experience analysis

Analyse relationships such as:

```text
Skill → Experience Level
```

This can help identify which skills are more frequently associated with junior, mid-level or senior positions.

## Geographic analysis

Analyse job demand across:

* Countries
* Regions
* Job titles
* Skills
* Remote options

---

# Business Questions

The project is designed around business-oriented questions rather than purely technical metrics.

### Hiring demand

* What are the most frequently advertised job roles?
* Which roles represent the largest share of job postings?
* Which companies advertise the highest number of positions?

### Skills

* Which skills are most demanded?
* Which skills appear together frequently?
* Which skills are associated with specific job roles?
* Which skills are more common at higher experience levels?

### Compensation

* Which roles have the highest salary ranges?
* How does compensation vary by experience level?
* Is higher experience associated with higher salary?
* Which skills are associated with higher-paying roles?

### Geography

* Which countries have the highest job-posting volume?
* How does demand vary by region?
* Which skills are most demanded in different locations?

### Work model

* How common are remote opportunities?
* Which roles have the highest proportion of remote postings?
* Does remote availability vary by country or experience level?

---

# Example Analytical Questions

The project can produce outputs such as:

```text
Top job titles by posting volume

Top skills by number of unique job postings

Average salary by experience level

Median salary by job title

Job demand by country

Remote vs non-remote opportunities

Skills by experience level

Companies with the highest hiring volume
```

The objective is not simply to calculate these metrics, but to transform them into information that can support interpretation and decision-making.

---

# Data Quality Principles

WORKEANLY follows several principles throughout the analytical workflow:

### Validate before analysing

Data is checked before being used to generate business conclusions.

### Separate responsibilities

Loading, validation, cleaning, analysis and database operations are kept in separate modules.

### Preserve traceability

Raw data remains separated from processed data.

### Avoid unnecessary transformations

Transformations are introduced when they have an analytical or modelling purpose.

### Use reproducible analysis

Important analytical operations are implemented as reusable Python functions rather than existing only as notebook cells.

### Validate relationships

Foreign-key-like relationships are checked before being represented in the relational database.

---

# SQL Server Data Model

The planned relational model is:

```text
dim_company
-----------
company (PK)


dim_country
-----------
country (PK)
region


dim_platform
------------
platform (PK)


dim_skill
---------
skill (PK)


fact_job_postings
-----------------
job_id (PK)
job_title
company (FK)
country (FK)
region
platform (FK)
experience_level
employment_type
salary_min_usd
salary_max_usd
remote_option
posting_date
applicants_estimate


bridge_job_skills
-----------------
job_id (FK)
skill (FK)

PRIMARY KEY (job_id, skill)
```

The exact implementation may evolve as the data model is validated and implemented in SQL Server.

---

# Power BI

Power BI will serve as the Business Intelligence layer.

The dashboard will focus on presenting the most relevant labour-market indicators in a clear and decision-oriented format.

Potential dashboard sections:

### Labour Market Overview

* Total job postings
* Number of companies
* Number of skills
* Average salary
* Average estimated applicants
* Remote-job share

### Job Demand

* Top job titles
* Job postings by experience level
* Job postings by employment type

### Skills Intelligence

* Most demanded skills
* Skills by job title
* Skills by experience level

### Compensation

* Salary by role
* Salary by experience
* Salary distribution

### Geographic Intelligence

* Job postings by country
* Job postings by region
* Skills by geography
* Remote opportunities by location

The final dashboard will be based on validated analytical data rather than raw CSV files.

---

# Installation

## Requirements

The project requires:

* Python 3.x
* Polars
* Microsoft SQL Server
* Power BI Desktop for the visualisation layer

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install the Python dependency:

```bash
pip install polars
```

---

# Running the Project

From the project root:

```bash
cd WORKEANLY
```

Run the main script:

```bash
python script.py
```

The ingestion layer can be used through:

```python
from src.workeanly.ingestion.loader import load_raw_data

tables = load_raw_data()
```

The returned dictionary contains the project's raw DataFrames.

---

# Development Approach

The project is being developed incrementally.

The current development sequence is:

```text
1. Data ingestion
        ↓
2. Data profiling
        ↓
3. Data quality validation
        ↓
4. Data cleaning
        ↓
5. Exploratory analysis
        ↓
6. Analytical functions
        ↓
7. SQL Server modelling
        ↓
8. SQL analytics
        ↓
9. Power BI dashboard
        ↓
10. Final documentation and insights
```

This approach makes it possible to validate each stage before building the next one.

---

# Project Status

### Completed / In Progress

* [x] Raw dataset acquisition
* [x] Dataset structure inspection
* [x] DataFrame profiling
* [x] Schema inspection
* [x] Null-value inspection
* [x] Duplicate checks
* [x] Initial exploratory analysis
* [x] Initial relational model design
* [x] Python project structure
* [x] Data ingestion module
* [x] Initial data-quality module
* [ ] Cleaning pipeline
* [ ] Reusable job analysis module
* [ ] Reusable skills analysis module
* [ ] SQL Server implementation
* [ ] Analytical SQL layer
* [ ] Power BI dashboard
* [ ] Final business insights
* [ ] Final project documentation

---

# Limitations

Job-posting data provides useful signals about labour-market demand, but it does not represent the entire labour market.

Potential limitations include:

* Not every job vacancy is published online.
* Different platforms may represent different segments of the labour market.
* Salary information may be incomplete or estimated.
* Applicant counts may be estimates rather than exact values.
* Job-posting distributions may reflect the composition of the source dataset rather than the entire global labour market.
* Historical or temporal analysis depends on the quality and consistency of the available posting dates.

Therefore, WORKEANLY treats the dataset as a source of **labour-market signals**, not as a complete representation of global employment.

---

# What This Project Demonstrates

WORKEANLY demonstrates practical skills across the data-analysis lifecycle:

### Data

* Data ingestion
* Data profiling
* Data cleaning
* Data validation
* Data transformation
* Exploratory Data Analysis

### Programming

* Python
* Polars
* Reusable functions
* Modular project structure

### Databases

* Relational modelling
* Fact and dimension tables
* Many-to-many relationships
* Primary and foreign keys
* SQL Server
* Analytical SQL

### Business Intelligence

* KPI design
* Data visualisation
* Dashboard development
* Business-oriented analysis
* Insight communication

### Analytical Thinking

* Translating business questions into analytical queries
* Validating data before drawing conclusions
* Identifying relationships between roles, skills, salaries and experience
* Communicating data-driven findings

---

# Future Improvements

Future iterations may include:

* More robust date handling
* Additional data-quality rules
* Advanced salary analysis
* Skill co-occurrence analysis
* Job-title normalisation
* Additional geographic analysis
* SQL Server views for BI consumption
* Power BI semantic modelling
* Automated data-quality reporting
* Additional labour-market indicators

New technologies will only be introduced when they provide a clear analytical or engineering benefit.

---

# Repository Philosophy

WORKEANLY is designed around three principles:

**Reliable data**

> Analytical results are only useful when the underlying data has been properly validated.

**Clear architecture**

> Each stage of the pipeline has a defined responsibility.

**Business-oriented analysis**

> The purpose of the project is not only to process data, but to turn data into information that can answer meaningful labour-market questions.

---

# Author

**Ana Juliana Avelino da Costa Sobrinho**

Software Engineer | Data Analytics

Luanda, Angola

---

# License

This project is licensed under the **MIT License**.

The MIT License permits others to use, modify, distribute and reuse the software, subject to the conditions defined in the license.

See the `LICENSE` file for the complete license text.
