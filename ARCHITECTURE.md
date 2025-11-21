# EduQuest Architecture Documentation

## System Overview

EduQuest is a multi-agent AI system designed using the **Manager-Worker Pattern** to provide specialized study assistance. This architecture document explains the design decisions, data flow, and component interactions.

## Architecture Pattern: Manager-Worker

### Why This Pattern?

**Problem**: A single AI agent trying to handle planning, search, teaching, and testing simultaneously produces mediocre results in all areas.

**Solution**: Separate concerns into specialized agents, each with focused responsibilities and optimized configurations.

### Benefits

1. **Specialization**: Each agent is optimized for its specific task
2. **Maintainability**: Easier to debug and improve individual components
3. **Scalability**: New agents can be added without affecting existing ones
4. **Quality**: Specialist agents produce better outputs than generalists
5. **Clarity**: Clear separation of concerns makes the system easier to understand

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                     (eduquest.py)                            │
│  - Terminal I/O with colored output                          │
│  - User input processing                                     │
│  - Response formatting                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   SESSION STATE MANAGER                      │
│                  (session_state.py)                          │
│  - QuizSession: Tracks active quiz state                    │
│  - StudyPlan: Stores created plans                          │
│  - ConversationHistory: Maintains context                   │
│  - Mode tracking: manager/planning/quizzing                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MANAGER AGENT                             │
│                 (manager_agent.py)                           │
│                                                              │
│  Responsibilities:                                           │
│  • Parse user input                                          │
│  • Determine user intent                                     │
│  • Extract relevant information                              │
│  • Route to appropriate specialist                           │
│  • Handle general queries                                    │
│                                                              │
│  Configuration:                                              │
│  • Model: Gemini 1.5 Flash                                   │
│  • Temperature: 0.3 (consistent routing)                     │
│  • Output: JSON with intent and extracted data              │
└───────────────┬──────────────────────┬──────────────────────┘
                │                      │
        ┌───────▼────────┐    ┌───────▼────────┐
        │                │    │                │
┌───────▼──────────┐  ┌──▼────▼──────────┐
│  PLANNER AGENT   │  │   QUIZ AGENT     │
│ (planner_agent)  │  │  (quiz_agent)    │
├──────────────────┤  ├──────────────────┤
│                  │  │                  │
│ Responsibilities │  │ Responsibilities │
│ • Schedule gen.  │  │ • Q generation   │
│ • Time alloc.    │  │ • Answer eval.   │
│ • Topic order    │  │ • Feedback       │
│ • Search verify  │  │ • Difficulty adj.│
│                  │  │                  │
│ Configuration:   │  │ Configuration:   │
│ • Gemini 1.5     │  │ • Gemini 1.5     │
│ • Temp: 0.5      │  │ • Temp: 0.7      │
│ • Google Search  │  │ • Higher variety │
│   Grounding: ON  │  │                  │
└──────────────────┘  └──────────────────┘
```

## Agent Specifications

### 1. Manager Agent

**File**: `agents/manager_agent.py`

**Purpose**: Primary interface and traffic controller

**Key Methods**:
- `analyze_intent(user_input, context)`: Analyzes input and determines routing
- `get_welcome_message()`: Initial user greeting
- `get_help_message()`: Help information

**Decision Logic**:
```python
if user mentions ("exam", "study plan", "prepare", "days"):
    route_to = PLANNER
elif user mentions ("quiz", "test", "practice", "questions"):
    route_to = QUIZZER
else:
    route_to = MANAGER (stay in current mode)
```

**Input**: Natural language user request
**Output**: JSON object with:
- `intent`: PLANNER | QUIZZER | MANAGER
- `extracted_info`: Dictionary of relevant data
- `user_message`: Conversational response

**Temperature**: 0.3 (low for consistent routing)

### 2. Planner Agent

**File**: `agents/planner_agent.py`

**Purpose**: Study schedule specialist with curriculum verification

**Key Methods**:
- `create_study_plan()`: Generates detailed study schedule
- `refine_plan()`: Modifies plan based on feedback
- `get_quick_tips()`: Provides study strategies

**Google Search Grounding**: 
- Enabled via `tools='google_search_retrieval'`
- Verifies current syllabus/curriculum
- Ensures topic accuracy and completeness

**Planning Algorithm**:
1. Parse user requirements (subject, topics, days)
2. Use Google Search to verify/expand topic list
3. Calculate time allocation per topic
4. Apply learning principles:
   - Start with fundamentals
   - Build to advanced concepts
   - Include spaced repetition
   - Reserve last day for review
5. Generate day-by-day breakdown

**Input**: 
- Subject name
- Topic list
- Days available
- Exam date (optional)

**Output**: Structured text plan with:
- Daily schedule
- Time breakdowns
- Learning objectives
- Study activities
- Review checkpoints

**Temperature**: 0.5 (balanced creativity and structure)

### 3. Quiz Agent

**File**: `agents/quiz_agent.py`

**Purpose**: Active recall and knowledge assessment specialist

**Key Methods**:
- `generate_question()`: Creates contextual questions
- `evaluate_answer()`: Grades and provides feedback
- `generate_quiz_intro()`: Session introduction
- `generate_quiz_summary()`: Performance summary
- `get_hint()`: Provides non-revealing hints

**Question Generation Strategy**:
1. Progressive difficulty:
   - First 30% of quiz: Easy questions
   - Middle 40%: Medium questions
   - Final 30%: Hard questions

2. Topic rotation:
   - Cycles through provided topics
   - Ensures balanced coverage

3. Question types:
   - Multiple Choice (MCQ)
   - Short Answer
   - Conceptual
   - Application-based

**Evaluation Criteria**:
- Exact matches: Full credit
- Partial correctness: Partial credit + explanation
- Alternative phrasings: Accepted if conceptually correct
- Incorrect: Full explanation with correct answer

**Input**:
- Topic(s) to cover
- Number of questions
- Current question context

**Output**:
- Formatted question with type
- Detailed evaluation with verdict
- Educational feedback
- Correct answer explanation

**Temperature**: 0.7 (higher for question variety) / 0.3 (lower for consistent grading)

## Data Flow

### Study Plan Creation Flow

```
User Input
    ↓
