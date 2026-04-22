# Responsi UTS - Infrastruktur dan Platform Big Data (IPBD)
**Studi Kasus: Automated Data Pipeline for Wired.com Articles**

## 📝 Deskripsi Tugas
Proyek ini membangun sebuah *Automated Data Pipeline* (ETL) yang mengambil data artikel berita dari Wired.com. Sistem ini mengintegrasikan teknik *web scraping*, penyajian data melalui API, orkestrasi alur kerja menggunakan Airflow, dan penyimpanan data ke dalam database PostgreSQL untuk analisis lanjut.

## 🏗️ Arsitektur Pipeline
1.  **Extract (Web Scraper):** Menggunakan **Selenium** untuk mengambil minimal 50 artikel dari kategori *Science* dan *Security* di Wired.com.
2.  **Storage (JSON/CSV):** Hasil *scraping* disimpan dalam format mentah `.json` dan `.csv` di folder `data/`.
3.  **API Service:** Menggunakan **FastAPI** untuk menyajikan data mentah tersebut melalui endpoint `GET /articles`.
4.  **Orchestration (Airflow DAG):**
    * Mengambil data dari API.
    * **Transformasi:** Membersihkan dan memastikan format tanggal (`scraped_at`) menjadi objek *datetime* yang valid.
6.  **Load (Database):** Menyimpan data hasil transformasi ke tabel `wired_articles` di **PostgreSQL**.

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python
* **Library Scraping:** Selenium, Webdriver Manager
* **Framework API:** FastAPI, Uvicorn
* **Workflow Orchestration:** Apache Airflow
* **Database:** PostgreSQL
* **Containerization:** Docker & Docker Compose

## 📁 Struktur Folder
```text
responsi-uts-ipbd/
├── dags/
│   └── wired_dag.py        # Logika orkestrasi Airflow
├── data/
│   ├── articles.json       # Output mentah scraper
│   └── articles.csv        # Output mentah scraper
├── src/
│   ├── api.py              # Service FastAPI
│   └── scraper.py          # Script Selenium Scraper
├── assets/                 # Dokumentasi screenshot
├── docker-compose.yml      # Konfigurasi Docker (Airflow & Postgres)
└── README.md
