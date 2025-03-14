# Air Quality
Source of Dataset : https://www.kaggle.com/datasets/malikiborneo/air-quality-dataset-from-dicoding-data-science

## Business Understanding
Pertanyaan bisnis:

1.Apakah ada periode atau bulan tertentu dalam setahun di mana kualitas udara lebih buruk?

2.Bagaimana hubungan antara kecepatan angin (WSPM) dan tingkat PM2.5 pada hari kerja dan akhir pekan di stasiun Wanliu dalam tahun 2016?

## Set up Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Set up shell/terminal
mkdir visualisasi_data_streamlit
cd visualisasi_data_streamlit
pipenv install
pipenv shell
pip install -r requirements.txt

## Run Streamlit app
streamlit run dashboard.py



