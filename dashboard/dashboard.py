from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="white")
GREY, HIGHLIGHT, ALERT = "#BFC5CC", "#1F6FB2", "#D1495B"

st.set_page_config(page_title="Dashboard Pelanggan Olist", page_icon="🛒", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    path = Path(__file__).parent / "main_data.csv"
    return pd.read_csv(path, dtype={"customer_zip_code_prefix": str})


def plot_top_states(df: pd.DataFrame, top_n: int):
    summary = (
        df.groupby("customer_state")["customer_unique_id"].nunique()
        .sort_values(ascending=False).head(top_n).iloc[::-1]
    )
    total = df["customer_unique_id"].nunique()
    colors = [HIGHLIGHT if i >= len(summary) - 5 else GREY for i in range(len(summary))]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(summary.index, summary.values, color=colors)
    for bar in bars:
        ax.text(bar.get_width() + summary.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():,.0f} ({bar.get_width() / total * 100:.1f}%)", va="center", fontsize=9)
    ax.set_xlim(0, summary.max() * 1.25)
    ax.set_xlabel("Jumlah pelanggan unik")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    sns.despine(left=True)
    plt.tight_layout()
    return fig


def plot_top_cities(df: pd.DataFrame, top_n: int):
    summary = (
        df.groupby(["customer_city", "customer_state"])["customer_unique_id"].nunique()
        .sort_values(ascending=False).head(top_n).iloc[::-1]
    )
    total = df["customer_unique_id"].nunique()
    labels = [f"{city.title()} ({state})" for city, state in summary.index]
    colors = [HIGHLIGHT if i == len(summary) - 1 else GREY for i in range(len(summary))]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(labels, summary.values, color=colors)
    for bar in bars:
        ax.text(bar.get_width() + summary.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():,.0f} ({bar.get_width() / total * 100:.1f}%)", va="center", fontsize=9)
    ax.set_xlim(0, summary.max() * 1.25)
    ax.set_xlabel("Jumlah pelanggan unik")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    sns.despine(left=True)
    plt.tight_layout()
    return fig


def plot_repeat_rate(df: pd.DataFrame):
    summary = (
        df.groupby("region")
        .agg(total=("customer_unique_id", "nunique"), repeat_rate=("is_repeat", "mean"))
        .assign(repeat_rate=lambda x: x["repeat_rate"] * 100)
        .sort_values("repeat_rate")
    )
    overall = df["is_repeat"].mean() * 100
    lowest = summary.index[0]
    colors = [HIGHLIGHT if r == lowest else GREY for r in summary.index]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(summary.index, summary["repeat_rate"], color=colors)
    label_x = max(summary["repeat_rate"].max(), overall) + 0.12
    for bar, n in zip(bars, summary["total"]):
        ax.text(label_x, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.2f}%  (n = {n:,.0f})", va="center", fontsize=9)
    ax.axvline(overall, color=ALERT, linestyle="--", linewidth=1.5)
    ax.text(overall + 0.03, -0.55, f"Rata-rata data terpilih {overall:.2f}%", color=ALERT, fontsize=9)
    ax.set_xlim(0, label_x * 1.6)
    ax.set_xlabel("Pelanggan dengan 2 order atau lebih (%)")
    sns.despine(left=True)
    plt.tight_layout()
    return fig


def plot_bubble_map(df: pd.DataFrame):
    geo = (
        df.groupby(["customer_state", "lat", "lon"])
        .agg(total=("customer_unique_id", "nunique"), repeat_rate=("is_repeat", "mean"))
        .reset_index()
    )
    geo["repeat_rate"] *= 100
    fig, ax = plt.subplots(figsize=(7, 7))
    sc = ax.scatter(geo["lon"], geo["lat"], s=geo["total"] / 25, c=geo["repeat_rate"],
                    cmap="YlOrRd", alpha=0.8, edgecolor="black", linewidth=0.6)
    for _, r in geo.iterrows():
        dy = 0 if r["total"] > 3000 else 0.9
        ax.text(r["lon"], r["lat"] + dy, r["customer_state"], ha="center", va="center", fontsize=7)
    fig.colorbar(sc, ax=ax, shrink=0.7).set_label("Repeat rate (%)")
    ax.set_xlabel("Longitude (pusat state, perkiraan)")
    ax.set_ylabel("Latitude (pusat state, perkiraan)")
    ax.set_aspect("equal")
    plt.tight_layout()
    return fig


def plot_segments(df: pd.DataFrame):
    order = ["One-time (1 order)", "Repeat (2 order)", "Loyal (3+ order)"]
    seg = pd.crosstab(df["region"], df["customer_segment"], normalize="index")[order] * 100
    fig, ax = plt.subplots(figsize=(8, 4.5))
    seg.plot(kind="barh", stacked=True, ax=ax, color=["#D9DEE3", "#7FB2DC", HIGHLIGHT], width=0.7)
    ax.set_xlabel("Persentase pelanggan (%)")
    ax.set_ylabel("")
    ax.set_xlim(0, 100)
    ax.legend(title="Segmen", loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)
    sns.despine(left=True)
    plt.tight_layout()
    return fig


# ----------------------------- Layout -----------------------------
data = load_data()

st.title("🛒 Dashboard Pelanggan E-Commerce Olist (Brasil)")
st.caption("Dataset: Brazilian E-Commerce Public Dataset by Olist (data pelanggan, periode 2016-2018)")

with st.sidebar:
    st.header("Filter")
    regions = sorted(data["region"].unique())
    selected_regions = st.multiselect("Region", regions, default=regions)
    top_state_n = st.slider("Jumlah state ditampilkan", 5, 15, 10)
    top_city_n = st.slider("Jumlah kota ditampilkan", 5, 20, 10)
    st.markdown("---")
    st.caption("Satu baris data = satu pelanggan unik (`customer_unique_id`). "
               "Pelanggan repeat = pelanggan dengan 2 order atau lebih.")

filtered = data[data["region"].isin(selected_regions)]

if filtered.empty:
    st.warning("Pilih minimal satu region pada sidebar.")
    st.stop()

# Ringkasan (metric cards)
total_customers = filtered["customer_unique_id"].nunique()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total pelanggan unik", f"{total_customers:,.0f}")
c2.metric("Jumlah state", f"{filtered['customer_state'].nunique()}")
c3.metric("Jumlah kota", f"{filtered.groupby(['customer_city', 'customer_state']).ngroups:,.0f}")
c4.metric("Repeat rate", f"{filtered['is_repeat'].mean() * 100:.2f}%")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. State teratas", "2. Kota teratas", "3. Repeat rate per region", "4. Peta & segmen pelanggan"
])

