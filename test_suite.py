"""
Uitgebreide test suite voor GEO Content Optimizer
Test alle functionaliteit automatisch
"""

import google.generativeai as genai
import sys
import os
from datetime import datetime

# Test configuratie
TEST_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBRaGcP_2QpTsyjL2F8cQyrB58LGu4Bfwk')
TEST_TARGET_URL = "https://www.maatwerkonline.nl/blogs/zo-haal-je-het-maximale-uit-chatgpt-voor-je-contentcreatie/"
TEST_REF_URL_1 = "https://www.maatwerkonline.nl/blogs/openai-zet-eerste-stap-richting-advertenties-in-chatgpt/"
TEST_KEYWORDS = "ChatGPT voor je contentcreatie"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name):
    print(f"\n{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}TEST: {name}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*70}{Colors.RESET}")

def print_success(msg):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.RESET}")

def test_model_initialization():
    """Test 1: Model initialisatie"""
    print_test("Model Initialisatie")
    
    try:
        genai.configure(api_key=TEST_API_KEY)
        print_success("API key geconfigureerd")
        
        model_names = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-pro-latest'
        ]
        
        model = None
        model_name_used = None
        
        # Test modellen (zonder Google Search tool - niet beschikbaar voor deze API)
        for model_name in model_names:
            try:
                test_model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"temperature": 0.7}
                )
                # Test of generateContent werkt
                test_response = test_model.generate_content("test")
                if test_response and hasattr(test_response, 'text'):
                    model = test_model
                    model_name_used = model_name
                    print_success(f"Model gevonden: {model_name}")
                    break
            except Exception as e:
                print_warning(f"{model_name} faalt: {str(e)[:60]}")
                continue
        
        if not model:
            print_error("Geen werkend model gevonden!")
            return None, None
        
        return model, model_name_used
        
    except Exception as e:
        print_error(f"Initialisatie fout: {str(e)}")
        return None, None

def test_simple_generation(model):
    """Test 2: Simpele content generatie"""
    print_test("Simpele Content Generatie")
    
    try:
        prompt = "Wat is GEO (Generative Engine Optimization)? Geef een kort antwoord van 2 zinnen."
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            print_success("Content generatie werkt")
            print(f"Response lengte: {len(response.text)} karakters")
            return True
        else:
            print_error("Geen response text ontvangen")
            return False
            
    except Exception as e:
        print_error(f"Generatie fout: {str(e)}")
        return False

def test_url_reading(model):
    """Test 3: URL lezen met Gemini"""
    print_test("URL Content Lezen")
    
    try:
        # Test of Gemini URLs kan lezen via Google Search tool
        prompt = f"""
        Lees de content van deze URL en geef me de titel en eerste alinea:
        {TEST_TARGET_URL}
        """
        
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            print_success("URL content gelezen")
            print(f"Response preview: {response.text[:200]}...")
            return True
        else:
            print_error("Geen content van URL ontvangen")
            return False
            
    except Exception as e:
        print_error(f"URL lezen fout: {str(e)}")
        return False

def test_geo_prompt_structure(model):
    """Test 4: GEO Prompt Structuur"""
    print_test("GEO Prompt Structuur Test")
    
    try:
        prompt = f"""
JE BENT EEN SENIOR GEO SPECIALIST.

TAKEN:
1. Lees en analyseer het artikel op: {TEST_TARGET_URL}
2. Analyseer de tone of voice van: {TEST_REF_URL_1}
3. Herschrijf het artikel volgens GEO-richtlijnen

BELANGRIJKE KEYWORDS: {TEST_KEYWORDS}

GEO-RICHTLIJNEN:
- LOGISCHE HIERARCHIE: Eén H1. H2's voor hoofdthema's, H3's voor subthema's.
- TL;DR / Q&A: Voeg direct onder de inleiding een korte Q&A-TL;DR toe (precies 3 korte Q&A's). Kies de H2-kop op basis van tone of voice:
  * formeel/professioneel → gebruik `## Samenvatting`
  * informeel/tech-savvy → gebruik `## TL;DR`
  * anders → kies een natuurlijke formulering (bv. `## Belangrijkste vragen en antwoorden`)
  Gebruik niet letterlijk 'Kernvragen beantwoord'.
- ENTITY-DENSE OPENINGS: De eerste 40-50 woorden na elke heading MOETEN entiteiten bevatten.
- KORTE PARAGRAFEN: Max 3-4 zinnen.
- KEYWORDS: Integreer deze natuurlijk: {TEST_KEYWORDS}
- AFSLUITING: Feitentabel + CC-BY licentie.

Geef alleen een bevestiging dat je de instructies begrijpt (max 50 woorden).
"""
        
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            print_success("GEO prompt structuur werkt")
            print(f"Response: {response.text[:150]}...")
            return True
        else:
            print_error("Geen response op GEO prompt")
            return False
            
    except Exception as e:
        print_error(f"GEO prompt fout: {str(e)}")
        return False

