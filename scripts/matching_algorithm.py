"""
Matching Algorithm for GSoC Buddy
Implements the logic for matching students with GitHub issues
"""

import math
from typing import Dict, Any, List, Tuple, Optional

class MatchingAlgorithm:
    """Class that implements the matching algorithm logic"""
    
    def __init__(self, 
                 weight_skill_alignment: float = 0.35,
                 weight_difficulty_fit: float = 0.20,
                 weight_org_fit: float = 0.15,
                 weight_time_fit: float = 0.15,
                 weight_strategic_value: float = 0.15):
        """
        Initialize the matching algorithm with configurable weights
        
        Args:
            weight_skill_alignment: Weight for skill alignment factor (default: 0.35)
            weight_difficulty_fit: Weight for difficulty fit factor (default: 0.20)
            weight_org_fit: Weight for organization fit factor (default: 0.15)
            weight_time_fit: Weight for time fit factor (default: 0.15)
            weight_strategic_value: Weight for strategic value factor (default: 0.15)
        """
        # Validate weights sum to 1.0
        total_weight = (weight_skill_alignment + weight_difficulty_fit + 
                        weight_org_fit + weight_time_fit + weight_strategic_value)
        if not math.isclose(total_weight, 1.0, rel_tol=1e-5):
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
        
        self.weight_skill_alignment = weight_skill_alignment
        self.weight_difficulty_fit = weight_difficulty_fit
        self.weight_org_fit = weight_org_fit
        self.weight_time_fit = weight_time_fit
        self.weight_strategic_value = weight_strategic_value
    
    def calculate_match_score(self, student: Dict[str, Any], issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate the match score between a student and an issue
        
        Args:
            student: Dictionary containing student profile data
            issue: Dictionary containing issue data
            
        Returns:
            Dictionary with match score and component scores
        """
        # Calculate component scores
        skill_alignment_score = self._calculate_skill_alignment(student, issue)
        difficulty_fit_score = self._calculate_difficulty_fit(student, issue)
        org_fit_score = self._calculate_org_fit(student, issue)
        time_fit_score = self._calculate_time_fit(student, issue)
        strategic_value_score = self._calculate_strategic_value(student, issue)
        
        # Calculate weighted final score
        final_score = (
            skill_alignment_score * self.weight_skill_alignment +
            difficulty_fit_score * self.weight_difficulty_fit +
            org_fit_score * self.weight_org_fit +
            time_fit_score * self.weight_time_fit +
            strategic_value_score * self.weight_strategic_value
        )
        
        # Determine match category
        match_category = self._get_match_category(final_score)
        
        # Create explanation for the match
        explanation = self._generate_explanation(
            student, issue,
            skill_alignment_score, difficulty_fit_score,
            org_fit_score, time_fit_score, strategic_value_score,
            final_score
        )
        
        # Return comprehensive result
        return {
            'student_id': student.get('student_id'),
            'issue_id': issue.get('issue_id'),
            'match_score': round(final_score, 2),
            'match_category': match_category,
            'component_scores': {
                'skill_alignment': round(skill_alignment_score, 2),
                'difficulty_fit': round(difficulty_fit_score, 2),
                'org_fit': round(org_fit_score, 2),
                'time_fit': round(time_fit_score, 2),
                'strategic_value': round(strategic_value_score, 2)
            },
            'explanation': explanation
        }
    
    def _calculate_skill_alignment(self, student: Dict[str, Any], issue: Dict[str, Any]) -> float:
        """
        Calculate the skill alignment score
        
        Args:
            student: Student profile data
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # Extract required skills from issue
        required_skills = issue.get('required_skills', [])
        if not required_skills:
            return 50.0  # Default middle score if no skills specified
        
        # Extract student skills
        student_skills = []
        for skill in student.get('skills', []):
            student_skills.append({
                'name': skill.get('skill_name', '').lower(),
                'type': skill.get('skill_type', '').lower(),
                'proficiency': skill.get('proficiency', 'beginner').lower()
            })
        
        # Calculate primary language match
        primary_language_score = 0
        primary_language = next((s for s in required_skills if s.lower() == issue.get('primary_language', '').lower()), None)
        if primary_language:
            # Check if student knows the primary language
            for skill in student_skills:
                if skill['type'] == 'language':
                    if skill['name'] == primary_language.lower():
                        # Perfect match
                        if skill['proficiency'] == 'advanced':
                            primary_language_score = 100
                        elif skill['proficiency'] == 'intermediate':
                            primary_language_score = 90
                        else:  # beginner
                            primary_language_score = 80
                        break
                    elif self._are_related_languages(skill['name'], primary_language.lower()):
                        # Related language
                        if skill['proficiency'] == 'advanced':
                            primary_language_score = 70
                        elif skill['proficiency'] == 'intermediate':
                            primary_language_score = 60
                        else:  # beginner
                            primary_language_score = 50
                        break
        
        # Calculate framework/library knowledge
        framework_scores = []
        for skill_name in required_skills:
            if skill_name.lower() == primary_language.lower():
                continue  # Skip primary language, already counted
            
            best_score = 0
            for skill in student_skills:
                if skill['name'] == skill_name.lower():
                    # Direct match
                    if skill['proficiency'] == 'advanced':
                        best_score = 100
                    elif skill['proficiency'] == 'intermediate':
                        best_score = 80
                    else:  # beginner
                        best_score = 60
                    break
                elif self._are_related_technologies(skill['name'], skill_name.lower()):
                    # Related technology
                    if skill['proficiency'] == 'advanced':
                        best_score = max(best_score, 70)
                    elif skill['proficiency'] == 'intermediate':
                        best_score = max(best_score, 50)
                    else:  # beginner
                        best_score = max(best_score, 30)
            
            framework_scores.append(best_score)
        
        # Calculate average framework score
        framework_score = sum(framework_scores) / max(len(framework_scores), 1)
        
        # Calculate overall proficiency level
        proficiency_mapping = {'beginner': 50, 'intermediate': 80, 'advanced': 100}
        proficiency_scores = [proficiency_mapping.get(skill['proficiency'], 0) for skill in student_skills]
        proficiency_score = sum(proficiency_scores) / max(len(proficiency_scores), 1)
        
        # Calculate final skill alignment score
        skill_alignment_score = (
            primary_language_score * 0.5 +
            framework_score * 0.3 +
            proficiency_score * 0.2
        )
        
        return skill_alignment_score
    
    def _calculate_difficulty_fit(self, student: Dict[str, Any], issue: Dict[str, Any]) -> float:
        """
        Calculate the difficulty fit score
        
        Args:
            student: Student profile data
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # Get issue difficulty
        issue_difficulty = issue.get('difficulty_score', 5)  # Default to middle difficulty
        
        # Estimate student skill level (1-10 scale)
        student_skill_level = self._estimate_student_skill_level(student)
        
        # Calculate difficulty gap
        difficulty_gap = issue_difficulty - student_skill_level
        
        # Score the difficulty gap
        difficulty_gap_score = 0
        if difficulty_gap == 0:
            # Perfect match
            difficulty_gap_score = 100
        elif difficulty_gap == 1:
            # Slightly challenging
            difficulty_gap_score = 90
        elif difficulty_gap == 2:
            # Moderately challenging
            difficulty_gap_score = 70
        elif difficulty_gap == 3:
            # Very challenging
            difficulty_gap_score = 40
        elif difficulty_gap > 3:
            # Too difficult
            difficulty_gap_score = 0
        elif difficulty_gap < 0:
            # Too easy
            difficulty_gap_score = 60
        
        # Calculate learning opportunity
        learning_opportunity_score = self._calculate_learning_opportunity(student, issue)
        
        # Calculate final difficulty fit score
        difficulty_fit_score = (
            difficulty_gap_score * 0.7 +
            learning_opportunity_score * 0.3
        )
        
        return difficulty_fit_score
    
    def _calculate_org_fit(self, student: Dict[str, Any], issue: Dict[str, Any]) -> float:
        """
        Calculate the organization fit score
        
        Args:
            student: Student profile data
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # Get organization name
        org_name = issue.get('org_name', '')
        
        # Check if organization is in student's target list
        target_org_score = 0
        for target_org in student.get('target_orgs', []):
            if target_org.get('org_name', '').lower() == org_name.lower():
                priority = target_org.get('priority', 3)  # Default to low priority
                if priority == 1:
                    target_org_score = 100  # Top priority
                elif priority == 2:
                    target_org_score = 80   # Medium priority
                else:
                    target_org_score = 60   # Low priority
                break
        
        # If not a target, check if it's in a related domain
        if target_org_score == 0:
            # This would require domain knowledge about organizations
            # For now, we'll use a simple heuristic based on student's skills
            student_domains = self._extract_student_domains(student)
            org_domains = self._extract_org_domains(issue)
            
            if any(domain in org_domains for domain in student_domains):
                target_org_score = 40  # Not a target but in same domain
        
        # Check previous contributions
        previous_contributions_score = 0
        accepted_count = 0
        pending_count = 0
        
        for contribution in student.get('contributions', []):
            if contribution.get('repo_name', '').startswith(org_name + '/'):
                if contribution.get('contribution_type') == 'pr':
                    accepted_count += 1
                else:
                    pending_count += 1
        
        if accepted_count > 1:
            previous_contributions_score = 100  # Multiple accepted contributions
        elif accepted_count == 1:
            previous_contributions_score = 80   # One accepted contribution
        elif pending_count > 0:
            previous_contributions_score = 50   # Pending contributions
        
        # Calculate final organization fit score
        org_fit_score = (
            target_org_score * 0.6 +
            previous_contributions_score * 0.4
        )
        
        return org_fit_score
    
    def _calculate_time_fit(self, student: Dict[str, Any], issue: Dict[str, Any]) -> float:
        """
        Calculate the time fit score
        
        Args:
            student: Student profile data
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # Get issue estimated time
        issue_time = issue.get('estimated_time_hours', 10)  # Default to 10 hours
        
        # Get student available time
        available_hours_weekly = student.get('available_hours_weekly', 10)  # Default to 10 hours
        
        # Assume student can dedicate 1/3 of their weekly time to a single issue
        available_time = available_hours_weekly / 3
        
        # Calculate time ratio
        time_ratio = available_time / issue_time if issue_time > 0 else 2.0  # Default to plenty of time
        
        # Score the time requirement
        time_requirement_score = 0
        if time_ratio > 2.0:
            time_requirement_score = 100  # Plenty of time
        elif time_ratio > 1.5:
            time_requirement_score = 90   # Adequate time
        elif time_ratio > 1.0:
            time_requirement_score = 70   # Just enough time
        elif time_ratio > 0.8:
            time_requirement_score = 40   # Tight schedule
        else:
            time_requirement_score = 0    # Not enough time
        
        # Calculate urgency score
        # This would typically come from issue metadata or be calculated based on
        # factors like issue age, organization deadlines, etc.
        # For now, we'll use a default value
        urgency_score = 80  # Default to low urgency
        
        # Calculate final time fit score
        time_fit_score = (
            time_requirement_score * 0.8 +
            urgency_score * 0.2
        )
        
        return time_fit_score
    
    def _calculate_strategic_value(self, student: Dict[str, Any], issue: Dict[str, Any]) -> float:
        """
        Calculate the strategic value score
        
        Args:
            student: Student profile data
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # Calculate visibility score
        # This would typically be based on issue importance, repository popularity, etc.
        # For now, we'll use a heuristic based on issue labels and repository stats
        visibility_score = self._calculate_visibility(issue)
        
        # Calculate mentor activity score
        mentor_activity_score = self._calculate_mentor_activity(issue)
        
        # Calculate competition level score
        competition_level_score = self._calculate_competition_level(issue)
        
        # Calculate final strategic value score
        strategic_value_score = (
            visibility_score * 0.4 +
            mentor_activity_score * 0.3 +
            competition_level_score * 0.3
        )
        
        return strategic_value_score
    
    def _get_match_category(self, score: float) -> str:
        """
        Determine the match category based on the score
        
        Args:
            score: Match score from 0-100
            
        Returns:
            Match category string
        """
        if score >= 90:
            return "Perfect Match"
        elif score >= 75:
            return "Strong Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Potential Match"
        else:
            return "Poor Match"
    
    def _generate_explanation(self, student: Dict[str, Any], issue: Dict[str, Any],
                             skill_score: float, difficulty_score: float,
                             org_score: float, time_score: float, strategic_score: float,
                             final_score: float) -> str:
        """
        Generate a human-readable explanation for the match
        
        Args:
            student: Student profile data
            issue: Issue data
            skill_score: Skill alignment score
            difficulty_score: Difficulty fit score
            org_score: Organization fit score
            time_score: Time fit score
            strategic_score: Strategic value score
            final_score: Final match score
            
        Returns:
            Explanation string
        """
        # Start with overall assessment
        category = self._get_match_category(final_score)
        explanation = f"This is a {category.lower()} ({round(final_score, 1)}/100) because:\n\n"
        
        # Add component explanations
        components = [
            ("Skill Alignment", skill_score, self.weight_skill_alignment),
            ("Difficulty Fit", difficulty_score, self.weight_difficulty_fit),
            ("Organization Fit", org_score, self.weight_org_fit),
            ("Time Fit", time_score, self.weight_time_fit),
            ("Strategic Value", strategic_score, self.weight_strategic_value)
        ]
        
        # Sort components by weighted contribution to final score
        components.sort(key=lambda x: x[1] * x[2], reverse=True)
        
        # Add explanation for each component
        for name, score, weight in components:
            contribution = score * weight
            percentage = round(contribution / final_score * 100 if final_score > 0 else 0)
            
            explanation += f"• {name}: {round(score, 1)}/100 "
            explanation += f"({percentage}% of match score)\n"
            
            # Add specific details for each component
            if name == "Skill Alignment":
                explanation += self._explain_skill_alignment(student, issue, score)
            elif name == "Difficulty Fit":
                explanation += self._explain_difficulty_fit(student, issue, score)
            elif name == "Organization Fit":
                explanation += self._explain_org_fit(student, issue, score)
            elif name == "Time Fit":
                explanation += self._explain_time_fit(student, issue, score)
            elif name == "Strategic Value":
                explanation += self._explain_strategic_value(student, issue, score)
            
            explanation += "\n"
        
        # Add recommendation
        if final_score >= 75:
            explanation += "Recommendation: This issue is highly recommended for you."
        elif final_score >= 60:
            explanation += "Recommendation: This issue is a good match, but consider the areas where the fit isn't perfect."
        elif final_score >= 40:
            explanation += "Recommendation: This issue could be a match, but be aware of the challenges noted above."
        else:
            explanation += "Recommendation: This issue is not recommended for you based on the current fit."
        
        return explanation
    
    def _explain_skill_alignment(self, student: Dict[str, Any], issue: Dict[str, Any], score: float) -> str:
        """Generate explanation for skill alignment score"""
        required_skills = issue.get('required_skills', [])
        primary_language = issue.get('primary_language', '')
        
        if score >= 80:
            return f"  You have strong skills in {primary_language} and most of the required technologies."
        elif score >= 60:
            return f"  You have some experience with {primary_language} and some of the required technologies."
        elif score >= 40:
            return f"  You have limited experience with the required skills ({', '.join(required_skills[:3])})."
        else:
            return f"  Your skills don't align well with the requirements ({', '.join(required_skills[:3])})."
    
    def _explain_difficulty_fit(self, student: Dict[str, Any], issue: Dict[str, Any], score: float) -> str:
        """Generate explanation for difficulty fit score"""
        difficulty = issue.get('difficulty_score', 5)
        
        if score >= 80:
            return f"  The difficulty level ({difficulty}/10) is well-suited to your experience."
        elif score >= 60:
            return f"  The difficulty level ({difficulty}/10) is somewhat challenging but manageable."
        elif score >= 40:
            return f"  The difficulty level ({difficulty}/10) may be challenging for your current experience."
        else:
            return f"  The difficulty level ({difficulty}/10) doesn't match your experience level well."
    
    def _explain_org_fit(self, student: Dict[str, Any], issue: Dict[str, Any], score: float) -> str:
        """Generate explanation for organization fit score"""
        org_name = issue.get('org_name', '')
        
        if score >= 80:
            return f"  {org_name} is one of your target organizations and/or you have previous contributions."
        elif score >= 60:
            return f"  {org_name} aligns with your interests, though not a top target."
        elif score >= 40:
            return f"  {org_name} is somewhat related to your interests."
        else:
            return f"  {org_name} doesn't appear to be among your target organizations."
    
    def _explain_time_fit(self, student: Dict[str, Any], issue: Dict[str, Any], score: float) -> str:
        """Generate explanation for time fit score"""
        estimated_time = issue.get('estimated_time_hours', 10)
        available_hours = student.get('available_hours_weekly', 10)
        
        if score >= 80:
            return f"  You have plenty of time ({available_hours} hrs/week) for this issue (est. {estimated_time} hrs)."
        elif score >= 60:
            return f"  You have adequate time ({available_hours} hrs/week) for this issue (est. {estimated_time} hrs)."
        elif score >= 40:
            return f"  You may have just enough time ({available_hours} hrs/week) for this issue (est. {estimated_time} hrs)."
        else:
            return f"  You may not have enough time ({available_hours} hrs/week) for this issue (est. {estimated_time} hrs)."
    
    def _explain_strategic_value(self, student: Dict[str, Any], issue: Dict[str, Any], score: float) -> str:
        """Generate explanation for strategic value score"""
        if score >= 80:
            return "  This issue has high strategic value for GSoC selection (visibility, mentor activity, low competition)."
        elif score >= 60:
            return "  This issue has good strategic value for GSoC selection."
        elif score >= 40:
            return "  This issue has moderate strategic value for GSoC selection."
        else:
            return "  This issue has limited strategic value for GSoC selection."
    
    def _estimate_student_skill_level(self, student: Dict[str, Any]) -> int:
        """
        Estimate the student's overall skill level on a 1-10 scale
        
        Args:
            student: Student profile data
            
        Returns:
            Skill level from 1-10
        """
        # Get student skills
        skills = student.get('skills', [])
        if not skills:
            return 3  # Default to beginner-intermediate
        
        # Count skills by proficiency
        beginner_count = 0
        intermediate_count = 0
        advanced_count = 0
        
        for skill in skills:
            proficiency = skill.get('proficiency', '').lower()
            if proficiency == 'beginner':
                beginner_count += 1
            elif proficiency == 'intermediate':
                intermediate_count += 1
            elif proficiency == 'advanced':
                advanced_count += 1
        
        # Calculate weighted average
        total_skills = beginner_count + intermediate_count + advanced_count
        if total_skills == 0:
            return 3  # Default
        
        weighted_sum = (beginner_count * 2 + intermediate_count * 5 + advanced_count * 9)
        average = weighted_sum / total_skills
        
        # Round to nearest integer
        return round(average)
    
    def _calculate_learning_opportunity(self, student: Dict[str, Any], issue: Dict[str, Any]) -> float:
        """
        Calculate the learning opportunity score
        
        Args:
            student: Student profile data
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # Get required skills from issue
        required_skills = issue.get('required_skills', [])
        if not required_skills:
            return 50  # Default
        
        # Get student's existing skills
        student_skills = [skill.get('skill_name', '').lower() for skill in student.get('skills', [])]
        
        # Get student's learning goals
        learning_goals = []
        gsoc_goals = student.get('gsoc_goals', '').lower()
        if gsoc_goals:
            # Extract potential technologies from goals
            # This is a simple approach; in a real system, you might use NLP
            learning_goals = [word.strip() for word in gsoc_goals.split() 
                             if len(word) > 3 and not word.lower() in ['want', 'learn', 'with', 'and', 'the']]
        
        # Count new skills that align with learning goals
        new_skills = [skill for skill in required_skills if skill.lower() not in student_skills]
        aligned_new_skills = [skill for skill in new_skills 
                             if any(goal in skill.lower() or skill.lower() in goal 
                                   for goal in learning_goals)]
        
        # Calculate score
        if not new_skills:
            return 30  # Minimal learning opportunity
        
        if aligned_new_skills:
            # Strong alignment with learning goals
            return 100
        elif len(new_skills) >= 2:
            # Multiple new skills to learn
            return 70
        else:
            # One new skill, not aligned with goals
            return 50
    
    def _are_related_languages(self, lang1: str, lang2: str) -> bool:
        """
        Determine if two programming languages are related
        
        Args:
            lang1: First language
            lang2: Second language
            
        Returns:
            True if related, False otherwise
        """
        # Define groups of related languages
        language_groups = [
            {'javascript', 'typescript', 'coffeescript', 'jsx', 'node.js', 'nodejs'},
            {'python', 'cython', 'jython'},
            {'java', 'kotlin', 'scala'},
            {'c', 'c++', 'c#', 'objective-c'},
            {'ruby', 'crystal'},
            {'php', 'hack'},
            {'go', 'golang'},
            {'rust', 'nim'},
            {'swift', 'objective-c'},
            {'haskell', 'purescript', 'elm'},
            {'clojure', 'scheme', 'lisp', 'common lisp'},
            {'r', 'julia'},
            {'perl', 'raku'},
            {'shell', 'bash', 'zsh', 'powershell'},
            {'sql', 'plsql', 't-sql', 'mysql', 'postgresql', 'sqlite'}
        ]
        
        # Check if languages are in the same group
        lang1, lang2 = lang1.lower(), lang2.lower()
        for group in language_groups:
            if lang1 in group and lang2 in group:
                return True
        
        return False
    
    def _are_related_technologies(self, tech1: str, tech2: str) -> bool:
        """
        Determine if two technologies are related
        
        Args:
            tech1: First technology
            tech2: Second technology
            
        Returns:
            True if related, False otherwise
        """
        # Define groups of related technologies
        tech_groups = [
            {'react', 'react.js', 'reactjs', 'react native', 'redux', 'flux'},
            {'angular', 'angularjs', 'angular.js', 'angular2', 'angular 2'},
            {'vue', 'vue.js', 'vuejs', 'vuex'},
            {'django', 'flask', 'pyramid', 'fastapi', 'tornado'},
            {'express', 'koa', 'hapi', 'nest.js', 'nestjs', 'next.js', 'nextjs'},
            {'spring', 'spring boot', 'hibernate', 'jakarta ee', 'java ee'},
            {'laravel', 'symfony', 'codeigniter', 'cakephp'},
            {'rails', 'ruby on rails', 'sinatra', 'hanami'},
            {'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'sklearn'},
            {'mysql', 'postgresql', 'sqlite', 'sql server', 'oracle'},
            {'mongodb', 'couchdb', 'firebase', 'dynamodb', 'cosmosdb'},
            {'redis', 'memcached', 'caching'},
            {'docker', 'kubernetes', 'k8s', 'containerization'},
            {'aws', 'azure', 'gcp', 'cloud'},
            {'html', 'css', 'sass', 'scss', 'less', 'stylus'},
            {'webpack', 'babel', 'parcel', 'rollup', 'vite'},
            {'git', 'github', 'gitlab', 'bitbucket', 'version control'},
            {'rest', 'graphql', 'api', 'soap', 'grpc'},
            {'oauth', 'jwt', 'authentication', 'authorization'},
            {'linux', 'unix', 'posix', 'bash', 'shell'}
        ]
        
        # Check if technologies are in the same group
        tech1, tech2 = tech1.lower(), tech2.lower()
        for group in tech_groups:
            if tech1 in group and tech2 in group:
                return True
        
        # Check for substring matches (e.g., "react" and "react-router")
        if (tech1 in tech2 or tech2 in tech1) and min(len(tech1), len(tech2)) > 3:
            return True
        
        return False
    
    def _extract_student_domains(self, student: Dict[str, Any]) -> List[str]:
        """
        Extract domains of interest from student profile
        
        Args:
            student: Student profile data
            
        Returns:
            List of domains
        """
        domains = set()
        
        # Extract from GSoC goals
        gsoc_goals = student.get('gsoc_goals', '').lower()
        
        # Simple keyword matching for domains
        domain_keywords = {
            'web': ['web', 'frontend', 'backend', 'fullstack', 'javascript', 'html', 'css'],
            'mobile': ['mobile', 'android', 'ios', 'flutter', 'react native'],
            'data science': ['data science', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'data'],
            'devops': ['devops', 'cloud', 'kubernetes', 'docker', 'ci/cd', 'deployment'],
            'security': ['security', 'cryptography', 'encryption', 'privacy'],
            'gaming': ['game', 'gaming', 'unity', 'unreal'],
            'embedded': ['embedded', 'iot', 'hardware', 'arduino', 'raspberry pi'],
            'blockchain': ['blockchain', 'crypto', 'web3', 'ethereum', 'smart contract']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in gsoc_goals for keyword in keywords):
                domains.add(domain)
        
        # Extract from skills
        for skill in student.get('skills', []):
            skill_name = skill.get('skill_name', '').lower()
            for domain, keywords in domain_keywords:
              for domain, keywords in domain_keywords.items():
                if any(keyword in skill_name for keyword in keywords):
                    domains.add(domain)
        
        return list(domains)
    
    def _extract_org_domains(self, issue: Dict[str, Any]) -> List[str]:
        """
        Extract domains related to an organization/issue
        
        Args:
            issue: Issue data
            
        Returns:
            List of domains
        """
        domains = set()
        
        # Extract from organization name and description
        org_name = issue.get('org_name', '').lower()
        org_description = issue.get('org_description', '').lower()
        combined_text = org_name + ' ' + org_description
        
        # Simple keyword matching for domains
        domain_keywords = {
            'web': ['web', 'frontend', 'backend', 'fullstack', 'javascript', 'html', 'css'],
            'mobile': ['mobile', 'android', 'ios', 'flutter', 'react native'],
            'data science': ['data science', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'data'],
            'devops': ['devops', 'cloud', 'kubernetes', 'docker', 'ci/cd', 'deployment'],
            'security': ['security', 'cryptography', 'encryption', 'privacy'],
            'gaming': ['game', 'gaming', 'unity', 'unreal'],
            'embedded': ['embedded', 'iot', 'hardware', 'arduino', 'raspberry pi'],
            'blockchain': ['blockchain', 'crypto', 'web3', 'ethereum', 'smart contract']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                domains.add(domain)
        
        # Extract from required skills
        for skill in issue.get('required_skills', []):
            skill_lower = skill.lower()
            for domain, keywords in domain_keywords.items():
                if any(keyword in skill_lower for keyword in keywords):
                    domains.add(domain)
        
        return list(domains)
    
    def _calculate_visibility(self, issue: Dict[str, Any]) -> float:
        """
        Calculate the visibility score for an issue
        
        Args:
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # This would typically use repository stats like stars, watchers, etc.
        # For now, we'll use a simple heuristic based on issue labels
        
        # Check for high-visibility labels
        labels = [label.lower() for label in issue.get('labels', [])]
        high_visibility_labels = ['feature', 'enhancement', 'core', 'critical', 'high-priority']
        medium_visibility_labels = ['improvement', 'moderate', 'medium-priority']
        low_visibility_labels = ['minor', 'trivial', 'low-priority']
        
        if any(label in labels for label in high_visibility_labels):
            return 100
        elif any(label in labels for label in medium_visibility_labels):
            return 70
        elif any(label in labels for label in low_visibility_labels):
            return 40
        
        # If no specific labels, use a default based on issue type
        if 'bug' in labels:
            return 70  # Bugs are usually medium visibility
        elif 'documentation' in labels:
            return 40  # Documentation is usually lower visibility
        
        # Default to medium visibility
        return 60
    
    def _calculate_mentor_activity(self, issue: Dict[str, Any]) -> float:
        """
        Calculate the mentor activity score for an issue
        
        Args:
            issue: Issue data
            
        Returns:
            Score from 0-100
        """
        # This would typically use data about mentor response times, comment frequency, etc.
        # For now, we'll use a simple heuristic based on issue activity
        
        # Check if there are recent comments
        comments_count = issue.get('comments_count', 0)
        
        if comments_count > 5:
            return 100  # Very active
        elif comments_count > 2:
            return 80   # Active
        elif comments_count > 0:
            return 50   # Moderately active
        else:
            return 30   # Relatively inactive
    
    def _calculate_competition_level(self, issue: Dict[str, Any]) -> float:
        """
        Calculate the competition level score for an issue
        
        Args:
            issue: Issue data
            
        Returns:
            Score from 0-100 (higher means less competition, which is better)
        """
        # This would typically use data about how many people have commented or expressed interest
        # For now, we'll use a simple heuristic based on issue age and comments
        
        comments_count = issue.get('comments_count', 0)
        
        if comments_count > 10:
            return 20   # High competition
        elif comments_count > 5:
            return 50   # Medium competition
        elif comments_count > 2:
            return 80   # Low competition
        else:
            return 100  # No competition
    
    def find_matches(self, student: Dict[str, Any], issues: List[Dict[str, Any]], 
                    limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find the best matches for a student from a list of issues
        
        Args:
            student: Student profile data
            issues: List of issue data
            limit: Maximum number of matches to return (default: 10)
            
        Returns:
            List of match results, sorted by score (highest first)
        """
        matches = []
        
        for issue in issues:
            match_result = self.calculate_match_score(student, issue)
            matches.append(match_result)
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top matches
        return matches[:limit]
    
    def find_matches_for_all_students(self, students: List[Dict[str, Any]], 
                                     issues: List[Dict[str, Any]],
                                     matches_per_student: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Find matches for all students
        
        Args:
            students: List of student profile data
            issues: List of issue data
            matches_per_student: Number of matches to find per student (default: 5)
            
        Returns:
            Dictionary mapping student_id to list of match results
        """
        all_matches = {}
        
        for student in students:
            student_id = student.get('student_id')
            if student_id:
                student_matches = self.find_matches(student, issues, matches_per_student)
                all_matches[student_id] = student_matches
        
        return all_matches
    
    def adjust_weights_for_gsoc_phase(self, phase: str) -> None:
        """
        Adjust weights based on GSoC timeline phase
        
        Args:
            phase: GSoC phase ('early', 'middle', or 'late')
        """
        if phase == 'early':
            # Early phase: Focus on skill alignment and difficulty fit
            self.weight_skill_alignment = 0.40
            self.weight_difficulty_fit = 0.25
            self.weight_org_fit = 0.15
            self.weight_time_fit = 0.10
            self.weight_strategic_value = 0.10
        elif phase == 'middle':
            # Middle phase: Balance all factors
            self.weight_skill_alignment = 0.35
            self.weight_difficulty_fit = 0.20
            self.weight_org_fit = 0.15
            self.weight_time_fit = 0.15
            self.weight_strategic_value = 0.15
        elif phase == 'late':
            # Late phase: Focus on time fit and strategic value
            self.weight_skill_alignment = 0.25
            self.weight_difficulty_fit = 0.15
            self.weight_org_fit = 0.15
            self.weight_time_fit = 0.20
            self.weight_strategic_value = 0.25
        else:
            raise ValueError(f"Unknown GSoC phase: {phase}")
    
    def adjust_weights_for_student_goals(self, goal: str) -> None:
        """
        Adjust weights based on student's primary goal
        
        Args:
            goal: Student's primary goal ('skill_development', 'selection', or 'portfolio')
        """
        if goal == 'skill_development':
            # Focus on learning new skills
            self.weight_skill_alignment = 0.30
            self.weight_difficulty_fit = 0.35
            self.weight_org_fit = 0.10
            self.weight_time_fit = 0.15
            self.weight_strategic_value = 0.10
        elif goal == 'selection':
            # Focus on maximizing selection chances
            self.weight_skill_alignment = 0.30
            self.weight_difficulty_fit = 0.15
            self.weight_org_fit = 0.15
            self.weight_time_fit = 0.15
            self.weight_strategic_value = 0.25
        elif goal == 'portfolio':
            # Focus on building a diverse portfolio
            self.weight_skill_alignment = 0.25
            self.weight_difficulty_fit = 0.20
            self.weight_org_fit = 0.25
            self.weight_time_fit = 0.10
            self.weight_strategic_value = 0.20
        else:
            raise ValueError(f"Unknown student goal: {goal}")


# Example usage
if __name__ == "__main__":
    # This is just an example, not meant to be run directly
    
    # Create the matching algorithm with default weights
    matcher = MatchingAlgorithm()
    
    # Example student data
    student = {
        'student_id': '123',
        'github_username': 'student123',
        'display_name': 'Test Student',
        'available_hours_weekly': 15,
        'skills': [
            {'skill_name': 'Python', 'skill_type': 'language', 'proficiency': 'intermediate'},
            {'skill_name': 'JavaScript', 'skill_type': 'language', 'proficiency': 'beginner'},
            {'skill_name': 'React', 'skill_type': 'framework', 'proficiency': 'beginner'}
        ],
        'target_orgs': [
            {'org_name': 'Zulip', 'priority': 1},
            {'org_name': 'Mozilla', 'priority': 2}
        ],
        'gsoc_goals': 'I want to learn more about web development and contribute to open source projects.'
    }
    
    # Example issue data
    issue = {
        'issue_id': '456',
        'repo_full_name': 'zulip/zulip',
        'org_name': 'Zulip',
        'title': 'Fix button alignment in dark mode',
        'primary_language': 'JavaScript',
        'required_skills': ['JavaScript', 'CSS', 'React'],
        'difficulty_score': 3,
        'estimated_time_hours': 5,
        'labels': ['good first issue', 'frontend', 'bug'],
        'comments_count': 2
    }
    
    # Calculate match score
    match_result = matcher.calculate_match_score(student, issue)
    
    # Print result
    print(f"Match Score: {match_result['match_score']}")
    print(f"Match Category: {match_result['match_category']}")
    print("\nComponent Scores:")
    for component, score in match_result['component_scores'].items():
        print(f"  {component}: {score}")
    
    print("\nExplanation:")
    print(match_result['explanation'])
            
