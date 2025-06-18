# Laporan Analisis Data E-Commerce Olist

## 1. Business Understanding

### 1.1 Latar Belakang
Proyek ini menganalisis dataset publik E-Commerce dari Olist untuk menjawab pertanyaan bisnis terkait performa penjualan.

### 1.2 Pertanyaan Bisnis
1. Bagaimana tren pendapatan harian & bulanan di Olist?
2. Produk apa saja yang memperoleh pendapatan besar di Olist?
3. Kota mana yang mengumpulkan pesanan terbanyak?
4. Metode pembayaran apa yang paling banyak digunakan di Olist?
5. Bagaimana segmentasi pelanggan berdasarkan tingkat recency, frequency, dan monetary mereka?

## 2. Data Understanding

Dataset E-Commerce Public dari Olist terdiri dari 9 tabel yang saling terkait. Berikut penjelasan detail setiap tabel beserta kolom-kolomnya:

### 1. Customers Dataset (`customers.csv`)
Dataset ini berisi informasi tentang pelanggan yang melakukan pembelian di Olist. Terdapat 99.441 record tanpa missing value atau duplikat.

**Kolom-kolom:**
- `customer_id`: ID unik untuk setiap pesanan (bukan ID pelanggan)
  - Tipe Data: String
  - Contoh Nilai: "06b8999e2fba1a1fbc88172c00ba8bc7"
- `customer_unique_id`: ID unik yang mengidentifikasi setiap pelanggan
  - Tipe Data: String
  - Contoh Nilai: "861eff4711a542e4b93843c6dd7febb0"
- `customer_zip_code_prefix`: Kode pos awal pelanggan
  - Tipe Data: Integer
  - Contoh Nilai: 14409
- `customer_city`: Kota tempat tinggal pelanggan
  - Tipe Data: String
  - Contoh Nilai: "franca"
- `customer_state`: Negara bagian tempat tinggal pelanggan
  - Tipe Data: String (2 karakter)
  - Contoh Nilai: "SP" (São Paulo)

### 2. Geolocation Dataset (`geolocation.csv`)
Dataset ini berisi data geografis berdasarkan kode pos. Terdapat 1.000.163 record dengan 261.831 duplikat.

**Kolom-kolom:**
- `geolocation_zip_code_prefix`: Kode pos awal
  - Tipe Data: Integer
  - Contoh Nilai: 1037
- `geolocation_lat`: Latitude koordinat geografis
  - Tipe Data: Float
  - Contoh Nilai: -23.545621
- `geolocation_lng`: Longitude koordinat geografis
  - Tipe Data: Float
  - Contoh Nilai: -46.639292
- `geolocation_city`: Nama kota
  - Tipe Data: String
  - Contoh Nilai: "sao paulo"
- `geolocation_state`: Negara bagian
  - Tipe Data: String (2 karakter)
  - Contoh Nilai: "SP"

### 3. Order Items Dataset (`order_items.csv`)
Dataset ini berisi item-item yang dipesan dalam setiap transaksi. Terdapat 112.650 record tanpa missing value atau duplikat.

**Kolom-kolom:**
- `order_id`: ID unik untuk setiap pesanan
  - Tipe Data: String
  - Contoh Nilai: "00010242fe8c5a6d1ba2dd792cb16214"
- `order_item_id`: Nomor urut item dalam pesanan
  - Tipe Data: Integer
  - Contoh Nilai: 1
- `product_id`: ID produk yang dipesan
  - Tipe Data: String
  - Contoh Nilai: "4244733e06e7ecb4970a6e2683c13e61"
- `seller_id`: ID penjual produk
  - Tipe Data: String
  - Contoh Nilai: "48436dade18ac8b2bce089ec2a041202"
- `shipping_limit_date`: Batas waktu pengiriman
  - Tipe Data: String (format datetime)
  - Contoh Nilai: "2017-09-19 09:45:35"
- `price`: Harga produk
  - Tipe Data: Float
  - Contoh Nilai: 58.90
- `freight_value`: Biaya pengiriman
  - Tipe Data: Float
  - Contoh Nilai: 13.29

### 4. Order Payments Dataset (`order_payments.csv`)
Dataset ini berisi informasi pembayaran untuk setiap pesanan. Terdapat 103.886 record tanpa missing value atau duplikat.

