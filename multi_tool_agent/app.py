# app.py (Versi Final yang Sudah Diperbaiki)

# Baris ini penting untuk memuat API Key dari file .env saat berjalan di komputer lokal
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from agent import rag_agent # Impor RAG agent yang sudah kita buat

# --- Konfigurasi Halaman Web ---
st.set_page_config(
    page_title="AI Ahli Hukum Korupsi",
    page_icon="⚖️",
    layout="centered"
)

# --- Judul dan Subjudul Aplikasi ---
st.title("⚖️ AI Ahli Hukum Korupsi")
st.caption("Tanyakan apapun terkait hukum korupsi di Indonesia berdasarkan peraturan yang berlaku.")

# --- Inisialisasi Riwayat Chat ---
# Menggunakan st.session_state agar riwayat chat tidak hilang saat aplikasi di-refresh
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selamat datang! Saya adalah AI yang dapat menjawab pertanyaan seputar hukum korupsi di Indonesia. Silakan ajukan pertanyaan Anda."}
    ]

# --- Menampilkan Riwayat Chat yang Sudah Ada ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Menerima Input dari Pengguna ---
if prompt := st.chat_input("Contoh: Apa saja unsur tindak pidana korupsi?"):
    # 1. Tambahkan pesan pengguna ke riwayat dan tampilkan di UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Dapatkan dan tampilkan respons dari AI
    with st.chat_message("assistant"):
        with st.spinner("AI sedang menganalisis dokumen hukum..."):
            # Panggil fungsi query dari agent kita
            response = rag_agent.query(prompt)
            st.markdown(response)
            # Tambahkan respons AI ke riwayat
            st.session_state.messages.append({"role": "assistant", "content": response})
