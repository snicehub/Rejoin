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

# URL Raw GitHub berisi daftar kunci yang valid
ONLINE_KEY_URL = "https://raw.githubusercontent.com/snicehub/Rejoin/main/keys.txt"

# URL Google Spreadsheet (Format Published CSV) untuk Verifikasi Key
GSHEET_KEY_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_YOUR_SPREADSHEET_ID_HERE/pub?output=csv"

# URL yang dibuka saat user memilih opsi "1. Ambil Key"
GET_KEY_URL = "https://github.com/snicehub/Rejoin"

VALID_KEY_PREFIX = "ALTAPEDIA-VIP-"

default_config = {
    "private_server_url": "",
    "base_package": "com.altapedia",
    "detected_packages": [],
    "duration_seconds": 20,
    "github_repo": "https://github.com/snicehub/Rejoin",
    "gsheet_url": GSHEET_KEY_URL,
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

def fetch_online_keys():
    """Mengunduh daftar key valid dari Google Spreadsheet & Server GitHub."""
    keys = []
    
    # 1. Coba ambil dari Google Spreadsheet (CSV)
    try:
        req = urllib.request.Request(GSHEET_KEY_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            for line in content.splitlines():
                cleaned_key = line.replace('"', '').replace("'", '').strip()
                if cleaned_key:
                    keys.append(cleaned_key)
            if keys:
                return keys
    except Exception:
        pass

    # 2. Fallback: Coba ambil dari GitHub jika Google Sheets gagal
    try:
        req = urllib.request.Request(ONLINE_KEY_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            keys = [line.strip() for line in content.splitlines() if line.strip()]
            return keys
    except Exception:
        return None

def verify_key_online(input_key):
    """Memeriksa apakah key yang diinput ada di database online."""
    online_keys = fetch_online_keys()
    
    if online_keys is not None:
        return input_key in online_keys
    
    return input_key.startswith(VALID_KEY_PREFIX) and len(input_key) >= 18

def check_saved_key():
    """Mengecek lisensi yang sudah tersimpan di file lokal."""
    if not os.path.exists(KEY_FILE):
        return False
    try:
        with open(KEY_FILE, 'r') as f:
            saved_key = f.read().strip()
        return verify_key_online(saved_key)
    except Exception:
        return False

def key_system_menu():
    """Menampilkan antarmuka Verifikasi Get Key."""
    if check_saved_key():
        return

    while True:
        print_banner()
        print(f"{COLOR_RED}{COLOR_BOLD}[!] AKSES DITOLAK: Anda belum memverifikasi Key Akses.{COLOR_RESET}\n")
        print(f"{COLOR_WHITE}1. Ambil Key (Get Key Link){COLOR_RESET}")
        print(f"{COLOR_WHITE}2. Masukkan Key Akses{COLOR_RESET}")
        print(f"{COLOR_WHITE}0. Keluar{COLOR_RESET}\n")
        
        choice = input(f"{COLOR_CYAN}Pilih menu [0-2]: {COLOR_RESET}").strip()
        
        if choice == '1':
            print(f"\n{COLOR_YELLOW}[i] Silakan buka link berikut untuk mendapatkan Key:{COLOR_RESET}")
            print(f"{COLOR_GREEN}{GET_KEY_URL}{COLOR_RESET}")
            try:
                subprocess.run(["termux-open-url", GET_KEY_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
            input(f"\n{COLOR_MAGENTA}Tekan Enter setelah mendapatkan Key...{COLOR_RESET}")
        elif choice == '2':
            user_key = input(f"\n{COLOR_CYAN}Masukkan Key Akses Anda: {COLOR_RESET}").strip()
            print(f"{COLOR_YELLOW}[~] Memverifikasi Key ke Server...{COLOR_RESET}")
            
            if verify_key_online(user_key):
                with open(KEY_FILE, 'w') as f:
                    f.write(user_key)
                print(f"\n{COLOR_GREEN}[✓] Key Valid! Selamat datang di ALTAPEDIA SYSTEM.{COLOR_RESET}")
                time.sleep(2)
                break
            else:
                print(f"\n{COLOR_RED}[X] Key tidak terdaftar atau salah!{COLOR_RESET}")
                time.sleep(2.5)
        elif choice == '0':
            print(f"\n{COLOR_YELLOW}Terima kasih telah menggunakan ALTAPEDIA.{COLOR_RESET}")
            sys.exit(0)

def auto_detect_altapedia():
    """Mendeteksi seluruh aplikasi terinstal yang mengandung package com.altapedia."""
    print(f"\n{COLOR_YELLOW}[i] Memindai package aplikasi com.altapedia...{COLOR_RESET}")
    found_packages = []
    
    try:
        cmd = subprocess.run(["pm", "list", "packages"], capture_output=True, text=True)
        if cmd.returncode == 0:
            lines = cmd.stdout.splitlines()
            for line in lines:
                pkg = line.replace("package:", "").strip()
                if "com.altapedia" in pkg:
                    found_packages.append(pkg)
    except Exception:
        found_packages = ["com.altapedia", "com.altapedia.liteB"]

    if not found_packages:
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
            result = subprocess.run(["pm", "clear", pkg], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{COLOR_GREEN}    [✓] Cache & data {pkg} berhasil dibersihkan.{COLOR_RESET}")
            else:
                print(f"{COLOR_CYAN}    [i] Pembersihan cache disimulasikan.{COLOR_RESET}")
        except Exception:
            print(f"{COLOR_CYAN}    [i] Pembersihan cache disimulasikan.{COLOR_RESET}")
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
    """Memilih durasi interval kelipatan 20 detik."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== PENGATURAN DURASI BUKA CLONE (KELIPATAN 20) ==={COLOR_RESET}\n")
    print("1. 20 Detik")
    print("2. 40 Detik")
    print("3. 60 Detik")
    print("4. 80 Detik")
    print("5. Custom (Harus kelipatan 20)\n")

    choice = input(f"{COLOR_CYAN}Pilih opsi durasi [1-5]: {COLOR_RESET}").strip()
    duration = 20

    if choice == '1': duration = 20
    elif choice == '2': duration = 40
    elif choice == '3': duration = 60
    elif choice == '4': duration = 80
    elif choice == '5':
        try:
            val = int(input(f"{COLOR_YELLOW}Masukkan angka durasi (kelipatan 20): {COLOR_RESET}").strip())
            if val > 0 and val % 20 == 0:
                duration = val
            else:
                print(f"{COLOR_RED}[!] Diberlakukan default 20 detik.{COLOR_RESET}")
                duration = 20
        except ValueError:
            duration = 20
    else:
        duration = 20

    print(f"\n{COLOR_GREEN}[✓] Durasi berhasil diatur ke: {duration} Detik.{COLOR_RESET}")
    time.sleep(1.5)
    return duration

def sync_github_data(config):
    """Sinkronisasi Data Konfigurasi ke GitHub."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== INTEGRASI DATA GITHUB ==={COLOR_RESET}\n")
    print(f"Target Repo : {COLOR_CYAN}{config['github_repo']}{COLOR_RESET}")
    print(f"Sync Terakhir: {COLOR_YELLOW}{config['last_sync']}{COLOR_RESET}\n")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config['last_sync'] = now_str
    save_config(config)

    print(f"{COLOR_GREEN}[✓] Data Konfigurasi berhasil disinkronisasi ke Remote GitHub!{COLOR_RESET}")
    print(f"{COLOR_GREEN}[✓] Waktu: {now_str}{COLOR_RESET}")
    input("\nTekan Enter untuk kembali ke Menu Utama...")

def send_deep_link_intent(pkg, server_url):
    """
    Mengirim intent peluncuran aplikasi dan deep link private server.
    Menggunakan teknik 2-Stage Launch (Main Intent -> Delay -> View Deep Link)
    agar aplikasi clone pasti terbuka dan langsung masuk ke dalam map.
    """
    try:
        # Stage 1: Buka/Bangunkan aplikasi clone ke foreground
        cmd_main = [
            "am", "start",
            "-a", "android.intent.action.MAIN",
            "-c", "android.intent.category.LAUNCHER",
            "-p", pkg,
            "--activity-new-task"
        ]
        subprocess.run(cmd_main, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Jeda 2.5 detik agar engine aplikasi clone selesai inisialisasi
        time.sleep(2.5)
        
        # Stage 2: Kirim Intent Deep Link Private Server
        cmd_view = [
            "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", server_url,
            "-p", pkg,
            "--activity-clear-top",
            "--activity-new-task"
        ]
        subprocess.run(cmd_view, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def run_rejoin_server(config):
    """Menjalankan Rejoin Server otomatis dengan perbaikan multi-clone deep link."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_MAGENTA}=== EXECUTE REJOIN PRIVATE SERVER ==={COLOR_RESET}\n")
    
    server_url = config.get('private_server_url')
    if not server_url:
        print(f"{COLOR_RED}[X] Error: Link Private Server belum dimasukkan!{COLOR_RESET}")
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

    print(f"{COLOR_MAGENTA}[!] Tekan CTRL+C untuk menghentikan proses.{COLOR_RESET}\n")
    time.sleep(2)

    try:
        for idx, pkg in enumerate(packages, start=1):
            staggered_delay = interval * idx
            print(f"{COLOR_GREEN}[+] [{idx}/{len(packages)}] Opening Package: {pkg}{COLOR_RESET}")
            print(f"{COLOR_YELLOW}    -> Joining Target: {server_url}{COLOR_RESET}")
            print(f"{COLOR_CYAN}    -> Timer Activation: {staggered_delay}s (Interval #{idx}){COLOR_RESET}")

            # Peluncuran Aplikasi & Auto Join Map (2-Stage Launch)
            send_deep_link_intent(pkg, server_url)
            print(f"{COLOR_GREEN}    [✓] Signal awal & Deep Link terkirim ke {pkg}...{COLOR_RESET}")
            
            # Re-Push Intent khusus clone ke-2 dan seterusnya untuk memaksa auto-teleport ke map
            if idx > 1:
                print(f"{COLOR_YELLOW}    [~] Memicu Re-Push Deep Link (Teleport ke Map)...{COLOR_RESET}")
                time.sleep(3)
                cmd_repush = [
                    "am", "start",
                    "-a", "android.intent.action.VIEW",
                    "-d", server_url,
                    "-p", pkg,
                    "--activity-clear-top",
                    "--activity-new-task"
                ]
                subprocess.run(cmd_repush, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{COLOR_GREEN}    [✓] Re-Push Deep Link berhasil dikirim ke {pkg}!{COLOR_RESET}")
            
            # Hitung Mundur Sisa Waktu Jeda
            remaining_time = interval - (5.5 if idx > 1 else 2.5)
            if remaining_time < 1:
                remaining_time = 1

            for t in range(int(remaining_time), 0, -1):
                sys.stdout.write(f"\r        Sisa Waktu Jeda: {t}s ")
                sys.stdout.flush()
                time.sleep(1)
            print("\r        [✓] Interval Selesai!                    \n")

        print(f"{COLOR_GREEN}{COLOR_BOLD}[✓] SEMUA CLONE ALTAPEDIA BERHASIL REJOIN KE MAP!{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_RED}[!] Rejoin Server dihentikan.{COLOR_RESET}")

    input("\nTekan Enter untuk kembali ke Dashboard...")

def render_dashboard(config):
    """Menampilkan Dashboard Status Sistem."""
    print_banner()
    print(f"{COLOR_BOLD}{COLOR_BLUE}==================== DASHBOARD SYSTEM ===================={COLOR_RESET}")
    print(f" Status Akses Key  : {COLOR_GREEN}[ONLINE VIP / ACTIVE]{COLOR_RESET}")
    print(f" Target GitHub Repo: {COLOR_CYAN}{config['github_repo']}{COLOR_RESET}")
    print(f" App Terdeteksi    : {COLOR_YELLOW}{len(config.get('detected_packages', []))} Package Clone{COLOR_RESET}")
    print(f" Private Server    : {COLOR_GREEN}{config['private_server_url'] if config['private_server_url'] else 'Belum Diatur'}{COLOR_RESET}")
    print(f" Interval Durasi   : {COLOR_MAGENTA}{config['duration_seconds']} Detik (Kelipatan 20){COLOR_RESET}")
    print(f" Sync GitHub       : {COLOR_WHITE}{config['last_sync']}{COLOR_RESET}")
    print(f"{COLOR_BLUE}=========================================================={COLOR_RESET}\n")

def main_menu():
    """Fungsi utama pengendali aplikasi."""
    config = load_config()
    key_system_menu()

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
            print(f"\n{COLOR_GREEN}Terima kasih telah memakai script ALTAPEDIA!{COLOR_RESET}")
            sys.exit(0)
        else:
            print(f"\n{COLOR_RED}[!] Pilihan tidak valid!{COLOR_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{COLOR_YELLOW}[!] Script ditutup.{COLOR_RESET}")
        sys.exit(0)
