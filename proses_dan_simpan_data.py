import pandas as pd
import os
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

print("=== MEMULAI PEMBROSESAN DATA SESUAI STRUKTUR ===")

# 1. Deteksi Path File Mentah secara Fleksibel
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
    files_di_root = [f for f in os.listdir('.') if f.endswith('.csv')]
    if files_di_root:
        path_mentah = files_di_root[0]
    elif os.path.exists('data'):
        files_di_data = [os.path.join('data', f) for f in os.listdir('data') if f.endswith('.csv')]
        if files_di_data:
            path_mentah = files_di_data[0]

if not path_mentah:
    raise FileNotFoundError("❌ File data mentah tidak ditemukan. Pastikan file CSV ada di folder proyek atau di dalam folder 'data/'!")

# Load Data Mentah
df_shop = pd.read_csv(path_mentah)
print(f"✅ Berhasil memuat data mentah: {df_shop.shape[0]} baris.")

# 2. Preprocessing Awal (Sama seperti alur kelompokmu)
df_shop['Target_Beli'] = df_shop['Order Status'].apply(lambda x: 1 if str(x).strip() == 'Delivered' else 0)

df_shop['Distance_Num'] = (
    df_shop['Distance']
    .astype(str)
    .str.replace('km', '', case=False)
    .str.strip()
)
df_shop['Distance_Num'] = pd.to_numeric(df_shop['Distance_Num'], errors='coerce')

fitur_pilihan = ['Distance_Num', 'Bill subtotal', 'Packaging charges', 'Total']
df_clean = df_shop[fitur_pilihan + ['Target_Beli']].dropna()

for col in fitur_pilihan:
    df_clean[col] = df_clean[col].astype(float)

X = df_clean[fitur_pilihan]
y = df_clean['Target_Beli']

# 3. STRUKTUR DATA SPLIT (Persis seperti di screenshot kamu)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. PROSES SMOTE PADA DATA TRAIN
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# 5. RECONSTRUCT / GABUNGKAN KEMBALI DATA SETELAH SMOTE (Sesuai cara di screenshot)
# Membuat DataFrame dari hasil SMOTE
df_X_train_res = pd.DataFrame(X_train_res, columns=fitur_pilihan)
df_y_train_res = pd.DataFrame(y_train_res, columns=['Target_Beli'])

# Menggabungkan fitur dan target menggunakan pd.concat secara horizontal (axis=1)
df_train_matang = pd.concat([df_X_train_res, df_y_train_res], axis=1)

# Tambahkan kolom keterangan teks agar mudah dibaca di CSV/Streamlit nanti
df_train_matang['Status_Transaksi'] = df_train_matang['Target_Beli'].map({
    1: 'Sukses (Delivered)', 
    0: 'Gagal (Cancelled/Missed)'
})

print(f"📈 Ukuran Training Data setelah SMOTE & Concat: {df_train_matang.shape[0]} baris.")

# 6. SIMPAN HASIL RECONSTRUCT KE FOLDER DATA
os.makedirs('data', exist_ok=True)
path_hasil = os.path.join('data', 'shoppers_data_matang_final.csv')
df_train_matang.to_csv(path_hasil, index=False)

print("\n" + "="*50)
print(f"🎉 SUKSES SELESAI!")
print(f"File matang terstruktur disimpan di: '{path_hasil}'")
print(f"Total data bersih siap pakai: {df_train_matang.shape[0]} baris.")
print("="*50)