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

st.title("Dashboard Kualitas Udara")
tab1, tab2 = st.tabs(["Tren Polusi (Line Chart)", "Hubungan WSPM dan PM2.5"])

def question_1(df_all):
    with tab1:
        st.header("Bagaimana tren perkembangan rata-rata polusi dari bulan ke bulan dalam periode tahun 2013 sampai 2017?")
        st.subheader(":sparkles: Visualisasi dengan Line Chart:sparkles:")
    
        all_cities_df_2013_2017 = df_all[df_all['year'].between(2013, 2018)]
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

        with st.expander("Penjelasan Tabel :"):
       
            st.markdown("""
### Kesimpulan Grafik Tren Polusi Udara (2013-2017)

1. **Jumlah total polutan cenderung tinggi pada awal tahun (Januari) dan akhir tahun (November-Desember).**
2. **Penurunan drastis terjadi pada bulan April - Juli, yang kemungkinan disebabkan oleh curah hujan dan kondisi atmosfer yang lebih bersih.**
3. **Tahun 2014 dan 2016 menunjukkan kenaikan drastis di bulan Januari, sedangkan tahun 2017 memiliki fluktuasi yang lebih stabil.**
4. **Mulai bulan Oktober, polusi meningkat kembali, mencapai puncak pada bulan Desember, mungkin karena peningkatan aktivitas industri dan transportasi.**

""")



def question_2(df_all):
    with tab2:
        st.header("Bagaimana hubungan antara kecepatan angin (WSPM) dan tingkat PM2.5 pada hari kerja dan akhir pekan di stasiun Wanliu dalam tahun 2016?")
        st.subheader(":sparkles: Visualisasi dengan Bar Plot:sparkles: ")
        
        df_filtered = airq2_df[(airq2_df['year'] == 2016) ]
        pm25_avg = df_filtered.groupby('day')['PM2.5'].mean().reset_index()
    
        bins = sorted([0, 3, df_filtered['WSPM'].max()])
        labels = ['Rendah', 'Sedang-Tinggi']
        df_filtered['WSPM_category'] = pd.cut(df_filtered['WSPM'], bins=bins, labels=labels)

# Kategorikan hari sebagai Weekday atau Weekend
        df_filtered['day_type'] = df_filtered['day'].apply(lambda x: 'Weekday' if x <= 5 else 'Weekend')

# Hitung rata-rata PM2.5 berdasarkan kategori WSPM dan jenis hari
        pm25_avg = df_filtered.groupby(['WSPM_category', 'day_type'])['PM2.5'].mean().reset_index()

# Visualisasi dengan Bar Chart
    
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=pm25_avg, x='WSPM_category', y='PM2.5', hue='day_type', palette=['#1d4ed8', '#6fa3ef'])

# Tambahkan label nilai di atas batang
        for p in ax.patches:
                if p.get_height() > 0:
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

