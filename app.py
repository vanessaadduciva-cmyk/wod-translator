import streamlit as st
from PIL import Image
import pytesseract
from openai import OpenAI
from gtts import gTTS
import tempfile

# -----------------------
# CONFIG
# -----------------------
client = OpenAI(api_key="YOUR_API_KEY")

st.set_page_config(
    page_title="WOD Translator ELITE",
    page_icon="🔥",
    layout="centered"
)

# -----------------------
# CSS PREMIUM
# -----------------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0e1117, #141821);
    color: white;
}
.block-container {
    padding-top: 1.5rem;
}
.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    animation: fadeIn 0.6s ease-in-out;
}
.title {
    font-size: 34px;
    font-weight: 700;
}
.subtitle {
    color: #9aa0a6;
    margin-bottom: 25px;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown('<div class="title">🔥 WOD Translator ELITE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Trasforma un WOD in esperienza 😏</div>', unsafe_allow_html=True)

# -----------------------
# UPLOAD
# -----------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📸 Carica il tuo WOD", type=["png", "jpg", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# PARAMETRI
# -----------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### 🎯 Personalizza")

col1, col2 = st.columns(2)

with col1:
    battute = st.selectbox(
        "Battute",
        ["sportive", "amichevoli", "flirt", "flirt spinto"]
    )

with col2:
    spiegazione = st.selectbox(
        "Spiegazione",
        ["tecniche", "base", "ultra semplificate"]
    )

modalita = st.selectbox(
    "Stile",
    ["normale", "drammatico divertente", "coach cinematografico"]
)

voce = st.toggle("🎤 Attiva voce coach")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# OCR
# -----------------------
def estrai_testo(img):
    return pytesseract.image_to_string(img).strip()

# -----------------------
# PROMPT SMART
# -----------------------
def genera_prompt(testo, battute, spiegazione, modalita):

    tono_extra = ""

    if modalita == "drammatico divertente":
        tono_extra = "tono teatrale, ironico, esagerato"
    elif modalita == "coach cinematografico":
        tono_extra = "tono motivazionale epico, stile film sportivo"

    return f"""
Analizza questo WOD:
\"\"\"{testo}\"\"\"

PARAMETRI:
- Spiegazione: {spiegazione}
- Battute: {battute}
- Stile: {modalita}

ISTRUZIONI:

Spiegazione:
- tecniche → dettagli su muscoli, strategia
- base → chiara e semplice
- ultra semplificate → super facile

Battute:
- sportive → motivazionali
- amichevoli → leggere
- flirt → seduttive leggere
- flirt spinto → più dirette ma non volgari

Stile:
- {tono_extra}

AGGIUNGI:
- coinvolgimento emotivo
- ritmo narrativo

STRUTTURA:

🔍 Spiegazione
😄 Aneddoto
🔥 Battute
🎤 Chiusura ad effetto
"""

# -----------------------
# GPT
# -----------------------
def genera_output(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content

# -----------------------
# VOCE
# -----------------------
def genera_voce(testo):
    tts = gTTS(testo, lang='it')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name

# -----------------------
# MAIN
# -----------------------
if uploaded_file:
    image = Image.open(uploaded_file)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image(image, caption="WOD caricato", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("💥 Analizza WOD"):

        with st.spinner("⏳ Simulazione sofferenza in corso..."):

            testo = estrai_testo(image)

            if not testo:
                st.error("❌ Non sono riuscito a leggere il WOD")
            else:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### 📄 Testo estratto")
                st.code(testo)
                st.markdown('</div>', unsafe_allow_html=True)

                prompt = genera_prompt(testo, battute, spiegazione, modalita)
                risultato = genera_output(prompt)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### 🔥 Modalità: {modalita} | {battute} | {spiegazione}")
                st.write(risultato)
                st.markdown('</div>', unsafe_allow_html=True)

                # VOCE
                if voce:
                    audio_file = genera_voce(risultato)
                    st.audio(audio_file)
