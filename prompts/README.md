# Prompt Templates for GSoC Buddy

This directory contains the prompt templates used by the GSoC Buddy AI agent to interact with LLM APIs.

## Directory Structure

- `issue_analysis/`: Prompts for analyzing GitHub issues (complexity, difficulty, etc.)
- `skill_extraction/`: Prompts for extracting required skills from issues
- `guide_generation/`: Prompts for generating resolution guides
- `resource_recommendation/`: Prompts for finding learning resources
- `pr_templates/`: Prompts for generating PR templates

## Prompt Format

Each prompt template is stored as a markdown file with the following structure:
[Prompt Name]
Description
Brief description of what this prompt does

Version
Current version number

Input Variables
variable_name: Description of the variable
Expected Output Format
Description of the expected output format (usually JSON)

Prompt Template
text

[The actual prompt template with {variable} placeholders]
Example Input
JSON

{
  "variable_name": "example value"
}
Example Output
JSON

{
  "field": "value"
}
Performance Notes
Any notes on the performance of this prompt, including common issues

text


## Usage

Prompts are loaded by the AI integration module and used to generate requests to the LLM APIs. To use a prompt:

1. Load the prompt template from the appropriate file
2. Replace the variables in the template with actual values
3. Send the resulting prompt to the AI model
4. Parse the response according to the expected output format

## Versioning

Prompt templates follow semantic versioning:
- MAJOR version changes when the output format changes in a backwards-incompatible way
- MINOR version changes when functionality is added in a backwards-compatible manner
- PATCH version changes when backwards-compatible bug fixes are made

When updating a prompt, create a new file with the updated version number and keep the old version for reference.

## Testing

Before committing a new prompt template, test it with several different inputs to ensure it produces consistent, well-formatted outputs.
