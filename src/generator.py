from openai import OpenAI
from src.config import OPENAI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context


def compile_quiz_data(sport: str, difficulty: str) -> tuple[str, str]:
    """
    RAG-based quiz generation engine.
    Retrieves historical + live context and generates structured quizzes.
    """

    # ----------------------
    # 1. Retrieve Historical Context
    # ----------------------
    db_query = f"{sport} history records champions tournaments famous players rules"
    historic_facts = query_historic_facts(
        sport=sport,
        query_text=db_query,
        n_results=4
    )

    historical_context = "\n".join(historic_facts) if historic_facts else "No historical facts available."

    # ----------------------
    # 2. Retrieve Live Context
    # ----------------------
    live_context = get_live_news_context(sport, max_results=3)

    # ----------------------
    # 3. Combine Context
    # ----------------------
    unified_context = f"""HISTORICAL FACTS:
{historical_context}

RECENT UPDATES:
{live_context}
"""

    # ----------------------
    # 4. Initialize Client
    # ----------------------
    client = OpenAI(api_key=OPENAI_API_KEY)

    # ----------------------
    # 5. System Prompt
    # ----------------------
    system_prompt = """You are an expert sports quiz creator.
Your job is to generate accurate multiple-choice quizzes strictly based on the given context.
Never invent facts. Only use information present in the context.
"""

    # ----------------------
    # 6. User Prompt (Strict Format matching PDF)
    # ----------------------
    user_prompt = f"""Create a sports quiz with the following details:

Sport: {sport}
Difficulty: {difficulty}

Generate exactly 4 questions.

Follow this exact output format (do not change it):

Sport: {sport}
Difficulty: {difficulty}

Question 1:
[Question text here]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Correct Answer: [Letter]. [Full correct option text]
Explanation: [Short explanation]

Question 2:
[Question text here]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Correct Answer: [Letter]. [Full correct option text]
Explanation: [Short explanation]

Question 3:
...

Question 4:
...

Important Rules:
- Use only facts from the context below.
- Keep explanations short and factual.
- Match the difficulty level properly.
- Do not add any extra text before or after the quiz.

CONTEXT:
{unified_context}
"""

    # ----------------------
    # 7. LLM Call
    # ----------------------
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,   # Lower temperature = more consistent format
    )

    quiz_text = response.choices[0].message.content.strip()

    return quiz_text, unified_context