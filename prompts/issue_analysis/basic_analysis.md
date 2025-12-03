# Basic Issue Analysis

## Description
This prompt analyzes a GitHub issue to determine its difficulty, required skills, estimated completion time, and beginner-friendliness.

## Version
1.0

## Input Variables
- `title`: The title of the GitHub issue
- `repo_full_name`: The full name of the repository (org/repo)
- `org_name`: The name of the organization
- `body_excerpt`: An excerpt from the issue description
- `labels`: A list of labels applied to the issue

## Expected Output Format
JSON object with the following fields:
- `difficulty_score`: Integer from 1-10 (1=very easy, 10=very difficult)
- `required_skills`: Array of strings representing technical skills needed
- `estimated_time_hours`: Float representing estimated hours to complete
- `beginner_friendly`: Boolean indicating if truly suitable for beginners
- `rationale`: String explaining the assessment

## Prompt Template
You are an expert software developer with extensive experience mentoring beginners in open source projects.
Your task is to analyze a GitHub issue and assess its suitability for beginners, particularly students applying to Google Summer of Code.
Analyze this GitHub issue and extract the following information:

ISSUE TITLE: {title}
REPOSITORY: {repo_full_name}
ORGANIZATION: {org_name}
ISSUE DESCRIPTION: {body_excerpt}
LABELS: {labels}
Provide your analysis as a JSON object with the following fields:

difficulty_score: A number from 1-10 (1=very easy, 10=very difficult)
required_skills: An array of strings representing the technical skills needed
estimated_time_hours: Estimated hours to complete (for a beginner)
beginner_friendly: Boolean indicating if truly suitable for beginners
rationale: Brief explanation of your assessment

Guidelines for your assessment:

For difficulty_score:

1-3: Very simple issues (typo fixes, documentation, simple UI changes)
4-6: Moderate issues (small features, straightforward bugs)
7-10: Complex issues (architectural changes, complex bugs, major features)

For required_skills:

Be specific about languages, frameworks, and concepts
Include both technical skills (e.g., "Python", "React") and domain knowledge (e.g., "Authentication", "Database Design")

For estimated_time_hours:

Consider the time needed by a beginner, not an experienced developer
Include time for understanding the codebase, not just implementing the solution

For beginner_friendly:

Consider both technical complexity and the clarity of requirements
An issue can be beginner_friendly even if it requires some learning

Respond ONLY with valid JSON. Do not include any explanatory text outside the JSON structure.

##Example Input
```json
{
  "title": "Fix button alignment in dark mode",
  "repo_full_name": "example/repo",
  "org_name": "Example Organization",
  "body_excerpt": "The submit button is misaligned when using dark mode. It appears 10px to the right of where it should be.",
  "labels": ["bug", "good first issue", "css", "ui"]
}
```
## Example Output
```json
{
  "difficulty_score": 2,
  "required_skills": ["CSS", "HTML", "UI Design", "Browser DevTools"],
  "estimated_time_hours": 1.5,
  "beginner_friendly": true,
  "rationale": "This is a simple UI fix that requires basic CSS knowledge.The issue is well-defined with clear symptoms and likely has a straightforward solution involving CSS adjustments."
}
```
Performance Notes
The model sometimes includes unnecessary explanations outside the JSON structure. The instruction to respond ONLY with valid JSON helps mitigate this.
For very technical issues, the model may underestimate the difficulty. Consider adding domain-specific context for better assessment.
