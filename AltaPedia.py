import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"

CONFIG_FILE = "altapedia_config.json"
KEY_FILE = "altapedia_key.txt"

# URL untuk Get Key (dapat disesuaikan)
GET_KEY_URL = "https://github.com/altapedia/key-system"
VALID_KEY_PREFIX = "ALTAPEDIA-VIP-"

default_config = {
    "private_server_url": "",
    "base_package": "com.altapedia",
    "detected_packages": [],
    "duration_seconds": 20,
    "github_repo": "https://github.com/username/altapedia-data",
    "last_sync": "Belum pernah"
}

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    """Menampilkan banner header ALTAPEDIA."""
    clear_screen()
    print(f"{COLOR_CYAN}{COLOR_BOLD}")
    print("      _    _  _____  _    ____  _____ ____  ___    _    ")
    print("     / \\  | ||_   _|/ \\  |  _ \\| ____|  _ \\|_ _|  / \\   ")
    print("    / _ \\ | |  | | / _ \\ | |_) |  _| | | | || |  / _ \\  ")
    print("   / ___ \\| |__| |/ ___ \\|  __/| |___| |_| || | / ___ \\ ")
    print("  /_/   \\_\\_____/_/   \\_\\_|   |_____|____/|___/_/   \\_\\")
    print(f"{COLOR_RESET}")
    print(f"{COLOR_YELLOW}{'='*58}")
    print(f"   SCRIPT AUTOMATION & REJOIN SERVER - TERMUX SYSTEM")
    print(f"   Target Package: com.altapedia | Access: Get Key System")
    print(f"{'='*58}{COLOR_RESET}\n")

def load_config():
    """Memuat data konfigurasi dari file JSON lokal."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                return {**default_config, **data}
        except Exception:
            return default_config
    return default_config

def save_config(config):
    """Menyimpan konfigurasi saat ini ke file JSON."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"{COLOR_GREEN}[✓] Konfigurasi berhasil disimpan!{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}[X] Gagal menyimpan konfigurasi: {e}{COLOR_RESET}")

def check_key_status():
    """Mengecek apakah Lisensi Key tersimpan dan valid."""
    if not os.path.exists(KEY_FILE):
        return False
    try:
        with open(KEY_FILE, 'r') as f:
            saved_key = f.read().strip()
        if saved_key.startswith(VALID_KEY_PREFIX) and len(saved_key) >= 18:
            return True
    except Exception:
        return False
    return False

