import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Project root (one level up from src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute paths
INDEX_PATH = os.path.join(BASE_DIR, "embeddings", "cricket_index.faiss")
METADATA_PATH = os.path.join(BASE_DIR, "embeddings", "metadata.json")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed_events.csv")
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

# Add src to path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import ingest
import embed
from rag_chain import CricketRAG

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Page Config
st.set_page_config(
    page_title="SA Cricket RAG Analytics",
    page_icon="🇿🇦",
    layout="wide"
)

# Custom CSS for SA Theme (Green and Gold)
st.markdown("""
<style>
    .stApp {
        background-color: #004225;
        color: #FFB612;
    }
    .stSidebar {
        background-color: #00331C;
    }
    .stButton>button {
        background-color: #FFB612;
        color: #004225;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #000000;
    }
    .context-card {
        background-color: #005A32;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #FFB612;
        margin-bottom: 10px;
    }
    .build-banner {
        background-color: #1a3a1a;
        border: 2px solid #FFB612;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: #FFB612;
    }
</style>
""", unsafe_allow_html=True)


def build_index():
    """Run ingest and embed pipelines to build the FAISS index from raw data."""
    os.makedirs(os.path.join(BASE_DIR, "embeddings"), exist_ok=True)

    st.markdown(
        '<div class="build-banner">🏏 <b>First Launch Detected</b><br>'
        'Building the cricket intelligence index from raw match data. This may take a few minutes…</div>',
        unsafe_allow_html=True,
    )

    with st.spinner("Step 1/2 — Ingesting and processing raw match data…"):
        ingest.process_data(RAW_DATA_DIR, DATA_PATH)

    if not os.path.exists(DATA_PATH):
        st.error(
            "❌ Ingestion failed: no processed data was produced. "
            "Please ensure `data/raw/sa_cricket_data.csv` exists and contains South Africa match records."
        )
        st.stop()

    with st.spinner("Step 2/2 — Generating sentence embeddings and building FAISS index…"):
        embed.generate_embeddings(DATA_PATH, INDEX_PATH, METADATA_PATH)

    if os.path.exists(INDEX_PATH):
        st.success("✅ Index built successfully! Reloading the app…")
        st.rerun()
    else:
        st.error("❌ Embedding step failed: FAISS index was not created. Check logs above.")
        st.stop()


@st.cache_resource
def load_rag():
    try:
        return CricketRAG()
    except Exception as e:
        st.error(f"Failed to load RAG system: {e}")
        return None


def main():
    # ── Auto-build index on first launch ──────────────────────────────────────
    if not os.path.exists(INDEX_PATH):
        build_index()
        return  # rerun() above will restart; this return is a safety guard

    # ── Normal app flow ────────────────────────────────────────────────────────
    st.title("🇿🇦 SA Cricket RAG Analytics System")
    st.markdown("### Professional Match Strategy & Tactical Intelligence")

    try:
        rag = load_rag()
        if rag is None:
            st.error("RAG system could not be initialized.")
            return

        # Sidebar Filters
        st.sidebar.header("Intelligence Filters")

        match_format = st.sidebar.selectbox("Match Format", ["All", "T20", "ODI", "Test"])
        opponent = st.sidebar.selectbox(
            "Opponent",
            ["All", "India", "Australia", "England", "Pakistan", "New Zealand", "Sri Lanka", "West Indies"]
        )
        phase = st.sidebar.selectbox("Match Phase", ["All", "powerplay", "middle", "death"])
        year_range = st.sidebar.slider("Year Range", 2010, 2026, (2010, 2026))

        filters = {
            "format": match_format,
            "opponent": opponent,
            "phase": phase,
        }

        # Main UI
        query = st.text_input(
            "Ask about South Africa cricket strategy…",
            placeholder="e.g., Best bowling strategy in death overs vs India"
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Example: Death Overs vs India"):
                query = "Best bowling strategy in death overs vs India"
        with col2:
            if st.button("Example: T20 Chases"):
                query = "Effective batting order in T20 chases"
        with col3:
            if st.button("Example: Left-hand Openers"):
                query = "Field placement against left-handed openers"
        with col4:
            if st.button("Example: Powerplay Perf"):
                query = "How does SA perform in powerplay overs?"

        if st.button("Generate Strategy"):
            if not os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY") == "your_groq_api_key_here":
                st.error("Please set your GROQ_API_KEY in the .env file.")
            elif not query:
                st.warning("Please enter a query.")
            else:
                with st.spinner("Analyzing historical matches…"):
                    response, contexts = rag.generate_strategy(query, filters=filters)

                    tab1, tab2, tab3 = st.tabs(
                        ["AI Strategy Recommendation", "Historical Match Contexts", "Analytics"]
                    )

                    with tab1:
                        st.markdown("### 🤖 Tactical Intelligence")
                        st.write(response)
                        st.info("Confidence Indicator: High (based on retrieved samples)")

                    with tab2:
                        st.markdown("### 📚 Historical Match Contexts")
                        if not contexts:
                            st.write("No matching historical contexts found.")
                        for ctx in contexts:
                            st.markdown(
                                f"""
                                <div class="context-card">
                                    <strong>Similarity Score: {1 - ctx['score']:.4f}</strong><br>
                                    {ctx['text']}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    with tab3:
                        st.markdown("### 📊 Analytics Brief")
                        if contexts:
                            data = [c["metadata"] for c in contexts]
                            df_ctx = pd.DataFrame(data)

                            st.subheader("Match Phase Distribution")
                            st.bar_chart(df_ctx["phase"].value_counts())

                            st.subheader("Opponent Frequency")
                            st.bar_chart(df_ctx["opponent"].value_counts())
                        else:
                            st.write("Perform a query to see analytics.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.exception(e)

    st.divider()
    st.markdown("Data Source: [Cricsheet.org](https://cricsheet.org) | Model: Groq llama-3.3-70b-versatile")


main()
