import time
import arxiv


def load_papers(query: str, max_results: int = 5) -> list[str]:
    """
    Busca papers en arXiv y devuelve título + resumen de cada uno.
    Maneja rate limits de arXiv silenciosamente.
    """
    try:
        client = arxiv.Client(
            page_size=5,
            delay_seconds=5,
            num_retries=2,
        )
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
            time.sleep(2)

        return papers

    except arxiv.HTTPError as e:
        if e.status == 429:
            raise ValueError(
                "arXiv está limitando las peticiones. "
                "Espera unos minutos e inténtalo de nuevo."
            )
        raise ValueError(f"Error al conectar con arXiv: {e}")
    except Exception as e:
        raise ValueError(f"Error al cargar papers: {e}")