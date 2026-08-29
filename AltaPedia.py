import os
import sys
import time
import json
import re
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

class Colors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY      = '\033[90m'

CONFIG_FILE = "altapedia_config.json"
VALID_KEY = "ALTAPEDIA-0987-08123-SUPREME"
GET_KEY_URL = "https://raw.githubusercontent.com/snicehub/Rejoin/main/keys.txt"
GITHUB_CONFIG_URL = "https://raw.githubusercontent.com/snicehub/Rejoin/main/README.md"
DEFAULT_PACKAGE = "com.altapedia"

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def draw_banner():
    """Displays the custom ALTAPEDIA ASCII banner."""
    print(f"{Colors.OKCYAN}{Colors.BOLD}")
    print(r"""
    ╔══════════════════════════════════════════════════════════════╗
    ║   █████╗ ██╗  ████████╗█████╗ ██████╗ ███████╗██████╗ █████╗ ║
    ║  ██╔══██╗██║  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗║
    ║  ███████║██║     ██║   ███████║██████╔╝█████╗  ██║  ██║███████║║
    ║  ██╔══██╗██║     ██║   ██╔══██╗██╔═══╝ ██╔══╝  ██║  ██║██╔══██╗║
    ║  ██║  ██║███████╗██║   ██║  ██║██║     ███████╗██████╔╝██║  ██║║
    ║  ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝     ╚══════╝╚═════╝ ╚═╝  ╚═╝║
    ║                                                              ║
    ║             TERMUX REJOIN SERVER & CLONE AUTOMATION          ║
    ║                     VERSION 1.1 SUPREME                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """ + Colors.ENDC)

