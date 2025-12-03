# Issue Resolution Guide

## Description
This prompt generates a comprehensive step-by-step guide for resolving a GitHub issue, tailored to the student's skill level.

## Version
1.0

## Input Variables
- `title`: The title of the GitHub issue
- `repo_full_name`: The full name of the repository (org/repo)
- `org_name`: The name of the organization
- `body_excerpt`: An excerpt from the issue description
- `labels`: A list of labels applied to the issue
- `required_skills`: Array of skills needed (from previous analysis)
- `difficulty_score`: Difficulty score from 1-10 (from previous analysis)
- `student_experience`: Optional information about the student's experience level

## Expected Output Format
Markdown-formatted guide with sections for setup, understanding the issue, step-by-step approach, testing, and creating a pull request.

## Prompt Template
    You are an experienced open source mentor helping a student contribute to a GitHub project. Your task is to create a detailed, step-by-step guide        for solving a specific issue.
    
    Create a comprehensive guide for resolving this GitHub issue:
    ISSUE TITLE: {title}
    REPOSITORY: {repo_full_name}
    ORGANIZATION: {org_name}
    ISSUE DESCRIPTION: {body_excerpt}
    LABELS: {labels}
    REQUIRED SKILLS: {required_skills}
    DIFFICULTY: {difficulty_score}/10
    STUDENT EXPERIENCE: {student_experience}

Your guide should be structured with the following sections:

1. Understanding the Issue
    Explain what the issue is about in simple terms
    Identify which parts of the codebase are likely involved
    Clarify any technical concepts the student might need to understand

2. Environment Setup
    Instructions for forking and cloning the repository
    Steps to set up the development environment
    How to run the project locally
    Any specific configuration needed for this issue

3. Step-by-Step Approach
    Break down the solution into clear, manageable steps
    Provide guidance on where to look in the codebase
    Suggest specific files or components that need modification
    Include code patterns or examples where helpful (but not complete solutions)

4. Testing Your Solution
    How to verify the issue is fixed
    Specific test cases to check
    How to run relevant tests

5. Creating a Pull Request
    Guidelines for commit messages
    What to include in the PR description
    How to reference the issue
    What to expect in the review process

Format your response as a helpful markdown guide with clear headings, bullet points, and code examples where appropriate. Be encouraging and supportive in your tone.


## Example Input
```json
{
  "title": "Fix button alignment in dark mode",
  "repo_full_name": "example/repo",
  "org_name": "Example Organization",
  "body_excerpt": "The submit button is misaligned when using dark mode. It appears 10px to the right of where it should be.",
  "labels": ["bug", "good first issue", "css", "ui"],
  "required_skills": ["CSS", "HTML", "UI Design", "Browser DevTools"],
  "difficulty_score": 2,
  "student_experience": "Beginner with basic HTML/CSS knowledge"
}
```
## Example Output
# Resolution Guide: Fix Button Alignment in Dark Mode

## Understanding the Issue

This issue involves a UI alignment problem that only appears in dark mode. The submit button is positioned incorrectly (10px to the right of where it should be) when the application is in dark mode. This suggests there might be some CSS rules specific to the dark mode theme that are affecting the button's positioning.

Key points to understand:
- The issue only occurs in dark mode, not in light mode
- The misalignment is specifically 10px to the right
- This is likely a CSS issue related to theme-specific styling

## Environment Setup

1. Fork and Clone the Repository
   ```bash
   git clone https://github.com/YOUR-USERNAME/repo.git
   cd repo
   ```
2. Install Dependencies
   ```bash
   npm install  # or yarn install, depending on the project
   ```
3. Run the Project Locally
  ```bash
  npm start  # or the appropriate command for this project
  ```
4. Switch to Dark Mode
    Open the application in your browser
    Find the theme toggle to switch to dark mode
    Navigate to the page with the submit button to observe the issue

Step-by-Step Approach
1. Locate the Submit Button in the Code
    Look for button components in the codebase
    Search for terms like "submit button", "form submit", etc.
    Check component directories for form-related components

2. Identify the Dark Mode CSS
    Look for theme-related CSS files
    Search for dark mode class definitions
    Common patterns include:
   ```CSS
   .dark-mode .button { ... }
   [data-theme="dark"] .button { ... }
   ```
3. Inspect the Button in Browser DevTools
    Right-click the button and select "Inspect"
    In the Styles panel, look for CSS rules affecting positioning
    Compare the computed styles between light and dark modes
    Look specifically for properties like margin, padding, or position

4. Fix the CSS Issue
    Once you've identified the problematic CSS rule, adjust it to fix the alignment
    The solution will likely involve removing or adjusting a margin/padding property
    Example fix:
    ```CSS
    /* If you find something like this: */
    .dark-mode .submit-button {
      margin-left: 10px; /* This might be the culprit */
    }
    
    /* Change it to: */
    .dark-mode .submit-button {
      margin-left: 0; /* Remove the extra margin */
    }
    ```
Testing Your Solution
1. Visual Verification
    Toggle between light and dark modes to ensure the button is aligned correctly in both themes
    Check at different screen sizes to ensure the fix works responsively
    Verify that fixing this alignment hasn't broken anything else

2. Run UI Tests (if available)
   ```bash
   npm run test:ui
   ```
3. Cross-Browser Testing
    Check the fix in at least Chrome and Firefox
    If possible, also verify in Safari and Edge

Creating a Pull Request
1. Commit Your Changes
   ```bash
   git add [files you modified]
   git commit -m "Fix: Correct button alignment in dark mode"
   ```
2. Push and Create PR
   ```bash
   git push origin main
   ```
 - Go to GitHub and create a new pull request

3. PR Description Template
   ## Description
    Fixed the submit button alignment issue in dark mode by removing the extra margin-left that was causing the 10px shift.
    
    ## How to Test
    1. Run the application locally
    2. Switch to dark mode
    3. Navigate to [page with the button]
    4. Verify the button is properly aligned
    
    Fixes #[issue number]

4. What to Expect

    A maintainer will review your PR
    They might suggest changes or improvements
    Be responsive to feedback and make requested changes promptly
    Once approved, your fix will be merged!

Good luck with your contribution! This is a great first issue to get familiar with the codebase and CSS structure of the project.


## Performance Notes
- The model generates high-quality guides but may sometimes include generic advice if the issue description is vague.
- Adding more specific details about the repository structure and codebase can improve the relevance of the guide.
- For complex issues, the model might oversimplify some steps. Consider breaking very complex issues into multiple prompts.
- The quality of the guide improves significantly when student_experience is provided.
- Code examples are generally accurate for common patterns but may need verification for project-specific conventions.
