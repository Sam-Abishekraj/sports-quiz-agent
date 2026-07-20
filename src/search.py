from duckduckgo_search import DDGS
import time
import random


def get_live_news_context(sport_name: str, max_results: int = 4) -> str:
    """
    More robust live search for Streamlit Cloud.
    Tries multiple strategies to get results from DuckDuckGo.
    """

    queries = [
        f"{sport_name} latest news 2025 2026",
        f"{sport_name} recent tournament results winners",
        f"{sport_name} latest match updates",
        f"{sport_name} news today",
        f"latest {sport_name} championship results"
    ]

    retrieved_texts = []

    try:
        with DDGS() as ddgs:
            for query in queries:
                try:
                    # Try different approaches
                    results = list(ddgs.text(
                        query,
                        max_results=5,
                        region="wt-wt",          # Worldwide
                        safesearch="off",
                        timelimit="y"            # Past year
                    ))

                    for r in results:
                        title = r.get("title", "").strip()
                        body = r.get("body", "").strip()

                        if title and body and len(body) > 40:
                            text = f"{title}: {body}"
                            if text not in retrieved_texts:
                                retrieved_texts.append(text)

                    if len(retrieved_texts) >= 3:
                        break

                    # Small random delay to avoid rate limit
                    time.sleep(random.uniform(0.6, 1.2))

                except Exception:
                    time.sleep(1)
                    continue

    except Exception as e:
        return f"Live search temporarily unavailable ({str(e)[:60]}). Using historical knowledge only."

    if not retrieved_texts:
        return "Live web search is currently limited. Historical knowledge from the vector database is being used."

    # Return top unique results
    return "\n\n".join(retrieved_texts[:max_results])