with tab1:
    st.subheader("State mana dengan pelanggan unik terbanyak?")
    top5 = (
        filtered.groupby("customer_state")["customer_unique_id"].nunique()
        .sort_values(ascending=False).head(5)
    )
    st.markdown(f"**5 state teratas menyumbang {top5.sum() / total_customers * 100:.1f}% pelanggan** "
                f"pada data terpilih: {', '.join(top5.index)}.")
    st.pyplot(plot_top_states(filtered, top_state_n))

with tab2:
    st.subheader("Kota mana dengan pelanggan unik terbanyak?")
    city_counts = (
        filtered.groupby(["customer_city", "customer_state"])["customer_unique_id"].nunique()
        .sort_values(ascending=False).head(top_city_n)
    )
    st.markdown(f"**{top_city_n} kota teratas menyumbang {city_counts.sum() / total_customers * 100:.1f}% pelanggan** "
                "pada data terpilih.")
    st.pyplot(plot_top_cities(filtered, top_city_n))

with tab3:
    st.subheader("Berapa repeat rate tiap region?")
    st.pyplot(plot_repeat_rate(filtered))
    st.info("Repeat rate = persentase pelanggan unik yang melakukan 2 order atau lebih. "
            "Garis putus-putus menunjukkan rata-rata dari region yang dipilih.")

with tab4:
    left, right = st.columns(2)
    with left:
        st.subheader("Persebaran pelanggan per state")
        st.pyplot(plot_bubble_map(filtered))
        st.caption("Koordinat adalah perkiraan titik pusat state, bukan lokasi pelanggan sebenarnya.")
    with right:
        st.subheader("Segmen pelanggan per region")
        st.pyplot(plot_segments(filtered))
        st.caption("Binning berdasarkan jumlah order: One-time (1), Repeat (2), Loyal (3+).")

st.caption("Proyek Analisis Data - Belajar Fundamental Analisis Data (Dicoding)")
