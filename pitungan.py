import streamlit as st
import datetime as dt
from datetime import datetime, timedelta

# Setup halaman utama web app agar responsif di HP
st.set_page_config(
    page_title="Pitung Jopo: Peringatan Kematian", 
    page_icon="🕯️", 
    layout="centered"
)

# Judul Aplikasi Utama dengan gaya elegan
st.title("🕯️ Pitung Jawa: Hitung Peringatan Kematian")
st.markdown("Aplikasi praktis untuk menghitung hari peringatan arwah (3 hari hingga 1000 hari) berdasarkan aturan perpindahan hari kalender Jawa kuno.")
st.markdown("---")

# --- DATABASE LOGIKA JAWA ---
DAFTAR_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
DAFTAR_PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]

def hitung_weton_jawa(tgl_target):
    """Mencari Hari & Pasaran Jawa berdasarkan tanggal Masehi"""
    tanggal_patokan = datetime(1900, 1, 1) # Patokan dasar: Senin Legi
    selisih_hari = (tgl_target - tanggal_patokan).days
    
    idx_h = (0 + selisih_hari) % 7
    idx_p = (1 + selisih_hari) % 5
    
    return DAFTAR_HARI[idx_h], DAFTAR_PASARAN[idx_p]

# --- USER INPUT SECTION ---
st.subheader("📅 Input Data Waktu Wafat")

min_date = dt.date(1940, 1, 1)
max_date = dt.date(2050, 12, 31)

tgl_input = st.date_input(
    "Pilih Tanggal Meninggal Dunia:", 
    value=dt.date(2005, 5, 8), 
    min_value=min_date, 
    max_value=max_date, 
    format="DD/MM/YYYY"
)

waktu_meninggal = st.radio(
    "Kapan Waktu Jam Meninggal Dunia?", 
    (
        "Siang / Pagi / Sore (Sebelum Jam 18.00 WIB)", 
        "Malam Hari (Sesudah Jam 18.00 WIB - Masuk Hari Jawa Berikutnya)"
    )
)

st.markdown("---")

