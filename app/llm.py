import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class NewsAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        self.model = "llama-3.1-8b-instant" 

    def get_system_prompt(self):
        """
        Refined Production Prompt: Satisfies Groq's requirement 
        to include the word 'json' in the prompt text.
        """
        return (
            "You are a Senior Crypto Quantitative Analyst at TransFi. "
            "You MUST return your response in JSON format. "  # <--- Added 'JSON' keyword
            "SCHEMA:\n"
            "{\n"
            "  \"summary\": \"2 sentences on market movers\",\n"
            "  \"sentiment\": \"Bullish\", \"Bearish\", or \"Neutral\"\n"
            "}\n\n"
            "RULES:\n"
            "1. Be objective. If the news is just a report, use 'Neutral'.\n"
            "2. Ensure the summary adds professional value, mentioning specific assets if applicable."
        )

    def analyze_article(self, title, text):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": f"TITLE: {title}\nTEXT: {text[:4000]}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            # --- PRODUCTION GRADE PARSING ---
            raw_content = response.choices[0].message.content
            data = json.loads(raw_content)
            
            # Normalize keys to lowercase to prevent 'None' errors
            normalized_data = {k.lower(): v for k, v in data.items()}
            
            # Return with strict defaults
            return {
                "summary": normalized_data.get("summary") or f"Analysis for: {title[:50]}...",
                "sentiment": normalized_data.get("sentiment") or "Neutral"
            }

        except Exception as e:
            print(f"LLM Error: {e}")
            return {
                "summary": "AI summary currently unavailable due to technical error.",
                "sentiment": "Neutral"
            }

analyzer = NewsAnalyzer()