import os
from groq import Groq

def get_llm_response(prompt: str) -> str:
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return ""
        
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return ""
