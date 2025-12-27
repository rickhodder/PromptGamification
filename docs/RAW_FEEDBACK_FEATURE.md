# Raw Feedback Feature

## Overview
The application now preserves both **raw** (unprocessed) and **processed** (cleaned/validated) AI feedback. This provides transparency into what the AI originally returned versus what was cleaned and validated by the ResponseProcessor.

## New Fields in Prompt Model

Added 6 new optional fields to the `Prompt` model in [models/__init__.py](models/__init__.py):

```python
# Raw AI responses (before processing)
raw_questions: Optional[List[str]] = None
raw_refinements: Optional[List[str]] = None
raw_feedback: Optional[str] = None

# Processed AI responses (after cleaning/validation)
processed_questions: Optional[List[str]] = None
processed_refinements: Optional[List[str]] = None
processed_feedback: Optional[str] = None
```

## How It Works

### 1. ResponseProcessor Updates
The `ResponseProcessor.process_review_response()` method in [utils/response_processor.py](utils/response_processor.py) now:
- Preserves raw versions before any processing
- Returns both raw and processed versions in the response dictionary
- Maintains backward compatibility (standard keys still contain processed versions)

### 2. Persona Integration
All 4 personas ([beginner.py](personas/beginner.py), [intermediate.py](personas/intermediate.py), [advanced.py](personas/advanced.py), [interviewer.py](personas/interviewer.py)) now:
- Store raw feedback from AI responses
- Store processed feedback after validation/cleaning
- Populate all 6 new fields in the Prompt object

### 3. UI Display
The Add Prompt page ([app/pages/add_prompt.py](app/pages/add_prompt.py)) now shows:
- **Tabbed interface** for Questions, Refinements, and Feedback sections
- **"📝 Processed Feedback" tab**: Shows the cleaned, validated feedback
- **"🔍 Raw AI Response" tab**: Shows the original AI output before processing
- **Debug expander**: Shows full raw JSON response for troubleshooting

### 4. Storage Backward Compatibility
The storage layer ([utils/storage.py](utils/storage.py)) now:
- Automatically adds null values for new fields when loading old prompts
- Preserves all 6 new fields when saving prompts
- Ensures existing data files work without migration

## Benefits

1. **Transparency**: Users can see exactly what the AI returned
2. **Debugging**: Developers can identify processing issues
3. **Trust**: Users understand what cleaning/validation was applied
4. **Comparison**: Side-by-side view of raw vs processed feedback

## Testing

Added comprehensive test suite in [tests/test_raw_feedback.py](tests/test_raw_feedback.py):
- ✅ Model field validation
- ✅ ResponseProcessor preserves raw data
- ✅ Persona integration
- ✅ Storage backward compatibility
- ✅ Save/retrieve round-trip testing

All 73 tests passing (excluding optional AI service tests that require anthropic package).

## Example Usage

```python
from models import Prompt
from personas.beginner import BeginnerPersona

# Create prompt
prompt = Prompt(
    user_id="user123",
    prompt_text="Write a Python function..."
)

# Get AI review
persona = BeginnerPersona()
review = persona.review_prompt(prompt)

# Raw feedback is now stored in prompt
print(prompt.raw_questions)      # Original AI questions
print(prompt.processed_questions) # Cleaned questions

# Review dict also contains both versions
print(review["raw_questions"])      # Same as prompt.raw_questions
print(review["questions"])          # Processed (backward compatible key)
```

## API Response Structure

The `review_prompt()` method now returns:

```json
{
  "suggested_prompt": "...",
  
  "questions": ["Processed Q1?", "Processed Q2?"],
  "refinements": ["Processed R1", "Processed R2"],
  "ratings": { ... },
  "feedback": "Processed feedback text",
  
  "raw_questions": ["**Raw** Q1?", "*Raw* Q2?"],
  "raw_refinements": ["* Raw R1", "- Raw R2"],
  "raw_feedback": "  Raw feedback text  ",
  
  "processed_questions": ["Processed Q1?", "Processed Q2?"],
  "processed_refinements": ["Processed R1", "Processed R2"],
  "processed_feedback": "Processed feedback text",
  
  "persona": "Friendly Guide",
  "ai_used": true
}
```

## Future Enhancements

Potential improvements:
- Add "Compare" view showing diff between raw and processed
- Track statistics on how often processing changes content
- Allow users to toggle between raw/processed in preferences
- Export both versions to JSON/PDF reports
