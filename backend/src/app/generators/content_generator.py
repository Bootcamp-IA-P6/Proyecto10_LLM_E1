from app.prompts.blog import blog_prompt
from app.prompts.twitter import twitter_prompt
from app.prompts.linkedin import linkedin_prompt
from app.prompts.instagram import instagram_prompt
from app.generators.llm_factory import get_llm


PROMPTS = {
    "blog": blog_prompt,
    "twitter": twitter_prompt,
    "linkedin": linkedin_prompt,
    "instagram": instagram_prompt,
}


def generate_content(
    platform: str,
    topic: str,
    audience: str,
    tone: str,
    language: str,
    company_profile: str = "",
) -> str:
    """
    Genera contenido para la plataforma indicada usando LangChain.
    """
    if platform not in PROMPTS:
        raise ValueError(f"Plataforma no soportada: {platform}")

    company_context = (
        f"Perfil de empresa: {company_profile}" if company_profile else ""
    )

    llm = get_llm()
    prompt = PROMPTS[platform]
    chain = prompt | llm

    response = chain.invoke({
        "topic": topic,
        "audience": audience,
        "tone": tone,
        "language": language,
        "company_context": company_context,
    })

    return response.content