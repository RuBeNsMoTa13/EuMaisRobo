# EuMaisRobo/tools/news_search.py
import os
from googleapiclient.discovery import build
from urllib.parse import urlparse

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

        # Adiciona o dateRestrict para buscar resultados do último dia
        res = service.cse().list(
            q=search_query,
            cx=SEARCH_ENGINE_ID,
            num=10,  # Aumenta o número de resultados para uma melhor amostra
            dateRestrict='d1'
        ).execute()

        if not res.get("items"):
            return "Nenhum resultado de notícia encontrado."

        filtered_results = []
        for item in res["items"]:
            link = item.get("link")
            # Extrai o caminho da URL para verificar se não é a página inicial
            parsed_link = urlparse(link)
            if parsed_link.path.strip('/') != '':
                title = item.get("title")
                snippet = item.get("snippet")
                filtered_results.append(f"Título: {title}\nResumo: {snippet}\nURL: {link}\n---\n")

        if not filtered_results:
            return "Nenhum resultado de notícia específico foi encontrado."

        return "".join(filtered_results)

    except Exception as e:
        return f"Ocorreu um erro ao realizar a busca: {e}"