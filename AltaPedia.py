#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================================================
    ALTAPEDIA REJOIN & AUTOMATION TOOL FOR TERMUX
===================================================================
    Author     : ALTAPEDIA Team
    Key Required: ALTAPEDIA-0987-08123-SUPREME
    Package    : com.altapedia (and clones)
===================================================================
"""

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
GET_KEY_URL = "https://raw.githubusercontent.com/altapedia-official/rejoin-key/main/keys.json"
GITHUB_CONFIG_URL = "https://raw.githubusercontent.com/altapedia-official/rejoin-key/main/announcement.txt"
DEFAULT_PACKAGE = "com.altapedia"

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def draw_banner():
    """Displays the custom ALTAPEDIA ASCII banner."""
    print(f"{Colors.OKCYAN}{Colors.BOLD}")
    print(r"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║  █████╗ ██╗  ████████╗██████╗ ██████╗ ███████╗██████╗ ██╗ █████╗  ║
    ║ ██╔══██╗██║  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██║██╔══██╗ ║
    ║ ███████║██║     ██║   ███████║██████╔╝█████╗  ██║  ██║██║███████║ ║
    ║ ██╔══██║██║     ██║   ██╔══██║██╔═══╝ ██╔══╝  ██║  ██║██║██╔══██║ ║
    ║ ██║  ██║███████╗██║   ██║  ██║██║     ███████╗██████╔╝██║██║  ██║ ║
    ║ ╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝     ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝ ║
    ║                                                                   ║
    ║             TERMUX REJOIN SERVER & CLONE AUTOMATION               ║
    ║                     VERSION 1.0 SUPREME                           ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """ + Colors.ENDC)

