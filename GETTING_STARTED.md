# Getting Started with Promptification

## Installation & Setup

### Step 1: Clone and Navigate
```bash
cd d:\GitHub\PromptGamification
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 5: Run Setup Verification
```bash
python setup.py
```

### Step 6: Launch the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## First Time Usage

### 1. Explore the Dashboard
- View your progress metrics (starts at 0)
- Set your daily goals (default: 2 prompts/day)
- Familiarize yourself with the interface

### 2. Create Your First Prompt
1. Click **➕ Add Prompt** in the sidebar
2. Enter a prompt you've used or want to test
3. Add a description (optional but recommended)
4. Reflect on what you learned
5. Add tags for organization
6. Click **Save Prompt**

### 3. Get AI Feedback
1. After saving, click **Get AI Review**
2. Review the AI-suggested improvements
3. Read the clarifying questions
4. Select refinements to apply
5. View quality ratings

### 4. Build Your Library
- Add more prompts over time
- Tag them consistently
- Mark useful ones as templates
- Search and filter as needed

### 5. Track Your Progress
- Return to Dashboard regularly
- Monitor your improvement over time
- Adjust goals as needed
- Try different personas

---

## Understanding Personas

### When to Use Each Persona

**🌱 Beginner** - Use when:
- You're new to prompt engineering
- You want simple, clear explanations
- You need foundational concepts
- You prefer encouraging feedback

**📚 Intermediate** - Use when:
- You understand basic prompting
- You want moderate technical depth
- You're ready for challenges
- You want to learn patterns

**🎓 Advanced** - Use when:
- You're experienced with prompts
- You want expert-level analysis
- You need sophisticated techniques
- You welcome tough questions

**💼 Interviewer** - Use when:
- Preparing for job interviews
- You want direct, critical feedback
- You need pressure simulation
- You want to identify weaknesses

---

## Tips for Success

### Writing Better Prompts
1. Be specific about what you want
2. Include context and examples
3. Define the output format
4. Consider edge cases
5. Think about security (prompt injection)

### Using Tags Effectively
- Use consistent naming (lowercase)
- Include: purpose, domain, difficulty
- Examples: `python`, `code-gen`, `beginner`

### Getting Good Feedback
- Fill out reflection fields honestly
- Answer clarifying questions thoughtfully
- Apply refinements and re-review
- Compare original vs improved prompts

### Building Your Knowledge Base
- Create prompts regularly
- Review and refine old prompts
- Mark successful patterns as templates
- Organize with meaningful tags

---

## Troubleshooting

### App Won't Start
- Verify Python 3.8+ is installed: `python --version`
- Check all dependencies installed: `pip list`
- Run setup script: `python setup.py`

### Import Errors
- Make sure you're in the project root directory
- Verify all `__init__.py` files exist
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

### No AI Reviews (Phase 1)
- AI integration is planned for Phase 2
- Currently shows placeholder feedback
- Use it to learn the interface and workflow

### Data Not Persisting
- Check `data/` directory exists
- Verify write permissions
- Look for JSON files in `data/`

---

## Development Workflow

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_storage.py -v
```

### Project Structure
```
app.py              # Main entry point
├── app/pages/      # UI pages
├── models/         # Data models
├── personas/       # AI personas (Strategy pattern)
├── utils/          # Utilities (storage, etc.)
├── tests/          # Test suite
└── data/           # JSON storage (gitignored)
```

### Making Changes
1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run test suite
5. Test manually in UI
6. Commit with clear message

---

## Next Steps

### After MVP Setup
1. Integrate real AI APIs (OpenAI/Anthropic)
2. Implement guided prompt creation (Use Case 2)
3. Add advanced analytics
4. Build interview practice mode
5. Migrate to database

### Contributing
- Check open issues
- Follow code style
- Add tests for new features
- Update documentation

---

## Support

**Issues?** Open an issue on GitHub
**Questions?** Check the README.md
**Updates?** Watch the repository

Happy Prompting! 🎯
