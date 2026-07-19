import os
from google import genai

class PostSummarizer:
    """Interfaces with the Gemini API to customize tone and structural layout."""
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=api_key)

    def generate_draft(self, article_title: str, article_context: str, tone: str, format_style: str) -> str:
        print(f"Generating post using Gemini with a {tone} tone in {format_style} style...")
        
        prompt = f"""
        Act as a professional tech content creator. Based on the following context parameters, 
        generate an engaging, crisp LinkedIn post draft.
        
        Article Title: {article_title}
        Context/Summary: {article_context}
        Requested Tone: {tone}
        Requested Structural Format Style: {format_style}
        
        STRICT FORMATTING REQUIREMENTS:
        1. DO NOT use any Markdown formatting whatsoever. 
        2. NEVER use double asterisks (**) or single asterisks (*) to bold or italicize phrases. 
        3. Do not include headers like 'Introduction:' or 'Key Takeaways:'.
        4. Output ONLY clean, standard plain text. Use normal capital letters for emphasis if needed, but keep text styling completely natural.
        
        CONTENT REQUIREMENTS:
        1. Hook the reader in the first sentence matching the tone.
        2. Format the layout exactly as requested: if 'Long Paragraphs', write deep analytical sentences. If 'Simple Bullet Points', keep lists short and punchy using standard unicode bullets like '-' or '•'.
        3. End with an engaging question to invite comments.
        4. Include 3 relevant tech hashtags at the very end.
        """
        
        response = self.client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        return response.text