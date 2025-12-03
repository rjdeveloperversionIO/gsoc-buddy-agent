# Detailed Skills Extraction

## Description
This prompt extracts a comprehensive list of technical skills required to solve a GitHub issue, with proficiency levels.

## Version
1.0

## Input Variables
- `title`: The title of the GitHub issue
- `repo_full_name`: The full name of the repository (org/repo)
- `body_excerpt`: An excerpt from the issue description
- `labels`: A list of labels applied to the issue

## Expected Output Format
JSON object with the following fields:
- `primary_language`: String representing the main programming language needed
- `frameworks`: Array of strings representing frameworks or libraries needed
- `concepts`: Array of strings representing technical concepts needed
- `tools`: Array of strings representing tools or systems needed
- `skill_levels`: Object mapping skills to required proficiency levels (beginner/intermediate/advanced)
## Prompt Template
    You are an expert in open source development with deep knowledge of programming languages, frameworks, and technical concepts.
    Your task is to extract the specific technical skills required to solve a GitHub issue.
    
    Analyze this GitHub issue and identify all required technical skills:
    
    ISSUE TITLE: {title}
    REPOSITORY: {repo_full_name}
    ISSUE DESCRIPTION: {body_excerpt}
    LABELS: {labels}
    
    Provide your analysis as a JSON object with the following fields:
    
    primary_language: The main programming language needed (single string)
    frameworks: Array of frameworks or libraries needed
    concepts: Array of technical concepts needed
    tools: Array of development tools or systems needed
    skill_levels: Object mapping skills to required proficiency levels (beginner/intermediate/advanced)
    
    Guidelines for your assessment:
    
    1. For primary_language:
        Identify the main programming language needed based on the repository and issue
        If multiple languages are needed, choose the most important one
    
    2. For frameworks:
        Include specific libraries, frameworks, and packages
        Be as specific as possible (e.g., "React" rather than just "JavaScript framework")
    
    3. For concepts:  
        Include programming paradigms, patterns, and domain knowledge
        Examples: "Authentication", "State Management", "Database Indexing"
    
    4. For tools:
        Include development tools, build systems, and infrastructure
        Examples: "Git", "Docker", "CI/CD", "Browser DevTools"
    
    5. For skill_levels:
        Assess each skill as "beginner", "intermediate", or "advanced"
        Example: {"React": "intermediate", "CSS": "beginner"}
    
    Respond ONLY with valid JSON. Do not include any explanatory text outside the JSON structure.
##Example Input
```json
{
  "title": "Implement OAuth authentication with Google",
  "repo_full_name": "example/web-app",
  "body_excerpt": "We need to add Google OAuth authentication to our login system. This should use the existing authentication framework but add a new provider.",
  "labels": ["enhancement", "authentication", "frontend"]
}
```
##Example Output
```json
{
  "primary_language": "JavaScript",
  "frameworks": ["OAuth 2.0", "Google API Client", "Express.js"],
  "concepts": ["Authentication", "API Integration", "Session Management", "Security"],
  "tools": ["Git", "Browser DevTools", "Postman"],
  "skill_levels": {
    "JavaScript": "intermediate",
    "OAuth 2.0": "intermediate",
    "Google API Client": "beginner",
    "Express.js": "intermediate",
    "Authentication": "intermediate",
    "API Integration": "intermediate",
    "Session Management": "intermediate",
    "Security": "intermediate",
    "Git": "beginner",
    "Browser DevTools": "beginner",
    "Postman": "beginner"
}
```
Performance Notes
The model may sometimes infer frameworks that aren't explicitly mentioned in the issue. This is generally helpful but can occasionally lead to incorrect assumptions.
For repositories with multiple languages, the model might need more context about the codebase to accurately determine the primary language.
