import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_day = pd.read_csv("Dashboard/bike_sharing_day.csv")
df_hour = pd.read_csv("Dashboard/bike_sharing_hour.csv")  

# Mapping angka musim ke nama musim sebenarnya
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df_day["season"] = df_day["season"].map(season_mapping)
df_hour["season"] = df_hour["season"].map(season_mapping)

# Mapping cuaca ke deskripsi
weather_mapping = {1: "Clear", 2: "Cloudy/Mist", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
df_day["weathersit"] = df_day["weathersit"].map(weather_mapping)
df_hour["weathersit"] = df_hour["weathersit"].map(weather_mapping)

# Mapping hari dalam seminggu
weekday_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
df_day["weekday"] = df_day["weekday"].map(weekday_mapping)
df_hour["weekday"] = df_hour["weekday"].map(weekday_mapping)

# Mapping bulan
month_mapping = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 
                 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
df_day["mnth"] = df_day["mnth"].map(month_mapping)
df_hour["mnth"] = df_hour["mnth"].map(month_mapping)

# Tambahkan kolom rush_hour ke df_hour (07:00-09:00 dan 17:00-19:00 sebagai rush hour)
df_hour["rush_hour"] = df_hour["hr"].apply(lambda x: 1 if (7 <= x <= 9 or 17 <= x <= 19) else 0)

# Set title
st.title("📊 Bike Sharing Dashboard")

# Sidebar untuk filter
st.sidebar.header("🔍 Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim:", options=["All"] + list(df_day['season'].unique()), index=0)
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca:", options=["All"] + list(df_day['weathersit'].unique()), index=0)
selected_year = st.sidebar.selectbox("Pilih Tahun:", options=["All", 2011, 2012], index=0)
selected_workingday = st.sidebar.selectbox("Pilih Tipe Hari:", options=["All", "Hari Kerja", "Akhir Pekan/Libur"], index=0)
selected_month = st.sidebar.selectbox("Pilih Bulan:", options=["All"] + list(df_day['mnth'].unique()), index=0)
selected_weekday = st.sidebar.selectbox("Pilih Hari dalam Seminggu:", options=["All"] + list(df_day['weekday'].unique()), index=0)
temp_range = st.sidebar.slider("Pilih Rentang Suhu (Normalized):", min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.01)

# Menampilkan informasi kontak di bawah filter
st.sidebar.markdown("---")
st.sidebar.header("📩 Kontak")
st.sidebar.write("**Nama:** Revo Pratama")
st.sidebar.write("**ID Dicoding:** MC19D5Y1619")
st.sidebar.write("**Email:** revopratama2004@gmail.com")

# Filter data berdasarkan pilihan pengguna
filtered_df_day = df_day.copy()
filtered_df_hour = df_hour.copy()

if selected_season != "All":
    filtered_df_day = filtered_df_day[filtered_df_day['season'] == selected_season]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['season'] == selected_season]

if selected_weather != "All":
    filtered_df_day = filtered_df_day[filtered_df_day['weathersit'] == selected_weather]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['weathersit'] == selected_weather]

if selected_year != "All":
    year_map = {2011: 0, 2012: 1}
    filtered_df_day = filtered_df_day[filtered_df_day['yr'] == year_map[selected_year]]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['yr'] == year_map[selected_year]]

if selected_workingday != "All":
    workingday_map = {"Hari Kerja": 1, "Akhir Pekan/Libur": 0}
    filtered_df_day = filtered_df_day[filtered_df_day['workingday'] == workingday_map[selected_workingday]]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['workingday'] == workingday_map[selected_workingday]]

if selected_month != "All":
    filtered_df_day = filtered_df_day[filtered_df_day['mnth'] == selected_month]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['mnth'] == selected_month]

if selected_weekday != "All":
    filtered_df_day = filtered_df_day[filtered_df_day['weekday'] == selected_weekday]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['weekday'] == selected_weekday]

