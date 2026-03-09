# SA Cricket RAG Analytics System

A complete RAG-powered analytics system for South Africa cricket using Cricsheet data, FAISS vector storage, and Groq LLM intelligence.

## Architecture
```text
[ Cricsheet CSVs ] -> [ src/ingest.py ] -> [ processed_events.csv ]
                                                     |
                                            [ src/embed.py ]
                                                     |
                                            [ FAISS Index + Metadata ]
                                                     |
[ Streamlit App ] <-> [ src/rag_chain.py ] <-> [ src/retriever.py ]
      |                      |
[ User Query ]         [ Groq llama-3.3-70b ]
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Edit `.env` and add your `GROQ_API_KEY`.

3. **Download Data**:
   - Go to [Cricsheet](https://cricsheet.org/downloads/)
   - Download "all matches" or specific "South Africa" matches in CSV format.
   - Extract CSVs into `data/raw/`.

4. **Prepare Index**:
   ```bash
   python src/ingest.py
   python src/embed.py
   ```

5. **Launch Dashboard**:
   ```bash
   streamlit run src/app.py
   ```

## Example Queries
- "Best bowling strategy in death overs vs India"
- "Effective batting order in T20 chases"
- "Field placement against left-handed openers"
- "How does SA perform in powerplay overs?"

## Technologies
- **Python**: Core logic
- **Pandas/NumPy**: Data processing
- **Sentence-Transformers**: Vector embeddings
- **FAISS**: Similarity search
- **Groq SDK**: LLM orchestration
- **Streamlit**: Interactive UI
