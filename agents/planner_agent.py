"""
Planner Agent - Study Schedule Specialist
Creates structured study plans with Google Search grounding
"""
import google.generativeai as genai
from typing import List, Dict
from datetime import datetime, timedelta
from config import GEMINI_API_KEY, PLANNER_MODEL, PLANNER_TEMPERATURE, DEFAULT_STUDY_HOURS_PER_DAY


class PlannerAgent:
    """
    The Planner Agent specializes in creating structured study schedules.
    Uses Google Search grounding to verify syllabus topics and breaks down
    workload into manageable chunks based on available time.
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize the model (Google Search grounding requires different API in newer models)
        self.model = genai.GenerativeModel(PLANNER_MODEL)
        
        self.system_prompt = """You are the Planner Agent for EduQuest, an expert study scheduler.

Your role is to create detailed, actionable study plans that break down complex subjects 
into manageable daily tasks.

PLANNING PRINCIPLES:
1. Time Management: Divide total study time realistically across available days
2. Topic Prioritization: Start with fundamentals, build to advanced topics
3. Spaced Repetition: Include review sessions for previously covered material
4. Balanced Workload: Avoid overwhelming days; include breaks
5. Active Learning: Mix theory with practice problems/exercises

WHEN CREATING PLANS:
- Use Google Search to verify current syllabus/curriculum if topics are vague
- Break topics into subtopics with estimated time requirements
- Include buffer time for revision
- Add specific learning objectives for each day
- Suggest resources or practice methods

OUTPUT FORMAT:
Provide a structured day-by-day breakdown with:
- Day number and date
- Topics to cover
- Specific subtopics and concepts
- Estimated time per topic
- Learning activities (read, practice, solve problems, etc.)
- Review tasks

Be encouraging and realistic. Quality over quantity."""
    
    def create_study_plan(self, subject: str, topics: List[str], 
                         days_available: int, exam_date: str = None,
                         additional_context: str = "") -> Dict:
        """
        Create a comprehensive study plan
        
        Args:
            subject: The subject/course name
            topics: List of topics to cover
            days_available: Number of days until exam
            exam_date: Exam date if provided
            additional_context: Any additional user requirements
            
        Returns:
            Dictionary containing the structured study plan
        """
        # Calculate dates
        today = datetime.now()
        if exam_date:
            exam_date_str = exam_date
        else:
            exam_day = today + timedelta(days=days_available)
            exam_date_str = exam_day.strftime("%B %d, %Y")
        
        # Construct the planning prompt
        topics_str = ", ".join(topics) if topics else "general curriculum"
        
        prompt = f"""{self.system_prompt}

STUDY PLAN REQUEST:
Subject: {subject}
Topics to Cover: {topics_str}
Days Available: {days_available}
Exam Date: {exam_date_str}
Additional Context: {additional_context if additional_context else "None"}
Today's Date: {today.strftime("%B %d, %Y")}

TASK:
Create a comprehensive {days_available}-day study plan for {subject}.

1. First, verify the key topics and concepts typically covered in {subject} curriculum
2. Organize the topics ({topics_str}) into a logical learning sequence
3. Create a day-by-day schedule that:
   - Allocates approximately {DEFAULT_STUDY_HOURS_PER_DAY} hours per day
   - Progresses from foundational to advanced concepts
   - Includes practice and review sessions
   - Leaves the last day for comprehensive revision

4. For each day, specify:
   - Date and Day number
   - Main topics/subtopics
   - Learning objectives
   - Estimated time breakdown
   - Recommended activities (reading, practice problems, video tutorials, etc.)
   - Review checkpoints

Make the plan specific, actionable, and motivating. Include study tips and strategies.
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': PLANNER_TEMPERATURE,
                    'candidate_count': 1,
                }
            )
            
            plan_text = response.text
            
            return {
                "success": True,
                "subject": subject,
                "topics": topics,
                "days_available": days_available,
                "exam_date": exam_date_str,
                "plan": plan_text,
                "created_at": today.strftime("%B %d, %Y %H:%M")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an error creating your study plan. Please try again."
            }
    
    def refine_plan(self, original_plan: str, user_feedback: str) -> str:
        """
        Refine an existing study plan based on user feedback
        
        Args:
            original_plan: The original plan text
            user_feedback: User's requested changes
            
        Returns:
            Refined plan text
        """
        prompt = f"""You are refining a study plan based on user feedback.

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{user_feedback}

TASK:
Modify the study plan according to the user's feedback while maintaining the same 
structured format and quality. Explain what changes you made.
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': PLANNER_TEMPERATURE,
                }
            )
            
            return response.text
            
        except Exception as e:
            return f"Error refining plan: {str(e)}"
    
    def get_quick_tips(self, subject: str, days_available: int) -> str:
        """
        Get quick study tips for a subject
        
        Args:
            subject: The subject name
            days_available: Days until exam
            
        Returns:
            Study tips and strategies
        """
        urgency = "urgent" if days_available <= 3 else "moderate" if days_available <= 7 else "relaxed"
        
        prompt = f"""Provide 5-7 focused study tips for preparing for a {subject} exam in {days_available} days.
        
The timeline is {urgency}. Make tips specific, actionable, and prioritized.
Include both study strategies and test-taking advice.
Keep it concise and motivating."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={'temperature': 0.7}
            )
            return response.text
        except Exception as e:
            return f"Error generating tips: {str(e)}"