**Kolom-kolom:**
- `order_id`: ID pesanan
  - Tipe Data: String
  - Contoh Nilai: "b81ef226f3fe1789b1e8b2acac839d17"
- `payment_sequential`: Urutan pembayaran jika ada multiple payments
  - Tipe Data: Integer
  - Contoh Nilai: 1
- `payment_type`: Metode pembayaran
  - Tipe Data: String
  - Contoh Nilai: "credit_card", "boleto", "voucher", "debit_card", "not_defined"
- `payment_installments`: Jumlah cicilan
  - Tipe Data: Integer
  - Contoh Nilai: 8
- `payment_value`: Nilai pembayaran
  - Tipe Data: Float
  - Contoh Nilai: 99.33

### 5. Order Reviews Dataset (`order_reviews.csv`)
Dataset ini berisi ulasan pelanggan untuk pesanan. Terdapat 99.224 record dengan banyak missing values pada kolom komentar.

**Kolom-kolom:**
- `review_id`: ID unik ulasan
  - Tipe Data: String
  - Contoh Nilai: "7bc2406110b926393aa56f80a40eba40"
- `order_id`: ID pesanan yang diulas
  - Tipe Data: String
  - Contoh Nilai: "73fc7af87114b39712e6da79b0a377eb"
- `review_score`: Skor ulasan (1-5)
  - Tipe Data: Integer
  - Contoh Nilai: 4
- `review_comment_title`: Judul ulasan
  - Tipe Data: String
  - Missing Values: 87.656 (88.3%)
  - Contoh Nilai: "Recomendo"
- `review_comment_message`: Isi ulasan
  - Tipe Data: String
  - Missing Values: 58.247 (58.7%)
  - Contoh Nilai: "Muito bom"
- `review_creation_date`: Tanggal pembuatan ulasan
  - Tipe Data: String (format datetime)
  - Contoh Nilai: "2018-01-18 00:00:00"
- `review_answer_timestamp`: Tanggal jawaban ulasan
  - Tipe Data: String (format datetime)
  - Contoh Nilai: "2018-01-18 21:46:59"

### 6. Orders Dataset (`orders.csv`)
Dataset ini berisi informasi utama tentang pesanan. Terdapat 99.441 record dengan beberapa missing values pada kolom-kolom time series terkait proses pengiriman.

**Kolom-kolom:**
- `order_id`: ID unik pesanan
  - Tipe Data: String
  - Contoh Nilai: "e481f51cbdc54678b7cc49136f2d6af7"
- `customer_id`: ID pelanggan
  - Tipe Data: String
  - Contoh Nilai: "9ef432eb6251297304e76186b10a928d"
- `order_status`: Status pesanan
  - Tipe Data: String
  - Contoh Nilai: "delivered", "shipped", "canceled", dll.
- `order_purchase_timestamp`: Waktu pembelian
  - Tipe Data: String (format datetime)
  - Contoh Nilai: "2017-10-02 10:56:33"
- `order_approved_at`: Waktu persetujuan pesanan
  - Tipe Data: String (format datetime)
  - Missing Values: 160 (0.16%)
  - Contoh Nilai: "2017-10-02 11:07:15"
- `order_delivered_carrier_date`: Waktu penyerahan ke kurir
  - Tipe Data: String (format datetime)
  - Missing Values: 1.783 (1.8%)
  - Contoh Nilai: "2017-10-04 19:55:00"
- `order_delivered_customer_date`: Waktu diterima pelanggan
  - Tipe Data: String (format datetime)
  - Missing Values: 2.965 (3.0%)
  - Contoh Nilai: "2017-10-10 21:25:13"
- `order_estimated_delivery_date`: Perkiraan waktu pengiriman
  - Tipe Data: String (format datetime)
  - Contoh Nilai: "2017-10-18 00:00:00"

### 7. Product Category Translation (`product_category_name_translation.csv`)
Dataset ini berisi terjemahan nama kategori produk dari Portugis ke Inggris. Terdapat 71 record tanpa missing value atau duplikat.

**Kolom-kolom:**
- `product_category_name`: Nama kategori dalam Bahasa Portugis
  - Tipe Data: String
  - Contoh Nilai: "beleza_saude"
