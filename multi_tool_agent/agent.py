import fitz  # PyMuPDF
from google.adk.agents import Agent

def get_uud45_content(file_path: str) -> str:
    """
    Membaca dan mengekstrak seluruh teks dari file PDF UUD 1945.
    Mengembalikan teks lengkap atau string kosong jika gagal.
    """
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n\n" 
        
        if not full_text.strip():
            print("Peringatan: Dokumen PDF kosong atau tidak dapat dibaca.")
            return ""
        
        return full_text
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat membaca file PDF: {str(e)}")
        return ""

# --- Langkah Utama ---
# 1. Tentukan path ke file PDF Anda
UUD_FILE_PATH = "multi_tool_agent/UUD45 ASLI.pdf"

# 2. Baca konten PDF untuk dijadikan konteks
UUD_CONTEXT = get_uud45_content(UUD_FILE_PATH)

# 3. Buat instruksi yang sangat detail untuk agen
# Pastikan konteks berhasil dimuat sebelum membuat agent
if UUD_CONTEXT:
    instruction = f"""
    Anda adalah seorang ahli hukum tata negara Indonesia yang memiliki spesialisasi pada Undang-Undang Dasar 1945.
    Tugas utama Anda adalah menjawab semua pertanyaan pengguna secara akurat, lugas, dan mudah dipahami **hanya berdasarkan teks lengkap UUD 1945** yang telah disediakan di bawah ini.
    Jangan menggunakan informasi dari sumber lain. Semua jawaban harus merujuk kembali ke pasal-pasal atau bagian dalam dokumen ini.

    Berikut adalah isi lengkap dari UUD 1945 sebagai satu-satunya sumber pengetahuan Anda:
    ---
    {UUD_CONTEXT}
    ---
    Jawablah pertanyaan pengguna dengan mengutip pasal yang relevan jika memungkinkan untuk memperkuat jawaban Anda.
    """
else:
    # Fallback jika PDF gagal dimuat
    instruction = "Peringatan: Konten UUD 1945 tidak dapat dimuat. Saya tidak bisa menjawab pertanyaan dengan akurat."

# 4. Definisikan `root_agent` yang akan dimuat oleh server ADK
# Ini adalah satu-satunya objek Agent yang perlu ada di file ini.
root_agent = Agent(
    name="uud45_expert_agent",
    model="gemini-2.0-flash",
    description="Agent yang sangat ahli mengenai isi Undang-Undang Dasar 1945 berdasarkan dokumen yang disediakan.",
    instruction=instruction
)

print("✅ UUD 1945 Expert Agent berhasil didefinisikan dan siap dimuat oleh server ADK.")