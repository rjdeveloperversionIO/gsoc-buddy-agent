"""
Test Script for Matching Algorithm
Tests the functionality of the MatchingAlgorithm class
"""

import sys
import json
from matching_algorithm import MatchingAlgorithm

def test_matching_algorithm():
    """Run tests for the matching algorithm"""
    print("Starting matching algorithm tests...")
    
    # Create the matching algorithm with default weights
    matcher = MatchingAlgorithm()
    
    # Test 1: Basic matching with ideal fit
    print("\nTest 1: Basic matching with ideal fit")
    student1 = {
        'student_id': 'student1',
        'github_username': 'student1',
        'display_name': 'Student One',
        'available_hours_weekly': 20,
        'skills': [
            {'skill_name': 'Python', 'skill_type': 'language', 'proficiency': 'advanced'},
            {'skill_name': 'Django', 'skill_type': 'framework', 'proficiency': 'intermediate'},
            {'skill_name': 'JavaScript', 'skill_type': 'language', 'proficiency': 'intermediate'}
        ],
        'target_orgs': [
            {'org_name': 'Zulip', 'priority': 1},
            {'org_name': 'Mozilla', 'priority': 2}
        ],
        'gsoc_goals': 'I want to improve my Python and web development skills.'
    }
    
    issue1 = {
        'issue_id': 'issue1',
        'repo_full_name': 'zulip/zulip',
        'org_name': 'Zulip',
        'title': 'Implement new API endpoint',
        'primary_language': 'Python',
        'required_skills': ['Python', 'Django', 'API'],
        'difficulty_score': 5,
        'estimated_time_hours': 8,
        'labels': ['enhancement', 'backend', 'good first issue'],
        'comments_count': 1
    }
    
    match_result1 = matcher.calculate_match_score(student1, issue1)
    print_match_result(match_result1)
    
    # Test 2: Skill mismatch
    print("\nTest 2: Skill mismatch")
    issue2 = {
        'issue_id': 'issue2',
        'repo_full_name': 'mozilla/firefox',
        'org_name': 'Mozilla',
        'title': 'Fix CSS rendering bug',
        'primary_language': 'C++',
        'required_skills': ['C++', 'CSS', 'Browser Internals'],
        'difficulty_score': 7,
        'estimated_time_hours': 15,
        'labels': ['bug', 'frontend', 'rendering'],
        'comments_count': 5
    }
    
    match_result2 = matcher.calculate_match_score(student1, issue2)
    print_match_result(match_result2)
    
    # Test 3: Difficulty mismatch
    print("\nTest 3: Difficulty mismatch")
    issue3 = {
        'issue_id': 'issue3',
        'repo_full_name': 'zulip/zulip',
        'org_name': 'Zulip',
        'title': 'Refactor authentication system',
        'primary_language': 'Python',
        'required_skills': ['Python', 'Django', 'Authentication', 'Security'],
        'difficulty_score': 9,
        'estimated_time_hours': 40,
        'labels': ['enhancement', 'security', 'authentication'],
        'comments_count': 8
    }
    
    match_result3 = matcher.calculate_match_score(student1, issue3)
    print_match_result(match_result3)
    
    # Test 4: Perfect beginner match
    print("\nTest 4: Perfect beginner match")
    student2 = {
        'student_id': 'student2',
        'github_username': 'student2',
        'display_name': 'Student Two',
        'available_hours_weekly': 10,
        'skills': [
            {'skill_name': 'JavaScript', 'skill_type': 'language', 'proficiency': 'beginner'},
            {'skill_name': 'HTML', 'skill_type': 'language', 'proficiency': 'intermediate'},
            {'skill_name': 'CSS', 'skill_type': 'language', 'proficiency': 'intermediate'}
        ],
        'target_orgs': [
            {'org_name': 'Mozilla', 'priority': 1}
        ],
        'gsoc_goals': 'I want to learn web development and contribute to open source.'
    }
    
    issue4 = {
        'issue_id': 'issue4',
        'repo_full_name': 'mozilla/firefox',
        'org_name': 'Mozilla',
        'title': 'Fix button styling in dark mode',
        'primary_language': 'CSS',
        'required_skills': ['CSS', 'HTML', 'JavaScript'],
        'difficulty_score': 2,
        'estimated_time_hours': 3,
        'labels': ['good first issue', 'frontend', 'ui', 'css'],
        'comments_count': 0
    }
    
    match_result4 = matcher.calculate_match_score(student2, issue4)
    print_match_result(match_result4)
    
    # Test 5: Finding best matches
    print("\nTest 5: Finding best matches for a student")
    issues = [issue1, issue2, issue3, issue4]
    
    matches = matcher.find_matches(student1, issues, limit=4)
    print(f"Found {len(matches)} matches for student1, sorted by score:")
    for i, match in enumerate(matches, 1):
        print(f"{i}. {match['issue_id']} - Score: {match['match_score']} - {match['match_category']}")
    
    # Test 6: Adjusting weights for GSoC phase
    print("\nTest 6: Adjusting weights for GSoC phase")
    
    # Test with early phase
    matcher.adjust_weights_for_gsoc_phase('early')
    early_result = matcher.calculate_match_score(student1, issue1)
    
    # Test with late phase
    matcher.adjust_weights_for_gsoc_phase('late')
    late_result = matcher.calculate_match_score(student1, issue1)
    
    print(f"Early phase score: {early_result['match_score']}")
    print(f"Late phase score: {late_result['match_score']}")
    
    # Test 7: Adjusting weights for student goals
    print("\nTest 7: Adjusting weights for student goals")
    
    # Test with skill development goal
    matcher.adjust_weights_for_student_goals('skill_development')
    skill_result = matcher.calculate_match_score(student1, issue1)
    
    # Test with selection goal
    matcher.adjust_weights_for_student_goals('selection')
    selection_result = matcher.calculate_match_score(student1, issue1)
    
    print(f"Skill development goal score: {skill_result['match_score']}")
    print(f"Selection goal score: {selection_result['match_score']}")
    
    print("\nAll matching algorithm tests completed!")

def print_match_result(result):
    """Print a match result in a readable format"""
    print(f"Match Score: {result['match_score']}")
    print(f"Match Category: {result['match_category']}")
    print("Component Scores:")
    for component, score in result['component_scores'].items():
        print(f"  {component}: {score}")
    
    # Print a shortened version of the explanation
    explanation_lines = result['explanation'].split('\n')
    print(f"Explanation: {explanation_lines[0]} ...")

if __name__ == "__main__":
    test_matching_algorithm()
