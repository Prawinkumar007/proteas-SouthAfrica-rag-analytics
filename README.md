<div align="center">

<!-- HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=006B3F,FFB81C&height=200&section=header&text=Proteas%20RAG%20Analytics&fontSize=42&fontColor=ffffff&fontAlignY=38&desc=AI-Powered%20South%20Africa%20Cricket%20Intelligence&descAlignY=58&descSize=18" width="100%"/>

<!-- BADGES -->
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-0078D4?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai)
[![Groq](https://img.shields.io/badge/Groq-LLM_Powered-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Prawinkumar007/proteas-SouthAfrica-rag-analytics?style=for-the-badge&color=FFB81C)](https://github.com/Prawinkumar007/proteas-SouthAfrica-rag-analytics)

<br/>

> 🏏 *"Where historical cricket data meets cutting-edge AI — delivering strategic intelligence for the Proteas."*

<br/>

[🚀 Live Demo](#-live-demo) • [📖 Documentation](#-how-it-works) • [⚡ Quick Start](#-quick-start) • [🎯 Features](#-features) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 What is Proteas RAG Analytics?

**Proteas RAG Analytics** is an AI-powered cricket intelligence platform built specifically for the **South Africa national cricket team**. It combines **Retrieval-Augmented Generation (RAG)** with ball-by-ball historical match data to deliver expert-level tactical insights — in plain English.

Ask it anything. It retrieves real match situations. It reasons like an analyst. It answers like a coach.

```
"What is the best bowling strategy for South Africa in death overs against India?"
```
```
🤖 Based on 15 retrieved historical match contexts...
   ➜ Deploy Kagiso Rabada with short-pitched deliveries targeting body line
   ➜ Tabraiz Shamsi's googly proved effective — 2019 T20I, 2/19 in 4 overs
   ➜ Vary pace between Ngidi yorkers and Nortje bouncers...
```

---

## 🎯 Features

| Feature | Description |
|--------|-------------|
| 🔍 **Semantic Search** | Finds historically similar match situations using vector embeddings |
| 🧠 **AI Strategy Engine** | Groq LLaMA 3.3-70B generates expert tactical recommendations |
| ⚡ **FAISS Vector DB** | Lightning-fast similarity retrieval across 72,000+ ball events |
| 🎛️ **Smart Filters** | Filter by format (T20/ODI/Test), opponent, phase, and year |
| 📊 **Analytics Dashboard** | Visual charts for run rates, dismissal patterns, and player stats |
| 💬 **Natural Language** | Ask questions in plain English — no SQL, no code |
| 🏟️ **Real Match Data** | Grounded in actual Cricsheet ball-by-ball data |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROTEAS RAG ANALYTICS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📁 Cricsheet CSVs                                              │
│       │                                                         │
│       ▼                                                         │
│  🔧 src/ingest.py  ──►  data/processed_events.csv              │
│       │                         │                              │
│       │                         ▼                              │
│       │              🔢 src/embed.py                           │
│       │                         │                              │
│       │              ┌──────────┴──────────┐                   │
│       │              │   FAISS Index       │                   │
│       │              │   embeddings/       │                   │
│       │              │   cricket_index     │                   │
│       │              └──────────┬──────────┘                   │
│       │                         │                              │
│       │              🔎 src/retriever.py                       │
│       │                         │                              │
│       │              🤖 src/rag_chain.py                       │
│       │                    │         │                         │
│       │              Groq LLM    Retrieved                     │
│       │              Response    Contexts                      │
│       │                    │         │                         │
│       └────────────►  🖥️ Streamlit Dashboard                   │
│                            │                                   │
│                     ┌──────┴───────┐                           │
│               AI Strategy    Historical Match                  │
│               Tab            Contexts Tab                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Prawinkumar007/proteas-SouthAfrica-rag-analytics.git
cd proteas-SouthAfrica-rag-analytics
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Key
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```
> 🔑 Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4️⃣ Add Cricket Data
```bash
# Download from cricsheet.org and place CSVs in:
mkdir -p data/raw
# Drop your Cricsheet CSV files into data/raw/

# OR use the sample dataset provided in the repo
cp data/sa_cricket_data.csv data/raw/
```

### 5️⃣ Build the Vector Index
```bash
python src/ingest.py     # Process & clean match data
python src/embed.py      # Generate FAISS embeddings
```

### 6️⃣ Launch the Dashboard 🚀
```bash
streamlit run src/app.py
```
Open your browser at `http://localhost:8501`

---

## 💡 Example Queries

Try these in the dashboard:

```
🏏 "What is the best bowling strategy in death overs against India?"
🏏 "Suggest an optimal batting order for T20 chases"
🏏 "How should SA field against left-handed opening pairs?"
🏏 "Which bowlers perform best in powerplay overs?"
🏏 "Analyze South Africa's performance in ODI run chases above 300"
🏏 "What patterns emerge in SA's batting collapse situations?"
```

---

## 📁 Project Structure

```
proteas-SouthAfrica-rag-analytics/
│
├── 📂 data/
│   ├── raw/                    # Raw Cricsheet CSV files
│   └── processed_events.csv    # Cleaned & structured match events
│
├── 📂 embeddings/
│   ├── cricket_index.faiss     # FAISS vector index
│   └── metadata.json           # Event metadata store
│
├── 📂 src/
│   ├── ingest.py               # Data loading & preprocessing
│   ├── embed.py                # Sentence-transformer embeddings
│   ├── retriever.py            # FAISS similarity search
│   ├── rag_chain.py            # Groq LLM + RAG orchestration
│   └── app.py                  # Streamlit dashboard
│
├── .env                        # API keys (never commit this!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.10+ | Core development |
| **Data** | Pandas, NumPy | Processing & analysis |
| **Embeddings** | Sentence-Transformers | Semantic vector generation |
| **Vector DB** | FAISS (Facebook AI) | Fast similarity search |
| **LLM** | Groq + LLaMA 3.3-70B | Strategy reasoning |
| **Dashboard** | Streamlit | Interactive web UI |
| **Data Source** | Cricsheet.org | Ball-by-ball match data |

</div>

---

## 📊 Dataset Overview

| Metric | Value |
|--------|-------|
| Total Ball Events | 72,000+ |
| Matches Covered | 150 |
| Formats | T20I, ODI, Test |
| Opponents | 8 international teams |
| Date Range | 2015 – 2024 |
| Players Tracked | 28+ SA & opposition players |
| Venues | 15+ international grounds |

---

## 🖥️ Dashboard Preview

```
┌─────────────────────────────────────────────────────┐
│  Intelligence Filters    │  ZA SA Cricket RAG        │
│  ─────────────────────   │  Analytics System         │
│  Match Format: [T20 ▼]   │                           │
│  Opponent:   [India ▼]   │  Ask about SA cricket...  │
│  Phase:       [All ▼]    │  ┌─────────────────────┐  │
│  Year: 2010 ───── 2024   │  │ Your query here...  │  │
│                          │  └─────────────────────┘  │
│                          │  [Generate Strategy 🏏]   │
│                          │                           │
│                          │  ┌─── AI Strategy ──────┐ │
│                          │  │ 🎯 Tactical Insight   │ │
│                          │  │ 👤 Player Suggestions │ │
│                          │  │ 📈 Historical Patterns│ │
│                          │  │ ✅ Recommendation     │ │
│                          │  └───────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Live Demo

> 🌐 **[Launch App →](https://proteas-southafrica-rag-analytics.streamlit.app)**
>
> *(Deployed on Streamlit Community Cloud)*

---

## 🤝 Contributing

Contributions are welcome! Here's how:

```bash
# 1. Fork the repo
# 2. Create your feature branch
git checkout -b feature/add-player-heatmaps

# 3. Commit your changes
git commit -m "feat: add player performance heatmap visualization"

# 4. Push and open a Pull Request
git push origin feature/add-player-heatmaps
```

### Ideas for Contributions
- 🗺️ Field placement heatmaps
- 📈 Player career trend charts
- 🌍 Venue-specific performance analysis
- 🔄 Real-time Cricsheet data sync
- 🧪 Unit tests for retrieval pipeline

---

## ⚠️ Security Note

Never commit your `.env` file. The `.gitignore` already excludes it, but double-check:

```bash
# Verify .env is ignored
git status  # .env should NOT appear here
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- 🏏 [Cricsheet.org](https://cricsheet.org) — Open ball-by-ball cricket data
- 🤖 [Groq](https://groq.com) — Ultra-fast LLM inference
- 🔢 [Facebook AI FAISS](https://faiss.ai) — Vector similarity search
- 🤗 [Sentence Transformers](https://sbert.net) — Semantic embeddings
- 🖥️ [Streamlit](https://streamlit.io) — Rapid dashboard development

---

<div align="center">

**Built with ❤️ for South African Cricket 🇿🇦**

<img src="https://capsule-render.vercel.app/api?type=waving&color=006B3F,FFB81C&height=100&section=footer" width="100%"/>

⭐ **Star this repo if you found it useful!** ⭐

</div>