- `product_category_name_english`: Nama kategori dalam Bahasa Inggris
  - Tipe Data: String
  - Contoh Nilai: "health_beauty"

### 8. Products Dataset (`products.csv`)
Dataset ini berisi informasi tentang produk yang dijual. Terdapat 32.951 record dengan beberapa missing values pada kolom-kolomnya, kecuali kolom kecuali product_id.

**Kolom-kolom:**
- `product_id`: ID unik produk
  - Tipe Data: String
  - Contoh Nilai: "1e9e8ef04dbcff4541ed26657ea517e5"
- `product_category_name`: Nama kategori produk
  - Tipe Data: String
  - Missing Values: 610 (1.85%)
  - Contoh Nilai: "perfumaria"
- `product_name_lenght`: Panjang karakter nama produk
  - Tipe Data: Float
  - Missing Values: 610 (1.85%)
  - Contoh Nilai: 40.0
- `product_description_lenght`: Panjang karakter deskripsi produk
  - Tipe Data: Float
  - Missing Values: 610 (1.85%)
  - Contoh Nilai: 287.0
- `product_photos_qty`: Jumlah foto produk
  - Tipe Data: Float
  - Missing Values: 610 (1.85%)
  - Contoh Nilai: 1.0
- `product_weight_g`: Berat produk dalam gram
  - Tipe Data: Float
  - Missing Values: 2 (0.006%)
  - Contoh Nilai: 225.0
- `product_length_cm`: Panjang produk dalam cm
  - Tipe Data: Float
  - Missing Values: 2 (0.006%)
  - Contoh Nilai: 16.0
- `product_height_cm`: Tinggi produk dalam cm
  - Tipe Data: Float
  - Missing Values: 2 (0.006%)
  - Contoh Nilai: 10.0
- `product_width_cm`: Lebar produk dalam cm
  - Tipe Data: Float
  - Missing Values: 2 (0.006%)
  - Contoh Nilai: 14.0

### 9. Sellers Dataset (`sellers.csv`)
Dataset ini berisi informasi tentang penjual di platform Olist. Terdapat 3.095 record tanpa missing value atau duplikat.

**Kolom-kolom:**
- `seller_id`: ID unik penjual
  - Tipe Data: String
  - Contoh Nilai: "3442f8959a84dea7ee197c632cb2df15"
- `seller_zip_code_prefix`: Kode pos awal penjual
  - Tipe Data: Integer
  - Contoh Nilai: 13023
- `seller_city`: Kota penjual
  - Tipe Data: String
  - Contoh Nilai: "campinas"
- `seller_state`: Negara bagian penjual
  - Tipe Data: String (2 karakter)
  - Contoh Nilai: "SP"


## 3. Data Preparation

### 3.1 Data Cleaning
- **Geolocation**: Menghapus 261.831 data duplikat
- **Order Reviews**: 
  - `review_comment_title`, 87656 null values, diisi dengan "tanpa title"  
  - `review_comment_message`, 58247 null values, diisi dengan "tanpa message"
- **Orders**: 
  - Mengisi nilai null dengan waktu rata-rata antar proses
  - `order_approved_at`, 160 null values, diisi dengan rata-rata rentang waktu dengan proses sebelumnya.   
  - `order_delivered_carrier_date`, 1783 null values, diisi dengan rata-rata rentang waktu dengan proses sebelumnya.   
  - `order_delivered_customer_date`, 2965 null values, diisi dengan rata-rata rentang waktu dengan proses sebelumnya.   
- **Products**: 
  - Kolom string diisi dengan "unknown"
  - Kolom numerik diisi dengan 0

### 3.2 Feature Engineering     
Berikut adalah penjelasan terkait Feature Engineering yang dilakukan pada tahap-tertentu dalam proses analisis ini:

#### a. **Exploratory Data Analysis (EDA) - Pertanyaan 1: Tren Pendapatan Bulanan**
   - **Feature Engineering**:
     - `order_date`: Ekstraksi tanggal dari `order_purchase_timestamp`
     - `revenue`: Penjumlahan `price` dan `freight_value` untuk menghitung pendapatan per order
     - `month_year`: Ekstraksi bulan dan tahun dari timestamp untuk analisis bulanan
   - **Tujuan**: Membuat metrik pendapatan dan dimensi waktu yang lebih berguna untuk analisis tren

