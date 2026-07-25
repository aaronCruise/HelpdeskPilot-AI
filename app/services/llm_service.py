# Call LLM for AI recommendation
from app.models.ticket import Ticket, CATEGORIES, PRIORITIES
from app.schemas.recommendation import RecommendationCreate
from google import genai

# For testing as a standalone file, TODO: delete after
from dotenv import load_dotenv

MODEL_CHOICE = "gemini-3.6-flash"

SYSTEM_INSTRUCTIONS = (
    "You are a senior IT helpdesk technician. "
    "Classify the ticket, improve or override the initial guess if needed, "
    "write a one-sentence summary, and recommend the next step. "
    f"Category must be one of: {', '.join(c.value for c in CATEGORIES)}. "
    f"Priority must be one of: {', '.join(p.value for p in PRIORITIES)}. "
    "Return valid JSON matching this schema: "
    '{"category":"...","priority":"...","summary":"...","recommended_step":"..."}'
)

def llm_analyze_ticket(ticket: Ticket) -> RecommendationCreate:
    client = genai.Client()

    response = client.models.generate_content(
        model=MODEL_CHOICE,
        contents=(
            f"Ticket text: {ticket.text}\n"
            f"Initial category: {ticket.category}\n"
            f"Initial priority: {ticket.priority}"
        ),
        config={
            "system_instruction": SYSTEM_INSTRUCTIONS,
            "response_schema": RecommendationCreate,
            "response_mime_type": "application/json",
        },
    )

    if not response.text:
        raise ValueError("The model returned an empty response.")

    return RecommendationCreate.model_validate_json(response.text)

# Testing purposes as a standalone file TODO: delete
if __name__ == "__main__":
    ticket_text = "This is the most urgent request in the history of requests." \
    "My microsoft 365 in my computer is not working."
    test_ticket = Ticket(
        tid=100,
        requester_name='test@email.com',
        requester_email='test@email.com',
        text=ticket_text,
        category='general',
        priority='low',
        status='new'
    )
    load_dotenv()
    response = llm_analyze_ticket(test_ticket)
    print(response)