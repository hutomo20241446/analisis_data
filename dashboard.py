import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from babel.numbers import format_currency

# Fungsi Load Data
def load_data():
    # Membaca file CSV
    orders = pd.read_csv("data_dashboard/orders.csv", parse_dates=["order_purchase_timestamp"])
    order_items = pd.read_csv("data_dashboard/order_items.csv")
    order_payments = pd.read_csv("data_dashboard/order_payments.csv")
    customers = pd.read_csv("data_dashboard/customers.csv")
    products = pd.read_csv("data_dashboard/products.csv")
    product_category = pd.read_csv("data_dashboard/product_category.csv")

    # Gabungkan data berdasarkan relasi antar tabel
    merged_df = orders.merge(order_items, on="order_id") \
                      .merge(order_payments, on="order_id") \
                      .merge(customers, on="customer_id") \
                      .merge(products, on="product_id") \
                      .merge(product_category, on="product_category_name")
    return merged_df

# Fungsi Analisis Data
def calculate_metrics(df):
    total_revenue = df['price'].sum()
    total_orders = df['order_id'].nunique()
    total_customers = df['customer_id'].nunique()
    aov = total_revenue / total_orders if total_orders > 0 else 0
    return total_revenue, total_orders, total_customers, aov

def top_payment_methods(df, threshold=0.05):
    payment_counts = df["payment_type"].value_counts().reset_index()
    payment_counts.columns = ["payment_type", "count"]
    payment_counts["percentage"] = payment_counts["count"] / payment_counts["count"].sum()
    payment_counts.loc[payment_counts["percentage"] < threshold, "payment_type"] = "Other"
    payment_counts_aggregated = payment_counts.groupby("payment_type")["count"].sum().reset_index()
    return payment_counts_aggregated.sort_values(by="count", ascending=False)

def top_regions(df):
    top_regions = df.groupby("customer_city")["order_id"].nunique().reset_index().rename(
        columns={"customer_city": "city", "order_id": "order_count"})
    top_regions = top_regions.sort_values(by="order_count", ascending=False).head(10)
    # top_regions = top_regions.iloc[::-1].reset_index(drop=True)
    return top_regions.iloc[::-1].reset_index(drop=True)

def daily_revenue(df):
    return df.resample('D', on='order_purchase_timestamp').agg({'price': 'sum'}).reset_index()

def top_products(df):
    top_products = df.groupby("product_category_name_english")["price"].sum().reset_index()
    return top_products.sort_values(by="price").head(10)

# **Fungsi untuk Segmentasi Pelanggan**
# **Fungsi untuk Segmentasi Pelanggan**
def segment_customers():
    # Membaca file CSV
    orders = pd.read_csv("data_dashboard/orders.csv", parse_dates=["order_purchase_timestamp"])
    order_payments = pd.read_csv("data_dashboard/order_payments.csv")
    customers = pd.read_csv("data_dashboard/customers.csv")
    # Pilih hanya pesanan yang sudah terkirim
    orders_df = orders[orders["order_status"] == "delivered"].copy()

    # Pilih kolom yang relevan
    orders_df = orders_df[['order_id', 'customer_id', 'order_purchase_timestamp']]
    order_payments_df = order_payments[['order_id', 'payment_value']].copy()

    # Merge orders dengan order_payments
    all_df = orders_df.merge(order_payments_df, on="order_id", how="left")
    all_df = all_df.merge(customers[['customer_id', 'customer_unique_id']], on="customer_id", how="left")
    
    # Agregasi untuk RFM Analysis
    rfm_df = all_df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",  # Tanggal order terakhir
        "order_id": "nunique",  # Frekuensi transaksi
        "payment_value": "sum"  # Total pengeluaran
    })
    
    # Ubah nama kolom
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    # Menghitung recency (hari sejak transaksi terakhir)
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = all_df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    # Hapus kolom max_order_timestamp
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    # Normalisasi ranking RFM
    rfm_df['r_rank'] = rfm_df['recency'].rank(ascending=False)
    rfm_df['f_rank'] = rfm_df['frequency'].rank(ascending=True)
    rfm_df['m_rank'] = rfm_df['monetary'].rank(ascending=True)

    rfm_df['r_rank_norm'] = (rfm_df['r_rank']/rfm_df['r_rank'].max())*100
    rfm_df['f_rank_norm'] = (rfm_df['f_rank']/rfm_df['f_rank'].max())*100
    rfm_df['m_rank_norm'] = (rfm_df['m_rank']/rfm_df['m_rank'].max())*100

    rfm_df.drop(columns=['r_rank', 'f_rank', 'm_rank'], inplace=True)

    # Menghitung skor RFM
    rfm_df['RFM_score'] = 0.15*rfm_df['r_rank_norm'] + 0.28*rfm_df['f_rank_norm'] + 0.57*rfm_df['m_rank_norm']
    rfm_df['RFM_score'] *= 0.05
    rfm_df = rfm_df.round(2)

    # Segmentasi pelanggan berdasarkan RFM Score
    rfm_df["customer_segment"] = np.where(
        rfm_df['RFM_score'] > 4.5, "Top customers",
        np.where(rfm_df['RFM_score'] > 4, "High value customer",
        np.where(rfm_df['RFM_score'] > 3, "Medium value customer",
        np.where(rfm_df['RFM_score'] > 1.6, "Low value customers", "Lost customers"))))

    # Hitung jumlah pelanggan per segmen
    customer_segment_df = rfm_df.groupby(by="customer_segment", as_index=False).customer_id.nunique()
    customer_segment_df['customer_segment'] = pd.Categorical(customer_segment_df['customer_segment'], [
        "Lost customers", "Low value customers", "Medium value customer",
        "High value customer", "Top customers"
    ])
    
    return customer_segment_df.sort_values(by="customer_segment", ascending=False)