#### b. **EDA - Pertanyaan 2: Produk dengan Pendapatan Besar**
   - **Feature Engineering**:
     - Penggabungan nama kategori produk dalam bahasa Inggris (translation)
     - Agregasi pendapatan per kategori produk
   - **Tujuan**: Memungkinkan analisis pendapatan berdasarkan kategori produk yang lebih mudah dipahami

#### c. **EDA - Pertanyaan 3: Daerah dengan Pesanan Terbanyak**
   - **Feature Engineering**:
     - `order_count`: Hitungan unik pesanan per kota
   - **Tujuan**: Mengubah data mentah menjadi metrik yang dapat diukur untuk analisis geografis

#### d. **Visualization & Explanatory Analysis - Pertanyaan 1**
   - **Feature Engineering**:
     - `order_month`: Konversi tanggal ke format bulan-tahun untuk visualisasi
     - Pembuatan bins untuk recency groups (0-90 days, 91-180 days, etc.)
   - **Tujuan**: Membuat dimensi waktu yang lebih sesuai untuk visualisasi dan segmentasi

#### e. **Analisis RFM (Recency, Frequency, Monetary)**
   - **Feature Engineering**:
     - `recency`: Menghitung hari sejak transaksi terakhir
     - `frequency`: Hitungan unik pesanan per customer
     - `monetary`: Total nilai pembayaran per customer
     - Normalisasi ranking (r_rank_norm, f_rank_norm, m_rank_norm)
     - `RFM_score`: Skor gabungan dengan bobot tertentu (0.15(r_rank_norm) + 0.28(f_rank_norm) + 0.57(m_rank_norm))
     - `customer_segment`: Kategorisasi customer berdasarkan RFM score
   - **Tujuan**: 
     - Membuat metrik komprehensif untuk mengukur seberapa bernilai customer tertentu

#### f. **Segmentasi Pelanggan**
   - **Feature Engineering**:
     - Kategorisasi customer menjadi:
       - Top customers `RFM_score' > 4.5`
       - High value customer `RFM_score' > 4`
       - Medium value customer `RFM_score' > 3`
       - Low value customers `RFM_score' > 1.6`
       - Lost customers `else`

   - **Tujuan**: Menyederhanakan analisis dengan mengelompokkan customer berdasarkan nilai bisnisnya.

## 4. Evaluation

### 4.1 Jawaban Pertanyaan Bisnis

#### Pertanyaan 1: Tren Pendapatan
- **Harian Tertinggi**: 24 Nov 2017 (R$175k, 1147 orders)
- **Bulanan Tertinggi**: Nov 2017 (R$1.15M, 7289 orders)
- Tren pendapatan bulanan selama tahun 2017 November menunjukkan pola peningkatan pendapatan setiap bulannya.
- Tren pendapatan bulanan selama tahun 2018 tidak menunjukkan peningkatan pendapatan bulanan yang kontinu setiap bulannya. Pola pendapatan bulanan di bulan Maret hingga Mei cukup stabil, sedangkan di bulan-bulan lainnya fluktuatif.

#### Pertanyaan 2: Produk Berpendapatan Tinggi
- **Top 3 Kategori**:
  1. Health & Beauty (sekitar R$1.26M)
  2. Watches & Gifts (sekitar R$1.2M)
  3. Bed & Bath Table (sekitar R$1.0M)

#### Pertanyaan 3: Kota dengan Pesanan Terbanyak
- **Sao Paulo**: 15,540 orders
- **Rio de Janeiro**: 6,882 orders
- **Belo Horizonte**: 2,747 orders

#### Pertanyaan 4: Metode Pembayaran
- **Credit Card**: 73% transaksi
- **Boleto**: 19%
- **Voucher**: 5.5%

#### Pertanyaan 5: Segmentasi Pelanggan (RFM)
1. **Top Customers**: 4.5%
2. **High Value Customers**: 12.3%
3. **Medium Value Customers**: 32.1%
4. **Low Value Customers**: 45.7%
5. **Lost Customers**: 5.4%

## 5. Langkah Analisis Selanjutnya
1. Analisis lebih dalam faktor penyebab lonjakan penjualan
2. Eksperimen promosi untuk produk kategori rendah
3. Pengembangan program loyalitas berdasarkan segmentasi RFM