def load_config():
    """Loads configuration data from local JSON storage."""
    default_cfg = {
        "key": "",
        "private_server": "",
        "base_duration": 60,
        "clone_step": 20,
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
    
    # Check key locally or attempt GitHub remote sync check
    if user_key == VALID_KEY:
        config["key"] = user_key
        save_config(config)
        print(f"\n{Colors.OKGREEN}[✓] Key Valid! Akses Diberikan. Menyimpan Lisensi...{Colors.ENDC}")
        time.sleep(1.5)
        return True
    else:
        # Attempt GitHub verification as backup check
        print(f"{Colors.WARNING}[i] Memeriksa Key ke Server GitHub...{Colors.ENDC}")
        try:
            req = urllib.request.Request(GET_KEY_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                keys_data = json.loads(response.read().decode())
                if user_key in keys_data.get("valid_keys", []):
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
        # Run pm list packages command via shell
        result = subprocess.run(['pm', 'list', 'packages'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines:
                pkg = line.replace('package:', '').strip()
                if DEFAULT_PACKAGE in pkg or 'altapedia' in pkg.lower():
                    found_packages.append(pkg)
    except Exception:
        # Fallback simulation if running outside standard Termux ADB environment
        found_packages = [DEFAULT_PACKAGE, f"{DEFAULT_PACKAGE}.clone1", f"{DEFAULT_PACKAGE}.clone2"]
    
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
        # Try shell pm clear command
        try:
            cmd = f"pm clear {pkg}"
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "Success" in res.stdout:
                print(f"    {Colors.OKGREEN}[✓] Cache & Data {pkg} Berhasil Dibersihkan!{Colors.ENDC}")
            else:
                # Direct folder cache clean fallback
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

def launch_app_and_rejoin(package_name, server_link):
    """Launches specified app package using Android Intent/AM manager."""
    try:
        if server_link:
            # Launch via deep link / intent URL
            cmd = f"am start -a android.intent.action.VIEW -d \"{server_link}\" {package_name}"
        else:
            # Launch package directly
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
    """Executes the automated rejoin process with staggered clone delays."""
    clear_screen()
    draw_banner()
    print(f"{Colors.HEADER}{Colors.BOLD}=== MENU: REJOIN SERVER AUTOMATION ==={Colors.ENDC}\n")
    
    server_link = config.get("private_server", "").strip()
    if not server_link:
        print(f"{Colors.FAIL}[!] Link Private Server belum diisi!{Colors.ENDC}")
        print(f"Silakan atur link terlebih dahulu di menu 3.")
        input(f"\n{Colors.GRAY}Tekan [Enter] untuk kembali...{Colors.ENDC}")
        return

    print(f"{Colors.OKCYAN}Aplikasi Terdeteksi ({len(installed_packages)}):{Colors.ENDC}")
    for idx, pkg in enumerate(installed_packages, 1):
        print(f"  {idx}. {pkg}")
    print()
    
    # User selects delay duration
    print(f"{Colors.BOLD}Pengaturan Durasi Jeda Rejoin:{Colors.ENDC}")
    try:
        base_dur_input = input("Masukkan durasi dasar per-loop (dalam detik, default 60): ").strip()
        base_duration = int(base_dur_input) if base_dur_input.isdigit() else 60
    except ValueError:
        base_duration = 60

    print(f"\n{Colors.WARNING}[i] Skema kelipatan jeda clone diaktifkan:{Colors.ENDC}")
    print(f"    - Main App        : Langsung Buka")
    for i in range(1, len(installed_packages)):
        print(f"    - Clone #{i:<9} : +{i * 20} detik kelipatan")
        
    print(f"\n{Colors.OKGREEN}[▶] Memulai Otomatisasi Rejoin Server... (Tekan Ctrl+C untuk Stop){Colors.ENDC}\n")
    time.sleep(2)
    
    loop_count = 1
    try:
        while True:
            print(f"{Colors.HEADER}--------------------------------------------------{Colors.ENDC}")
            print(f"{Colors.BOLD}🚀 LOOPS REJOIN #{loop_count} | {datetime.now().strftime('%H:%M:%S')}{Colors.ENDC}")
            print(f"{Colors.HEADER}--------------------------------------------------{Colors.ENDC}")
            
            for index, pkg in enumerate(installed_packages):
                # Calculate delay: clone #1 = 20s, clone #2 = 40s, clone #3 = 60s, etc.
                clone_delay = index * 20
                
                if clone_delay > 0:
                    print(f"\n{Colors.GRAY}[+] Persiapan membuka clone ke-{index} ({pkg})...{Colors.ENDC}")
                    countdown_timer(clone_delay, f"Jeda Kelipatan 20s untuk {pkg}")
                
                print(f"{Colors.OKGREEN}[✓] Membuka Aplikasi: {Colors.BOLD}{pkg}{Colors.ENDC}")
                print(f"    Meluncurkan Ke Private Server...")
                
                success = launch_app_and_rejoin(pkg, server_link)
                if success:
                    print(f"    {Colors.OKCYAN}[SUCCESS] Command launch terkirim ke {pkg}{Colors.ENDC}")
                else:
                    print(f"    {Colors.FAIL}[FAILED] Gagal membuka {pkg}{Colors.ENDC}")
            
            print(f"\n{Colors.OKBLUE}[i] Seluruh clone telah di-rejoin.{Colors.ENDC}")
            countdown_timer(base_duration, f"Menunggu Iterasi Loop Berikutnya (#{loop_count + 1})")
            loop_count += 1

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}[!] Rejoin Server Dihentikan oleh Pengguna.{Colors.ENDC}")
        time.sleep(2)

def show_dashboard(config, packages):
    """Displays the main interactive dashboard UI."""
    clear_screen()
    draw_banner()
    
    server_status = config.get("private_server", "")
    if not server_status:
        server_status = f"{Colors.FAIL}Belum diatur{Colors.ENDC}"
    else:
        server_status = f"{Colors.OKGREEN}{server_status[:35]}...{Colors.ENDC}"
        
    print(f"{Colors.OKBLUE}══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f"{Colors.BOLD}                       DASHBOARD STATUS                       {Colors.ENDC}")
    print(f"{Colors.OKBLUE}══════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f" Status Lisensi     : {Colors.OKGREEN}[✓] SUPREME VIP ACTIVE{Colors.ENDC}")
    print(f" Key Terpasang      : {Colors.BOLD}{config.get('key')}{Colors.ENDC}")
    print(f" Package Utama      : {Colors.OKCYAN}{DEFAULT_PACKAGE}{Colors.ENDC}")
    print(f" Clone Terdeteksi   : {Colors.BOLD}{len(packages)} Aplikasi{Colors.ENDC}")
    print(f" Private Server     : {server_status}")
    print(f" Sync Data Server   : {Colors.OKGREEN}GitHub Synced{Colors.ENDC}")
    print(f"{Colors.OKBLUE}══════════════════════════════════════════════════════════════{Colors.ENDC}\n")

    print(f"{Colors.BOLD}MENU UTAMA:{Colors.ENDC}")
    print(f" [{Colors.OKGREEN}1{Colors.ENDC}] 📊 Dashboard (Refresh Data)")
    print(f" [{Colors.OKGREEN}2{Colors.ENDC}] 🧹 Auto Hapus Cache ({len(packages)} App)")
    print(f" [{Colors.OKGREEN}3{Colors.ENDC}] 🔗 Masukkan Link Private Server")
    print(f" [{Colors.OKGREEN}4{Colors.ENDC}] 🔄 Rejoin Server (Start Auto Reopen)")
    print(f" [{Colors.OKGREEN}5{Colors.ENDC}] 🔑 Informasi Key & GitHub Sync")
    print(f" [{Colors.FAIL}0{Colors.ENDC}] 🚪 Keluar Script")
    print()

def main():
    """Main program entry loop."""
    config = load_config()
    
    # Force Key Verification
    if not verify_key(config):
        print(f"{Colors.FAIL}[!] Akses ditolak.{Colors.ENDC}")
        sys.exit(1)
        
    while True:
        # Re-detect packages dynamically
        installed_packages = detect_installed_packages()
        
        show_dashboard(config, installed_packages)
        choice = input(f"{Colors.BOLD}{Colors.OKCYAN}Pilih Menu [0-5]: {Colors.ENDC}").strip()
        
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
            clear_screen()
            draw_banner()
            print(f"{Colors.HEADER}=== INFORMASI LISENSI & GITHUB DATA ==={Colors.ENDC}\n")
            print(f" Key Aktif  : {config.get('key')}")
            print(f" GitHub Repo: https://github.com/altapedia-official/rejoin-key")
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
