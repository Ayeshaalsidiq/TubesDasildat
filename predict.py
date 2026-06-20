import sys
import os
import joblib
import pandas as pd
import json
import sqlite3
import warnings

# ==============================================================================
# SCRIPT UTAMA UNTUK PREDIKSI MACHINE LEARNING (BACKEND)
# Script ini dipanggil oleh PHP. Menerima file CSV, membersihkannya, 
# lalu memasukkannya ke dalam 4 model (Decision Tree, KNN, Neural Network, SVM).
# ==============================================================================

# Menyembunyikan peringatan/warning merah dari Python agar tidak mengotori output JSON
warnings.filterwarnings('ignore')

def main():
    # Menentukan folder asal model
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if dir_path != '':
        dir_path = dir_path + '/'
        
    # Validasi argumen input
    if len(sys.argv) < 2:
        print("Error: Path dataset input wajib diisi.")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    # Model files map
    model_files = {
        'dt': 'shopping_decision_tree_classification_model.sav',
        'knn': 'shopping_knn_classification_model.sav',
        'nn': 'shopping_neural_network_classification_model.sav',
        'svm': 'shopping_svm_classification_model.sav'
    }
    
    scaler_shopping_dir = dir_path + 'model/scaler_shopping.sav'
    
    # Validasi keberadaan file model & scaler
    for m_type, filename in model_files.items():
        m_path = dir_path + 'model/' + filename
        if not os.path.exists(m_path):
            print(f"Error: File model tidak ditemukan di '{m_path}'.\nSilakan unduh file model .sav dari Google Drive Anda dan masukkan ke folder tersebut.")
            sys.exit(1)
            
    if not os.path.exists(scaler_shopping_dir):
        print(f"Error: File scaler tidak ditemukan di '{scaler_shopping_dir}'.\nSilakan unduh file scaler_shopping.sav dari Google Drive Anda dan masukkan ke folder tersebut.")
        sys.exit(1)
        
    # Memuat semua model dan scaler
    try:
        models = {}
        for m_type, filename in model_files.items():
            models[m_type] = joblib.load(dir_path + 'model/' + filename)
        scaler_shopping = joblib.load(scaler_shopping_dir)
    except Exception as e:
        print(f"Error saat memuat model/scaler: {e}")
        sys.exit(1)
        
    # Validasi file input
    if not os.path.exists(input_file):
        print(f"Error: File input '{input_file}' tidak ditemukan.")
        sys.exit(1)
        
    # Membaca file input (CSV atau Excel)
    ext = os.path.splitext(input_file)[1].lower()
    try:
        if ext in ['.xlsx', '.xls']:
            data_file = pd.read_excel(input_file)
        else:
            data_file = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error saat membaca file data ({ext}): {e}\nPastikan library 'openpyxl' terinstall jika membaca Excel (pip install openpyxl).")
        sys.exit(1)
        
    # Prapemrosesan Data
    try:
        df_processed = data_file.copy()
        
        # Hapus kolom label target 'Revenue' jika ada di file upload
        if 'Revenue' in df_processed.columns:
            df_processed = df_processed.drop('Revenue', axis=1)
            
        # [PROSES LABEL ENCODING]
        # Mengubah data yang berupa teks menjadi angka agar bisa dibaca oleh matematika model AI.
        
        # 1. Map Kolom Month (Bulan)
        # Meniru proses LabelEncoder yang dilakukan di file Jupyter Notebook.
        month_map = {
            'Aug': 0, 'Dec': 1, 'Feb': 2, 'Jul': 3, 'June': 4,
            'Mar': 5, 'May': 6, 'Nov': 7, 'Oct': 8, 'Sep': 9
        }
        
        def map_month(val):
            if isinstance(val, str):
                return month_map.get(val.strip(), 6) # default ke May (6) jika tidak cocok
            try:
                return int(float(val))
            except:
                return 6
                
        df_processed['Month'] = df_processed['Month'].apply(map_month)
            
        # 2. Map Kolom VisitorType
        visit_map = {
            'New_Visitor': 0, 'Other': 1, 'Returning_Visitor': 2
        }
        
        def map_visitor(val):
            if isinstance(val, str):
                return visit_map.get(val.strip(), 2) # default ke Returning_Visitor (2) jika tidak cocok
            try:
                return int(float(val))
            except:
                return 2
                
        df_processed['VisitorType'] = df_processed['VisitorType'].apply(map_visitor)
            
        # 3. Map Kolom Weekend (True/False -> 1/0)
        def map_weekend(val):
            if isinstance(val, str):
                val_upper = val.strip().upper()
                if val_upper in ['TRUE', '1', 'YES', 'Y']:
                    return 1
                return 0
            if isinstance(val, bool):
                return 1 if val else 0
            try:
                return int(float(val))
            except:
                return 0
                
        df_processed['Weekend'] = df_processed['Weekend'].apply(map_weekend)
            
        # Susun urutan fitur yang sesuai dengan format training
        features_cols = [
            'Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
            'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues',
            'SpecialDay', 'Month', 'OperatingSystems', 'Browser', 'Region', 'TrafficType', 'VisitorType', 'Weekend'
        ]
        
        # Tambahkan nilai default 0 jika ada kolom fitur yang tidak terunggah di CSV
        for col in features_cols:
            if col not in df_processed.columns:
                df_processed[col] = 0
                
        # Konversi semua tipe data kolom fitur menjadi float/numeric agar aman untuk scaler
        for col in features_cols:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce').fillna(0)
            
        # Ambil hanya kolom fitur yang sudah ditentukan urutannya
        df_features = df_processed[features_cols]
        
        # [PROSES SCALING DATA]
        # Meratakan skala angka (misalnya durasi waktu yang mencapai ribuan) agar seimbang dengan angka kecil.
        # Proses ini mutlak diperlukan untuk model jarak (seperti KNN & SVM) dan Neural Network.
        # Kita menggunakan 'scaler_shopping.sav' hasil pelatihan dari Jupyter Notebook.
        scaled_feature = scaler_shopping.transform(df_features)
        
        # [PROSES PREDIKSI]
        # Jalankan prediksi (menebak 1/Purchase atau 0/No Purchase) menggunakan keempat model yang sudah dimuat.
        preds = {}
        for m_key, model_obj in models.items():
            # Memasukkan data yang sudah di-scale (scaled_feature) ke otak model
            preds[m_key] = model_obj.predict(scaled_feature)
            
        # Gabungkan hasil prediksi ke dataset asli
        df_output = data_file.copy()
        
        # Tambahkan kolom prediksi masing-masing model
        df_output['Prediksi_DT'] = preds['dt']
        df_output['Prediksi_KNN'] = preds['knn']
        df_output['Prediksi_NN'] = preds['nn']
        df_output['Prediksi_SVM'] = preds['svm']
        
        # Tambahkan juga label teks untuk kemudahan pembacaan
        df_output['Label_DT'] = df_output['Prediksi_DT'].map({1: 'Purchase', 0: 'No Purchase'})
        df_output['Label_KNN'] = df_output['Prediksi_KNN'].map({1: 'Purchase', 0: 'No Purchase'})
        df_output['Label_NN'] = df_output['Prediksi_NN'].map({1: 'Purchase', 0: 'No Purchase'})
        df_output['Label_SVM'] = df_output['Prediksi_SVM'].map({1: 'Purchase', 0: 'No Purchase'})
        
        # 1. Tulis hasil penggabungan ke database SQLite
        db_path = dir_path + 'database.db'
        try:
            conn = sqlite3.connect(db_path)
            # Simpan dataframe hasil ke tabel hasil_prediksi di database SQLite (Replace jika sudah ada)
            df_output.to_sql('hasil_prediksi', conn, if_exists='replace', index=False)
            conn.close()
        except Exception as db_err:
            print(f"Error saat menulis ke database SQLite: {db_err}")
            
        # 2. Menyimpan ke file hasil (hasil.csv dan hasil.xlsx)
        df_output.to_csv('hasil.csv', index=False)
        try:
            df_output.to_excel('hasil.xlsx', index=False)
        except Exception:
            pass # abaikan jika openpyxl belum terinstall
            
        # Output data statistik untuk ditangkap oleh shell_exec PHP
        total = len(data_file)
        
        # Hitung statistik masing-masing model
        stats = {
            "total": int(total),
            "dt": {
                "purchase": int(sum(preds['dt'])),
                "no_purchase": int(total - sum(preds['dt']))
            },
            "knn": {
                "purchase": int(sum(preds['knn'])),
                "no_purchase": int(total - sum(preds['knn']))
            },
            "nn": {
                "purchase": int(sum(preds['nn'])),
                "no_purchase": int(total - sum(preds['nn']))
            },
            "svm": {
                "purchase": int(sum(preds['svm'])),
                "no_purchase": int(total - sum(preds['svm']))
            }
        }
        
        print("JSON_START")
        print(json.dumps(stats))
        print("JSON_END")
        
    except Exception as e:
        print(f"Error saat preprocessing/prediksi: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
