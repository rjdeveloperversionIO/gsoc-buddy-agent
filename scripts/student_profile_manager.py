"""
Student Profile Manager for GSoC Buddy
Provides functions to manage student profiles in both Google Sheets and Supabase
"""

import os
import json
import uuid
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from supabase import create_client, Client
from typing import Dict, Any, Optional, List, Union

class StudentProfileManager:
    """Class to manage student profiles in Google Sheets and Supabase"""
    
    def __init__(self, sheets_key_path: str, spreadsheet_id: str, 
                 supabase_url: Optional[str] = None, supabase_key: Optional[str] = None):
        """
        Initialize the profile manager
        
        Args:
            sheets_key_path: Path to the Google Sheets service account key file
            spreadsheet_id: ID of the Google Spreadsheet
            supabase_url: Supabase URL (optional)
            supabase_key: Supabase API key (optional)
        """
        # Initialize Google Sheets client
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(sheets_key_path, scope)
        gc = gspread.authorize(credentials)
        self.spreadsheet = gc.open_by_key(spreadsheet_id)
        
        # Get worksheet references
        self.students_sheet = self.spreadsheet.worksheet('Students')
        self.skills_sheet = self.spreadsheet.worksheet('Student_Skills')
        self.target_orgs_sheet = self.spreadsheet.worksheet('Student_Target_Orgs')
        self.contributions_sheet = self.spreadsheet.worksheet('Student_Contributions')
        self.preferences_sheet = self.spreadsheet.worksheet('Student_Preferences')
        
        # Initialize Supabase client if credentials provided
        self.supabase = None
        if supabase_url and supabase_key:
            self.supabase = create_client(supabase_url, supabase_key)
    
    def add_student(self, github_username: str, display_name: str, 
                   email: Optional[str] = None, telegram_id: Optional[str] = None,
                   discord_id: Optional[str] = None, timezone: Optional[str] = None,
                   available_hours_weekly: Optional[int] = None, 
                   preferred_contact_method: Optional[str] = None,
                   learning_style: Optional[str] = None, gsoc_goals: Optional[str] = None,
                   bio: Optional[str] = None) -> str:
        """
        Add a new student profile
        
        Args:
            github_username: GitHub username (unique identifier)
            display_name: Name to display in communications
            email: Email address (optional)
            telegram_id: Telegram user ID (optional)
            discord_id: Discord user ID (optional)
            timezone: Student's timezone (optional)
            available_hours_weekly: Hours available per week (optional)
            preferred_contact_method: Preferred contact method (optional)
            learning_style: Preferred learning style (optional)
            gsoc_goals: Goals for GSoC participation (optional)
            bio: Short student bio (optional)
            
        Returns:
            The student_id of the created profile
        
        Raises:
            ValueError: If a student with the given GitHub username already exists
        """
        # Check if student already exists
        existing_student = self.get_student_by_github(github_username)
        if existing_student:
            raise ValueError(f"Student with GitHub username '{github_username}' already exists")
        
        # Generate a new student ID
        student_id = str(uuid.uuid4())
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare row data
        row_data = [
            student_id,
            github_username,
            display_name,
            email or '',
            telegram_id or '',
            discord_id or '',
            timezone or '',
            available_hours_weekly or '',
            preferred_contact_method or '',
            learning_style or '',
            gsoc_goals or '',
            bio or '',
            'TRUE',  # is_active
            now,     # created_at
            now      # updated_at
        ]
        
        # Add to Google Sheets
        self.students_sheet.append_row(row_data)
        
        # Add to Supabase if available
        if self.supabase:
            student_data = {
                'student_id': student_id,
                'github_username': github_username,
                'display_name': display_name,
                'email': email,
                'telegram_id': telegram_id,
                'discord_id': discord_id,
                'timezone': timezone,
                'available_hours_weekly': available_hours_weekly,
                'preferred_contact_method': preferred_contact_method,
                'learning_style': learning_style,
                'gsoc_goals': gsoc_goals,
                'bio': bio,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            }
            
            # Remove None values
            student_data = {k: v for k, v in student_data.items() if v is not None}
            
            self.supabase.table('students').insert(student_data).execute()
        
        return student_id
    
    def update_student(self, student_id: str, **kwargs) -> bool:
        """
        Update a student profile
        
        Args:
            student_id: The ID of the student to update
            **kwargs: Fields to update (any field from the student table)
            
        Returns:
            True if successful, False otherwise
        
        Raises:
            ValueError: If the student_id doesn't exist
        """
        # Get current student data
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' not found")
        
        # Find the row index in Google Sheets
        all_students = self.students_sheet.get_all_values()
        row_idx = None
        for i, row in enumerate(all_students):
            if row[0] == student_id:
                row_idx = i + 1  # +1 because sheets are 1-indexed
                break
        
        if not row_idx:
            raise ValueError(f"Student with ID '{student_id}' not found in Google Sheets")
        
        # Update timestamp
        kwargs['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Update in Google Sheets
        for field, value in kwargs.items():
            # Find the column index
            col_idx = None
            for j, header in enumerate(all_students[0]):
                if header == field:
                    col_idx = j + 1  # +1 because sheets are 1-indexed
                    break
            
            if col_idx:
                self.students_sheet.update_cell(row_idx, col_idx, value)
        
        # Update in Supabase if available
        if self.supabase:
            self.supabase.table('students').update(kwargs).eq('student_id', student_id).execute()
        
        return True
    
    def get_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a student profile by ID
        
        Args:
            student_id: The ID of the student to retrieve
            
        Returns:
            The student profile as a dictionary, or None if not found
        """
        # Try to get from Google Sheets
        all_students = self.students_sheet.get_all_records()
        headers = self.students_sheet.row_values(1)
        
        for student in all_students:
            if student.get('student_id') == student_id:
                return student
        
        # If not found in Sheets, try Supabase if available
        if self.supabase:
            response = self.supabase.table('students').select('*').eq('student_id', student_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
        
        return None
    
    def get_student_by_github(self, github_username: str) -> Optional[Dict[str, Any]]:
        """
        Get a student profile by GitHub username
        
        Args:
            github_username: The GitHub username to look up
            
        Returns:
            The student profile as a dictionary, or None if not found
        """
        # Try to get from Google Sheets
        all_students = self.students_sheet.get_all_records()
        
        for student in all_students:
            if student.get('github_username') == github_username:
                return student
        
        # If not found in Sheets, try Supabase if available
        if self.supabase:
            response = self.supabase.table('students').select('*').eq('github_username', github_username).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
        
        return None
    
    def add_skill(self, student_id: str, skill_name: str, skill_type: str, 
                 proficiency: str, years_experience: Optional[float] = None,
                 is_primary: bool = False) -> str:
        """
        Add a skill to a student profile
        
        Args:
            student_id: The ID of the student
            skill_name: Name of the skill (e.g., "Python")
            skill_type: Type of skill ("language", "framework", "tool", or "domain")
            proficiency: Skill level ("beginner", "intermediate", or "advanced")
            years_experience: Years of experience with this skill (optional)
            is_primary: Whether this is a primary/focus skill (default: False)
            
        Returns:
            The skill_id of the created skill
            
        Raises:
            ValueError: If the student_id doesn't exist
        """
        # Verify student exists
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' not found")
        
        # Generate a new skill ID
        skill_id = str(uuid.uuid4())
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare row data
        row_data = [
            skill_id,
            student_id,
            skill_name,
            skill_type,
            proficiency,
            years_experience or '',
            'TRUE' if is_primary else 'FALSE',
            now,     # created_at
            now      # updated_at
        ]
        
        # Add to Google Sheets
        self.skills_sheet.append_row(row_data)
        
        # Add to Supabase if available
        if self.supabase:
            skill_data = {
                'skill_id': skill_id,
                'student_id': student_id,
                'skill_name': skill_name,
                'skill_type': skill_type,
                'proficiency': proficiency,
                'years_experience': years_experience,
                'is_primary': is_primary,
                'created_at': now,
                'updated_at': now
            }
            
            # Remove None values
            skill_data = {k: v for k, v in skill_data.items() if v is not None}
            
            self.supabase.table('student_skills').insert(skill_data).execute()
        
        return skill_id
    
    def get_student_skills(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get all skills for a student
        
        Args:
            student_id: The ID of the student
            
        Returns:
            List of skill dictionaries
        """
        # Get from Google Sheets
        all_skills = self.skills_sheet.get_all_records()
        student_skills = []
        
        for skill in all_skills:
            if skill.get('student_id') == student_id:
                student_skills.append(skill)
        
        return student_skills
    
    def add_target_org(self, student_id: str, org_name: str, 
                      priority: Optional[int] = None, reason: Optional[str] = None) -> str:
        """
        Add a target organization to a student profile
        
        Args:
            student_id: The ID of the student
            org_name: Name of the target organization
            priority: Priority level (1=highest) (optional)
            reason: Why the student is interested in this org (optional)
            
        Returns:
            The target_id of the created target
            
        Raises:
            ValueError: If the student_id doesn't exist
        """
        # Verify student exists
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' not found")
        
        # Generate a new target ID
        target_id = str(uuid.uuid4())
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare row data
        row_data = [
            target_id,
            student_id,
            org_name,
            priority or '',
            reason or '',
            now      # created_at
        ]
        
        # Add to Google Sheets
        self.target_orgs_sheet.append_row(row_data)
        
        # Add to Supabase if available
        if self.supabase:
            target_data = {
                'target_id': target_id,
                'student_id': student_id,
                'org_name': org_name,
                'priority': priority,
                'reason': reason,
                'created_at': now
            }
            
            # Remove None values
            target_data = {k: v for k, v in target_data.items() if v is not None}
            
            self.supabase.table('student_target_orgs').insert(target_data).execute()
        
        return target_id
    
    def get_student_target_orgs(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get all target organizations for a student
        
        Args:
            student_id: The ID of the student
            
        Returns:
            List of target organization dictionaries
        """
        # Get from Google Sheets
        all_targets = self.target_orgs_sheet.get_all_records()
        student_targets = []
        
        for target in all_targets:
            if target.get('student_id') == student_id:
                student_targets.append(target)
        
        return student_targets
    
    def add_contribution(self, student_id: str, repo_name: str, contribution_type: str,
                        url: str, description: Optional[str] = None, 
                        is_gsoc_related: bool = False) -> str:
        """
        Add a contribution to a student profile
        
        Args:
            student_id: The ID of the student
            repo_name: Repository name with owner (e.g., "org/repo")
            contribution_type: Type of contribution ("issue", "pr", or "discussion")
            url: URL to the contribution
            description: Brief description of the contribution (optional)
            is_gsoc_related: Whether it was part of GSoC (default: False)
            
        Returns:
            The contribution_id of the created contribution
            
        Raises:
            ValueError: If the student_id doesn't exist
        """
        # Verify student exists
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' not found")
        
        # Generate a new contribution ID
        contribution_id = str(uuid.uuid4())
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Prepare row data
        row_data = [
            contribution_id,
            student_id,
            repo_name,
            contribution_id,
            student_id,
            repo_name,
            contribution_type,
            url,
            description or '',
            now,     # created_at
            'TRUE' if is_gsoc_related else 'FALSE'
        ]
        
        # Add to Google Sheets
        self.contributions_sheet.append_row(row_data)
        
        # Add to Supabase if available
        if self.supabase:
            contribution_data = {
                'contribution_id': contribution_id,
                'student_id': student_id,
                'repo_name': repo_name,
                'contribution_type': contribution_type,
                'url': url,
                'description': description,
                'created_at': now,
                'is_gsoc_related': is_gsoc_related
            }
            
            # Remove None values
            contribution_data = {k: v for k, v in contribution_data.items() if v is not None}
            
            self.supabase.table('student_contributions').insert(contribution_data).execute()
        
        return contribution_id
    
    def get_student_contributions(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get all contributions for a student
        
        Args:
            student_id: The ID of the student
            
        Returns:
            List of contribution dictionaries
        """
        # Get from Google Sheets
        all_contributions = self.contributions_sheet.get_all_records()
        student_contributions = []
        
        for contribution in all_contributions:
            if contribution.get('student_id') == student_id:
                student_contributions.append(contribution)
        
        return student_contributions
    
    def set_preference(self, student_id: str, preference_key: str, preference_value: str) -> str:
        """
        Set a preference for a student
        
        Args:
            student_id: The ID of the student
            preference_key: Preference identifier
            preference_value: Preference value
            
        Returns:
            The preference_id of the created/updated preference
            
        Raises:
            ValueError: If the student_id doesn't exist
        """
        # Verify student exists
        student = self.get_student(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' not found")
        
        # Check if preference already exists
        all_preferences = self.preferences_sheet.get_all_records()
        existing_preference = None
        row_idx = None
        
        for i, pref in enumerate(all_preferences, start=2):  # Start from row 2 (1-indexed)
            if pref.get('student_id') == student_id and pref.get('preference_key') == preference_key:
                existing_preference = pref
                row_idx = i
                break
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if existing_preference:
            # Update existing preference
            preference_id = existing_preference.get('preference_id')
            self.preferences_sheet.update_cell(row_idx, 4, preference_value)  # Column D (4) is preference_value
            self.preferences_sheet.update_cell(row_idx, 6, now)  # Column F (6) is updated_at
            
            # Update in Supabase if available
            if self.supabase:
                self.supabase.table('student_preferences').update({
                    'preference_value': preference_value,
                    'updated_at': now
                }).eq('preference_id', preference_id).execute()
        else:
            # Create new preference
            preference_id = str(uuid.uuid4())
            
            # Prepare row data
            row_data = [
                preference_id,
                student_id,
                preference_key,
                preference_value,
                now,     # created_at
                now      # updated_at
            ]
            
            # Add to Google Sheets
            self.preferences_sheet.append_row(row_data)
            
            # Add to Supabase if available
            if self.supabase:
                preference_data = {
                    'preference_id': preference_id,
                    'student_id': student_id,
                    'preference_key': preference_key,
                    'preference_value': preference_value,
                    'created_at': now,
                    'updated_at': now
                }
                
                self.supabase.table('student_preferences').insert(preference_data).execute()
        
        return preference_id
    
    def get_student_preferences(self, student_id: str) -> Dict[str, str]:
        """
        Get all preferences for a student
        
        Args:
            student_id: The ID of the student
            
        Returns:
            Dictionary mapping preference keys to values
        """
        # Get from Google Sheets
        all_preferences = self.preferences_sheet.get_all_records()
        student_preferences = {}
        
        for pref in all_preferences:
            if pref.get('student_id') == student_id:
                student_preferences[pref.get('preference_key')] = pref.get('preference_value')
        
        return student_preferences
    
    def get_all_students(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get all student profiles
        
        Args:
            active_only: Whether to return only active students (default: True)
            
        Returns:
            List of student dictionaries
        """
        # Get from Google Sheets
        all_students = self.students_sheet.get_all_records()
        
        if active_only:
            return [student for student in all_students if student.get('is_active') == 'TRUE']
        else:
            return all_students
    
    def deactivate_student(self, student_id: str) -> bool:
        """
        Deactivate a student profile
        
        Args:
            student_id: The ID of the student to deactivate
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_student(student_id, is_active=False)
    
    def activate_student(self, student_id: str) -> bool:
        """
        Activate a student profile
        
        Args:
            student_id: The ID of the student to activate
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_student(student_id, is_active=True)
    
    def get_student_full_profile(self, student_id: str) -> Dict[str, Any]:
        """
        Get a complete student profile including skills, target orgs, contributions, and preferences
        
        Args:
            student_id: The ID of the student
            
        Returns:
            Dictionary with all student information
        """
        # Get basic profile
        student = self.get_student(student_id)
        if not student:
            return None
        
        # Add related information
        student['skills'] = self.get_student_skills(student_id)
        student['target_orgs'] = self.get_student_target_orgs(student_id)
        student['contributions'] = self.get_student_contributions(student_id)
        student['preferences'] = self.get_student_preferences(student_id)
        
        return student

# Example usage
if __name__ == "__main__":
    # This is just an example, not meant to be run directly
    # Replace with actual values when using
    manager = StudentProfileManager(
        sheets_key_path="service_account.json",
        spreadsheet_id="your-spreadsheet-id",
        supabase_url="your-supabase-url",
        supabase_key="your-supabase-key"
    )
    
    # Example: Add a student
    try:
        student_id = manager.add_student(
            github_username="johndoe",
            display_name="John Doe",
            email="john@example.com",
            telegram_id="johndoe123",
            timezone="UTC+2",
            available_hours_weekly=10,
            preferred_contact_method="telegram",
            learning_style="Visual learner, prefers hands-on tutorials",
            gsoc_goals="Gain experience in open source development",
            bio="Computer Science student interested in web development"
        )
        print(f"Added student with ID: {student_id}")
        
        # Example: Add skills
        manager.add_skill(
            student_id=student_id,
            skill_name="Python",
            skill_type="language",
            proficiency="intermediate",
            years_experience=2.5,
            is_primary=True
        )
        
        # Example: Add target organization
        manager.add_target_org(
            student_id=student_id,
            org_name="Zulip",
            priority=1,
            reason="Interested in their tech stack and community"
        )
        
        # Example: Set preferences
        manager.set_preference(
            student_id=student_id,
            preference_key="difficulty_max",
            preference_value="7"
        )
        
        # Example: Get full profile
        profile = manager.get_student_full_profile(student_id)
        print(f"Student profile: {profile}")
        
    except Exception as e:
        print(f"Error: {str(e)}")              