# Fungsi untuk memformat angka dengan simbol mata uang
def format_number_with_currency(value, currency_code='BRL', locale='pt_BR'):
    if value >= 1_000_000:
        formatted_value = value / 1_000_000
        return f"{format_currency(formatted_value, currency_code, locale=locale)}M"
    elif value >= 1_000:
        formatted_value = value / 1_000
        return f"{format_currency(formatted_value, currency_code, locale=locale)}k"
    else:
        return format_currency(value, currency_code, locale=locale)

# Load Data
df = load_data()

# Sidebar - Filter Rentang Waktu
st.sidebar.header("Filter Rentang Waktu")
min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Filter DataFrame berdasarkan rentang waktu
filtered_df = df[  
    (df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

# Kalkulasi Metrik Utama
total_revenue, total_orders, total_customers, aov = calculate_metrics(filtered_df)
daily_revenue_df = daily_revenue(filtered_df)
top_payment_df = top_payment_methods(filtered_df)
top_regions_df = top_regions(filtered_df)
top_products_df = top_products(filtered_df)
segment_customers_df = segment_customers()

# Display Metrik Utama
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pendapatan", format_number_with_currency(total_revenue, 'BRL'))
col2.metric("Jumlah Pesanan", total_orders)
col3.metric("Jumlah Pelanggan", total_customers)
col4.metric("Average Order Value (AOV)", format_number_with_currency(aov, 'BRL'))

# **Tren Pendapatan Harian**
st.subheader("1. Tren Pendapatan Harian")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=daily_revenue_df, x="order_purchase_timestamp", y="price", ax=ax)
ax.set_title(f"Tren Pendapatan Harian ({start_date} hingga {end_date})")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Pendapatan (R$)")
plt.xticks(rotation=45)
st.pyplot(fig)

# **Produk dengan Pendapatan Terbesar**
st.subheader("2. Produk dengan Pendapatan Terbesar")
top_products_df = top_products_df.sort_values(by="price", ascending=False)  # Urutkan dari terbesar ke terkecil
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_products_df, x="price", y="product_category_name_english", ax=ax, palette="Blues_r")
ax.set_title("Top 10 Produk dengan Pendapatan Terbesar")
ax.set_xlabel("Pendapatan (R$)")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

# **Kota dengan Jumlah Pesanan Terbanyak**
st.subheader("3. Kota dengan Jumlah Pesanan Terbanyak")
top_regions_df = top_regions_df.sort_values(by="order_count", ascending=False)  # Urutkan dari terbesar ke terkecil
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_regions_df, x="order_count", y="city", ax=ax, palette="Blues_r")
ax.set_title("Top 10 Kota dengan Jumlah Pesanan Terbanyak")
ax.set_xlabel("Jumlah Pesanan")
ax.set_ylabel("Kota")
st.pyplot(fig)

# **Metode Pembayaran Paling Populer**
st.subheader("4. Metode Pembayaran Paling Populer")
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(top_payment_df["count"], labels=top_payment_df["payment_type"], autopct='%1.1f%%', colors=sns.color_palette("pastel"))
ax.set_title("Distribusi Metode Pembayaran")
st.pyplot(fig)

# **Visualisasi Segmentasi Pelanggan**
st.subheader("5. Segmentasi Pelanggan berdasarkan RFM score")
segment_customers_df = segment_customers_df.sort_values(by="customer_id", ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="customer_id", y="customer_segment", data=segment_customers_df,  ax=ax)
ax.set_title("Jumlah Pelanggan per Segmen")
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Segmentasi Pelanggan")
st.pyplot(fig)


# Footer
st.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: gray;">
        Copyright © 2025 Coding Camp | Powered by DBS Foundation
    </div>
    """,
    unsafe_allow_html=True
)
