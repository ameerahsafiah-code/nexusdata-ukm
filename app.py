import streamlit as st
import pandas as pd
import os
import subprocess

# Set tema dashboard
st.set_page_config(page_title="NexusData Dashboard", layout="wide")

st.title("📊 NexusData: Sistem Pengumpulan Data Automatik")
st.markdown("Projek Penyelidikan Data - Universiti Kebangsaan Malaysia")

# Tambah Metrik di bahagian atas
if os.path.exists('data_buku_besar.csv'):
    df = pd.read_csv('data_buku_besar.csv')
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Jumlah Buku", len(df))
    col_m2.metric("Harga Purata", f"£{df['Harga (GBP)'].mean():.2f}")
    col_m3.metric("Harga Tertinggi", f"£{df['Harga (GBP)'].max()}")

    # Tambah butang muat turun di sidebar
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Muat Turun Data (CSV)",
        data=csv,
        file_name='hasil_nexusdata.csv',
        mime='text/csv',
    )
# Bahagian tepi (Sidebar)
st.sidebar.header("Pusat Kawalan")
if st.sidebar.button("🚀 Jalankan Bot Sekarang"):
    with st.spinner("Bot sedang mengumpul data... Sila tunggu."):
        # Menjalankan main.py secara automatik
        subprocess.run(["python", "main.py"])
    st.sidebar.success("Selesai! Data terbaru telah dikemas kini.")

# Susun atur Dashboard (2 Lajur)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Jadual Data Terkini")
    if os.path.exists('data_buku_besar.csv'):
        df = pd.read_csv('data_buku_besar.csv')
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Tiada data dijumpai. Sila jalankan bot terlebih dahulu.")

with col2:
    st.subheader("📈 Visualisasi Harga")
    if os.path.exists('data_buku_besar.csv'):
        # Paparkan graf bar ringkas
        st.bar_chart(df.set_index('Tajuk Buku')['Harga (GBP)'])
    else:
        st.write("Graf akan muncul selepas data dikumpul.")

# Bahagian Rumusan AI di bawah
st.divider()
st.subheader("🤖 Rumusan Strategik AI (Llama 3.1)")
# Nota: Pastikan main.py anda menyimpan output AI ke dalam fail teks
if os.path.exists('laporan_ai.txt'):
    with open('laporan_ai.txt', 'r') as f:
        st.info(f.read())
else:
    st.write("Menunggu analisis AI...")