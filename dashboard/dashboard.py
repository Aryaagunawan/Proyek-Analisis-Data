import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# **Konfigurasi Dashboard**
st.set_page_config(page_title="Analisis Kualitas Udara", page_icon="🌍", layout="wide")

# **Memuat dataset**
dataset_url = "https://raw.githubusercontent.com/Aryaagunawan/Proyek-Analisis-Data/master/PRSA_Data_Dingling_20130301-20170228.csv"
try:
    df = pd.read_csv(dataset_url, on_bad_lines='skip')
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# **Sidebar - Navigasi dan Filter**
st.sidebar.image("https://cdn-icons-png.flaticon.com/128/10424/10424017.png", width=150)
st.sidebar.title("🌍 Analisis Kualitas Udara")

# **Proses Data**
if 'date' not in df.columns and {'year', 'month', 'day'}.issubset(df.columns):
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
elif 'date' not in df.columns:
    st.error("Kolom 'date' tidak ditemukan dan tidak dapat dibuat.")
    st.stop()

df.set_index('date', inplace=True)

# **Filter Data Berdasarkan Rentang Waktu**
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Awal", df.index.min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df.index.max().date())

# **Pilihan Polutan dengan Checkbox**
st.sidebar.subheader("Pilih Polutan")
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
selected_pollutants = [p for p in pollutants if st.sidebar.checkbox(p, value=True)]

if not selected_pollutants:
    st.error("Pilih setidaknya satu polutan untuk dianalisis.")
    st.stop()

# **Filter dataset berdasarkan tanggal**
df_filtered = df[(df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))]

# **Tampilkan Statistik Rata-rata**
st.header("📊 Statistik Polutan")
st.dataframe(df_filtered[selected_pollutants].describe())

# **Visualisasi Tren Polutan**
st.subheader("📈 Tren Polutan dari Tahun ke Tahun")
avg_trend = df_filtered[selected_pollutants].resample('M').mean()
st.line_chart(avg_trend)

# **Visualisasi Distribusi Data dengan Boxplot**
st.subheader("📊 Distribusi Polutan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_filtered[selected_pollutants], ax=ax)
ax.set_title("Boxplot Distribusi Polutan")
st.pyplot(fig)

# **Menampilkan Korelasi dalam Bentuk Heatmap**
st.subheader("🔥 Korelasi Antar Polutan")
corr_matrix = df_filtered[selected_pollutants].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
st.pyplot(fig)
