# Student Profile Database Schema

This document outlines the database schema for storing student profiles in the GSoC Buddy system.

## Tables

### students

Primary table for student information.

| Column | Type | Description |
|--------|------|-------------|
| student_id | uuid | Primary key, auto-generated |
| github_username | text | GitHub username (unique) |
| display_name | text | Name to display in communications |
| email | text | Email address (optional) |
| telegram_id | text | Telegram user ID (optional) |
| discord_id | text | Discord user ID (optional) |
| timezone | text | Student's timezone (e.g., "UTC+2") |
| available_hours_weekly | integer | Hours available for contributions per week |
| preferred_contact_method | text | "telegram", "discord", or "email" |
| learning_style | text | Brief description of preferred learning style |
| gsoc_goals | text | Student's goals for GSoC participation |
| bio | text | Short student bio/introduction |
| is_active | boolean | Whether the student is actively using the system |
| created_at | timestamp | When the profile was created |
| updated_at | timestamp | When the profile was last updated |

### student_skills

Skills possessed by students with proficiency levels.

| Column | Type | Description |
|--------|------|-------------|
| skill_id | uuid | Primary key, auto-generated |
| student_id | uuid | Foreign key to students.student_id |
| skill_name | text | Name of the skill (e.g., "Python", "React") |
| skill_type | text | "language", "framework", "tool", or "domain" |
| proficiency | text | "beginner", "intermediate", or "advanced" |
| years_experience | float | Years of experience with this skill |
| is_primary | boolean | Whether this is a primary/focus skill |
| created_at | timestamp | When the skill was added |
| updated_at | timestamp | When the skill was last updated |

### student_target_orgs

Organizations that students are targeting for GSoC.

| Column | Type | Description |
|--------|------|-------------|
| target_id | uuid | Primary key, auto-generated |
| student_id | uuid | Foreign key to students.student_id |
| org_name | text | Name of the target organization |
| priority | integer | Priority level (1=highest) |
| reason | text | Why the student is interested in this org |
| created_at | timestamp | When the target was added |

### student_contributions

Past open source contributions made by students.

| Column | Type | Description |
|--------|------|-------------|
| contribution_id | uuid | Primary key, auto-generated |
| student_id | uuid | Foreign key to students.student_id |
| repo_name | text | Repository name with owner (e.g., "org/repo") |
| contribution_type | text | "issue", "pr", or "discussion" |
| url | text | URL to the contribution |
| description | text | Brief description of the contribution |
| created_at | timestamp | When the contribution was made |
| is_gsoc_related | boolean | Whether it was part of GSoC |

### student_preferences

Additional preferences for matching and recommendations.

| Column | Type | Description |
|--------|------|-------------|
| preference_id | uuid | Primary key, auto-generated |
| student_id | uuid | Foreign key to students.student_id |
| preference_key | text | Preference identifier |
| preference_value | text | Preference value |
| created_at | timestamp | When the preference was set |
| updated_at | timestamp | When the preference was last updated |

## Relationships

- `students` 1:N `student_skills` (one student has many skills)
- `students` 1:N `student_target_orgs` (one student targets many orgs)
- `students` 1:N `student_contributions` (one student has many contributions)
- `students` 1:N `student_preferences` (one student has many preferences)

## Common Preference Keys

- `difficulty_max`: Maximum preferred issue difficulty (1-10)
- `difficulty_min`: Minimum preferred issue difficulty (1-10)
- `notify_new_issues`: Whether to notify about new issues ("yes"/"no")
- `notify_frequency`: How often to send digests ("daily"/"weekly"/"never")
- `exclude_languages`: Comma-separated list of languages to exclude
- `focus_languages`: Comma-separated list of languages to prioritize
- `project_size_preference`: Preferred project size ("small"/"medium"/"large")
