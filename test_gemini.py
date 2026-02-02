"""
Eenvoudig test script om Gemini 2.0 Flash te testen zonder Streamlit.
Dit script test de Google Search tool configuratie.
"""

import google.generativeai as genai
import sys

def test_gemini():
    print("=" * 60)
    print("Gemini 2.0 Flash Test Script")
    print("=" * 60)
    
    # Vraag om API key
    api_key = input("\nVoer je Gemini API Key in: ").strip()
    
    if not api_key:
        print("❌ Geen API key ingevoerd. Script wordt afgebroken.")
        return
    
    try:
        # Configureer Gemini
        genai.configure(api_key=api_key)
        print("\n✅ API key geconfigureerd")
        
        # Maak model met Google Search tool
        print("\n🔄 Initialiseren van Gemini 2.0 Flash met Google Search tool...")
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            tools=[{'google_search_retrieval': {}}],
            generation_config={"temperature": 0.7}
        )
        print("✅ Model geïnitialiseerd")
        
        # Test prompt
        test_prompt = """
        Wat zijn de nieuwste ontwikkelingen in AI volgens Google Search?
        Geef een kort overzicht van maximaal 3 punten.
        """
        
        print("\n🔄 Test query verzenden...")
        print(f"Prompt: {test_prompt.strip()}")
        print("-" * 60)
        
        response = model.generate_content(test_prompt)
        
        print("\n✅ Response ontvangen!")
        print("=" * 60)
        print("RESULTAAT:")
        print("=" * 60)
        print(response.text)
        print("=" * 60)
        
        print("\n✅ Test succesvol! Gemini 2.0 Flash werkt correct met Google Search tool.")
        
    except Exception as e:
        print(f"\n❌ Fout opgetreden: {str(e)}")
        print("\nMogelijke oorzaken:")
        print("- API key is ongeldig")
        print("- Geen toegang tot Gemini 2.0 Flash")
        print("- Netwerkproblemen")
        print("- Google Search tool niet beschikbaar voor je account")
        sys.exit(1)

if __name__ == "__main__":
    test_gemini()
