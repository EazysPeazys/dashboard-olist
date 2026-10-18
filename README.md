# Dashboard Pelanggan E-Commerce Olist (Brasil) 🛒

- Nama: Nabil Daffa Athalasyah
- Email: athalasyahnabil@gmail.com
- ID Dicoding: nabdaff95

Proyek akhir kelas **Belajar Fundamental Analisis Data** (Dicoding - Asah led by Dicoding 2026).

Analisis menggunakan **E-Commerce Public Dataset (Brazilian E-Commerce by Olist)**, file `olist_customers_dataset.csv`, untuk menjawab tiga pertanyaan bisnis periode 2016-2018:

1. 5 state mana dengan pelanggan unik terbanyak dan berapa kontribusinya?
2. 10 kota mana dengan pelanggan unik terbanyak, berapa jumlah pelanggan unik tiap kota, dan berapa kontribusinya?
3. Berapa repeat rate tiap region dan region mana yang terendah?

Analisis lanjutan: geospatial analysis (bubble map per state) dan clustering tanpa machine learning (manual grouping region + binning segmen pelanggan).

## Struktur Proyek

```
submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   └── olist_customers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment

### Menggunakan Anaconda / venv
```
conda create --name olist-dashboard python=3.10
conda activate olist-dashboard
pip install -r requirements.txt
```

Atau dengan virtual environment biasa:
```
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Menjalankan Dashboard

Dari folder utama `submission`:
```
cd dashboard
streamlit run dashboard.py
```
Dashboard akan terbuka di browser pada `http://localhost:8501`.

## Menjalankan Notebook

Buka `notebook.ipynb` dari folder utama `submission` (agar path `data/` dan `dashboard/` terbaca), lalu pilih **Run All**. Jika memakai Google Colab, unggah folder `data` ke Colab dan buat folder `dashboard` terlebih dahulu.

## Dashboard Online

Tautan dashboard (Streamlit Community Cloud) tersedia pada berkas `url.txt`.
