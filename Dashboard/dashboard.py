import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

airq1_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Tiantan_20130301-20170228.csv") 
airq2_df = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Wanliu_20130301-20170228.csv")

def load_and_process_data():
    df_all = pd.concat([airq1_df, airq2_df])
    df_all['date_time'] = pd.to_datetime(df_all[['year', 'month', 'day', 'hour']])
    
    return df_all
def question_1(df_all):
    st.header("Apakah ada periode atau bulan tertentu dalam setahun di mana kualitas udara lebih buruk?")
    st.subheader(":sparkles: Visualisasi dengan Line Chart:sparkles:")
    
    all_cities_df_2013_2017 = df_all[df_all['year'].between(2013, 2017)]
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    monthly_avg = all_cities_df_2013_2017.groupby(['year', 'month'])[pollutants].mean().reset_index()
    monthly_avg['Total_Pollutants'] = monthly_avg['PM2.5'] + monthly_avg['PM10'] + monthly_avg['SO2'] + monthly_avg['NO2'] + monthly_avg['CO'] + monthly_avg['O3']
    
    # visualisasi tren bulanan
    fig, ax = plt.subplots(figsize=(12, 8))
    for year in range(2013, 2017 + 1):
        data_per_year = monthly_avg[monthly_avg['year'] == year]
        ax.plot(data_per_year['month'], data_per_year['Total_Pollutants'], marker='o', label=f'Total Pollutants - {year}')
    
    ax.set_title('Tren Bulanan Total Polutan (2013-2017)')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Total Polutan')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    with st.sidebar:
    
        st.text('Air Quality')
    
        values = st.slider(
            label='Select a range of year',
            min_value=2013, max_value=2017, value=(2013,2017),
            key="slider_unique_id"
        )
        st.write('Tahun:', values)

    with st.expander("Penjelasan Tabel :"):
        st.write(
            """Line Chart ini menunjukkan tren bulanan rata-rata total polutan dari tahun 2013 hingga 2017. Sumbu X mewakili bulan dalam satu tahun, sedangkan sumbu Y menunjukkan rata-rata total polutan yang terdiri dari PM2.5, PM10, SO2, NO2, CO, dan O3."""
        )
    st.markdown("""
### Kesimpulan Grafik Tren Polusi Udara (2013-2017)

1. **Polusi tertinggi terjadi di bulan Januari dan Desember, kemungkinan karena penggunaan pemanas dan kondisi atmosfer musim dingin.**
2. **Penurunan drastis terjadi pada bulan Maret - Mei, yang kemungkinan disebabkan oleh curah hujan dan kondisi atmosfer yang lebih bersih.**
3. **Musim panas (Juni - Agustus) menunjukkan fluktuasi, dengan beberapa lonjakan polusi akibat peningkatan suhu.
4. **Mulai bulan Oktober, polusi meningkat kembali, mencapai puncak pada bulan Desember, mungkin karena peningkatan aktivitas industri dan transportasi.**

""")



def question_2(df_all):
    st.header("Bagaimana hubungan antara kecepatan angin (WSPM) dan tingkat PM2.5 pada hari kerja dan akhir pekan di stasiun Wanliu dalam tahun 2016?")
    st.subheader(":sparkles: Visualisasi dengan Scatter Plot:sparkles: ")
    df_filtered = df_all[(df_all['year'] == 2016) & (df_all['station'] == 'Tiantan')]

    df_filtered['date'] = pd.to_datetime(df_filtered[['year', 'month', 'day']])
    df_filtered['dayofweek'] = df_filtered['date'].dt.dayofweek
    df_filtered['day_type'] = df_filtered['dayofweek'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

    # scatter plot hubungan antara WSPM dan PM2.5
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df_filtered, x='WSPM', y='PM2.5', hue='day_type', alpha=0.6, ax=ax)
    ax.set_xlabel("Kecepatan Angin (WSPM)")
    ax.set_ylabel("Tingkat PM2.5")
    ax.set_title("Hubungan Kecepatan Angin dan PM2.5 (Weekday vs Weekend) di Wanliu (2016)")
    st.pyplot(fig)

    with st.expander("Penjelasan Tabel :"):
        st.write(
            """Scatter plot digunakan untuk melihat hubungan antara dua variabel. Dalam hal ini, scatter plot mungkin menunjukkan hubungan antara waktu dan tingkat PM2.5 di lokasi tertentu. Jika titik-titik pada scatter plot membentuk pola tertentu (naik atau turun), maka dua variabel tersebut berhubungan."""
        )
    st.markdown("""
### Kesimpulan Hubungan kecepatan angin dan PM2.5 di Wanliu pada Weekday vs Weekend.

1. **Jika titik-titik tidak membentuk pola tertentu, tidak ada hubungan yang jelas antara waktu dan tingkat PM2.5.**
2. **Jika ada pola naik atau turun, berarti ada hubungan antara waktu dan tingkat PM2.5.**
3. **Scatter plot juga dapat membantu mengidentifikasi outlier (anomali) dalam data.**

""")


    st.subheader(":sparkles: Visualisasi Boxplot PM2.5:sparkles:")

# Membuat figure
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df_filtered, x='day_type', y='PM2.5', ax=ax)
    ax.set_xlabel("Jenis Hari")
    ax.set_ylabel("Tingkat PM2.5")
    ax.set_title("Distribusi PM2.5 pada Hari Kerja vs Akhir Pekan (Tiantan 2016)")
    st.pyplot(fig)

    with st.expander("Penjelasan Tabel :"):
        st.write(
            """Boxplot digunakan untuk membandingkan distribusi data dari dua atau lebih kategori. Dalam konteks ini, boxplot membandingkan tingkat PM2.5 pada Weekdaydan Weekend."""
        )
    st.markdown("""
### Kesimpulan Distribusi PM2.5 pada Weekday vs Weekend di tiantan (2016)

1. **Jika median pada boxplot weekday lebih tinggi daripada weekend, berarti polusi udara lebih tinggi pada hari kerja dibanding akhir pekan.**
2. **Jika distribusi weekday lebih menyebar daripada weekend, berarti variasi tingkat PM2.5 lebih besar pada hari kerja.**
3. **Jika ada banyak outlier, itu menunjukkan adanya lonjakan atau penurunan ekstrem dalam tingkat polusi udara.**
""")


    # main function untuk run streamlit
def main():
    st.title("Dashboard Kualitas Udara")
    df_all = load_and_process_data()
    
    
    question_1(df_all)
    question_2(df_all)

if __name__ == "__main__":
    main()

