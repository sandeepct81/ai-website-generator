import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
# model = genai.GenerativeModel('gemini-pro')
# model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_website(prompt: str):
    """
    Call Gemini API to generate HTML, CSS, and JavaScript based on user prompt
    """
    try:
        # Enhanced prompt for better website generation
        ai_prompt = f"""
        Create a complete, modern, and responsive website for: {prompt}
        
        Return the response in JSON format with three fields:
        1. html: Complete HTML structure with semantic tags
        2. css: CSS styles (modern, responsive, beautiful)
        3. javascript: Any interactive JavaScript code (if needed)
        
        Requirements:
        - Make it responsive (mobile-first)
        - Use modern CSS (flexbox/grid)
        - Include a navigation bar
        - Add a hero section
        - Include appropriate content sections
        - Make it visually appealing with gradients/shadows
        - Keep it professional and clean
        
        Format the response as valid JSON only, no additional text.
        """
        
        # Generate content
        response = model.generate_content(ai_prompt)
        
        # Parse JSON response
        try:
            # Clean the response text (remove markdown if present)
            response_text = response.text
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]
            
            website_data = json.loads(response_text)
            
            # Ensure all fields exist
            return {
                "html": website_data.get("html", "<html><body>Error generating HTML</body></html>"),
                "css": website_data.get("css", "body { font-family: Arial; }"),
                "javascript": website_data.get("javascript", "// No JavaScript needed")
            }
        except json.JSONDecodeError:
            # Fallback response
            return {
                "html": f"<html><body><h1>Website for {prompt}</h1><p>Generated with AI</p></body></html>",
                "css": "body { font-family: Arial; text-align: center; padding: 50px; }",
                "javascript": "console.log('Website generated');"
            }
            
    except Exception as e:
        print(f"Error generating website: {e}")
        raise Exception(f"Failed to generate website: {str(e)}")

def combine_code(html: str, css: str, javascript: str) -> str:
    """
    Combine HTML, CSS, and JavaScript into a single HTML file
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Website</title>
    <style>
        /* CSS Styles */
        {css}
    </style>
</head>
<body>
    <!-- HTML Content -->
    {html}
    
    <!-- JavaScript -->
    <script>
        {javascript}
    </script>
</body>
</html>"""

if __name__ == "__main__":
    result = generate_website("Create a simple portfolio website")
    print(result)