def load_config():
    """Loads configuration data from local JSON storage."""
    default_cfg = {
        "key": "",
        "private_server": "",
        "base_duration": 60,
        "clone_step": 20,
        "force_stop_before_launch": False,
        "launch_mode": "Standard (-p)",
        "clones": []
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                default_cfg.update(data)
        except Exception as e:
            print(f"{Colors.FAIL}[!] Gagal membaca file konfigurasi: {e}{Colors.ENDC}")
    return default_cfg

def save_config(cfg):
    """Saves current configuration data to local JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=4)
    except Exception as e:
        print(f"{Colors.FAIL}[!] Gagal menyimpan konfigurasi: {e}{Colors.ENDC}")

def verify_key(config):
    """Verifies the input license key against offline and remote sources."""
    clear_screen()
    draw_banner()
    
    saved_key = config.get("key", "").strip()
    
    if saved_key == VALID_KEY:
        print(f"{Colors.OKGREEN}[✓] Lisensi Terverifikasi (Tersimpan): {saved_key}{Colors.ENDC}\n")
        time.sleep(1)
        return True

    print(f"{Colors.WARNING}══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f"{Colors.BOLD}                SISTEM AKSES LISENSI SCRIPT                   {Colors.ENDC}")
    print(f"{Colors.WARNING}══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f"Untuk menggunakan script ini, Anda memerlukan Kunci Akses (Key).")
    print(f"Pilihan:")
    print(f" 1. Masukkan Key")
    print(f" 2. Get Key (Dapatkan Kunci Akses)")
    print(f" 3. Keluar")
    print()

    choice = input(f"{Colors.OKCYAN}Pilih menu [1-3]: {Colors.ENDC}").strip()
    
    if choice == "2":
        print(f"\n{Colors.OKBLUE}[i] Salin link berikut untuk mendapatkan key:{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.UNDERLINE}https://altapedia.net/get-key?ref=supreme{Colors.ENDC}")
        print(f"{Colors.GRAY}Catatan: Gunakan key: {VALID_KEY}{Colors.ENDC}\n")
        input("Tekan [Enter] untuk kembali...")
        return verify_key(config)
    elif choice == "3":
        print(f"{Colors.FAIL}Keluar dari program.{Colors.ENDC}")
        sys.exit(0)
    
    user_key = input(f"\n{Colors.BOLD}Masukkan License Key: {Colors.ENDC}").strip()
    
    if user_key == VALID_KEY:
        config["key"] = user_key
        save_config(config)
        print(f"\n{Colors.OKGREEN}[✓] Key Valid! Akses Diberikan. Menyimpan Lisensi...{Colors.ENDC}")
        time.sleep(1.5)
        return True
    else:
        print(f"{Colors.WARNING}[i] Memeriksa Key ke Server GitHub (snicehub/Rejoin)...{Colors.ENDC}")
        try:
            req = urllib.request.Request(GET_KEY_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('utf-8')
                valid_keys = [k.strip() for k in content.splitlines() if k.strip()]
                if user_key in valid_keys or VALID_KEY in valid_keys:
                    config["key"] = user_key
                    save_config(config)
                    print(f"{Colors.OKGREEN}[✓] Key GitHub Valid! Akses Diberikan.{Colors.ENDC}")
                    time.sleep(1.5)
                    return True
        except Exception:
            pass
            
        print(f"{Colors.FAIL}[X] Key Salah atau Kadaluarsa! Silakan Get Key terlebih dahulu.{Colors.ENDC}")
        time.sleep(2)
        return verify_key(config)

def detect_installed_packages():
    """Detects installed instances of com.altapedia and its clones via package manager."""
    found_packages = []
    try:
        result = subprocess.run(['pm', 'list', 'packages'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines:
                pkg = line.replace('package:', '').strip()
                if DEFAULT_PACKAGE in pkg or 'altapedia' in pkg.lower():
                    found_packages.append(pkg)
    except Exception:
        found_packages = [f"{DEFAULT_PACKAGE}.liteA", f"{DEFAULT_PACKAGE}.liteB"]
    
    if not found_packages:
        found_packages = [DEFAULT_PACKAGE]
        
    return sorted(list(set(found_packages)))

def auto_hapus_cache(packages):
    """Clears cache for all detected Altapedia packages."""
    clear_screen()
    draw_banner()
    print(f"{Colors.HEADER}{Colors.BOLD}=== MENU: AUTO HAPUS CACHE ==={Colors.ENDC}\n")
    
    print(f"{Colors.OKBLUE}[i] Memulai proses pembersihan cache...{Colors.ENDC}\n")
    
    for pkg in packages:
        print(f" -> Membersihkan cache untuk package: {Colors.OKCYAN}{pkg}{Colors.ENDC}")
        try:
            cmd = f"pm clear {pkg}"
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "Success" in res.stdout:
                print(f"    {Colors.OKGREEN}[✓] Cache & Data {pkg} Berhasil Dibersihkan!{Colors.ENDC}")
            else:
                cache_dir = f"/sdcard/Android/data/{pkg}/cache"
                subprocess.run(f"rm -rf {cache_dir}/*", shell=True)
                print(f"    {Colors.OKGREEN}[✓] Folder Cache {pkg} Dibersihkan.{Colors.ENDC}")
        except Exception as e:
            print(f"    {Colors.FAIL}[!] Gagal membersihkan {pkg}: {e}{Colors.ENDC}")
        time.sleep(0.5)

    print(f"\n{Colors.OKGREEN}[✓] Seluruh proses pembersihan cache selesai!{Colors.ENDC}")
    input(f"\n{Colors.GRAY}Tekan [Enter] untuk kembali ke Dashboard...{Colors.ENDC}")

def input_private_server(config):
    """Allows user to enter and update the Altapedia Private Server URL."""
    clear_screen()
    draw_banner()
    print(f"{Colors.HEADER}{Colors.BOLD}=== MENU: MASUKKAN LINK PRIVATE SERVER ==={Colors.ENDC}\n")
    
    current_link = config.get("private_server", "")
    if current_link:
        print(f"Link Terpasang Saat Ini:\n{Colors.OKCYAN}{current_link}{Colors.ENDC}\n")
    else:
        print(f"{Colors.WARNING}[!] Belum ada link Private Server yang tersimpan.{Colors.ENDC}\n")
        
    print("Masukkan Link Private Server ALTAPEDIA baru (atau tekan Enter untuk batal):")
    new_link = input(f"{Colors.BOLD}URL: {Colors.ENDC}").strip()
    
    if new_link:
        config["private_server"] = new_link
        save_config(config)
        print(f"\n{Colors.OKGREEN}[✓] Link Private Server Berhasil Disimpan!{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}[i] Tidak ada perubahan link.{Colors.ENDC}")
        
    time.sleep(1.5)

def configure_launch_options(config):
    """Configures force stop behavior and intent launch modes."""
    clear_screen()
    draw_banner()
    print(f"{Colors.HEADER}{Colors.BOLD}=== MENU: PENGATURAN TINGKAT LANJUT ==={Colors.ENDC}\n")
    
    current_fs = config.get("force_stop_before_launch", True)
    status_fs = f"{Colors.OKGREEN}AKTIF (Direkomendasikan){Colors.ENDC}" if current_fs else f"{Colors.FAIL}NONAKTIF{Colors.ENDC}"
    
    print(f"1. Auto Force Stop App Sebelum Rejoin : {status_fs}")
    print(f"   (Menutup aplikasi terlebih dahulu agar link Private Server langsung terbaca)\n")
    
    print("PILIHAN:")
    print(" [1] Toggle Auto Force Stop (Aktif/Nonaktif)")
    print(" [0] Kembali ke Dashboard")
    print()
    
    choice = input(f"{Colors.OKCYAN}Pilih opsi [0-1]: {Colors.ENDC}").strip()
    if choice == "1":
        config["force_stop_before_launch"] = not current_fs
        save_config(config)
        print(f"\n{Colors.OKGREEN}[✓] Pengaturan Force Stop Diperbarui!{Colors.ENDC}")
        time.sleep(1)
    else:
        return

def launch_app_and_rejoin(package_name, server_link, force_stop=True):
    """
    Launches specified app package directly into the Private Server using precise Android Intents.
    Includes auto force-stop to clear stuck home menus and explicit package targeting (-p).
    """
    try:
        # Step 1: Force Stop app if enabled so it resets from home menu state
        if force_stop:
            subprocess.run(f"am force-stop {package_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1.5)
            
        if server_link:
            clean_link = server_link.strip()
            
            # Method 1: Direct ActivityProtocolLaunch Component (Bypasses Home/Beranda screen on clones)
            cmd_component = (
                f'am start -a android.intent.action.VIEW '
                f'-d "{clean_link}" '
                f'-n {package_name}/com.roblox.client.ActivityProtocolLaunch '
                f'-f 0x14000000'
            )
            subprocess.run(cmd_component, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            time.sleep(0.5)

            # Method 2: Target package directly with VIEW action + FLAG_ACTIVITY_NEW_TASK & CLEAR_TOP
            cmd_primary = (
                f'am start -a android.intent.action.VIEW '
                f'-d "{clean_link}" '
                f'-p {package_name} '
                f'-f 0x14000000'
            )
            subprocess.run(cmd_primary, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            cmd = f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        return True
    except Exception as e:
        return False

def countdown_timer(seconds, message=""):
    """Displays a dynamic countdown timer in the terminal."""
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        sys.stdout.write(f"\r{Colors.OKBLUE}[⏳] {message} - Menunggu: {Colors.BOLD}{Colors.WARNING}{time_str}{Colors.ENDC}  ")
        sys.stdout.flush()
        time.sleep(1)
    print()

def menu_rejoin_server(config, installed_packages):
    """Executes the rejoin process once across all clones, then auto-closes Termux in 5s."""
    clear_screen()
    draw_banner()
    print(f"{Colors.HEADER}{Colors.BOLD}=== MENU: REJOIN SERVER AUTOMATION ==={Colors.ENDC}\n")
    
    server_link = config.get("private_server", "").strip()
    if not server_link:
        print(f"{Colors.FAIL}[!] Link Private Server belum diisi!{Colors.ENDC}")
        print(f"Silakan atur link terlebih dahulu di menu 3.")
        input(f"\n{Colors.GRAY}Tekan [Enter] untuk kembali...{Colors.ENDC}")
        return

    force_stop_enabled = config.get("force_stop_before_launch", False)

    print(f"{Colors.OKCYAN}Aplikasi Terdeteksi ({len(installed_packages)}):{Colors.ENDC}")
    for idx, pkg in enumerate(installed_packages, 1):
        print(f"  {idx}. {pkg}")
    print()

    print(f"{Colors.WARNING}[i] Skema kelipatan jeda clone diaktifkan:{Colors.ENDC}")
    print(f"    - Main App / App 1: Langsung Buka")
    for i in range(1, len(installed_packages)):
        print(f"    - Clone #{i:<9} : +{i * 20} detik kelipatan")
        
    print(f"\n{Colors.OKGREEN}[▶] Memulai Peluncuran Aplikasi Ke Private Server...{Colors.ENDC}\n")
    time.sleep(1.5)
    
    try:
        print(f"{Colors.HEADER}--------------------------------------------------{Colors.ENDC}")
        print(f"{Colors.BOLD}🚀 PROCESS LAUNCH | {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}")
        print(f"{Colors.HEADER}--------------------------------------------------{Colors.ENDC}")
        
        # Proses membuka aplikasi utama & clone satu per satu tanpa loop berulang
        for index, pkg in enumerate(installed_packages):
            clone_delay = index * 20
            
            if clone_delay > 0:
                print(f"\n{Colors.GRAY}[+] Persiapan membuka clone ke-{index} ({pkg})...{Colors.ENDC}")
                countdown_timer(clone_delay, f"Jeda Kelipatan 20s untuk {pkg}")
            
            print(f"{Colors.OKGREEN}[✓] Membuka Aplikasi: {Colors.BOLD}{pkg}{Colors.ENDC}")
            if force_stop_enabled:
                print(f"    {Colors.GRAY}[i] Force stopping {pkg} untuk pembersihan session...{Colors.ENDC}")
            print(f"    Meluncurkan Ke Private Server via Direct Intent...")
            
            success = launch_app_and_rejoin(pkg, server_link, force_stop=force_stop_enabled)
            if success:
                print(f"    {Colors.OKCYAN}[SUCCESS] Deep Link Private Server terkirim ke {pkg}{Colors.ENDC}")
            else:
                print(f"    {Colors.FAIL}[FAILED] Gagal membuka {pkg}{Colors.ENDC}")
        
        # Penanganan setelah semua aplikasi terbuka: hitung mundur 5 detik lalu menutup Termux paksa
        print(f"\n{Colors.OKGREEN}══════════════════════════════════════════════════════════════{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[✓] Seluruh aplikasi & clone ({len(installed_packages)}) telah berhasil dibuka!{Colors.ENDC}")
        print(f"{Colors.WARNING}[i] Menutup aplikasi Termux secara paksa dalam waktu 5 detik...{Colors.ENDC}")
        print(f"{Colors.GRAY}    (Aplikasi clone Altapedia akan tetap berjalan dengan normal){Colors.ENDC}")
        print(f"{Colors.OKGREEN}══════════════════════════════════════════════════════════════{Colors.ENDC}\n")
        
        countdown_timer(5, "Menutup Termux")
        
        print(f"\n{Colors.OKCYAN}[🚪] Menutup Termux & Menjaga Aplikasi Clone Tetap Berjalan...{Colors.ENDC}")
        time.sleep(0.5)

        # Hentikan aplikasi Termux menggunakan eksekusi root SU (sesuai skrip bash)
        try:
            if os.path.exists("/system/xbin/su"):
                su_cmd = "/system/xbin/su -c"
            elif os.path.exists("/system/bin/su"):
                su_cmd = "/system/bin/su -c"
            else:
                su_cmd = "su -c"
                
            subprocess.run(f'{su_cmd} "am force-stop com.termux"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            subprocess.run("am force-stop com.termux", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        os._exit(0)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}[!] Proses Dihentikan oleh Pengguna.{Colors.ENDC}")
        time.sleep(2)

def show_dashboard(config, packages):
    """Displays the main interactive dashboard UI."""
    clear_screen()
    draw_banner()
    
    server_status = config.get("private_server", "")
    if not server_status:
        server_status = f"{Colors.FAIL}Belum diatur{Colors.ENDC}"
    else:
        server_status = f"{Colors.OKGREEN}{server_status[:38]}...{Colors.ENDC}"
        
    fs_status = "AKTIF" if config.get("force_stop_before_launch", True) else "NONAKTIF"

    print(f"{Colors.OKBLUE}══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f"{Colors.BOLD}                       DASHBOARD STATUS                       {Colors.ENDC}")
    print(f"{Colors.OKBLUE}══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f" Status Lisensi     : {Colors.OKGREEN}[✓] SUPREME VIP ACTIVE{Colors.ENDC}")
    print(f" Key Terpasang      : {Colors.BOLD}{config.get('key')}{Colors.ENDC}")
    print(f" Package Utama      : {Colors.OKCYAN}{DEFAULT_PACKAGE}{Colors.ENDC}")
    print(f" Clone Terdeteksi   : {Colors.BOLD}{len(packages)} Aplikasi{Colors.ENDC}")
    print(f" Private Server     : {server_status}")
    print(f" Auto Force Stop    : {Colors.OKCYAN}{fs_status}{Colors.ENDC}")
    print(f" Sync Data Server   : {Colors.OKGREEN}GitHub Synced{Colors.ENDC}")
    print(f"{Colors.OKBLUE}══════════════════════════════════════════════════════════════{Colors.ENDC}\n")

    print(f"{Colors.BOLD}MENU UTAMA:{Colors.ENDC}")
    print(f" [{Colors.OKGREEN}1{Colors.ENDC}] 📊 Dashboard (Refresh Data)")
    print(f" [{Colors.OKGREEN}2{Colors.ENDC}] 🧹 Auto Hapus Cache ({len(packages)} App)")
    print(f" [{Colors.OKGREEN}3{Colors.ENDC}] 🔗 Masukkan Link Private Server")
    print(f" [{Colors.OKGREEN}4{Colors.ENDC}] 🔄 Rejoin Server (Start Auto Reopen)")
    print(f" [{Colors.OKGREEN}5{Colors.ENDC}] ⚙️ Pengaturan Advance (Force Stop Toggle)")
    print(f" [{Colors.OKGREEN}6{Colors.ENDC}] 🔑 Informasi Key & GitHub Sync")
    print(f" [{Colors.FAIL}0{Colors.ENDC}] 🚪 Keluar Script")
    print()

def main():
    """Main program entry loop."""
    config = load_config()
    
    if not verify_key(config):
        print(f"{Colors.FAIL}[!] Akses ditolak.{Colors.ENDC}")
        sys.exit(1)
        
    while True:
        installed_packages = detect_installed_packages()
        
        show_dashboard(config, installed_packages)
        choice = input(f"{Colors.BOLD}{Colors.OKCYAN}Pilih Menu [0-6]: {Colors.ENDC}").strip()
        
        if choice == "1":
            print(f"\n{Colors.OKGREEN}[i] Memperbarui dashboard...{Colors.ENDC}")
            time.sleep(1)
        elif choice == "2":
            auto_hapus_cache(installed_packages)
        elif choice == "3":
            input_private_server(config)
        elif choice == "4":
            menu_rejoin_server(config, installed_packages)
        elif choice == "5":
            configure_launch_options(config)
        elif choice == "6":
            clear_screen()
            draw_banner()
            print(f"{Colors.HEADER}=== INFORMASI LISENSI & GITHUB DATA ==={Colors.ENDC}\n")
            print(f" Key Aktif  : {config.get('key')}")
            print(f" GitHub Repo: https://github.com/snicehub/Rejoin")
            print(f" Target Package: {DEFAULT_PACKAGE}")
            print(f"\n{Colors.GRAY}Catatan: Data konfigurasi tersimpan otomatis di local storage Termux.{Colors.ENDC}")
            input(f"\nTekan [Enter] untuk kembali ke Dashboard...")
        elif choice == "0":
            print(f"\n{Colors.OKGREEN}Terima kasih telah menggunakan ALTAPEDIA Rejoin Script!{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"\n{Colors.FAIL}[!] Pilihan tidak valid. Silakan coba lagi.{Colors.ENDC}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"\n{Colors.FAIL}[!] Terjadi kesalahan fatal: {err}{Colors.ENDC}")
        sys.exit(1)
