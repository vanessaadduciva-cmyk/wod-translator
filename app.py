import streamlit as st
from PIL import Image
from openai import OpenAI
import base64
import io
from gtts import gTTS
import tempfile

# -----------------------
# CONFIG
# -----------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="WOD Translator ELITE",
    page_icon="🔥",
    layout="centered"
)

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0e1117, #141821);
    color: white;
}
.card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.title {
    font-size: 34px;
    font-weight: bold;
}
.subtitle {
    color: #9aa0a6;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown('<div class="title">🔥 WOD Translator ELITE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Scopri quanto soffrirai… prima di iniziare 😏</div>', unsafe_allow_html=True)

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
    tipo_battute = st.selectbox(
        "Battute",
        ["sportive", "amichevoli", "flirt", "flirt spinto"]
    )

with col2:
    tipo_spiegazione = st.selectbox(
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
# OCR con AI (FUNZIONA SU CLOUD)
# -----------------------
def estrai_testo(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Leggi e trascrivi il testo presente in questa immagine di un WOD di crossfit. Mantieni struttura e numeri."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_base64}"}
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content


# -----------------------
# PROMPT
# -----------------------
def genera_prompt(testo, battute, spiegazione, modalita):

    tono = ""

    if modalita == "drammatico divertente":
        tono = "tono teatrale, ironico ed esagerato"
    elif modalita == "coach cinematografico":
        tono = "tono epico motivazionale stile film sportivo"

    return f"""
Analizza questo WOD:

{testo}

PARAMETRI:
- Spiegazione: {spiegazione}
- Battute: {battute}
- Stile: {modalita}

ISTRUZIONI:

Spiegazione:
- tecniche → dettagli su muscoli e strategia
- base → semplice e chiara
- ultra semplificate → facilissima

Battute:
- sportive → motivazionali
- amichevoli → leggere
- flirt → seduttive leggere
- flirt spinto → più dirette ma non volgari

Stile:
- {tono}

Struttura:

🔍 Spiegazione
😄 Aneddoto
🔥 Battute
🎤 Chiusura ad effetto
"""


# -----------------------
# GPT OUTPUT
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

        with st.spinner("⏳ Analisi in corso... preparati mentalmente..."):

            testo = estrai_testo(image)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📄 Testo estratto")
            st.code(testo)
            st.markdown('</div>', unsafe_allow_html=True)

            prompt = genera_prompt(
                testo,
                tipo_battute,
                tipo_spiegazione,
                modalita
            )

            risultato = genera_output(prompt)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### 🔥 Modalità: {modalita} | {tipo_battute} | {tipo_spiegazione}")
            st.write(risultato)
            st.markdown('</div>', unsafe_allow_html=True)

            if voce:
                audio = genera_voce(risultato)
                st.audio(audio)
