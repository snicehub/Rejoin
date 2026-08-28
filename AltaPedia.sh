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

run_clear_cache() {
    stty sane 2>/dev/null
    clear
    echo -e "\033[1;33m[*] Memindai aplikasi kloningan Altapedia...\033[0m"
    PACKAGES=$($SU_CMD "pm list packages | grep altapedia" | sed 's/package://g' | tr -d '\r' | sort)

    if [ -z "$PACKAGES" ]; then
        echo -e "\n\033[1;31m[!] Tidak ada aplikasi Altapedia yang terdeteksi!\033[0m"
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
    echo -e "\033[1;33m"
    echo "========================================"
    echo "          AUTO JOIN PRIVATE SERVER      "
    echo "========================================"
    echo -e "\033[0m"
    
    printf "\033[1;36m[?]\033[0m \033[1;37mMasukkan Link Private Server : \033[0m"
    read -r PS_LINK

    while [ -z "$PS_LINK" ]; do
        echo -e "\n\033[1;31m[!] Link Private Server tidak boleh kosong!\033[0m"
        printf "\033[1;36m[?]\033[0m \033[1;37mMasukkan Link Private Server : \033[0m"
        read -r PS_LINK
    done

    echo ""
    echo -e "\033[1;33m[*] Memindai aplikasi kloningan Altapedia...\033[0m"
    PACKAGES=$($SU_CMD "pm list packages | grep altapedia" | sed 's/package://g' | tr -d '\r' | sort)

    if [ -z "$PACKAGES" ]; then
        echo -e "\n\033[1;31m[!] Tidak ada aplikasi Altapedia yang terdeteksi!\033[0m"
        sleep 2
        return
    fi

    TOTAL_PKG=$(echo "$PACKAGES" | wc -w)
    CURRENT=1
    DELAY=40  # Jeda awal 40 detik dari apk 1 ke apk 2

    echo "========================================"
    echo -e "\033[1;32m[*] Memulai Auto Join ke $TOTAL_PKG aplikasi...\033[0m"
    echo "========================================"

    for pkg in $PACKAGES; do
        echo ""
        echo "----------------------------------------"
        echo -e "\033[1;36m[$CURRENT/$TOTAL_PKG] Memproses: $pkg\033[0m"
        echo "----------------------------------------"
        
        # 1. Hentikan aplikasi
        $SU_CMD "am force-stop $pkg" >/dev/null 2>&1
        
        # 2. Buka aplikasi & masuk Private Server
        echo -e "\033[1;33m[*] Membuka aplikasi & masuk PS...\033[0m"
        $SU_CMD "am start -a android.intent.action.VIEW -d '$PS_LINK' -p $pkg" >/dev/null 2>&1
        echo -e "\033[1;32m[✓] Berhasil membuka $pkg.\033[0m"

        # 3. Jeda waktu dinamis (40s, 60s, 80s, dst)
        if [ $CURRENT -lt $TOTAL_PKG ]; then
            echo ""
            echo -e "\033[1;35m[⏳] Menunggu jeda waktu ${DELAY} detik ke akun berikutnya...\033[0m"
            for ((i=DELAY; i>0; i--)); do
                printf "\r\033[1;33m[⏳] Sisa waktu jeda: %2d detik... \033[0m" $i
                sleep 1
            done
            printf "\r\033[1;32m[✓] Jeda waktu selesai.                         \033[0m\n"
            
            # Kelipatan tambah 20 detik untuk apk berikutnya
            DELAY=$((DELAY + 20))
        else
            # Jeda khusus 10 detik setelah aplikasi terakhir terbuka sebelum Termux tertutup
            echo ""
            echo -e "\033[1;35m[⏳] Aplikasi terakhir selesai. Menunggu 10 detik sebelum menutup Termux...\033[0m"
            for ((i=10; i>0; i--)); do
                printf "\r\033[1;33m[⏳] Menutup Termux dalam: %2d detik... \033[0m" $i
                sleep 1
            done
            printf "\r\033[1;32m[✓] Selesai. Menutup Termux sekarang...          \033[0m\n"
        fi

        CURRENT=$((CURRENT + 1))
    done

    echo ""
    echo "========================================"
    echo -e "\033[1;32m SUCCESS: Semua proses selesai!\033[0m"
    echo "========================================"
    sleep 1

    # Perintah otomatis menutup Termux via root
    $SU_CMD "am force-stop com.termux" >/dev/null 2>&1
    exit 0
done

while true; do
    stty sane 2>/dev/null
    clear
    # Warna Orange (Kode ANSI 38;5;208 atau 33)
    printf "\033[38;5;208m"
    printf " █████╗ ██╗  ████████╗██████╗ ██████╗ ███████╗██████╗ ██╗ █████╗ \n"
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
