import streamlit as st
import google.generativeai as genai
import time
import threading

# Configuratie van de pagina
st.set_page_config(page_title="GEO Content Optimizer", page_icon="🚀")

st.title("🚀 GEO Specialist: Content Optimizer")
st.markdown("Optimaliseer je content voor LLM's zoals Gemini & ChatGPT.")

# Zijbalk voor instellingen
st.sidebar.header("Instellingen")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

st.sidebar.markdown("### 🌡️ Temperature Controls")
st.sidebar.markdown("*Vind je perfecte sweet spot voor optimalisatie*")

content_temp = st.sidebar.slider(
    "📝 Content Creativiteit",
    0.0, 2.0, 0.4, 0.1,
    help="Hoe creatief mag de AI zijn met woorden/formuleringen?\n\n0.0-0.3: Behoud origineel maximaal\n0.4-0.7: Lichte optimalisatie\n0.8-1.5: Mag flink herschrijven\n1.6-2.0: Zeer creatief"
)

structure_temp = st.sidebar.slider(
    "🏗️ Structuur Vrijheid",
    0.0, 2.0, 0.8, 0.1,
    help="Hoe vrij mag de AI zijn met GEO-regels?\n\n0.0-0.3: Volg regels LETTERLIJK (gevaarlijk!)\n0.4-0.7: Intelligente toepassing\n0.8-1.2: Gebruik gezond verstand\n1.3-2.0: Creatief met structuur"
)

# Toon aanbeveling
if content_temp < 0.3 and structure_temp < 0.4:
    st.sidebar.warning("⚠️ Beide sliders laag = mogelijk onnatuurlijk resultaat")
elif content_temp < 0.5 and structure_temp > 0.7:
    st.sidebar.success("✅ Goede combinatie voor 'light touch' optimalisatie")
elif content_temp > 1.2 and structure_temp > 1.2:
    st.sidebar.info("💡 Beide hoog = maximale AI vrijheid")

