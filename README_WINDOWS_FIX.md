# Windows Beveiliging Blokkade Oplossen

Als Windows Defender of andere beveiliging Streamlit blokkeert, zijn er verschillende oplossingen:

## Optie 1: PowerShell Script (Aanbevolen)

1. **Open PowerShell als Administrator:**
   - Rechtsklik op Start menu
   - Kies "Windows PowerShell (Admin)" of "Terminal (Admin)"

2. **Voer dit commando uit:**
   ```powershell
   cd "C:\Users\TiborgWulffelevanMaa\OneDrive - Maatwerk Online\Documenten\geo-content-optimaliseren"
   .\fix_windows_block.ps1
   ```

3. **Of voer handmatig uit:**
   ```powershell
   Add-MpPreference -ExclusionPath "C:\Users\TiborgWulffelevanMaa\OneDrive - Maatwerk Online\Documenten\geo-content-optimaliseren"
   ```

## Optie 2: Via Windows Defender GUI

1. Open **Windows Security** (Windows Defender)
2. Ga naar **Virus & threat protection**
3. Klik op **Manage settings** onder Virus & threat protection settings
4. Scroll naar **Exclusions** en klik op **Add or remove exclusions**
5. Klik **Add an exclusion** → **Folder**
6. Selecteer de map: `C:\Users\TiborgWulffelevanMaa\OneDrive - Maatwerk Online\Documenten\geo-content-optimaliseren`

## Optie 3: Voor ICT (Groepbeleid)

Als je in een bedrijfsomgeving werkt, kan ICT helpen door:

1. **Groepbeleid aanpassen** om Streamlit toe te staan
2. **Firewall regel toevoegen** voor poort 8501
3. **AppLocker uitzondering** voor Python/Streamlit

**Informatie voor ICT:**
- Poort: 8501 (Streamlit default)
- Executable: `python.exe` en `streamlit.exe`
- Project path: `C:\Users\TiborgWulffelevanMaa\OneDrive - Maatwerk Online\Documenten\geo-content-optimaliseren`

## Optie 4: CLI Versie (Geen Streamlit nodig)

Als Streamlit niet werkt, gebruik de CLI versie:

```bash
python app_cli.py
```

Deze werkt zonder Streamlit en heeft dezelfde functionaliteit.

## Testen

Na het toevoegen van uitzonderingen, test of het werkt:

```bash
cd "C:\Users\TiborgWulffelevanMaa\OneDrive - Maatwerk Online\Documenten\geo-content-optimaliseren"
streamlit run app.py
```

Als het nog steeds niet werkt, controleer:
- Windows Event Viewer voor specifieke foutmeldingen
- Of er andere antivirus software actief is (bijv. McAfee, Norton)
- Of er firewall regels zijn die poort 8501 blokkeren
