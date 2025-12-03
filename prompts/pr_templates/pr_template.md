# Pull Request Template Generator

## Description
This prompt generates a customized pull request template for a specific GitHub issue, including sections for description, testing instructions, and related information.

## Version
1.0

## Input Variables
- `title`: The title of the GitHub issue
- `repo_full_name`: The full name of the repository (org/repo)
- `issue_number`: The issue number
- `body_excerpt`: An excerpt from the issue description
- `labels`: A list of labels applied to the issue
- `changes_made`: Optional description of the changes made to resolve the issue

## Expected Output Format
Markdown-formatted PR template with sections for description, changes made, testing instructions, and related information.

## Prompt Template
You are an experienced open source contributor who writes excellent pull request descriptions. Your task is to create a professional PR template for a GitHub issue that has been resolved.

Generate a pull request template for this issue:

ISSUE TITLE: {title}
REPOSITORY: {repo_full_name}
ISSUE NUMBER: {issue_number}
ISSUE DESCRIPTION: {body_excerpt}
LABELS: {labels}
CHANGES MADE: {changes_made}

Create a comprehensive PR template with the following sections:
1. Title (a clear, concise title for the PR)
2. Description (summary of what the PR does)
3. Changes Made (technical details of the implementation)
4. How to Test (step-by-step instructions for reviewers)
5. Screenshots (placeholder for before/after screenshots if applicable)
6. Related Issues (reference to the original issue)
7. Checklist (items to verify before merging)

Format your response as a markdown template that can be directly copied into a GitHub PR description. Use appropriate markdown formatting including headers, lists, and code blocks where relevant.


## Example Input
```json
{
  "title": "Fix button alignment in dark mode",
  "repo_full_name": "example/repo",
  "issue_number": 123,
  "body_excerpt": "The submit button is misaligned when using dark mode. It appears 10px to the right of where it should be.",
  "labels": ["bug", "good first issue", "css", "ui"],
  "changes_made": "Removed the extra margin-left in the dark mode CSS class that was causing the misalignment"
}
```
## Example Output
# Fix button alignment in dark mode

## Description
This PR fixes the submit button alignment issue in dark mode by removing the extra margin that was causing it to appear 10px to the right of its intended position.

## Changes Made
- Identified the cause of the misalignment in the dark mode CSS
- Removed the `margin-left: 10px` property from the `.dark-mode .submit-button` class
- Ensured the button alignment is consistent between light and dark modes

## How to Test
1. Checkout this branch
2. Run the application locally (`npm start`)
3. Navigate to the page with the submit button
4. Toggle between light and dark modes
5. Verify that the button is properly aligned in both modes
6. Test on different screen sizes to ensure responsive behavior is maintained

## Screenshots
<!-- Please add before/after screenshots if applicable -->

## Related Issues
Fixes #123

## Checklist

- [x] Code follows the project's coding style
- [x] Changes have been tested in multiple browsers (Chrome, Firefox, Safari)
- [x] Changes are responsive on different screen sizes
- [x] Documentation has been updated (if applicable)
- [x] This PR is ready for review

Performance Notes
The model generates high-quality PR templates but may include generic sections if the issue or changes description is vague.
For complex issues, consider providing more details about the changes made to get more specific technical descriptions.
