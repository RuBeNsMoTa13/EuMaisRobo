# EuMaisRobo/tools/news_search.py
import os
from googleapiclient.discovery import build

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

def search_news(query: str) -> str:
    """
    Busca notícias recentes sobre o tema de IA usando a Google Custom Search API.

    Args:
        query (str): A consulta de busca em inglês.

    Returns:
        str: Um resumo em texto dos resultados encontrados, com URLs.
    """
    if not API_KEY or not SEARCH_ENGINE_ID:
        return "Erro: Credenciais da API de busca não configuradas."

    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        
        # Filtra os resultados para sites de notícias
        search_query = f'{query} site:theverge.com OR site:wired.com OR site:techcrunch.com OR site:venturebeat.com OR site:g1.globo.com'

        
        res = service.cse().list(
            q=search_query,
            cx=SEARCH_ENGINE_ID,
            num=5,  # Retorna 5 resultados
            dateRestrict='d1'  # Resultados do último dia   
        ).execute()

        if not res.get("items"):
            return "Nenhum resultado de notícia encontrado."

        formatted_results = []
        for item in res["items"]:
            title = item.get("title")
            snippet = item.get("snippet")
            link = item.get("link")
            formatted_results.append(f"Título: {title}\nResumo: {snippet}\nURL: {link}\n---\n")

        return "".join(formatted_results)

    except Exception as e:
        return f"Ocorreu um erro ao realizar a busca: {e}"