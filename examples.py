"""
Example demonstration of EduQuest functionality
This is for testing purposes - requires a valid API key in .env
"""

# This file demonstrates the expected workflow
# DO NOT RUN without setting up your .env file first!

EXAMPLE_INTERACTIONS = """
========================================
EXAMPLE 1: Creating a Study Plan
========================================

You: I have a Java exam in 3 days covering OOPs and Threads

EduQuest Manager: I understand you need to prepare for a Java exam in 3 days, 
focusing on Object-Oriented Programming and Threads. Let me create a structured 
study plan for you...

[Planner Agent activates]
- Uses Google Search to verify Java curriculum
- Creates 3-day breakdown
- Allocates ~3 hours per day
- Day 1: OOP Fundamentals (Classes, Objects, Inheritance)
- Day 2: Advanced OOP + Thread Basics
- Day 3: Thread Synchronization + Review

========================================
EXAMPLE 2: Taking a Quiz
========================================

You: Quiz me on Python decorators

EduQuest Manager: Great! I'll prepare a quiz on Python decorators. 
How many questions would you like?

You: 5

[Quiz Agent activates]

Question 1/5 (Easy):
QUESTION: What is the primary purpose of decorators in Python?
TYPE: Conceptual

You: To modify the behavior of functions or classes without changing their code

EVALUATION:
VERDICT: CORRECT
SCORE: 10/10 points
FEEDBACK: Excellent! You correctly identified that decorators are used to modify 
or enhance the behavior of functions or classes in a clean, readable way...

========================================
EXAMPLE 3: Mixed Workflow
========================================

You: Help me prepare for my Data Structures final in a week

[Manager routes to Planner]
Creates 7-day plan covering:
- Arrays and Linked Lists
- Stacks and Queues  
- Trees and Graphs
- Hash Tables
- Sorting and Searching

You: Quiz me on linked lists

[Manager routes to Quizzer]
Generates questions on:
- Singly vs Doubly linked lists
- Time complexity operations
- Implementation details
- Common algorithms

========================================
FEATURES DEMONSTRATED
========================================

✅ Multi-Agent Routing
   - Manager analyzes intent
   - Routes to specialist agents
   - Maintains conversation flow

✅ Google Search Grounding
   - Verifies curriculum topics
   - Ensures up-to-date information
   - Adds context to plans

✅ Session State Management
   - Tracks quiz progress
   - Stores study plans
   - Maintains conversation history

✅ Intelligent Question Generation
   - Progressive difficulty
   - Varied question types
   - Topic coverage

✅ Educational Feedback
   - Detailed explanations
   - Correct answers provided
   - Encouraging tone

========================================
"""


def show_examples():
    """Display example interactions"""
    print(EXAMPLE_INTERACTIONS)


if __name__ == "__main__":
    show_examples()
