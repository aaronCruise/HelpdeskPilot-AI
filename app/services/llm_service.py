# Call LLM for AI recommendation
import logging

from app.models.ticket import Ticket, CATEGORIES, PRIORITIES
from app.schemas.recommendation import RecommendationCreate
from google import genai
from os import environ

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    )
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

try:
    from ollama import chat
except ImportError:
    chat = None

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

def api_key_present() -> bool:
    """
    Checks if the GEMINI_API_KEY is present in the environment variables.
    Returns True if present, False otherwise.
    """
    return "GEMINI_API_KEY" in environ


def llm_analyze_ticket(ticket: Ticket, relevant_chunks: list) -> RecommendationCreate:
    if api_key_present():
        return llm_analyze_ticket_with_api_key(ticket, relevant_chunks)
    else:
        return llm_analyze_ticket_no_api_key(ticket, relevant_chunks)


def llm_analyze_ticket_with_api_key(ticket: Ticket, relevant_chunks: list) -> RecommendationCreate:
    client = genai.Client()

    prompt = (
        f"Ticket text: {ticket.text}\n"
        f"Initial category: {ticket.category}\n"
        f"Initial priority: {ticket.priority}\n"
        f"Relevant knowledge: {relevant_chunks}"
    )

    logger.info("LLM selected model: %s", MODEL_CHOICE)
    logger.debug("LLM prompt: %s", prompt)

    response = client.models.generate_content(
        model=MODEL_CHOICE,
        contents=prompt,
        config={
            "system_instruction": SYSTEM_INSTRUCTIONS,
            "response_schema": RecommendationCreate,
            "response_mime_type": "application/json",
        },
    )

    response_text = response.text
    logger.debug("LLM output: %s", response_text)

    if not response_text:
        raise ValueError("The model returned an empty response.")

    return RecommendationCreate.model_validate_json(response_text)

def llm_analyze_ticket_no_api_key(ticket: Ticket, relevant_chunks: list) -> RecommendationCreate:
    if chat is None:
        raise ImportError("Ollama is not installed.")

    model_name = "llama3.2:1b"
    prompt = (
        f"Ticket text: {ticket.text}\n"
        f"Initial category: {ticket.category}\n"
        f"Initial priority: {ticket.priority}\n"
        f"Relevant knowledge: {relevant_chunks}"
    )

    logger.info("LLM selected model: %s", model_name)
    logger.debug("LLM prompt: %s", prompt)

    response = chat(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt},
        ],
        format=RecommendationCreate.model_json_schema()
    )

    return RecommendationCreate.model_validate_json(response.message.content)
"""

    if hasattr(response, "message") and hasattr(response.message, "content"):
        response_text = response.message.content
    elif isinstance(response, dict):
        response_text = response.get("message", {}).get("content", "")
    else:
        response_text = str(response)

    logger.debug("LLM output: %s", response_text)

    if not response_text:
        raise ValueError("The model returned an empty response.")

    return RecommendationCreate.model_validate_json(response_text)
    """