Manager Agent (analyzes intent)
    ↓
Extracts: subject, topics, days
    ↓
Planner Agent
    ↓
Google Search (verify curriculum)
    ↓
Generate day-by-day plan
    ↓
Store in SessionState
    ↓
Display to user
```

### Quiz Flow

```
User Input
    ↓
Manager Agent (analyzes intent)
    ↓
Extracts: topics, preferences
    ↓
Quiz Agent (initialize session)
    ↓
Generate Question 1
    ↓
User answers
    ↓
Evaluate answer
    ↓
Store in QuizSession
    ↓
Display feedback
    ↓
[Repeat for all questions]
    ↓
Generate summary
    ↓
End session
```

## State Management

### Session State (`session_state.py`)

**Global State Object**: `session`

**Components**:

1. **QuizSession**:
   ```python
   - topics: List[str]
   - questions: List[QuizQuestion]
   - current_question_index: int
   - score: int
   - is_active: bool
   ```

2. **StudyPlan**:
   ```python
   - subject: str
   - topics: List[str]
   - days_available: int
   - daily_schedule: List[Dict]
   ```

3. **ConversationHistory**:
   ```python
   - role: str (user/assistant)
   - content: str
   - timestamp: datetime
   ```

4. **Mode Tracking**:
   - `manager`: Default state
   - `planning`: During plan creation
   - `quizzing`: During active quiz

## Configuration (`config.py`)

**Environment Variables**:
- `GEMINI_API_KEY`: API authentication

**Model Settings**:
```python
MANAGER_MODEL = "gemini-1.5-flash"
PLANNER_MODEL = "gemini-1.5-flash"  
QUIZ_MODEL = "gemini-1.5-flash"

MANAGER_TEMPERATURE = 0.3  # Consistent routing
PLANNER_TEMPERATURE = 0.5  # Balanced
QUIZ_TEMPERATURE = 0.7     # Variety in questions
```

**Application Settings**:
```python
MAX_QUIZ_QUESTIONS = 10
DEFAULT_STUDY_HOURS_PER_DAY = 3
```

## Error Handling

### Graceful Degradation

1. **API Errors**:
   - Catch exceptions in each agent
   - Return fallback responses
   - Log errors for debugging
   - Inform user without crashing

2. **Invalid Input**:
   - Validate user input
   - Prompt for clarification
   - Provide defaults when reasonable

3. **Session Issues**:
   - Check session state before operations
   - Reset to safe state on errors
   - Preserve user progress when possible

## Security Considerations

1. **API Key Protection**:
   - Stored in `.env` file
   - Not committed to version control
   - Loaded at runtime only

2. **Input Validation**:
   - Sanitize user input
   - Limit response lengths
   - Prevent injection attacks

## Performance Optimizations

1. **Lazy Loading**:
   - Agents initialized only when needed
   - Questions generated on-demand

2. **Context Management**:
   - Limit conversation history to recent exchanges
   - Summarize long contexts

3. **Caching** (Future):
   - Cache common curriculum verifications
   - Store frequently used study plans

## Extensibility

### Adding New Agents

1. Create new agent file in `agents/`
2. Implement base agent interface
3. Add routing logic in Manager
4. Update session state if needed
5. Add configuration in `config.py`

**Example**: File Reader Agent
```python
class FileReaderAgent:
    def extract_content(self, file_path):
        # Extract text from PDF/DOCX
        pass
    
    def generate_plan_from_file(self, content):
        # Create plan from actual notes
        pass
```

### Adding New Features

- **Progress Tracking**: Extend SessionState with user profiles
- **Analytics**: Add performance tracking to QuizSession
- **Export**: Add methods to export plans/results

## Testing Strategy

1. **Unit Tests**:
   - Test each agent independently
   - Mock Gemini API responses
   - Validate state transitions

2. **Integration Tests**:
   - Test multi-agent workflows
   - Verify routing logic
   - Check state persistence

3. **User Acceptance Tests**:
   - Real-world scenarios
   - Example conversations
   - Error handling

## Future Architecture Improvements

1. **Agent Communication**:
   - Direct agent-to-agent communication
   - Shared context passing

2. **Persistent Storage**:
   - Database for user profiles
   - Long-term progress tracking

3. **Microservices**:
   - Separate API services per agent
   - Horizontal scaling

4. **Machine Learning**:
   - Personalized difficulty adjustment
   - Adaptive study plans based on performance

---

## Technology Stack Summary

- **Language**: Python 3.8+
- **AI Model**: Google Gemini 1.5 Flash
- **Libraries**:
  - `google-generativeai`: AI model API
  - `python-dotenv`: Configuration
  - `colorama`: Terminal formatting
  - Built-in: `dataclasses`, `datetime`, `json`

## Deployment Considerations

**Current**: Local CLI application

**Future Options**:
1. **Web Application**: Flask/FastAPI backend with React frontend
2. **Mobile App**: React Native with API backend
3. **Cloud Deployment**: Google Cloud Run or AWS Lambda
4. **Desktop App**: Electron wrapper

---

**Last Updated**: Based on initial implementation
**Version**: 1.0
**Author**: EduQuest Development Team
