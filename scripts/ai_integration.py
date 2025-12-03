"""
AI Integration Module for GSoC Buddy
Provides functions to interact with Gemini and Groq APIs with fallback mechanisms
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional, List, Union

# API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Models
GEMINI_MODEL = "gemini-2.0-flash"
GROQ_MODEL = "llama-3.1-8b-instant"  # Using LLaMA 3 8B model
GROQ_BACKUP_MODEL = "mixtral-8x7b-32768"  # Backup model if LLaMA has issues

# Maximum retries
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

class AIError(Exception):
    """Custom exception for AI-related errors"""
    pass

def call_gemini_api(prompt: str, temperature: float = 0.2) -> Dict[Any, Any]:
    """
    Call the Gemini API with the given prompt
    
    Args:
        prompt: The text prompt to send to the API
        temperature: Controls randomness (0.0 to 1.0)
        
    Returns:
        The JSON response from the API
        
    Raises:
        AIError: If the API call fails
    """
    if not GEMINI_API_KEY:
        raise AIError("Gemini API key not found in environment variables")
    
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "topP": 0.8,
            "topK": 40
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                raise AIError(f"Gemini API call failed after {MAX_RETRIES} attempts: {str(e)}")
            time.sleep(RETRY_DELAY)
    
    # This should never be reached due to the exception in the loop
    raise AIError("Unexpected error in Gemini API call")

def call_groq_api(prompt: str, temperature: float = 0.2, model: str = GROQ_MODEL) -> Dict[Any, Any]:
    """
    Call the Groq API with the given prompt
    
    Args:
        prompt: The text prompt to send to the API
        temperature: Controls randomness (0.0 to 1.0)
        model: The model to use
        
    Returns:
        The JSON response from the API
        
    Raises:
        AIError: If the API call fails
    """
    if not GROQ_API_KEY:
        raise AIError("Groq API key not found in environment variables")
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 4000
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                # If we're using the primary model and failed, try the backup model
                if model == GROQ_MODEL and GROQ_BACKUP_MODEL:
                    print(f"Primary Groq model failed, trying backup model {GROQ_BACKUP_MODEL}")
                    return call_groq_api(prompt, temperature, GROQ_BACKUP_MODEL)
                raise AIError(f"Groq API call failed after {MAX_RETRIES} attempts: {str(e)}")
            time.sleep(RETRY_DELAY)
    
    # This should never be reached due to the exception in the loop
    raise AIError("Unexpected error in Groq API call")

def extract_text_from_gemini(response: Dict[Any, Any]) -> str:
    """
    Extract the text content from a Gemini API response
    
    Args:
        response: The JSON response from the Gemini API
        
    Returns:
        The extracted text
        
    Raises:
        AIError: If the text cannot be extracted
    """
    try:
        return response['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError) as e:
        raise AIError(f"Failed to extract text from Gemini response: {str(e)}")

def extract_text_from_groq(response: Dict[Any, Any]) -> str:
    """
    Extract the text content from a Groq API response
    
    Args:
        response: The JSON response from the Groq API
        
    Returns:
        The extracted text
        
    Raises:
        AIError: If the text cannot be extracted
    """
    try:
        return response['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        raise AIError(f"Failed to extract text from Groq response: {str(e)}")

def get_ai_response(prompt: str, temperature: float = 0.2) -> str:
    """
    Get a response from an AI model, with fallback mechanisms
    
    Args:
        prompt: The text prompt to send to the API
        temperature: Controls randomness (0.0 to 1.0)
        
    Returns:
        The text response from the AI
        
    Raises:
        AIError: If all API calls fail
    """
    # Try Gemini first
    if GEMINI_API_KEY:
        try:
            gemini_response = call_gemini_api(prompt, temperature)
            return extract_text_from_gemini(gemini_response)
        except AIError as e:
            print(f"Gemini API error: {str(e)}")
            # Fall through to Groq
    
    # Try Groq as fallback
    if GROQ_API_KEY:
        try:
            groq_response = call_groq_api(prompt, temperature)
            return extract_text_from_groq(groq_response)
        except AIError as e:
            print(f"Groq API error: {str(e)}")
            # No more fallbacks, raise error
            raise AIError("All AI providers failed to respond")
    
    # If we get here, no API keys were available
    raise AIError("No AI API keys available")

def get_json_response(prompt: str, temperature: float = 0.2) -> Dict[Any, Any]:
    """
    Get a JSON response from an AI model
    
    Args:
        prompt: The text prompt to send to the API
        temperature: Controls randomness (0.0 to 1.0)
        
    Returns:
        The parsed JSON response
        
    Raises:
        AIError: If the response cannot be parsed as JSON
    """
    # Add explicit instructions for JSON format
    json_prompt = f"{prompt}\n\nRespond ONLY with valid JSON. Do not include any explanatory text outside the JSON structure."
    
    # Get the response
    response_text = get_ai_response(json_prompt, temperature)
    
    # Extract JSON from the response (in case there's any text before or after)
    json_match = extract_json_from_text(response_text)
    
    if not json_match:
        # Try again with a more explicit prompt
        retry_prompt = f"{prompt}\n\nYou MUST respond with ONLY a valid JSON object. No markdown formatting, no explanations, just the JSON object."
        response_text = get_ai_response(retry_prompt, temperature)
        json_match = extract_json_from_text(response_text)
        
        if not json_match:
            raise AIError(f"Failed to extract JSON from AI response: {response_text[:100]}...")
    
    # Parse the JSON
    try:
        return json.loads(json_match)
    except json.JSONDecodeError as e:
        raise AIError(f"Failed to parse JSON from AI response: {str(e)}")

def extract_json_from_text(text: str) -> Optional[str]:
    """
    Extract JSON from text that might contain other content
    
    Args:
        text: The text that might contain JSON
        
    Returns:
        The extracted JSON string, or None if no JSON is found
    """
    # Try to find JSON between triple backticks (markdown code blocks)
    import re
    json_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_block_match:
        return json_block_match.group(1)
    
    # Try to find JSON between curly braces
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        return json_match.group(1)
    
    # If the entire text looks like JSON, return it
    if text.strip().startswith('{') and text.strip().endswith('}'):
        return text.strip()
    
    return None

def analyze_issue(issue_data: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Analyze a GitHub issue to extract key information
    
    Args:
        issue_data: Dictionary containing issue information
        
    Returns:
        Dictionary with analysis results
    """
    # Construct the prompt
    prompt = f"""
    Analyze this GitHub issue and extract the following information:
    
    ISSUE TITLE: {issue_data.get('title', 'No title provided')}
    REPOSITORY: {issue_data.get('repo_full_name', 'No repository provided')}
    ORGANIZATION: {issue_data.get('org_name', 'No organization provided')}
    ISSUE DESCRIPTION: {issue_data.get('body_excerpt', 'No description provided')}
    LABELS: {', '.join(issue_data.get('labels', []))}
    
    Provide your analysis as a JSON object with the following fields:
    - difficulty_score: A number from 1-10 (1=very easy, 10=very difficult)
    - required_skills: An array of strings representing the technical skills needed
    - estimated_time_hours: Estimated hours to complete (for a beginner)
    - beginner_friendly: Boolean indicating if truly suitable for beginners
    - rationale: Brief explanation of your assessment
    
    Example response format:
    {{
      "difficulty_score": 3,
      "required_skills": ["JavaScript", "React", "CSS"],
      "estimated_time_hours": 4,
      "beginner_friendly": true,
      "rationale": "This is a simple UI fix that requires basic React knowledge."
    }}
    """
    
    # Get the analysis
    try:
        return get_json_response(prompt, temperature=0.1)
    except AIError as e:
        print(f"Error analyzing issue: {str(e)}")
        # Return a default analysis if AI fails
        return {
            "difficulty_score": 5,
            "required_skills": ["Unknown"],
            "estimated_time_hours": 8,
            "beginner_friendly": issue_data.get('labels', []) and any('beginner' in label.lower() for label in issue_data.get('labels', [])),
            "rationale": "Analysis failed, default values provided based on labels."
        }

