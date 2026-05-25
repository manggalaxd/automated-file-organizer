 📁 Automated File Organizer with Auto-Purge System

Sistem otomatisasi lokal berbasis **Event-Driven Programming** menggunakan bahasa Python. Sistem ini dirancang untuk memantau, menganalisis, dan menyortir file yang masuk ke direktori tertentu (seperti `Downloads`) secara *real-time*, serta dilengkapi dengan mekanisme pembersihan otomatis (**Auto-Purge System**) untuk menjaga efisiensi ruang penyimpanan komputer (*disk space*).

Fitur Utama

1. Real-Time Automated Sorting: Memantau folder target secara instan menggunakan pustaka `watchdog` dan langsung memindahkan file baru ke folder kategori (Dokumen, Gambar, Video, dll.) berdasarkan ekstensinya.
2. Auto-Purge System: Pembersihan terjadwal otomatis setiap 24 jam untuk menghapus berkas usang yang berada di folder `Applications` dan `Compressed` apabila umurnya telah melewati batas 30 hari.
3. Smart Delay Handle: Menerapkan jeda I/O selama 1 detik untuk mencegah kegagalan pemindahan data yang belum selesai diunduh oleh browser secara sempurna (*corrupted file prevention*).
4. Clean Code Architecture: Kode program dipecah secara modular menganut *Single Responsibility Principle*, bebas dari *magic numbers*, dan dibekali penanganan error yang kokoh (*Robust Error Handling*).

 💻 Aturan Pemilahan Direktori

Penyortiran dan pembersihan otomatis diatur secara ketat berdasarkan aturan tabel berikut:

| Kategori Direktori | Jenis Berkas yang Ditampung | Cakupan Ekstensi Format | Target Auto-Purge |
| :--- | :--- | :--- | :--- |
| Dokumen | Berkas teks, spreadsheet, presentasi, dan catatan | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.md` | ❌ Aman (Disimpan) |
| Gambar | Dokumentasi visual, foto, dan aset grafis | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp` | ❌ Aman (Disimpan) |
| Video | Berkas rekaman multimedia bergerak | `.mp4`, `.mkv`, `.avi`, `.mov`, `.flv` | ❌ Aman (Disimpan) |
| Musik | Berkas klip audio dan rekaman suara | `.mp3`, `.wav`, `.flac`, `.m4a` | ❌ Aman (Disimpan) |
| Compressed | Berkas pengarsipan data terkompresi | `.zip`, `.rar`, `.7z`, `.tar.gz` | **✔️ Aktif (Hapus >30 Hari)** |
| Applications | Berkas mentah instalasi perangkat lunak | `.exe`, `.msi`, `.dmg`, `.deb` | **✔️ Aktif (Hapus >30 Hari)** |

---

## 🚀 Cara Instalasi & Menjalankan

1. Persiapan Lingkungan & Dependensi
Pastikan kamu sudah mengisolasi *environment* Python dan menginstal pustaka yang dibutuhkan:

```bash
# Membuat & mengaktifkan virtual environment
python -m venv venv
source venv/bin/activate  # Untuk Linux/macOS
.\venv\Scripts\activate   # Untuk Windows

# Instalasi library watchdog via requirements.txt
pip install -r requirements.txt
```

file-organizer/
│
├── venv/                      # Folder Virtual Environment Python
├── requirements.txt           # File daftar library (watchdog==4.0.0)
├── cleaner.pyw                # File kode utama Python (Background Mode)
├── run_satpam.bat             # File script launcher Windows
└── README.md                  # Dokumentasi ini
