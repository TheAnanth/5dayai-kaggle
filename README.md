# EduQuest 🎓

**An AI-Powered Multi-Agent Study Assistant**

EduQuest is a sophisticated multi-agent application designed to solve the "analysis paralysis" problem students face when preparing for exams. Instead of wasting time worrying about what to study, EduQuest acts as both a study manager and an interactive tutor.

## 🎯 Problem Statement

Students often spend more time stressing about exam preparation than actually studying. They struggle with:
- Not knowing where to start
- Inefficient time management
- Lack of structured study plans
- No way to actively test their knowledge
- Overwhelming amounts of material

EduQuest takes this cognitive load off the user by providing intelligent organization and active learning support.

## ✨ What It Does

EduQuest functions as an **interactive study concierge** that:

1. **📅 Creates Personalized Study Plans**: Enter a prompt like *"I have a Java exam in 3 days covering OOPs and Threads"* and get a detailed day-by-day schedule
2. **❓ Conducts Interactive Quizzes**: Switch to quiz mode to actively test your knowledge with real-time grading and explanations
3. **🧠 Manages Your Learning**: Automatically routes you to the right mode based on your needs

### Example Interactions

```
You: I have a Java exam in 3 days covering OOPs and Threads

EduQuest: I understand you need to prepare for a Java exam in 3 days, 
focusing on Object-Oriented Programming and Threads. Let me create 
a structured study plan for you...

[Generates detailed 3-day plan with daily topics, time allocation, 
and learning activities]
```

```
You: Quiz me on Python decorators

EduQuest: Great! Let's test your knowledge on Python decorators.
How many questions would you like? (default: 5)

[Conducts interactive quiz with immediate feedback]
```

## 🏗️ Technical Architecture

EduQuest uses a **Manager-Worker multi-agent architecture** powered by Google's Gemini API. This design separates concerns to provide specialized, focused functionality.

### Multi-Agent System

```
┌─────────────────────────────────────────────────────┐
│                  MANAGER AGENT                      │
│  (Primary Interface & Intent Router)                │
│  - Analyzes user input                              │
│  - Determines intent                                │
│  - Routes to specialist agents                      │
└──────────────┬────────────────────┬─────────────────┘
               │                    │
       ┌───────▼────────┐   ┌──────▼──────────┐
       │ PLANNER AGENT  │   │  QUIZ AGENT     │
       │                │   │                 │
       │ • Schedule     │   │ • Questions     │
       │ • Organization │   │ • Grading       │
       │ • Google Search│   │ • Feedback      │
       │   Grounding    │   │ • Active Recall │
       └────────────────┘   └─────────────────┘
```

### The Three Agents

#### 1. **Manager Agent** 🎯
- **Role**: Primary interface and traffic controller
- **Responsibilities**:
  - Analyzes user input to determine intent
  - Routes requests to Planner or Quizzer
  - Maintains conversation flow
  - Handles general queries
- **Technology**: Gemini 1.5 Flash with low temperature for consistent routing

#### 2. **Planner Agent** 📚
- **Role**: Study schedule specialist
- **Responsibilities**:
  - Creates detailed day-by-day study plans
  - Uses Google Search grounding to verify curriculum details
  - Breaks down topics into manageable chunks
  - Allocates time based on days available
  - Includes review sessions and breaks
- **Technology**: Gemini 1.5 Flash with Google Search grounding enabled
- **Key Features**:
  - Time-based workload distribution
  - Topic prioritization (fundamentals → advanced)
  - Spaced repetition principles
  - Realistic daily schedules

#### 3. **Quiz Agent** 🧠
- **Role**: Active recall and knowledge testing specialist
- **Responsibilities**:
  - Generates contextual questions based on topics
  - Evaluates answers with detailed feedback
  - Explains mistakes and provides correct answers
  - Tracks quiz session state
  - Identifies weak areas
- **Technology**: Gemini 1.5 Flash with higher temperature for variety
- **Key Features**:
  - Progressive difficulty (easy → medium → hard)
  - Multiple question types (MCQ, conceptual, application)
  - Fair grading with partial credit
  - Educational feedback (not just right/wrong)

### Session State Management

The application maintains persistent state across interactions:
- **QuizSession**: Tracks current quiz, questions, answers, score
- **StudyPlan**: Stores created study plans
- **ConversationHistory**: Maintains context for intelligent responses

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/TheAnanth/5dayai-kaggle.git
   cd 5dayai-kaggle
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run EduQuest**
   ```bash
   python eduquest.py
   ```

