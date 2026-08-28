#!/usr/bin/env bash
stty sane 2>/dev/null
clear

if [ -f /system/xbin/su ]; then
    SU_CMD="/system/xbin/su -c"
elif [ -f /system/bin/su ]; then
    SU_CMD="/system/bin/su -c"
else
    SU_CMD="su -c"
fi

get_installed_packages() {
    local detected=""
    local target_list="com.altapedia.liteA com.altapedia.liteB com.altapedia.liteC com.altapedia.liteD com.altapedia.liteE com.altapedia.liteF com.altapedia.liteG com.altapedia.liteH com.altapedia.liteI com.altapedia.liteJ com.altapedia.liteK com.altapedia.liteL com.altapedia.liteM com.altapedia.liteN com.altapedia.liteO"
    
    for pkg in $target_list; do
        if $SU_CMD "[ -d /data/data/$pkg ] || [ -d /data/app/$pkg* ]" 2>/dev/null; then
            detected="$detected $pkg"
        fi
    done
    
    echo "$detected" | xargs
}

run_clear_cache() {
    stty sane 2>/dev/null
    clear
    echo -e "\033[1;33m[*] Memindai aplikasi Altapedia yang terinstal...\033[0m"
    
    PACKAGES=$(get_installed_packages)

    if [ -z "$PACKAGES" ]; then
        echo -e "\n\033[1;31m[!] Tidak ada aplikasi Altapedia yang terinstal di HP ini! Sistem dibatalkan.\033[0m"
        sleep 2
        return
    fi

    echo -e "\n\033[1;33m[*] Memulai pembersihan cache secara berurutan...\033[0m"
    echo "----------------------------------------"

    for pkg in $PACKAGES; do
        echo -e "\033[1;36m[*] Memproses: $pkg\033[0m"
        $SU_CMD "am force-stop $pkg" >/dev/null 2>&1
        $SU_CMD "rm -rf /data/data/$pkg/cache/* /data/data/$pkg/code_cache/* /sdcard/Android/data/$pkg/cache/* /storage/emulated/0/Android/data/$pkg/cache/*" >/dev/null 2>&1
        echo -e "\033[1;32m[✓] Cache $pkg berhasil dibersihkan.\033[0m"
        echo ""
    done

    echo "----------------------------------------"
    echo -e "\033[1;32m SUCCESS: Semua cache berhasil dihapus!\033[0m"
    echo "----------------------------------------"
    echo ""
    read -p "Tekan [Enter] untuk kembali ke menu..."
}

