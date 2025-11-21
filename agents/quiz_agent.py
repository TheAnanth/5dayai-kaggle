"""
Quiz Agent - Active Recall Specialist
Generates questions, grades answers, and provides feedback
"""
import google.generativeai as genai
from typing import List, Dict, Optional
from config import GEMINI_API_KEY, QUIZ_MODEL, QUIZ_TEMPERATURE, MAX_QUIZ_QUESTIONS


class QuizAgent:
    """
    The Quiz Agent specializes in active recall and knowledge testing.
    Generates contextual questions, evaluates answers, and provides
    detailed feedback with corrections.
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(QUIZ_MODEL)
        
        self.system_prompt = """You are the Quiz Agent for EduQuest, an expert educational assessor.

Your role is to conduct interactive quizzes that help students actively recall and test their knowledge.

QUIZ PRINCIPLES:
1. Progressive Difficulty: Start with fundamental questions, increase complexity
2. Varied Question Types: Mix MCQ, short answer, conceptual, and application questions
3. Clear Grading: Evaluate answers fairly with specific feedback
4. Educational Feedback: Explain WHY an answer is correct/incorrect
5. Encouraging Tone: Motivate learning, not just testing

QUESTION GENERATION:
- Focus on understanding, not just memorization
- Include real-world applications when relevant
- Make MCQs with plausible distractors
- Ask "why" and "how" questions, not just "what"
- Cover different aspects of the topic

ANSWER EVALUATION:
- Be fair but thorough
- Accept correct answers phrased differently
- Give partial credit for partially correct answers
- Highlight what was good and what needs improvement
- Provide the correct/complete answer with explanation

Keep responses focused and educational."""
    
    def generate_question(self, topic: str, difficulty: str = "medium", 
                         question_number: int = 1, total_questions: int = 10,
                         previous_topics: List[str] = None) -> Dict:
        """
        Generate a single quiz question
        
        Args:
            topic: The topic/subject area
            difficulty: easy, medium, or hard
            question_number: Current question number
            total_questions: Total questions in quiz
            previous_topics: Previously covered topics for variety
            
        Returns:
            Dictionary with question details
        """
        previous_context = ""
        if previous_topics:
            previous_context = f"\nPreviously asked about: {', '.join(previous_topics)}"
        
        prompt = f"""{self.system_prompt}

QUESTION GENERATION REQUEST:
Topic: {topic}
Difficulty Level: {difficulty}
Question {question_number} of {total_questions}{previous_context}

CRITICAL CONSTRAINTS:
- ONLY test knowledge of {topic}
- DO NOT require knowledge of other topics or operations
- If topic is "addition", ONLY use addition - no multiplication, division, or other operations
- Questions must be solvable using ONLY the stated topic
- Keep questions focused and simple for the difficulty level

TASK:
Generate ONE high-quality question about {topic} at {difficulty} difficulty level.

FORMAT YOUR RESPONSE EXACTLY AS:
QUESTION: [Your question here]
TYPE: [MCQ/Short Answer/Conceptual/Application]
DIFFICULTY: {difficulty}
[If MCQ, include options A, B, C, D on separate lines]

