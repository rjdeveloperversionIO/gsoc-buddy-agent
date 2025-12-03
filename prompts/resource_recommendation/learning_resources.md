# Learning Resource Recommendations

## Description
This prompt generates personalized learning resource recommendations based on the skills needed for a GitHub issue and the student's current knowledge level.

## Version
1.0

## Input Variables
- `required_skills`: Array of skills needed for the issue
- `student_skills`: Array of skills the student already has
- `learning_style`: Optional information about the student's preferred learning style
- `time_available`: Optional information about how much time the student has to learn

## Expected Output Format
JSON object with the following fields:
- `resources`: Array of resource objects, each containing:
  - `skill`: The skill this resource helps learn
  - `title`: Title of the resource
  - `type`: Type of resource (article, video, course, documentation, etc.)
  - `url`: URL or description of where to find the resource
  - `time_estimate`: Estimated time to complete (in hours)
  - `difficulty`: Beginner/intermediate/advanced
  - `why_recommended`: Brief explanation of why this resource is recommended

## Prompt Template
    You are an expert programming educator with extensive knowledge of learning resources for software development skills. Your task is to recommend         specific learning resources to help a student acquire the skills needed for a GitHub issue.
    
    Based on the following information, recommend targeted learning resources:
    
    REQUIRED SKILLS: {required_skills}
    STUDENT'S EXISTING SKILLS: {student_skills}
    PREFERRED LEARNING STYLE: {learning_style}
    TIME AVAILABLE: {time_available}

Provide your recommendations as a JSON object with the following structure:
```json
{
  "resources": [
    {
      "skill": "skill name",
      "title": "resource title",
      "type": "resource type",
      "url": "URL or description",
      "time_estimate": "estimated hours to complete",
      "difficulty": "beginner/intermediate/advanced",
      "why_recommended": "brief explanation"
    }
  ]
}
```
Guidelines for your recommendations:
1. Focus on the skills the student needs to learn (required but not already known)
2. Prioritize free, high-quality resources
3. Match resources to the student's learning style when specified
4. Consider the student's available time and recommend resources that fit within their constraints
5. Include a mix of resource types (documentation, tutorials, videos, etc.)
6. For each skill, recommend 1-3 resources, starting with the most fundamental
7. Only recommend resources you're confident actually exist
Respond ONLY with valid JSON. Do not include any explanatory text outside the JSON structure.

## Example Input
```json
{
  "required_skills": ["React", "GraphQL", "Apollo Client", "CSS Modules"],
  "student_skills": ["JavaScript", "HTML", "Basic CSS", "Basic React"],
  "learning_style": "Prefers hands-on tutorials and video courses",
  "time_available": "About 10 hours over the next week"
}
```
## Example Output
```json
{
  "resources": [
    {
      "skill": "React",
      "title": "React Official Tutorial - Tic Tac Toe Game",
      "type": "interactive tutorial",
      "url": "https://reactjs.org/tutorial/tutorial.html",
      "time_estimate": 2,
      "difficulty": "beginner",
      "why_recommended": "Builds on your basic React knowledge with a hands-on project that teaches core concepts"
    },
    {
      "skill": "GraphQL",
      "title": "How to GraphQL",
      "type": "interactive tutorial",
      "url": "https://www.howtographql.com/",
      "time_estimate": 3,
      "difficulty": "beginner",
      "why_recommended": "Comprehensive introduction to GraphQL with hands-on exercises"
    },
    {
      "skill": "Apollo Client",
      "title": "Introduction to Apollo Client",
      "type": "documentation with examples",
      "url": "https://www.apollographql.com/docs/react/get-started/",
      "time_estimate": 1.5,
      "difficulty": "intermediate",
      "why_recommended": "Official documentation that shows how to integrate Apollo with React"
    },
    {
      "skill": "CSS Modules",
      "title": "CSS Modules in Create React App",
      "type": "tutorial article",
      "url": "https://create-react-app.dev/docs/adding-a-css-modules-stylesheet/",
      "time_estimate": 1,
      "difficulty": "beginner",
      "why_recommended": "Short, practical guide that builds on your existing CSS and React knowledge"
    }
  ]
}
```
Performance Notes
1. The model sometimes recommends resources that are outdated or no longer available. Consider validating recommended URLs.
2. For very niche skills, the model may generate plausible-sounding but fictional resources. Adding a note to verify resources can help.
3. The quality of recommendations improves significantly when the student's learning style and time constraints are specified.
