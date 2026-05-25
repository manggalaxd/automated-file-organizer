import os
import shutil
import time
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# GLOBAL CONFIGURATION

TARGET_DIRECTORY = os.path.expanduser("~/Downloads") #SUMBER FILE YANG AKAN DIAWASI
I_O_DELAY_SECONDS = 1 #JEDA AMAN UNTUK MEMASTIKAN PROSES PENULISAN FILE SELESAI SEBELUM DILAKUKAN PEMINDAHAN
RETENTION_DAYS = 30 #BATAS WAKTU RETENSI UNTUK FILE USANG (DENGAN SATUAN HARI) YANG AKAN DIHAPUS OLEH SISTEM AUTO-PURGE

EXTENSION_MAPPING = {
    'Dokumen': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md'],
    'Gambar': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
    'Video': ['.mp4', '.mkv', '.avi', '.mov', '.flv'],
    'Musik': ['.mp3', '.wav', '.flac', '.m4a'],
    'Compressed': ['.zip', '.rar', '.7z', '.tar.gz'],
    'Applications': ['.exe', '.msi', '.dmg', '.deb']
}

PURGE_TARGET_CATEGORIES = ['Compressed', 'Applications']


# FILE ORGANIZER MODULE
class FileOrganizer:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def get_file_extension(self, file_path):
        """Mengisolasi ekstensi file dan mengubahnya ke huruf kecil."""
        _, extension = os.path.splitext(file_path)
        return extension.lower()

    def ensure_directory_exists(self, directory_path):
        """Membuat direktori jika belum tersedia di sistem."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def organize_file(self, file_path):
        """Memeriksa ekstensi file dan memindahkannya ke folder kategori."""
        if os.path.isdir(file_path):
            return

        file_name = os.path.basename(file_path)
        file_extension = self.get_file_extension(file_name)
        
        # Jeda aman untuk memastikan browser selesai menulis data ke disk
        time.sleep(I_O_DELAY_SECONDS)

        for category, extensions in EXTENSION_MAPPING.items():
            if file_extension in extensions:
                target_folder = os.path.join(self.base_directory, category)
                self.ensure_directory_exists(target_folder)
                
                destination_path = os.path.join(target_folder, file_name)
                
                try:
                    shutil.move(file_path, destination_path)
                    print(f"[SUKSES] {file_name} -> Folder {category}")
                except Exception as error:
                    print(f"[ERROR] Gagal memindahkan {file_name}. Log: {error}")
                break

# 3. AUTO-PURGE SYSTEM MODULE (MODUL PEMBERSIH SAMPAH)
class AutoPurgeSystem:
    def __init__(self, base_directory, expiration_days):
        self.base_directory = base_directory
        self.expiration_threshold = timedelta(days=expiration_days)

    def is_file_older_than_threshold(self, file_path):
        """Mengecek apakah umur file berdasarkan waktu modifikasi > batas retensi."""
        file_modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        current_time = datetime.now()
        return (current_time - file_modification_time) > self.expiration_threshold

    def execute_purge(self):
        """Menghapus file usang di folder target yang melebihi batas waktu."""
        print(f"\n[AUTO-PURGE] Memulai pembersihan berkala (Batas: {RETENTION_DAYS} hari)...")
        for category in PURGE_TARGET_CATEGORIES:
            target_folder = os.path.join(self.base_directory, category)
            
            if not os.path.exists(target_folder):
                continue
                
            for file_name in os.listdir(target_folder):
                file_path = os.path.join(target_folder, file_name)
                
                if os.path.isfile(file_path) and self.is_file_older_than_threshold(file_path):
                    try:
                        os.remove(file_path)
                        print(f"[PURGED] Berhasil menghapus file usang: {file_name}")
                    except Exception as error:
                        print(f"[ERROR] Gagal menghapus {file_name}. Log: {error}")
        print("[AUTO-PURGE] Pembersihan selesai.\n")


# 4. EVENT HANDLER BRIDGE (JEMBATAN EVENT KERNEL)
class ManggalaHandler(FileSystemEventHandler):
    def __init__(self, organizer):
        self.organizer = organizer

    def on_created(self, event):
        """Merespons event ketika ada file baru yang masuk."""
        self.organizer.organize_file(event.src_path)


# 5. MAIN APPLICATION RUNNER (EKSEKUTOR UTAMA)
if __name__ == "__main__":
    # Injeksi dependensi objek
    organizer = FileOrganizer(TARGET_DIRECTORY)
    purger = AutoPurgeSystem(TARGET_DIRECTORY, RETENTION_DAYS)
    
    # Jalankan pembersihan awal saat script pertama kali dinyalakan
    purger.execute_purge()

    # Inisialisasi Watchdog Observer
    event_handler = ManggalaHandler(organizer)
    observer = Observer()
    observer.schedule(event_handler, path=TARGET_DIRECTORY, recursive=False)
    observer.start()
    
    print(f"Satpam Python Aktif! Memantau direktori: {TARGET_DIRECTORY}")
    
    last_purge_time = time.time()
    one_day_seconds = 86400  # Interval eksekusi Auto-Purge (24 jam)

    try:
        while True:
            time.sleep(1)
            
            # Memicu fungsi Auto-Purge otomatis setiap siklus 24 jam terlewati
            current_time = time.time()
            if (current_time - last_purge_time) > one_day_seconds:
                purger.execute_purge()
                last_purge_time = current_time
                
    except KeyboardInterrupt:
        observer.stop()
        print("\nSatpam Python dinonaktifkan secara aman.")
    observer.join()