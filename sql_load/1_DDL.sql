-- SQL Server Code
-- Creating the jobs DB
CREATE DATABASE linkedin_jobs_db;
USE linkedin_jobs_db;

-- Designing the Database & Tables
-- Create company_dim table with primary key
CREATE TABLE dbo.company_dim
(   company_id INT PRIMARY KEY,
    name NVARCHAR(MAX),
    link NVARCHAR(MAX),
    link_google NVARCHAR(MAX),
    thumbnail NVARCHAR(MAX) );

-- Create skills_dim table with primary key
CREATE TABLE dbo.skills_dim
(   skill_id INT PRIMARY KEY,
    skills NVARCHAR(MAX),
    type NVARCHAR(MAX) );

-- Create job_postings_fact table with primary key
CREATE TABLE dbo.job_postings_fact
(  job_id INT PRIMARY KEY,
    company_id INT,
    job_title_short VARCHAR(255),
    job_title NVARCHAR(MAX),
    job_location NVARCHAR(MAX),
    job_via NVARCHAR(MAX),
    job_schedule_type NVARCHAR(MAX),
    job_work_from_home BIT,
    search_location NVARCHAR(MAX),
    job_posted_year DATE, 
    job_no_degree_mention BIT,
    job_health_insurance BIT,
    job_country NVARCHAR(MAX),
    salary_rate NVARCHAR(MAX),
    salary_year_avg DECIMAL(18,2), 
    salary_hour_avg DECIMAL(18,2),
    CONSTRAINT FK_JobPostings_Company FOREIGN KEY (company_id) 
       REFERENCES dbo.company_dim (company_id) );

-- Create skills_job_dim table with a composite primary key and foreign keys
CREATE TABLE dbo.skills_job_dim
(
    job_id INT,
    skill_id INT,
    PRIMARY KEY (job_id, skill_id),
    CONSTRAINT FK_SkillsJob_Job FOREIGN KEY (job_id) 
       REFERENCES dbo.job_postings_fact (job_id),
    CONSTRAINT FK_SkillsJob_Skill FOREIGN KEY (skill_id) 
       REFERENCES dbo.skills_dim (skill_id) );

-- Create indexes on foreign key columns for better performance
CREATE INDEX idx_company_id ON dbo.job_postings_fact (company_id);
CREATE INDEX idx_skill_id ON dbo.skills_job_dim (skill_id);
CREATE INDEX idx_job_id ON dbo.skills_job_dim (job_id);

SELECT * FROM job_postings_fact
