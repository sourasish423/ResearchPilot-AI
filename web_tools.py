from ddgs import DDGS
import time


def web_search(query: str):

    try:
        with DDGS() as ddgs:

            for attempt in range(3):

                try:
                    results = list(ddgs.text(
                        query,
                        max_results=5,
                        backend="auto"
                    ))

                    if results:
                        return results

                except Exception:
                    pass

                time.sleep(2)

            # Final attempt using Bing
            try:
                results = list(ddgs.text(
                    query,
                    max_results=5,
                    backend="bing"
                ))

                if results:
                    return results

            except Exception as e:
                return [{"error": f"Search failed: {e}"}]

            return [{"error": "No search results after retries."}]

    except Exception as e:
        return [{"error": f"Search failed: {e}"}]