import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Fungsi untuk membuat koneksi ke database MySQL
def buat_koneksi():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='kalkulator_db'
    )
    return conn

# Fungsi untuk menghitung operasi matematika
def hitung():
    try:
        operasi = entry.get()
        hasil = eval(operasi)
        if isinstance(hasil, int):
            result_label.config(text="Hasil: {}".format(hasil)) 
        else:
            result_label.config(text="Hasil: {:.2f}".format(hasil)) 
        simpan_ke_histori(operasi, hasil) 
    except Exception as e: 
        messagebox.showerror("Error", str(e)) 

# Fungsi untuk menyimpan perhitungan ke dalam database MySQL
def simpan_ke_histori(operasi, hasil):
    conn = buat_koneksi()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS histori (operasi TEXT, hasil REAL)")
    c.execute("INSERT INTO histori (operasi, hasil) VALUES (%s, %s)", (operasi, hasil))
    conn.commit()
    conn.close()

# Fungsi untuk menampilkan histori perhitungan
def tampilkan_histori():
    conn = buat_koneksi()
    c = conn.cursor()
    c.execute("SELECT * FROM histori")
    histori = c.fetchall()
    conn.close()
    if not histori:
        messagebox.showinfo("Info", "Histori kosong")
        return

    display_history = tk.Toplevel(root)
    display_history.title("Histori")
    display_history.configure(bg='#2E2E2E')
    label_histori = tk.Label(display_history, text="Histori:", bg='#2E2E2E', fg='white')
    label_histori.grid(row=0, column=0, padx=10, pady=5)
    nomor_baris = 1
    for item in histori:
        operasi, hasil = item
        teks_histori = operasi + " = {:.2f}".format(hasil)
        label_item_histori = tk.Label(display_history, text=teks_histori, bg='#2E2E2E', fg='white')
        label_item_histori.grid(row=nomor_baris, column=0, padx=10, pady=2, sticky="w")

        # Tombol untuk memasukkan hasil histori ke kotak masukan
        tombol_masukkan = tk.Button(display_history, text="Gunakan", command=lambda res=hasil: masukkan_hasil_histori(res), bg='#4A4A4A', fg='white')
        tombol_masukkan.grid(row=nomor_baris, column=1, padx=5, pady=2, sticky="e")

        nomor_baris += 1

# Fungsi untuk memasukkan hasil histori ke kotak masukan
def masukkan_hasil_histori(hasil):
    entry.delete(0, tk.END)  
    entry.insert(tk.END, str(hasil))  
    
# Fungsi untuk membersihkan kotak masukan
def bersihkan_entry():
    entry.delete(0, tk.END) 

# Membuat GUI
root = tk.Tk()
root.title("Kalkulator")
root.configure(bg='#2E2E2E')
root.geometry("350x600")
root.resizable(True, True)

# Mengatur grid weights untuk root
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_columnconfigure(0, weight=1)

# Frame untuk hasil dan kotak masukan
frame_hasil = tk.Frame(root, bg="#2E2E2E")
frame_hasil.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Mengatur grid weights untuk frame_hasil
frame_hasil.grid_rowconfigure(0, weight=1)
frame_hasil.grid_rowconfigure(1, weight=1)
frame_hasil.grid_columnconfigure(0, weight=1)

entry = tk.Entry(frame_hasil, font=("Segoe UI", 20), bd=5, justify="right", bg="#4A4A4A", fg="white")
entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

result_label = tk.Label(frame_hasil, text="Hasil: ", font=("Segoe UI", 14), bg="#2E2E2E", fg="white")
result_label.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

# Frame untuk tombol-tombol kalkulator
frame_tombol = tk.Frame(root, bg="#2E2E2E")
frame_tombol.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

tombol = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '+', '%', '=', 'C'
]

# Warna lebih gelap untuk tombol operasi
warna_tombol_operasi = "#3A3A3A"

nomor_baris = 0
kolom = 0
for teks_tombol in tombol:
    if teks_tombol == '=':
        tk.Button(frame_tombol, text=teks_tombol, font=("Segoe UI", 14), bg="#0078D7", fg="white", command=hitung).grid(row=nomor_baris, column=kolom, padx=5, pady=5, sticky="nsew")
    elif teks_tombol == '0':
        tk.Button(frame_tombol, text=teks_tombol, font=("Segoe UI", 14), bg="#4A4A4A", fg="white", command=lambda b=teks_tombol: entry.insert(tk.END, b)).grid(row=nomor_baris, column=kolom, columnspan=2, padx=5, pady=5, sticky="nsew")
        kolom += 1
    elif teks_tombol == 'C':
        tk.Button(frame_tombol, text=teks_tombol, font=("Segoe UI", 14), bg="#D70000", fg="white", command=bersihkan_entry).grid(row=nomor_baris, column=kolom, padx=5, pady=5, sticky="nsew")
    elif teks_tombol in ['/', '*', '-', '+', '%']:
        tk.Button(frame_tombol, text=teks_tombol, font=("Segoe UI", 14), bg=warna_tombol_operasi, fg="white", command=lambda b=teks_tombol: entry.insert(tk.END, b)).grid(row=nomor_baris, column=kolom, padx=5, pady=5, sticky="nsew")
    else:
        tk.Button(frame_tombol, text=teks_tombol, font=("Segoe UI", 14), bg="#4A4A4A", fg="white", command=lambda b=teks_tombol: entry.insert(tk.END, b)).grid(row=nomor_baris, column=kolom, padx=5, pady=5, sticky="nsew")
    kolom += 1
    if kolom > 3:
        kolom = 0
        nomor_baris += 1

# Mengatur grid weights untuk frame_tombol
for i in range(4):
    frame_tombol.grid_columnconfigure(i, weight=1)
for i in range(5):
    frame_tombol.grid_rowconfigure(i, weight=1)

# Tombol untuk menampilkan histori
tombol_histori = tk.Button(root, text="Histori", font=("Segoe UI", 12), bg="#4A4A4A", fg="white", command=tampilkan_histori)
tombol_histori.grid(row=2, column=0, pady=5)

# Mengatur grid weights untuk root (agar histori tetap di bagian bawah)
root.grid_rowconfigure(2, weight=1)

root.mainloop()
