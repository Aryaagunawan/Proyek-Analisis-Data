import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = 'dashboard/PRSA_Data_Dingling_20130301-20170228'
df = pd.read_csv(file_path)
try:
    df = pd.read_csv(file_url, on_bad_lines='skip')
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# Pastikan dataset tidak kosong
if df.empty:
    st.error("Dataset kosong! Periksa kembali file CSV.")
    st.stop()

# Cek apakah 'date' ada, jika tidak, buat dari 'year', 'month', 'day'
if 'date' not in df.columns:
    if {'year', 'month', 'day'}.issubset(df.columns):
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']], errors='coerce')
    else:
        st.error("Kolom 'date' tidak ditemukan dan tidak bisa dibuat dari 'year', 'month', 'day'.")
        st.stop()

# Hapus data dengan tanggal NaT (tidak valid)
df = df.dropna(subset=['date'])

# Set kolom 'date' sebagai index
df.set_index('date', inplace=True)

# Sidebar
st.sidebar.header("Filter Data")

# Pastikan ada data sebelum lanjut
if df.empty:
    st.error("Dataset kosong setelah pembersihan.")
    st.stop()

# Date Input dengan validasi rentang
start_date = st.sidebar.date_input("Pilih Tanggal Awal", df.index.min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", df.index.max().date())

if start_date > end_date:
    st.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")
    st.stop()

# Radio Button untuk memilih polutan
pollutants = [col for col in ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'] if col in df.columns]
if not pollutants:
    st.error("Tidak ada polutan yang tersedia dalam dataset!")
    st.stop()

selected_pollutant = st.sidebar.radio("Pilih Polutan", pollutants)

# MultiSelect untuk memilih parameter lingkungan
available_params = [col for col in ['TEMP', 'DEWP', 'PRES', 'RAIN'] if col in df.columns]
selected_params = st.sidebar.multiselect("Pilih Parameter Lingkungan", available_params)

# Slider untuk memilih rentang tahun
year_range = st.sidebar.slider("Pilih Rentang Tahun", int(df.index.year.min()), int(df.index.year.max()), 
                               (int(df.index.year.min()), int(df.index.year.max())))

# Filter Data
df_filtered = df[(df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))]
df_filtered = df_filtered[(df_filtered.index.year >= year_range[0]) & (df_filtered.index.year <= year_range[1])]

# Pastikan ada data setelah filter
if df_filtered.empty:
    st.error("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# **Visualisasi Tren PM2.5 dan PM10**
st.header('Tren PM2.5 dan PM10 (2013-2017)')

# Pastikan kolom ada sebelum membuat grafik
if 'PM2.5' in df_filtered.columns and 'PM10' in df_filtered.columns:
    pm_trend = df_filtered.groupby(df_filtered.index.year)[['PM2.5', 'PM10']].mean()
    st.line_chart(pm_trend)

    # **Korelasi PM2.5 dan PM10**
    correlation = df_filtered['PM2.5'].corr(df_filtered['PM10'])
    st.write(f"Korelasi antara PM2.5 dan PM10: {correlation:.2f}")
else:
    st.warning("Data untuk PM2.5 dan PM10 tidak tersedia!")

# **Distribusi PM2.5 dan PM10**
st.subheader('Distribusi PM2.5 dan PM10')

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
if 'PM2.5' in df_filtered.columns:
    sns.histplot(df_filtered['PM2.5'].dropna(), bins=50, kde=True, color='blue', ax=ax[0])
    ax[0].set_title('Distribusi PM2.5')

if 'PM10' in df_filtered.columns:
    sns.histplot(df_filtered['PM10'].dropna(), bins=50, kde=True, color='orange', ax=ax[1])
    ax[1].set_title('Distribusi PM10')

st.pyplot(fig)

# **Heatmap Korelasi Polutan dan Parameter Lingkungan**
if selected_params:
    if selected_pollutant in df_filtered.columns:
        correlation_matrix = df_filtered[[selected_pollutant] + selected_params].corr()
        st.subheader('Heatmap Korelasi')
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)
    else:
        st.warning(f"Polutan '{selected_pollutant}' tidak tersedia dalam dataset!")

st.write(f"Polutan yang dipilih: {selected_pollutant}")

# Tampilkan statistik deskriptif
if selected_pollutant in df_filtered.columns:
    col1, col2 = st.columns([2, 3])
    with col1:
        st.write("Polutan yang dipilih:", selected_pollutant)
    with col2:
        st.write(df_filtered[[selected_pollutant]].describe())
else:
    st.warning(f"Data untuk '{selected_pollutant}' tidak tersedia.")
