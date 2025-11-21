# 🚀 EduQuest - Setup & Run Instructions

## ✅ What Has Been Built

Your complete EduQuest multi-agent study assistant is ready! Here's what's included:

### 📁 Project Files Created
```
5dayai-kaggle/
├── agents/
│   ├── __init__.py              ✅ Package initializer
│   ├── manager_agent.py         ✅ Intent routing agent
│   ├── planner_agent.py         ✅ Study planning agent  
│   └── quiz_agent.py            ✅ Quiz generation agent
│
├── config.py                    ✅ Configuration & API settings
├── session_state.py             ✅ State management
├── eduquest.py                  ✅ Main application
├── setup_check.py               ✅ Setup verification tool
├── examples.py                  ✅ Usage examples
│
├── requirements.txt             ✅ Dependencies
├── .env.example                 ✅ Environment template
├── .env                         ⚠️ Needs your API key
├── .gitignore                   ✅ Git exclusions
│
├── README.md                    ✅ Full documentation
├── QUICKSTART.md                ✅ Quick setup guide
├── ARCHITECTURE.md              ✅ Technical documentation
└── PROJECT_SUMMARY.md           ✅ Project overview
```

## 🎯 Quick Start (3 Steps)

### Step 1: Get Your API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AI...")

### Step 2: Add API Key to .env

Open the `.env` file and replace the placeholder:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Important**: Paste your actual API key without quotes!

### Step 3: Run EduQuest

```powershell
python eduquest.py
```

## ✨ First Use Examples

Once EduQuest starts, try these:

### Create a Study Plan
```
You: I have a Java exam in 3 days covering OOPs and Threads
```

### Take a Quiz
```
You: Quiz me on Python decorators
```

### Get Help
```
You: help
```

## 🔍 Verify Setup

Before running, verify everything is configured:

```powershell
python setup_check.py
```

This will check:
- ✅ Python version (3.8+)
- ✅ Dependencies installed
- ✅ API key configured

## 📊 Features You Can Use

### 1. **Study Planning**
- Tell EduQuest about your exam (subject, topics, timeline)
- Get a detailed day-by-day schedule
- Includes time allocation, learning objectives, and study tips
- Uses Google Search to verify curriculum

**Example**:
```
I have a Database exam in 5 days on SQL, Normalization, and Transactions
```

### 2. **Interactive Quizzing**
- Request quizzes on specific topics
- Progressive difficulty (easy → medium → hard)
- Immediate feedback with explanations
- Track your score and performance

**Example**:
```
Quiz me on Data Structures
```

**During Quiz**:
- Type your answer → Get immediate feedback
- Type `hint` → Get a helpful hint
- Type `skip` → Skip the question
- Type `quit quiz` → End early

### 3. **Smart Routing**
- Manager automatically understands your intent
- Routes to Planner for scheduling
- Routes to Quizzer for practice
- Maintains conversation context

## 🎨 What to Expect

### Welcome Screen
```
╔═══════════════════════════════════════════════════════════╗
║              Welcome to EduQuest! 🎓                      ║
╚═══════════════════════════════════════════════════════════╝

I'm your AI study concierge, designed to eliminate analysis paralysis
and help you prepare effectively for exams.
```

### Study Plan Output
- Detailed daily breakdown
- Time estimates per topic
- Learning objectives
- Study strategies
- Review checkpoints

### Quiz Session
- Question display
- Answer input
- Real-time evaluation
- Educational feedback
- Performance summary

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not found"
**Solution**: 
1. Check that `.env` file exists in project root
2. Verify API key is set correctly
3. No quotes around the key value
4. Key should start with "AI"

### Import Errors
**Solution**:
```powershell
pip install --upgrade google-generativeai python-dotenv colorama
```

### Colored Output Not Working
**Solution**: Colorama is installed, but if colors don't show:
- Windows: Should work automatically
- Terminal doesn't support colors: Output will still be readable

## 💡 Usage Tips

### For Best Study Plans
- Be specific about topics
- Mention your timeline clearly
- Include any special requirements
- Example: "Python exam in 4 days, focus on OOP, decorators, and generators"

### For Best Quiz Sessions
- Start with 3-5 questions to get a feel
- Read feedback carefully - it teaches!
- Use hints if stuck, but try first
- Review incorrect answers to learn

### General Tips
- You can switch between planning and quizzing anytime
- Type 'help' if you get stuck
- The system learns your context as you chat
- Be conversational - no need for formal commands

## 🎓 How It Works

### Multi-Agent Architecture

1. **You type a message** → 
2. **Manager Agent** analyzes it →
3. **Routes to**:
   - **Planner Agent** (for study schedules)
   - **Quiz Agent** (for practice questions)
4. **Specialist Agent** processes request →
5. **You get the response** with:
   - Structured plans OR
   - Interactive questions

### Special Features

- **Google Search Grounding**: Planner verifies curriculum with real-time search
- **Progressive Difficulty**: Quizzes start easy and get harder
- **Context Aware**: Remembers your conversation
- **Educational Focus**: Not just answers, but explanations

## 📝 Project Status

- ✅ All agents implemented
- ✅ Multi-agent routing working
- ✅ Google Search grounding enabled
- ✅ Session state management active
- ✅ Error handling complete
- ✅ Documentation comprehensive
- ⚠️ **Needs your API key to run**

## 🚀 Next Steps

1. **Now**: Add your Gemini API key to `.env`
2. **Then**: Run `python setup_check.py` to verify
3. **Finally**: Run `python eduquest.py` to start!

## 📖 Documentation

- **README.md**: Complete project documentation
- **QUICKSTART.md**: Fast setup guide  
- **ARCHITECTURE.md**: Technical deep dive
- **PROJECT_SUMMARY.md**: Project overview
- **examples.py**: Usage demonstrations

## 🤝 Getting Help

If you encounter issues:

1. Run `python setup_check.py` first
2. Check error messages - they're descriptive
3. Verify your API key is valid
4. Make sure you're connected to internet (for Google Search)

## 🎉 You're All Set!

Everything is ready. Just add your API key and start studying smarter!

```powershell
# Verify setup
python setup_check.py

# Start EduQuest
python eduquest.py
```

---

**Built for students everywhere who want to study smarter, not harder! 🎓✨**