## 📖 Usage Guide

### Creating Study Plans

Simply tell EduQuest about your exam:

```
You: I have a Database Management exam in 5 days covering SQL, 
Normalization, and Transactions
```

EduQuest will:
1. Verify the curriculum using Google Search
2. Create a day-by-day breakdown
3. Allocate time for each topic
4. Include review sessions
5. Provide study tips and resources

### Taking Quizzes

Request a quiz on specific topics:

```
You: Quiz me on Data Structures and Algorithms
```

During the quiz:
- Type your answer and press Enter
- Get immediate feedback with explanations
- Type `hint` for a helpful hint
- Type `skip` to skip a question
- Type `quit quiz` to end early

### Special Commands

- `help` - Show help information
- `hint` - Get a hint (during quiz)
- `skip` - Skip current question (during quiz)
- `quit quiz` - End quiz session
- `exit` / `quit` - Exit EduQuest

## 💡 Why Multi-Agent Architecture?

**The Problem with Single-Prompt Systems:**
A single AI model trying to be a scheduler, search engine, and teacher simultaneously often gets confused and provides mediocre results in all areas.

**The Multi-Agent Solution:**
By separating concerns:
- The **Planner** can focus entirely on logic, time management, and curriculum organization
- The **Quizzer** can specialize in educational content, question generation, and assessment
- The **Manager** ensures smooth orchestration without getting bogged down in specialist tasks

This results in:
- ✅ Better quality outputs from each agent
- ✅ Clearer separation of concerns
- ✅ Easier to debug and improve individual components
- ✅ More natural conversation flow
- ✅ Scalable for adding new agents (e.g., File Reader)

## 🔮 Future Improvements

### Planned Features

1. **File Reader Agent** 📄
   - Upload lecture notes, PDFs, or textbooks
   - Generate plans and quizzes based on YOUR actual class material
   - Extract key concepts automatically

2. **Progress Tracker** 📊
   - Persistent user profiles
   - Long-term progress tracking
   - Performance analytics
   - Weak area identification

3. **Flashcard Generator** 🗂️
   - Auto-generate flashcards from topics
   - Spaced repetition system
   - Export to Anki format

4. **Study Group Mode** 👥
   - Collaborative study sessions
   - Shared quizzes and plans
   - Peer comparison

5. **Voice Interface** 🎤
   - Voice-based quizzing
   - Hands-free study sessions

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **AI Model**: Google Gemini 1.5 Flash
- **Key Libraries**:
  - `google-generativeai` - Gemini API client
  - `python-dotenv` - Environment configuration
  - `colorama` - Cross-platform colored terminal output
- **Architecture**: Multi-agent system with Manager-Worker pattern
- **State Management**: Custom session state with dataclasses

## 📁 Project Structure

```
5dayai-kaggle/
├── agents/
│   ├── __init__.py
│   ├── manager_agent.py    # Intent routing and conversation management
│   ├── planner_agent.py    # Study plan generation
│   └── quiz_agent.py       # Quiz generation and evaluation
├── config.py               # Configuration and API settings
├── session_state.py        # State management classes
├── eduquest.py            # Main application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore
└── README.md
```

## 🎓 Design Principles

1. **User-Centric**: Focus on solving real student problems
2. **Intelligent Routing**: Right agent for the right task
3. **Educational Quality**: Not just answers, but learning
4. **Time-Aware**: Realistic scheduling based on actual available time
5. **Active Learning**: Emphasis on recall and practice, not passive reading
6. **Conversational**: Natural language interaction
7. **Encouraging**: Positive reinforcement and motivation

## 🤝 Contributing

This is a capstone project, but suggestions and improvements are welcome! 

## 📝 License

This project is part of an educational capstone and is provided as-is for learning purposes.

## 🙏 Acknowledgments

- Built with Google's Gemini API
- Inspired by the challenges students face during exam preparation
- Designed for the 5-Day AI Capstone

---

**Built with ❤️ for students everywhere who want to study smarter, not harder.**

## 📞 Support

If you encounter issues:
1. Ensure your `.env` file has a valid Gemini API key
2. Check that all dependencies are installed
3. Verify Python version is 3.8+
4. Review error messages for specific guidance

---

### Quick Start Example

```bash
# Install
pip install -r requirements.txt

# Configure
echo "GEMINI_API_KEY=your_key_here" > .env

# Run
python eduquest.py
```

Then try:
```
You: I have a Python exam tomorrow on functions, classes, and decorators
```

Happy studying! 🚀
