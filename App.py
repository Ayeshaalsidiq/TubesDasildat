import streamlit as st
import os
import pandas as pd

st.set_page_config(
    page_title="Shoppers Predictor — Analytics Portal",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load FontAwesome Icons untuk merender ikon list secara valid dan profesional
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# ==============================================================================
# INJEKSI FILE CSS EKSTERNAL (assets/style.css)
# ==============================================================================
css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("⚠️ File 'assets/style.css' tidak ditemukan. Pastikan folder dan file CSS sudah diperbarui!")

# ==============================================================================
# 1. HERO SECTION (BANNER UTAMA SLATE GREY & CORPORATE NAVY)
# ==============================================================================
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Shoppers Predictor Apps v2.0</div>
        <div class="hero-subtitle">Industrial-Grade Analytics for E-Commerce Transaction Validity & Risk Mitigation</div>
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. EXECUTIVE SUMMARY & DATABASE ARCHITECTURE (3 COLUMNS GRID)
# ==============================================================================
st.markdown("<div class='section-header'>Executive Summary & Data Architecture</div>", unsafe_allow_html=True)

col_db1, col_db2, col_db3 = st.columns([1.2, 1, 1], gap="large")

with col_db1:
    st.markdown("""
        <div class="consulting-card">
            <span class="badge-blue">Dataset Overview</span>
            <h4 style="margin: 15px 0 10px 0; font-weight: 600; color: #0f172a;">📦 Database Specification</h4>
            <p style="font-size: 13.5px; color: #64748b; line-height: 1.5;">
                Database utama memuat total <b>20.653 baris data riwayat transaksi</b> belanja dari lapangan dengan karakteristik ketimpangan kelas target (Highly Imbalanced Data) yang sangat kontras:
            </p>
            <ul class="data-list">
                <li><i class="fas fa-database"></i> <b>Total Records:</b> 20.653 baris data</li>
                <li><i class="fas fa-check-circle"></i> <b>Kelas Sukses (Delivered):</b> 20.471 baris data</li>
                <li><i class="fas fa-times-circle"></i> <b>Kelas Gagal (Cancelled/Missed):</b> 182 baris data</li>
                <li><i class="fas fa-balance-scale"></i> <b>Balancing Teknik:</b> SMOTE (Data Training Only)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_db2:
    st.markdown("""
        <div class="consulting-card">
            <span class="badge-blue">Feature Engineering</span>
            <h4 style="margin: 15px 0 10px 0; font-weight: 600; color: #0f172a;">⚙️ Arsitektur 6 Fitur Analitis</h4>
            <p style="font-size: 13.5px; color: #64748b; line-height: 1.5;">
                Sistem mengisolasi 6 parameter operasional murni angka dari database untuk memproses pemodelan secara objektif:
            </p>
            <ul class="data-list">
                <li><i class="fas fa-route"></i> <b>Distance_Num:</b> Jarak kurir ke pemesan (Maks. 30 km).</li>
                <li><i class="fas fa-file-invoice-dollar"></i> <b>Bill subtotal:</b> Nominal harga menu belanja bruto.</li>
                <li><i class="fas fa-box"></i> <b>Packaging charges:</b> Biaya pengemasan barang.</li>
                <li><i class="fas fa-tags"></i> <b>Discounts:</b> Potongan Harga Promo & Member Gold.</li>
                <li><i class="fas fa-calculator"></i> <b>Total:</b> Akumulasi linear pembayaran otomatis.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_db3:
    st.markdown("""
        <div class="consulting-card">
            <span class="badge-blue">Business Objective</span>
            <h4 style="margin: 15px 0 10px 0; font-weight: 600; color: #0f172a;">🎯 Target Variabel Dependen</h4>
            <p style="font-size: 13.5px; color: #475569; line-height: 1.6;">
                Isi dari target biner yang diprediksi merujuk pada konversi kolom status pesanan (Order Status) ke angka mutlak:
            </p>
            <div style="background: #f8fafc; padding: 15px; border-radius: 12px; margin-top: 15px; border: 1px solid #e2e8f0;">
                <p style="font-size: 13px; margin: 0; color: #1e293b;"><i class="fas fa-square" style="color: #0284c7; margin-right: 5px;"></i> <b>Nilai [1] (Delivered):</b> Transaksi valid, aman, dan sukses.</p>
                <p style="font-size: 13px; margin: 8px 0 0 0; color: #1e293b;"><i class="fas fa-square" style="color: #64748b; margin-right: 5px;"></i> <b>Nilai [0] (Cancelled):</b> Transaksi berisiko tinggi atau pesanan fiktif.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 3. GLOBAL PERFORMANCE EVALUATION (DIFOKUSKAN PADA RECALL + TABEL PREMIUM BLUES)
# ==============================================================================
st.markdown("<div class='section-header'>Global Performance Evaluation</div>", unsafe_allow_html=True)

col_ev1, col_ev2 = st.columns([1, 1.8], gap="large")

with col_ev1:
    st.markdown("""
    <div class="consulting-card" style="background: #ffffff;">
        <h5 style="color: #0f172a; font-weight: 600; margin-bottom: 10px;"><i class="fas fa-chart-line" style="color:#0ea5e9; margin-right: 8px;"></i> Recall Priority Analysis</h5>
        <p class="card-body" style="font-size: 13.5px; color: #64748b; line-height: 1.6; margin: 0;">
            Dalam kasus klasifikasi ketimpangan data belanja ini, fokus analisis kelompok kami dipusatkan pada metrik <b>Recall (Sensitivitas)</b>, bukan akurasi standar belaka.<br><br>
            Recall yang tinggi menjamin sistem mampu mendeteksi sebanyak mungkin transaksi yang berpotensi gagal/batal (memperkecil celah <i>False Negative</i>). 
            Jika nilai Recall lemah, sistem akan meloloskan pesanan palsu/batal ke kurir, yang berakibat pada kerugian finansial merchant dan waktu kurir secara nyata.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_ev2:
    # Memuat data leaderboard hasil training lengkap (Accuracy, Precision, Recall, F1)
    path_leaderboard = os.path.join('data', 'leaderboard_performa.csv')
    if os.path.exists(path_leaderboard):
        df_lb = pd.read_csv(path_leaderboard)
        
        # Penamaan kolom visualisasi header tabel agar rapi dan informatif
        df_lb.columns = ['Machine Learning Model', 'Accuracy (%)', 'Precision (%)', 'Recall (%)', 'F1-Score (%)']
        
        # Terapkan gradient warna Blues pada metrik performa secara aman lewat Streamlit dataframe
        try:
            styled_df = df_lb.style.background_gradient(cmap='Blues', subset=['Accuracy (%)', 'Precision (%)', 'Recall (%)', 'F1-Score (%)'])\
                                   .format(precision=2)
            st.write("📊 **Model Metrics Comparison Matrix (Data Uji Murni)**")
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        except Exception:
            # Fallback tanpa gradien warna jika library matplotlib belum ter-install sempurna
            st.write("📊 **Model Metrics Comparison Matrix (Data Uji Murni)**")
            st.dataframe(df_lb, use_container_width=True, hide_index=True)
    else:
        st.warning("📊 File leaderboard_performa.csv belum ditemukan. Silakan jalankan file 'train_and_evaluate.py' terlebih dahulu di terminal untuk membuat data metrik lengkap!")


# ==============================================================================
# 4. TEORI JALUR 4 MODEL MACHINE LEARNING
# ==============================================================================
st.markdown("<div class='section-header'>Arsitektur & Teori Core Algoritma Klasifikasi</div>", unsafe_allow_html=True)

col_mod1, col_mod2, col_mod3, col_mod4 = st.columns(4, gap="medium")

with col_mod1:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #0284c7;">
            <div style="font-weight:700; font-size:15px; color:#0f172a; margin-bottom:8px;">1. K-Nearest Neighbors</div>
            <p class="card-body" style="font-size:12.5px; color: #475569;">
                <b>Instance-Based Learning:</b> Mengklasifikasikan objek transaksi baru berdasarkan kedekatan klaster spasial (<em>Euclidean distance</em>) terhadap mayoritas 5 data tetangga terdekat.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_mod2:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #334155;">
            <div style="font-weight:700; font-size:15px; color:#0f172a; margin-bottom:8px;">2. Decision Tree</div>
            <p class="card-body" style="font-size:12.5px; color: #475569;">
                <b>Hierarchical Split Rules:</b> Memetakan diagram pohon keputusan terstruktur menggunakan pemisahan nilai indeks ketidakmurnian Gini (<em>Gini Impurity</em>) dengan kedalaman pohon diatur maks 6 tingkat.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_mod3:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #0284c7;">
            <div style="font-weight:700; font-size:15px; color:#0f172a; margin-bottom:8px;">3. Support Vector Machine</div>
            <p class="card-body" style="font-size:12.5px; color: #475569;">
                <b>Hyperplane Maximization:</b> Memisahkan ruang dimensi data secara optimal dengan batas margin terbesar menggunakan bantuan fungsi <em>Kernel RBF</em> serta kalibrasi kecocokan probabilitas.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_mod4:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #334155;">
            <div style="font-weight:700; font-size:15px; color:#0f172a; margin-bottom:8px;">4. Neural Network (MLP)</div>
            <p class="card-body" style="font-size:12.5px; color: #475569;">
                <b>Multi-Layer Perceptron:</b> Memodelkan interaksi sinyal data non-linear kompleks lewat interkoneksi 2 hidden layer (50 & 25 neuron) menggunakan mekanisme optimasi rambatan balik.
            </p>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 5. STRUKTUR TIM PENGEMBANG & SPESIALISASI
# ==============================================================================
st.markdown("<div class='section-header'>Struktur Pengembang & Spesialisasi Model</div>", unsafe_allow_html=True)

col_team1, col_team2, col_team3, col_team4 = st.columns(4, gap="medium")

team_data = [
    {"name": "Ayesha Al Sidiq", "role": "SVM Specialist", "desc": "Fokus pada kalkulasi penemuan hyperplane optimal, penyelarasan hyperparameter penalti C, serta integrasi pemetaan probabilistik model."},
    {"name": "Saskia Naila Sagita", "role": "KNN Specialist", "desc": "Bertanggung jawab penuh atas visualisasi sebaran metrik kedekatan klaster data transaksi serta validasi pembobotan tetangga terdekat."},
    {"name": "Fahreza Azhar Ramadhan", "role": "DT Specialist", "desc": "Berfokus pada analisis kriteria penentuan nodus akar keputusan (root node) serta pencegahan over-parameterisasi kedalaman cabang."},
    {"name": "Aninda Irfani", "role": "NN Specialist", "desc": "Bertanggung jawab penuh dalam penyusunan bobot bias arsitektur multi-layer neural network serta minimalisasi laju loss error iterasi."}
]

cols_list = [col_team1, col_team2, col_team3, col_team4]
for idx, member in enumerate(team_data):
    with cols_list[idx]:
        st.markdown(f"""
        <div class="profile-card-container">
            <div class="p-name">{member['name']}</div>
            <div class="p-role">{member['role']}</div>
            <p class="p-desc">{member['desc']}</p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 6. BUSINESS SAFETY LOGIC (THRESHOLD TUNING INFO)
# ==============================================================================
st.markdown("<div class='section-header'>Kebijakan Filter & Kontrol Sensitivitas Bisnis</div>", unsafe_allow_html=True)
st.markdown("""
    <div class="premium-card" style="background: linear-gradient(90deg, #ffffff 75%, #f8fafc 100%); border-left: 5px solid #0f172a;">
        <p class="card-body" style="color: #334155; font-size: 13.5px; margin: 0;">
            <strong>Mekanisme Penilaian Ketat (Probability Thresholding 92%):</strong> 
            Karena distribusi dataset awal bersifat timpang ekstrem, platform analitik ini mengabaikan batas toleransi bawaan default model (50%). 
            Sistem mengunci regulasi ketat: Apabila tingkat keyakinan model matematika untuk kelas sukses bernilai di bawah <b>92.00%</b>, 
            back-end website secara otomatis membatalkan transaksi dan mengubah keputusan menjadi status risiko tinggi (<strong>Cancelled/Missed Order</strong>). 
            Hal ini bertujuan memberikan lapisan keamanan preventif bagi merchant e-commerce dari ancaman pesanan fiktif.
        </p>
    </div>
""", unsafe_allow_html=True)

# Footer Platform Akademik
st.markdown("<br><p style='text-align: center; color: #94a3b8; font-size: 12px; font-weight:500;'>Proyek Praktikum Dasar Ilmu Data 2026 • Kurikulum Diploma (D3) Sistem Informasi • Telkom University</p>", unsafe_allow_html=True)