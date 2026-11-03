"""Analisis penjualan retail 2025 (data sintetis).

Alur: generate data -> bersihkan -> hitung KPI -> buat grafik -> simpan ringkasan.
Jalankan dari folder proyek:  python analysis.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).parent
DATA = BASE / "data"
OUT = BASE / "output"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

rng = np.random.default_rng(42)


def generate_data(n: int = 3000) -> pd.DataFrame:
    """Membuat data transaksi sintetis (sengaja disisipi data kotor)."""
    kategori = {
        "Elektronik": (1_500_000, 400_000),
        "Fashion": (250_000, 80_000),
        "Makanan": (60_000, 20_000),
        "Rumah Tangga": (400_000, 120_000),
    }
    kota = ["Jakarta", "Bandung", "Surabaya", "Medan", "Yogyakarta"]
    tanggal = pd.to_datetime("2025-01-01") + pd.to_timedelta(
        rng.integers(0, 365, n), unit="D"
    )
    kat = rng.choice(list(kategori), n, p=[0.2, 0.3, 0.35, 0.15])
    harga = np.array([max(rng.normal(*kategori[k]), 10_000) for k in kat]).round(-3)
    df = pd.DataFrame(
        {
            "order_id": np.arange(1, n + 1),
            "tanggal": tanggal,
            "kota": rng.choice(kota, n, p=[0.35, 0.2, 0.2, 0.1, 0.15]),
            "kategori": kat,
            "harga_satuan": harga,
            "jumlah": rng.integers(1, 5, n),
        }
    )
    # Data kotor: nilai kosong, duplikat, dan penulisan tidak konsisten
    df.loc[rng.choice(n, 40, replace=False), "kota"] = np.nan
    df.loc[rng.choice(n, 25, replace=False), "kota"] = "  jakarta "
    df = pd.concat([df, df.sample(30, random_state=1)], ignore_index=True)
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().copy()
    df["kota"] = df["kota"].str.strip().str.title().fillna("Tidak Diketahui")
    df["omzet"] = df["harga_satuan"] * df["jumlah"]
    df["bulan"] = df["tanggal"].dt.to_period("M").dt.to_timestamp()
    return df


def rupiah(x: float) -> str:
    return f"Rp{x:,.0f}".replace(",", ".")


def main() -> None:
    raw = generate_data()
    raw.to_csv(DATA / "transaksi_mentah.csv", index=False)
    df = clean(raw)
    df.to_csv(DATA / "transaksi_bersih.csv", index=False)

    total = df["omzet"].sum()
    kpi = {
        "Total omzet": rupiah(total),
        "Jumlah transaksi": f"{len(df):,}".replace(",", "."),
        "Rata-rata nilai order": rupiah(df["omzet"].mean()),
    }
    bulanan = df.groupby("bulan")["omzet"].sum()
    per_kat = df.groupby("kategori")["omzet"].sum().sort_values()
    per_kota = df.groupby("kota")["omzet"].sum().sort_values()

    plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(bulanan.index, bulanan.values / 1e6, marker="o", color="#2563eb")
    ax.set_title("Omzet bulanan 2025")
    ax.set_ylabel("Juta Rupiah")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT / "omzet_bulanan.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].barh(per_kat.index, per_kat.values / 1e6, color="#2563eb")
    axes[0].set_title("Omzet per kategori (juta Rp)")
    axes[1].barh(per_kota.index, per_kota.values / 1e6, color="#0d9488")
    axes[1].set_title("Omzet per kota (juta Rp)")
    fig.tight_layout()
    fig.savefig(OUT / "omzet_kategori_kota.png", dpi=150)
    plt.close(fig)

    top_kat = per_kat.index[-1]
    top_kota = per_kota.index[-1]
    puncak = bulanan.idxmax().strftime("%B %Y")
    lines = ["# Ringkasan Temuan", ""]
    lines += [f"- **{k}:** {v}" for k, v in kpi.items()]
    lines += [
        f"- **Kategori terbesar:** {top_kat} ({per_kat.iloc[-1] / total:.0%} dari omzet)",
        f"- **Kota terbesar:** {top_kota} ({per_kota.iloc[-1] / total:.0%} dari omzet)",
        f"- **Bulan omzet tertinggi:** {puncak}",
        f"- **Data dibersihkan:** {len(raw) - len(df)} baris duplikat dihapus, "
        f"{int((df['kota'] == 'Tidak Diketahui').sum())} nilai kota kosong diberi label 'Tidak Diketahui'",
    ]
    (OUT / "ringkasan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
