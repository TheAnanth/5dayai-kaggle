"""
EduQuest - Main Application
Multi-Agent Study Assistant
"""
import sys
from typing import Optional
from colorama import init, Fore, Style

from agents.manager_agent import ManagerAgent
from agents.planner_agent import PlannerAgent
from agents.quiz_agent import QuizAgent
from session_state import session, StudyPlan
from config import MAX_QUIZ_QUESTIONS

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class EduQuest:
    """
    Main application class for EduQuest
    Orchestrates the multi-agent system
    """
    
    def __init__(self):
        print(f"{Fore.CYAN}Initializing EduQuest...{Style.RESET_ALL}")
        
        try:
            self.manager = ManagerAgent()
            self.planner = PlannerAgent()
            self.quizzer = QuizAgent()
            print(f"{Fore.GREEN}All agents initialized successfully{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}Error initializing agents: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please check your .env file and API key{Style.RESET_ALL}")
            sys.exit(1)
    
    def run(self):
        """Main application loop"""
        # Display welcome message
        print(f"{Fore.WHITE}{self.manager.get_welcome_message()}{Style.RESET_ALL}")
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n{Fore.GREEN}You: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    self._handle_exit()
                    break
                
                # Check for help
                if user_input.lower() in ['help', '?', 'help me']:
                    print(f"{Fore.CYAN}{self.manager.get_help_message()}{Style.RESET_ALL}")
                    continue
                
                # Check if in quiz mode
                if session.quiz_session and session.quiz_session.is_active:
                    self._handle_quiz_interaction(user_input)
                else:
                    # Route through manager
                    self._handle_manager_routing(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
                self._handle_exit()
                break
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Let's try again.{Style.RESET_ALL}")
    
    def _handle_manager_routing(self, user_input: str):
        """Handle routing through the manager agent"""
        # Build conversation context
        context = self._get_conversation_context()
        
        # Analyze intent
        print(f"{Fore.CYAN}Analyzing your request...{Style.RESET_ALL}")
        result = self.manager.analyze_intent(user_input, context)
        
        intent = result.get("intent", "MANAGER")
        extracted_info = result.get("extracted_info", {})
        user_message = result.get("user_message", "")
        
        # Display manager's understanding
        if user_message:
            print(f"\n{Fore.BLUE}EduQuest: {user_message}{Style.RESET_ALL}\n")
        
        # Route to appropriate agent
        if intent == "PLANNER":
            self._handle_planning(extracted_info)
        elif intent == "QUIZZER":
            self._handle_quiz_start(extracted_info)
        else:
            # Stay in manager mode - general conversation
            pass
        
        # Add to history
        session.add_to_history("user", user_input)
        session.add_to_history("assistant", user_message)
    
    def _handle_planning(self, info: dict):
        """Handle study plan creation"""
        subject = info.get("subject", "General Studies")
        topics = info.get("topics", [])
        days = info.get("days_available")
        exam_date = info.get("exam_date")
        context = info.get("additional_context", "")
        
        # Validate inputs
        if not days:
            print(f"{Fore.YELLOW}How many days do you have until your exam?{Style.RESET_ALL}")
            days_input = input(f"{Fore.GREEN}Days: {Style.RESET_ALL}").strip()
            try:
                days = int(days_input)
            except ValueError:
                print(f"{Fore.RED}Invalid number. Using default of 7 days.{Style.RESET_ALL}")
                days = 7
        
        if not topics:
            print(f"{Fore.YELLOW}What specific topics should I include? (comma-separated){Style.RESET_ALL}")
            topics_input = input(f"{Fore.GREEN}Topics: {Style.RESET_ALL}").strip()
            if topics_input:
                topics = [t.strip() for t in topics_input.split(',')]
        
        # Create the study plan
        print(f"\n{Fore.CYAN}Creating your personalized study plan...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}(Using Google Search to verify curriculum details...){Style.RESET_ALL}\n")
        
        plan_result = self.planner.create_study_plan(
            subject=subject,
            topics=topics,
            days_available=days,
            exam_date=exam_date,
            additional_context=context
        )
        
        if plan_result.get("success"):
            # Display the plan
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{plan_result['plan']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            
            # Store in session
            study_plan = StudyPlan(
                subject=subject,
                topics=topics,
                days_available=days,
                exam_date=exam_date
            )
            session.set_study_plan(study_plan)
            
            # Ask if they want to start quizzing
            print(f"\n{Fore.CYAN}Would you like to quiz yourself on any of these topics? (yes/no){Style.RESET_ALL}")
            quiz_response = input(f"{Fore.GREEN}Answer: {Style.RESET_ALL}").strip().lower()
            
            if quiz_response in ['yes', 'y', 'yeah', 'sure']:
                # Start quiz with the topics from the study plan
                self._handle_quiz_start({"topics": topics, "subject": subject})
            
        else:
            print(f"{Fore.RED}Error creating plan: {plan_result.get('message')}{Style.RESET_ALL}")
    
    def _handle_quiz_start(self, info: dict):
        """Handle quiz session initialization"""
        topics = info.get("topics", [])
        subject = info.get("subject", "")
        
        # If no specific topics, ask
        if not topics and subject:
            topics = [subject]
        
        if not topics:
            print(f"{Fore.YELLOW}What topics would you like to be quizzed on? (comma-separated){Style.RESET_ALL}")
            topics_input = input(f"{Fore.GREEN}Topics: {Style.RESET_ALL}").strip()
            if topics_input:
                topics = [t.strip() for t in topics_input.split(',')]
            else:
                print(f"{Fore.RED}No topics specified. Returning to main menu.{Style.RESET_ALL}")
                return
        
        # Ask for number of questions
        print(f"{Fore.CYAN}How many questions? (default: 5, max: {MAX_QUIZ_QUESTIONS}){Style.RESET_ALL}")
        num_input = input(f"{Fore.GREEN}Number: {Style.RESET_ALL}").strip()
        
        try:
            num_questions = int(num_input) if num_input else 5
            num_questions = min(num_questions, MAX_QUIZ_QUESTIONS)
        except ValueError:
            num_questions = 5
        
        # Start quiz session
        session.start_quiz(topics, num_questions)
        
        # Display intro
        print(f"{Fore.WHITE}{self.quizzer.generate_quiz_intro(topics, num_questions)}{Style.RESET_ALL}")
        
        # Generate and ask first question
        self._ask_next_question()
    
    def _handle_quiz_interaction(self, user_input: str):
        """Handle interaction during an active quiz"""
        # Check for special commands
        if user_input.lower() == 'hint':
            self._provide_hint()
            return
        elif user_input.lower() == 'skip':
            print(f"{Fore.YELLOW}Skipping this question...{Style.RESET_ALL}")
            self._record_skip()
            self._ask_next_question()
            return
        elif user_input.lower() == 'quit quiz':
            self._end_quiz()
            return
        
        # This is an answer to the current question
        self._evaluate_answer(user_input)
        
        # Check if quiz is complete
        if session.quiz_session.is_complete():
            self._end_quiz()
        else:
            self._ask_next_question()
    
    def _ask_next_question(self):
        """Generate and display the next quiz question"""
        quiz = session.quiz_session
        
        # Determine difficulty based on progress
        progress = quiz.current_question_index / quiz.total_questions
        if progress < 0.3:
            difficulty = "easy"
        elif progress < 0.7:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        # Pick a topic (rotate through topics)
        topic_index = quiz.current_question_index % len(quiz.topics)
        topic = quiz.topics[topic_index]
        
        # Get previously covered topics for variety
        previous_topics = [q.topic for q in quiz.questions]
        
        # Generate question
        print(f"\n{Fore.CYAN}Generating question...{Style.RESET_ALL}\n")
        
        q_result = self.quizzer.generate_question(
            topic=topic,
            difficulty=difficulty,
            question_number=quiz.current_question_index + 1,
            total_questions=quiz.total_questions,
            previous_topics=previous_topics if previous_topics else None
        )
        
        if q_result.get("success"):
            question_text = q_result["question"]
            
            # Add to session
            quiz.add_question(question_text, topic)
            
            # Display question
            print(f"{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{question_text}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}(Type 'hint' for a hint, 'skip' to skip, 'quit quiz' to end){Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Error generating question. Skipping...{Style.RESET_ALL}")
            quiz.current_question_index += 1
            if not quiz.is_complete():
                self._ask_next_question()
            else:
                self._end_quiz()
    
    def _evaluate_answer(self, user_answer: str):
        """Evaluate the user's answer"""
        quiz = session.quiz_session
        current_q = quiz.get_current_question()
        
        if not current_q:
            return
        
        print(f"\n{Fore.CYAN}Evaluating your answer...{Style.RESET_ALL}\n")
        
        eval_result = self.quizzer.evaluate_answer(
            question=current_q.question,
            user_answer=user_answer,
            topic=current_q.topic
        )
        
        if eval_result.get("success"):
            evaluation = eval_result["evaluation"]
            is_correct = eval_result["is_correct"]
            is_partial = eval_result["is_partial"]
            
            # Display evaluation
            if is_correct:
                print(f"{Fore.GREEN}CORRECT!{Style.RESET_ALL}\n")
            elif is_partial:
                print(f"{Fore.YELLOW}PARTIALLY CORRECT{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}INCORRECT{Style.RESET_ALL}\n")
            
            print(f"{Fore.WHITE}{evaluation}{Style.RESET_ALL}\n")
            
            # Record in session
            quiz.record_answer(
                user_answer=user_answer,
                is_correct=is_correct,
                correct_answer="See feedback above",
                feedback=evaluation
            )
        else:
            print(f"{Fore.RED}Error evaluating answer.{Style.RESET_ALL}")
            quiz.current_question_index += 1
    
    def _provide_hint(self):
        """Provide a hint for the current question"""
        quiz = session.quiz_session
        current_q = quiz.get_current_question()
        
        if current_q:
            hint = self.quizzer.get_hint(current_q.question, current_q.topic)
            print(f"\n{Fore.CYAN}{hint}{Style.RESET_ALL}\n")
    
    def _record_skip(self):
        """Record a skipped question"""
        quiz = session.quiz_session
        quiz.record_answer(
            user_answer="[Skipped]",
            is_correct=False,
            correct_answer="Question was skipped",
            feedback="You chose to skip this question."
        )
    
    def _end_quiz(self):
        """End the quiz session and show summary"""
        quiz = session.quiz_session
        
        if not quiz:
            return
        
        summary_info = quiz.get_summary()
        
        # Identify weak areas
        weak_topics = []
        topic_scores = {}
        
        for q in quiz.questions:
            if q.topic not in topic_scores:
                topic_scores[q.topic] = {"correct": 0, "total": 0}
            topic_scores[q.topic]["total"] += 1
            if q.is_correct:
                topic_scores[q.topic]["correct"] += 1
        
        for topic, scores in topic_scores.items():
            if scores["total"] > 0:
                percentage = (scores["correct"] / scores["total"]) * 100
                if percentage < 70:
                    weak_topics.append(topic)
        
        # Display summary
        summary = self.quizzer.generate_quiz_summary(
            score=quiz.score,
            total=len(quiz.questions),
            topics=quiz.topics,
            weak_areas=weak_topics if weak_topics else None
        )
        
        print(f"{Fore.WHITE}{summary}{Style.RESET_ALL}")
        
        # End session
        session.end_quiz()
    
    def _get_conversation_context(self) -> str:
        """Build conversation context from history"""
        if not session.conversation_history:
            return ""
        
        # Get last 5 exchanges
        recent = session.conversation_history[-10:]
        context_parts = []
        
        for msg in recent:
            role = msg["role"]
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def _handle_exit(self):
        """Handle application exit"""
        print(f"\n{Fore.CYAN}Thank you for using EduQuest! Keep up the great work!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Remember: Consistent study beats cramming every time!{Style.RESET_ALL}\n")


def main():
    """Main entry point"""
    try:
        app = EduQuest()
        app.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
