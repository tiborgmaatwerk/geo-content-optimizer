import streamlit as st
import google.generativeai as genai

# Configuratie van de pagina
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀")

st.title("🚀 GEO Specialist: Content Optimizer")
st.markdown("Optimaliseer je content voor LLM's zoals Gemini & ChatGPT.")

# Zijbalk voor instellingen
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
temp_value = st.sidebar.slider("Creativiteit (Temperatuur)", 0.0, 2.0, 0.7, 0.1)

if api_key:
    genai.configure(api_key=api_key)
    
    # Gebruik werkend model (getest: gemini-pro-latest werkt)
    @st.cache_resource
    def get_model(_temp_value):
        # Probeer eerst nieuwere modellen, dan fallback naar gemini-pro-latest
        model_names = [
            'gemini-2.5-flash',
            'gemini-2.0-flash',
            'gemini-pro-latest'
        ]
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"temperature": _temp_value}
                )
                # Test of het werkt
                test_response = model.generate_content("test")
                if test_response and hasattr(test_response, 'text'):
                    return model, model_name
            except Exception:
                continue
        
        raise Exception("Geen werkend Gemini model gevonden.")
    
    try:
        model, model_info = get_model(temp_value)
        st.sidebar.success(f"Model: {model_info}")
    except Exception as e:
        st.sidebar.error(f"Model fout: {str(e)}")
        st.stop()

    # Input velden
    target_url = st.text_input("Target URL (Te optimaliseren artikel)")
    ref_url_1 = st.text_input("Referentie URL 1 (Tone of Voice)")
    ref_url_2 = st.text_input("Referentie URL 2 (Tone of Voice)")
    keywords = st.text_area("Belangrijke Keywords & Focus")

    if st.button("Start GEO-Optimalisatie"):
        if target_url and ref_url_1:
            with st.spinner('De AI leest de pagina\'s en herschrijft je artikel...'):
                # Natuurlijke, mensvriendelijke instructie voor output (TL;DR + natuurlijke koppen)
                ref_urls_text = f"{ref_url_1}" + (f" en {ref_url_2}" if ref_url_2 else "")
                keywords_text = keywords if keywords else "N/A"

                prompt = f"""LET OP: Schrijf natuurlijk en mensvriendelijk — voer de richtlijnen uit zonder ze letterlijk woord-voor-woord in de tekst te herhalen.
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

Begin nu met het lezen van de URLs en herschrijf het artikel volledig volgens deze richtlijnen.""" 
                
                try:
                    # Generate content - Google Search tool wordt automatisch gebruikt indien nodig
                    response = model.generate_content(prompt)
                    
                    # Extract text from response
                    response_text = response.text
                    
                    st.markdown("---")
                    st.markdown(response_text)
                    
                    # Download knop voor de klant
                    st.download_button("Download als Markdown", response_text, file_name="geo-artikel.md")
                except Exception as e:
                    st.error(f"Er is een fout opgetreden: {str(e)}")
                    st.info("Controleer of je API key geldig is en of je toegang hebt tot Gemini 2.0 Flash.")
        else:
            st.warning("Vul a.u.b. de Target URL en minimaal één Referentie URL in.")
else:
    st.info("Voer je Gemini API Key in de zijbalk in om de tool te activeren.")