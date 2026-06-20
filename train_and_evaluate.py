import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

print("=== RE-TRAINING MULTI-MODEL DENGAN SINKRONISASI METRIK COLAB ===")

# 1. Deteksi Jalur File Dataset Mentah Asli
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
    raise FileNotFoundError("❌ File data mentah asli tidak ditemukan. Pastikan file CSV ada di proyek!")

# Load Data Mentah
df_shop = pd.read_csv(path_mentah)
print(f"✅ Berhasil memuat data mentah asli: {df_shop.shape[0]} baris.")

# 2. Preprocessing & Pembuatan Label Target Biner
df_shop['Target_Beli'] = df_shop['Order Status'].apply(lambda x: 1 if str(x).strip() == 'Delivered' else 0)

# Pembersihan string unit jarak 'km' menjadi numerik murni
df_shop['Distance_Num'] = pd.to_numeric(
    df_shop['Distance'].astype(str).str.replace('km', '', case=False).str.strip(), 
    errors='coerce'
)

# 3. Spesifikasi 6 Fitur Analitis Berdasarkan Struktur Database
fitur_pilihan = [
    'Distance_Num', 'Bill subtotal', 'Packaging charges', 'Total',
    'Restaurant discount (Promo)', 'Gold discount'
]

# Konversi semua kolom fitur menjadi numerik angka murni
for col in fitur_pilihan:
    df_shop[col] = pd.to_numeric(df_shop[col], errors='coerce')

# Filter data sampah / baris tidak realistis (Total kosong dan Jarak kosong)
df_filtered = df_shop[(df_shop['Total'] > 0) & (df_shop['Distance_Num'] > 0)].dropna(subset=['Target_Beli'])

X = df_filtered[fitur_pilihan].fillna(0.0).astype(float)
y = df_filtered['Target_Beli'].astype(int)

print(f"📊 Distribusi Database Asli:\n{y.value_counts()}")

# 4. Splitting Data Uji & Data Latih (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Penyeimbangan Data Menggunakan SMOTE Eksklusif pada Data Training
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print(f"📈 Penyeimbangan Selesai. Volume Latih setelah SMOTE: {pd.Series(y_train_res).value_counts().to_dict()}")

# 6. Definisi Parameter Terbaik dari 4 Arsitektur Model (Kunci Fitur Probabilitas)
models_dict = {
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='uniform'),
    'Decision Tree': DecisionTreeClassifier(criterion='gini', max_depth=6, min_samples_leaf=5, random_state=42),
    'Support Vector Machine': SVC(kernel='rbf', C=1.0, probability=True, random_state=42), # probability=True Wajib ada
    'Neural Network': MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=500, activation='logistic', random_state=42)
}

performa_list = []
os.makedirs('models', exist_ok=True)

print("\n--- Memulai Proses Pelatihan Multi-Model ---")

# 7. Loop Pelatihan, Evaluasi Metrik Komprehensif, dan Penyimpanan Model
for name, model in models_dict.items():
    # Menggabungkan Standarisasi Skala (StandardScaler) ke dalam Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', model)
    ])
    
    # Latih model menggunakan data training hasil SMOTE
    pipeline.fit(X_train_res, y_train_res)
    
    # Prediksi menggunakan data test asli murni
    y_pred = pipeline.predict(X_test)
    
    # === PERBAIKAN METRIK: Sinkron dengan Weighted Average dari Report Colab ===
    acc = accuracy_score(y_test, y_pred)
    pre = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1  = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Masukkan data ke list dengan pembulatan persentase yang rapi
    performa_list.append({
        'Machine Learning Model': name,
        'Accuracy': round(acc * 100, 2),
        'Precision': round(pre * 100, 2),
        'Recall': round(rec * 100, 2),
        'F1-Score': round(f1 * 100, 2)
    })
    
    # Simpan file biner model pintar .pkl
    filename = f"model_{name.lower().replace(' ', '_').replace('-', '_')}.pkl"
    joblib.dump(pipeline, os.path.join('models', filename))
    print(f"✔ {name} sukses dilatih & disimpan sebagai 'models/{filename}'")

# 8. Cetak & Export Tabel Evaluasi Global ke CSV agar dibaca oleh App.py
df_leaderboard = pd.DataFrame(performa_list)
os.makedirs('data', exist_ok=True)
df_leaderboard.to_csv(os.path.join('data', 'leaderboard_performa.csv'), index=False)

print("\n" + "="*70)
print("🏆 GLOBAL PERFORMANCE EVALUATION LEADERBOARD (SINKRON COLAB) 🏆")
print("="*70)
print(df_leaderboard.to_string(index=False))
print("="*70)
print("📄 Sukses mengekspor matriks perbandingan ke 'data/leaderboard_performa.csv'")