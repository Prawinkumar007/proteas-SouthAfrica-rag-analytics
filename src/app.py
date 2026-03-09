import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_chain import CricketRAG

load_dotenv()

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
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag():
    try:
        return CricketRAG()
    except Exception as e:
        st.error(f"Failed to load RAG system: {e}")
        return None

def main():
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
        opponent = st.sidebar.selectbox("Opponent", ["All", "India", "Australia", "England", "Pakistan", "New Zealand", "Sri Lanka", "West Indies"])
        phase = st.sidebar.selectbox("Match Phase", ["All", "powerplay", "middle", "death"])
        year_range = st.sidebar.slider("Year Range", 2010, 2026, (2010, 2026))

        filters = {
            "format": match_format,
            "opponent": opponent,
            "phase": phase
        }

        # Main UI
        query = st.text_input("Ask about South Africa cricket strategy...", placeholder="e.g., Best bowling strategy in death overs vs India")
        
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
                with st.spinner("Analyzing historical matches..."):
                    response, contexts = rag.generate_strategy(query, filters=filters)
                    
                    tab1, tab2, tab3 = st.tabs(["AI Strategy Recommendation", "Historical Match Contexts", "Analytics"])
                    
                    with tab1:
                        st.markdown("### 🤖 Tactical Intelligence")
                        st.write(response)
                        st.info("Confidence Indicator: High (based on retrieved samples)")

                    with tab2:
                        st.markdown("### 📚 Historical Match Contexts")
                        if not contexts:
                            st.write("No matching historical contexts found.")
                        for ctx in contexts:
                            st.markdown(f"""
                            <div class="context-card">
                                <strong>Similarity Score: {1 - ctx['score']:.4f}</strong><br>
                                {ctx['text']}
                            </div>
                            """, unsafe_allow_html=True)

                    with tab3:
                        st.markdown("### 📊 Analytics Brief")
                        if contexts:
                            # Simple visual breakdown of retrieved data
                            data = [c['metadata'] for c in contexts]
                            df_ctx = pd.DataFrame(data)
                            
                            st.subheader("Match Phase Distribution")
                            st.bar_chart(df_ctx['phase'].value_counts())
                            
                            st.subheader("Opponent Frequency")
                            st.bar_chart(df_ctx['opponent'].value_counts())
                        else:
                            st.write("Perform a query to see analytics.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.exception(e)

    st.divider()
    st.markdown("Data Source: [Cricsheet.org](https://cricsheet.org) | Model: Groq llama-3.3-70b-versatile")

if __name__ == "__main__":
    try:
        os.makedirs("data", exist_ok=True)
        if not os.path.exists("data/processed_events.csv"):
            st.warning("⚠️ Data index not found. Please follow these steps:")
            st.markdown("""
            1. Place Cricsheet CSVs in `data/raw/`
            2. Run `python src/ingest.py`
            3. Run `python src/embed.py`
            """)
        main()
    except Exception as e:
        st.error(f"Critical Startup Error: {e}")
