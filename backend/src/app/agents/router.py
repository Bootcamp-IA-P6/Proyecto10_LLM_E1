from app.agents.state import ContentState
from app.generators.llm_factory import get_llm

SCIENCE_KEYWORDS = [
    "physics", "quantum", "biology", "chemistry", "astronomy",
    "neuroscience", "genetics", "artificial intelligence", "machine learning",
    "mathematics", "fisic", "quantic", "biolog", "quimic", "astronomia",
    "neurociencia", "genetica", "inteligencia artificial", "matematica",
    "ciencia", "science", "research", "paper", "study", "arxiv",
]

FINANCE_KEYWORDS = [
    "bolsa", "mercado", "finanzas", "inversion", "bitcoin", "crypto",
    "acciones", "economia", "stock", "market", "finance", "investment",
    "trading", "forex", "bonos", "fondos", "etf", "divisa",
]


def classify_content(platform: str, topic: str) -> str:
    topic_lower = topic.lower()

    # Blog siempre va a BlogAgent
    if platform == "blog":
        return "blog"

    # Detectar por keywords del topic
    for keyword in SCIENCE_KEYWORDS:
        if keyword in topic_lower:
            return "science"

    for keyword in FINANCE_KEYWORDS:
        if keyword in topic_lower:
            return "finance"

    # Twitter, LinkedIn, Instagram sin keyword específica → SocialAgent
    if platform in ["twitter", "linkedin", "instagram"]:
        return "social"

    # Default → social
    return "social"


def router_node(state: ContentState) -> ContentState:
    content_type = classify_content(state["platform"], state["topic"])
    return {**state, "content_type": content_type}


def route_to_agent(state: ContentState) -> str:
    return state["content_type"]