## 6. Dashboard Interaktif
Dashboard hasil analisis ini di deploy menggunakan aplikasi streamlit. Berikut adalah langkah-langkah menjalankan aplikasi streamlit di komputer lokal:

### Setup Environment - Shell
mkdir analisis_data (membuat direktori analisis_data untuk menyimpan data_dashboard, dashboard.py, dan requirements.txt)

conda create --name analisis-data-env python  (membuat environment untuk menjalankan aplikasi streamlit di dalam komputer lokal)

### Membuat requirements.txt
cd analisis_data (berpindah ke direktori analisis_data)    
pip freeze > requirements.txt (membuat file requirements.txt)    

### Install semua dipendensi di analisis-data-env
conda activate analisis-data-env (aktivasi environment untuk install semua dependensi)    
pip install -r requirements.txt

### Run streamlit app
streamlit run dashboard.py

## 7. Dashboard Interaktif Online
Setelah pengecekan aplikasi di komputer lokal dan semuanya OK, aplikasi bisa dideploy ke streamlit cloud via github. Berikut langkah-langkah untuk push aplikasi dari komputer lokal ke github dan dilanjutkan deployment ke streamlit cloud:      

### **1. Login akun GitHub**
Buka Git Bash dari direktori analisis-data. Kemudian jalankan command di bawah ini:     
```sh
git config --global user.name "Nama"
git config --global user.email "email@example.com"
```
Gunakan nama dan email yang terhubung ke akun GitHub.

### **2. Buat dan Konfigurasi SSH Key**     
Jika belum adaSSH key, buat kunci SSH baru:
```sh
ssh-keygen -t ed25519 -C "email@example.com"
```
Tekan `Enter` tiga kali untuk menggunakan pengaturan default. Ini akan membuat file **id_ed25519** dan **id_ed25519.pub** di `~/.ssh/`.

Tambahkan kunci SSH ke agent:
```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### **3. Tambahkan Kunci ke GitHub**
Salin kunci publik:
```sh
cat ~/.ssh/id_ed25519.pub
```
Buka GitHub → **Settings** → **SSH and GPG Keys** → **New SSH Key** → tempelkan kunci.

Cek koneksi:
```sh
ssh -T git@github.com
```
Jika berhasil, akan muncul pesan:  
`Hi username! You've successfully authenticated, but GitHub does not provide shell access.`

### **4. Buat Repository Baru di GitHub via situs web GitHub**

1. Buka [GitHub](https://github.com/) dan login dengan akun GitHub.
2. Klik ikon **"+"** di pojok kanan atas, lalu pilih **"New repository"**.
3. Masukkan nama repositori **analisis_data**, pilih visibilitas **Public**.
4. Jika diperlukan, tambahkan **.gitignore** dan **lisensi** sesuai proyek.
5. Klik **"Create repository"**, lalu tunggu hingga repositori berhasil dibuat.

### **5. Inisialisasi Repository dan Hubungkan ke GitHub**
```sh
git init
```
Tambahkan repository sebagai remote:
```sh
git remote add origin git@github.com:username/analisis_data.git
```

### **6. Tambahkan, Commit, dan Push File**
Tambahkan semua file:
```sh
git add .
git commit -m "Inisialisasi repository, load semua file"
```
Ganti ke branch utama:
```sh
git branch -M main
```
Push ke repository GitHub menggunakan SSH:
```sh
git push -u origin main
```

### **7. Deploy ke Streamlit Cloud**
1. Buka [Streamlit Cloud](https://share.streamlit.io/).
2. Login dengan akun GitHub dan pilih **create app**.
3. Klik **"Deploy now"** pada bagian  **Deploy a public app from GitHub**.
4. Masukkan nama repositori **analisis_data**, branch **main**, main file path **dashboard.py**, dan nama urlfile utama **coding-camp-2025-submission**.     
5. Lanjutkan ke **Advanced Settings** jika diperlukan.
5. Klik **"Deploy"**, tunggu hingga aplikasi berhasil dibangun.


### **8. Bagikan Link Aplikasi**
Setelah sukses, Streamlit akan memberikan URL aplikasi yang bisa langsung diakses dan dibagikan. https://coding-camp-2025-submission.streamlit.app/



