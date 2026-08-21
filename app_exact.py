from io import BytesIO
import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RM Equity NS Strategy Lab",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS / THEME
# ============================================================

GOLD = "#D4AF37"
GOLD2 = "#BFA24A"
TEXT = "#F3F0E7"
MUTED = "#9F9B90"
CARD = "#111111"
GRID = "rgba(212,175,55,.12)"
BORDER = "rgba(212,175,55,.24)"

# FINAL workbook formula: PBT / Revenue = Net Sales * 0.6%
REVENUE_FACTOR = 0.6 / 100.0

MONTHS = {
    1: "July",
    2: "August",
    3: "September",
    4: "October",
    5: "November",
    6: "December",
    7: "January",
    8: "February",
    9: "March",
}


st.markdown(
    """
<style>
.stApp {background:#070707;color:#F3F0E7;}
[data-testid="stSidebar"] {background:#0B0B0B;border-right:1px solid rgba(212,175,55,.24);}
[data-testid="stSidebar"] * {color:#F3F0E7;}
.hero {border:1px solid rgba(212,175,55,.24);border-radius:22px;padding:24px 26px;margin-bottom:18px;background:linear-gradient(110deg,rgba(212,175,55,.10),rgba(255,255,255,.015));}
.eyebrow {color:#D4AF37;font-size:.76rem;letter-spacing:.17em;font-weight:750;text-transform:uppercase;margin-bottom:8px;}
.hero-title {font-size:clamp(1.9rem,3vw,3rem);line-height:1.05;font-weight:760;}
.hero-sub {color:#AAA69A;margin-top:10px;font-size:.94rem;line-height:1.65;max-width:1150px;}
.section-title {font-size:1.22rem;font-weight:730;margin-top:15px;}
.section-note {color:#9F9B90;font-size:.87rem;margin-bottom:13px;line-height:1.55;}
.kpi {border:1px solid rgba(212,175,55,.24);border-radius:16px;padding:14px 15px;min-height:108px;background:linear-gradient(145deg,#121212,#0D0D0D);}
.kpi-label {color:#9F9B90;font-size:.70rem;letter-spacing:.04em;text-transform:uppercase;font-weight:650;}
.kpi-value {font-size:1.48rem;font-weight:760;margin-top:7px;}
.gold {color:#D4AF37;}
.kpi-foot {color:#9F9B90;font-size:.70rem;margin-top:7px;line-height:1.35;}
.info,.callout {background:#0D0D0D;border:1px solid rgba(212,175,55,.24);border-left:3px solid #D4AF37;border-radius:12px;padding:13px 15px;color:#B9B5A9;font-size:.87rem;margin:8px 0 16px;line-height:1.65;}
.callout {background:linear-gradient(145deg,rgba(212,175,55,.07),rgba(255,255,255,.01));}
[data-testid="stDataFrame"] {border:1px solid rgba(212,175,55,.20);border-radius:14px;overflow:hidden;}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# EXCEL / DATA HELPERS
# ============================================================

def excel_col_to_index(col: str) -> int:
    """Excel column letter -> zero-based index."""
    result = 0
    for ch in col.upper():
        result = result * 26 + (ord(ch) - ord("A") + 1)
    return result - 1


def get_excel_cell(raw_df: pd.DataFrame, ref: str):
    match = re.fullmatch(r"([A-Za-z]+)(\d+)", ref)
    if not match:
        return np.nan
    col, row = match.groups()
    r = int(row) - 1
    c = excel_col_to_index(col)
    if r < 0 or c < 0 or r >= len(raw_df) or c >= raw_df.shape[1]:
        return np.nan
    return raw_df.iat[r, c]


def numeric_series(raw_df: pd.DataFrame, col: str, start_excel_row: int = 3) -> pd.Series:
    c = excel_col_to_index(col)
    return pd.to_numeric(
        raw_df.iloc[start_excel_row - 1 :, c],
        errors="coerce",
    ).reset_index(drop=True)


def text_series(raw_df: pd.DataFrame, col: str, start_excel_row: int = 3) -> pd.Series:
    c = excel_col_to_index(col)
    s = raw_df.iloc[start_excel_row - 1 :, c].reset_index(drop=True)
    return s.fillna("").astype(str).str.strip()


def normalize_market_type(value):
    value = "" if value is None else str(value).strip()
    if not value:
        return "Unknown"

    clean = value.upper().replace("_", "-").strip()

    aliases = {
        "B30": "B30",
        "B30-SELECT": "B30",
        "B30 SELECT": "B30",
        "T30": "T30",
        "T30-EXT": "T30",
        "T30 EXT": "T30",
        "T2": "T2",
        "T6": "T6",
        "EM": "EM",
    }
    return aliases.get(clean, clean)


@st.cache_data(show_spinner=False)
def load_model(file_bytes):
    """
    Read the exact RM Retail Sales columns that feed FINAL.

    Important workbook columns:
      AS = FY26 Equity NS target
      AT = YTD June Equity NS target
      AU = YTD June Equity NS actual
      EE = current achievement basis
      EI/EJ = 5% scenario achievement / scenario amount
      EK/EL = 10% scenario achievement / scenario amount
      EM/EN = 15% scenario achievement / scenario amount
    """

    raw_rm = pd.read_excel(
        BytesIO(file_bytes),
        sheet_name="RM Retail Sales",
        header=None,
        engine="openpyxl",
    )

    raw_final = pd.read_excel(
        BytesIO(file_bytes),
        sheet_name="FINAL",
        header=None,
        engine="openpyxl",
    )

    df = pd.DataFrame(
        {
            "Excel Row": np.arange(3, 3 + max(0, len(raw_rm) - 2)),
            "Emp Code": text_series(raw_rm, "A"),
            "ADID": text_series(raw_rm, "B"),
            "Status": text_series(raw_rm, "C"),
            "Type": text_series(raw_rm, "D"),
            "Employee Name": text_series(raw_rm, "E"),
            "ZONE": text_series(raw_rm, "G"),
            "REGION": text_series(raw_rm, "H"),
            "Raw Market Type": text_series(raw_rm, "J"),
            "FY 26 TGT EQ NS": numeric_series(raw_rm, "AS"),
            "YTD June EQ NS TGT": numeric_series(raw_rm, "AT"),
            "Equity NS Ach YTD June": numeric_series(raw_rm, "AU"),
            "Current Achievement Basis": numeric_series(raw_rm, "EE"),
            "5% Achievement Basis": numeric_series(raw_rm, "EI"),
            "5% Scenario Amount": numeric_series(raw_rm, "EJ"),
            "10% Achievement Basis": numeric_series(raw_rm, "EK"),
            "10% Scenario Amount": numeric_series(raw_rm, "EL"),
            "15% Achievement Basis": numeric_series(raw_rm, "EM"),
            "15% Scenario Amount": numeric_series(raw_rm, "EN"),
        }
    )

    identity = df["Emp Code"].ne("") | df["Employee Name"].ne("")
    df = df.loc[identity].copy().reset_index(drop=True)

    df["Market Type"] = df["Raw Market Type"].apply(normalize_market_type)

    # The workbook contains a small set of rows where EI/EK/EM are deliberately
    # not following the normal +5/+10/+15 & 150% cap rule. Preserve those as
    # locked/manual exceptions when a custom scenario is created.
    def close(a, b):
        return np.isclose(a, b, rtol=0, atol=1e-12, equal_nan=False)

    df["Scenario Locked"] = (
        close(df["5% Achievement Basis"], df["Current Achievement Basis"])
        & close(df["10% Achievement Basis"], df["Current Achievement Basis"])
        & close(df["15% Achievement Basis"], df["Current Achievement Basis"])
    )

    # FINAL!G39 uses SUM(AU:AU). RM Retail Sales!AU1 contains a numeric formula,
    # so the 5/10/15 totals include this small adjustment. We retain it to match
    # the workbook exactly.
    au1_adjustment = pd.to_numeric(
        pd.Series([get_excel_cell(raw_rm, "AU1")]),
        errors="coerce",
    ).iloc[0]
    if pd.isna(au1_adjustment):
        au1_adjustment = 0.0

    benchmark = {
        "Target": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FN16")]), errors="coerce").iloc[0],
        "Current NS": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FO16")]), errors="coerce").iloc[0],
        "5% NS": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FP16")]), errors="coerce").iloc[0],
        "10% NS": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FQ16")]), errors="coerce").iloc[0],
        "15% NS": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FR16")]), errors="coerce").iloc[0],
        "Current PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FO18")]), errors="coerce").iloc[0],
        "5% PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FP18")]), errors="coerce").iloc[0],
        "10% PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FQ18")]), errors="coerce").iloc[0],
        "15% PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FR18")]), errors="coerce").iloc[0],
        "5% Incremental PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FP19")]), errors="coerce").iloc[0],
        "10% Incremental PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FQ19")]), errors="coerce").iloc[0],
        "15% Incremental PBT": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FR19")]), errors="coerce").iloc[0],
        "Kitty %": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FO20")]), errors="coerce").iloc[0],
        "5% Kitty": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FP20")]), errors="coerce").iloc[0],
        "10% Kitty": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FQ20")]), errors="coerce").iloc[0],
        "15% Kitty": pd.to_numeric(pd.Series([get_excel_cell(raw_final, "FR20")]), errors="coerce").iloc[0],
    }

    # Exact FINAL bucketing values FO:FR, rows 8:14.
    benchmark["Bucket Current"] = [get_excel_cell(raw_final, f"FO{r}") for r in range(8, 15)]
    benchmark["Bucket 5%"] = [get_excel_cell(raw_final, f"FP{r}") for r in range(8, 15)]
    benchmark["Bucket 10%"] = [get_excel_cell(raw_final, f"FQ{r}") for r in range(8, 15)]
    benchmark["Bucket 15%"] = [get_excel_cell(raw_final, f"FR{r}") for r in range(8, 15)]

    return df, benchmark, float(au1_adjustment)


# ============================================================
# FORMATTING / UI
# ============================================================

def fmt(value):
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):,.2f}"


def pct(value):
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):,.1f}%"


def revenue(net_sales):
    return net_sales * REVENUE_FACTOR


def section(title, note=""):
    st.html(
        f"""
<div class="section-title">{title}</div>
<div class="section-note">{note}</div>
"""
    )


def kpi(label, value, foot="", accent=False):
    value_class = "kpi-value gold" if accent else "kpi-value"
    st.html(
        f"""
<div class="kpi">
    <div class="kpi-label">{label}</div>
    <div class="{value_class}">{value}</div>
    <div class="kpi-foot">{foot}</div>
</div>
"""
    )


def showdf(dataframe, height=None):
    display = dataframe.copy()
    numeric_columns = display.select_dtypes(include=[np.number]).columns
    display[numeric_columns] = display[numeric_columns].round(2)
    kwargs = {"data": display, "width": "stretch", "hide_index": True}
    if height is not None:
        kwargs["height"] = height
    st.dataframe(**kwargs)


def style(fig, height=400):
    fig.update_layout(
        template=None,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD,
        font=dict(color=TEXT),
        margin=dict(l=28, r=24, t=58, b=48),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=GRID, linecolor=BORDER, tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, linecolor=BORDER, tickfont=dict(color=MUTED))
    return fig


# ============================================================
# EXACT EXCEL SCENARIO ENGINE
# ============================================================

def build_exact_scenario(base_df, uplift_pct, au1_adjustment):
    """
    Replicate the RM Retail Sales + FINAL logic.

    Current:
      achievement basis = EE
      projected final NS = AU / 3 * 12 = AU * 4

    5/10/15:
      use the workbook's stored EI/EJ, EK/EL, EM/EN values.
      projected final NS per RM = AU + 3 * Scenario Amount.
      The first workbook row receives AU1 adjustment so aggregate matches
      FINAL!FP16/FQ16/FR16 exactly (because FINAL!G39 sums AU:AU).

    Custom:
      unlocked rows: IF(EE > 150%, 150%, EE + uplift)
      locked rows: preserve EE
      amount = achievement basis * AS
      projected final NS = AU + 3 * amount
    """

    df = base_df.copy()
    u = float(uplift_pct)

    if abs(u) < 1e-12:
        df["Achievement Basis"] = df["Current Achievement Basis"]
        df["Scenario Amount"] = df["Equity NS Ach YTD June"]
        df["Projected Final NS"] = df["Equity NS Ach YTD June"] * 4.0
        df["Scenario"] = "Current Run Rate"

    elif abs(u - 5.0) < 1e-12:
        df["Achievement Basis"] = df["5% Achievement Basis"]
        df["Scenario Amount"] = df["5% Scenario Amount"]
        df["Projected Final NS"] = (
            df["Equity NS Ach YTD June"] + 3.0 * df["Scenario Amount"]
        )
        df.loc[df["Excel Row"].eq(3), "Projected Final NS"] += au1_adjustment
        df["Scenario"] = "+5%"

    elif abs(u - 10.0) < 1e-12:
        df["Achievement Basis"] = df["10% Achievement Basis"]
        df["Scenario Amount"] = df["10% Scenario Amount"]
        df["Projected Final NS"] = (
            df["Equity NS Ach YTD June"] + 3.0 * df["Scenario Amount"]
        )
        df.loc[df["Excel Row"].eq(3), "Projected Final NS"] += au1_adjustment
        df["Scenario"] = "+10%"

    elif abs(u - 15.0) < 1e-12:
        df["Achievement Basis"] = df["15% Achievement Basis"]
        df["Scenario Amount"] = df["15% Scenario Amount"]
        df["Projected Final NS"] = (
            df["Equity NS Ach YTD June"] + 3.0 * df["Scenario Amount"]
        )
        df.loc[df["Excel Row"].eq(3), "Projected Final NS"] += au1_adjustment
        df["Scenario"] = "+15%"

    else:
        current = df["Current Achievement Basis"]
        generic = np.where(
            current > 1.50,
            1.50,
            current + u / 100.0,
        )
        generic = pd.Series(generic, index=df.index, dtype="float64")
        generic = generic.where(current.notna(), np.nan)
        custom_ach = generic.where(~df["Scenario Locked"], current)

        df["Achievement Basis"] = custom_ach
        df["Scenario Amount"] = custom_ach * df["FY 26 TGT EQ NS"]
        df["Projected Final NS"] = (
            df["Equity NS Ach YTD June"] + 3.0 * df["Scenario Amount"]
        )
        df.loc[df["Excel Row"].eq(3), "Projected Final NS"] += au1_adjustment
        df["Scenario"] = f"Custom +{u:.1f}%"

    df["Revenue"] = revenue(df["Projected Final NS"])

    # FINAL uses >100%, not >=100%.
    df["Qualified"] = df["Achievement Basis"] > 1.0

    return df


def scenario_summary(df, label, uplift, baseline_df):
    total_target = df["FY 26 TGT EQ NS"].sum(skipna=True)
    total_ns = df["Projected Final NS"].sum(skipna=True)
    total_ytd = df["Equity NS Ach YTD June"].sum(skipna=True)
    eligible = df["Achievement Basis"].notna()
    q = df["Qualified"] & eligible
    q_count = int(q.sum())
    q_ns = df.loc[q, "Projected Final NS"].sum(skipna=True)
    q_revenue = revenue(q_ns)

    base_q = baseline_df["Qualified"] & baseline_df["Achievement Basis"].notna()
    # Align by Excel row so filtering/reindexing cannot break the comparison.
    current_qual_rows = set(baseline_df.loc[base_q, "Excel Row"].tolist())
    new_qual_rows = set(df.loc[q, "Excel Row"].tolist())
    newly = len(new_qual_rows - current_qual_rows)

    baseline_total_ns = baseline_df["Projected Final NS"].sum(skipna=True)
    incremental_ns = total_ns - baseline_total_ns

    return {
        "Scenario": label,
        "Run Rate / Achievement Uplift %": uplift,
        "Achievement-Eligible RMs": int(eligible.sum()),
        "Total Target": total_target,
        "YTD Achieved NS": total_ytd,
        "Total Projected NS": total_ns,
        "Revenue / PBT": revenue(total_ns),
        "Portfolio Achievement %": (total_ns / total_target * 100) if total_target else 0,
        "RMs >100%": q_count,
        "Qualification Rate %": (q_count / int(eligible.sum()) * 100) if eligible.sum() else 0,
        "Qualifying RM NS": q_ns,
        "Qualifying Revenue": q_revenue,
        "Qualifying NS Contribution %": (q_ns / total_ns * 100) if total_ns else 0,
        "Newly >100% vs Current": newly,
        "Incremental NS vs Current": incremental_ns,
        "Incremental Revenue vs Current": revenue(incremental_ns),
    }


# ============================================================
# EXACT FINAL ACHIEVEMENT BUCKETS
# ============================================================

def final_bucket_counts(df, is_current=False):
    a = df["Achievement Basis"]
    valid = a.notna()

    if is_current:
        conditions = [
            a < 0,
            (a >= 0) & (a <= 0.30),
            (a > 0.30) & (a <= 0.50),
            (a > 0.50) & (a <= 0.80),
            (a > 0.80) & (a <= 1.00),
            a > 1.00,
        ]
    else:
        # FINAL FP:FQ:FR uses >0 for the 0-30 scenario bands.
        conditions = [
            a < 0,
            (a > 0) & (a <= 0.30),
            (a > 0.30) & (a <= 0.50),
            (a > 0.50) & (a <= 0.80),
            (a > 0.80) & (a <= 1.00),
            a > 1.00,
        ]

    counts = [int((cond & valid).sum()) for cond in conditions]
    return counts + [sum(counts)]


def broad_bucket_comparison(scenario_map):
    labels = ["< 0%", "0 - 30%", "30 - 50%", "50 - 80%", "80 - 100%", "> 100%", "Total"]
    out = pd.DataFrame({"Achievement Bucketing": labels})
    for name, (df, uplift) in scenario_map.items():
        out[name] = final_bucket_counts(df, is_current=abs(uplift) < 1e-12)
    return out


# ============================================================
# MARKET TYPE SUMMARY
# ============================================================

def market_summary(df):
    total_projected = df["Projected Final NS"].sum(skipna=True)
    total_ytd = df["Equity NS Ach YTD June"].sum(skipna=True)

    grouped = (
        df.groupby("Market Type", dropna=False)
        .agg(
            RMs=("Employee Name", "size"),
            Achievement_Eligible_RMs=("Achievement Basis", "count"),
            Target=("FY 26 TGT EQ NS", "sum"),
            YTD_Achieved_NS=("Equity NS Ach YTD June", "sum"),
            Projected_NS=("Projected Final NS", "sum"),
            Revenue=("Revenue", "sum"),
            RMs_Above_100=("Qualified", "sum"),
        )
        .reset_index()
    )

    q = (
        df.loc[df["Qualified"]]
        .groupby("Market Type", dropna=False)
        .agg(Qualifying_NS=("Projected Final NS", "sum"))
        .reset_index()
    )

    grouped = grouped.merge(q, on="Market Type", how="left")
    grouped["Qualifying_NS"] = grouped["Qualifying_NS"].fillna(0)
    grouped["Qualifying Revenue"] = revenue(grouped["Qualifying_NS"])
    grouped["Qualification Rate %"] = np.where(
        grouped["Achievement_Eligible_RMs"] > 0,
        grouped["RMs_Above_100"] / grouped["Achievement_Eligible_RMs"] * 100,
        0,
    )
    grouped["Projected NS Contribution %"] = np.where(
        total_projected != 0,
        grouped["Projected_NS"] / total_projected * 100,
        0,
    )
    grouped["YTD Achieved NS Contribution %"] = np.where(
        total_ytd != 0,
        grouped["YTD_Achieved_NS"] / total_ytd * 100,
        0,
    )
    grouped["Qualifying NS Contribution to Total %"] = np.where(
        total_projected != 0,
        grouped["Qualifying_NS"] / total_projected * 100,
        0,
    )

    return grouped.sort_values("Projected NS Contribution %", ascending=False)


# ============================================================
# 5% DETAILED BUCKETS
# ============================================================

def achievement_bucket_5pct(value):
    if pd.isna(value):
        return "Unknown"
    if value > 1.0:
        return "> 100%"
    if value < 0:
        return "< 0%"

    p = value * 100.0
    # Intervals use (lower, upper], so 100 belongs to 95-100.
    if p <= 0:
        return "0 - 5%"
    upper = int(np.ceil(p / 5.0) * 5)
    upper = max(5, min(100, upper))
    lower = upper - 5
    return f"{lower} - {upper}%"


def detailed_bucket_table(df, trip_cost_lakh):
    work = df.copy()
    work["Achievement Bucket"] = work["Achievement Basis"].apply(achievement_bucket_5pct)

    total_projected = work["Projected Final NS"].sum(skipna=True)
    total_ytd = work["Equity NS Ach YTD June"].sum(skipna=True)

    market_totals = (
        work.groupby("Market Type", dropna=False)
        .agg(
            Market_Projected_NS=("Projected Final NS", "sum"),
            Market_YTD_NS=("Equity NS Ach YTD June", "sum"),
        )
        .reset_index()
    )

    # Extension of the workbook scenario logic:
    # a move from achievement basis x to 100% changes each of the 3 future
    # periods by (1-x)*Target.
    work["Additional NS to 100%"] = np.where(
        work["Achievement Basis"].notna() & (work["Achievement Basis"] <= 1.0),
        np.maximum(0, 1.0 - work["Achievement Basis"]) * work["FY 26 TGT EQ NS"] * 3.0,
        0.0,
    )

    grouped = (
        work.groupby(["Market Type", "Achievement Bucket"], dropna=False)
        .agg(
            RMs=("Employee Name", "size"),
            Target=("FY 26 TGT EQ NS", "sum"),
            YTD_Achieved_NS=("Equity NS Ach YTD June", "sum"),
            Projected_NS=("Projected Final NS", "sum"),
            Revenue=("Revenue", "sum"),
            Avg_Achievement=("Achievement Basis", "mean"),
            Additional_NS_to_100=("Additional NS to 100%", "sum"),
        )
        .reset_index()
        .merge(market_totals, on="Market Type", how="left")
    )

    grouped["Projected NS Contribution to Total %"] = np.where(
        total_projected != 0,
        grouped["Projected_NS"] / total_projected * 100,
        0,
    )
    grouped["Projected NS Contribution within Market %"] = np.where(
        grouped["Market_Projected_NS"] != 0,
        grouped["Projected_NS"] / grouped["Market_Projected_NS"] * 100,
        0,
    )
    grouped["YTD NS Contribution to Total %"] = np.where(
        total_ytd != 0,
        grouped["YTD_Achieved_NS"] / total_ytd * 100,
        0,
    )
    grouped["YTD NS Contribution within Market %"] = np.where(
        grouped["Market_YTD_NS"] != 0,
        grouped["YTD_Achieved_NS"] / grouped["Market_YTD_NS"] * 100,
        0,
    )

    grouped["Additional Revenue to 100%"] = revenue(grouped["Additional_NS_to_100"])

    # Only sub-100 buckets incur new trip cost if converted.
    grouped["Additional Trip Cost if Converted (₹ Cr)"] = np.where(
        grouped["Achievement Bucket"].eq("> 100%") | grouped["Achievement Bucket"].eq("Unknown"),
        0.0,
        grouped["RMs"] * trip_cost_lakh / 100.0,
    )
    grouped["Net Additional Revenue After Trip"] = (
        grouped["Additional Revenue to 100%"]
        - grouped["Additional Trip Cost if Converted (₹ Cr)"]
    )
    grouped["Break-even Trip Cost / RM (₹ lakh)"] = np.where(
        grouped["RMs"] > 0,
        grouped["Additional Revenue to 100%"] * 100.0 / grouped["RMs"],
        np.nan,
    )
    grouped["NS After Conversion"] = grouped["Projected_NS"] + grouped["Additional_NS_to_100"]
    grouped["Contribution % After Conversion"] = np.where(
        total_projected + grouped["Additional_NS_to_100"] != 0,
        grouped["NS After Conversion"]
        / (total_projected + grouped["Additional_NS_to_100"])
        * 100,
        0,
    )

    def bucket_sort(label):
        if label == "> 100%":
            return 10000
        if label == "Unknown":
            return -1000
        if label == "< 0%":
            return -1
        try:
            return int(str(label).split(" - ")[0])
        except Exception:
            return -999

    grouped["_sort"] = grouped["Achievement Bucket"].map(bucket_sort)
    grouped = grouped.sort_values(
        ["Market Type", "_sort"],
        ascending=[True, False],
    ).drop(columns=["_sort", "Market_Projected_NS", "Market_YTD_NS"])

    grouped["Avg Achievement %"] = grouped.pop("Avg_Achievement") * 100.0
    return grouped


# ============================================================
# 90-100% CONVERSION OPPORTUNITY
# ============================================================

def near_miss_table(df, trip_cost_lakh):
    total_projected = df["Projected Final NS"].sum(skipna=True)
    total_ytd = df["Equity NS Ach YTD June"].sum(skipna=True)

    qualified = df["Achievement Basis"] > 1.0
    near_mask = df["Achievement Basis"].between(0.90, 1.00, inclusive="both")

    base = (
        df.groupby("Market Type", dropna=False)
        .agg(
            Total_RMs=("Employee Name", "size"),
            Achievement_Eligible_RMs=("Achievement Basis", "count"),
            Market_Target=("FY 26 TGT EQ NS", "sum"),
            Market_Projected_NS=("Projected Final NS", "sum"),
            Market_YTD_NS=("Equity NS Ach YTD June", "sum"),
        )
    )

    current_q = (
        df.loc[qualified]
        .groupby("Market Type", dropna=False)
        .agg(
            Current_RMs_Above_100=("Employee Name", "size"),
            Current_Qualified_NS=("Projected Final NS", "sum"),
        )
    )

    near = df.loc[near_mask].copy()
    near["Additional NS to 100%"] = (
        np.maximum(0, 1.0 - near["Achievement Basis"])
        * near["FY 26 TGT EQ NS"]
        * 3.0
    )

    near_group = (
        near.groupby("Market Type", dropna=False)
        .agg(
            RMs_90_100=("Employee Name", "size"),
            NS_90_100=("Projected Final NS", "sum"),
            YTD_NS_90_100=("Equity NS Ach YTD June", "sum"),
            Additional_NS_to_100=("Additional NS to 100%", "sum"),
        )
    )

    result = (
        base.join(current_q, how="left")
        .join(near_group, how="left")
        .fillna(0)
        .reset_index()
    )

    result["Current 100%+ NS Contribution %"] = np.where(
        total_projected != 0,
        result["Current_Qualified_NS"] / total_projected * 100,
        0,
    )
    result["90-100% NS Contribution %"] = np.where(
        total_projected != 0,
        result["NS_90_100"] / total_projected * 100,
        0,
    )
    result["90-100% YTD Contribution %"] = np.where(
        total_ytd != 0,
        result["YTD_NS_90_100"] / total_ytd * 100,
        0,
    )

    result["Additional Revenue"] = revenue(result["Additional_NS_to_100"])
    result["Additional Trip Cost (₹ Cr)"] = result["RMs_90_100"] * trip_cost_lakh / 100.0
    result["Net Additional Revenue After Trip"] = (
        result["Additional Revenue"] - result["Additional Trip Cost (₹ Cr)"]
    )
    result["Revenue / Trip Cost (x)"] = np.where(
        result["Additional Trip Cost (₹ Cr)"] > 0,
        result["Additional Revenue"] / result["Additional Trip Cost (₹ Cr)"],
        np.nan,
    )
    result["Additional NS / Near-Miss RM"] = np.where(
        result["RMs_90_100"] > 0,
        result["Additional_NS_to_100"] / result["RMs_90_100"],
        np.nan,
    )
    result["Break-even Trip Cost / RM (₹ lakh)"] = np.where(
        result["RMs_90_100"] > 0,
        result["Additional Revenue"] * 100.0 / result["RMs_90_100"],
        np.nan,
    )
    result["Qualified RMs After Conversion"] = (
        result["Current_RMs_Above_100"] + result["RMs_90_100"]
    )
    result["Qualified NS After Conversion"] = (
        result["Current_Qualified_NS"]
        + result["NS_90_100"]
        + result["Additional_NS_to_100"]
    )
    result["Total NS After Conversion"] = total_projected + result["Additional_NS_to_100"]
    result["Qualified NS Contribution % After Conversion"] = np.where(
        result["Total NS After Conversion"] != 0,
        result["Qualified NS After Conversion"] / result["Total NS After Conversion"] * 100,
        0,
    )
    result["Economically Positive After Trip?"] = result["Net Additional Revenue After Trip"] >= 0

    return result.sort_values(
        ["RMs_90_100", "Additional_NS_to_100"],
        ascending=[False, False],
    )


# ============================================================
# VALIDATION AGAINST FINAL
# ============================================================

def render_workbook_validation(full_df, benchmark, au1_adjustment):
    current = build_exact_scenario(full_df, 0, au1_adjustment)
    s5 = build_exact_scenario(full_df, 5, au1_adjustment)
    s10 = build_exact_scenario(full_df, 10, au1_adjustment)
    s15 = build_exact_scenario(full_df, 15, au1_adjustment)

    computed_ns = {
        "Current": current["Projected Final NS"].sum(skipna=True),
        "5%": s5["Projected Final NS"].sum(skipna=True),
        "10%": s10["Projected Final NS"].sum(skipna=True),
        "15%": s15["Projected Final NS"].sum(skipna=True),
    }
    final_ns = {
        "Current": benchmark["Current NS"],
        "5%": benchmark["5% NS"],
        "10%": benchmark["10% NS"],
        "15%": benchmark["15% NS"],
    }

    validation = pd.DataFrame(
        {
            "Scenario": ["Current", "5%", "10%", "15%"],
            "Calculated from RM Retail Sales": [computed_ns[x] for x in ["Current", "5%", "10%", "15%"]],
            "FINAL Sheet": [final_ns[x] for x in ["Current", "5%", "10%", "15%"]],
        }
    )
    validation["Difference"] = (
        validation["Calculated from RM Retail Sales"] - validation["FINAL Sheet"]
    )

    target_calc = full_df["FY 26 TGT EQ NS"].sum(skipna=True)

    section(
        "Workbook Formula Validation",
        "This checks the app engine directly against the uploaded FINAL sheet before any dashboard filters are applied.",
    )

    cols = st.columns(4)
    with cols[0]:
        kpi("FINAL Target", fmt(benchmark["Target"]), f"RM calc {fmt(target_calc)}", True)
    with cols[1]:
        kpi("Locked / Manual Rows", int(full_df["Scenario Locked"].sum()), "Preserved exactly for 5/10/15", False)
    with cols[2]:
        kpi("FINAL AU1 Adjustment", fmt(au1_adjustment), "Included in scenario totals because FINAL!G39 uses AU:AU", False)
    with cols[3]:
        max_diff = validation["Difference"].abs().max()
        kpi("Max NS Difference", f"{max_diff:.10f}", "Should be ~0", True)

    showdf(validation)

    pbt_validation = pd.DataFrame(
        {
            "Metric": ["Projected PBT / Revenue", "Incremental PBT vs Current", "Kitty @ 15%"],
            "Current": [revenue(computed_ns["Current"]), np.nan, 0.15],
            "5%": [revenue(computed_ns["5%"]), revenue(computed_ns["5%"] - computed_ns["Current"]), revenue(computed_ns["5%"] - computed_ns["Current"]) * 0.15],
            "10%": [revenue(computed_ns["10%"]), revenue(computed_ns["10%"] - computed_ns["Current"]), revenue(computed_ns["10%"] - computed_ns["Current"]) * 0.15],
            "15%": [revenue(computed_ns["15%"]), revenue(computed_ns["15%"] - computed_ns["Current"]), revenue(computed_ns["15%"] - computed_ns["Current"]) * 0.15],
        }
    )
    final_pbt_validation = pd.DataFrame(
        {
            "Metric": ["Projected PBT / Revenue", "Incremental PBT vs Current", "Kitty @ 15%"],
            "FINAL Current": [benchmark["Current PBT"], np.nan, benchmark["Kitty %"]],
            "FINAL 5%": [benchmark["5% PBT"], benchmark["5% Incremental PBT"], benchmark["5% Kitty"]],
            "FINAL 10%": [benchmark["10% PBT"], benchmark["10% Incremental PBT"], benchmark["10% Kitty"]],
            "FINAL 15%": [benchmark["15% PBT"], benchmark["15% Incremental PBT"], benchmark["15% Kitty"]],
        }
    )
    showdf(pbt_validation.merge(final_pbt_validation, on="Metric", how="left"))

    count_calc = broad_bucket_comparison(
        {
            "Current": (current, 0),
            "5%": (s5, 5),
            "10%": (s10, 10),
            "15%": (s15, 15),
        }
    )

    final_counts = pd.DataFrame(
        {
            "Achievement Bucketing": ["< 0%", "0 - 30%", "30 - 50%", "50 - 80%", "80 - 100%", "> 100%", "Total"],
            "FINAL Current": benchmark["Bucket Current"],
            "FINAL 5%": benchmark["Bucket 5%"],
            "FINAL 10%": benchmark["Bucket 10%"],
            "FINAL 15%": benchmark["Bucket 15%"],
        }
    )

    count_validation = count_calc.merge(final_counts, on="Achievement Bucketing", how="left")
    showdf(count_validation)

    st.html(
        f"""
<div class="callout">
<b style="color:#D4AF37">Verified workbook logic</b><br><br>
Current projected NS = SUM(AU3:AU529) / 3 × 12.<br>
Current achievement buckets use EE = AU / AT.<br>
5% buckets use EI, 10% use EK and 15% use EM.<br>
Scenario amounts are EJ / EL / EN and FINAL calculates scenario NS as 3 × SUM(scenario amount) + G39.<br>
PBT / Revenue = Net Sales × 0.6%. Incremental PBT = scenario PBT − current PBT. Kitty = 15% × incremental PBT.<br><br>
The uploaded workbook has <b>{int(full_df['Scenario Locked'].sum())}</b> rows where the saved 5/10/15 scenario values are manual/locked exceptions to the generic uplift rule; the app preserves them.
</div>
"""
    )


# ============================================================
# MANAGEMENT SUMMARY
# ============================================================

def render_management_summary(comparison_df, current_df, trip_cost_lakh):
    section(
        "Management Summary",
        "Key commercial implications from qualification count, contribution, near-miss conversion and foreign-trip economics.",
    )

    current = comparison_df.iloc[0]
    highest = comparison_df.sort_values("Run Rate / Achievement Uplift %", ascending=False).iloc[0]
    near = near_miss_table(current_df, trip_cost_lakh)

    near_count = int(near["RMs_90_100"].sum())
    near_ns = near["NS_90_100"].sum()
    extra_ns = near["Additional_NS_to_100"].sum()
    extra_rev = revenue(extra_ns)
    trip_cost = near_count * trip_cost_lakh / 100.0
    net_rev = extra_rev - trip_cost

    cols = st.columns(5)
    items = [
        ("Current RMs >100%", int(current["RMs >100%"]), pct(current["Qualification Rate %"]), True),
        ("Qualified RM NS", fmt(current["Qualifying RM NS"]), pct(current["Qualifying NS Contribution %"]) + " of projected NS", True),
        ("Qualified Revenue", fmt(current["Qualifying Revenue"]), "NS × 0.6%", False),
        ("RMs 90%-100%", near_count, "Immediate near-miss pool", True),
        ("NS Needed to Reach 100%", fmt(extra_ns), "Using the workbook's 3 future-period logic", False),
    ]
    for i, item in enumerate(items):
        with cols[i]:
            kpi(*item)

    cols = st.columns(5)
    items = [
        ("Highest Scenario RMs >100%", int(highest["RMs >100%"]), f"+{int(highest['Newly >100% vs Current'])} vs current", True),
        ("Highest Scenario Incremental NS", fmt(highest["Incremental NS vs Current"]), f"{highest['Run Rate / Achievement Uplift %']:.1f}% uplift", True),
        ("Incremental Revenue", fmt(highest["Incremental Revenue vs Current"]), "Incremental NS × 0.6%", False),
        ("90%-100% Extra Revenue", fmt(extra_rev), "If entire near-miss pool reaches 100%", True),
        ("New Trip Cost", f"₹{trip_cost:,.2f} Cr", f"{near_count} people × ₹{trip_cost_lakh:.2f} lakh", False),
    ]
    for i, item in enumerate(items):
        with cols[i]:
            kpi(*item)

    market = market_summary(current_df)
    qualified_markets = market.loc[market["RMs_Above_100"] > 0].copy()
    if not qualified_markets.empty:
        low_value = qualified_markets.sort_values("Qualifying NS Contribution to Total %").iloc[0]
        st.html(
            f"""
<div class="callout">
<b style="color:#D4AF37">Qualification count vs commercial value</b><br><br>
<b style="color:#F3F0E7">{low_value['Market Type']}</b> has
<b style="color:#F3F0E7">{int(low_value['RMs_Above_100'])}</b> RMs above 100%, but those RMs contribute only
<b style="color:#F3F0E7">{low_value['Qualifying NS Contribution to Total %']:.1f}%</b> of total projected NS.
This is a case where qualifier count alone can overstate business value.
</div>
"""
        )

    opportunity = near.loc[near["RMs_90_100"] > 0].copy()
    if not opportunity.empty:
        biggest_pool = opportunity.sort_values("RMs_90_100", ascending=False).iloc[0]
        cheapest = opportunity.sort_values("Additional NS / Near-Miss RM", ascending=True).iloc[0]
        biggest_ns = opportunity.sort_values("Additional_NS_to_100", ascending=False).iloc[0]

        st.html(
            f"""
<div class="callout">
<b style="color:#D4AF37">Largest near-target pool</b><br><br>
<b style="color:#F3F0E7">{biggest_pool['Market Type']}</b> has
<b style="color:#F3F0E7">{int(biggest_pool['RMs_90_100'])}</b> RMs between 90% and 100%.
They already contribute <b>{biggest_pool['90-100% NS Contribution %']:.1f}%</b> of projected NS and need
<b>{fmt(biggest_pool['Additional_NS_to_100'])}</b> additional NS to reach the 100% threshold under the workbook projection method.
</div>
"""
        )

        st.html(
            f"""
<div class="callout">
<b style="color:#D4AF37">Most efficient conversion pool</b><br><br>
<b style="color:#F3F0E7">{cheapest['Market Type']}</b> has the lowest additional NS requirement per near-miss RM:
<b>{fmt(cheapest['Additional NS / Near-Miss RM'])}</b> NS per RM.
Its break-even foreign-trip cost is approximately
<b>₹{cheapest['Break-even Trip Cost / RM (₹ lakh)']:.2f} lakh per converted RM</b> based only on the 0.6% PBT / Revenue assumption.
</div>
"""
        )

        st.html(
            f"""
<div class="callout">
<b style="color:#D4AF37">Largest incremental NS opportunity</b><br><br>
<b style="color:#F3F0E7">{biggest_ns['Market Type']}</b> has the largest total conversion ask:
<b>{fmt(biggest_ns['Additional_NS_to_100'])}</b> additional NS, generating
<b>{fmt(biggest_ns['Additional Revenue'])}</b> additional Revenue / PBT.
Trip cost for all of these near-miss RMs is <b>₹{biggest_ns['Additional Trip Cost (₹ Cr)']:.2f} Cr</b>.
</div>
"""
        )

    st.html(
        f"""
<div class="callout">
<b style="color:#D4AF37">Overall 90%-100% conversion economics</b><br><br>
Near-miss RMs: <b>{near_count}</b><br>
Current projected NS from the pool: <b>{fmt(near_ns)}</b><br>
Additional NS needed: <b>{fmt(extra_ns)}</b><br>
Additional Revenue / PBT: <b>{fmt(extra_rev)}</b><br>
Additional trip cost: <b>₹{trip_cost:,.2f} Cr</b><br>
Additional Revenue less trip cost: <b>{fmt(net_rev)}</b>
</div>
"""
    )


# ============================================================
# BELL CURVE VISUAL
# ============================================================

def bell_fig(before_df, after_df):
    before = before_df["Achievement Basis"].replace([np.inf, -np.inf], np.nan).dropna()
    after = after_df["Achievement Basis"].replace([np.inf, -np.inf], np.nan).dropna()
    fig = go.Figure()

    if before.empty or after.empty:
        return style(fig)

    minimum = min(before.min(), after.min())
    maximum = max(before.max(), after.max())

    for values, name, color in [
        (before, "Current", "#888888"),
        (after, "Selected Scenario", GOLD),
    ]:
        mean = values.mean()
        std = values.std()
        if pd.isna(std) or std == 0:
            std = 0.000001
        x = np.linspace(minimum, maximum, 400)
        y = np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=name,
                line=dict(color=color, width=3),
                fill="tozeroy",
            )
        )

    fig.add_vline(x=1.0, line_dash="dot", line_color=TEXT, annotation_text="100%")
    fig.update_layout(
        title="Achievement Distribution · Current vs Selected Scenario",
        xaxis_title="Excel Achievement Basis",
        yaxis_title="Density",
    )
    fig.update_xaxes(tickformat=".0%")
    return style(fig, 440)


# ============================================================
# FILTER HELPERS
# ============================================================

def filter_data(df, market_type, statuses, types, zones, regions):
    out = df.copy()
    if market_type != "All Market Types":
        out = out.loc[out["Market Type"].eq(market_type)]
    if statuses:
        out = out.loc[out["Status"].isin(statuses)]
    if types:
        out = out.loc[out["Type"].isin(types)]
    if zones:
        out = out.loc[out["ZONE"].isin(zones)]
    if regions:
        out = out.loc[out["REGION"].isin(regions)]
    return out.copy()


# ============================================================
# PAGE 1
# ============================================================

def page1(data, au1_adjustment, uplift):
    current = build_exact_scenario(data, 0, au1_adjustment)
    selected = build_exact_scenario(data, uplift, au1_adjustment)

    st.html(
        f"""
<div class="hero">
    <div class="eyebrow">Page 1 · Scenario Lab</div>
    <div class="hero-title">Excel-Consistent Scenario Projection</div>
    <div class="hero-sub">
        Current vs +{uplift:.1f}% using the exact achievement-basis logic from RM Retail Sales.
        Standard 5/10/15 scenarios use the workbook's saved EI/EJ, EK/EL and EM/EN values.
    </div>
</div>
"""
    )

    tabs = st.tabs(["Current", f"+{uplift:.1f}%", "Comparison"])

    for tab, name, df in [(tabs[0], "Current", current), (tabs[1], f"+{uplift:.1f}%", selected)]:
        with tab:
            total_target = df["FY 26 TGT EQ NS"].sum(skipna=True)
            total_ns = df["Projected Final NS"].sum(skipna=True)
            q = df["Qualified"]
            q_ns = df.loc[q, "Projected Final NS"].sum(skipna=True)
            cols = st.columns(5)
            cards = [
                ("Total Target", fmt(total_target), "Excel AS target", False),
                ("Projected NS", fmt(total_ns), "Exact scenario engine", True),
                ("RMs >100%", int(q.sum()), pct(q.sum() / df["Achievement Basis"].notna().sum() * 100) if df["Achievement Basis"].notna().sum() else "—", True),
                ("Qualified NS", fmt(q_ns), pct(q_ns / total_ns * 100) if total_ns else "—", True),
                ("Revenue / PBT", fmt(revenue(total_ns)), "Projected NS × 0.6%", False),
            ]
            for i, card in enumerate(cards):
                with cols[i]:
                    kpi(*card)

            section("Market Type Contribution")
            showdf(market_summary(df))

    with tabs[2]:
        comparison = pd.DataFrame(
            [
                scenario_summary(current, "Current", 0, current),
                scenario_summary(selected, f"+{uplift:.1f}%", uplift, current),
            ]
        )
        showdf(comparison)

    section("Achievement Bucketing")
    showdf(
        broad_bucket_comparison(
            {
                "Current": (current, 0),
                f"+{uplift:.1f}%": (selected, uplift),
            }
        )
    )

    st.plotly_chart(bell_fig(current, selected), config={"displayModeBar": False})


# ============================================================
# PAGE 2
# ============================================================

def page2(data, au1_adjustment):
    current = build_exact_scenario(data, 0, au1_adjustment)

    st.html(
        """
<div class="hero">
    <div class="eyebrow">Page 2 · New Insights</div>
    <div class="hero-title">Current Run-Rate Opportunity</div>
    <div class="hero-sub">Cuts by Market Type, Zone and Region using the same current projection as the FINAL workbook.</div>
</div>
"""
    )

    total_target = current["FY 26 TGT EQ NS"].sum(skipna=True)
    total_ns = current["Projected Final NS"].sum(skipna=True)
    q = current["Qualified"]
    cols = st.columns(4)
    cards = [
        ("Total Target", fmt(total_target), "", False),
        ("Projected NS", fmt(total_ns), pct(total_ns / total_target * 100) if total_target else "", True),
        ("RMs >100%", int(q.sum()), "Excel uses strict >100%", True),
        ("Revenue / PBT", fmt(revenue(total_ns)), "NS × 0.6%", False),
    ]
    for i, card in enumerate(cards):
        with cols[i]:
            kpi(*card)

    for dim in ["Market Type", "ZONE", "REGION"]:
        section(f"{dim} Cut")
        g = (
            current.groupby(dim, dropna=False)
            .agg(
                RMs=("Employee Name", "size"),
                Eligible_RMs=("Achievement Basis", "count"),
                Target=("FY 26 TGT EQ NS", "sum"),
                YTD_NS=("Equity NS Ach YTD June", "sum"),
                Projected_NS=("Projected Final NS", "sum"),
                RMs_Above_100=("Qualified", "sum"),
            )
            .reset_index()
        )
        g["Revenue"] = revenue(g["Projected_NS"])
        g["Achievement %"] = np.where(g["Target"] != 0, g["Projected_NS"] / g["Target"] * 100, 0)
        showdf(g.sort_values("Projected_NS", ascending=False))


# ============================================================
# PAGE 3
# ============================================================

def page3(data, au1_adjustment):
    current = build_exact_scenario(data, 0, au1_adjustment)
    df = current.copy()

    df["No-Incentive Expected NS"] = np.maximum(
        df["FY 26 TGT EQ NS"],
        df["Projected Final NS"],
    )
    df["Stretch Target"] = df["No-Incentive Expected NS"] * 1.15
    df["Incremental NS"] = (df["Stretch Target"] - df["No-Incentive Expected NS"]).clip(lower=0)
    df["Incremental Revenue"] = revenue(df["Incremental NS"])

    st.html(
        """
<div class="hero">
    <div class="eyebrow">Page 3 · BonVoyage</div>
    <div class="hero-title">Incentive Stretch View</div>
    <div class="hero-sub">Uses the corrected current projection from RM Retail Sales as the no-incentive baseline.</div>
</div>
"""
    )

    cols = st.columns(4)
    metrics = [
        ("Official Target", df["FY 26 TGT EQ NS"].sum()),
        ("No-Incentive Expected", df["No-Incentive Expected NS"].sum()),
        ("15% Stretch Target", df["Stretch Target"].sum()),
        ("Incremental NS", df["Incremental NS"].sum()),
    ]
    for i, (label, value) in enumerate(metrics):
        with cols[i]:
            kpi(label, fmt(value), "", i >= 2)

    display_cols = [
        "Emp Code",
        "Employee Name",
        "Market Type",
        "ZONE",
        "REGION",
        "FY 26 TGT EQ NS",
        "Projected Final NS",
        "No-Incentive Expected NS",
        "Stretch Target",
        "Incremental NS",
        "Incremental Revenue",
    ]
    showdf(df[display_cols].sort_values("Incremental NS", ascending=False), 600)


# ============================================================
# PAGE 4
# ============================================================

def page4(filtered_base, full_base, benchmark, au1_adjustment, custom_uplift, market_label):
    st.html(
        f"""
<div class="hero">
    <div class="eyebrow">Page 4 · Run Rate Analysis</div>
    <div class="hero-title">Qualification & Revenue Opportunity</div>
    <div class="hero-sub">
        Exact RM Retail Sales / FINAL scenario logic.<br>
        Selected Market Type: <b style="color:#F3F0E7">{market_label}</b>.<br>
        B30 includes B30-Select. T30 includes T30-Ext.
    </div>
</div>
"""
    )

    st.html(
        """
<div class="callout">
<b style="color:#D4AF37">Important</b><br><br>
The Excel workbook is <b>not</b> doing a simple monthly run-rate × 1.05 / 1.10 / 1.15 calculation.<br>
Its 5/10/15 columns are achievement-basis scenarios stored in EI/EK/EM, with scenario amounts in EJ/EL/EN.
The dashboard below follows those exact columns.
<br><br>
Revenue / PBT = Net Sales × 0.6 / 100 = Net Sales × 0.006.
</div>
"""
    )

    with st.expander("Verified Excel calculation chain", expanded=False):
        st.markdown(
            """
**RM Retail Sales**
- `AS` = FY 26 TGT EQ NS
- `AT` = YTD June EQ NS TGT. In the workbook `AT = AS / 3`.
- `AU` = Equity NS Ach YTD June
- `EE = AU / AT` = current achievement basis used by the FINAL bucketing table
- `EI/EJ` = 5% scenario achievement basis / scenario amount
- `EK/EL` = 10% scenario achievement basis / scenario amount
- `EM/EN` = 15% scenario achievement basis / scenario amount
- Normal rows follow `IF(EE>150%,150%,EE+uplift)` and `Scenario Amount = Scenario Achievement × AS`.
- The uploaded workbook has a few manual/locked exception rows; standard 5/10/15 values are read directly from the saved columns so they remain exact.

**FINAL**
- Target = `F39 = SUM('RM Retail Sales'!AS:AS)`
- Current projected NS = the saved current-RR basis, equal to `SUM(AU3:AU529)/3*12`
- 5% = `EJ2*3 + G39`
- 10% = `EL2*3 + G39`
- 15% = `EN2*3 + G39`
- `G39 = SUM('RM Retail Sales'!AU:AU)`
- Achievement % = projected NS / target
- PBT = projected NS × 0.6%
- Incremental PBT = scenario PBT − current PBT
- Kitty = 15% × incremental PBT
            """
        )

    trip_cost_lakh = st.number_input(
        "Foreign Trip Cost per Qualified Person (₹ lakh)",
        min_value=0.0,
        max_value=100.0,
        value=3.0,
        step=0.25,
        key="page4_trip_cost",
    )

    current = build_exact_scenario(filtered_base, 0, au1_adjustment)
    s5 = build_exact_scenario(filtered_base, 5, au1_adjustment)
    s10 = build_exact_scenario(filtered_base, 10, au1_adjustment)
    s15 = build_exact_scenario(filtered_base, 15, au1_adjustment)
    custom = build_exact_scenario(filtered_base, custom_uplift, au1_adjustment)

    scenario_map = {
        "Current": (current, 0.0),
        "+5%": (s5, 5.0),
        "+10%": (s10, 10.0),
        "+15%": (s15, 15.0),
        f"Custom +{custom_uplift:.1f}%": (custom, float(custom_uplift)),
    }

    comparison = pd.DataFrame(
        [
            scenario_summary(df, label, uplift, current)
            for label, (df, uplift) in scenario_map.items()
        ]
    )

    comparison["Trip Cost / Person (₹ lakh)"] = trip_cost_lakh
    comparison["Total Trip Cost (₹ Cr)"] = (
        comparison["RMs >100%"] * trip_cost_lakh / 100.0
    )
    comparison["Qualifying Revenue After Trip Cost"] = (
        comparison["Qualifying Revenue"] - comparison["Total Trip Cost (₹ Cr)"]
    )
    comparison["Trip Cost as % of Qualifying Revenue"] = np.where(
        comparison["Qualifying Revenue"] != 0,
        comparison["Total Trip Cost (₹ Cr)"] / comparison["Qualifying Revenue"] * 100,
        0,
    )

    section(
        "Executive Comparison",
        "This is the Excel-consistent equivalent of the FINAL matrix, expanded with qualification contribution and trip economics.",
    )
    showdf(comparison)

    # Always validate the unfiltered source workbook against FINAL.
    render_workbook_validation(full_base, benchmark, au1_adjustment)

    render_management_summary(comparison, current, trip_cost_lakh)

    section(
        "Qualified RM Revenue & Foreign Trip Cost",
        "Number of qualified RMs, their NS contribution, PBT / Revenue and the cost of taking all qualified RMs on the trip.",
    )
    showdf(
        comparison[
            [
                "Scenario",
                "RMs >100%",
                "Qualification Rate %",
                "Qualifying RM NS",
                "Qualifying NS Contribution %",
                "Qualifying Revenue",
                "Trip Cost / Person (₹ lakh)",
                "Total Trip Cost (₹ Cr)",
                "Qualifying Revenue After Trip Cost",
                "Trip Cost as % of Qualifying Revenue",
            ]
        ]
    )

    left, right = st.columns(2)
    with left:
        fig = go.Figure()
        fig.add_bar(
            x=comparison["Scenario"],
            y=comparison["Total Projected NS"],
            name="Total Projected NS",
            marker_color="#555555",
        )
        fig.add_bar(
            x=comparison["Scenario"],
            y=comparison["Qualifying RM NS"],
            name="NS from >100% RMs",
            marker_color=GOLD,
        )
        fig.update_layout(title="Total NS vs NS from >100% RMs", barmode="group")
        st.plotly_chart(style(fig, 420), config={"displayModeBar": False})

    with right:
        fig = go.Figure()
        fig.add_bar(
            x=comparison["Scenario"],
            y=comparison["RMs >100%"],
            name="RMs >100%",
            marker_color=GOLD,
        )
        fig.add_scatter(
            x=comparison["Scenario"],
            y=comparison["Qualifying NS Contribution %"],
            mode="lines+markers",
            yaxis="y2",
            name="Qualifying NS Contribution %",
            line=dict(color=TEXT, width=2),
        )
        fig.update_layout(
            title="Qualifier Count & NS Contribution",
            yaxis_title="RMs >100%",
            yaxis2=dict(title="Contribution %", overlaying="y", side="right"),
        )
        st.plotly_chart(style(fig, 420), config={"displayModeBar": False})

    section(
        "FINAL-Style Achievement Bucketing",
        "These are the exact broad buckets used by FINAL: <0, 0-30, 30-50, 50-80, 80-100 and >100.",
    )
    showdf(broad_bucket_comparison(scenario_map))

    section(
        "Detailed Scenario Analysis",
        "Each scenario contains Market Type contribution, 5% buckets, 90-100% conversion economics and an RM action list.",
    )

    tabs = st.tabs(list(scenario_map.keys()))

    for tab, (label, (df, uplift)) in zip(tabs, scenario_map.items()):
        with tab:
            total_target = df["FY 26 TGT EQ NS"].sum(skipna=True)
            total_ns = df["Projected Final NS"].sum(skipna=True)
            q = df["Qualified"]
            q_ns = df.loc[q, "Projected Final NS"].sum(skipna=True)
            eligible = int(df["Achievement Basis"].notna().sum())

            cols = st.columns(6)
            cards = [
                ("Total Target", fmt(total_target), "AS sum", False),
                ("Total Projected NS", fmt(total_ns), pct(total_ns / total_target * 100) if total_target else "", True),
                ("Revenue / PBT", fmt(revenue(total_ns)), "NS × 0.6%", False),
                ("RMs >100%", int(q.sum()), pct(q.sum() / eligible * 100) if eligible else "", True),
                ("Qualified NS", fmt(q_ns), pct(q_ns / total_ns * 100) if total_ns else "", True),
                ("Qualified Revenue", fmt(revenue(q_ns)), "Qualified NS × 0.6%", True),
            ]
            for i, card in enumerate(cards):
                with cols[i]:
                    kpi(*card)

            section(
                "Market Type Contribution",
                "B30 includes B30-Select; T30 includes T30-Ext. Shows count, target, YTD NS, projected NS, Revenue, qualifiers and contribution.",
            )
            showdf(market_summary(df))

            section(
                "5% Achievement Buckets by Market Type",
                "5-point bands for every Market Type, with projected final NS, YTD contribution, Revenue and conversion economics.",
            )
            showdf(detailed_bucket_table(df, trip_cost_lakh), 720)

            section(
                "90%-100% Conversion Opportunity by Market Type",
                "How many RMs are close to 100%, the NS they already produce, additional NS / Revenue required and additional foreign-trip cost if converted.",
            )
            near = near_miss_table(df, trip_cost_lakh)
            showdf(near)

            section(
                "90%-100% RM Action List",
                "Individual near-miss RMs sorted closest to the threshold first.",
            )
            action = df.loc[df["Achievement Basis"].between(0.90, 1.00, inclusive="both")].copy()
            if action.empty:
                st.info("No RMs between 90% and 100% in this selection.")
            else:
                action["Additional NS to 100%"] = (
                    np.maximum(0, 1.0 - action["Achievement Basis"])
                    * action["FY 26 TGT EQ NS"]
                    * 3.0
                )
                action["Additional Revenue"] = revenue(action["Additional NS to 100%"])
                action["Additional Trip Cost (₹ Cr)"] = trip_cost_lakh / 100.0
                action["Net Additional Revenue After Trip"] = (
                    action["Additional Revenue"] - action["Additional Trip Cost (₹ Cr)"]
                )
                action["% Contribution to Total Projected NS"] = np.where(
                    total_ns != 0,
                    action["Projected Final NS"] / total_ns * 100,
                    0,
                )
                cols_action = [
                    "Emp Code",
                    "Employee Name",
                    "Market Type",
                    "ZONE",
                    "REGION",
                    "FY 26 TGT EQ NS",
                    "Equity NS Ach YTD June",
                    "Achievement Basis",
                    "Projected Final NS",
                    "% Contribution to Total Projected NS",
                    "Revenue",
                    "Additional NS to 100%",
                    "Additional Revenue",
                    "Additional Trip Cost (₹ Cr)",
                    "Net Additional Revenue After Trip",
                ]
                display = action[cols_action].copy()
                display["Achievement Basis"] = display["Achievement Basis"] * 100.0
                display = display.rename(columns={"Achievement Basis": "Achievement Basis %"})
                showdf(display.sort_values("Achievement Basis %", ascending=False), 560)

    section(
        "What Do We Gain by Increasing the Scenario?",
        "Sensitivity versus the current workbook projection.",
    )
    showdf(
        comparison[
            [
                "Scenario",
                "Run Rate / Achievement Uplift %",
                "RMs >100%",
                "Newly >100% vs Current",
                "Total Projected NS",
                "Revenue / PBT",
                "Incremental NS vs Current",
                "Incremental Revenue vs Current",
                "Qualifying RM NS",
                "Qualifying Revenue",
                "Qualifying NS Contribution %",
                "Total Trip Cost (₹ Cr)",
            ]
        ]
    )


# ============================================================
# MAIN APP
# ============================================================

st.html(
    """
<div class="hero">
    <div class="eyebrow">RM Equity Net Sales · Strategy Lab</div>
    <div class="hero-title">Excel-Consistent Target & Incentive Analysis</div>
    <div class="hero-sub">
        The calculation engine is built from the uploaded RM Retail Sales and FINAL sheets rather than a generic run-rate assumption.
    </div>
</div>
"""
)

with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio(
        "Page",
        [
            "1 · Scenario Lab",
            "2 · New Insights",
            "3 · BonVoyage",
            "4 · Run Rate Analysis",
        ],
    )
    st.divider()
    uploaded = st.file_uploader("Upload RM Workbook", type=["xlsx"])

if uploaded is None:
    st.info("Upload the Excel workbook containing RM Retail Sales and FINAL sheets.")
    st.stop()

try:
    full_base, benchmark, au1_adjustment = load_model(uploaded.getvalue())
except Exception as exc:
    st.error(f"Could not read workbook: {exc}")
    st.stop()

with st.sidebar:
    st.divider()
    st.markdown("### Filters")
    st.caption("Defaults use all rows so the dashboard matches FINAL before filtering.")

    market_values = sorted(
        x for x in full_base["Market Type"].dropna().unique().tolist() if x != "Unknown"
    )
    selected_market_type = st.selectbox(
        "Market Type",
        ["All Market Types"] + market_values,
        help="B30 includes B30-Select; T30 includes T30-Ext.",
    )
    st.caption("B30 = B30 + B30-Select · T30 = T30 + T30-Ext")

    status_values = sorted(x for x in full_base["Status"].dropna().unique().tolist() if x != "")
    type_values = sorted(x for x in full_base["Type"].dropna().unique().tolist() if x != "")
    zone_values = sorted(x for x in full_base["ZONE"].dropna().unique().tolist() if x != "")
    region_values = sorted(x for x in full_base["REGION"].dropna().unique().tolist() if x != "")

    selected_status = st.multiselect("Status", status_values, default=status_values)
    selected_type = st.multiselect("Type", type_values, default=type_values)
    selected_zone = st.multiselect("Zone", zone_values, default=zone_values)
    selected_region = st.multiselect("Region", region_values, default=region_values)

    selected_uplift = 10.0
    if page == "1 · Scenario Lab":
        st.divider()
        st.markdown("### Scenario")
        choice = st.selectbox("Achievement Uplift", ["5%", "10%", "15%", "Custom"], index=1)
        if choice == "Custom":
            selected_uplift = st.number_input(
                "Custom Achievement Uplift (%)",
                min_value=-100.0,
                max_value=500.0,
                value=10.0,
                step=1.0,
            )
        else:
            selected_uplift = float(choice.replace("%", ""))

    custom_uplift = 20.0
    if page == "4 · Run Rate Analysis":
        st.divider()
        st.markdown("### Custom Scenario")
        custom_uplift = st.number_input(
            "Custom Achievement Uplift (%)",
            min_value=-100.0,
            max_value=500.0,
            value=20.0,
            step=1.0,
            help="5/10/15 are read from Excel exactly. Other values follow the same rule and preserve locked rows.",
        )

filtered_base = filter_data(
    full_base,
    selected_market_type,
    selected_status,
    selected_type,
    selected_zone,
    selected_region,
)

if filtered_base.empty:
    st.warning("No RMs remain after the selected filters.")
    st.stop()

if page == "1 · Scenario Lab":
    page1(filtered_base, au1_adjustment, selected_uplift)
elif page == "2 · New Insights":
    page2(filtered_base, au1_adjustment)
elif page == "3 · BonVoyage":
    page3(filtered_base, au1_adjustment)
else:
    page4(
        filtered_base,
        full_base,
        benchmark,
        au1_adjustment,
        custom_uplift,
        selected_market_type,
    )
