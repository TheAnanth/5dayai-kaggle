"""
Manager Agent - Primary Interface
Analyzes user input and routes to appropriate specialist agents
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, MANAGER_MODEL, MANAGER_TEMPERATURE


class ManagerAgent:
    """
    The Manager Agent is the primary interface that determines user intent
    and routes requests to either the Planner or Quiz agent.
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MANAGER_MODEL)
        
        self.system_prompt = """You are the Manager Agent for EduQuest, an intelligent study assistant.

Your role is to analyze user input and determine their intent. You have two specialist agents:
1. PLANNER - Creates structured study schedules and plans
2. QUIZZER - Conducts interactive quizzes and tests knowledge

ROUTING RULES:
- Route to PLANNER when user:
  * Mentions exam preparation, study schedule, or planning
  * Asks about organizing study time
  * Provides exam dates or timeframes
  * Wants to know what/how to study
  * Examples: "I have an exam in 3 days", "Help me prepare for Java", "Create a study plan"

- Route to QUIZZER when user:
  * Wants to practice or test knowledge
  * Asks for questions or quizzes
  * Wants to review specific topics actively
  * Says they're ready to study/practice
  * Examples: "Quiz me on OOPs", "I want to practice", "Test my knowledge"

- Stay in MANAGER mode when user:
  * Asks general questions about the system
  * Greets or has casual conversation
  * Asks for help or clarification

RESPONSE FORMAT:
Respond with a JSON object:
{
    "intent": "PLANNER" | "QUIZZER" | "MANAGER",
    "extracted_info": {
        "subject": "subject name if mentioned",
        "topics": ["list", "of", "topics"],
        "days_available": number or null,
        "exam_date": "date if mentioned" or null,
        "additional_context": "any other relevant info"
    },
    "user_message": "A friendly message to the user explaining what you understood"
}

Be conversational and helpful. Extract as much relevant information as possible from the user's input.
"""
    
    def analyze_intent(self, user_input: str, conversation_context: str = "") -> dict:
        """
        Analyze user input and determine routing intent
        
        Args:
            user_input: The user's message
            conversation_context: Previous conversation context
            
        Returns:
            Dictionary with intent, extracted info, and user message
        """
        prompt = f"""{self.system_prompt}

Previous Context: {conversation_context if conversation_context else "This is the start of the conversation"}

User Input: {user_input}

Analyze this input and respond with the JSON object as specified."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': MANAGER_TEMPERATURE,
                    'candidate_count': 1,
                }
            )
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            import json
            result = json.loads(response_text)
            
            return result
            
        except Exception as e:
            print(f"Error in Manager Agent: {e}")
            # Fallback response
            return {
                "intent": "MANAGER",
                "extracted_info": {},
                "user_message": "I'm having trouble understanding. Could you rephrase that?"
            }
    
    def get_welcome_message(self) -> str:
        """Get welcome message for new users"""
        return """
╔═══════════════════════════════════════════════════════════╗
║              Welcome to EduQuest!                         ║
╚═══════════════════════════════════════════════════════════╝

Hi! I'm your AI tutor designed to help u ace ur exams.

I can help you:
  - Create structured study plans based on your timeline
  - Quiz you on specific topics with real-time feedback
  - Track your progress and identify weak areas

Examples of what you can say:
  • "I have a Java exam in 3 days covering OOPs and Threads"
  • "Help me prepare for my Data Structures final"
  • "Quiz me on Python decorators and generators"
  • "I want to practice Algorithms"

What would you like to do today?
"""
    
    def get_help_message(self) -> str:
        """Get help information"""
        return """
EduQuest Help

CREATING STUDY PLANS:
  Tell me about your exam, subject, topics, and timeline.
  Example: "I have a Database exam in 5 days on SQL, Normalization, and Transactions"

TAKING QUIZZES:
  Ask to be quizzed on specific topics.
  Example: "Quiz me on Java OOPs concepts"

TIPS:
  • Be specific about topics and timeframes
  • You can switch between planning and quizzing anytime
  • Type 'exit' or 'quit' to end the session

What would you like help with?
"""
