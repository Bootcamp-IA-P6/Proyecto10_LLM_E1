from langgraph.graph import StateGraph, END
from app.agents.state import ContentState
from app.agents.router import router_node, route_to_agent
from app.agents.blog_agent import blog_agent_node
from app.agents.social_agent import social_agent_node
from app.agents.science_agent import science_agent_node
from app.agents.finance_agent import finance_agent_node
from app.agents.quality_check import quality_check_node


def build_graph():
    graph = StateGraph(ContentState)

    # Añadir nodos
    graph.add_node("router",        router_node)
    graph.add_node("blog_agent",    blog_agent_node)
    graph.add_node("social_agent",  social_agent_node)
    graph.add_node("science_agent", science_agent_node)
    graph.add_node("finance_agent", finance_agent_node)
    graph.add_node("quality_check", quality_check_node)

    # Punto de entrada
    graph.set_entry_point("router")

    # Router decide a qué agente ir
    graph.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "blog":    "blog_agent",
            "social":  "social_agent",
            "science": "science_agent",
            "finance": "finance_agent",
        }
    )

    # Todos los agentes van al quality_check
    graph.add_edge("blog_agent",    "quality_check")
    graph.add_edge("social_agent",  "quality_check")
    graph.add_edge("science_agent", "quality_check")
    graph.add_edge("finance_agent", "quality_check")

    # quality_check es el nodo final
    graph.add_edge("quality_check", END)

    return graph.compile()


# Instancia global del grafo
content_graph = build_graph()