if api_key:
    genai.configure(api_key=api_key)
    
    # Gebruik werkend model
    @st.cache_resource
    def get_model(_temp_value):
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
                test_response = model.generate_content("test")
                if test_response and hasattr(test_response, 'text'):
                    return model, model_name
            except Exception:
                continue
        
        raise Exception("Geen werkend Gemini model gevonden.")
    
    try:
        model, model_info = get_model(content_temp)
        st.sidebar.success(f"Model: {model_info}")
    except Exception as e:
        st.sidebar.error(f"Model fout: {str(e)}")
        st.stop()

    # CC Licentie tip
    st.info("💡 **Bonus Tip voor Extra Vindbaarheid:** Overweeg een [CC BY 4.0 licentie](https://creativecommons.org/chooser/) toe te voegen aan je artikel. Dit vergroot de kans dat LLM's je content gebruiken als trainingsdata en verwijzen naar je werk. Voeg ook `Updated YYYY-MM-DD` toe aan je pagina voor recency signals.")

    # Input velden
    target_url = st.text_input("Target URL (Te optimaliseren artikel)")
    ref_url_1 = st.text_input("Referentie URL 1 (Tone of Voice)")
    ref_url_2 = st.text_input("Referentie URL 2 (Tone of Voice)")
    keywords = st.text_area("Belangrijke Keywords & Focus")

    # Extra optimalisatie opties
    st.markdown("### 🎯 Extra Optimalisatie Opties")
    col1, col2 = st.columns(2)
    
    with col1:
        entity_optimization = st.checkbox("🔤 Entity-Based Optimalisatie", help="Verrijk eerste zinnen na koppen met specifieke entities (40-50 woorden)")
        add_facts_table = st.checkbox("📊 Voeg Feiten Tabel toe", help="AI voegt een compacte feiten tabel toe op natuurlijke plek in artikel")
    
    with col2:
        if entity_optimization:
            entity_keywords = st.text_input("Entities (komma gescheiden)", placeholder="product naam, bedrijf, locatie, technologie")
        else:
            entity_keywords = ""

    if st.button("Start GEO-Optimalisatie"):
        if target_url and ref_url_1:
            # Eerlijke progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Voorbereiding
            status_text.markdown("🔄 **AI analyseert URLs en optimaliseert artikel...**")
            progress_bar.progress(5)
            
            # Bepaal structuur style op basis van structure_temp
            if structure_temp < 0.4:
                structure_style = "STRIKT - Volg alle regels letterlijk"
            elif structure_temp < 1.0:
                structure_style = "GEBALANCEERD - Gebruik gezond verstand"
            else:
                structure_style = "FLEXIBEL - Creatieve vrijheid met structuur"
            
            # Bouw dynamische prompt
            ref_urls_text = f"{ref_url_1}" + (f" en {ref_url_2}" if ref_url_2 else "")
            keywords_text = keywords if keywords else "N/A"
            
            # Entity instructies
            entity_instruction = ""
            if entity_optimization and entity_keywords:
                entity_instruction = f"""

ENTITY OPTIMALISATIE (BELANGRIJK):
- Verrijk de eerste 40-50 woorden NA elke H2/H3 kop met deze entities: {entity_keywords}
- Doe dit NATUURLIJK - geen opsomming, maar verweven in de tekst
- Voorbeeld: "Grilling steak" → "Grilling steak on a Weber Kettle charcoal grill is easy when you season the beef ribeye with salt and olive oil"
- Pas ALLEEN toe op eerste zin(nen) na koppen, niet overal"""
            
            # Facts table instructies
            facts_table_instruction = ""
            if add_facts_table:
                facts_table_instruction = """

FEITEN TABEL:
- Voeg 1 compacte Markdown tabel toe (max 5-8 rijen)
- Plaats op natuurlijke plek (niet bovenaan, niet onderaan)
- Format: | Aspect | Detail |
- Voorbeeld onderwerpen: specificaties, tijdlijn, vergelijking, kernfeiten"""

            prompt = f"""KRITIEKE INSTRUCTIE: Dit is NIET een herschrijf-opdracht. Dit is een MINIMALE STRUCTUUR-OPTIMALISATIE.

STRUCTUUR AANPAK: {structure_style}

=== JE PRIMAIRE TAAK (in volgorde van prioriteit) ===

STAP 1 - KOPIEER DE ORIGINELE CONTENT:
Neem het artikel over zoals het is. Wijzig NIETS aan de inhoud, woorden of zinnen.

STAP 2 - VOEG TL;DR TOE (alleen deze toevoeging!):
- Plaats boven de eerste sectie (na H1)
- Maak 3 korte Q&A's die de kern samenvatten
- H2 kop: `## TL;DR` (informeel) of `## Samenvatting` (formeel)
- Elk antwoord: maximum 2 zinnen

STAP 3 - KOPPEN OPTIMALISEREN (enige wijzigingen toegestaan):
- Verander ALLEEN koppen die LLM-vindbaarheid missen
- Maak ze vraag-georiënteerd waar zinvol
- Voorbeeld: "ChatGPT Tips" → "Hoe gebruik je ChatGPT effectief?"
- BEHOUD alle originele woorden in de kop
- Maximaal 30-40% van koppen aanpassen

STAP 4 - PARAGRAFEN EN STRUCTUUR EXACT KOPIËREN:
- KOPIEER alle paragrafen precies zoals ze zijn (zelfde aantal zinnen!)
- Als origineel 4 zinnen in alinea heeft: behoud 4 zinnen
- Als origineel 2 zinnen in alinea heeft: behoud 2 zinnen
- SPLITS GEEN paragrafen - laat ze zoals ze zijn
- VERKORT GEEN paragrafen - alle zinnen moeten blijven
- KOPIEER alle bullets, nummers, tabellen exact zoals ze zijn
- Wijzig NIETS aan formattering
- Als origineel geen lijst gebruikt: voeg er GEEN toe
- Als origineel wel lijst gebruikt: behoud het exact{entity_instruction}{facts_table_instruction}

=== ABSOLUUT VERBODEN ===
❌ Zinnen herschrijven
❌ Woorden vervangen door synoniemen
❌ Paragrafen splitsen of herstructureren
❌ Paragrafen inkorten tot 1-2 zinnen (BEHOUD originele lengte!)
❌ Zinnen uit paragrafen weglaten
❌ Semantic cues toevoegen aan bestaande tekst
❌ "Frontloading" van content
❌ Lijsten toevoegen waar ze niet waren
❌ Tone aanpassen
❌ Alinea's korter maken dan origineel

=== WAT JE MAG DOEN ===
✅ TL;DR toevoegen (nieuw)
✅ H2/H3 koppen als vraag formuleren (bewaar originele woorden)
✅ Bestaande lijsten/tabellen exact kopiëren
✅ NIETS anders

=== MINDSET ===
Denk als een "copy-paste editor" die alleen:
1. TL;DR toevoegt
2. Koppen optimaliseert
3. Rest exact kopieert (inclusief alle zinnen in elke paragraaf!)

De klant is al 100% blij met de content. Jij maakt het alleen beter vindbaar voor LLM's door minimale strukturele aanpassingen.

CRUCIALE REGEL: Als een originele paragraaf 5 zinnen heeft, moet jouw output ook 5 zinnen hebben in die paragraaf. VERKORT NIETS.

=== CONTEXT ===
Target URL: {target_url}
Referentie URLs: {ref_urls_text}
Keywords/Focus: {keywords_text}

Begin nu met het lezen van de URLs en optimaliseer volgens deze instructies."""

            # Simuleer progress tijdens API call met threading
            def update_progress():
                for i in range(5, 95, 5):
                    time.sleep(2)
                    progress_bar.progress(i)
            
            progress_thread = threading.Thread(target=update_progress)
            progress_thread.start()
            
            try:
                # Generate content
                response = model.generate_content(prompt)
                
                # Stop progress thread
                progress_thread.join(timeout=0.1)
                
                status_text.markdown("🔄 **Content wordt verwerkt...**")
                progress_bar.progress(98)
                
                response_text = response.text
                
                status_text.markdown("✅ **Optimalisatie voltooid!**")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                # Clear progress
                progress_bar.empty()
                status_text.empty()
                
                st.markdown("---")
                st.markdown(response_text)
                
                # Download knop
                st.download_button("📥 Download als Markdown", response_text, file_name="geo-artikel.md")
                
            except Exception as e:
                progress_thread.join(timeout=0.1)
                progress_bar.empty()
                status_text.empty()
                st.error(f"Er is een fout opgetreden: {str(e)}")
                st.info("Controleer of je API key geldig is en of je toegang hebt tot Gemini modellen.")
        else:
            st.warning("Vul a.u.b. de Target URL en minimaal één Referentie URL in.")
else:
    st.info("Voer je Gemini API Key in de zijbalk in om de tool te activeren.")
