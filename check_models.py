"""
Script om beschikbare Gemini modellen te checken
"""

import google.generativeai as genai
import sys

def check_models():
    print("=" * 70)
    print("Beschikbare Gemini Modellen Checker")
    print("=" * 70)
    
    api_key = input("\nVoer je Gemini API Key in: ").strip()
    if not api_key:
        print("❌ Geen API key ingevoerd.")
        return
    
    try:
        genai.configure(api_key=api_key)
        print("\n✅ API key geconfigureerd")
        print("\n🔄 Ophalen van beschikbare modellen...\n")
        
        models = genai.list_models()
        
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"✅ {model.name}")
                if hasattr(model, 'display_name'):
                    print(f"   Display Name: {model.display_name}")
        
        print("\n" + "=" * 70)
        print(f"Totaal {len(available_models)} beschikbare modellen gevonden")
        print("=" * 70)
        
        # Test welke modellen Google Search ondersteunen
        print("\n🔄 Testen welke modellen Google Search tool ondersteunen...\n")
        
        test_models = [
            'gemini-2.0-flash-exp',
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        working_model = None
        for model_name in test_models:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    tools=[{'google_search_retrieval': {}}]
                )
                # Test met een simpele query
                response = model.generate_content("Test")
                print(f"✅ {model_name} - Werkt met Google Search tool")
                if not working_model:
                    working_model = model_name
            except Exception as e:
                print(f"❌ {model_name} - {str(e)[:80]}")
        
        if working_model:
            print(f"\n✅ Aanbevolen model: {working_model}")
        else:
            print("\n⚠️ Geen model gevonden met Google Search tool ondersteuning")
            print("   Gebruik een standaard model zonder Google Search tool")
        
    except Exception as e:
        print(f"\n❌ Fout: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    check_models()
