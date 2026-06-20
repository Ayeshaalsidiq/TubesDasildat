<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload File & Prediksi (Dark Mode)</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Load Chart.js from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #6366F1; /* Indigo 500 */
            --primary-hover: #818CF8; /* Indigo 400 */
            --bg-grad: #0F172A; /* Slate 900 (Deep Dark) */
            --card-bg: #1E293B; /* Slate 800 */
            --text-dark: #F8FAFC; /* Slate 50 */
            --text-light: #94A3B8; /* Slate 400 */
            --success: #10B981; /* Emerald 500 */
            --danger: #EF4444; /* Red 500 */
            --border: #334155; /* Slate 700 */
            --input-bg: #0F172A; /* Slate 900 */
            --results-bg: #0F172A; /* Slate 900 */
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-grad);
            color: var(--text-dark);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
        }

        .container {
            width: 100%;
            max-width: 950px;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
        }

        header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            color: #60A5FA; /* Light Blue for dark mode readability */
            margin-bottom: 0.5rem;
        }

        header p {
            color: var(--text-light);
            font-size: 1rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border);
            padding: 2.5rem;
            margin-bottom: 2rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-dark);
        }

        .select-style, .file-input {
            width: 100%;
            padding: 0.8rem 1rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--input-bg);
            color: var(--text-dark);
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .select-style:focus, .file-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .select-style option {
            background-color: var(--input-bg);
            color: var(--text-dark);
        }

        /* Styling upload file input */
        .file-input::file-selector-button {
            background: #334155;
            color: white;
            border: none;
            padding: 0.4rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            margin-right: 1rem;
            font-weight: 600;
            transition: background 0.2s ease;
        }

        .file-input::file-selector-button:hover {
            background: #475569;
        }

        .btn-submit {
            display: block;
            width: 100%;
            background: var(--primary);
            color: white;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
            text-align: center;
        }

        .btn-submit:hover {
            background: var(--primary-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3);
        }

        .results {
            background: var(--results-bg);
            border-radius: 15px;
            border: 1px solid var(--border);
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .results h2 {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.8rem;
            color: var(--text-dark);
        }

        /* Dashboard layout for results */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .chart-box {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid var(--border);
            max-height: 280px;
        }

        .stats-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 1rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 1rem 1.2rem;
            border-radius: 10px;
            border-left: 5px solid #3B82F6; /* Blue for total */
        }

        .stat-card.purchase {
            border-left-color: var(--success); /* Green for purchase */
        }

        .stat-card.no-purchase {
            border-left-color: var(--danger); /* Red for no purchase */
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-light);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stat-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--text-dark);
            margin: 0.2rem 0;
        }

        .stat-desc {
            font-size: 0.85rem;
            color: var(--text-light);
        }

        .results-summary {
            background: var(--input-bg);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            font-family: monospace;
            font-size: 0.95rem;
            white-space: pre-wrap;
            border-left: 4px solid var(--primary);
        }

        .download-box {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--card-bg);
            padding: 1.2rem 1.5rem;
            border-radius: 10px;
            margin-top: 1.5rem;
            gap: 1rem;
            border: 1px solid var(--border);
        }

        .download-buttons {
            display: flex;
            gap: 0.8rem;
        }

        .download-link {
            background: var(--success);
            color: white;
            text-decoration: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);
            transition: all 0.2s ease;
        }

        .download-link.excel-btn {
            background: #217346; /* Excel green */
            box-shadow: 0 4px 10px rgba(33, 115, 70, 0.2);
        }

        .download-link:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Online Shoppers Intent Predictor</h1>
            <p>Deployment Model Machine Learning Berbasis Web untuk Klasifikasi Minat Beli Pengunjung</p>
        </header>

        <div class="card">
            <form action="" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="model">Pilih Model Machine Learning:</label>
                    <select name="model" id="model" class="select-style">
                        <option value="dt" <?php if(isset($_POST['model']) && $_POST['model'] == 'dt') echo 'selected'; ?>>Decision Tree Classifier (HPO)</option>
                        <option value="knn" <?php if(isset($_POST['model']) && $_POST['model'] == 'knn') echo 'selected'; ?>>K-Nearest Neighbors (KNN) Classifier (HPO)</option>
                        <option value="nn" <?php if(isset($_POST['model']) && $_POST['model'] == 'nn') echo 'selected'; ?>>Neural Network (MLP) Classifier (HPO)</option>
                        <option value="svm" <?php if(isset($_POST['model']) && $_POST['model'] == 'svm') echo 'selected'; ?>>Support Vector Machine (SVM) Classifier (HPO)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="berkas">Pilih file dataset (Format CSV atau Excel .xlsx/.xls):</label>
                    <input type="file" name="berkas" id="berkas" class="file-input" required accept=".csv, .xlsx, .xls" />
                </div>

                <input type="submit" name="upload" value="upload" class="btn-submit" />
            </form>

            <?php
            function panggil_model($input_file_path, $model){
                // Jalankan script Python dengan argumen path file dan model type
                $perintah = "python C:\\laragon\\www\\shoppers_v2\\predict.py " . escapeshellarg($input_file_path) . " " . escapeshellarg($model) . " 2>&1";
                $output = shell_exec($perintah); 
                return $output; 
            }
            ?>

            <?php
            if (isset($_POST["upload"])) {
                $model = $_POST["model"];
                $namaOriginal = $_FILES['berkas']['name'];
                $ext = pathinfo($namaOriginal, PATHINFO_EXTENSION);
                $namaFile = 'dataset.' . $ext;
                
                // Tentukan lokasi file akan dipindahkan
                $dirUpload = "dataset/";
                if (!file_exists($dirUpload)) {
                    mkdir($dirUpload, 0777, true);
                }
                
                $pathTujuan = $dirUpload . $namaFile;
                
                // Pindahkan file
                $terupload = move_uploaded_file($_FILES['berkas']['tmp_name'], $pathTujuan);
                
                if ($terupload) {
                    echo "<div class='results'>";
                    echo "<h2>Hasil Prediksi Model</h2>";
                    echo "Upload berhasil!<br/>";
                    echo "Link dataset: <a href='".$pathTujuan."' style='color: #60A5FA; text-decoration: underline;'>".$namaOriginal."</a><br/><br/>";
                    
                    // Panggil model machine learning
                    $hasil = panggil_model($pathTujuan, $model);
                    
                    if (empty($hasil) || strpos($hasil, 'Error') !== false) {
                        echo "<div class='results-summary' style='border-left-color: var(--danger); color: var(--danger);'>";
                        echo htmlspecialchars(empty($hasil) ? 'Error: Gagal menjalankan predict.py. Pastikan python terinstall di path komputer.' : $hasil);
                        echo "</div>";
                    } else {
                        // Pisahkan output teks log dengan JSON data
                        $parts = explode("JSON_START", $hasil);
                        
                        $json_str = "";
                        if (count($parts) > 1) {
                            $subparts = explode("JSON_END", $parts[1]);
                            $json_str = trim($subparts[0]);
                        }
                        
                        // Parse JSON
                        $stats = json_decode($json_str, true);
                        
                        if ($stats) {
                            $total = $stats['total'];
                            
                            // Ambil data sesuai model yang dipilih
                            $selected_model = isset($_POST['model']) ? $_POST['model'] : 'dt';
                            $model_stats = isset($stats[$selected_model]) ? $stats[$selected_model] : $stats['dt'];
                            
                            $purchase = $model_stats['purchase'];
                            $no_purchase = $model_stats['no_purchase'];
                            $purchase_pct = ($total > 0) ? round(($purchase / $total) * 100, 2) : 0;
                            $nopurchase_pct = ($total > 0) ? round(($no_purchase / $total) * 100, 2) : 0;
                            
                            // Tampilkan Dropdown Filter Bulan
                            echo "<div style='margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; background: var(--card-bg); padding: 1rem 1.5rem; border-radius: 10px; border: 1px solid var(--border);'>";
                            echo "<label for='monthFilter' style='font-weight: 600; color: var(--text-dark);'>Filter Berdasarkan Bulan:</label>";
                            echo "<select id='monthFilter' class='select-style' style='width: auto; min-width: 150px; padding: 0.5rem 1rem;'>";
                            echo "<option value=''>-- Semua Bulan --</option>";
                            
                            $unique_months = [];
                            $file_handle = fopen("hasil.csv", "r");
                            if ($file_handle !== FALSE) {
                                $csv_headers = fgetcsv($file_handle, 10000, ",");
                                if ($csv_headers !== FALSE) {
                                    $month_index = array_search('Month', $csv_headers);
                                    if ($month_index !== FALSE) {
                                        while (($row = fgetcsv($file_handle, 10000, ",")) !== FALSE) {
                                            if (isset($row[$month_index])) {
                                                $m = trim($row[$month_index]);
                                                if (!empty($m) && !in_array($m, $unique_months)) {
                                                    $unique_months[] = $m;
                                                }
                                            }
                                        }
                                    }
                                }
                                fclose($file_handle);
                            }
                            // Custom sort based on calendar months could be done, but alphabetical or as-is is fine.
                            // Let's preserve standard order from data or sort alphabetically
                            sort($unique_months);
                            foreach ($unique_months as $m) {
                                echo "<option value='" . htmlspecialchars($m) . "'>" . htmlspecialchars($m) . "</option>";
                            }
                            echo "</select>";
                            echo "</div>";

                            // Tampilkan Dashboard Visualisasi
                            echo "<div class='dashboard-grid'>";
                            
                            // Kiri: Statistik Cards
                            echo "<div class='stats-box'>";
                            echo "  <div class='stat-card'>";
                            echo "    <div class='stat-label'>Total Data Yang Diproses</div>";
                            echo "    <div class='stat-value' id='stat-total'>" . number_format($total) . " baris</div>";
                            echo "    <div class='stat-desc'>Sesi kunjungan shopper selesai dianalisis</div>";
                            echo "  </div>";
                            
                            echo "  <div class='stat-card purchase'>";
                            echo "    <div class='stat-label'>Prediksi Purchase (Akan Membeli)</div>";
                            echo "    <div class='stat-value' id='stat-purchase' style='color: var(--success);'>" . number_format($purchase) . "</div>";
                            echo "    <div class='stat-desc' id='desc-purchase'>Persentase: " . $purchase_pct . "% dari total pengunjung</div>";
                            echo "  </div>";
                            
                            echo "  <div class='stat-card no-purchase'>";
                            echo "    <div class='stat-label'>Prediksi No Purchase (Tidak Membeli)</div>";
                            echo "    <div class='stat-value' id='stat-nopurchase' style='color: var(--danger);'>" . number_format($no_purchase) . "</div>";
                            echo "    <div class='stat-desc' id='desc-nopurchase'>Persentase: " . $nopurchase_pct . "% dari total pengunjung</div>";
                            echo "  </div>";
                            echo "</div>";
                            
                            // Kanan: Pie Chart Canvas
                            echo "<div class='chart-box'>";
                            echo "  <canvas id='resultChart' width='250' height='250'></canvas>";
                            echo "</div>";
                            
                            echo "</div>"; // dashboard-grid
                            
                            // Script untuk inisialisasi Chart.js
                            echo "
                            <script>
                            document.addEventListener('DOMContentLoaded', function() {
                                var ctx = document.getElementById('resultChart').getContext('2d');
                                window.myChart = new Chart(ctx, {
                                    type: 'pie',
                                    data: {
                                        labels: ['Purchase (Akan Membeli)', 'No Purchase (Tidak Membeli)'],
                                        datasets: [{
                                            data: [" . $purchase . ", " . $no_purchase . "],
                                            backgroundColor: ['#10B981', '#EF4444'],
                                            borderWidth: 2,
                                            borderColor: '#1E293B'
                                        }]
                                    },
                                    options: {
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        plugins: {
                                            legend: {
                                                position: 'bottom',
                                                labels: {
                                                    boxWidth: 12,
                                                    font: { size: 11, family: 'Plus Jakarta Sans', weight: '600' },
                                                    color: '#94A3B8' /* Light labels for dark mode */
                                                }
                                            }
                                        }
                                    }
                                });
                            });
                            </script>
                            ";
                        }
                        
                        // Menampilkan link download file hasil prediksi dan info database
                        if (file_exists('hasil.csv')) {
                            echo "<div class='download-box' style='display: flex; flex-direction: column; align-items: flex-start; gap: 0.5rem;'>";
                            echo "  <span style='font-weight: 600; color: var(--text-dark);'>Database SQLite & File Hasil:</span>";
                            echo "  <span style='font-size: 0.85rem; color: var(--text-light);'>Semua hasil prediksi (DT, KNN, NN, SVM) telah digabungkan dan disimpan ke file database: <strong>database.db</strong> (tabel: <strong>hasil_prediksi</strong>).</span>";
                            echo "  <div class='download-buttons' style='margin-top: 0.5rem;'>";
                            echo "    <a href='hasil.csv' class='download-link' download>Unduh</a>";
                            if (file_exists('hasil.xlsx')) {
                                echo "    <a href='hasil.xlsx' class='download-link excel-btn' download>Unduh Excel</a>";
                            }
                            echo "</div>"; // End download-box

                            // TAMPILKAN TABEL DATA HASIL
                            echo "<div style='margin-top: 2rem; background: var(--card-bg); padding: 1.5rem; border-radius: 10px; border: 1px solid var(--border); overflow-x: auto;'>";
                            echo "<h3 style='margin-bottom: 1rem; color: var(--text-dark);'>Detail Data Hasil Prediksi</h3>";
                            echo "<table id='dataTableHasil' class='display' style='width:100%; color: var(--text-dark); font-size: 0.9rem; text-align: left; border-collapse: collapse;'>";
                            echo "<thead style='background-color: var(--input-bg); border-bottom: 2px solid var(--border);'><tr>";
                            
                            $file_handle = fopen("hasil.csv", "r");
                            if ($file_handle !== FALSE) {
                                // Baca header
                                $headers = fgetcsv($file_handle, 10000, ",");
                                if ($headers !== FALSE) {
                                    // Kolom yang ingin ditampilkan
                                    $target_cols = ['Administrative', 'ProductRelated', 'PageValues', 'Month', 'VisitorType', 'Weekend'];
                                    
                                    // Cari index untuk kolom target
                                    $col_indices = [];
                                    foreach ($target_cols as $tc) {
                                        $col_indices[$tc] = array_search($tc, $headers);
                                    }
                                    
                                    // Cari index untuk kolom 'Label' model yang dipilih
                                    $model_label_col = 'Label_' . strtoupper(isset($_POST['model']) ? $_POST['model'] : 'DT');
                                    $label_index = array_search($model_label_col, $headers);
                                    
                                    // Print th
                                    foreach ($target_cols as $tc) {
                                        echo "<th style='padding: 12px 10px; font-weight: 600; color: var(--text-dark);'>" . htmlspecialchars($tc) . "</th>";
                                    }
                                    echo "<th style='padding: 12px 10px; font-weight: 600; color: var(--text-dark);'>Hasil Prediksi</th>";
                                    
                                    echo "</tr></thead><tbody>";
                                    
                                    // Baca SEMUA baris
                                    while (($data = fgetcsv($file_handle, 10000, ",")) !== FALSE) {
                                        echo "<tr style='border-bottom: 1px solid var(--border);'>";
                                        
                                        // Print cell sesuai urutan target_cols
                                        foreach ($target_cols as $tc) {
                                            $idx = $col_indices[$tc];
                                            $val = ($idx !== false && isset($data[$idx])) ? $data[$idx] : '';
                                            echo "<td style='padding: 12px 10px;'>" . htmlspecialchars($val) . "</td>";
                                        }
                                        
                                        // Print Hasil Prediksi dengan Pill
                                        $label_val = ($label_index !== false && isset($data[$label_index])) ? $data[$label_index] : '';
                                        
                                        if (strtoupper($label_val) === 'PURCHASE' || strtoupper($label_val) === 'MEMBELI') {
                                            $pill_bg = 'rgba(16, 185, 129, 0.2)'; // Dark theme transparent green
                                            $pill_color = '#34D399'; // Light green text
                                            $pill_text = 'MEMBELI';
                                        } else {
                                            $pill_bg = 'rgba(239, 68, 68, 0.2)'; // Dark theme transparent red
                                            $pill_color = '#F87171'; // Light red text
                                            $pill_text = 'TIDAK MEMBELI';
                                        }
                                        
                                        echo "<td style='padding: 12px 10px;'>
                                                <span style='background-color: {$pill_bg}; color: {$pill_color}; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; display: inline-block; text-align: center; border: 1px solid {$pill_color};'>{$pill_text}</span>
                                              </td>";
                                              
                                        echo "</tr>";
                                    }
                                    echo "</tbody></table>";
                                }
                                fclose($file_handle);
                            } else {
                                echo "<tr><td>Gagal membaca file hasil.csv</td></tr></table>";
                            }
                            echo "</div>";

                            // Include DataTables JS
                            echo "
                            <link rel='stylesheet' href='https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css'>
                            <style>
                                .dataTables_wrapper .dataTables_length, .dataTables_wrapper .dataTables_filter, .dataTables_wrapper .dataTables_info, .dataTables_wrapper .dataTables_processing, .dataTables_wrapper .dataTables_paginate { color: var(--text-light) !important; font-size: 0.85rem; margin-top: 10px;}
                                .dataTables_wrapper .dataTables_filter input { background: var(--input-bg); border: 1px solid var(--border); color: var(--text-dark); padding: 4px 8px; border-radius: 4px; }
                                .dataTables_wrapper .dataTables_length select { background: var(--input-bg); border: 1px solid var(--border); color: var(--text-dark); padding: 4px; border-radius: 4px; }
                                table.dataTable tbody tr { background-color: var(--card-bg) !important; }
                                table.dataTable tbody tr:hover { background-color: var(--input-bg) !important; }
                                table.dataTable thead th { border-bottom: none !important; }
                                table.dataTable.no-footer { border-bottom: 1px solid var(--border) !important; }
                                .dataTables_wrapper .dataTables_paginate .paginate_button { color: var(--text-light) !important; }
                                .dataTables_wrapper .dataTables_paginate .paginate_button.current, .dataTables_wrapper .dataTables_paginate .paginate_button.current:hover { background: var(--primary) !important; color: white !important; border: 1px solid var(--primary) !important; }
                            </style>
                            <script src='https://code.jquery.com/jquery-3.7.0.min.js'></script>
                            <script src='https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js'></script>
                            <script>
                            $(document).ready(function() {
                                var table = $('#dataTableHasil').DataTable({
                                    pageLength: 10,
                                    scrollX: true,
                                    language: {
                                        search: 'Cari:',
                                        lengthMenu: 'Tampilkan _MENU_ data per halaman',
                                        info: 'Menampilkan _START_ sampai _END_ dari _TOTAL_ data',
                                        paginate: { first: 'Awal', last: 'Akhir', next: 'Selanjutnya', previous: 'Sebelumnya' }
                                    }
                                });

                                // Event listener untuk filter bulan
                                $('#monthFilter').on('change', function() {
                                    var val = $(this).val();
                                    // Cari tepat sesuai nilai bulan pada kolom ke-4 (index 3)
                                    var searchVal = val ? '^' + $.fn.dataTable.util.escapeRegex(val) + '$' : '';
                                    table.column(3).search(searchVal, true, false).draw();
                                    
                                    // Hitung ulang statistik dari baris yang tersisa (terfilter)
                                    var filteredData = table.rows({ search: 'applied' }).data();
                                    var total = filteredData.length;
                                    var purchase = 0;
                                    var noPurchase = 0;
                                    
                                    for(var i=0; i<total; i++){
                                        // Kolom 'Hasil Prediksi' berada pada index 6 (0-indexed)
                                        var labelHtml = filteredData[i][6]; 
                                        if(labelHtml.includes('TIDAK MEMBELI')) {
                                            noPurchase++;
                                        } else if(labelHtml.includes('MEMBELI')) {
                                            purchase++;
                                        }
                                    }
                                    
                                    var purchasePct = total > 0 ? ((purchase / total) * 100).toFixed(2) : 0;
                                    var nopurchasePct = total > 0 ? ((noPurchase / total) * 100).toFixed(2) : 0;
                                    
                                    // Fungsi format angka ribuan
                                    var formatNumber = function(num) {
                                        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                                    };
                                    
                                    // Update elemen HTML di layar
                                    $('#stat-total').text(formatNumber(total) + ' baris');
                                    $('#stat-purchase').text(formatNumber(purchase));
                                    $('#stat-nopurchase').text(formatNumber(noPurchase));
                                    $('#desc-purchase').text('Persentase: ' + purchasePct + '% dari total pengunjung');
                                    $('#desc-nopurchase').text('Persentase: ' + nopurchasePct + '% dari total pengunjung');
                                    
                                    // Update grafik Pie Chart
                                    if(window.myChart) {
                                        window.myChart.data.datasets[0].data = [purchase, noPurchase];
                                        window.myChart.update();
                                    }
                                });
                            });
                            </script>
                            ";
                        }
                    }
                    echo "</div>";
                } else {
                    echo "<div class='results' style='color: var(--danger);'>Upload Gagal!</div>";
                }
            }
            ?>
        </div>
    </div>
</body>
</html>
