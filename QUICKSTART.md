# EduQuest - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Get your Gemini API key from: https://makersuite.google.com/app/apikey
2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Step 3: Run EduQuest
```bash
python eduquest.py
```

---

## 🔧 Verify Setup

Run the setup checker:
```bash
python setup_check.py
```

This will verify:
- ✅ Python version (3.8+)
- ✅ All dependencies installed
- ✅ API key configured

---

## 💡 Example Usage

### Creating a Study Plan
```
You: I have a Java exam in 3 days covering OOPs and Threads

EduQuest will:
1. Analyze your requirements
2. Use Google Search to verify curriculum
3. Create a detailed 3-day study plan
```

### Taking a Quiz
```
You: Quiz me on Python decorators

EduQuest will:
1. Ask how many questions
2. Generate progressive difficulty questions
3. Grade your answers with detailed feedback
```

---

## 📋 Command Reference

### During Main Menu
- Type your study request or quiz request
- `help` - Show help information
- `exit` or `quit` - Exit EduQuest

### During Quiz
- Type your answer normally
- `hint` - Get a hint for the current question
- `skip` - Skip the current question
- `quit quiz` - End the quiz session

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists in the project root
- Verify the API key is correctly set
- Don't use quotes around the API key value

### Import errors
```bash
pip install --upgrade google-generativeai python-dotenv colorama
```

### Permission errors on Windows
Run PowerShell as Administrator or use:
```bash
python -m pip install -r requirements.txt
```

---

## 🎯 Tips for Best Results

1. **Be Specific**: Include subject, topics, and timeline
   - Good: "Java exam in 3 days on OOPs and Threads"
   - Vague: "Help me study"

2. **Follow the Plan**: The study plans are optimized for your timeline

3. **Practice Actively**: Use quizzes to test understanding, not just memorize

4. **Review Feedback**: Read the explanations, don't just check if you were right

---

## 📞 Need Help?

Check the main README.md for:
- Detailed architecture explanation
- Technical documentation
- Future features
- Contributing guidelines

---

**Happy Studying! 🎓**
