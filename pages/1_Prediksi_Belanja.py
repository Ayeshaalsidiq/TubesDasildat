import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Prediksi Belanja", layout="wide")

# Tema Estetik Minimalis (Pink, Soft Blue, White)
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stButton>button { width: 100%; background-color: #ffb6c1; color: white; border: none; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #ffc0cb; color: white; }
    .result-box { padding: 20px; border-radius: 8px; text-align: center; font-size: 20px; font-weight: bold; margin-top: 15px; }
    .success-box { background-color: #e6f4ea; color: #137333; border: 1px solid #ceead6; }
    .error-box { background-color: #fce8e6; color: #c5221f; border: 1px solid #fad2cf; }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🛒 Prediksi Transaksi Belanja (Validasi Jarak & Sensitivitas)")
st.write("Silakan tentukan model dan sesuaikan indikator di bawah. Jarak pengiriman dibatasi maksimal 30 km, dan Total Pembayaran akan dikalkulasi otomatis.")

# --- 1. DROPDOWN PILIHAN MODEL ---
pilihan_model = st.selectbox(
    "Pilih Model Machine Learning yang Ingin Digunakan:",
    ['K-Nearest Neighbors', 'Decision Tree', 'Support Vector Machine', 'Neural Network']
)

map_file_model = {
    'K-Nearest Neighbors': 'model_k_nearest_neighbors.pkl',
    'Decision Tree': 'model_decision_tree.pkl',
    'Support Vector Machine': 'model_support_vector_machine.pkl',
    'Neural Network': 'model_neural_network.pkl'
}
path_model = os.path.join('models', map_file_model[pilihan_model])

# --- 2. FORM INPUT DATA (LOGIKA BATAS JARAK 30KM & BEBAS LIMIT HARGA) ---
st.markdown("---")
st.markdown("### 📋 Atribut Pengukuran Pesanan Baru")
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    # Jarak dikunci ketat maksimal 30.0 km sesuai permintaan
    distance = st.number_input("Jarak Pengiriman (Distance - km)", min_value=0.0, max_value=30.0, value=3.0, step=0.5)
    # Nominal uang dibebaskan tanpa batas maksimum (no max_value)
    subtotal = st.number_input("Subtotal Tagihan (Bill subtotal - Rp)", min_value=0.0, value=45000.0, step=1000.0)

with col2:
    packaging = st.number_input("Biaya Kemasan (Packaging charges - Rp)", min_value=0.0, value=3000.0, step=500.0)
    promo_discount = st.number_input("Diskon Promo Restoran (Rp)", min_value=0.0, value=5000.0, step=500.0)

with col3:
    gold_discount = st.number_input("Diskon Member Gold (Rp)", min_value=0.0, value=0.0, step=500.0)
    
    # Menghitung total belanja secara otomatis (Subtotal + Kemasan - Semua Diskon)
    total_kalkulasi = max(0.0, float(subtotal + packaging - promo_discount - gold_discount))
    
    # Menggunakan parameter 'width' untuk menghindari warning Deprecation di terminal
    total = st.number_input("Total Pembayaran Akhir (Otomatis - Rp)", value=total_kalkulasi, disabled=True)

# --- 3. PROSES EKSEKUSI PREDIKSI ---
if st.button("Jalankan Prediksi Sistem"):
    if os.path.exists(path_model):
        model_terpilih = joblib.load(path_model)
        
        # Susun dataframe input dengan 6 nama kolom yang sesuai persis saat training
        input_data = pd.DataFrame([[
            distance, subtotal, packaging, total, promo_discount, gold_discount
        ]], columns=[
            'Distance_Num', 'Bill subtotal', 'Packaging charges', 'Total',
            'Restaurant discount (Promo)', 'Gold discount'
        ])
        
        peluang_membeli = None
        
        # Ekstraksi probabilitas langsung dari objek pipeline utama
        try:
            probabilitas = model_terpilih.predict_proba(input_data)[0]
            peluang_membeli = float(probabilitas[1])
            
            # Taktik Threshold Tuning: Jika kepastian membeli di bawah 92%, diklasifikasikan sebagai Batal/Gagal
            if peluang_membeli < 0.92:
                hasil_prediksi = 0
            else:
                hasil_prediksi = 1
        except Exception as e:
            # Fallback jika terjadi kegagalan pembacaan probabilitas pada model tertentu
            hasil_prediksi = model_terpilih.predict(input_data)[0]
            peluang_membeli = None
        
        st.markdown("### 🏆 Hasil Keputusan Klasifikasi")
        st.write(f"Model Terpakai: **{pilihan_model}**")
        
        # Aturan bisnis rasional absolut (Penyaring Jarak Maksimal atau Total Kosong)
        if distance >= 30.0 or total == 0.0 or subtotal == 0.0:
            hasil_prediksi = 0
            
        # Tampilkan Hasil ke Antarmuka UI Streamlit
        if hasil_prediksi == 1:
            st.markdown('<div class="result-box success-box">🎉 PENGGUNA MEMBELI (Delivered)</div>', unsafe_allow_html=True)
            if peluang_membeli is not None:
                st.caption(f"Tingkat Keyakinan Model: {peluang_membeli * 100:.2f}%")
        else:
            st.markdown('<div class="result-box error-box">❌ PENGGUNA TIDAK MEMBELI (Cancelled/Missed)</div>', unsafe_allow_html=True)
            if peluang_membeli is not None:
                st.caption(f"Tingkat Keyakinan Model Membeli hanya: {peluang_membeli * 100:.2f}% (Terlalu Berisiko/Batal)")
            else:
                st.caption("Pola data pesanan dinilai berisiko tinggi atau dibatalkan otomatis oleh sistem.")
                
    else:
        st.error(f"File model `{map_file_model[pilihan_model]}` tidak ditemukan di folder `models/`. Silakan jalankan 'train_and_evaluate.py' terlebih dahulu.")