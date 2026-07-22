# Dashboard TPT Provinsi Banten

Aplikasi Streamlit untuk menampilkan visualisasi dan data Tingkat Pengangguran Terbuka (TPT)
Provinsi Banten periode 2017–2024.

## Halaman
- Beranda
- Dashboard TPT
- Tentang Data

## Menjalankan aplikasi

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Menambahkan dashboard Power BI

Buka file `app.py`, lalu ubah:

```python
POWER_BI_EMBED_URL = ""
```

menjadi tautan Publish to web dari Power BI:

```python
POWER_BI_EMBED_URL = "https://app.powerbi.com/view?r=..."
```

Atau simpan sebagai environment variable bernama `POWER_BI_EMBED_URL`.

## Dataset
- Periode: 2017–2024
- Wilayah: 8 kabupaten/kota
- Agregat tambahan: Provinsi Banten
- Sumber: BPS Provinsi Banten
