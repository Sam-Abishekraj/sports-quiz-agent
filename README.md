# AI-Powered Sports Quiz Generation Agent

An intelligent quiz generation system built using **Retrieval-Augmented Generation (RAG)**.  
It combines a local vector database (ChromaDB) with live web search to generate accurate and engaging sports quizzes.

**Developer:** Sam Abishekraj  
**Role:** AI Product / Engineer Intern Assignment

---

## Project Overview

Traditional sports content on social media is mostly limited to news and highlights. This project introduces an interactive format by automatically generating high-quality multiple-choice sports quizzes.

The system allows users to:
- Select a sport
- Choose difficulty level (Easy / Medium / Hard)
- Generate factually grounded quizzes
- Regenerate new quizzes on demand

---

## Key Features

- **RAG Architecture** → Combines historical knowledge + live web data
- **ChromaDB** → Local vector database for historical sports facts
- **DuckDuckGo Search** → Fetches recent sports news and results
- **OpenAI (gpt-4o-mini)** → Generates structured multiple-choice questions
- **Streamlit Dashboard** → Clean and interactive user interface
- **Anti-hallucination design** → LLM is strictly grounded on retrieved context

---

## Tech Stack

| Component              | Technology              |
|------------------------|-------------------------|
| Frontend               | Streamlit               |
| Vector Database        | ChromaDB                |
| Embeddings             | sentence-transformers   |
| Web Search             | DuckDuckGo Search       |
| LLM                    | OpenAI (gpt-4o-mini)    |
| Language               | Python 3.10+            |

---

## Project Structure

```text
sports-quiz-agent/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── app.py
├── data/
│   └── sports_facts.json
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── search.py
│   └── generator.py
└── chroma_db/                  # Auto-generated
```

---

## Setup Instructions

### 1. Clone / Open the project
```bash
cd sports-quiz-agent
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add OpenAI API Key
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## How It Works

1. User selects a **Sport** and **Difficulty**.
2. System retrieves relevant historical facts from **ChromaDB**.
3. System fetches recent updates using **DuckDuckGo Search**.
4. Both contexts are combined and sent to the LLM.
5. LLM generates 4 well-structured multiple-choice questions with answers and explanations.
6. Quiz is displayed in a clean interactive interface.

---

## Example Output Format

```
Sport: Badminton
Difficulty: Medium

Question 1: Which country won the Thomas Cup in 2022?
A) Indonesia
B) India
C) China
D) Denmark
Correct Answer: B
Explanation: India won its first-ever Thomas Cup title in 2022...
```

---

## Notes

- The local knowledge base (`sports_facts.json`) is loaded into ChromaDB on first run.
- The system prioritizes factual accuracy by grounding the LLM on retrieved context.
- `gpt-4o-mini` is used for cost efficiency while maintaining good quality.

---

## Author

**Sam Abishekraj**  
AI/ML Practitioner | AI Product Engineer Intern Candidate

## Project Scrrenshots

<img width="1918" height="939" alt="image" src="https://github.com/user-attachments/assets/f47a2757-3a00-4ff8-9af2-4a8a437a299c" />

<img width="1910" height="1024" alt="image" src="https://github.com/user-attachments/assets/2dc777a6-4f84-464b-a317-2eb19fb9a2a9" />

<img width="1910" height="1024" alt="image" src="https://github.com/user-attachments/assets/27341807-77a8-47dd-8596-21e11d359eca" />





