import os
from groq import Groq
from dotenv import load_dotenv
import sys

# Add src to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from retriever import CricketRetriever

load_dotenv()

class CricketRAG:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.retriever = CricketRetriever()
        self.model = "llama-3.3-70b-versatile"

    def generate_strategy(self, query, filters=None):
        # Step 1: Retrieve contexts
        contexts = self.retriever.retrieve(query, top_k=5, filters=filters)
        
        context_text = ""
        for i, res in enumerate(contexts):
            context_text += f"\nContext {i+1}:\n{res['text']}\n"

        # Step 2: Format prompt
        system_prompt = (
            "You are an expert South Africa cricket analyst with deep knowledge of tactics, "
            "player strengths, and match strategy. Use the retrieved historical match data "
            "to generate specific, actionable insights. Always cite which matches or "
            "situations informed your recommendation."
        )
        
        user_prompt = f"""Question: {query}

Retrieved Historical Contexts:
{context_text}

Based on these historical South Africa match situations, provide a detailed strategic recommendation. Include:
1. Key tactical insight
2. Player-specific suggestions
3. Historical patterns observed
4. Specific recommendation for this situation"""

        # Step 3: Call Groq
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            response = completion.choices[0].message.content
            return response, contexts
            
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}", contexts

if __name__ == "__main__":
    rag = CricketRAG()
    # Test query
    # strategy, contexts = rag.generate_strategy("Bowling strategy vs Kohli in T20")
    # print(strategy)
