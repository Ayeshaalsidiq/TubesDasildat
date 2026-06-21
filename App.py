import streamlit as st
import os
import pandas as pd

# ==============================================================================
# KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Shoppers Predictor — Analytics Portal",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load FontAwesome Icons untuk ikon
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# ==============================================================================
# INJEKSI CSS CUSTOM (Menggantikan assets/style.css agar langsung berjalan)
# ==============================================================================
custom_css = """
<style>
    /* --- 1. SEMBUNYIKAN MENU DEFAULT STREAMLIT --- */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* --- 2. WARNA SIDEBAR CORPORATE NAVY --- */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        padding-top: 20px;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important; 
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #38bdf8 !important; /* Warna biru muda untuk judul sidebar */
        font-weight: 700;
    }
    hr {
        border-color: #334155 !important;
    }

    /* --- 3. STYLING UNTUK CUSTOM MENU LINK DI SIDEBAR --- */
    div[data-testid="stPageLink-NavLink"] {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 12px;
        border-left: 4px solid transparent;
        transition: all 0.3s ease;
    }
    div[data-testid="stPageLink-NavLink"]:hover {
        background-color: #334155;
        border-left: 4px solid #0ea5e9;
        transform: translateX(6px); /* Efek bergeser ke kanan saat disentuh mouse */
    }

    /* Hero Section (Banner Atas) */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 40px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.4);
        border-bottom: 4px solid #0ea5e9;
    }
    .hero-title {
        /* Membuat warna judul banner menjadi gradient biru muda ke ungu */
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 18px;
        font-weight: 400;
    }

    /* Header Tiap Section */
    .section-header {
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Kartu (Cards) untuk Konten */
    .consulting-card, .premium-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .consulting-card:hover, .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Badge Label */
    .badge-blue {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* List Item Custom */
    .data-list {
        list-style: none;
        padding-left: 0;
        margin-top: 10px;
    }
    .data-list li {
        font-size: 13.5px;
        color: #475569;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    .data-list i {
        color: #0ea5e9;
        margin-right: 10px;
        width: 16px;
        text-align: center;
    }

    /* Profile Cards (Tim Pengembang) */
    .profile-card-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .profile-card-container:hover {
        transform: translateY(-6px);
        border-color: #38bdf8; /* Garis pinggir biru saat disentuh mouse */
    }
    .p-name {
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .p-role {
        font-size: 13px;
        font-weight: 600;
        color: #0ea5e9;
        margin-bottom: 12px;
    }
    .p-desc {
        font-size: 12.5px;
        color: #64748b;
        line-height: 1.5;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR CONTENT (Navigasi Kustom 3 Menu Utama)
# ==============================================================================
with st.sidebar:
    st.markdown("## 🛒 Shoppers Portal")
    st.markdown("<p style='color: #94a3b8; font-size: 14px;'>Portal analisis data transaksi e-commerce tingkat lanjut.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📌 Menu Utama")
    
    # 1. Tombol Menu Home (Mengarah ke App.py)
    st.page_link("App.py", label="Home App", icon="🏠")
    
    # 2. Tombol Menu Prediksi Belanja
    if os.path.exists("pages/1_Prediksi_Belanja.py"):
        st.page_link("pages/1_Prediksi_Belanja.py", label="Prediksi Belanja", icon="🛒")
        
    # 3. Tombol Menu Evaluasi Model
    # PENTING: Ubah teks "pages/2_Evaluasi_Model.py" di bawah jika nama file Anda berbeda!
    if os.path.exists("pages/2_Evaluasi_Model.py"):
        st.page_link("pages/2_Evaluasi_Model.py", label="Evaluasi Model", icon="📊")

    st.markdown("---")
    st.success("🟢 Sistem berjalan optimal")
    st.info("💡 Model AI aktif dengan threshold ketat 92%.")

# ==============================================================================
# 1. HERO SECTION (BANNER UTAMA)
# ==============================================================================
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Shoppers Predictor Apps v2.0</div>
        <div class="hero-subtitle">Industrial-Grade Analytics for E-Commerce Transaction Validity & Risk Mitigation</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. EXECUTIVE SUMMARY & DATABASE ARCHITECTURE
# ==============================================================================
st.markdown("<div class='section-header'>Executive Summary & Data Architecture</div>", unsafe_allow_html=True)

col_db1, col_db2, col_db3 = st.columns([1.2, 1, 1], gap="medium")

with col_db1:
    st.markdown("""
        <div class="consulting-card">
            <span class="badge-blue">Dataset Overview</span>
            <h4 style="margin: 10px 0; font-weight: 700; color: #0f172a;">📦 Database Specification</h4>
            <p style="font-size: 13.5px; color: #64748b; line-height: 1.6;">
                Database utama memuat total <b>20.653 baris data riwayat transaksi</b> belanja dari lapangan dengan karakteristik ketimpangan kelas target (Highly Imbalanced Data) yang sangat kontras:
            </p>
            <ul class="data-list">
                <li><i class="fas fa-database"></i> <b>Total Records:</b> 20.653 baris data</li>
                <li><i class="fas fa-check-circle" style="color: #10b981;"></i> <b>Kelas Sukses (Delivered):</b> 20.471 baris</li>
                <li><i class="fas fa-times-circle" style="color: #ef4444;"></i> <b>Kelas Gagal (Cancelled):</b> 182 baris</li>
                <li><i class="fas fa-balance-scale"></i> <b>Balancing Teknik:</b> SMOTE (Data Training)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_db2:
    st.markdown("""
        <div class="consulting-card">
            <span class="badge-blue">Feature Engineering</span>
            <h4 style="margin: 10px 0; font-weight: 700; color: #0f172a;">⚙️ Arsitektur 6 Fitur</h4>
            <p style="font-size: 13.5px; color: #64748b; line-height: 1.6;">
                Sistem mengisolasi 6 parameter operasional murni angka dari database untuk memproses pemodelan secara objektif:
            </p>
            <ul class="data-list">
                <li><i class="fas fa-route"></i> <b>Distance_Num:</b> Jarak kurir (Maks 30km)</li>
                <li><i class="fas fa-file-invoice-dollar"></i> <b>Bill subtotal:</b> Harga bruto</li>
                <li><i class="fas fa-box"></i> <b>Packaging:</b> Biaya kemasan</li>
                <li><i class="fas fa-tags"></i> <b>Discounts:</b> Potongan harga</li>
                <li><i class="fas fa-calculator"></i> <b>Total:</b> Akumulasi bayar</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_db3:
    st.markdown("""
        <div class="consulting-card">
            <span class="badge-blue">Business Objective</span>
            <h4 style="margin: 10px 0; font-weight: 700; color: #0f172a;">🎯 Target Variabel</h4>
            <p style="font-size: 13.5px; color: #475569; line-height: 1.6;">
                Isi dari target biner yang diprediksi merujuk pada konversi kolom status pesanan ke angka mutlak:
            </p>
            <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #0284c7;">
                <p style="font-size: 13px; margin: 0; color: #0f172a;"><b>[1] Delivered:</b><br>Transaksi valid, aman, & sukses.</p>
            </div>
            <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin-top: 10px; border-left: 4px solid #ef4444;">
                <p style="font-size: 13px; margin: 0; color: #0f172a;"><b>[0] Cancelled:</b><br>Transaksi berisiko/fiktif.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. GLOBAL PERFORMANCE EVALUATION
# ==============================================================================
st.markdown("<div class='section-header'>Global Performance Evaluation</div>", unsafe_allow_html=True)

col_ev1, col_ev2 = st.columns([1, 1.8], gap="medium")

with col_ev1:
    st.markdown("""
    <div class="consulting-card">
        <h5 style="color: #0f172a; font-weight: 700; margin-bottom: 15px; font-size: 18px;">
            <i class="fas fa-chart-line" style="color:#0ea5e9; margin-right: 8px;"></i> Recall Priority Analysis
        </h5>
        <p style="font-size: 14px; color: #475569; line-height: 1.6; margin: 0;">
            Dalam kasus klasifikasi ketimpangan data belanja ini, fokus analisis kami dipusatkan pada metrik <b>Recall (Sensitivitas)</b>, bukan akurasi standar belaka.<br><br>
            Recall yang tinggi menjamin sistem mampu mendeteksi sebanyak mungkin transaksi yang berpotensi gagal/batal. 
            Jika nilai Recall lemah, sistem akan meloloskan pesanan palsu ke kurir, yang berakibat pada kerugian finansial nyata.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_ev2:
    # Memuat data leaderboard
    path_leaderboard = os.path.join('data', 'leaderboard_performa.csv')
    if os.path.exists(path_leaderboard):
        df_lb = pd.read_csv(path_leaderboard)
        df_lb.columns = ['Machine Learning Model', 'Accuracy (%)', 'Precision (%)', 'Recall (%)', 'F1-Score (%)']
        
        try:
            styled_df = df_lb.style.background_gradient(cmap='Blues', subset=['Accuracy (%)', 'Precision (%)', 'Recall (%)', 'F1-Score (%)']).format(precision=2)
            st.markdown("<p style='font-weight: 600; color: #0f172a; margin-bottom: 10px;'>📊 Model Metrics Comparison Matrix (Data Uji Murni)</p>", unsafe_allow_html=True)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        except Exception:
            st.markdown("<p style='font-weight: 600; color: #0f172a; margin-bottom: 10px;'>📊 Model Metrics Comparison Matrix (Data Uji Murni)</p>", unsafe_allow_html=True)
            st.dataframe(df_lb, use_container_width=True, hide_index=True)
    else:
        st.warning("📊 File 'data/leaderboard_performa.csv' belum ditemukan. Pastikan data sudah ada!")

# ==============================================================================
# 4. TEORI JALUR 4 MODEL MACHINE LEARNING
# ==============================================================================
st.markdown("<div class='section-header'>Arsitektur & Teori Core Algoritma Klasifikasi</div>", unsafe_allow_html=True)

col_mod1, col_mod2, col_mod3, col_mod4 = st.columns(4, gap="small")

with col_mod1:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #0284c7;">
            <div style="font-weight:700; font-size:16px; color:#0f172a; margin-bottom:10px;">1. K-Nearest Neighbors</div>
            <p style="font-size:13px; color: #475569; line-height: 1.5;">
                <b>Instance-Based Learning:</b> Mengklasifikasikan objek transaksi baru berdasarkan kedekatan klaster spasial (<em>Euclidean distance</em>) terhadap 5 data tetangga terdekat.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_mod2:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #10b981;">
            <div style="font-weight:700; font-size:16px; color:#0f172a; margin-bottom:10px;">2. Decision Tree</div>
            <p style="font-size:13px; color: #475569; line-height: 1.5;">
                <b>Hierarchical Split:</b> Memetakan diagram pohon keputusan terstruktur menggunakan pemisahan nilai indeks ketidakmurnian (<em>Gini Impurity</em>).
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_mod3:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #f59e0b;">
            <div style="font-weight:700; font-size:16px; color:#0f172a; margin-bottom:10px;">3. Support Vector Machine</div>
            <p style="font-size:13px; color: #475569; line-height: 1.5;">
                <b>Hyperplane:</b> Memisahkan ruang dimensi data secara optimal dengan batas margin terbesar menggunakan bantuan fungsi <em>Kernel RBF</em>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col_mod4:
    st.markdown("""
        <div class="premium-card" style="border-top: 4px solid #8b5cf6;">
            <div style="font-weight:700; font-size:16px; color:#0f172a; margin-bottom:10px;">4. Neural Network (MLP)</div>
            <p style="font-size:13px; color: #475569; line-height: 1.5;">
                <b>Multi-Layer Perceptron:</b> Memodelkan interaksi sinyal data non-linear lewat interkoneksi 2 hidden layer menggunakan optimasi rambatan balik.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. STRUKTUR TIM PENGEMBANG & SPESIALISASI
# ==============================================================================
st.markdown("<div class='section-header'>Struktur Pengembang & Spesialisasi Model</div>", unsafe_allow_html=True)

col_team1, col_team2, col_team3, col_team4 = st.columns(4, gap="small")

team_data = [
    {"name": "Ayesha Al Sidiq", "role": "SVM Specialist", "desc": "Fokus kalkulasi penemuan hyperplane optimal, penyelarasan hyperparameter, dan probabilitas."},
    {"name": "Saskia Naila Sagita", "role": "KNN Specialist", "desc": "Visualisasi sebaran metrik kedekatan klaster data transaksi serta validasi pembobotan."},
    {"name": "Fahreza Azhar Ramadhan", "role": "DT Specialist", "desc": "Analisis kriteria penentuan nodus akar keputusan dan pencegahan over-parameterisasi."},
    {"name": "Aninda Irfani", "role": "NN Specialist", "desc": "Penyusunan bobot bias arsitektur multi-layer neural network & minimalisasi loss error."}
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
    <div class="premium-card" style="background: #f8fafc; border-left: 6px solid #0f172a; padding: 25px;">
        <h4 style="margin-top:0; color:#0f172a; font-size:16px;">🛡️ Mekanisme Penilaian Ketat (Probability Thresholding 92%)</h4>
        <p style="color: #475569; font-size: 14px; margin: 10px 0 0 0; line-height: 1.6;">
            Karena distribusi dataset awal bersifat timpang ekstrem, platform analitik ini mengabaikan batas toleransi bawaan default model (50%). 
            Sistem mengunci regulasi ketat: Apabila tingkat keyakinan model untuk kelas sukses bernilai di bawah <b>92.00%</b>, 
            sistem otomatis membatalkan transaksi dan mengubah keputusan menjadi status risiko tinggi (<strong>Cancelled/Missed Order</strong>). 
            Hal ini memberikan lapisan keamanan preventif bagi merchant dari ancaman pesanan fiktif.
        </p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<hr style='margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px; font-weight:500; margin-bottom: 30px;'>Proyek Praktikum Dasar Ilmu Data 2026 • Kurikulum Diploma (D3) Sistem Informasi • Telkom University</p>", unsafe_allow_html=True)