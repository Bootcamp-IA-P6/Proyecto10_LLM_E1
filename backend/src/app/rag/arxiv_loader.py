import arxiv


def load_papers(query: str, max_results: int = 10) -> list[str]:
    """
    Busca papers en arXiv y devuelve título + resumen de cada uno.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in client.results(search):
        papers.append(
            f"Título: {result.title}\nResumen: {result.summary}"
        )

    return papers