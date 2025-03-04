import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman aplikasi Streamlit
st.set_page_config(
    page_title="Analisis Kualitas Udara",
    page_icon="📝",
    layout="wide"
)

# Memuat dataset dari sumber eksternal
data_url = "https://raw.githubusercontent.com/Aryaagunawan/Proyek-Analisis-Data/refs/heads/master/dashboard/PRSA_Data_Dingling_20130301-20170228.csv"
df = pd.read_csv(data_url, on_bad_lines='skip')

# Menampilkan sidebar dengan logo dan judul
st.sidebar.image("https://cdn-icons-png.flaticon.com/128/10424/10424017.png", width=180)
st.sidebar.title("📊 Dashboard Kualitas Udara")

# Validasi kolom tanggal dalam dataset
if 'date' not in df.columns:
    if {'year', 'month', 'day'}.issubset(df.columns):
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    else:
        st.error("Data tidak memiliki kolom tanggal yang valid.")
        st.stop()

# Menetapkan kolom 'date' sebagai indeks
df.set_index('date', inplace=True)

# Sidebar: Filter data berdasarkan tanggal dan tahun
st.sidebar.header("🔎 Filter Data")
start_date = st.sidebar.date_input("Tanggal Awal", df.index.min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df.index.max().date())
year_range = st.sidebar.slider("Rentang Tahun", int(df.index.year.min()), int(df.index.year.max()), 
                               (int(df.index.year.min()), int(df.index.year.max())))

# Sidebar: Pilih polutan dan parameter lingkungan
pollutant = st.sidebar.selectbox("Pilih Polutan", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
selected_params = st.sidebar.multiselect("Pilih Parameter", ['TEMP', 'DEWP', 'PRES', 'RAIN'])

# Filter data berdasarkan input pengguna
df_filtered = df[(df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))]
df_filtered = df_filtered[(df_filtered.index.year >= year_range[0]) & (df_filtered.index.year <= year_range[1])]

# Menampilkan grafik tren polutan utama
st.header("📈 Tren PM2.5 dan PM10")
avg_pm_trend = df_filtered.groupby(df_filtered.index.year)[['PM2.5', 'PM10']].mean()
st.line_chart(avg_pm_trend)

# Korelasi antara PM2.5 dan PM10
st.write(f"🔗 Korelasi antara PM2.5 dan PM10: {df_filtered['PM2.5'].corr(df_filtered['PM10']):.2f}")

# Histogram distribusi polutan
st.subheader("📊 Distribusi PM2.5 dan PM10")
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(df_filtered['PM2.5'].dropna(), bins=50, kde=True, color='blue', ax=ax[0])
ax[0].set_title("Distribusi PM2.5")
sns.histplot(df_filtered['PM10'].dropna(), bins=50, kde=True, color='orange', ax=ax[1])
ax[1].set_title("Distribusi PM10")
st.pyplot(fig)

# Heatmap korelasi jika parameter lingkungan dipilih
if selected_params:
    st.subheader("🔥 Heatmap Korelasi")
    correlation_matrix = df_filtered[[pollutant] + selected_params].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)

# Tampilkan ringkasan statistik untuk polutan yang dipilih
st.write(f"📌 Statistik untuk {pollutant}")
st.write(df_filtered[[pollutant]].describe())

# Penutup
st.markdown("---")
st.markdown("📌 **By Arya Gunawan**")
st.markdown("📅 **Tahun: 2025**")
