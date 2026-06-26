import streamlit as st
import datetime
from datetime import datetime, timedelta

# ==========================================
# CONFIG & STYLE HALAMAN
# ==========================================
st.set_page_config(page_title="Primbon & Pitung Adat Jawa", page_icon="🔮", layout="wide")

# CSS kustom minimalis khusus untuk mempercantik komponen utama
st.markdown("""
<style>
    /* Desain teks judul agar memiliki estetika Jawa yang kuat */
    .main-title { 
        font-size: 26px !important; 
        font-weight: bold; 
        text-align: center; 
        color: #8B4513 !important; 
        margin-bottom: 5px; 
    }
    .subtitle { 
        font-size: 13px !important; 
        text-align: center; 
        color: #444444 !important; 
        margin-bottom: 20px; 
    }
    
    /* Kotak Hasil (Card) Krem dengan border cokelat tegas */
    .card-hasil { 
        background-color: #FFF8DC !important; 
        padding: 18px; 
        border-radius: 10px; 
        border: 2px solid #8B4513 !important; 
        border-left: 8px solid #8B4513 !important; 
        margin-top: 15px; 
        margin-bottom: 15px; 
    }
    .card-hasil *, .card-hasil p, .card-hasil h3, .card-hasil h4 { 
        color: #111111 !important; 
    }
    
    /* Status warna indikator */
    .status-baik { color: #1B5E20 !important; font-weight: bold; font-size: 16px; } 
    .status-perhatian { color: #B71C1C !important; font-weight: bold; font-size: 16px; } 
    .highlight-text { font-weight: bold; color: #8B4513 !important; }

    /* Desain Tombol Cetak PDF agar kontras tinggi */
    button, [data-testid="stBaseButton-secondary"] {
        background-color: #8B4513 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    button p { color: #FFFFFF !important; }

    @media print {
        .stButton, div[data-testid="stSidebar"], header, footer {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def tambah_tombol_pdf():
    if st.button("🖨️ Download / Cetak PDF Halaman Ini"):
        st.components.v1.html("<script>window.print();</script>", height=0, width=0)

# ==========================================
# UTILITY & DATABASE PRIMBON JAWA
# ==========================================
DAFTAR_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
DAFTAR_PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]

NEPTU_HARI = {"Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9, "Minggu": 5}
NEPTU_PASARAN = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}

KONVERSI_BULAN_JAWA = {
    1: {"jawa": "Sura / Sapar", "titik": "📐 Sudut Tenggara lahan", "arah": "🧘 Menghadap ke arah Barat"},
    2: {"jawa": "Sapar / Mulud", "titik": "📐 Sudut Tenggara lahan", "arah": "🧘 Menghadap ke arah Barat"},
    3: {"jawa": "Mulud / Bakdamulud", "titik": "📐 Sudut Tenggara lahan", "arah": "🧘 Menghadap ke arah Barat"},
    4: {"jawa": "Bakdamulud / Jumadilawal", "titik": "📐 Sudut Timur Laut lahan", "arah": "🧘 Menghadap ke arah Selatan"},
    5: {"jawa": "Jumadilawal / Jumadilakhir", "titik": "📐 Sudut Timur Laut lahan", "arah": "🧘 Menghadap ke arah Selatan"},
    6: {"jawa": "Jumadilakhir / Rejeb", "titik": "📐 Sudut Timur Laut lahan", "arah": "🧘 Menghadap ke arah Selatan"},
    7: {"jawa": "Rejeb / Ruwah", "titik": "📐 Sudut Barat Laut lahan", "arah": "🧘 Menghadap ke arah Timur"},
    8: {"jawa": "Ruwah / Pasa", "titik": "📐 Sudut Barat Laut lahan", "arah": "🧘 Menghadap ke arah Timur"},
    9: {"jawa": "Pasa / Sawal", "titik": "📐 Sudut Barat Laut lahan", "arah": "🧘 Menghadap ke arah Timur"},
    10: {"jawa": "Sawal / Sela", "titik": "📐 Sudut Barat Daya lahan", "arah": "🧘 Menghadap ke arah Utara"},
    11: {"jawa": "Sela / Besar", "titik": "📐 Sudut Barat Daya lahan", "arah": "🧘 Menghadap ke arah Utara"},
    12: {"jawa": "Besar / Sura", "titik": "📐 Sudut Barat Daya lahan", "arah": "🧘 Menghadap ke arah Utara"}
}

WATAK_NEPTU_DETIL = {
    7: "🎯 Pandalan Jiwa (Pendiam & Merantau): Suka bepergian jauh, setia, jujur, namun cenderung kaku dan sulit dipengaruhi orang lain.",
    8: "🎯 Lakuning Geni (Emosional namun Penolong): Cepat marah tapi cepat reda, pemberani, tidak suka melihat ketidakadilan, berhati emas.",
    9: "🎯 Lakuning Angin (Lincah & Goyah): Mudah bergaul, berwawasan luas, cerdas, tetapi pendiriannya mudah goyah oleh hasutan.",
    10: "🎯 Pendito Sakti (Cerdas & Penasihat): Suka menasihati tapi tidak suka dinasihati, pemikir ulung, mandiri, jalannya rezeki stabil.",
    11: "🎯 Lakuning Setan (Pemberani & Penyelamat): Berjiwa ksatria, tidak tega melihat orang susah, sangat setia kawan, tapi kalau marah sulit diredam.",
    12: "🎯 Lakuning Kembang (Pemimpin Populer): Pandai bergaul, pembawaannya damai, sering jadi pusat perhatian, rezekinya selalu mengalir.",
    13: "🎯 Lakuning Lintang (Pesona Bintang): Memiliki daya pikat kuat, tutur katanya halus, cerdas, tapi menyukai kesendirian (introvert).",
    14: "🎯 Lakuning Bulan (Penerang & Pengayom): Sangat berbakti, cepat belajar hal baru, ikhlas menolong, pendengar yang baik bagi teman.",
    15: "🎯 Lakuning Srengenge (Wibawa Matahari): Berwibawa tinggi, disegani, tegas, keras kepala, protektif terhadap keluarga dan kelompoknya.",
    16: "🎯 Lakuning Bumi (Penyabar & Pemurah): Penuh semangat, mandiri, jiwanya lapang dada, sangat sabar menghadapi ujian hidup.",
    17: "🎯 Resi Sakti (Firasat Tajam): Pendiam namun sangat cerdas, memiliki firasat yang sering jadi kenyataan, suka menolong tanpa pamrih.",
    18: "🎯 Paripurna (Kewibawaan Mutlak): Bijaksana, berjiwa ksatria, emosinya stabil, memiliki keberuntungan besar dalam karier dan usaha."
}

def hitung_weton_jawa_akurat(tgl_target, jam_input=None):
    if jam_input and jam_input >= datetime.strptime("18:00", "%H:%M").time():
        tgl_target = tgl_target + timedelta(days=1)
        
    tanggal_patokan = datetime(1900, 1, 1)
    selisih_hari = (tgl_target - tanggal_patokan).days
    idx_hari = (0 + selisih_hari) % 7
    idx_pasaran = (1 + selisih_hari) % 5
    return DAFTAR_HARI[idx_hari], DAFTAR_PASARAN[idx_pasaran]

# ==========================================
# MENU UTAMA DI HALAMAN AWAL 
# ==========================================
st.markdown('<div class="main-title">🔮 PRIMBON & PITUNG ADAT JAWA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sistem Otomatisasi Kalender & Perhitungan Modular Finansial/Keluarga</div>', unsafe_allow_html=True)

menu_terpilih = st.selectbox("📂 SILAKAN PILIH MODUL PERHITUNGAN DI SINI:", [
    "🔍 Cek Weton Kelahiran",
    "💍 Puthu Penganten (Jodoh & Hajatan)",
    "🏡 Petungan Rumah & Nyecek Lemah",
    "🕯️ Pitung Kematian & Kenduri",
    "👶 Siklus & Selamatan Bayi"
])

st.markdown("---")

# ==========================================
# MODUL 1: CEK WETON KELAHIRAN
# ==========================================
if menu_terpilih == "🔍 Cek Weton Kelahiran":
    st.subheader("🔍 DATA KELAHIRAN LENGKAP")
    col1, col2 = st.columns([1, 2])
    with col1:
        tgl_input = st.date_input("Masukkan Tanggal Lahir:", value=datetime(2000, 1, 1))
        jam_input = st.time_input("Masukkan Jam Lahir (Estimasi):", value=datetime.strptime("08:00", "%H:%M").time())
        
        if jam_input >= datetime.strptime("04:00", "%H:%M").time() and jam_input < datetime.strptime("10:00", "%H:%M").time():
            kategori_jam = "🌅 Pagi Hari (Penuh Semangat & Ide Baru)"
        elif jam_input >= datetime.strptime("10:00", "%H:%M").time() and jam_input < datetime.strptime("15:00", "%H:%M").time():
            kategori_jam = "☀️ Siang Hari (Logis, Tegas & Pekerja Keras)"
        elif jam_input >= datetime.strptime("15:00", "%H:%M").time() and jam_input < datetime.strptime("18:00", "%H:%M").time():
            kategori_jam = "🌇 Sore Hari (Tenang, Diplomatis & Pengayom)"
        else:
            kategori_jam = "🌙 Malam Hari (Sudah Masuk Siklus Hari Esoknya - Karakter Intuitif & Pemikir)"

        tgl_dt = datetime.combine(tgl_input, datetime.min.time())
        hari, pasaran = hitung_weton_jawa_akurat(tgl_dt, jam_input)
        neptu = NEPTU_HARI[hari] + NEPTU_PASARAN[pasaran]
        
    with col2:
        idx_hari_ini = DAFTAR_HARI.index(hari)
        idx_pasaran_ini = DAFTAR_PASARAN.index(pasaran)
        
        hari_nahas_1 = f"{DAFTAR_HARI[(idx_hari_ini + 3) % 7]} {DAFTAR_PASARAN[(idx_pasaran_ini + 3) % 5]}"
        hari_nahas_2 = f"{DAFTAR_HARI[(idx_hari_ini + 5) % 7]} {DAFTAR_PASARAN[(idx_pasaran_ini + 1) % 5]}"
        
        hari_baik_1 = f"{DAFTAR_HARI[(idx_hari_ini + 2) % 7]} {DAFTAR_PASARAN[(idx_pasaran_ini + 2) % 5]}"
        hari_baik_2 = f"{DAFTAR_HARI[(idx_hari_ini + 4) % 7]} {DAFTAR_PASARAN[(idx_pasaran_ini + 4) % 5]}"
        
        watak_desc = WATAK_NEPTU_DETIL.get(neptu, "Adaptif, fleksibel, dan memiliki potensi sukses besar.")
        
        st.markdown(f"""
        <div class="card-hasil">
            <h3>Hasil Analisis Kelahiran Jawa Berdasarkan Jam Lahir:</h3>
            <p>⏰ Waktu Lahir: <span class="highlight-text">{kategori_jam}</span> pada jam {jam_input.strftime('%H:%M')} WIB</p>
            <p>📆 Hari Pasaran (Adat): <span class="highlight-text" style="font-size: 20px;">{hari.upper()} {pasaran.upper()}</span></p>
            <p>🔢 Jumlah Neptu: <span class="highlight-text">{neptu}</span> (Hari: {NEPTU_HARI[hari]} + Pasaran: {NEPTU_PASARAN[pasaran]})</p>
            <hr style="border-top: 1px solid #8B4513;">
            <p>🧬 <b>Perwatakan & Tabiat Hasil Weton:</b><br><i>"{watak_desc}"</i></p>
            <hr style="border-top: 1px solid #8B4513;">
            <p>🚨 <span class="status-perhatian">HARI NAHAS / APES (Hindari untuk Hajatan/Pondasi):</span><br>
            • <b>{hari_nahas_1}</b> (Dina Sampar Wangke)<br>• <b>{hari_nahas_2}</b> (Dina Geringan)</p>
            <p>🍀 <span class="status-baik">HARI BAIK BAWAAN LAHIR (Ideal untuk Memulai Usaha/Aktivitas Mulia):</span><br>
            • <b>{hari_baik_1}</b><br>• <b>{hari_baik_2}</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    tambah_tombol_pdf()

# ==========================================
# MODUL 2: PUTHU PENGANTEN
# ==========================================
elif menu_terpilih == "💍 Puthu Penganten (Jodoh & Hajatan)":
    st.subheader("💍 JODOH & JADWAL HAJATAN")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Data Pria**")
        tgl_pria = st.date_input("Tanggal Lahir Pria:", value=datetime(1998, 5, 10))
        h_pria, p_pria = hitung_weton_jawa_akurat(datetime.combine(tgl_pria, datetime.min.time()))
        nep_pria = NEPTU_HARI[h_pria] + NEPTU_PASARAN[p_pria]
        st.caption(f"Weton: {h_pria} {p_pria} (Neptu: {nep_pria})")
        
    with col2:
        st.write("**Data Wanita**")
        tgl_wanita = st.date_input("Tanggal Lahir Wanita:", value=datetime(2000, 8, 15))
        h_wanita, p_wanita = hitung_weton_jawa_akurat(datetime.combine(tgl_wanita, datetime.min.time()))
        nep_wanita = NEPTU_HARI[h_wanita] + NEPTU_PASARAN[p_wanita]
        st.caption(f"Weton: {h_wanita} {p_wanita} (Neptu: {nep_wanita})")

    total_neptu_jodoh = nep_pria + nep_wanita
    sisa_jodoh = total_neptu_jodoh % 8
    
    KATEGORI_JODOH = {
        1: ("PEGAT", "Rawan masalah ekonomi atau kecocokan di kemudian hari.", "status-perhatian"),
        2: ("RATU", "Sangat serasi, disegani tetangga, dan berwibawa.", "status-baik"),
        3: ("JODOH", "Saling menerima kelebihan/kekurangan, rumah tangga harmonis.", "status-baik"),
        4: ("TOPO", "Awal pernikahan berat/banyak tirakat, namun sukses di akhir.", "status-baik"),
        5: ("TINARI", "Murah rezeki, berkah, sering mendapat keberuntungan.", "status-baik"),
        6: ("PADU", "Sering bertengkar tapi tidak sampai cerai.", "status-perhatian"),
        7: ("SUJANAN", "Rawan pertengkaran akibat perselisihan.", "status-perhatian"),
        0: ("PESTHI", "Rukun, adem ayem, tenteram hingga tua.", "status-baik")
    }
    
    nama_kat, ket_kat, kelas_css = KATEGORI_JODOH[sisa_jodoh]
    st.markdown(f"<div class='card-hasil'><h4>Hasil Jodoh (Neptu: {total_neptu_jodoh})</h4>Kategori: <span class='{kelas_css}'>{nama_kat}</span><br><small>{ket_kat}</small></div>", unsafe_allow_html=True)
    
    st.write("### 📅 Pencarian Otomatis Hari Baik Hajatan")
    bln_hajatan = st.selectbox("Pilih Bulan Target Pernikahan:", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"])
    thn_hajatan = st.number_input("Tahun Target:", min_value=2026, max_value=2035, value=2026)
    
    bulan_angka = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"].index(bln_hajatan) + 1
    hari_baik_ditemukan = []
    start_date = datetime(thn_hajatan, bulan_angka, 1)
    
    for d in range(32):
        try:
            curr_date = start_date + timedelta(days=d)
            if curr_date.month != bulan_angka: break
            h_h, p_h = hitung_weton_jawa_akurat(curr_date)
            nep_hari_ini = NEPTU_HARI[h_h] + NEPTU_PASARAN[p_h]
            
            if (total_neptu_jodoh + nep_hari_ini) % 5 in [1, 2]:
                besok_date = curr_date + timedelta(days=1)
                h_b, p_b = hitung_weton_jawa_akurat(besok_date)
                nep_besok = NEPTU_HARI[h_b] + NEPTU_PASARAN[p_b]
                if (total_neptu_jodoh + nep_besok) % 5 in [1, 2]:
                    hari_baik_ditemukan.append({
                        "ijab": curr_date.strftime("%d/%m/%Y"), "weton_ijab": f"{h_h} {p_h}",
                        "resepsi": besok_date.strftime("%d/%m/%Y"), "weton_resepsi": f"{h_b} {p_b}"
                    })
        except: pass
            
    if hari_baik_ditemukan:
        st.success(f"Ditemukan {len(hari_baik_ditemukan)} pasangan tanggal ideal:")
        for idx, item in enumerate(hari_baik_ditemukan):
            st.markdown(f"👉 **Opsi {idx+1}:** Ijab Qabul pada **{item['ijab']}** ({item['weton_ijab']}) & dilanjutkan Resepsi pada **{item['resepsi']}** ({item['weton_resepsi']})")
    else:
        st.warning("Tidak ditemukan tanggal ideal di bulan ini.")
    tambah_tombol_pdf()

# ==========================================
# MODUL 3: PETUNGAN RUMAH
# ==========================================
elif menu_terpilih == "🏡 Petungan Rumah & Nyecek Lemah":
    st.subheader("🏡 ADAT PETUNGAN RUMAH")
    tab1, tab2 = st.tabs(["🧭 Arah Hadap Rumah", "🏗️ Pencarian Hari Baik Nyecek Lemah"])
    
    with tab1:
        st.write("**Kecocokan Arah Hadap Rumah**")
        tgl_kk = st.date_input("Tanggal Lahir Kepala Keluarga (Suami):", value=datetime(1988, 3, 20), key="rumah_kk")
        h_kk, p_kk = hitung_weton_jawa_akurat(datetime.combine(tgl_kk, datetime.min.time()))
        nep_kk = NEPTU_HARI[h_kk] + NEPTU_PASARAN[p_kk]
        
        st.info(f"Weton Kepala Keluarga: **{h_kk} {p_kk}** (Neptu: {nep_kk})")
        arah_uji = st.selectbox("Pilih Rencana Arah Hadap Rumah:", ["Utara", "Timur", "Selatan", "Barat"])
        
        peta_arah = {"Utara": 1, "Timur": 2, "Selatan": 3, "Barat": 4}
        sisa_rumah = (nep_kk + peta_arah[arah_uji]) % 5
        
        HASIL_RUMAH = {
            1: ("KERTARTA", "Sangat Baik: Aman, tenteram, murah rezeki, berkah.", "status-baik"),
            2: ("YASA", "Sangat Baik: Dihormati, usaha/karier maju pesat.", "status-baik"),
            3: ("CANDRA", "Cukup Baik: Rumah tangga harmonis, berwibawa.", "status-baik"),
            4: ("ROGOH", "Kurang Baik: Rawan kehilangan benda, boros rezeki.", "status-perhatian"),
            0: ("SEMPAL", "Tidak Baik: Sering sakit-sakitan atau banyak rintangan.", "status-perhatian")
        }
        nama_r, ket_r, css_r = HASIL_RUMAH[sisa_rumah]
        st.markdown(f"<div class='card-hasil'>Arah Hadap Rumah ke <b>{arah_uji}</b> menghasilkan hitungan: <span class='{css_r}'>{nama_r}</span><br><small>{ket_r}</small></div>", unsafe_allow_html=True)
        
    with tab2:
        st.write("**Otomatisasi Hari Baik & Jam Ideal Nyecek Lemah**")
        bln_masehi_pilih = st.selectbox("Pilih Bulan Kalender Masehi:", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "December"], key="bln_ny")
        thn_masehi_pilih = st.number_input("Tahun Rencana:", min_value=2026, max_value=2035, value=2026, key="thn_ny")
        
        idx_masehi = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "December"].index(bln_masehi_pilih) + 1
        start_date_ny = datetime(thn_masehi_pilih, idx_masehi, 1)
        
        info_siklus = KONVERSI_BULAN_JAWA[idx_masehi]
        titik_awal = info_siklus["titik"]
        arah_orang = info_siklus["arah"]
        perkiraan_jawa = info_siklus["jawa"]
        
        st.info(f"ℹ️ **Deteksi Otomatis Sistem:** Bulan Masehi {bln_masehi_pilih} bertepatan dengan siklus Bulan Jawa **{perkiraan_jawa}**.")
        
        JAM_IDEAL = {
            "Senin": "🕒 Pukul 06.00 - 08.24 (Saat Samudra / Rezeki Luas)",
            "Selasa": "🕒 Pukul 08.24 - 10.48 (Saat Ratu / Dihormati)",
            "Rabu": "🕒 Pukul 10.48 - 13.12 (Saat Ratu / Kejayaan)",
            "Kamis": "🕒 Pukul 13.12 - 15.36 (Saat Rezeki Mulia)",
            "Jumat": "🕒 Pukul 06.00 - 08.24 (Saat Agung / Selamat)",
            "Sabtu": "🕒 Pukul 08.24 - 10.48 (Saat Rezeki)",
            "Minggu": "🕒 Pukul 06.00 - 08.24 (Saat Ratu)"
        }
            
        opsi_nyecek = []
        for day_offset in range(32):
            try:
                date_ny = start_date_ny + timedelta(days=day_offset)
                if date_ny.month != idx_masehi: break
                
                h_ny, p_ny = hitung_weton_jawa_akurat(date_ny)
                nep_hari_ny = NEPTU_HARI[h_ny] + NEPTU_PASARAN[p_ny]
                
                total_suku = nep_kk + nep_hari_ny
                sisa_suku = total_suku % 4
                
                if sisa_suku == 1:
                    opsi_nyecek.append((date_ny.strftime("%d/%m/%Y"), f"{h_ny} {p_ny}", "GURU (Sangat Baik / Berkah & Pengayom)", JAM_IDEAL[h_ny]))
                elif sisa_suku == 2:
                    opsi_nyecek.append((date_ny.strftime("%d/%m/%Y"), f"{h_ny} {p_ny}", "RATU (Sangat Baik / Harmonis & Berwibawa)", JAM_IDEAL[h_ny]))
            except: pass
                
        if opsi_nyecek:
            st.success(f"Ditemukan {len(opsi_nyecek)} tanggal ideal di bulan {bln_masehi_pilih} untuk Nyecek Lemah:")
            for tgl_s, weton_s, status_s, jam_s in opsi_nyecek:
                with st.expander(f"📅 Tanggal: {tgl_s} ({weton_s}) — Kategori: {status_s}"):
                    st.write(f"* **Jam Ideal Mulai Menggali:** {jam_s}")
                    st.write(f"* **Titik Pertama Pondasi digali:** {titik_awal}")
                    st.write(f"* **Posisi Pekerja/Orang yang mencangkul pertama:** {arah_orang}")
        else:
            st.warning("Tidak ditemukan tanggal dengan hitungan Guru/Ratu di bulan ini.")
    tambah_tombol_pdf()

