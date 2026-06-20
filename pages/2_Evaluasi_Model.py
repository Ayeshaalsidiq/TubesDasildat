import streamlit as st
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

st.set_page_config(page_title="Evaluasi Model", layout="wide")

st.markdown("## 📊 Laporan Performa Klasifikasi Model (6 Fitur)")
st.write("Halaman ini menampilkan metrik evaluasi (Precision, Recall, F1-Score) secara akurat menggunakan data uji murni asli.")

# 1. AMBIL DATA MENTAH ASLI untuk memisahkan data uji murni (Tanpa Kebocoran SMOTE)
nama_file_target = 'order_history_kaggle_data.xlsx - order_history_kaggle_data.csv'
path_mentah = None

lokasi_kemungkinan = [
    os.path.join('data', nama_file_target),
    nama_file_target,
    os.path.join('data', 'order_history_kaggle_data.csv'),
    'order_history_kaggle_data.csv'
]

for lokasi in lokasi_kemungkinan:
    if os.path.exists(lokasi):
        path_mentah = lokasi
        break

if not path_mentah:
    # Cari file alternatif jika nama tidak pas
    files_csv = [f for f in os.listdir('.') if f.endswith('.csv')] + \
                ([os.path.join('data', f) for f in os.listdir('data') if f.endswith('.csv')] if os.path.exists('data') else [])
    if files_csv:
        path_mentah = files_csv[0]

if path_mentah:
    df_shop = pd.read_csv(path_mentah)
    
    # Preprocessing Biner Target
    df_shop['Target_Beli'] = df_shop['Order Status'].apply(lambda x: 1 if str(x).strip() == 'Delivered' else 0)
    
    # Bersihkan kolom jarak
    df_shop['Distance_Num'] = pd.to_numeric(
        df_shop['Distance'].astype(str).str.replace('km', '', case=False).str.strip(), 
        errors='coerce'
    ).fillna(0)
    
    # Kunci 6 Fitur Utama & Amankan dari NaN
    fitur_pilihan = [
        'Distance_Num', 'Bill subtotal', 'Packaging charges', 'Total',
        'Restaurant discount (Promo)', 'Gold discount'
    ]
    for col in fitur_pilihan:
        df_shop[col] = pd.to_numeric(df_shop[col], errors='coerce').fillna(0.0)
        
    X = df_shop[fitur_pilihan].astype(float)
    y = df_shop['Target_Beli'].astype(int)
    
    # Split dengan parameter yang sama persis (random_state=42) untuk mengambil data uji murni
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # --- 2. SELECTBOX PILIHAN MODEL INTERAKTIF ---
    pilihan_model = st.selectbox("Pilih Arsitektur Model untuk Melihat Detail Metrik:", [
        'K-Nearest Neighbors', 'Decision Tree', 'Support Vector Machine', 'Neural Network'
    ])
    
    map_file = {
        'K-Nearest Neighbors': 'model_k_nearest_neighbors.pkl',
        'Decision Tree': 'model_decision_tree.pkl',
        'Support Vector Machine': 'model_support_vector_machine.pkl',
        'Neural Network': 'model_neural_network.pkl'
    }
    
    path_model = os.path.join('models', map_file[pilihan_model])
    
    if os.path.exists(path_model):
        # Load model pkl
        pipeline = joblib.load(path_model)
        
        # Prediksi data uji murni
        y_pred = pipeline.predict(X_test)
        
        # Hitung Report Klasifikasi
        report_dict = classification_report(y_test, y_pred, output_dict=True)
        df_report = pd.DataFrame(report_dict).transpose()
        
        st.markdown(f"### 📋 Classification Report - {pilihan_model}")
        st.dataframe(df_report.style.format(precision=4), use_container_width=True)
        st.success(f"Metrik di atas dihitung secara objektif menggunakan {X_test.shape[0]} baris data uji murni.")
    else:
        st.error(f"File model `{map_file[pilihan_model]}` tidak ditemukan.")
else:
    st.error("Gagal memuat dataset untuk proses evaluasi.")