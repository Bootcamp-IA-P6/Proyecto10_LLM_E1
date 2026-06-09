from app.agents.state import ContentState
from app.generators.llm_factory import get_llm
from app.generators.content_generator import generate_content
from app.services.image_service import get_image


def social_agent_node(state: ContentState) -> ContentState:
    try:
        content = generate_content(
            platform=state["platform"],
            topic=state["topic"],
            audience=state["audience"],
            tone=state["tone"],
            language=state["language"],
            model=state["model"],
            company_profile=state["company_profile"],
        )

        image_url = get_image(state["topic"])

        return {
            **state,
            "generated_content": content,
            "image_url":         image_url,
        }

    except Exception as e:
        return {**state, "error": str(e)}