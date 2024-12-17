import pandas as pd
import streamlit as st
import plotly.express as px
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

# Dashboard Header
st.title("E-Commerce Business Dashboard \U0001F4C8")

# Display Metrik Utama
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pendapatan", format_number_with_currency(total_revenue, 'BRL'))
col2.metric("Jumlah Pesanan", total_orders)
col3.metric("Jumlah Pelanggan", total_customers)
col4.metric("Average Order Value (AOV)", format_number_with_currency(aov, 'BRL'))

# Grafik Interaktif
st.subheader("1. Tren Pendapatan Harian")
fig_daily_revenue = px.line(
    daily_revenue_df, 
    x='order_purchase_timestamp', 
    y='price',
    title= f"1. Tren Pendapatan Harian ({start_date} hingga {end_date})",
    labels={'order_purchase_timestamp': 'Tanggal', 'price': 'Pendapatan (R$)'}
)
st.plotly_chart(fig_daily_revenue)

st.subheader("2. Produk dengan Pendapatan Terbesar")
fig_top_products = px.bar(
    top_products_df, 
    x='price', 
    y='product_category_name_english', 
    orientation='h',
    title='Top 10 Produk dengan Pendapatan Terbesar',
    labels={'price': 'Pendapatan (R$)', 'product_category_name_english': 'Kategori Produk'}
)
st.plotly_chart(fig_top_products)

st.subheader("3. Kota dengan Jumlah Pesanan Terbanyak")
fig_top_regions = px.bar(
    top_regions_df, 
    y='city', 
    x='order_count', 
    orientation='h',
    title='Top 10 Kota dengan Jumlah Pesanan Terbanyak',
    labels={'city': 'Kota', 'order_count': 'Jumlah Pesanan'}
)
st.plotly_chart(fig_top_regions)

st.subheader("4. Metode Pembayaran Paling Populer")
fig_payment_methods = px.pie(
    top_payment_df, 
    names='payment_type',
    values='count',
    title='Distribusi Metode Pembayaran'
)
st.plotly_chart(fig_payment_methods)

# Footer
st.caption("Copyright © 2024 E-Commerce Dashboard")
