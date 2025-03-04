import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# **Set konfigurasi halaman Streamlit**
st.set_page_config(
    page_title="Dashboard",
    page_icon="📝",
    layout="wide"
)
# Load dataset
file_path = "https://raw.githubusercontent.com/Aryaagunawan/Proyek-Analisis-Data/refs/heads/master/dashboard/PRSA_Data_Dingling_20130301-20170228.csv"
df = pd.read_csv(file_path, on_bad_lines='skip')

st.sidebar.image("https://www.flaticon.com/free-icon/air-quality-sensor_10424017?term=air+quality&page=2&position=39&origin=search&related_id=10424017", width=100)
st.sidebar.title("Air Quality Dataset")

# Cek apakah 'date' ada, jika tidak, buat dari 'year', 'month', 'day'
if 'date' not in df.columns:
    if {'year', 'month', 'day'}.issubset(df.columns):
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    else:
        st.error("Kolom 'date' tidak ditemukan dan tidak bisa dibuat dari 'year', 'month', 'day'.")
        st.stop()

# Set kolom 'date' sebagai index
df.set_index('date', inplace=True)

# Sidebar
st.sidebar.header("Filter Data")

# Date Input
start_date = st.sidebar.date_input("Pilih Tanggal Awal", df.index.min().date())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", df.index.max().date())

# Radio Button untuk memilih polutan
selected_pollutant = st.sidebar.radio("Pilih Polutan", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])

# MultiSelect untuk memilih parameter lingkungan
selected_params = st.sidebar.multiselect("Pilih Parameter Lingkungan", ['TEMP', 'DEWP', 'PRES', 'RAIN'])

# Slider untuk memilih rentang tahun
year_range = st.sidebar.slider("Pilih Rentang Tahun", int(df.index.year.min()), int(df.index.year.max()), 
                               (int(df.index.year.min()), int(df.index.year.max())))

# **Perbaikan: Filter Data dengan Boolean Mask**
df_filtered = df[(df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))]
df_filtered = df_filtered[(df_filtered.index.year >= year_range[0]) & (df_filtered.index.year <= year_range[1])]

# **Visualisasi Tren PM2.5 dan PM10**
st.header('Tren PM2.5 dan PM10 (2013-2017)')
pm_trend = df_filtered.groupby(df_filtered.index.year)[['PM2.5', 'PM10']].mean()
st.line_chart(pm_trend)

# **Korelasi PM2.5 dan PM10**
correlation = df_filtered['PM2.5'].corr(df_filtered['PM10'])
st.write(f"Korelasi antara PM2.5 dan PM10: {correlation:.2f}")

# **Distribusi PM2.5 dan PM10**
st.subheader('Distribusi PM2.5 dan PM10')
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sns.histplot(df_filtered['PM2.5'].dropna(), bins=50, kde=True, color='blue', ax=ax[0])
ax[0].set_title('Distribusi PM2.5')

sns.histplot(df_filtered['PM10'].dropna(), bins=50, kde=True, color='orange', ax=ax[1])
ax[1].set_title('Distribusi PM10')

st.pyplot(fig)

# **Heatmap Korelasi Polutan dan Parameter Lingkungan**
if selected_params:
    correlation_matrix = df_filtered[[selected_pollutant] + selected_params].corr()
    st.subheader('Heatmap Korelasi')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)

st.write(f"Polutan yang dipilih: {selected_pollutant}")

if selected_pollutant not in df_filtered.columns:
    st.error(f"Polutan '{selected_pollutant}' tidak ditemukan dalam dataset!")
    st.stop()

col1, col2 = st.columns([2, 3])  # Atur rasio kolom

with col1:
    st.write("Polutan yang dipilih:", selected_pollutant)

with col2:
    st.write(df_filtered[[selected_pollutant]].describe())
