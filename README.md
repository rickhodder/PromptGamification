# Promptification 🎯

A gamified web application to help you master AI prompt engineering through practice, feedback, and structured learning.

## Features

- **Add & Review Prompts**: Create prompts and get expert AI feedback
- **Four AI Personas**: Choose from Beginner, Intermediate, Advanced, or Interviewer mentors
- **Progress Tracking**: Dashboard with analytics and statistics
- **Prompt Library**: Searchable knowledge base with tags and templates
- **Goal Setting**: Track daily and weekly prompt creation targets
- **Quality Ratings**: Six-dimensional quality assessment for each prompt

## Tech Stack

- **Framework**: Streamlit
- **Language**: Python 3.8+
- **Storage**: JSON (Phase 1)
- **AI Integration**: OpenAI/Anthropic APIs
- **Testing**: pytest with AI mocking
- **Visualization**: Plotly

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- OpenAI API key (or Anthropic API key)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rickhodder/PromptGamification.git
   cd PromptGamification
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   # OPENAI_API_KEY=your_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## Usage

### Adding a Prompt

1. Click **➕ Add Prompt** in the sidebar
2. Enter your prompt text and optional details
3. Add tags for organization
4. Click **Save Prompt**
5. Click **Get AI Review** to receive feedback

### Reviewing Prompts

- Select your preferred persona (Beginner, Intermediate, Advanced, Interviewer)
- Review the AI-suggested improvements
- Answer clarifying questions to refine the prompt
- Select and apply specific refinements
- View quality ratings across six dimensions

### Managing Your Library

1. Go to **📚 My Prompts**
2. Search by text or filter by tags
3. View templates only if needed
4. Sort by date or rating
5. Copy, edit, or delete prompts

### Tracking Progress

1. Visit **🏠 Dashboard**
2. View prompt creation trends over time
3. Monitor average quality ratings
4. See tag distribution
5. Track persona usage

## Project Structure

```
PromptGamification/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── app/
│   └── pages/
│       ├── add_prompt.py      # Add/Review prompt page
│       ├── my_prompts.py      # Prompt library page
│       └── dashboard.py       # Analytics dashboard
│
├── models/
│   └── __init__.py        # Pydantic data models
│
├── personas/
│   ├── __init__.py        # Persona factory
│   ├── base_persona.py    # Abstract base class
│   ├── beginner.py        # Beginner persona
│   ├── intermediate.py    # Intermediate persona
│   ├── advanced.py        # Advanced persona
│   └── interviewer.py     # Interviewer persona
│
├── utils/
│   └── storage.py         # JSON storage handler
│
├── tests/
│   ├── conftest.py        # Pytest fixtures
│   ├── test_models.py     # Model tests
│   ├── test_storage.py    # Storage tests
│   └── test_personas.py   # Persona tests
│
└── data/                  # JSON data storage (gitignored)
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_storage.py

# Run with verbose output
pytest -v
```

The test suite includes AI mocking to prevent API costs during testing.

## Configuration

### Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=your_key_here
DEFAULT_PERSONA=beginner
DEFAULT_DAILY_GOAL=2
```

### User Settings

Configure in the app:
- Default AI persona
- Daily prompt goal
- Weekly prompt goal

## Personas

### 🌱 Beginner
- Patient and encouraging
- Simple, non-technical explanations
- Foundational guidance
- Great for those new to prompt engineering

### 📚 Intermediate
- Balanced technical depth
- Assumes basic knowledge
- Introduces advanced concepts gradually
- Ideal for developing skills

### 🎓 Advanced
- Expert-level guidance
- Sophisticated technical analysis
- Challenging questions
- For experienced prompt engineers

### 💼 Interviewer
- Direct and critical
- Simulates interview pressure
- No hand-holding
- Perfect for job interview preparation

## Data Model

### Prompt Object
- Prompt text and description
- Reflection fields (what I learned, what went well)
- Tags and template flag
- Sharing preference
- Quality ratings (6 dimensions)
- Review history

### User Object
- User preferences (persona, goals)
- Statistics (totals, averages, streaks)
- Activity timestamps

## Development Roadmap

### Phase 1 - MVP ✅
- [x] Basic Streamlit structure
- [x] JSON storage
- [x] Add/Review prompts
- [x] Four AI personas
- [x] Tagging system
- [x] Dashboard
- [x] Prompt library
- [x] Test framework

### Phase 2 - Enhanced Features
- [ ] AI integration (OpenAI/Anthropic)
- [ ] Guided prompt creation
- [ ] Template system
- [ ] Advanced analytics
- [ ] Database migration
- [ ] AI-suggested tags

### Phase 3 - Interview Mode
- [ ] Interview practice scenarios
- [ ] Rating and assessment
- [ ] Performance tracking

## Contributing

This is a personal learning project. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational purposes.

## Acknowledgments

- Inspired by "Prompt Engineering for Generative AI" by O'Reilly
- Built with Streamlit
- Strategy pattern implementation for personas

## Support

For issues or questions, please open an issue on GitHub.

---

**Version**: 1.0.0 (MVP)  
**Status**: Active Development  
**Last Updated**: December 27, 2025
