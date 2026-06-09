from typing import TypedDict, Optional


class ContentState(TypedDict):
    # Input
    platform:         str
    topic:            str
    audience:         str
    tone:             str
    language:         str
    model:            str
    company_profile:  str

    # Router
    content_type:     str  # blog | social | science | finance

    # Output
    generated_content: Optional[str]
    image_url:         Optional[str]

    # Quality
    quality_score:    Optional[float]
    quality_feedback: Optional[str]

    # Error
    error:            Optional[str]