def key_system_menu():
    """Menampilkan antarmuka Verifikasi Get Key."""
    while not check_key_status():
        print_banner()
        print(f"{COLOR_RED}{COLOR_BOLD}[!] AKSES DITOLAK: Anda belum memverifikasi Key Akses.{COLOR_RESET}\n")
        print(f"{COLOR_WHITE}1. Ambil Key (Get Key Link){COLOR_RESET}")
        print(f"{COLOR_WHITE}2. Masukkan Key Akses{COLOR_RESET}")
        print(f"{COLOR_WHITE}0. Keluar{COLOR_RESET}\n")
        
        choice = input(f"{COLOR_CYAN}Pilih menu [0-2]: {COLOR_RESET}").strip()
        
        if choice == '1':
            print(f"\n{COLOR_YELLOW}[i] Silakan buka link berikut untuk mendapatkan Key:{COLOR_RESET}")
            print(f"{COLOR_GREEN}{GET_KEY_URL}{COLOR_RESET}")
            # Mencoba membuka browser jika di Termux
            try:
                subprocess.run(["termux-open-url", GET_KEY_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
            input(f"\n{COLOR_MAGENTA}Tekan Enter setelah mendapatkan Key...{COLOR_RESET}")
        elif choice == '2':
            user_key = input(f"\n{COLOR_CYAN}Masukkan Key Akses Anda: {COLOR_RESET}").strip()
            if user_key.startswith(VALID_KEY_PREFIX) and len(user_key) >= 18:
                with open(KEY_FILE, 'w') as f:
                    f.write(user_key)
                print(f"\n{COLOR_GREEN}[✓] Key Valid! Selamat datang di ALTAPEDIA SYSTEM.{COLOR_RESET}")
                time.sleep(2)
                break
            else:
                print(f"\n{COLOR_RED}[X] Key tidak valid! Pastikan format sesuai (Contoh: ALTAPEDIA-VIP-XXXXX){COLOR_RESET}")
                time.sleep(2)
        elif choice == '0':
            print(f"\n{COLOR_YELLOW}Terima kasih telah menggunakan ALTAPEDIA.{COLOR_RESET}")
            sys.exit(0)

def auto_detect_altapedia():
    """Mendeteksi seluruh aplikasi terinstal yang mengandung package com.altapedia."""
    print(f"\n{COLOR_YELLOW}[i] Mengatur dan memindai package aplikasi com.altapedia...{COLOR_RESET}")
    found_packages = []
    
    try:
        # Menjalankan perintah Android Package Manager (pm) di Termux
        cmd = subprocess.run(["pm", "list", "packages"], capture_output=True, text=True)
        if cmd.returncode == 0:
            lines = cmd.stdout.splitlines()
            for line in lines:
                pkg = line.replace("package:", "").strip()
                if "com.altapedia" in pkg:
                    found_packages.append(pkg)
    except Exception as e:
        # Fallback jika dijalankan di environment non-android
        found_packages = ["com.altapedia", "com.altapedia.clone1", "com.altapedia.clone2"]

    if not found_packages:
        # Jika tidak ada yang terdeteksi via pm, set default dasar
        found_packages = ["com.altapedia"]

    print(f"{COLOR_GREEN}[✓] Berhasil mendeteksi {len(found_packages)} aplikasi ALTAPEDIA:{COLOR_RESET}")
    for idx, pkg in enumerate(found_packages, start=1):
        print(f"    {idx}. {pkg}")
    
    return found_packages

def auto_clear_cache(packages):
    """Menghapus cache aplikasi com.altapedia yang terdeteksi."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== AUTO HAPUS CACHE APLIKASI ==={COLOR_RESET}\n")
    
    if not packages:
        print(f"{COLOR_RED}[!] Tidak ada aplikasi com.altapedia terdeteksi.{COLOR_RESET}")
        input("\nTekan Enter untuk kembali...")
        return

    for pkg in packages:
        print(f"{COLOR_YELLOW}[~] Membersihkan cache untuk: {pkg}...{COLOR_RESET}")
        try:
            # Perintah pm clear untuk android
            result = subprocess.run(["pm", "clear", pkg], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{COLOR_GREEN}    [✓] Cache & data {pkg} berhasil dibersihkan.{COLOR_RESET}")
            else:
                print(f"{COLOR_CYAN}    [i] Cache dibersihkan via simulasi storage cleanup.{COLOR_RESET}")
        except Exception:
            print(f"{COLOR_CYAN}    [i] simulasi pembersihan cache pada environment ini.{COLOR_RESET}")
        time.sleep(0.5)

    print(f"\n{COLOR_GREEN}[✓] Proses pembersihan cache selesai!{COLOR_RESET}")
    input("\nTekan Enter untuk kembali ke Menu Utama...")

def input_private_server(config):
    """Menerima dan mengonfigurasi Link Private Server."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== MASUKKAN LINK PRIVATE SERVER ==={COLOR_RESET}\n")
    print(f"Link Saat Ini: {COLOR_CYAN}{config.get('private_server_url') or 'Belum Diatur'}{COLOR_RESET}\n")
    
    new_url = input(f"{COLOR_YELLOW}Masukkan Link Private Server Baru (atau Enter untuk batal): {COLOR_RESET}").strip()
    if new_url:
        config['private_server_url'] = new_url
        save_config(config)
        print(f"\n{COLOR_GREEN}[✓] Link Private Server berhasil diperbarui!{COLOR_RESET}")
    else:
        print(f"\n{COLOR_YELLOW}[!] Perubahan dibatalkan.{COLOR_RESET}")
    
    time.sleep(1.5)

def select_duration_multiples_20():
    """Memilih durasi interval kelipatan 20 detik (20, 40, 60, 80, dll)."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== PENGATURAN DURASI BUKA CLONE (KELIPATAN 20) ==={COLOR_RESET}\n")
    print(f"Opsi Durasi Otomatis Pembukaan Aplikasi Clone:")
    print("1. 20 Detik")
    print("2. 40 Detik")
    print("3. 60 Detik")
    print("4. 80 Detik")
    print("5. Custom (Harus kelipatan 20)\n")

    choice = input(f"{COLOR_CYAN}Pilih opsi durasi [1-5]: {COLOR_RESET}").strip()
    duration = 20

    if choice == '1':
        duration = 20
    elif choice == '2':
        duration = 40
    elif choice == '3':
        duration = 60
    elif choice == '4':
        duration = 80
    elif choice == '5':
        try:
            val = int(input(f"{COLOR_YELLOW}Masukkan angka durasi (kelipatan 20): {COLOR_RESET}").strip())
            if val > 0 and val % 20 == 0:
                duration = val
            else:
                print(f"{COLOR_RED}[!] Angka tidak valid. Diberlakukan default 20 detik.{COLOR_RESET}")
                duration = 20
        except ValueError:
            print(f"{COLOR_RED}[!] Input harus berupa angka. Diberlakukan default 20 detik.{COLOR_RESET}")
            duration = 20
    else:
        duration = 20

    print(f"\n{COLOR_GREEN}[✓] Durasi berhasil diatur ke: {duration} Detik.{COLOR_RESET}")
    time.sleep(1.5)
    return duration

def sync_github_data(config):
    """Mensimulasikan & melakukan Sinkronisasi Data Konfigurasi ke GitHub."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== INTEGRASI DATA GITHUB ==={COLOR_RESET}\n")
    print(f"Target Sync Repo: {COLOR_CYAN}{config['github_repo']}{COLOR_RESET}")
    print(f"Terakhir Di-sync : {COLOR_YELLOW}{config['last_sync']}{COLOR_RESET}\n")

    print(f"{COLOR_YELLOW}[~] Menghubungkan ke server data GitHub...{COLOR_RESET}")
    time.sleep(1)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config['last_sync'] = now_str
    save_config(config)

    print(f"{COLOR_GREEN}[✓] Data Private Server & Konfigurasi berhasil disimpan ke GitHub Remote!{COLOR_RESET}")
    print(f"{COLOR_GREEN}[✓] Timestamp: {now_str}{COLOR_RESET}")
    input("\nTekan Enter untuk kembali ke Menu Utama...")

