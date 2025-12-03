"""
Test Script for Student Profile Management
Tests the functionality of the StudentProfileManager class
"""

import os
import sys
import uuid
import time
from datetime import datetime
from student_profile_manager import StudentProfileManager

def test_student_profiles(sheets_key_path: str, spreadsheet_id: str, 
                         supabase_url: str = None, supabase_key: str = None):
    """
    Run tests for the student profile management functionality
    
    Args:
        sheets_key_path: Path to the Google Sheets service account key file
        spreadsheet_id: ID of the Google Spreadsheet
        supabase_url: Supabase URL (optional)
        supabase_key: Supabase API key (optional)
    """
    print("Starting student profile tests...")
    
    # Initialize the profile manager
    manager = StudentProfileManager(
        sheets_key_path=sheets_key_path,
        spreadsheet_id=spreadsheet_id,
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
    
    # Generate a unique test username to avoid conflicts
    test_username = f"test_user_{uuid.uuid4().hex[:8]}"
    test_display_name = "Test User"
    
    # Test 1: Add a student
    print("\nTest 1: Adding a student...")
    try:
        student_id = manager.add_student(
            github_username=test_username,
            display_name=test_display_name,
            email="test@example.com",
            telegram_id="test123",
            timezone="UTC+0",
            available_hours_weekly=15,
            preferred_contact_method="telegram",
            learning_style="Hands-on learner",
            gsoc_goals="Gain experience in open source",
            bio="Test student profile"
        )
        print(f"✅ Added student with ID: {student_id}")
    except Exception as e:
        print(f"❌ Failed to add student: {str(e)}")
        return
    
    # Test 2: Get student by ID
    print("\nTest 2: Getting student by ID...")
    try:
        student = manager.get_student(student_id)
        if student and student.get('github_username') == test_username:
            print(f"✅ Retrieved student: {student.get('display_name')}")
        else:
            print("❌ Failed to retrieve student by ID")
            return
    except Exception as e:
        print(f"❌ Error retrieving student: {str(e)}")
        return
    
    # Test 3: Get student by GitHub username
    print("\nTest 3: Getting student by GitHub username...")
    try:
        student = manager.get_student_by_github(test_username)
        if student and student.get('student_id') == student_id:
            print(f"✅ Retrieved student by GitHub username")
        else:
            print("❌ Failed to retrieve student by GitHub username")
            return
    except Exception as e:
        print(f"❌ Error retrieving student by GitHub username: {str(e)}")
        return
    
    # Test 4: Update student
    print("\nTest 4: Updating student...")
    try:
        updated_bio = "Updated test student profile"
        success = manager.update_student(student_id, bio=updated_bio)
        if success:
            # Verify update
            student = manager.get_student(student_id)
            if student.get('bio') == updated_bio:
                print("✅ Updated student successfully")
            else:
                print("❌ Update verification failed")
                return
        else:
            print("❌ Failed to update student")
            return
    except Exception as e:
        print(f"❌ Error updating student: {str(e)}")
        return
    
    # Test 5: Add skills
    print("\nTest 5: Adding skills...")
    try:
        skill_id1 = manager.add_skill(
            student_id=student_id,
            skill_name="Python",
            skill_type="language",
            proficiency="intermediate",
            years_experience=2.0,
            is_primary=True
        )
        
        skill_id2 = manager.add_skill(
            student_id=student_id,
            skill_name="React",
            skill_type="framework",
            proficiency="beginner",
            years_experience=0.5,
            is_primary=False
        )
        
        print(f"✅ Added skills with IDs: {skill_id1}, {skill_id2}")
    except Exception as e:
        print(f"❌ Error adding skills: {str(e)}")
        return
    
    # Test 6: Get student skills
    print("\nTest 6: Getting student skills...")
    try:
        skills = manager.get_student_skills(student_id)
        if len(skills) >= 2:
            print(f"✅ Retrieved {len(skills)} skills")
        else:
            print(f"❌ Expected at least 2 skills, got {len(skills)}")
            return
    except Exception as e:
        print(f"❌ Error retrieving skills: {str(e)}")
        return
    
    # Test 7: Add target organizations
    print("\nTest 7: Adding target organizations...")
    try:
        target_id1 = manager.add_target_org(
            student_id=student_id,
            org_name="Zulip",
            priority=1,
            reason="Interested in their tech stack"
        )
        
        target_id2 = manager.add_target_org(
            student_id=student_id,
            org_name="TensorFlow",
            priority=2,
            reason="Want to learn more about machine learning"
        )
        
        print(f"✅ Added target orgs with IDs: {target_id1}, {target_id2}")
    except Exception as e:
        print(f"❌ Error adding target orgs: {str(e)}")
        return
    
    # Test 8: Get student target orgs
    print("\nTest 8: Getting student target orgs...")
    try:
        targets = manager.get_student_target_orgs(student_id)
        if len(targets) >= 2:
            print(f"✅ Retrieved {len(targets)} target orgs")
        else:
            print(f"❌ Expected at least 2 target orgs, got {len(targets)}")
            return
    except Exception as e:
        print(f"❌ Error retrieving target orgs: {str(e)}")
        return
    
    # Test 9: Add contributions
    print("\nTest 9: Adding contributions...")
    try:
        contribution_id = manager.add_contribution(
            student_id=student_id,
            repo_name="zulip/zulip",
            contribution_type="pr",
            url="https://github.com/zulip/zulip/pull/12345",
            description="Fixed a bug in the UI",
            is_gsoc_related=False
        )
        
        print(f"✅ Added contribution with ID: {contribution_id}")
    except Exception as e:
        print(f"❌ Error adding contribution: {str(e)}")
        return
    
    # Test 10: Get student contributions
    print("\nTest 10: Getting student contributions...")
    try:
        contributions = manager.get_student_contributions(student_id)
        if len(contributions) >= 1:
            print(f"✅ Retrieved {len(contributions)} contributions")
        else:
            print(f"❌ Expected at least 1 contribution, got {len(contributions)}")
            return
    except Exception as e:
        print(f"❌ Error retrieving contributions: {str(e)}")
        return
    
    # Test 11: Set preferences
    print("\nTest 11: Setting preferences...")
    try:
        pref_id1 = manager.set_preference(
            student_id=student_id,
            preference_key="difficulty_max",
            preference_value="7"
        )
        
        pref_id2 = manager.set_preference(
            student_id=student_id,
            preference_key="notify_new_issues",
            preference_value="yes"
        )
        
        print(f"✅ Set preferences with IDs: {pref_id1}, {pref_id2}")
    except Exception as e:
        print(f"❌ Error setting preferences: {str(e)}")
        return
    
    # Test 12: Get student preferences
    print("\nTest 12: Getting student preferences...")
    try:
        preferences = manager.get_student_preferences(student_id)
        if len(preferences) >= 2:
            print(f"✅ Retrieved {len(preferences)} preferences")
        else:
            print(f"❌ Expected at least 2 preferences, got {len(preferences)}")
            return
    except Exception as e:
        print(f"❌ Error retrieving preferences: {str(e)}")
        return
    
    # Test 13: Get full profile
    print("\nTest 13: Getting full student profile...")
    try:
        profile = manager.get_student_full_profile(student_id)
        if profile and 'skills' in profile and 'target_orgs' in profile and 'contributions' in profile and 'preferences' in profile:
            print("✅ Retrieved full profile successfully")
        else:
            print("❌ Failed to retrieve complete profile")
            return
    except Exception as e:
        print(f"❌ Error retrieving full profile: {str(e)}")
        return
    
    # Test 14: Deactivate student
    print("\nTest 14: Deactivating student...")
    try:
        success = manager.deactivate_student(student_id)
        if success:
            # Verify deactivation
            student = manager.get_student(student_id)
            if student.get('is_active') in [False, 'FALSE', 'false']:
                print("✅ Deactivated student successfully")
            else:
                print("❌ Deactivation verification failed")
                return
        else:
            print("❌ Failed to deactivate student")
            return
    except Exception as e:
        print(f"❌ Error deactivating student: {str(e)}")
        return
    
    # Test 15: Activate student
    print("\nTest 15: Activating student...")
    try:
        success = manager.activate_student(student_id)
        if success:
            # Verify activation
            student = manager.get_student(student_id)
            if student.get('is_active') in [True, 'TRUE', 'true']:
                print("✅ Activated student successfully")
            else:
                print("❌ Activation verification failed")
                return
        else:
            print("❌ Failed to activate student")
            return
    except Exception as e:
        print(f"❌ Error activating student: {str(e)}")
        return
    
    # Test 16: Get all students
    print("\nTest 16: Getting all students...")
    try:
        all_students = manager.get_all_students()
        print(f"✅ Retrieved {len(all_students)} active students")
    except Exception as e:
        print(f"❌ Error retrieving all students: {str(e)}")
        return
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    # Check if environment variables are set
    sheets_key_path = os.environ.get('GOOGLE_SERVICE_ACCOUNT_PATH')
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not sheets_key_path or not spreadsheet_id:
        print("Error: Required environment variables not set.")
        print("Please set GOOGLE_SERVICE_ACCOUNT_PATH and SPREADSHEET_ID.")
        sys.exit(1)
    
    test_student_profiles(
        sheets_key_path=sheets_key_path,
        spreadsheet_id=spreadsheet_id,
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
