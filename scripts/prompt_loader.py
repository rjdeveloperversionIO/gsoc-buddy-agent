"""
Prompt Loader Module for GSoC Buddy
Provides functions to load and use prompt templates
"""

import os
import re
from typing import Dict, Any, Optional, List

def load_prompt_template(template_path: str) -> Optional[str]:
    """
    Load a prompt template from a file
    
    Args:
        template_path: Path to the template file
        
    Returns:
        The prompt template string, or None if the file couldn't be loaded
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract the prompt template section
        prompt_match = re.search(r'## Prompt Template\s+```\s+(.*?)\s+```', content, re.DOTALL)
        if prompt_match:
            return prompt_match.group(1).strip()
        else:
            print(f"Error: Could not find prompt template section in {template_path}")
            return None
    except Exception as e:
        print(f"Error loading prompt template from {template_path}: {str(e)}")
        return None

def fill_prompt_template(template: str, variables: Dict[str, Any]) -> str:
    """
    Fill a prompt template with variables
    
    Args:
        template: The prompt template string
        variables: Dictionary of variable names and values
        
    Returns:
        The filled prompt string
    """
    filled_prompt = template
    
    # Replace each variable in the template
    for var_name, var_value in variables.items():
        placeholder = f"{{{var_name}}}"
        
        # Handle different types of values
        if isinstance(var_value, list):
            # Join lists with commas
            value_str = ", ".join(str(item) for item in var_value)
        else:
            # Convert other types to string
            value_str = str(var_value)
        
        filled_prompt = filled_prompt.replace(placeholder, value_str)
    
    return filled_prompt

def get_prompt(prompt_type: str, prompt_name: str, variables: Dict[str, Any]) -> Optional[str]:
    """
    Get a filled prompt by type and name
    
    Args:
        prompt_type: The type of prompt (e.g., 'issue_analysis', 'skill_extraction')
        prompt_name: The name of the prompt file without extension
        variables: Dictionary of variable names and values
        
    Returns:
        The filled prompt string, or None if the prompt couldn't be loaded
    """
    # Construct the path to the prompt template
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'prompts', prompt_type, f"{prompt_name}.md")
    
    # Load the template
    template = load_prompt_template(template_path)
    if not template:
        return None
    
    # Fill the template with variables
    return fill_prompt_template(template, variables)

def list_available_prompts() -> Dict[str, List[str]]:
    """
    List all available prompt templates
    
    Returns:
        Dictionary mapping prompt types to lists of available prompt names
    """
    prompts = {}
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_dir = os.path.join(base_dir, 'prompts')
    
    # Check if the prompts directory exists
    if not os.path.isdir(prompts_dir):
        print(f"Error: Prompts directory not found at {prompts_dir}")
        return prompts
    
    # Iterate through prompt type directories
    for prompt_type in os.listdir(prompts_dir):
        type_dir = os.path.join(prompts_dir, prompt_type)
        
        # Skip if not a directory
        if not os.path.isdir(type_dir):
            continue
        
        # Get all markdown files in the directory
        prompt_files = [f[:-3] for f in os.listdir(type_dir) if f.endswith('.md')]
        prompts[prompt_type] = prompt_files
    
    return prompts

# Test function to verify the module works
def test_prompt_loader():
    """Test the prompt loader module"""
    # List available prompts
    available_prompts = list_available_prompts()
    print("Available prompts:")
    for prompt_type, prompt_names in available_prompts.items():
        print(f"  {prompt_type}: {', '.join(prompt_names)}")
    
    # Test loading a prompt
    if 'issue_analysis' in available_prompts and 'basic_analysis' in available_prompts.get('issue_analysis', []):
        test_variables = {
            'title': 'Test Issue',
            'repo_full_name': 'test/repo',
            'org_name': 'Test Org',
            'body_excerpt': 'This is a test issue description',
            'labels': ['bug', 'test']
        }
        
        prompt = get_prompt('issue_analysis', 'basic_analysis', test_variables)
        if prompt:
            print("\nSuccessfully loaded and filled prompt template:")
            print(f"{prompt[:200]}...\n[Prompt truncated for brevity]")
            return True
        else:
            print("Failed to load prompt template")
            return False
    else:
        print("Test prompt not found. Make sure you've created the issue_analysis/basic_analysis.md template.")
        return False

if __name__ == "__main__":
    # Run test if executed directly
    test_prompt_loader()