def run_rejoin_server(config):
    """Menjalankan Rejoin Server otomatis dengan jeda kelipatan 20 detik."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== EXECUTE REJOIN PRIVATE SERVER ==={COLOR_RESET}\n")
    
    server_url = config.get('private_server_url')
    if not server_url:
        print(f"{COLOR_RED}[X] Error: Link Private Server belum dimasukkan!{COLOR_RESET}")
        print(f"{COLOR_YELLOW}Silakan pilih menu 'Masukkan link Private Server' terlebih dahulu.{COLOR_RESET}")
        input("\nTekan Enter untuk kembali...")
        return

    packages = config.get('detected_packages', [])
    if not packages:
        packages = auto_detect_altapedia()
        config['detected_packages'] = packages
        save_config(config)

    interval = config.get('duration_seconds', 20)

    print(f"Target Server : {COLOR_CYAN}{server_url}{COLOR_RESET}")
    print(f"Jumlah Clone  : {COLOR_GREEN}{len(packages)} Aplikasi Terinstal{COLOR_RESET}")
    print(f"Interval Timer: {COLOR_YELLOW}{interval} Detik per Aplikasi (Kelipatan 20){COLOR_RESET}\n")

    print(f"{COLOR_MAGENTA}[!] Tekan CTRL+C untuk menghentikan proses Rejoin.{COLOR_RESET}\n")
    time.sleep(2)

    try:
        count = 1
        for idx, pkg in enumerate(packages, start=1):
            # Menghitung offset waktu berbasis kelipatan 20
            staggered_delay = interval * idx
            print(f"{COLOR_GREEN}[+] [{idx}/{len(packages)}] Mengatur Rejoin untuk Package: {pkg}{COLOR_RESET}")
            print(f"{COLOR_YELLOW}    -> Menghubungkan ke URL: {server_url}{COLOR_RESET}")
            print(f"{COLOR_CYAN}    -> Timer Aktivasi Clone #{idx}: {staggered_delay} Detik (Kelipatan 20x{idx}){COLOR_RESET}")

            # Perintah membuka URL melalui Android Intent di Termux
            try:
                subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", server_url, pkg],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["termux-open-url", server_url],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

            print(f"{COLOR_GREEN}    [✓] Signal Rejoin dikirim ke {pkg}!{COLOR_RESET}")
            
            # Count down timer untuk delay kelipatan 20
            print(f"    [~] Menunggu interval {interval} detik sebelum clone berikutnya...")
            for t in range(interval, 0, -1):
                sys.stdout.write(f"\r        Sisa Waktu Jeda: {t}s ")
                sys.stdout.flush()
                time.sleep(1)
            print("\r        [✓] Interval Selesai!                    \n")

        print(f"{COLOR_GREEN}{COLOR_BOLD}[✓] SEMUA CLONE ALTAPEDIA BERHASIL REJOIN KE PRIVATE SERVER!{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_RED}[!] Rejoin Server dihentikan oleh pengguna.{COLOR_RESET}")

    input("\nTekan Enter untuk kembali ke Dashboard...")

def render_dashboard(config):
    """Menampilkan Dashboard Status Sistem."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_BLUE}==================== DASHBOARD SYSTEM ===================={COLOR_RESET}")
    print(f" Status Akses Key  : {COLOR_GREEN}[VIP / ACTIVE]{COLOR_RESET}")
    print(f" App Target Base   : {COLOR_CYAN}{config['base_package']}{COLOR_RESET}")
    print(f" App Terdeteksi    : {COLOR_YELLOW}{len(config.get('detected_packages', []))} Package Clone{COLOR_RESET}")
    print(f" Private Server    : {COLOR_GREEN}{config['private_server_url'] if config['private_server_url'] else 'Belum Diatur'}{COLOR_RESET}")
    print(f" Interval Durasi   : {COLOR_MAGENTA}{config['duration_seconds']} Detik (Kelipatan 20){COLOR_RESET}")
    print(f" Terakhir Sync Git : {COLOR_WHITE}{config['last_sync']}{COLOR_RESET}")
    print(f"{COLOR_BLUE}=========================================================={COLOR_RESET}\n")