# ==========================================
# MODUL 4: PITUNG KEMATIAN
# ==========================================
elif menu_terpilih == "🕯️ Pitung Kematian & Kenduri":
    st.subheader("🕯️ SIKLUS PERINGATAN KEMATIAN")
    
    tgl_wafat = st.date_input("Tanggal Meninggal (Masehi):", value=datetime.today())
    waktu_kejadian = st.radio("Waktu Kejadian Wafat:", ["Siang / Pagi / Sore (Sebelum 18.00 WIB)", "Malam Hari (Setelah 18.00 WIB - Masuk Adat Esoknya)"])
    
    tgl_wafat_dt = datetime.combine(tgl_wafat, datetime.min.time())
    tgl_hitung = tgl_wafat_dt + timedelta(days=1) if "Malam" in waktu_kejadian else tgl_wafat_dt
    h_wafat, p_wafat = hitung_weton_jawa_akurat(tgl_hitung)
    
    st.markdown(f"<div class='card-hasil'><strong>WETON MENINGGAL (ADAT JAWA):</strong><br><span style='font-size: 20px; color: #8B4513; font-weight: bold;'>{h_wafat.upper()} {p_wafat.upper()}</span></div>", unsafe_allow_html=True)
    
    jarak_peringatan = {
        "Geblag (Hari H Wafat)": 0, "Nelung Dina (3 Hari)": 2, "Mitung Dina (7 Hari)": 6,
        "Matang Puluh (40 Hari)": 39, "Nyatus Dina (100 Hari)": 99, "Pendak I (1 Thn Jawa)": 353,
        "Pendak II (2 Thn Jawa)": 707, "Nyewu Dina (1000 Hari)": 999
    }
    
    data_tabel = []
    for nama, tambah in jarak_peringatan.items():
        tgl_hari_h = tgl_hitung + timedelta(days=tambah)
        h_h, p_h = hitung_weton_jawa_akurat(tgl_hari_h)
        tgl_kenduri = tgl_hari_h - timedelta(days=1)
        h_k, p_k = hitung_weton_jawa_akurat(tgl_kenduri)
        
        data_tabel.append({
            "Jenis Peringatan": nama,
            "Weton Hari H": f"{h_h} {p_h} ({tgl_hari_h.strftime('%d/%m/%Y')})",
            "Jadwal Kenduri (H-1 Malam)": f"{h_k} {p_k} ({tgl_kenduri.strftime('%d/%m/%Y')})"
        })
    st.table(data_tabel)
    tambah_tombol_pdf()

