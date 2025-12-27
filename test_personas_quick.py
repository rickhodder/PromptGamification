"""Quick test to verify all personas work"""

from personas import PersonaFactory
from models import Prompt

# Create test prompt
prompt = Prompt(
    user_id="test",
    prompt_text="Write a function to sort a list"
)

# Test all personas
personas = ["beginner", "intermediate", "advanced", "interviewer"]
results = {}

for persona_name in personas:
    persona = PersonaFactory.get_persona(persona_name)
    result = persona.review_prompt(prompt)
    results[persona_name] = result
    
    # Check result structure
    has_fields = all(field in result for field in ["suggested_prompt", "questions", "refinements", "ratings", "feedback"])
    print(f"✓ {persona_name:12} - {'OK' if has_fields else 'FAILED'}")

print(f"\nAll {len([r for r in results.values() if 'ratings' in r])}/4 personas working!")
