import streamlit as st
from src.generator import compile_quiz_data
from src.database import setup_and_populate_db


# ---------------------------------------------
# Page Config
# ---------------------------------------------
st.set_page_config(
    page_title="Sports Quiz Agent | Sam Abishekraj",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------
# Custom CSS (Dark theme friendly)
# ---------------------------------------------
st.markdown("""
<style>
    /* Main title */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        font-size: 1rem;
        opacity: 0.75;
        margin-bottom: 1.8rem;
    }

    /* Quiz container */
    .quiz-box {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.8rem;
        margin-top: 1rem;
        line-height: 1.7;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        height: 2.7rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        opacity: 0.55;
        font-size: 0.85rem;
        margin-top: 4rem;
        padding-top: 1rem;
    }

    /* Sidebar caption */
    .sidebar .stCaption {
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------
# Initialize Knowledge Base
# ---------------------------------------------
@st.cache_resource
def initialize_knowledge_base():
    return setup_and_populate_db()

initialize_knowledge_base()


# ---------------------------------------------
# Sidebar
# ---------------------------------------------
with st.sidebar:
    st.header("Quiz Controls")
    st.markdown("---")

    sport = st.selectbox(
        "Select Sport",
        options=["Cricket", "Football", "Tennis", "Badminton", "Basketball", "Hockey", "Formula 1", "Athletics"]
    )

    difficulty = st.select_slider(
        "Difficulty Level",
        options=["Easy", "Medium", "Hard"],
        value="Medium"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        generate_btn = st.button("Generate", use_container_width=True, type="primary")
    with col2:
        clear_btn = st.button("Clear", use_container_width=True)

    st.markdown("---")
    st.caption("Built by **Sam Abishekraj**")
    st.caption("AI Product Engineer Intern Assignment")


# ---------------------------------------------
# Session State
# ---------------------------------------------
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None
    st.session_state.last_sport = None
    st.session_state.last_difficulty = None


# ---------------------------------------------
# Clear Action
# ---------------------------------------------
if clear_btn:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None
    st.session_state.last_sport = None
    st.session_state.last_difficulty = None
    st.rerun()


# ---------------------------------------------
# Header
# ---------------------------------------------
st.markdown('<div class="main-title">🏆 AI-Powered Sports Quiz Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate accurate sports quizzes using RAG (ChromaDB + Live Web Search)</div>', unsafe_allow_html=True)


# ---------------------------------------------
# Generate Quiz
# ---------------------------------------------
if generate_btn:
    with st.spinner("Retrieving knowledge and generating quiz..."):
        try:
            quiz_text, context_used = compile_quiz_data(sport, difficulty)
            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            st.session_state.last_sport = sport
            st.session_state.last_difficulty = difficulty
            st.success("Quiz generated successfully!")
        except Exception as e:
            st.error(f"Failed to generate quiz: {str(e)}")


# ---------------------------------------------
# Display Quiz
# ---------------------------------------------
if st.session_state.quiz_output:
    st.markdown(f"### {st.session_state.last_sport}  •  {st.session_state.last_difficulty}")

    # Quiz content
    st.markdown(f'<div class="quiz-box">{st.session_state.quiz_output}</div>', unsafe_allow_html=True)

    st.write("")

    # Regenerate button
    if st.button("🔄 Regenerate Quiz"):
        with st.spinner("Generating a new version..."):
            quiz_text, context_used = compile_quiz_data(
                st.session_state.last_sport,
                st.session_state.last_difficulty
            )
            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            st.rerun()

    # Context Viewer
    with st.expander("View Retrieved Context (RAG Source)"):
        st.code(st.session_state.quiz_context, language="text")

else:
    st.info("Select a sport and difficulty from the sidebar, then click **Generate**.")


# ---------------------------------------------
# Footer
# ---------------------------------------------
st.markdown("""
<div class="footer">
    Developed by <b>Sam Abishekraj</b> &nbsp;•&nbsp; AI Product / Engineer Intern Assignment<br>
    Stack: Streamlit + ChromaDB + DuckDuckGo + OpenAI (gpt-4o-mini)
</div>
""", unsafe_allow_html=True)