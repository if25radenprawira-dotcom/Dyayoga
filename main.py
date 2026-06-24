import csv
import os
import sys  

FILE_BUKU = 'buku.csv'
FILE_PENGUNJUNG = 'pengunjung.csv'

class QueuePengunjung:
    def __init__(self):
        self.data = []
        
    def tambah_pengunjung(self, nama):
        self.data.append(nama)
        # Langsung simpan ke CSV tiap ada yang masuk
        with open(FILE_PENGUNJUNG, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([nama])
            
    def lihat_pengunjung(self):
        return self.data

antrean_pengunjung = QueuePengunjung()

# --- FUNGSI INISIALISASI (Membuat 5 Data Awal) ---
def init_csv():
    # Jika file buku belum ada, buatkan otomatis beserta 5 isinya
    if not os.path.exists(FILE_BUKU):
        with open(FILE_BUKU, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id_buku', 'judul', 'pengarang', 'status'])
            writer.writerows([
                ['B001', 'Naruto', 'Masashi Kishimoto', 'Tersedia'],
                ['B002', 'One Piece', 'Eiichiro Oda', 'Tersedia'],
                ['B003', 'Attack on Titan', 'Hajime Isayama', 'Tersedia'],
                ['B004', 'Jujutsu Kaisen', 'Gege Akutami', 'Tersedia'],
                ['B005', 'Demon Slayer', 'Koyoharu Gotouge', 'Tersedia']
            ])
            
    # Buat file pengunjung jika belum ada
    if not os.path.exists(FILE_PENGUNJUNG):
        with open(FILE_PENGUNJUNG, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nama_pengunjung'])

# --- FUNGSI BACA DATA ---
def baca_buku():
    data = []
    try:
        with open(FILE_BUKU, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass
    return data

# --- FUNGSI CRUD BUKU ---
def lihat_buku():
    buku_list = baca_buku()
    print("\n  DAFTAR BUKU PERPUSTAKAAN:")
    print("  " + "-"*60)
    for buku in buku_list:
        print(f"  [{buku['id_buku']}] {buku['judul']} - {buku['pengarang']} ({buku['status']})")
    print("  " + "-"*60)

def tambah_buku():
    print("\n  [+] TAMBAH BUKU BARU")
    id_buku = input("  Masukkan ID Buku  : ")
    judul = input("  Masukkan Judul    : ")
    pengarang = input("  Masukkan Pengarang: ")
    
    with open(FILE_BUKU, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id_buku, judul, pengarang, "Tersedia"])
    print("  ✅ Buku berhasil ditambahkan!")

def proses_pinjam():
    lihat_buku()
    data_buku = baca_buku()
    id_target = input("\n  Masukkan ID Buku yang mau dipinjam: ")
    
    ditemukan = False
    for buku in data_buku:
        if buku['id_buku'] == id_target:
            ditemukan = True
            if buku['status'] == 'Tersedia':
                buku['status'] = 'Dipinjam'
                print(f"  ✅ Anda berhasil meminjam '{buku['judul']}'")
            else:
                print("  ❌ Maaf, buku ini sedang dipinjam orang lain.")
            break
            
    if ditemukan:
        simpan_ulang_buku(data_buku)
    else:
        print("  ❌ ID Buku tidak ditemukan.")

def proses_kembali():
    data_buku = baca_buku()
    id_target = input("\n  Masukkan ID Buku yang mau dikembalikan: ")
    
    ditemukan = False
    for buku in data_buku:
        if buku['id_buku'] == id_target:
            ditemukan = True
            if buku['status'] == 'Dipinjam':
                buku['status'] = 'Tersedia'
                print(f"  ✅ Buku '{buku['judul']}' berhasil dikembalikan.")
            else:
                print("  ℹ️ Buku ini memang sedang tidak dipinjam (Tersedia).")
            break
            
    if ditemukan:
        simpan_ulang_buku(data_buku)
    else:
        print("  ❌ ID Buku tidak ditemukan.")

def simpan_ulang_buku(data_buku):
    with open(FILE_BUKU, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id_buku', 'judul', 'pengarang', 'status'])
        writer.writeheader()
        writer.writerows(data_buku)

def catat_pengunjung():
    print("\n  [+] CATAT PENGUNJUNG")
    nama = input("  Masukkan Nama Pengunjung: ")
    antrean_pengunjung.tambah_pengunjung(nama)
    print(f"  ✅ Selamat membaca di perpustakaan, {nama}!")

# --- UI MENU UTAMA ---
def tampilkan_menu():
    print("\n  ┌──────────────────────────────────────────┐")
    print("  │        SISTEM PERPUSTAKAAN DIGITAL       │")
    print("  ├──────────────────────────────────────────┤")
    print("  │  1. Lihat Daftar Buku                    │")
    print("  │  2. Tambah Buku Baru                     │")
    print("  │  3. Pinjam Buku                          │")
    print("  │  4. Kembalikan Buku                      │")
    print("  │  5. Catat Pengunjung Masuk               │")
    print("  │  0. Keluar                               │")
    print("  └──────────────────────────────────────────┘")

def main():
    init_csv() 
    while True:
        tampilkan_menu()
        pilihan = input("  Pilih menu (0-5): ")
        
        if pilihan == '1':
            lihat_buku()
        elif pilihan == '2':
            tambah_buku()
        elif pilihan == '3':
            proses_pinjam()
        elif pilihan == '4':
            proses_kembali()
        elif pilihan == '5':
            catat_pengunjung()
        elif pilihan == '0':
            print("\n  Terima kasih telah menggunakan sistem ini! Program ditutup.")
            sys.exit()  
        else:
            print("  ❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()