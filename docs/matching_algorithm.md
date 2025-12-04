# GSoC Buddy Matching Algorithm

This document outlines the matching algorithm used by GSoC Buddy to connect students with appropriate GitHub issues.

## Matching Factors

The algorithm considers the following factors when calculating a match score between a student and an issue:

### 1. Skill Alignment (35%)

Measures how well the student's skills match the requirements of the issue.

- **Primary Language Match**: Does the student know the primary programming language required?
  - Perfect match: 100 points
  - Related language (same family): 60 points
  - Unrelated language: 0 points

- **Framework/Library Knowledge**: Does the student know the frameworks/libraries needed?
  - For each required framework:
    - Student knows it: 100 points
    - Student knows related technology: 50 points
    - Student doesn't know it: 0 points
  - Average the scores across all required frameworks

- **Proficiency Level**: How proficient is the student in the required skills?
  - Advanced: 100 points
  - Intermediate: 80 points
  - Beginner: 50 points
  - No experience: 0 points

- **Skill Alignment Score** = (Primary Language Match × 0.5) + (Framework Knowledge × 0.3) + (Proficiency Level × 0.2)

### 2. Difficulty Fit (20%)

Evaluates whether the issue's difficulty level is appropriate for the student.

- **Difficulty Gap**: Difference between issue difficulty and student's skill level
  - Perfect match (same level): 100 points
  - Slightly challenging (+1 level): 90 points
  - Moderately challenging (+2 levels): 70 points
  - Very challenging (+3 levels): 40 points
  - Too difficult (>+3 levels): 0 points
  - Too easy (-1 or more levels): 60 points

- **Learning Opportunity**: Does the issue help the student learn new skills they're interested in?
  - Strong learning opportunity: 100 points
  - Moderate learning opportunity: 70 points
  - Minimal learning opportunity: 30 points
  - No learning opportunity: 0 points

- **Difficulty Fit Score** = (Difficulty Gap × 0.7) + (Learning Opportunity × 0.3)

### 3. Organization Fit (15%)

Assesses how well the issue's organization aligns with the student's interests.

- **Target Organization**: Is this organization on the student's target list?
  - Top priority target: 100 points
  - Medium priority target: 80 points
  - Low priority target: 60 points
  - Not a target but in same domain: 40 points
  - Not a target or related: 0 points

- **Previous Contributions**: Has the student contributed to this organization before?
  - Multiple accepted contributions: 100 points
  - One accepted contribution: 80 points
  - Pending contributions: 50 points
  - No previous contributions: 0 points

- **Organization Fit Score** = (Target Organization × 0.6) + (Previous Contributions × 0.4)

### 4. Time Fit (15%)

Evaluates whether the student has enough time to complete the issue.

- **Time Requirement**: Does the student have enough available time?
  - Plenty of time (>2× estimated time): 100 points
  - Adequate time (1.5-2× estimated time): 90 points
  - Just enough time (1-1.5× estimated time): 70 points
  - Tight schedule (0.8-1× estimated time): 40 points
  - Not enough time (<0.8× estimated time): 0 points

- **Urgency**: How soon does the issue need to be addressed?
  - No urgency: 100 points
  - Low urgency: 80 points
  - Medium urgency: 60 points
  - High urgency: 40 points
  - Critical urgency: 0 points

- **Time Fit Score** = (Time Requirement × 0.8) + (Urgency × 0.2)

### 5. Strategic Value (15%)

Assesses the strategic value of the issue for GSoC selection.

- **Visibility**: How visible is this contribution likely to be?
  - High visibility (core feature/fix): 100 points
  - Medium visibility (important component): 70 points
  - Low visibility (minor component): 40 points
  - Minimal visibility (trivial fix): 10 points

- **Mentor Activity**: How active are mentors on this issue/repository?
  - Very active (responds within hours): 100 points
  - Active (responds within a day): 80 points
  - Moderately active (responds within days): 50 points
  - Inactive (rarely responds): 0 points

- **Competition Level**: How many other contributors are interested?
  - No competition: 100 points
  - Low competition (1-2 others): 80 points
  - Medium competition (3-5 others): 50 points
  - High competition (>5 others): 20 points

- **Strategic Value Score** = (Visibility × 0.4) + (Mentor Activity × 0.3) + (Competition Level × 0.3)

## Final Match Score Calculation

The final match score is a weighted average of the five factors:

**Match Score** = (Skill Alignment × 0.35) + (Difficulty Fit × 0.20) + (Organization Fit × 0.15) + (Time Fit × 0.15) + (Strategic Value × 0.15)

The result is a score from 0-100, where higher scores indicate better matches.

## Match Categories

Based on the final score, matches are categorized as:

- **Perfect Match (90-100)**: Exceptional fit across all factors
- **Strong Match (75-89)**: Very good fit with minor misalignments
- **Good Match (60-74)**: Good fit with some misalignments
- **Potential Match (40-59)**: Possible fit but significant misalignments
- **Poor Match (0-39)**: Not recommended

## Adjustable Weights

The weights for each factor can be adjusted based on:

1. **GSoC Timeline Phase**:
   - Early phase: Emphasize skill alignment and difficulty fit
   - Middle phase: Emphasize organization fit and strategic value
   - Late phase: Emphasize time fit and strategic value

2. **Student Goals**:
   - Skill development: Increase weight of difficulty fit and learning opportunity
   - Maximizing selection chances: Increase weight of strategic value
   - Building portfolio: Increase weight of visibility and organization fit

3. **Feedback Learning**:
   - Weights can be adjusted based on which factors correlate most strongly with successful contributions
