"""
CLI versie van de GEO Content Optimizer - werkt zonder Streamlit
Gebruik dit script als Windows beveiliging Streamlit blokkeert.
"""

import google.generativeai as genai
import sys
from datetime import datetime

def main():
    print("=" * 70)
    print("🚀 GEO Specialist: Content Optimizer (CLI Versie)")
    print("=" * 70)
    print()
    
    # API Key
    api_key = input("Voer je Gemini API Key in: ").strip()
    if not api_key:
        print("❌ Geen API key ingevoerd.")
        return
    
    # Temperatuur
    try:
        temp_input = input("Creativiteit/Temperatuur (0.0-2.0, standaard 0.7): ").strip()
        temp_value = float(temp_input) if temp_input else 0.7
        if not 0.0 <= temp_value <= 2.0:
            temp_value = 0.7
    except:
        temp_value = 0.7
    
    try:
        # Configureer Gemini
        genai.configure(api_key=api_key)
        print("\n✅ API key geconfigureerd")
        
        # Gebruik werkend model (getest: gemini-pro-latest werkt)
        print("[INFO] Initialiseren van Gemini model...")
        model_names = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-pro-latest'
        ]
        
        model = None
        model_name_used = None
        
        for model_name in model_names:
            try:
                test_model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"temperature": temp_value}
                )
                # Test of het werkt
                test_response = test_model.generate_content("test")
                if test_response and hasattr(test_response, 'text'):
                    model = test_model
                    model_name_used = model_name
                    print(f"[OK] Model gevonden: {model_name}")
                    break
            except Exception:
                continue
        
        if not model:
            raise Exception("Geen werkend Gemini model gevonden. Controleer je API key en toegang.")
        
        print(f"✅ Model '{model_name_used}' geïnitialiseerd\n")
        
        # Input velden
        print("-" * 70)
        target_url = input("Target URL (Te optimaliseren artikel): ").strip()
        ref_url_1 = input("Referentie URL 1 (Tone of Voice): ").strip()
        ref_url_2 = input("Referentie URL 2 (Tone of Voice) [optioneel]: ").strip()
        print("\nBelangrijke Keywords & Focus (druk Enter op een lege regel om te stoppen):")
        keywords_lines = []
        while True:
            line = input()
            if line == "":
                break
            keywords_lines.append(line)
        keywords = "\n".join(keywords_lines)
        
        if not target_url or not ref_url_1:
            print("\n❌ Target URL en Referentie URL 1 zijn verplicht!")
            return
        
        # Volledige GEO-optimalisatie prompt
        ref_urls_text = f"{ref_url_1}" + (f" en {ref_url_2}" if ref_url_2 else "")
        keywords_text = keywords if keywords else "N/A"
        
        # Natuurlijke, mensvriendelijke instructie voor output (TL;DR + natuurlijke koppen)
        ref_urls_text = f"{ref_url_1}" + (f" en {ref_url_2}" if ref_url_2 else "")
        keywords_text = keywords if keywords else "N/A"

        prompt = f\"\"\"LET OP: Schrijf natuurlijk en mensvriendelijk — voer de richtlijnen uit zonder ze letterlijk woord-voor-woord in de tekst te herhalen.
Lever de output in Markdown en houd altijd de tone of voice van de referentie-artikelen aan.

Structuur & stijl (voorkeuren, maar wees natuurlijk):
- Titel: één H1.
- Begin met een korte TL;DR in Q&A-formaat (precies 3 korte Q&A's).
  - Kies de wording van de H2-kop op basis van de tone of voice van de referentie-artikelen:
    * Als de tone of voice formeel/professioneel is, gebruik de kop: `## Samenvatting`
    * Als de tone of voice informeel/tech-savvy is, gebruik de kop: `## TL;DR`
    * Anders kies een natuurlijke formulering die past bij de klant (bijv. `## Belangrijkste vragen en antwoorden`)
  - De H2-regel moet beginnen met `## ` zodat downstream parsers het als een echte heading herkennen.
  - Gebruik NIET letterlijk de frase "Kernvragen beantwoord".
  - Antwoorden = 1-2 zinnen, bondig en helder.
- Houd daarna logische H2/H3-hiërarchie aan voor hoofdsecties; H2 voor top-level onderwerpen, H3 voor subthema's.
- Beperk paragrafen tot 1-4 zinnen; voorkom walls of text.
- Frontload key insights en gebruik semantische cues (bijv. "Key takeaway", "In summary") waar passend.
- Voor openingszinnen na headings: maak ze entity-dense (40–50 woorden met relevante entiteiten) maar natuurlijk lezend.
- Pas koppen en formuleringen aan naar de tone of voice van de referentie-artikelen — kies natuurlijke, klant-geschikte koppen in plaats van stijve technische labels.
- Output: Markdown met echte headings (#, ##, ###). Als strikt format vereist is door downstream tools, vermeld dat expliciet; anders prioriteer natuurlijke leesbaarheid.

Extra context:
- Target URL: {target_url}
- Referentie: {ref_urls_text}
- Keywords en focus: {keywords_text}

Begin nu met het lezen van de URLs en herschrijf het artikel volledig volgens deze richtlijnen.\"\"\" 
        
        print("\n" + "=" * 70)
        print("🔄 De AI leest de pagina's en herschrijft je artikel...")
        print("=" * 70)
        print()
        
        # Generate content
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Toon resultaat
        print("=" * 70)
        print("RESULTAAT:")
        print("=" * 70)
        print(response_text)
        print("=" * 70)
        
        # Opslaan optie
        save = input("\n💾 Opslaan als Markdown bestand? (j/n): ").strip().lower()
        if save == 'j':
            filename = f"geo-artikel-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response_text)
            print(f"✅ Opgeslagen als: {filename}")
        
        print("\n✅ Klaar!")
        
    except Exception as e:
        print(f"\n❌ Fout opgetreden: {str(e)}")
        print("\nMogelijke oorzaken:")
        print("- API key is ongeldig")
        print("- Geen toegang tot Gemini 2.0 Flash")
        print("- Netwerkproblemen")
        print("- Google Search tool niet beschikbaar voor je account")
        sys.exit(1)

if __name__ == "__main__":
    main()
