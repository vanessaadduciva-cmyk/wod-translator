
import streamlit as st
from PIL import Image
import requests
import io
from gtts import gTTS
import tempfile

# -----------------------
# CONFIG
# -----------------------
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
    ["normale", "drammatico divertente"]
)

voce = st.toggle("🎤 Attiva voce coach")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# OCR SPACE
# -----------------------
def estrai_testo(img):
    url = "https://api.ocr.space/parse/image"

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")

    files = {
        "file": ("image.png", buffered.getvalue())
    }

    payload = {
        "apikey": "helloworld",
        "language": "ita"
    }

    response = requests.post(url, data=payload, files=files)
    result = response.json()

    try:
        return result["ParsedResults"][0]["ParsedText"]
    except:
        return "Errore nella lettura del testo"

# -----------------------
# GENERAZIONE TESTO (LOGICA SMART)
# -----------------------
def genera_output(testo, battute, spiegazione, modalita):

    base = f"Questo è il WOD:\n{testo}\n\n"

    # Spiegazione
    if spiegazione == "ultra semplificate":
        spieg = "Devi fare questi esercizi uno dopo l'altro, cercando di non fermarti. È molto faticoso."
    elif spiegazione == "base":
        spieg = "È un circuito di esercizi che combina cardio e forza. Più vai avanti, più diventa difficile mantenere il ritmo."
    else:
        spieg = "Questo WOD combina lavoro cardiovascolare e forza muscolare, con un accumulo progressivo di fatica su gambe e core."

    # Aneddoto
    aneddoto = "Una volta pensavo fosse facile… dopo 5 minuti stavo già rivalutando tutte le mie scelte di vita."

    # Battute
    if battute == "sportive":
        jokes = "Questo WOD ti costruisce. O ti distrugge. Non c'è via di mezzo."
    elif battute == "amichevoli":
        jokes = "A metà allenamento inizierai a chiederti chi te l'ha fatto fare 😄"
    elif battute == "flirt":
        jokes = "Se resisti fino alla fine… potrei iniziare a trovarti interessante 😏"
    else:
        jokes = "Se reggi questo WOD… ho decisamente bisogno di conoscerti meglio 😌🔥"

    # Stile
    if modalita == "drammatico divertente":
        finale = "Questo non è allenamento. È un viaggio emotivo. Preparati."
    else:
        finale = "Dai il massimo e sopravvivi 💪"

    return f"""
🔍 Spiegazione  
{spieg}

😄 Aneddoto  
{aneddoto}

🔥 Battute  
{jokes}

🎤 Chiusura  
{finale}
"""

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

        with st.spinner("⏳ Analisi in corso..."):

            testo = estrai_testo(image)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📄 Testo estratto")
            st.code(testo)
            st.markdown('</div>', unsafe_allow_html=True)

            risultato = genera_output(
                testo,
                tipo_battute,
                tipo_spiegazione,
                modalita
            )

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(risultato)
            st.markdown('</div>', unsafe_allow_html=True)

            if voce:
                audio = genera_voce(risultato)
                st.audio(audio)