if tgl_input:
    # Konversi ke objek datetime untuk operasi timedelta
    tgl_wafat = datetime.combine(tgl_input, datetime.min.time())
    
    # Logika Inti: Jika malam hari (setelah magrib), hari Jawa maju 1 hari
    is_malam = "Malam Hari" in waktu_meninggal
    tgl_hitung_jawa = tgl_wafat + timedelta(days=1) if is_malam else tgl_wafat
    
    # Hitung weton dasar kematian
    h_wafat, p_wafat = hitung_weton_jawa(tgl_hitung_jawa)
    weton_wafat_lengkap = f"{h_wafat} {p_wafat}"
    
    st.subheader("📊 Hasil Perhitungan Tradisional & Jadwal Kenduri")
    
    # Alert Box Informasi Weton Utama
    st.warning(
        f"**Weton Meninggal (Adat Jawa): {weton_wafat_lengkap.upper()}**\n\n"
        f"*(Tanggal Input: {tgl_input.strftime('%d/%m/%Y')} | "
        f"Kondisi Waktu: {'Hari Digeser ke Esoknya (Malam)' if is_malam else 'Hari Tetap (Siang)'})*"
    )
    
    # Rumus Interval Pitung Jawa (Hari H dihitung sebagai hari ke-1)
    jarak_peringatan = {
        "Geblag (Hari H Wafat)": 0,
        "Nelung Dina (3 Hari)": 2,
        "Mitung Dina (7 Hari)": 6,
        "Matang Puluh Dina (40 Hari)": 39,
        "Nyatus Dina (100 Hari)": 99,
        "Pendak I (1 Tahun Jawa)": 353,
        "Pendak II (2 Tahun Jawa)": 707,
        "Nyewu Dina (1000 Hari)": 999
    }
    
    # Penampung baris data untuk di-render ke dalam dokumen cetak PDF
    html_rows = ""
    
    # Menampilkan data interaktif di Streamlit sekaligus menyusun tabel PDF
    for nama_peringatan, tambah_hari in jarak_peringatan.items():
        tgl_peringatan = tgl_hitung_jawa + timedelta(days=tambah_hari)
        h_per, p_per = hitung_weton_jawa(tgl_peringatan)
        weton_per_lengkap = f"{h_per} {p_per}"
        
        # LOGIKA KENDURI TRADISIONAL JAWA:
        # Acara kenduri/selamatan dilakukan malam hari sebelum hari H pitung masehi (H-1 sore setelah Magrib)
        tgl_kenduri = tgl_peringatan - timedelta(days=1)
        h_kenduri, p_kenduri = hitung_weton_jawa(tgl_kenduri)
        
        tgl_per_str = tgl_peringatan.strftime('%d/%m/%Y')
        tgl_kenduri_str = tgl_kenduri.strftime('%d/%m/%Y')
        
        # UI Streamlit Expander yang Informatif bagi Tuan Rumah
        with st.expander(f"📌 {nama_peringatan}", expanded=True):
            st.markdown(f"**Weton Pitung:** {weton_per_lengkap} ({tgl_per_str})")
            st.markdown(f"🟩 **JADWAL KENDURI:** **{h_kenduri} {p_kenduri} Malam**, Tanggal **{tgl_kenduri_str}** *(Habis Magrib)*")
            
        # Baris Tabel untuk Template PDF
        html_rows += f"""
        <tr>
            <td class="label">{nama_peringatan}</td>
            <td>
                <b>{weton_per_lengkap}</b><br>
                <span style="font-size:11px; color:#666;">Hari H: {tgl_per_str}</span>
            </td>
            <td class="kenduri-col">
                <b>{h_kenduri} {p_kenduri} Malam</b><br>
                <span>{tgl_kenduri_str} (Habis Magrib)</span>
            </td>
        </tr>
        """
        
    st.markdown("---")
    st.markdown("### 📜 Cetak Dokumen Peringatan Adat")
    st.markdown("Klik tombol di bawah untuk mengunduh atau mencetak sertifikat rincian jadwal selamatan *Pitung Jopo* resmi dalam format PDF.")
    
    # --- TEMPLATE HTML/CSS PRINTABLE SERTIFIKAT PITUNG NUANSA BATIK JAWA ---
    html_sertifikat = f"""
    <html>
    <head>
    <style>
        @media print {{
            body {{ background: white; color: black; }}
            .no-print {{ display: none !important; }}
        }}
        .cert-container {{
            border: 6px double #4a3b32;
            padding: 35px 25px;
            background-color: #fcf9f2;
            background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgdmlld0JveD0iMCAwIDYwIDYwIj4KPGcgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjNGEzYjMyIiBzdHJva2Utd2lkdGg9IjAuNSIgc3Ryb2tlLW9wYWNpdHk9IjAuMDUiPgo8Y2lyY2xlIGN4PSIzMCIgY3k9IjMwIiByPSIyNSIvPgo8Y2lyY2xlIGN4PSIwIiBjeT0iMCIgcj0iMjUiLz4KPGNpcmNsZSBjeD0iNjAiIGN5PSIwIiByPSIyNSIvPgo8Y2lyY2xlIGN4PSIwIiBjeT0iNjAiIHI9IjI1Ii8+CjxjaXJjbGUgY3g9IjYwIiBjeT0iNjAiIHI9IjI1Ii8+CjxwYXRoIGQ9Ik0zMCw1IEwzMCw1NSBNNSwzMCBMNTUsMzAiLz4KPC9nPgo8L3N2Zz4=');
            font-family: 'Georgia', serif;
            color: #333;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(74,59,50,0.1);
            margin: 10px auto;
            max-width: 620px;
            position: relative;
        }}
        .cert-container::before {{
            content: "◆";
            position: absolute;
            top: 10px;
            left: 10px;
            color: #4a3b32;
            font-size: 14px;
            opacity: 0.6;
        }}
        .cert-container::after {{
            content: "◆";
            position: absolute;
            top: 10px;
            right: 10px;
            color: #4a3b32;
            font-size: 14px;
            opacity: 0.6;
        }}
        .cert-title {{
            font-size: 22px;
            font-weight: bold;
            color: #4a3b32;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }}
        .cert-subtitle {{
            font-size: 13px;
            font-style: italic;
            color: #555;
            margin-bottom: 22px;
        }}
        .main-weton {{
            font-size: 15px;
            background-color: #f3edd9;
            padding: 12px;
            border-radius: 6px;
            font-weight: bold;
            color: #4a3b32;
            margin-bottom: 25px;
            border: 1px dashed #4a3b32;
        }}
        .cert-table {{
            width: 100%;
            margin: 15px 0;
            border-collapse: collapse;
        }}
        .cert-table th {{
            background-color: #4a3b32;
            color: #fff;
            padding: 8px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .cert-table td {{
            padding: 10px 6px;
            text-align: left;
            font-size: 12.5px;
            border-bottom: 1px dashed #cfc8b9;
            vertical-align: middle;
        }}
        .cert-table td.label {{
            font-weight: bold;
            color: #4a3b32;
        }}
        .kenduri-col {{
            background-color: rgba(40, 167, 69, 0.05);
            border-left: 2px solid #28a745;
            color: #1e622b;
        }}
        .watermark-container {{
            margin-top: 35px;
            padding-top: 15px;
            border-top: 1px dashed #4a3b32;
            text-align: right;
        }}
        .watermark-text {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            font-weight: bold;
            color: #4a3b32;
            letter-spacing: 2px;
            opacity: 0.85;
        }}
        .watermark-sub {{
            font-size: 9px;
            color: #777;
            letter-spacing: 1px;
            font-family: sans-serif;
        }}
        .print-btn {{
            background-color: #28a745;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
            transition: 0.3s;
        }}
        .print-btn:hover {{
            background-color: #218838;
        }}
    </style>
    </head>
    <body>
        <div class="cert-container">
            <div class="cert-title">🕯️ Piagam Pitung Jawa 🕯️</div>
            <div class="cert-subtitle">Panduan Jadwal Kenduri Peringatan Adat Kematian</div>
            
            <div class="main-weton">
                Weton Wafat: {weton_wafat_lengkap.upper()}<br>
                <span style="font-size: 11px; font-weight: normal; font-style: italic; color:#555;">
                    Masehi: {tgl_input.strftime('%d/%m/%Y')} ({waktu_meninggal.split('(')[0].strip()})
                </span>
            </div>
            
            <table class="cert-table">
                <thead>
                    <tr>
                        <th style="text-align:left;">Peringatan</th>
                        <th style="text-align:left;">Hari H & Weton</th>
                        <th style="text-align:left; background-color:#28a745;">📅 WAKTU KENDURI</th>
                    </tr>
                </thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
            
            <div class="watermark-container">
                <div class="watermark-text">✍️ JARULISME.DEV-APP</div>
                <div class="watermark-sub">Verified Pitung & Kenduri Schedule</div>
            </div>
            
            <div class="no-print" style="margin-top: 25px;">
                <button class="print-btn" onclick="window.print()">📥 Download / Cetak Jadwal Kenduri (PDF)</button>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Mengalirkan komponen sertifikat interaktif ke dalam halaman web app (Tinggi dinaikkan sedikit ke 820 karena tabel melebar)
    st.components.v1.html(html_sertifikat, height=820, scrolling=False)

# Footer Aplikasi
st.markdown("---")
st.caption("Aplikasi dikembangkan oleh JARULISME.DEV-APP © 2026")