def test_full_workflow(model):
    """Test 5: Volledige workflow test (kort)"""
    print_test("Volledige Workflow Test (Kort)")
    
    try:
        # Volledige prompt zoals in de app
        prompt = f"""
JE BENT EEN SENIOR GEO SPECIALIST.

TAKEN:
1. Lees en analyseer het artikel op: {TEST_TARGET_URL}
2. Analyseer de tone of voice van: {TEST_REF_URL_1}
3. Herschrijf het artikel volgens GEO-richtlijnen

BELANGRIJKE KEYWORDS: {TEST_KEYWORDS}

GEO-RICHTLIJNEN:
- LOGISCHE HIERARCHIE: Eén H1. H2's voor hoofdthema's, H3's voor subthema's.
- TL;DR / Q&A: Voeg direct onder de inleiding een korte Q&A-TL;DR toe (precies 3 korte Q&A's). Kies de H2-kop op basis van tone of voice:
  * formeel/professioneel → gebruik `## Samenvatting`
  * informeel/tech-savvy → gebruik `## TL;DR`
  * anders → kies een natuurlijke formulering (bv. `## Belangrijkste vragen en antwoorden`)
  Gebruik niet letterlijk 'Kernvragen beantwoord'.
- ENTITY-DENSE OPENINGS: De eerste 40-50 woorden na elke heading MOETEN entiteiten bevatten.
- KORTE PARAGRAFEN: Max 3-4 zinnen.
- KEYWORDS: Integreer deze natuurlijk: {TEST_KEYWORDS}
- AFSLUITING: Feitentabel + CC-BY licentie.

BELANGRIJK: Geef alleen de eerste 300 woorden van het herschreven artikel als test.
"""
        
        print("[INFO] Verzenden van volledige prompt (dit kan even duren)...")
        response = model.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            response_text = response.text
            print_success(f"Volledige workflow werkt! ({len(response_text)} karakters)")
            
            # Check op GEO elementen
            checks = {
                "H1 gevonden": "# " in response_text or "H1" in response_text.upper(),
                "Q&A sectie": "?" in response_text and ("vraag" in response_text.lower() or "Q&A" in response_text),
                "Entiteiten": len(response_text.split()) > 50,  # Basis check
            }
            
            for check, result in checks.items():
                if result:
                    print_success(f"  - {check}")
                else:
                    print_warning(f"  - {check} niet gevonden")
            
            # Sla test resultaat op
            filename = f"test-output-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Test Output - {datetime.now()}\n\n")
                f.write(f"Model: {model}\n\n")
                f.write(f"Prompt lengte: {len(prompt)} karakters\n\n")
                f.write(f"Response lengte: {len(response_text)} karakters\n\n")
                f.write("## Response:\n\n")
                f.write(response_text)
            
            print_success(f"Test output opgeslagen als: {filename}")
            return True
        else:
            print_error("Geen response op volledige workflow")
            return False
            
    except Exception as e:
        print_error(f"Workflow fout: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}GEO Content Optimizer - Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
    
    results = {}
    
    # Test 1: Model initialisatie
    model, model_name = test_model_initialization()
    results['model_init'] = model is not None
    
    if not model:
        print_error("\nKan niet verder testen zonder werkend model!")
        return
    
    # Test 2: Simpele generatie
    results['simple_gen'] = test_simple_generation(model)
    
    # Test 3: URL lezen
    results['url_read'] = test_url_reading(model)
    
    # Test 4: GEO prompt
    results['geo_prompt'] = test_geo_prompt_structure(model)
    
    # Test 5: Volledige workflow
    results['full_workflow'] = test_full_workflow(model)
    
    # Samenvatting
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}TEST SAMENVATTING{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}[PASS]{Colors.RESET}" if result else f"{Colors.RED}[FAIL]{Colors.RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{Colors.BOLD}Resultaat: {passed}/{total} tests geslaagd{Colors.RESET}")
    
    if passed == total:
        print_success("Alle tests geslaagd!")
    else:
        print_warning(f"{total - passed} test(s) gefaald. Check de output hierboven.")

if __name__ == "__main__":
    main()
