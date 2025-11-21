"""
Session State Management for EduQuest
Tracks quiz progress, user history, and conversation context
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class QuizQuestion:
    """Represents a single quiz question"""
    question: str
    topic: str
    user_answer: Optional[str] = None
    correct_answer: Optional[str] = None
    feedback: Optional[str] = None
    is_correct: Optional[bool] = None


@dataclass
class QuizSession:
    """Manages a quiz session state"""
    topics: List[str] = field(default_factory=list)
    questions: List[QuizQuestion] = field(default_factory=list)
    current_question_index: int = 0
    score: int = 0
    total_questions: int = 0
    is_active: bool = False
    started_at: Optional[datetime] = None
    
    def start(self, topics: List[str], total_questions: int):
        """Initialize a new quiz session"""
        self.topics = topics
        self.total_questions = total_questions
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.is_active = True
        self.started_at = datetime.now()
    
    def add_question(self, question: str, topic: str):
        """Add a new question to the session"""
        self.questions.append(QuizQuestion(question=question, topic=topic))
    
    def record_answer(self, user_answer: str, is_correct: bool, 
                     correct_answer: str, feedback: str):
        """Record the user's answer and feedback"""
        if self.current_question_index < len(self.questions):
            q = self.questions[self.current_question_index]
            q.user_answer = user_answer
            q.is_correct = is_correct
            q.correct_answer = correct_answer
            q.feedback = feedback
            
            if is_correct:
                self.score += 1
            
            self.current_question_index += 1
    
    def get_current_question(self) -> Optional[QuizQuestion]:
        """Get the current question"""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def is_complete(self) -> bool:
        """Check if the quiz is complete"""
        return self.current_question_index >= self.total_questions
    
    def end(self):
        """End the quiz session"""
        self.is_active = False
    
    def get_summary(self) -> Dict:
        """Get a summary of the quiz session"""
        return {
            "total_questions": len(self.questions),
            "score": self.score,
            "percentage": (self.score / len(self.questions) * 100) if self.questions else 0,
            "topics_covered": self.topics,
            "duration": (datetime.now() - self.started_at) if self.started_at else None
        }


@dataclass
class StudyPlan:
    """Represents a study plan"""
    subject: str
    topics: List[str]
    days_available: int
    exam_date: Optional[str] = None
    daily_schedule: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class SessionState:
    """Global session state manager"""
    def __init__(self):
        self.quiz_session: Optional[QuizSession] = None
        self.current_study_plan: Optional[StudyPlan] = None
        self.conversation_history: List[Dict] = []
        self.current_mode: str = "manager"  # manager, planning, quizzing
    
    def start_quiz(self, topics: List[str], total_questions: int):
        """Start a new quiz session"""
        self.quiz_session = QuizSession()
        self.quiz_session.start(topics, total_questions)
        self.current_mode = "quizzing"
    
    def end_quiz(self):
        """End the current quiz session"""
        if self.quiz_session:
            self.quiz_session.end()
        self.current_mode = "manager"
    
    def set_study_plan(self, plan: StudyPlan):
        """Set the current study plan"""
        self.current_study_plan = plan
        self.current_mode = "planning"
    
    def reset_mode(self):
        """Reset to manager mode"""
        self.current_mode = "manager"
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })


# Global session instance
session = SessionState()
