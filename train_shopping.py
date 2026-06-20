import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline

# 1. Load Data dari Folder data/
# Memastikan sistem membaca dataset asli dari subfolder 'data'
path_data = os.path.join('data', 'order_history_kaggle_data.xlsx - order_history_kaggle_data.csv')
df_shop = pd.read_csv(path_data)

print(f"Berhasil memuat data mentah asli: {df_shop.shape[0]} baris.")

# 2. Preprocessing & Labeling Biner Target
# 1 = Delivered (Sukses/Membeli), 0 = Selain itu (Cancelled, Missed, dll)
df_shop['Target_Beli'] = df_shop['Order Status'].apply(lambda x: 1 if str(x).strip() == 'Delivered' else 0)

# Membersihkan string unit jarak 'km' agar aman menjadi numerik float
df_shop['Distance_Num'] = (
    df_shop['Distance']
    .astype(str)
    .str.replace('km', '', case=False)
    .str.strip()
)
df_shop['Distance_Num'] = pd.to_numeric(df_shop['Distance_Num'], errors='coerce')

# 3. Penentuan Fitur & Pembersihan Baris Kosong
fitur_pilihan = ['Distance_Num', 'Bill subtotal', 'Packaging charges', 'Total']
df_clean = df_shop[fitur_pilihan + ['Target_Beli']].dropna()

# Mengonversi seluruh nilai prediktor menjadi float murni
for col in fitur_pilihan:
    df_clean[col] = df_clean[col].astype(float)

X = df_clean[fitur_pilihan]
y = df_clean['Target_Beli']

# 4. Splitting Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Mengatasi Imbalance Data Menggunakan SMOTE pada Training Set
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print(f"Data setelah penyeimbangan SMOTE: {X_train_res.shape[0]} baris.")

# 6. Melatih Multi-Model & Menyimpannya ke folder models/
os.makedirs('models', exist_ok=True)

# Definisikan 4 arsitektur model berdasarkan konfigurasi terbaik kelompokmu
models_dict = {
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=3, metric='manhattan', weights='distance'),
    'Decision Tree': DecisionTreeClassifier(criterion='entropy', max_depth=5, min_samples_leaf=0.1, random_state=42),
    'Support Vector Machine': SVC(kernel='rbf', probability=True, random_state=42),
    'Neural Network': MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
}

print("\n--- Memulai Proses Pelatihan Multi-Model ---")
for name, model in models_dict.items():
    # Bungkus standarisasi data dan model ke dalam pipeline tunggal
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', model)
    ])
    
    # Latih model
    pipeline.fit(X_train_res, y_train_res)
    
    # Konversi nama file agar aman (spasi jadi underscore, lowercase)
    filename = f"model_{name.lower().replace(' ', '_').replace('-', '_')}.pkl"
    joblib.dump(pipeline, os.path.join('models', filename))
    print(f"✔ {name} berhasil dilatih & disimpan sebagai 'models/{filename}'")

print("\n" + "="*50)
print("PROSES SELESAI: Semua arsitektur model siap digunakan!")
print("="*50)