from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard TPT Banten",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).parent / "tpt_banten_2017_2024.csv"

st.markdown(
    """
    <style>
        /* ===== Tampilan utama ===== */
        .stApp {
            background: var(--background-color) !important;
            color: var(--text-color) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f2f57 0%, #174f78 100%) !important;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stRadio label {
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 8px 10px;
            margin-bottom: 6px;
        }

        /* ===== Hero / Banner Beranda ===== */
        .hero {
            padding: 2.2rem 2.4rem;
            border-radius: 24px;
            background:
                radial-gradient(circle at 90% 15%, rgba(255,255,255,0.26), transparent 25%),
                linear-gradient(135deg, #0f2f57 0%, #1472a6 100%);
            color: white;
            margin-bottom: 1.4rem;
            box-shadow: 0 14px 34px rgba(15, 47, 87, 0.20);
        }

        .hero h1 {
            margin: 0 0 0.65rem 0;
            font-size: 2.35rem;
            line-height: 1.15;
            color: #ffffff !important;
        }

        .hero p {
            margin: 0;
            max-width: 760px;
            font-size: 1.04rem;
            opacity: 0.93;
            color: #ffffff !important;
        }

        .eyebrow {
            display: inline-block;
            padding: 0.34rem 0.72rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            font-size: 0.82rem;
            font-weight: 600;
            margin-bottom: 0.85rem;
            color: #ffffff !important;
        }

        /* ===== Kartu informasi ===== */
        .info-card {
            min-height: 118px;
            padding: 1.15rem 1.2rem;
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 18px;
            background: var(--secondary-background-color) !important;
            box-shadow: 0 8px 22px rgba(20, 54, 86, 0.07);
        }

        .info-label {
            color: rgba(128, 128, 128, 0.95) !important;
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }

        .info-value {
            color: var(--text-color) !important;
            font-size: 1.18rem;
            font-weight: 700;
        }

        /* ===== Kotak catatan ===== */
        .note-box {
            padding: 1rem 1.1rem;
            border-radius: 14px;
            border-left: 5px solid #1a77a8;
            background: rgba(26, 119, 168, 0.12) !important;
            color: var(--text-color) !important;
            margin: 0.7rem 0 1rem;
        }

        /* ===== KPI Metric ===== */
        div[data-testid="stMetric"] {
            background: var(--secondary-background-color) !important;
            border: 1px solid rgba(128, 128, 128, 0.22);
            padding: 1rem;
            border-radius: 16px;
            box-shadow: 0 7px 18px rgba(20, 54, 86, 0.06);
            color: var(--text-color) !important;
        }

        div[data-testid="stMetric"] * {
            color: var(--text-color) !important;
        }

        /* ===== Footer custom ===== */
        .footer {
            text-align: center;
            color: rgba(128, 128, 128, 0.95) !important;
            font-size: 0.82rem;
            padding: 2.2rem 0 0.8rem;
        }

        .block-container {
            padding-top: 1.7rem;
            padding-bottom: 2rem;
        }

        /* ===== Sembunyikan menu bawaan Streamlit ===== */
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    required_columns = {"Tahun", "Kabupaten/Kota", "TPT"}
    if not required_columns.issubset(data.columns):
        missing = required_columns.difference(data.columns)
        raise ValueError(f"Kolom dataset belum lengkap: {', '.join(sorted(missing))}")
    data["Tahun"] = pd.to_numeric(data["Tahun"], errors="coerce")
    data["TPT"] = pd.to_numeric(data["TPT"], errors="coerce")
    data = data.dropna(subset=["Tahun", "Kabupaten/Kota", "TPT"]).copy()
    data["Tahun"] = data["Tahun"].astype(int)
    return data.sort_values(["Tahun", "Kabupaten/Kota"]).reset_index(drop=True)

def format_percent(value: float) -> str:
    return f"{value:.2f}%".replace(".", ",")

def render_footer() -> None:
    st.markdown('<div class="footer">Dashboard TPT Provinsi Banten · Data BPS · Periode 2017–2024</div>', unsafe_allow_html=True)

try:
    df = load_data()
except Exception as error:
    st.error(f"Gagal memuat dataset: {error}")
    st.stop()

regional_df = df[df["Kabupaten/Kota"] != "Provinsi Banten"].copy()
province_df = df[df["Kabupaten/Kota"] == "Provinsi Banten"].copy()

with st.sidebar:
    st.markdown("## 📊 TPT Banten")
    st.caption("Dashboard visualisasi dan analisis tren")
    st.markdown("---")
    page = st.radio(
        "Navigasi",
        ["🏠 Beranda", "📈 Dashboard TPT", "🗂️ Tentang Data"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Sumber data**  \nBPS Provinsi Banten")
    st.markdown("**Periode**  \n2017–2024")
    st.markdown("**Cakupan**  \n8 kabupaten/kota")

if page == "🏠 Beranda":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Visualisasi data ketenagakerjaan</div>
            <h1>Dashboard Tingkat Pengangguran Terbuka Provinsi Banten</h1>
            <p>
                Website ini menyajikan visualisasi dan analisis tren Tingkat Pengangguran
                Terbuka berdasarkan kabupaten/kota di Provinsi Banten selama periode
                2017–2024. Data bersumber dari Badan Pusat Statistik dan disajikan secara
                interaktif agar lebih mudah dipahami.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="info-card"><div class="info-label">Periode data</div><div class="info-value">2017–2024</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card"><div class="info-label">Cakupan wilayah</div><div class="info-value">8 Kabupaten/Kota</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="info-card"><div class="info-label">Sumber data</div><div class="info-value">BPS Provinsi Banten</div></div>', unsafe_allow_html=True)

    st.markdown("### Gambaran website")
    st.write("Dashboard membantu pengguna melihat perubahan TPT dari tahun ke tahun, membandingkan kondisi antarwilayah, serta meninjau data aktual yang digunakan.")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("#### Informasi yang tersedia")
        st.markdown("""
        - Tren TPT Provinsi Banten tahun 2017–2024.
        - Perbandingan TPT antar kabupaten/kota.
        - Ringkasan nilai rata-rata, tertinggi, dan terendah.
        - Proporsi TPT berdasarkan kabupaten/kota.
        - Data aktual yang dapat disaring dan diunduh.
        """)
    with right:
        latest_year = int(regional_df["Tahun"].max())
        latest_data = regional_df[regional_df["Tahun"] == latest_year]
        st.markdown("#### Ringkasan data terbaru")
        m1, m2 = st.columns(2)
        m1.metric("Tahun terbaru", latest_year)
        m2.metric("Rata-rata TPT", format_percent(latest_data["TPT"].mean()))
    st.markdown('<div class="note-box">Penelitian difokuskan pada visualisasi dan analisis tren. Website ini tidak melakukan prediksi atau peramalan TPT pada tahun berikutnya.</div>', unsafe_allow_html=True)
    render_footer()

elif page == "📈 Dashboard TPT":
    st.title("Dashboard TPT Provinsi Banten")
    st.caption("Visualisasi Tingkat Pengangguran Terbuka berdasarkan tahun dan kabupaten/kota.")

    all_years = sorted(regional_df["Tahun"].unique().tolist())
    all_regions = sorted(regional_df["Kabupaten/Kota"].unique().tolist())

    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        selected_years = st.multiselect("Pilih tahun", options=all_years, default=all_years)
    with filter_col2:
        selected_regions = st.multiselect("Pilih kabupaten/kota", options=all_regions, default=all_regions)

    if not selected_years or not selected_regions:
        st.warning("Pilih minimal satu tahun dan satu kabupaten/kota.")
        st.stop()

    filtered = regional_df[
        regional_df["Tahun"].isin(selected_years)
        & regional_df["Kabupaten/Kota"].isin(selected_regions)
    ].copy()

    highest_row = filtered.loc[filtered["TPT"].idxmax()]
    lowest_row = filtered.loc[filtered["TPT"].idxmin()]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Rata-rata TPT", format_percent(filtered["TPT"].mean()))
    kpi2.metric("TPT tertinggi", format_percent(highest_row["TPT"]), f'{highest_row["Kabupaten/Kota"]} · {int(highest_row["Tahun"])}', delta_color="off")
    kpi3.metric("TPT terendah", format_percent(lowest_row["TPT"]), f'{lowest_row["Kabupaten/Kota"]} · {int(lowest_row["Tahun"])}', delta_color="off")
    kpi4.metric("Jumlah wilayah", filtered["Kabupaten/Kota"].nunique())

    st.markdown("### Visualisasi Data TPT")
    line_data = filtered.groupby("Tahun", as_index=False)["TPT"].mean().sort_values("Tahun")
    bar_data = filtered.groupby("Kabupaten/Kota", as_index=False)["TPT"].mean().sort_values("TPT", ascending=False)
    pie_data = bar_data.copy()

    chart_left, chart_right = st.columns([1.1, 1])
    with chart_left:
        line_fig = px.line(line_data, x="Tahun", y="TPT", markers=True, title="Tren Rata-rata TPT", labels={"Tahun": "Tahun", "TPT": "TPT (%)"})
        line_fig.update_traces(line_width=3)
        line_fig.update_layout(height=420, margin=dict(l=20, r=20, t=60, b=20), xaxis=dict(tickmode="array", tickvals=line_data["Tahun"].tolist()))
        st.plotly_chart(line_fig, use_container_width=True)
    with chart_right:
        pie_fig = px.pie(pie_data, names="Kabupaten/Kota", values="TPT", title="Proporsi Rata-rata TPT Kabupaten/Kota", hole=0.35)
        pie_fig.update_layout(height=420, margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(pie_fig, use_container_width=True)

    bar_fig = px.bar(
        bar_data,
        x="Kabupaten/Kota",
        y="TPT",
        title="Perbandingan Rata-rata TPT Kabupaten/Kota",
        labels={"Kabupaten/Kota": "Kabupaten/Kota", "TPT": "TPT (%)"},
        text=bar_data["TPT"].map(lambda value: f"{value:.2f}%"),
    )
    bar_fig.update_traces(textposition="outside")
    bar_fig.update_layout(height=460, margin=dict(l=20, r=20, t=60, b=100), xaxis_tickangle=-35)
    st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown(
        """
        <div class="note-box">
            Seluruh visual pada halaman ini mengikuti filter tahun dan kabupaten/kota.
            Jika hanya satu tahun dipilih, line chart akan menampilkan titik data pada tahun tersebut.
            Jika beberapa tahun dipilih, line chart akan menampilkan tren berdasarkan rentang tahun yang dipilih.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Data aktual")
    show_data = st.checkbox("Tampilkan data aktual", value=True)
    if show_data:
        display_df = filtered.sort_values(["Tahun", "Kabupaten/Kota"]).reset_index(drop=True)
        formatted_df = display_df.copy()
        formatted_df["TPT"] = formatted_df["TPT"].map(format_percent)
        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
        csv_data = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("Unduh data terfilter (CSV)", data=csv_data, file_name="data_tpt_banten_terfilter.csv", mime="text/csv")
    render_footer()

elif page == "🗂️ Tentang Data":
    st.title("Tentang Data")
    st.caption("Informasi mengenai sumber, cakupan, struktur, dan pengolahan dataset.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah baris", len(df))
    col2.metric("Periode", "2017–2024")
    col3.metric("Kabupaten/Kota", regional_df["Kabupaten/Kota"].nunique())
    col4.metric("Kolom dataset", len(df.columns))

    st.markdown("### Sumber dan cakupan")
    st.write("Data yang digunakan berasal dari Badan Pusat Statistik Provinsi Banten. Dataset mencakup TPT tahun 2017–2024 pada delapan kabupaten/kota di Provinsi Banten. Baris **Provinsi Banten** dipertahankan sebagai data agregat provinsi dan tidak dihitung sebagai kabupaten/kota.")

    st.markdown("### Struktur dataset")
    structure_df = pd.DataFrame({
        "Kolom": ["Tahun", "Kabupaten/Kota", "TPT"],
        "Keterangan": ["Tahun pengamatan data.", "Nama kabupaten/kota atau agregat Provinsi Banten.", "Persentase Tingkat Pengangguran Terbuka."],
    })
    st.dataframe(structure_df, use_container_width=True, hide_index=True)

    st.markdown("### Proses pengolahan")
    st.write("Data tahunan melalui proses pembersihan, pemilihan kolom, penyesuaian format, penambahan atribut tahun, serta penggabungan menggunakan Python dan Pandas sebelum digunakan pada dashboard dan website.")

    st.markdown("### Pratinjau dataset")
    preview_option = st.radio("Pilih tampilan", ["Kabupaten/Kota", "Agregat Provinsi Banten"], horizontal=True)
    preview_df = regional_df if preview_option == "Kabupaten/Kota" else province_df
    preview_formatted = preview_df.copy()
    preview_formatted["TPT"] = preview_formatted["TPT"].map(format_percent)
    st.dataframe(preview_formatted.reset_index(drop=True), use_container_width=True, hide_index=True)
    full_csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Unduh dataset lengkap (CSV)", data=full_csv, file_name="tpt_banten_2017_2024.csv", mime="text/csv")
    render_footer()