def generate_resolution_guide(issue_data: Dict[Any, Any], analysis: Dict[Any, Any]) -> str:
    """
    Generate a guide for resolving a GitHub issue
    
    Args:
        issue_data: Dictionary containing issue information
        analysis: Dictionary containing issue analysis
        
    Returns:
        A markdown-formatted guide
    """
    # Construct the prompt
    prompt = f"""
    Create a step-by-step guide for a student to solve this GitHub issue:
    
    ISSUE TITLE: {issue_data.get('title', 'No title provided')}
    REPOSITORY: {issue_data.get('repo_full_name', 'No repository provided')}
    ORGANIZATION: {issue_data.get('org_name', 'No organization provided')}
    ISSUE DESCRIPTION: {issue_data.get('body_excerpt', 'No description provided')}
    LABELS: {', '.join(issue_data.get('labels', []))}
    
    REQUIRED SKILLS: {', '.join(analysis.get('required_skills', ['Unknown']))}
    DIFFICULTY: {analysis.get('difficulty_score', 5)}/10
    
    Your guide should include:
    1. Initial setup and environment preparation
    2. Understanding the issue and its context
    3. Step-by-step approach to solving it
    4. Testing the solution
    5. Creating a good pull request
    
    Format your response as a helpful markdown guide with sections and code examples where appropriate.
    """
    
    # Get the guide
    try:
        return get_ai_response(prompt, temperature=0.3)
    except AIError as e:
        print(f"Error generating resolution guide: {str(e)}")
        # Return a simple guide if AI fails
        return f"""
        # Resolution Guide for Issue: {issue_data.get('title', 'Unknown Issue')}
        
        ## Setup
        1. Fork the repository
        2. Clone your fork
        3. Set up the development environment according to the repository's README
        
        ## Understanding the Issue
        Review the issue description carefully and look at related code.
        
        ## Approach
        1. Identify the files that need to be modified
        2. Make the necessary changes
        3. Test your solution
        
        ## Creating a Pull Request
        1. Commit your changes with a descriptive message
        2. Push to your fork
        3. Create a pull request with a clear description referencing the issue
        
        *Note: This is a generic guide. The AI service was unable to generate a specific guide for this issue.*
        """

# Test function to verify the module works
def test_ai_integration():
    """Test the AI integration module"""
    try:
        # Test basic response
        response = get_ai_response("What is Google Summer of Code?", temperature=0.2)
        print("Basic response test:", "PASSED" if len(response) > 100 else "FAILED")
        
        # Test JSON response
        json_response = get_json_response(
            "List 3 programming languages as a JSON array with fields 'name' and 'difficulty'.",
            temperature=0.2
        )
        print("JSON response test:", "PASSED" if isinstance(json_response, dict) else "FAILED")
        
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Run test if executed directly
    test_ai_integration()
