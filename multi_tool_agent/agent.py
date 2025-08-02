import os
from pathlib import Path
import fitz  # PyMuPDF
import google.generativeai as genai
import streamlit as st # Ditambahkan untuk mengakses secrets saat deploy

# --- Konfigurasi API Key ---
# Fungsi ini akan mencoba mengambil API key dari secrets Streamlit (saat deploy)
# atau dari environment variable (saat dijalankan lokal dengan file .env)
def configure_genai():
    """Mengkonfigurasi API Key Google AI."""
    api_key = None
    try:
        # Prioritas pertama: Coba ambil dari secrets Streamlit
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except (AttributeError, FileNotFoundError):
        # Jika gagal (misalnya berjalan lokal), coba ambil dari environment variable
        print("Secrets Streamlit tidak ditemukan, mencoba environment variable...")
        api_key = os.getenv("GOOGLE_API_KEY")

    if api_key:
        genai.configure(api_key=api_key)
        print("API Key Google AI berhasil dikonfigurasi.")
    else:
        # Jika keduanya gagal, tampilkan error yang jelas
        error_message = "API Key Google AI tidak ditemukan. Pastikan Anda sudah mengatur GOOGLE_API_KEY di Secrets Streamlit (untuk deployment) atau di file .env (untuk lokal)."
        print(error_message)
        st.error(error_message) # Tampilkan juga di UI Streamlit

class SimpleRAG:
    """
    Kelas sederhana untuk melakukan Retrieval-Augmented Generation.
    Dia akan memuat dokumen dan memberikan konteks yang relevan ke model AI.
    """
    def __init__(self):
        self.texts = self._load_documents()
        if self.texts: # Hanya inisialisasi model jika dokumen berhasil dimuat
            self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        else:
            self.model = None
            print("Model tidak diinisialisasi karena tidak ada dokumen yang berhasil dimuat.")

    @st.cache_data(show_spinner=False) # Menggunakan cache agar PDF tidak dimuat ulang setiap saat
    def _load_documents(_self):
        """Memuat semua file PDF menjadi satu dictionary teks."""
        BASE_DIR = Path(__file__).parent.absolute()
        file_names = [
            "UUD45 ASLI.pdf",
            "UU Nomor 31 Tahun 1999.pdf",
            "UU Nomor 19 Tahun 2019.pdf",
            "UU Nomor  8 Tahun 2010.pdf",
            "Kitab-Undang-undang-Hukum-Pidana_KUHP.pdf",
            "part 1.pdf",
            "UUD45 ASLI.pdf"
        ]
        
        all_texts = {}
        print("Memuat dokumen hukum...")
        for file_name in file_names:
            file_path = BASE_DIR / file_name
            if file_path.exists():
                print(f"Membaca file: {file_name}")
                try:
                    with fitz.open(file_path) as doc:
                        all_texts[file_name] = "".join(page.get_text() for page in doc)
                except Exception as e:
                    print(f"Gagal membaca {file_name} karena error: {e}")
            else:
                print(f"PERINGATAN: File tidak ditemukan di {file_path}")
        
        if not all_texts:
            st.error("Tidak ada dokumen PDF yang berhasil dimuat. Pastikan file PDF ada di dalam folder yang sama dengan agent.py dan tidak rusak.")

        print("✅ Dokumen berhasil dimuat.")
        return all_texts

    def query(_self, question: str) -> str:
        """Menjawab pertanyaan menggunakan konteks dari dokumen."""
        if not _self.model:
            return "Model AI tidak dapat digunakan karena dokumen gagal dimuat atau API Key tidak valid."

        # Menggabungkan semua teks dari PDF menjadi satu konteks besar
        context = "\n\n--- PEMISAH DOKUMEN ---\n\n".join(_self.texts.values())

        # Membuat prompt yang terstruktur untuk model AI
        system_instruction = (
            "Anda adalah AI Ahli Hukum yang berspesialisasi dalam tindak pidana korupsi di Indonesia. "
            "Jawab pertanyaan pengguna HANYA berdasarkan konteks dari dokumen hukum yang disediakan di bawah ini. "
            "Setiap jawaban HARUS menyertakan sumber hukumnya (contoh: Berdasarkan Pasal X Undang-Undang Y...)."
        )
        
        prompt = f"""
        {system_instruction}

        --- AWAL DARI KONTEKS DOKUMEN HUKUM ---
        {context}
        --- AKHIR DARI KONTEKS DOKUMEN HUKUM ---

        PERTANYAAN PENGGUNA:
        {question}

        JAWABAN ANDA:
        """

        try:
            response = _self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Terjadi kesalahan saat menghubungi model AI: {e}"

# --- Inisialisasi Agent ---
# Pertama, konfigurasikan API key
configure_genai()
# Kemudian, buat satu instance dari RAG agent kita
rag_agent = SimpleRAG()
