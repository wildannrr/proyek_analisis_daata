import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_all = pd.read_csv("https://raw.githubusercontent.com/wildannrr/proyek_analisis_daata/refs/heads/main/Dashboard/airquality_new%20(3).csv")

with st.sidebar:
     st.header("Air Quality 🌬️")
     st.subheader("Course by Dicoding")

def load_and_process_data():
    df_all['date_time'] = pd.to_datetime(df_all[['year', 'month', 'day', 'hour']])
    return df_all

st.title("Dashboard Kualitas Udara")
tab1, tab2 = st.tabs(["Tren Polusi (Line Chart)", "Hubungan WSPM dan PM2.5"])

def question_1(df_all):
    with tab1:
        st.header("Bagaimana tren perkembangan rata-rata polusi dari bulan ke bulan dalam periode tahun 2013 sampai 2017?")
        
        
        
        df_all = df_all.drop(columns=['No'])

        df_all = df_all.dropna(subset=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'WSPM'])
        df_all['year'] = pd.to_datetime(df_all['year'], format='%Y')
        df_all['year'] = df_all['year'].dt.year

        years = sorted(df_all['year'].unique())
        selected_years = st.sidebar.multiselect("Pilih Tahun:", years, default=years[0])

        if not selected_years:
            st.warning("Silakan pilih minimal satu tahun.")
            return

        filtered_data = df_all[df_all['year'].isin(selected_years)]
        # Visualisasi Data
        st.text(f"Perkembangan Rata-rata Polusi Tahun {[str(year) for year in selected_years]}")

        st.subheader(":sparkles: Visualisasi dengan Line Chart :sparkles:")

        pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
        monthly_avg = filtered_data.groupby(['year', 'month'])[pollutants].mean().reset_index()
        monthly_avg['Total_Pollutants'] = monthly_avg[pollutants].sum(axis=1)

        
        
        fig, ax = plt.subplots(figsize=(13, 8))
        for year in selected_years:
            data_per_year = monthly_avg[monthly_avg['year'] == year]
            ax.plot(data_per_year['month'], data_per_year['Total_Pollutants'], marker='o', label=f'Total Pollutants - {year}')
            
        ax.set_title(f'Tren Bulanan Total Polutan Tahun {[str(year) for year in selected_years]}')
    
        
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Rata-rata Total Polutan')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        descriptions = {
            2013: "Pada tahun 2013, Polusi tertinggi terjadi pada bulan Juni, puncak polusi lainnya juga terjadi pada Maret, Oktober, dan Desember",
            2014: "Pada tahun 2014, Polusi tertinggi terjadi pada bulan Februari,Juni menjadi titik terendah, dan peningkatan signifikan terjadi dari September hingga November .",
            2015: "Pada tahun 2015, Januari memulai dengan level tinggi, terjadi penurunan konsisten dari Januari hingga Mei, Mei menjadi titik terendah, dan peningkatan tajam terjadi dari bulan Oktober hingga Desember, dengan Desember menjadi titik tertinggi.",
            2016: "Pada tahun 2016, Januari memulai dengan level tinggi, penurunan tajam di Februari dan kembali meningkat di bulan Maret, Mei menjadi titik terendah, dan kembali meningkat dari bulan Oktober hingga Desember",
            2017: "Pada tahun 2017, Januari menunjukan level sekitar 1950 dan Februari menunjukan penurunan hingga sekitar 1510."
}
        with st.expander("Penjelasan Tabel :"):
       
            for year in selected_years:
                st.markdown(f"**{year}: {descriptions[year]}**")




def question_2(df_all):
    with tab2:
        st.header("Bagaimana hubungan antara kecepatan angin (WSPM) dan tingkat PM2.5 pada hari kerja dan akhir pekan di stasiun Wanliu dalam tahun 2016?")
        st.subheader(":sparkles: Visualisasi dengan Bar Plot:sparkles: ")
        
        df_filtered = df_all[(df_all['year'] == 2016) ]
        pm25_avg = df_filtered.groupby('day')['PM2.5'].mean().reset_index()
    
        bins = sorted([0, 3, df_filtered['WSPM'].max()])
        labels = ['Rendah', 'Sedang-Tinggi']
        df_filtered['WSPM_category'] = pd.cut(df_filtered['WSPM'], bins=bins, labels=labels)

# Kategorikan hari sebagai Weekday atau Weekend
        df_filtered['day_type'] = df_filtered['day'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

# Hitung rata-rata PM2.5 berdasarkan kategori WSPM dan jenis hari
        pm25_avg = df_filtered.groupby(['WSPM_category', 'day_type'])['PM2.5'].mean().reset_index()

# Visualisasi dengan Bar Chart
    
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=pm25_avg, x='WSPM_category', y='PM2.5', hue='day_type', palette=['#1d4ed8', '#6fa3ef'])

# Tambahkan label nilai di atas batang
        for p in ax.patches:
                    ax.annotate(f'{p.get_height():.1f}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=8, color='black')

# Tambahkan judul dan label
        ax.set_xlabel("Kategori Kecepatan Angin")
        ax.set_ylabel("Rata-rata PM2.5")
        ax.set_title("Hubungan Kecepatan Angin dan PM2.5 pada Weekday vs Weekend (Wanliu 2016)")
        ax.legend(title='Jenis Hari')

# Tampilkan plot di Streamlit
        st.pyplot(fig)

        with st.expander("Penjelasan Tabel :"):
        
            st.markdown("""
### Kesimpulan Hubungan kecepatan angin dan PM2.5 di Wanliu pada Weekday vs Weekend.

1. **Kategori kecepatan angin sedang-tinggi = ketika kecepatan angin sedang - tinggi, rata rata PM2.5 menurun signifikan baik pada weekday maupun weekend, menunjukan bahwa kecepatan angin yg lebih tinggi membantu mengurangi konsentrasi polutan di udara dengan menyebarkannya lebih jauh**
2. **Kategori kecepatan angin rendah =  pada hari weekday, rata rata PM2.5 jauh lebih tinggi, dibandingkan weekend, menunjukan bahwa ketika kecepatan angin rendah, polusi udara lebih tinggi.**

""")
    # main function untuk run streamlit
def main():
    df_all = load_and_process_data()
    
    
    question_1(df_all)
    question_2(df_all)

if __name__ == "__main__":
        main()

