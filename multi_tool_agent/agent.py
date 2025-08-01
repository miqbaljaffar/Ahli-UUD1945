import fitz  # PyMuPDF
from google.adk.agents import Agent
import os

def get_pdf_content(file_path: str) -> str:
    """
    Membaca dan mengekstrak seluruh teks dari file PDF.
    Mengembalikan teks lengkap atau string kosong jika gagal.
    """
    try:
        if not os.path.exists(file_path):
            print(f"PERINGATAN: File tidak ditemukan di path: {file_path}")
            return ""
            
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n\n" 
        
        if not full_text.strip():
            print(f"Peringatan: Dokumen PDF {file_path} kosong atau tidak dapat dibaca.")
            return ""
        
        return full_text
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat membaca file PDF {file_path}: {str(e)}")
        return ""

# --- Langkah Utama ---
# 1. Tentukan path ke semua file PDF yang relevan untuk hukum korupsi
LAW_FILES_DIR = "multi_tool_agent/"
LAW_FILE_PATHS = [
    os.path.join(LAW_FILES_DIR, "UU Nomor 31 Tahun 1999.pdf"),
    os.path.join(LAW_FILES_DIR, "UU Nomor 19 Tahun 2019.pdf"),
    os.path.join(LAW_FILES_DIR, "UU Nomor 8 Tahun 2010.pdf"),
    os.path.join(LAW_FILES_DIR, "Kitab-Undang-undang-Hukum-Pidana_KUHP.pdf"),
    os.path.join(LAW_FILES_DIR, "part 1.pdf") # Yurisprudensi MA
]

# 2. Baca konten dari semua PDF untuk dijadikan konteks gabungan
all_law_context = ""
print("Memuat dokumen hukum...")
for path in LAW_FILE_PATHS:
    print(f"Membaca file: {os.path.basename(path)}")
    content = get_pdf_content(path)
    if content:
        all_law_context += f"--- DOKUMEN DARI FILE: {os.path.basename(path)} ---\n\n"
        all_law_context += content
        all_law_context += "\n\n--- AKHIR DOKUMEN ---\n\n"

# 3. Buat instruksi yang sangat detail untuk agen
# Pastikan konteks berhasil dimuat sebelum membuat agent
if all_law_context:
    instruction = f"""
    Anda adalah seorang ahli hukum Indonesia dengan spesialisasi tinggi dalam bidang tindak pidana korupsi.
    Tugas utama Anda adalah untuk menjawab semua pertanyaan pengguna secara akurat, komprehensif, dan mudah dipahami **hanya berdasarkan teks lengkap dari peraturan perundang-undangan dan yurisprudensi** yang telah disediakan di bawah ini.
    Jangan gunakan pengetahuan eksternal atau informasi dari sumber lain. Semua jawaban Anda harus merujuk kembali ke pasal-pasal atau bagian dalam dokumen-dokumen ini.

    Berikut adalah isi lengkap dari peraturan perundang-undangan yang menjadi satu-satunya sumber pengetahuan Anda:
    
    {all_law_context}
    
    Saat menjawab, ikuti panduan berikut:
    1.  **Akurasi Tinggi**: Pastikan setiap jawaban didasarkan sepenuhnya pada teks yang diberikan.
    2.  **Sebutkan Sumber**: Wajib mengutip dasar hukum dari jawaban Anda (contoh: "Berdasarkan Pasal 2 UU No. 31 Tahun 1999...").
    3.  **Jawaban Terstruktur**: Sajikan jawaban dengan jelas dan logis. Gunakan poin-poin jika diperlukan untuk menjelaskan konsep yang kompleks.
    4.  **Netral dan Objektif**: Jangan memberikan opini pribadi. Tetaplah berpegang pada interpretasi hukum yang ada dalam dokumen.
    """
else:
    # Fallback jika PDF gagal dimuat
    instruction = "Peringatan: Konten hukum korupsi tidak dapat dimuat. Saya tidak bisa menjawab pertanyaan dengan akurat."

# 4. Definisikan `root_agent` yang akan dimuat oleh server ADK
root_agent = Agent(
    name="corruption_law_expert_agent",
    model="gemini-2.0-flash",
    description="Agent ahli hukum yang berspesialisasi dalam tindak pidana korupsi berdasarkan dokumen hukum yang disediakan.",
    instruction=instruction
)

print("✅ Corruption Law Expert Agent berhasil didefinisikan dan siap dimuat oleh server ADK.")