from duckduckgo_search import DDGS


def get_live_news_context(sport_name: str, max_results: int = 4) -> str:
    """
    Fetches recent news and updates related to the given sport
    using DuckDuckGo Search. Returns a clean text block that can
    be used as context for the LLM.
    """
    search_query = f"{sport_name} latest tournament results winners news 2025 2026"

    retrieved_texts = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=max_results)

            for index, result in enumerate(results, start=1):
                title = result.get("title", "No Title")
                snippet = result.get("body", "No content available")
                retrieved_texts.append(
                    f"[Source {index}] {title}\n{snippet}"
                )

    except Exception as e:
        print(f"Web search failed: {e}")
        return "No recent web updates available due to connectivity or search issues."

    if not retrieved_texts:
        return "No relevant recent news found for this sport."

    return "\n\n".join(retrieved_texts)