# Filter berdasarkan rentang suhu
filtered_df_day = filtered_df_day[(filtered_df_day['temp'] >= temp_range[0]) & (filtered_df_day['temp'] <= temp_range[1])]
filtered_df_hour = filtered_df_hour[(filtered_df_hour['temp'] >= temp_range[0]) & (filtered_df_hour['temp'] <= temp_range[1])]

# Statistik ringkasan
st.subheader("📈 Statistik Data Harian")
st.write(filtered_df_day.describe())

# Visualisasi 1: Distribusi Penyewaan Sepeda Harian
st.subheader("📊 Distribusi Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(12, 5))
sns.histplot(filtered_df_day["cnt"], bins=30, kde=True, color="blue", ax=ax)
ax.axvline(filtered_df_day["cnt"].mean(), color='red', linestyle='dashed', linewidth=2, label="Mean")
ax.set_title("Distribusi Penyewaan Sepeda Harian", fontsize=14)
ax.set_xlabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.set_ylabel("Frekuensi", fontsize=12)
ax.legend()
st.pyplot(fig)

# Visualisasi 2: Distribusi Penyewaan Sepeda Per Jam
st.subheader("📊 Distribusi Penyewaan Sepeda Per Jam")
fig, ax = plt.subplots(figsize=(12, 5))
sns.histplot(filtered_df_hour["cnt"], bins=30, kde=True, color="green", ax=ax)
ax.axvline(filtered_df_hour["cnt"].mean(), color='red', linestyle='dashed', linewidth=2, label="Mean")
ax.set_title("Distribusi Penyewaan Sepeda Per Jam", fontsize=14)
ax.set_xlabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.set_ylabel("Frekuensi", fontsize=12)
ax.legend()
st.pyplot(fig)

# Visualisasi 3: Rata-rata Penyewaan Sepeda Berdasarkan Musim
st.subheader("🚲 Rata-rata Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
season_avg = filtered_df_day.groupby("season")["cnt"].mean().reset_index()
sns.barplot(x="season", y="cnt", data=season_avg, palette="coolwarm", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", fontsize=14)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
st.pyplot(fig)

# Visualisasi 4: Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader("🌤️ Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
weather_avg = filtered_df_day.groupby("weathersit")["cnt"].mean().reset_index()
sns.barplot(x="weathersit", y="cnt", data=weather_avg, palette="magma", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=14)
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Visualisasi 5: Rata-rata Penyewaan Sepeda Berdasarkan Jam
st.subheader("⏰ Rata-rata Penyewaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(12, 5))
hour_avg = filtered_df_hour.groupby("hr")["cnt"].mean().reset_index()
sns.lineplot(x="hr", y="cnt", data=hour_avg, marker="o", color="red", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(True)
st.pyplot(fig)

# Visualisasi 6: Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu
st.subheader("📅 Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
fig, ax = plt.subplots(figsize=(10, 5))
weekday_avg = filtered_df_day.groupby("weekday")["cnt"].mean().reset_index()
sns.barplot(x="weekday", y="cnt", data=weekday_avg, palette="viridis", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu", fontsize=14)
ax.set_xlabel("Hari dalam Seminggu", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Visualisasi 7: Identifikasi Jam Sibuk (Rush Hour)
st.subheader("⏰ Rata-rata Penyewaan Sepeda pada Rush Hour vs Non-Rush Hour")
fig, ax = plt.subplots(figsize=(10, 5))
rush_hour_avg = filtered_df_hour.groupby("rush_hour")["cnt"].mean().reset_index()
sns.barplot(x="rush_hour", y="cnt", data=rush_hour_avg, palette="plasma", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda pada Rush Hour vs Non-Rush Hour", fontsize=14)
ax.set_xlabel("Rush Hour (0=Tidak, 1=Ya)", fontsize=12)
ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Non-Rush Hour", "Rush Hour"])
st.pyplot(fig)