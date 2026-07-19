from duckduckgo_search import DDGS
import time


def get_live_news_context(sport_name: str, max_results: int = 4) -> str:
    """
    Fetches recent news related to the sport using DuckDuckGo.
    Made more robust for cloud environments.
    """
    
    # Multiple query variations to improve success rate
    queries = [
        f"{sport_name} latest news results 2025 2026",
        f"{sport_name} tournament winners recent",
        f"{sport_name} latest match updates"
    ]

    retrieved_texts = []

    try:
        with DDGS() as ddgs:
            for query in queries:
                try:
                    results = ddgs.text(query, max_results=3)
                    
                    for index, result in enumerate(results, start=1):
                        title = result.get("title", "").strip()
                        body = result.get("body", "").strip()
                        
                        if title and body:
                            retrieved_texts.append(f"{title}: {body}")
                    
                    # If we got some results, no need to try more queries
                    if retrieved_texts:
                        break
                        
                    time.sleep(0.5)  # small delay
                    
                except Exception:
                    continue

    except Exception as e:
        return f"Web search currently unavailable. ({str(e)[:80]})"

    if not retrieved_texts:
        return "No recent web updates found for this sport at the moment."

    # Return top unique results
    unique_results = list(dict.fromkeys(retrieved_texts))  # remove duplicates
    return "\n\n".join(unique_results[:4])
