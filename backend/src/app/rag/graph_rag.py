import json
import re
import networkx as nx
from app.generators.llm_factory import get_llm


ENTITY_EXTRACTION_PROMPT = """Extrae las entidades principales de este texto científico.

Texto:
{text}

Responde ÚNICAMENTE con JSON válido, sin texto adicional:
{{
  "entities": [
    {{"name": "nombre entidad", "type": "concept|person|institution|technology"}}
  ]
}}

Máximo 5 entidades. Solo las más relevantes.
"""


def extract_entities(text: str) -> list[dict]:
    try:
        llm    = get_llm("ollama")
        prompt = ENTITY_EXTRACTION_PROMPT.format(text=text[:500])

        response = llm.invoke(prompt)
        text_out = response if isinstance(response, str) else str(response)

        json_match = re.search(r'\{.*?\}', text_out, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            entities = data.get("entities", [])
            # Verificar que cada entidad es un dict con "name"
            return [
                e for e in entities
                if isinstance(e, dict) and "name" in e
            ]
        return []

    except Exception:
        return []


def build_knowledge_graph(papers: list[str]) -> nx.DiGraph:
    G = nx.DiGraph()

    for i, paper_text in enumerate(papers):
        # Extraer título del paper (primera línea)
        lines      = paper_text.split("\n")
        paper_title = lines[0].replace("Título: ", "").strip() if lines else f"Paper {i}"

        # Añadir nodo paper
        G.add_node(paper_title, type="paper")

        # Extraer entidades del resumen
        summary   = "\n".join(lines[1:]) if len(lines) > 1 else paper_text
        entities  = extract_entities(summary)

        for entity in entities:
            entity_name = entity.get("name", "")
            entity_type = entity.get("type", "concept")
            if entity_name:
                G.add_node(entity_name, type=entity_type)
                G.add_edge(paper_title, entity_name, relation="mentions")

    return G


def query_graph(G: nx.DiGraph, topic: str) -> str:
    if G.number_of_nodes() == 0:
        return ""

    topic_lower = topic.lower()

    # Buscar nodos relevantes al topic
    relevant = [
        n for n in G.nodes
        if any(word in n.lower() for word in topic_lower.split())
    ]

    if not relevant:
        return ""

    # Recuperar vecinos del nodo más relevante
    node      = relevant[0]
    neighbors = list(G.neighbors(node))

    if not neighbors:
        return f"Concepto relacionado encontrado: {node}"

    context = (
        f"Entidades relacionadas con '{topic}' encontradas en papers científicos:\n"
        f"- {node} se relaciona con: {', '.join(neighbors[:8])}"
    )

    return context


def get_graph_context(topic: str, papers: list[str]) -> str:
    try:
        G       = build_knowledge_graph(papers)
        context = query_graph(G, topic)
        return context
    except Exception:
        return ""