import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Visualisasi & Analisis Eksplanatori",
    page_icon="📊",
    layout="wide"
)

# Judul aplikasi
st.title("📊 Visualisasi & Analisis Eksplanatori")

# Memuat dataset
@st.cache_data  # Menggunakan cache untuk meningkatkan performa
def load_data():
    data_url = "https://raw.githubusercontent.com/Aryaagunawan/Proyek-Analisis-Data/refs/heads/master/dashboard/PRSA_Data_Dingling_20130301-20170228.csv"
    df = pd.read_csv(data_url, on_bad_lines='skip')
    
    # Validasi kolom tanggal
    if 'date' not in df.columns:
        if {'year', 'month', 'day'}.issubset(df.columns):
            df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        else:
            st.error("Data tidak memiliki kolom tanggal yang valid.")
            st.stop()
    
    df.set_index('date', inplace=True)
    return df

df_Dingling = load_data()

# Sidebar untuk filter
st.sidebar.header("🔧 Filter Data")

# Filter 1: Rentang Tanggal
st.sidebar.subheader("📅 Filter Berdasarkan Tanggal")
start_date = st.sidebar.date_input("Tanggal Awal", df_Dingling.index.min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df_Dingling.index.max().date())

# Filter 2: Rentang Tahun
st.sidebar.subheader("📅 Filter Berdasarkan Tahun")
year_range = st.sidebar.slider(
    "Pilih Rentang Tahun",
    min_value=int(df_Dingling.index.year.min()),
    max_value=int(df_Dingling.index.year.max()),
    value=(int(df_Dingling.index.year.min()), int(df_Dingling.index.year.max()))
)

# Filter 3: Kategori PM2.5
st.sidebar.subheader("🏷️ Filter Berdasarkan Kategori PM2.5")
bins = [0, 50, 100, df_Dingling['PM2.5'].max()]
labels = ['Rendah', 'Sedang', 'Tinggi']
df_Dingling['PM2.5_Category'] = pd.cut(df_Dingling['PM2.5'], bins=bins, labels=labels)
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori PM2.5",
    options=labels,
    default=labels
)

# Mengaplikasikan filter ke dataset
filtered_df = df_Dingling[
    (df_Dingling.index >= pd.Timestamp(start_date)) &
    (df_Dingling.index <= pd.Timestamp(end_date)) &
    (df_Dingling.index.year >= year_range[0]) &
    (df_Dingling.index.year <= year_range[1]) &
    (df_Dingling['PM2.5_Category'].isin(selected_categories))
]

# Menampilkan dataset yang telah difilter
st.subheader("📋 Dataset yang Telah Difilter")
st.write(filtered_df)

# Visualisasi 1: Tren PM2.5 dan PM10
st.subheader("📈 Tren PM2.5 dan PM10 (2013-2017)")
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

sns.lineplot(data=filtered_df.resample('M')['PM2.5'].mean(), ax=ax[0], color='red')
ax[0].set_title('Tren PM2.5 (2013-2017)')

sns.lineplot(data=filtered_df.resample('M')['PM10'].mean(), ax=ax[1], color='blue')
ax[1].set_title('Tren PM10 (2013-2017)')

st.pyplot(fig)

# Visualisasi 2: Heatmap Korelasi
st.subheader("📜 Heatmap Korelasi PM2.5, PM10 dengan Faktor Lingkungan")
plt.figure(figsize=(10, 5))
sns.heatmap(filtered_df[['PM2.5', 'PM10', 'TEMP', 'PRES', 'DEWP', 'RAIN']].corr(), annot=True, cmap='coolwarm')
plt.title('Korelasi PM2.5, PM10 dengan Faktor Lingkungan')
st.pyplot(plt.gcf())

# Visualisasi 3: Distribusi Kategori PM2.5
st.subheader("📊 Distribusi Kategori PM2.5")
plt.figure(figsize=(8, 4))
sns.countplot(x=filtered_df['PM2.5_Category'], palette='coolwarm')
plt.title('Distribusi Kategori PM2.5')
plt.xlabel('Kategori')
plt.ylabel('Jumlah Observasi')
st.pyplot(plt.gcf())

# Penutup
st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 Dibuat oleh [Nama Anda]")
st.sidebar.markdown("📅 Tahun 2023")