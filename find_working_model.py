"""
Script om het werkende model te vinden door daadwerkelijk generateContent te testen
"""

import google.generativeai as genai
import sys
import os

TEST_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBRaGcP_2QpTsyjL2F8cQyrB58LGu4Bfwk')

def find_working_model():
    print("=" * 70)
    print("Zoeken naar werkend Gemini model...")
    print("=" * 70)
    
    try:
        genai.configure(api_key=TEST_API_KEY)
        print("\n[OK] API key geconfigureerd")
        
        # Eerst lijst van beschikbare modellen ophalen
        print("\n[INFO] Ophalen van beschikbare modellen...")
        try:
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    model_name = model.name.replace('models/', '')
                    available_models.append(model_name)
                    print(f"  - {model_name}")
            
            print(f"\n[OK] {len(available_models)} modellen gevonden met generateContent support")
        except Exception as e:
            print(f"[WARN] Kon modellen niet ophalen: {str(e)[:80]}")
            available_models = []
        
        # Test modellen in volgorde van voorkeur
        test_models = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro-latest',
            'gemini-pro',
            'gemini-pro-latest',
            'gemini-2.0-flash-exp',
        ]
        
        # Voeg beschikbare modellen toe aan test lijst
        for model_name in available_models:
            if model_name not in test_models:
                test_models.append(model_name)
        
        print("\n[INFO] Testen welke modellen daadwerkelijk werken...\n")
        
        working_model = None
        working_model_name = None
        
        # Test met Google Search tool eerst
        print("[INFO] Testen met Google Search tool...")
        for model_name in test_models:
            try:
                print(f"  Testen {model_name}...", end=" ")
                model = genai.GenerativeModel(
                    model_name=model_name,
                    tools=[{'google_search_retrieval': {}}],
                    generation_config={"temperature": 0.7}
                )
                # Test daadwerkelijk generateContent
                response = model.generate_content("Say hello")
                if response and hasattr(response, 'text') and response.text:
                    working_model = model
                    working_model_name = model_name
                    print(f"[OK] Werkt met Google Search!")
                    break
                else:
                    print("[FAIL] Geen response")
            except Exception as e:
                error_msg = str(e)[:60]
                print(f"[FAIL] {error_msg}")
                continue
        
        # Fallback zonder Google Search
        if not working_model:
            print("\n[INFO] Testen zonder Google Search tool...")
            for model_name in test_models:
                try:
                    print(f"  Testen {model_name}...", end=" ")
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        generation_config={"temperature": 0.7}
                    )
                    # Test daadwerkelijk generateContent
                    response = model.generate_content("Say hello")
                    if response and hasattr(response, 'text') and response.text:
                        working_model = model
                        working_model_name = model_name
                        print(f"[OK] Werkt zonder Google Search!")
                        break
                    else:
                        print("[FAIL] Geen response")
                except Exception as e:
                    error_msg = str(e)[:60]
                    print(f"[FAIL] {error_msg}")
                    continue
        
        if working_model:
            print(f"\n[OK] Werkend model gevonden: {working_model_name}")
            return working_model_name
        else:
            print("\n[FAIL] Geen werkend model gevonden!")
            return None
            
    except Exception as e:
        print(f"\n[FAIL] Fout: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = find_working_model()
    if result:
        print(f"\nGebruik dit model in je code: '{result}'")
        sys.exit(0)
    else:
        sys.exit(1)
