

# ⚖️ Verijudge - AI Agent Pendamping Hakim Korupsi

**Verijudge** adalah proyek AI agent yang dirancang untuk membantu hakim dalam menganalisis, mempertimbangkan, dan memutuskan kasus **tindak pidana korupsi** di Indonesia secara transparan dan terdokumentasi. Agent ini menggunakan pendekatan **Retrieval-Augmented Generation (RAG)** yang dipadukan dengan **model Gemini 1.5 Flash** dari Google AI.

## 🎯 Tujuan Proyek

Proyek ini menjawab pertanyaan:

> _"Bisakah AI membantu hakim dalam menganalisis, mempertimbangkan, dan memutuskan kasus korupsi beserta hukuman yang sesuai?"_

Dengan membaca dan memahami dokumen hukum seperti:
- **UUD 1945**
- **KUHP**
- **UU Tindak Pidana Korupsi**
- **UU Pencucian Uang**
  
Verijudge dapat menjawab pertanyaan hukum secara kontekstual dan menyertakan **referensi pasal** sebagai dasar hukumnya.

---

## 🧠 Teknologi yang Digunakan

- Python
- [Streamlit](https://streamlit.io/) – UI dan deployment
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) – Ekstraksi teks dari PDF
- [Google Generative AI (Gemini 1.5 Flash)](https://ai.google.dev/)
- RAG (Retrieval-Augmented Generation)

---

## ⚙️ Cara Kerja

1. **Muat Dokumen PDF Hukum:**  
   Sistem membaca 6+ dokumen hukum dalam format PDF dan mengekstrak teks menggunakan `PyMuPDF`.

2. **Gabungkan Konteks:**  
   Semua isi dokumen digabung menjadi satu konteks besar yang digunakan oleh model.

3. **Bangun Prompt Dinamis:**  
   Prompt disusun secara otomatis dan berisi:
   - Instruksi sistem (AI sebagai ahli hukum)
   - Teks hukum
   - Pertanyaan dari pengguna

4. **Jawaban dari Model:**  
   Pertanyaan dikirim ke **Gemini 1.5 Flash** dan dijawab berdasarkan konteks hukum, lengkap dengan sumber pasal yang relevan.

---

## 🚀 Cara Menjalankan (Lokal)

### 1. Instalasi dependensi

```bash
pip install -r requirements.txt

2. Siapkan API Key Google AI

Buat file .env di root folder:

GOOGLE_API_KEY=your_google_api_key_here

3. Jalankan dengan Streamlit

streamlit run app.py

> 📌 Catatan: Pastikan file PDF hukum berada di folder yang sama dengan file Python agent.py.




---

📉 Tantangan yang Dihadapi

📄 Dokumen rusak atau berbentuk gambar (scan) menyulitkan proses ekstraksi teks.

⏱️ Keterbatasan waktu untuk mempelajari konsep RAG dari nol.

🔋 Kendala teknis seperti baterai laptop habis saat pengembangan 😅


Namun, aplikasi berhasil dijalankan secara lokal dengan Streamlit!


---

🛣️ Rencana Pengembangan Selanjutnya

✅ Tambahkan semantic search agar pencarian konteks lebih akurat.

☁️ Deploy ke Streamlit Cloud untuk akses online.

🎙️ Integrasi speech-to-text agar pengguna bisa bertanya lewat suara.

📚 Penambahan dataset hukum lainnya agar cakupan lebih luas.



---

📎 Contoh Pertanyaan

Apa hukuman untuk seseorang yang menyuap pejabat negara?

Contoh Jawaban (dari Verijudge):

> Berdasarkan Pasal 5 ayat (1) huruf a UU No. 31 Tahun 1999, pemberi suap dapat dikenakan pidana penjara paling lama 5 tahun dan/atau denda paling banyak Rp250.000.000.




---

📁 Struktur File Penting

├── app.py                # Entry point Streamlit
├── agent.py              # Kelas SimpleRAG (retrieval dan query)
├── .env                  # API Key lokal (jika tidak pakai Streamlit secrets)
├── requirements.txt      # Semua dependensi Python
├── UUD45 ASLI.pdf        # Contoh file dokumen hukum
├── ...


---

🧑‍💻 Kontributor

Nama: Mohammad Iqbal Jaffar

Peran: AI Engineer, Prompt Engineer, Streamlit Developer

Tujuan: Menguji kemampuan RAG dan penerapannya dalam dunia hukum Indonesia 🇮🇩



---

🏛️ Penutup

Verijudge adalah langkah awal untuk menjawab tantangan kompleks dalam penegakan hukum dengan bantuan AI. Meski belum sempurna, proyek ini membuktikan bahwa AI dapat memberikan dampak nyata dalam transparansi hukum dan kepercayaan publik.

> ✨ "Hukum adalah cahaya keadilan, dan AI bisa jadi lentera yang membantunya bersinar lebih terang." – Verijudge Vision



