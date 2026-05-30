import streamlit as st
import pandas as pd
import sqlite3
import bcrypt
import matplotlib.pyplot as plt

# ======================================
# KONFIGURASI HALAMAN
# ======================================
st.set_page_config(
    page_title='Cluster Tunggakan PDAM',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# ======================================
# CSS GLOBAL & KUSTOMISASI ELEMEN (LAYOUT DASHBOARD PERSIS GAMBAR)
# ======================================
st.markdown("""
<style>
/* Sembunyikan elemen bawaan Streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
[data-testid="stSidebar"] {display: none !important;} /* Sembunyikan default sidebar */

.stApp {
    background-color:#ffffff;
}

/* Input Field styling */
.stTextInput > div > div > input {
    border-radius:10px;
    height: 45px;
    font-size: 16px;
}

/* Kustomisasi Teks Link Navigasi Bawah Sebaris Rapi */
.footer-text-container {
    text-align: center;
    font-size: 16px;
    color: #374151;
    margin-top: 15px;
}

.custom-link {
    color: #1aa1e2 !important;
    text-decoration: underline !important;
    cursor: pointer;
    font-weight: normal;
    background: none;
    border: none;
    padding: 0;
    display: inline;
}

.custom-link:hover {
    color: #1588c2 !important;
}

/* CSS Global untuk Tombol */
div.stButton > button {
    text-decoration: none !important;
}

/* Header Dashboard Kustom - Teks Diperbarui */
.dashboard-header {
    background-color: #1aa1e2;
    color: white;
    text-align: center;
    padding: 20px 15px;
    font-size: 26px;
    font-weight: bold;
    letter-spacing: 1px;
    margin-bottom: 0px;
    border-bottom: 2px solid #000000;
    text-transform: uppercase;
}

/* Panel Navigasi Kiri (Border Pemisah Vertikal Hitam) */
.nav-container {
    border-right: 2px solid #000000;
    height: 100%;
    padding-right: 20px;
}

/* Info Tentang PDAM di halaman utama (Diperbarui dengan Logo Stop Menunggak) */
.tentang-pdam-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 65vh;
    text-align: center;
}

.stop-pay-container {
    background-color: #fff5f5;
    border: 5px solid #dc2626;
    border-radius: 50%;
    width: 240px;
    height: 240px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0px 8px 20px rgba(220, 38, 38, 0.2);
}

.stop-pay-icon {
    font-size: 70px;
    line-height: 1;
    margin-bottom: 5px;
}

.stop-pay-text {
    color: #dc2626;
    font-size: 18px;
    font-weight: 900;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* Styling Tombol Menu Navigasi di Kolom Kiri secara Otomatis */
div[data-testid="column"]:first-of-type button {
    background-color: #1aa1e2 !important;
    color: white !important;
    border-radius: 4px !important;
    height: 60px !important;
    width: 100% !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 1px solid #000000 !important;
    margin-bottom: 15px !important;
    text-transform: uppercase;
}

div[data-testid="column"]:first-of-type button:hover {
    background-color: #1588c2 !important;
}

/* Menargetkan Tombol LOGOUT (Tombol terakhir di Kolom Kiri) agar berwarna Merah Marun */
div[data-testid="column"]:first-of-type div[data-testid="stButton"]:last-of-type button {
    background-color: #8B001A !important;
    border: 1px solid #000000 !important;
}

div[data-testid="column"]:first-of-type div[data-testid="stButton"]:last-of-type button:hover {
    background-color: #6B0014 !important;
}
</style>
""", unsafe_allow_html=True)

# Sembunyikan default sidebar secara mutlak via CSS
st.markdown("<style>[data-testid='stSidebarNav'] {display: none !important;}</style>", unsafe_allow_html=True)

# ======================================
# DATABASE SQLITE
# ======================================
conn = sqlite3.connect(
    'users.db',
    check_same_thread=False
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password BLOB
)
''')
conn.commit()

# ======================================
# INITIAL STATE MANAGEMENT
# ======================================
if 'login' not in st.session_state:
    st.session_state.login = False

if "action" in st.query_params:
    st.session_state.menu = st.query_params["action"]

if 'menu' not in st.session_state:
    st.session_state.menu = 'Login'

# State untuk menu aktif di dalam dashboard
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Home'

# ======================================
# HALAMAN UTAMA (LOGIN / REGISTER)
# ======================================
if not st.session_state.login:
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # Grid susunan form di tengah
    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:
        # FORM: LOGIN
        if st.session_state.menu == 'Login':
            st.markdown("""
            <div style='text-align: center; margin-bottom: 40px;'>
                <h2 style='color:#1f2937; font-size:26px; font-weight:800; letter-spacing: 1px;'>
                    LOGIN APLIKASI CLUSTER
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input(
                'Username',
                placeholder='username',
                label_visibility='collapsed',
                key='input_user'
            )
            
            st.write("")

            password = st.text_input(
                'Password',
                type='password',
                placeholder='password',
                label_visibility='collapsed',
                key='input_pass'
            )

            st.write("")
            st.write("")

            # CSS khusus tombol login biru cerah di form login luar
            st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: #1aa1e2 !important;
                color: white !important;
                border-radius: 8px !important;
                height: 46px !important;
                width: 100% !important;
                font-size: 16px !important;
                font-weight: bold !important;
                border: none !important;
            }
            div.stButton > button:first-child:hover {
                background-color: #1588c2 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            if st.button('Login', use_container_width=True):
                cursor.execute(
                    'SELECT * FROM users WHERE username=?',
                    (username,)
                )
                user = cursor.fetchone()

                if user:
                    if bcrypt.checkpw(password.encode(), user[2]):
                        st.session_state.login = True
                        st.session_state.active_tab = 'Home'  # Kembali ke halaman tentang pdam
                        st.query_params.clear()
                        st.success('Login berhasil!')
                        st.rerun()
                    else:
                        st.error('Password salah.')
                else:
                    st.error('Username tidak ditemukan.')

            st.write("")
            
            st.markdown("""
            <div class='footer-text-container'>
                <span>Belum Punya Akun / </span><a href='?action=Daftar+Akun' target='_self' class='custom-link'>Daftar Akun</a>
            </div>
            """, unsafe_allow_html=True)

        # FORM: DAFTAR AKUN
        elif st.session_state.menu == 'Daftar Akun':
            st.markdown("<h2 style='color:#1f2937; margin-bottom:35px; font-size:24px; font-weight:800; text-align:center;'>DAFTAR AKUN ADMIN</h2>", unsafe_allow_html=True)

            username_baru = st.text_input(
                'Username Baru',
                placeholder='Masukkan username baru',
                label_visibility='collapsed',
                key='reg_user'
            )
            
            st.write("")

            password_baru = st.text_input(
                'Password Baru',
                type='password',
                placeholder='Masukkan password baru',
                label_visibility='collapsed',
                key='reg_pass'
            )

            st.write("")
            st.write("")

            # CSS khusus agar tombol Daftar berwarna biru cerah
            st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: #1aa1e2 !important;
                color: white !important;
                border-radius: 8px !important;
                height: 46px !important;
                width: 100% !important;
                font-size: 16px !important;
                font-weight: bold !important;
                border: none !important;
            }
            div.stButton > button:first-child:hover {
                background-color: #1588c2 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            if st.button('Daftar', use_container_width=True):
                cursor.execute(
                    'SELECT * FROM users WHERE username=?',
                    (username_baru,)
                )
                cek = cursor.fetchone()

                if cek:
                    st.error('Username sudah digunakan!')
                else:
                    hash_password = bcrypt.hashpw(password_baru.encode(), bcrypt.gensalt())
                    cursor.execute(
                        'INSERT INTO users(username, password) VALUES (?,?)',
                        (username_baru, hash_password)
                    )
                    conn.commit()
                    st.success('Akun berhasil dibuat!')
                    st.query_params.clear()
                    st.session_state.menu = 'Login'
                    st.rerun()
            
            st.write("")
            
            st.markdown("""
            <div class='footer-text-container'>
                <a href='?action=Login' target='_self' class='custom-link'>Kembali ke Halaman Login</a>
            </div>
            """, unsafe_allow_html=True)

# ======================================
# DASHBOARD UTAMA (SETELAH LOGIN)
# ======================================
else:
    # 1. Header Atas Diperbarui sesuai permintaan Anda
    st.markdown("<div class='dashboard-header'>APLIKASI CLUSTER TUNGGAKAN PELANGGAN PDAM TIRTA MUARE ULAKAN SAMBAS</div>", unsafe_allow_html=True)
    st.write("")

    # 2. Pembagian Layout Kolom Kiri (Navigasi) & Kolom Kanan (Konten Utama)
    col_nav, col_content = st.columns([1, 3])

    # --------------------------------------
    # PANEL NAVIGASI (KOLOM KIRI)
    # --------------------------------------
    with col_nav:
        st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
        
        # Tombol Kembali Ke Dashboard (Home) - Ditambahkan Ikon & Warna diatur CSS
        if st.button("📊 DASHBOARD", key="btn_home", use_container_width=True):
            st.session_state.active_tab = "Home"
            st.rerun()

        st.write("")

        # Tombol Upload Data - Ditambahkan Ikon & Warna diatur CSS
        if st.button("📥 UPLOAD DATA", key="btn_upload", use_container_width=True):
            st.session_state.active_tab = "Upload Data"
            st.rerun()

        st.write("")

        # Tombol Analisis Data - Ditambahkan Ikon & Warna diatur CSS
        if st.button("⚙️ ANALISIS DATA", key="btn_analisis", use_container_width=True):
            st.session_state.active_tab = "Analisis Data"
            st.rerun()

        st.write("")

        # Tombol Lihat Hasil - Ditambahkan Ikon & Warna diatur CSS
        if st.button("👁️ LIHAT HASIL", key="btn_hasil", use_container_width=True):
            st.session_state.active_tab = "Lihat Hasil"
            st.rerun()

        st.write("")
        st.write("")

        # Tombol Logout - Ditambahkan Ikon (Warna Merah Marun dipertahankan via CSS)
        if st.button("🚪 LOGOUT", key="btn_logout", use_container_width=True):
            st.session_state.login = False
            st.session_state.active_tab = "Home"
            st.success('Logout berhasil')
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # AREA KONTEN UTAMA (KOLOM KANAN)
    # --------------------------------------
    with col_content:
        
        # TAB DEFAULT / HOME: LOGO PERINGATAN "STOP MENUNGGAK"
        if st.session_state.active_tab == "Home":
            st.markdown("""
            <div class='tentang-pdam-box'>
                <div class='stop-pay-container'>
                    <div class='stop-pay-icon'>⚠️💳</div>
                    <div class='stop-pay-text'>STOP<br>MENUNGGAK</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # TAB: UPLOAD DATA
        elif st.session_state.active_tab == "Upload Data":
            st.subheader('Upload Dataset')

            uploaded_file = st.file_uploader(
                'Upload CSV / Excel',
                type=['csv', 'xlsx']
            )

            if uploaded_file is not None:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Rapikan nama kolom
                df.columns = (
                    df.columns
                    .str.strip()
                    .str.lower()
                    .str.replace(' ', '_')
                )

                st.session_state.df = df
                st.success('Data berhasil diupload')
                st.dataframe(df, use_container_width=True)

        # TAB: ANALISIS DATA
        elif st.session_state.active_tab == "Analisis Data":
            st.subheader('Cleansing dan Transformasi Data')

            if 'df' in st.session_state:
                df = st.session_state.df.copy()

                # ======================================
                # CLEANSING 
                # ======================================
                df['id_pelanggan'] = df['id_pelanggan'].ffill()
                df = df.fillna(0)

                # Hilangkan spasi
                for col in df.select_dtypes(include='object').columns:
                    df[col] = df[col].astype(str).str.strip()

                # Ganti simbol kosong
                df = df.replace(['-', ' -', '- ', '–', '--', ''], 0)

                # Hapus duplikat
                df = df.drop_duplicates()

                # Konversi total
                df['total'] = pd.to_numeric(df['total'], errors='coerce').fillna(0)

                st.success('Cleansing berhasil')

                # ======================================
                # TRANSFORMASI 
                # ======================================
                df['jatuh_tempo'] = pd.to_datetime(df['jatuh_tempo'])
                df['tahun'] = df['jatuh_tempo'].dt.year
                df['tutup_buku'] = pd.to_datetime(df['tahun'].astype(str) + '-12-31')
                df['hari_tunggakan'] = (df['tutup_buku'] - df['jatuh_tempo']).dt.days

                st.success('Transformasi berhasil')
                st.session_state.clean_df = df
                st.dataframe(df, use_container_width=True)

                # ======================================
                # ANALISIS CLUSTERING 
                # ======================================
                st.write("---")
                st.subheader('Analisis Clustering')

                if 'clean_df' in st.session_state:
                    df_cluster = st.session_state.clean_df.copy()

                    # KATEGORI TUNGGAKAN
                    def kategori_tunggakan(hari):
                        if hari <= 90:
                            return 'Dalam Perhatian Khusus'
                        elif hari <= 180:
                            return 'Kurang Lancar'
                        elif hari <= 270:
                            return 'Diragukan'
                        else:
                            return 'Macet'

                    df_cluster['cluster'] = df_cluster['hari_tunggakan'].apply(kategori_tunggakan)
                    st.session_state.cluster_df = df_cluster

                    st.success('Clustering berhasil')
                    st.dataframe(
                        df_cluster[['id_pelanggan', 'hari_tunggakan', 'cluster']],
                        use_container_width=True
                    )
            else:
                st.warning('Upload data terlebih dahulu')

        # TAB: LIHAT HASIL
        elif st.session_state.active_tab == "Lihat Hasil":
            
            if 'cluster_df' in st.session_state:
                df = st.session_state.cluster_df

                # ======================================
                # METRIK DASHBOARD
                # ======================================
                st.subheader('Ringkasan Data')

                col1, col2, col3 = st.columns(3)

                col1.metric('Jumlah Data', len(df))

                col2.metric('Jumlah Pelanggan', df['id_pelanggan'].nunique())

                col3.metric('Total Tunggakan', int(df['total'].sum()))

                # ======================================
                # VISUALISASI CLUSTER
                # ======================================
                st.subheader('Visualisasi Hasil Clustering')

                warna = {
                    'Dalam Perhatian Khusus': 'green',
                    'Kurang Lancar': 'yellow',
                    'Diragukan': 'orange',
                    'Macet': 'red'
                }

                fig1, ax1 = plt.subplots(figsize=(12, 8))

                for kategori in warna:
                    subset = df[df['cluster'] == kategori]
                    ax1.scatter(
                        subset['hari_tunggakan'],
                        subset['total'],
                        color=warna[kategori],
                        label=kategori
                    )

                ax1.set_title('Visualisasi Cluster Pelanggan PDAM')
                ax1.set_xlabel('Hari Tunggakan')
                ax1.set_ylabel('Total Tagihan')
                ax1.legend()

                st.pyplot(fig1)

                # ======================================
                # JUMLAH DATA TIAP CLUSTER
                # ======================================
                st.subheader('Jumlah Data Tiap Cluster')

                cluster_count = df['cluster'].value_counts()

                st.bar_chart(cluster_count)
                st.dataframe(cluster_count)

                # ======================================
                # DISTRIBUSI GOLONGAN
                # ======================================
                st.subheader('Distribusi Berdasarkan ID Golongan')

                tabel_golongan = pd.crosstab(df['id_golongan'], df['cluster'])

                st.bar_chart(tabel_golongan)
                st.dataframe(tabel_golongan)

                # ======================================
                # VISUALISASI TUNGGAKAN PER TAHUN
                # ======================================
                st.subheader('Jumlah Tunggakan Berdasarkan Tahun')

                # Hitung jumlah data per tahun
                data_tahun = (
                    df.groupby('tahun')['hari_tunggakan']
                    .count()
                    .sort_index()
                )

                # Figure
                fig2, ax2 = plt.subplots(figsize=(12, 6))

                # Grafik batang
                bars = ax2.bar(
                    data_tahun.index.astype(str),
                    data_tahun.values
                )

                # Judul
                ax2.set_title('Jumlah Tunggakan Berdasarkan Tahun', fontsize=16)
                ax2.set_xlabel('Tahun', fontsize=12)
                ax2.set_ylabel('Jumlah Data Tunggakan', fontsize=12)

                # Grid
                ax2.grid(axis='y', linestyle='--', alpha=0.5)

                # Tambahkan angka
                for bar in bars:
                    yval = bar.get_height()
                    ax2.text(
                        bar.get_x() + bar.get_width() / 2,
                        yval + 5,
                        int(yval),
                        ha='center',
                        fontsize=10
                    )

                st.pyplot(fig2)

                # Simpan gambar
                fig2.savefig('tunggakan_per_tahun.png', dpi=300, bbox_inches='tight')

                # ======================================
                # DOWNLOAD HASIL
                # ======================================
                st.subheader('Download Hasil')

                csv = df.to_csv(index=False).encode('utf-8')

                st.download_button(
                    label='Download CSV',
                    data=csv,
                    file_name='hasil_cluster.csv',
                    mime='text/csv'
                )

            else:
                st.warning('Belum ada hasil clustering')