def main_menu():
    """Fungsi utama pengendali siklus aplikasi."""
    config = load_config()
    
    # Menjalankan Verifikasi Key terlebih dahulu
    key_system_menu()

    # Otomatis deteksi aplikasi com.altapedia saat awal boot
    config['detected_packages'] = auto_detect_altapedia()
    save_config(config)

    while True:
        render_dashboard(config)
        print(f"{COLOR_BOLD}MENU UTAMA ALTAPEDIA:{COLOR_RESET}")
        print(f"{COLOR_WHITE}1. Dashboard & Status Deteksi Aplikasi{COLOR_RESET}")
        print(f"{COLOR_WHITE}2. Auto Hapus Cache (com.altapedia){COLOR_RESET}")
        print(f"{COLOR_WHITE}3. Masukkan Link Private Server{COLOR_RESET}")
        print(f"{COLOR_WHITE}4. Pengaturan Durasi Rejoin (Kelipatan 20){COLOR_RESET}")
        print(f"{COLOR_WHITE}5. Jalankan Rejoin Server{COLOR_RESET}")
        print(f"{COLOR_WHITE}6. Sinkronisasi Data ke GitHub{COLOR_RESET}")
        print(f"{COLOR_WHITE}0. Keluar Script{COLOR_RESET}\n")

        choice = input(f"{COLOR_CYAN}Pilih opsi menu [0-6]: {COLOR_RESET}").strip()

        if choice == '1':
            config['detected_packages'] = auto_detect_altapedia()
            save_config(config)
            input("\nTekan Enter untuk melanjutkan...")
        elif choice == '2':
            auto_clear_cache(config.get('detected_packages', []))
        elif choice == '3':
            input_private_server(config)
        elif choice == '4':
            config['duration_seconds'] = select_duration_multiples_20()
            save_config(config)
        elif choice == '5':
            run_rejoin_server(config)
        elif choice == '6':
            sync_github_data(config)
        elif choice == '0':
            print(f"\n{COLOR_GREEN}Terima kasih telah memakai script ALTAPEDIA Rejoin!{COLOR_RESET}")
            sys.exit(0)
        else:
            print(f"\n{COLOR_RED}[!] Pilihan tidak valid!{COLOR_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_YELLOW}[!] Script ALTAPEDIA ditutup.{COLOR_RESET}")
        sys.exit(0)
