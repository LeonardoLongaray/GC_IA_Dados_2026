import streamlit as st

st.set_page_config(
    page_title="Agente de Áudio",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Agente de Áudio")
st.write(
    "Envie uma gravação para gerar "
    "uma transcrição e um relatório."
)

audio = st.file_uploader(
    "Selecione seu arquivo de áudio",
    type=["mp3", "wav", "m4a", "ogg"]
)

if audio:
    st.success(f"Arquivo recebido: {audio.name}")
    st.write(f"Tamanho: {audio.size / 1024:.2f} KB")

    st.info("A transcrição será implementada em uma próxima etapa.")
