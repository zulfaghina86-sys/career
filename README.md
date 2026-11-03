# Analisis Penjualan Retail 2025

Proyek analisis end-to-end: membuat data transaksi, membersihkannya, menghitung KPI, dan memvisualisasikan temuan.

> **Catatan:** data pada proyek ini **sintetis** (dibuat oleh `analysis.py` dengan seed tetap) agar hasilnya bisa direproduksi oleh siapa pun. Ganti dengan data asli untuk analisis nyata.

## Pertanyaan bisnis
1. Berapa total omzet dan bagaimana tren bulanannya?
2. Kategori dan kota mana yang paling berkontribusi?
3. Seberapa bersih data mentahnya?

## Temuan utama
- Total omzet **Rp3,46 miliar** dari 3.000 transaksi, rata-rata nilai order sekitar Rp1,15 juta.
- **Elektronik** menyumbang sekitar 66% omzet meski bukan kategori dengan transaksi terbanyak.
- **Jakarta** adalah kota terbesar (sekitar 33% omzet).
- Pembersihan data: 30 baris duplikat dihapus, 39 nilai kota kosong diberi label "Tidak Diketahui", dan penulisan kota diseragamkan.

![Omzet bulanan](output/omzet_bulanan.png)
![Omzet per kategori dan kota](output/omzet_kategori_kota.png)

## Cara menjalankan
```bash
pip install -r ../../requirements.txt
python analysis.py
```
Hasil tersimpan di folder `data/` (CSV mentah dan bersih) dan `output/` (grafik dan `ringkasan.md`).

## Tools
Python, pandas, NumPy, Matplotlib
