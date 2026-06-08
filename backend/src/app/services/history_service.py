from sqlalchemy.orm import Session
from app.database.models import Generation


def save_generation(
    db:         Session,
    platform:   str,
    topic:      str,
    audience:   str,
    content:    str,
    model_used: str,
    tone:       str = "",
    language:   str = "es",
    image_url:  str = "",
    gen_type:   str = "general",
) -> Generation:
    """
    Guarda una generación en el historial.
    """
    generation = Generation(
        platform=platform,
        topic=topic,
        audience=audience,
        tone=tone,
        language=language,
        model_used=model_used,
        content=content,
        image_url=image_url,
        gen_type=gen_type,
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)
    return generation


def get_history(
    db:    Session,
    limit: int = 20,
    skip:  int = 0,
) -> list[Generation]:
    """
    Devuelve las últimas generaciones ordenadas por fecha descendente.
    """
    return (
        db.query(Generation)
        .order_by(Generation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_generation(db: Session, generation_id: int) -> bool:
    """
    Elimina una generación por ID. Devuelve True si existía, False si no.
    """
    generation = (
        db.query(Generation)
        .filter(Generation.id == generation_id)
        .first()
    )
    if not generation:
        return False
    db.delete(generation)
    db.commit()
    return True