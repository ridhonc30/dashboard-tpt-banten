from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


def format_pp(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f} pp".replace(".", ",")


def render_footer() -> None:
    st.markdown(
        '<div class="footer">Dashboard TPT Provinsi Banten · Data BPS · Periode 2017–2024</div>',
        unsafe_allow_html=True,
    )


try:
    df = load_data()
except Exception as error:
    st.error(f"Gagal memuat dataset: {error}")
    st.stop()

# PENTING: baris "Provinsi Banten" adalah angka resmi TPT tingkat provinsi
# dari BPS (agregat), BUKAN rata-rata sederhana dari 8 kabupaten/kota.
# Kedua nilai ini berbeda karena bobot jumlah angkatan kerja tiap wilayah
# tidak sama, sehingga keduanya ditampilkan secara terpisah di dashboard.
regional_df = df[df["Kabupaten/Kota"] != "Provinsi Banten"].copy()
province_df = df[df["Kabupaten/Kota"] == "Provinsi Banten"].copy().sort_values("Tahun")

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
    st.markdown("**Cakupan**  \n8 kabupaten/kota + agregat provinsi")

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
        - Tren TPT resmi Provinsi Banten (angka agregat BPS) tahun 2017–2024.
        - Perbandingan TPT antar kabupaten/kota, termasuk perubahan tahunan (poin persentase & persen).
        - Ringkasan nilai rata-rata, tertinggi, dan terendah antarwilayah.
        - Peta sebaran (heatmap) TPT per kabupaten/kota tiap tahun.
        - Data aktual yang dapat disaring dan diunduh.
        """)
    with right:
        latest_year = int(province_df["Tahun"].max())
        latest_prov = province_df[province_df["Tahun"] == latest_year]["TPT"].iloc[0]
        st.markdown("#### TPT Provinsi Banten terbaru")
        m1, m2 = st.columns(2)
        m1.metric("Tahun terbaru", latest_year)
        m2.metric("TPT Provinsi Banten (BPS)", format_percent(latest_prov))
        st.caption(
            "Angka di atas adalah TPT resmi tingkat provinsi dari BPS, bukan "
            "rata-rata sederhana 8 kabupaten/kota."
        )
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
    filtered_prov = province_df[province_df["Tahun"].isin(selected_years)].copy()

    highest_row = filtered.loc[filtered["TPT"].idxmax()]
    lowest_row = filtered.loc[filtered["TPT"].idxmin()]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(
        "TPT Provinsi Banten (BPS, tahun terpilih)",
        format_percent(filtered_prov["TPT"].mean()) if not filtered_prov.empty else "-",
    )
    kpi2.metric("TPT tertinggi (kab/kota)", format_percent(highest_row["TPT"]), f'{highest_row["Kabupaten/Kota"]} · {int(highest_row["Tahun"])}', delta_color="off")
    kpi3.metric("TPT terendah (kab/kota)", format_percent(lowest_row["TPT"]), f'{lowest_row["Kabupaten/Kota"]} · {int(lowest_row["Tahun"])}', delta_color="off")
    kpi4.metric("Jumlah wilayah", filtered["Kabupaten/Kota"].nunique())
    st.caption(
        "KPI 'TPT Provinsi Banten' menggunakan angka agregat resmi BPS, bukan rata-rata "
        "dari 8 kabupaten/kota yang ditampilkan pada grafik perbandingan."
    )

    st.markdown("### Tren TPT Provinsi Banten (Data Resmi BPS)")
    prov_trend = filtered_prov.sort_values("Tahun").copy()
    prov_trend["Perubahan (pp)"] = prov_trend["TPT"].diff()
    prov_trend["Perubahan (%)"] = prov_trend["TPT"].pct_change() * 100

    line_fig = px.line(
        prov_trend, x="Tahun", y="TPT", markers=True,
        title="Tren TPT Provinsi Banten (Agregat BPS)",
        labels={"Tahun": "Tahun", "TPT": "TPT (%)"},
    )
    line_fig.update_traces(line_width=3)
    line_fig.update_layout(height=380, margin=dict(l=20, r=20, t=60, b=20), xaxis=dict(tickmode="array", tickvals=prov_trend["Tahun"].tolist()))
    st.plotly_chart(line_fig, use_container_width=True)

    if len(prov_trend) >= 2:
        awal = prov_trend.iloc[0]
        akhir = prov_trend.iloc[-1]
        total_pp = akhir["TPT"] - awal["TPT"]
        total_pct = (akhir["TPT"] - awal["TPT"]) / awal["TPT"] * 100
        naik_row = prov_trend.loc[prov_trend["Perubahan (pp)"].idxmax()] if prov_trend["Perubahan (pp)"].notna().any() else None
        turun_row = prov_trend.loc[prov_trend["Perubahan (pp)"].idxmin()] if prov_trend["Perubahan (pp)"].notna().any() else None
        ringkas = (
            f"Dari tahun {int(awal['Tahun'])} ({format_percent(awal['TPT'])}) ke tahun "
            f"{int(akhir['Tahun'])} ({format_percent(akhir['TPT'])}), TPT Provinsi Banten "
            f"berubah sebesar {format_pp(total_pp)} atau {total_pct:+.2f}%. "
        )
        if naik_row is not None:
            ringkas += (
                f"Kenaikan tahunan terbesar terjadi pada {int(naik_row['Tahun'])} "
                f"sebesar {format_pp(naik_row['Perubahan (pp)'])}. "
            )
        if turun_row is not None:
            ringkas += (
                f"Penurunan tahunan terbesar terjadi pada {int(turun_row['Tahun'])} "
                f"sebesar {format_pp(turun_row['Perubahan (pp)'])}."
            )
        st.info(ringkas)

    show_trend_table = st.checkbox("Tampilkan tabel perubahan tahunan TPT Provinsi Banten", value=True)
    if show_trend_table:
        trend_display = prov_trend[["Tahun", "TPT", "Perubahan (pp)", "Perubahan (%)"]].copy()
        trend_display["TPT"] = trend_display["TPT"].map(format_percent)
        trend_display["Perubahan (pp)"] = trend_display["Perubahan (pp)"].map(
            lambda v: format_pp(v) if pd.notna(v) else "-"
        )
        trend_display["Perubahan (%)"] = trend_display["Perubahan (%)"].map(
            lambda v: f"{v:+.2f}%" if pd.notna(v) else "-"
        )
        st.dataframe(trend_display, use_container_width=True, hide_index=True)

    st.markdown("### Perbandingan Antar Kabupaten/Kota")
    bar_data = filtered.groupby("Kabupaten/Kota", as_index=False)["TPT"].mean().sort_values("TPT", ascending=False)

    chart_left, chart_right = st.columns([1, 1.1])
    with chart_left:
        bar_fig = px.bar(
            bar_data,
            x="TPT",
            y="Kabupaten/Kota",
            orientation="h",
            title="Ranking Rata-rata TPT Kabupaten/Kota",
            labels={"Kabupaten/Kota": "Kabupaten/Kota", "TPT": "TPT (%)"},
            text=bar_data["TPT"].map(lambda value: f"{value:.2f}%"),
        )
        bar_fig.update_traces(textposition="outside")
        bar_fig.update_layout(
            height=420, margin=dict(l=20, r=20, t=60, b=20),
            yaxis=dict(categoryorder="total ascending"),
        )
        st.plotly_chart(bar_fig, use_container_width=True)
    with chart_right:
        heatmap_data = filtered.pivot_table(index="Kabupaten/Kota", columns="Tahun", values="TPT")
        heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=heatmap_data.values,
                x=[str(c) for c in heatmap_data.columns],
                y=heatmap_data.index,
                colorscale="YlOrRd",
                text=heatmap_data.round(2).values,
                texttemplate="%{text}",
                colorbar=dict(title="TPT (%)"),
            )
        )
        heatmap_fig.update_layout(
            title="Heatmap TPT per Kabupaten/Kota per Tahun",
            height=420, margin=dict(l=20, r=20, t=60, b=20),
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

    st.markdown(
        """
        <div class="note-box">
            Seluruh visual pada halaman ini mengikuti filter tahun dan kabupaten/kota, kecuali
            grafik "Tren TPT Provinsi Banten" yang selalu memakai angka resmi agregat BPS untuk
            tahun-tahun yang dipilih (tidak mengikuti filter kabupaten/kota, karena angka provinsi
            tidak dipecah per wilayah). Ranking dan heatmap menampilkan rata-rata TPT kabupaten/kota
            sesuai kabupaten/kota dan tahun yang dipilih.
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
    st.write("Data yang digunakan berasal dari Badan Pusat Statistik Provinsi Banten. Dataset mencakup TPT tahun 2017–2024 pada delapan kabupaten/kota di Provinsi Banten.")
    st.markdown(
        '<div class="note-box"><b>Catatan definisi:</b> baris <b>Provinsi Banten</b> adalah angka '
        'TPT tingkat provinsi yang dipublikasikan langsung oleh BPS (agregat), bukan hasil '
        'perhitungan rata-rata sederhana dari 8 kabupaten/kota pada dataset ini. Kedua angka '
        'tersebut dapat berbeda karena penghitungan TPT provinsi memperhitungkan bobot jumlah '
        'angkatan kerja tiap wilayah.</div>',
        unsafe_allow_html=True,
    )

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