run_auto_join() {
    stty sane 2>/dev/null
    clear
    echo -e "\033[1;33m[*] Memindai aplikasi Altapedia yang terinstal...\033[0m"
    
    PACKAGES=$(get_installed_packages)

    if [ -z "$PACKAGES" ]; then
        echo -e "\n\033[1;31m[!] Tidak ada aplikasi Altapedia yang terinstal di HP ini! Sistem dibatalkan.\033[0m"
        sleep 2
        return
    fi

    echo -e "\n\033[1;32m========================================\033[0m"
    echo -e "\033[1;32m       MASUKKAN LINK PRIVATE SERVER     \033[0m"
    echo -e "\033[1;32m========================================\033[0m"

    i=1
    declare -a PKG_ARRAY
    declare -a LINK_ARRAY

    for pkg in $PACKAGES; do
        PKG_ARRAY[$i]="$pkg"
        echo -e "\033[1;36m${i}.) $pkg\033[0m"
        printf "\033[1;33m   - Link Private Server : \033[0m"
        read -r input_link
        
        while [ -z "$input_link" ]; do
            echo -e "\033[1;31m   [!] Link tidak boleh kosong!\033[0m"
            printf "\033[1;33m   - Link Private Server : \033[0m"
            read -r input_link
        done
        
        LINK_ARRAY[$i]="$input_link"
        i=$((i + 1))
    done

    TOTAL_PKG=${#PKG_ARRAY[@]}
    DELAY=40

    echo ""
    echo "========================================"
    echo -e "\033[1;32m[*] Memulai Auto Join ke $TOTAL_PKG aplikasi...\033[0m"
    echo "========================================"

    for ((idx=1; idx<=TOTAL_PKG; idx++)); do
        pkg="${PKG_ARRAY[idx]}"
        ps_link="${LINK_ARRAY[idx]}"

        echo ""
        echo "----------------------------------------"
        echo -e "\033[1;36m[$idx/$TOTAL_PKG] Memproses: $pkg\033[0m"
        echo "----------------------------------------"
        
        # 1. Hentikan aplikasi agar bersih saat dibuka ulang
        $SU_CMD "am force-stop $pkg" >/dev/null 2>&1
        sleep 1

        # 2. Buka aplikasi dan paksa masuk ke Private Server
        echo -e "\033[1;33m[*] Membuka aplikasi & masuk PS...\033[0m"
        $SU_CMD "am start -n $pkg/com.roblox.client.Activity -a android.intent.action.VIEW -d '$ps_link'" >/dev/null 2>&1
        
        if [ $? -ne 0 ]; then
            $SU_CMD "am start -a android.intent.action.VIEW -d '$ps_link' -p $pkg" >/dev/null 2>&1
        fi
        
        echo -e "\033[1;32m[✓] Perintah buka $pkg dikirim.\033[0m"

        # 3. Hitung mundur jeda waktu
        if [ $idx -lt $TOTAL_PKG ]; then
            echo ""
            echo -e "\033[1;35m[⏳] Menunggu jeda waktu ${DELAY} detik ke akun berikutnya...\033[0m"
            for ((t=DELAY; t>0; t--)); do
                printf "\r\033[1;33m[⏳] Sisa waktu jeda: %2d detik...      \033[0m" $t
                sleep 1
            done
            echo -e "\n\033[1;32m[✓] Jeda waktu selesai.\033[0m"
            
            DELAY=$((DELAY + 20))
        else
            echo ""
            echo -e "\033[1;35m[⏳] Aplikasi terakhir selesai. Menunggu 10 detik sebelum menutup Termux...\033[0m"
            for ((t=10; t>0; t--)); do
                printf "\r\033[1;33m[⏳] Menutup Termux dalam: %2d detik...      \033[0m" $t
                sleep 1
            done
            echo -e "\n\033[1;32m[✓] Selesai. Menutup Termux sekarang...\033[0m"
        fi
    done

    echo ""
    echo "========================================"
    echo -e "\033[1;32m SUCCESS: Semua proses selesai!\033[0m"
    echo "========================================"
    sleep 1

    $SU_CMD "am force-stop com.termux" >/dev/null 2>&1
    exit 0
}

while true; do
    stty sane 2>/dev/null
    clear
    printf "\033[38;5;208m"
    printf " █████╗ ██╗  ████████╗█████╗ ██████╗ ███████╗██████╗ ██╗ █████╗ \n"
    printf "██╔══██╗██║  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██║██╔══██╗\n"
    printf "███████║██║     ██║   ███████║██████╔╝█████╗  ██║  ██║██║███████║\n"
    printf "██╔══██║██║     ██║   ██╔══██║██╔═══╝ ██╔══╝  ██║  ██║██║██╔══██║\n"
    printf "██║  ██║███████╗██║   ██║  ██║██║     ███████╗██████╔╝██║██║  ██║\n"
    printf "╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝     ╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝\n"
    printf "\033[1;37mVersion 1.0.0\033[0m\n\n"
    echo "======================================================================="
    echo -e "  \033[1;32m1)\033[0m Automatic Clear Cache"
    echo -e "  \033[1;32m2)\033[0m Auto Join PS"
    echo -e "  \033[1;31m3)\033[0m Exit\n"
    
    echo -ne "\033[1;36m[?]\033[0m \033[1;37mPilih Menu [1-3]: \033[0m"
    read -r choice

    case "$choice" in
        1)
            run_clear_cache
            ;;
        2)
            run_auto_join
            ;;
        3)
            echo -e "\n\033[1;31m[!] Keluar dari script.\033[0m"
            exit 0
            ;;
        * )
            echo -e "\n\033[1;31m[!] Pilihan tidak valid!\033[0m"
            sleep 1
            ;;
    esac
done
