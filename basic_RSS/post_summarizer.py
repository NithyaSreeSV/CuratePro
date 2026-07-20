import os
from google import genai

class PostSummarizer:
    """Interfaces with the Gemini API to create highly engaging drafts."""
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        # Initialize the official GenAI client
        self.client = genai.Client(api_key=api_key)

    def generate_draft(self, article_title: str, article_context: str, tone: str) -> str:
        """Sends data to Gemini to generate a professional post draft."""
        print("Generating summary using Gemini...")
        
        prompt = f"""
        Act as a professional tech content creator. Based on the following article title and context, 
        write an engaging, concise LinkedIn post draft.
        
        Article Title: {article_title}
        Context/Summary: {article_context}
        Requested Tone: {tone}
        
        STRICT FORMATTING REQUIREMENTS:
        1. DO NOT use any Markdown formatting whatsoever. 
        2. NEVER use double asterisks (**) or single asterisks (*) to bold or italicize phrases. 
        3. Do not include headers like 'Introduction:' or 'Key Takeaways:'.
        4. Output ONLY clean, standard plain text. Use normal capital letters for emphasis if needed, but keep text styling completely natural.
        
        Requirements:
        1. Hook the reader in the first sentence matching the requested tone.
        2. Break the core point down into 3-4 bullet points, keep lists short and punchy using standard unicode bullets like '-' or '•'..
        3. End with an engaging question to invite comments.
        4. Include 5 relevant tech hashtags.
        5. Keep it precise, avoiding corporate fluff.
        """
        
        # Using gemini-3.5-flash model for extracting the response
        response = self.client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        return response.text