# ==========================================
# MODUL 5: SIKLUS & SELAMATAN BAYI
# ==========================================
elif menu_terpilih == "👶 Siklus & Selamatan Bayi":
    st.subheader("👶 SIKLUS KELAHIRAN BAYI")
    tgl_lahir_bayi = st.date_input("Tanggal Lahir Bayi:", value=datetime.today())
    tgl_bayi_dt = datetime.combine(tgl_lahir_bayi, datetime.min.time())
    hb, pb = hitung_weton_jawa_akurat(tgl_bayi_dt)
    
    selapan = tgl_bayi_dt + timedelta(days=35)
    h_sel, p_sel = hitung_weton_jawa_akurat(selapan)
    tedhak_siten = tgl_bayi_dt + timedelta(days=245)
    h_ted, p_ted = hitung_weton_jawa_akurat(tedhak_siten)
    
    st.markdown(f"""
    <div class="card-hasil">
        <h4>Kalender Siklus Kelahiran Bayi:</h4>
        <p>👶 Weton Kelahiran: <b>{hb} {pb}</b></p>
        <p>🍼 <b>Selapanan (35 Hari):</b> {selapan.strftime('%d/%m/%Y')} (Weton asli: <i>{h_sel} {p_sel}</i>)</p>
        <p>👣 <b>Tedhak Siten (Turun Tanah / 7 Selapan):</b> {tedhak_siten.strftime('%d/%m/%Y')} (Weton: <i>{h_ted} {p_ted}</i>)</p>
    </div>
    """, unsafe_allow_html=True)
    tambah_tombol_pdf()