Make the question clear, specific, and educational.
For MCQs, ensure all options are plausible.
REMEMBER: Only test {topic} - no other mathematical operations or concepts!
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': QUIZ_TEMPERATURE,
                    'candidate_count': 1,
                }
            )
            
            question_text = response.text.strip()
            
            return {
                "success": True,
                "question": question_text,
                "topic": topic,
                "difficulty": difficulty,
                "number": question_number
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": f"Error generating question: {str(e)}"
            }
    
    def evaluate_answer(self, question: str, user_answer: str, 
                       topic: str, question_type: str = "general") -> Dict:
        """
        Evaluate a user's answer to a quiz question
        
        Args:
            question: The question that was asked
            user_answer: The user's response
            topic: The topic being tested
            question_type: Type of question (MCQ, Short Answer, etc.)
            
        Returns:
            Dictionary with evaluation results
        """
        prompt = f"""{self.system_prompt}

ANSWER EVALUATION REQUEST:
Topic: {topic}
Question Type: {question_type}

QUESTION:
{question}

STUDENT'S ANSWER:
{user_answer}

TASK:
Evaluate this answer thoroughly and provide feedback.

FORMAT YOUR RESPONSE EXACTLY AS:
VERDICT: [CORRECT/PARTIALLY CORRECT/INCORRECT]
SCORE: [X/10 points]
CORRECT ANSWER: [The complete correct answer]
FEEDBACK: [Detailed explanation of what was right/wrong and why]
KEY CONCEPTS: [Main concepts the student should understand]

Be fair in evaluation. Accept alternative correct phrasings.
If partially correct, explain what was right and what was missing.
Make feedback educational and encouraging.
"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,  # Lower temperature for consistent evaluation
                    'candidate_count': 1,
                }
            )
            
            evaluation_text = response.text.strip()
            
            # Parse the verdict
            is_correct = "VERDICT: CORRECT" in evaluation_text
            is_partial = "PARTIALLY CORRECT" in evaluation_text
            
            return {
                "success": True,
                "is_correct": is_correct,
                "is_partial": is_partial,
                "evaluation": evaluation_text,
                "topic": topic
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "evaluation": f"Error evaluating answer: {str(e)}"
            }
    
    def generate_quiz_intro(self, topics: List[str], num_questions: int) -> str:
        """
        Generate an introduction for the quiz session
        
        Args:
            topics: List of topics to be covered
            num_questions: Number of questions in the quiz
            
        Returns:
            Introduction text
        """
        topics_str = ", ".join(topics)
        
        return f"""
╔═══════════════════════════════════════════════════════════╗
║                 Quiz Session Starting!                    ║
╚═══════════════════════════════════════════════════════════╝

Topics: {topics_str}
Questions: {num_questions}

INSTRUCTIONS:
• Read each question carefully
• Type your answer and press Enter
• You'll receive immediate feedback
• Try to explain your reasoning when possible
• Learn from the explanations provided

Ready? Let's begin!
"""
    
    def generate_quiz_summary(self, score: int, total: int, 
                             topics: List[str], weak_areas: List[str] = None) -> str:
        """
        Generate a summary of quiz performance
        
        Args:
            score: Number of correct answers
            total: Total number of questions
            topics: Topics covered
            weak_areas: Areas where student struggled
            
        Returns:
            Summary text
        """
        percentage = (score / total * 100) if total > 0 else 0
        
        # Determine performance level
        if percentage >= 90:
            performance = "Excellent!"
            message = "You have a strong grasp of these topics!"
        elif percentage >= 75:
            performance = "Good Job!"
            message = "You're doing well, just a few areas to review."
        elif percentage >= 60:
            performance = "Fair"
            message = "You understand the basics, but need more practice."
        else:
            performance = "Needs Improvement"
            message = "Don't worry! Review the concepts and try again."
        
        summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                Quiz Complete!                             ║
╚═══════════════════════════════════════════════════════════╝

SCORE: {score}/{total} ({percentage:.1f}%)
PERFORMANCE: {performance}

{message}

Topics Covered: {", ".join(topics)}
"""
        
        if weak_areas:
            summary += f"\nAreas to Review: {', '.join(weak_areas)}\n"
        
        summary += "\nWhat would you like to do next?\n• Take another quiz\n• Create a study plan\n• Exit\n"
        
        return summary
    
    def get_hint(self, question: str, topic: str) -> str:
        """
        Generate a hint for a question without giving away the answer
        
        Args:
            question: The question
            topic: The topic
            
        Returns:
            Hint text
        """
        prompt = f"""Provide a helpful hint for this question without revealing the answer:

Question: {question}
Topic: {topic}

Give a hint that guides thinking without giving away the answer directly.
Keep it brief (1-2 sentences)."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={'temperature': 0.5}
            )
            return f"Hint: {response.text.strip()}"
        except Exception as e:
            return "Hint: Think about the fundamental concepts of this topic."
