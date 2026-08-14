# import io
# from typing import Dict, List, Tuple

# import numpy as np
# import pandas as pd
# import streamlit as st


# st.set_page_config(
#     page_title="Sales Performance Scenario Planner",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# st.markdown(
#     """
# <style>
# .block-container {
#     max-width: 1500px;
#     padding-top: 0.6rem;
#     padding-bottom: 2.5rem;
# }

# /* ------------------------------
#    APP BACKGROUND + TEXT
# ------------------------------ */
# .stApp {
#     background: #06101f;
#     color: #f8fafc;
# }

# h1, h2, h3, h4, h5, h6 {
#     color: #f8fafc !important;
# }

# p, div, label, span {
#     color: #cbd5e1;
# }

# /* ------------------------------
#    SIDEBAR
# ------------------------------ */
# section[data-testid="stSidebar"] {
#     background: #e5e7eb;
#     border-right: 1px solid #cbd5e1;
# }

# section[data-testid="stSidebar"] * {
#     color: #0f172a !important;
# }

# /* ------------------------------
#    METRIC CARDS
# ------------------------------ */
# div[data-testid="stMetric"] {
#     background: #111827 !important;
#     border: 1px solid #334155 !important;
#     border-radius: 14px !important;
#     padding: 0.8rem 0.9rem !important;
#     min-height: 108px;
#     box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
# }

# div[data-testid="stMetricLabel"] {
#     color: #94a3b8 !important;
#     font-weight: 700 !important;
#     font-size: 0.85rem !important;
# }

# div[data-testid="stMetricValue"] {
#     color: #f8fafc !important;
#     font-weight: 800 !important;
#     font-size: 2rem !important;
# }

# div[data-testid="stMetricDelta"] {
#     color: #22c55e !important;
#     font-weight: 700 !important;
# }

# /* fallback for older streamlit metric text rendering */
# div[data-testid="stMetric"] label,
# div[data-testid="stMetric"] p,
# div[data-testid="stMetric"] span {
#     color: #94a3b8 !important;
# }

# div[data-testid="stMetric"] [data-testid="stMarkdownContainer"] p {
#     color: #f8fafc !important;
# }

# /* ------------------------------
#    TABLES / DATAFRAMES
# ------------------------------ */
# div[data-testid="stDataFrame"] {
#     border: 1px solid #334155;
#     border-radius: 12px;
#     overflow: hidden;
# }

# /* ------------------------------
#    EXPANDER
# ------------------------------ */
# [data-testid="stExpander"] {
#     border: 1px solid #334155;
#     border-radius: 12px;
#     background: #0f172a;
# }

# [data-testid="stExpander"] * {
#     color: #e2e8f0 !important;
# }

# /* ------------------------------
#    BUTTONS
# ------------------------------ */
# .stButton > button,
# .stDownloadButton > button {
#     background: #1d4ed8 !important;
#     color: white !important;
#     border: 1px solid #2563eb !important;
#     border-radius: 10px !important;
#     font-weight: 700 !important;
# }

# .stButton > button:hover,
# .stDownloadButton > button:hover {
#     background: #2563eb !important;
#     color: white !important;
# }

# /* ------------------------------
#    RADIO BUTTON AREA
# ------------------------------ */
# div[role="radiogroup"] label {
#     background: transparent;
#     border-radius: 8px;
# }

# /* ------------------------------
#    HORIZONTAL RULE
# ------------------------------ */
# hr {
#     margin: 0.7rem 0;
#     border-color: #334155;
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ================================================================
# # WORKBOOK STRUCTURE
# # ================================================================

# VERTICAL_SHEETS = {
#     "Retail": "RM Retail Sales",
#     "DHNI": "RM DHNI",
# }


# ASSETS = [
#     "Equity",
#     "Debt",
#     "Liquid",
# ]


# MODES = [
#     "GS",
#     "NS",
# ]


# MODE_COLUMNS = {

#     "GS": {

#         "Equity": (
#             "FY 26 TGT EQ",
#             "Equity GS Ach YTD June",
#         ),

#         "Debt": (
#             "FY 26 TGT DT",
#             "Debt GS Ach",
#         ),

#         "Liquid": (
#             "FY 26 TGT LIQ",
#             "Liquid GS Ach",
#         ),
#     },

#     "NS": {

#         "Equity": (
#             "FY 26 TGT EQ NS",
#             "Equity NS Ach YTD June",
#         ),

#         "Debt": (
#             "FY 26 TGT DT NS",
#             "Debt NS Ach",
#         ),

#         "Liquid": (
#             "FY 26 TGT LIQ NS",
#             "Liquid NS Ach",
#         ),
#     },
# }


# YTD_TARGET_COLUMNS = {

#     "GS": {

#         "Equity":
#             "YTD June EQ TGT",

#         "Debt":
#             "YTD June DT TGT",

#         "Liquid":
#             "YTD June LIQ TGT",
#     },

#     "NS": {

#         "Equity":
#             "YTD June EQ NS TGT",

#         "Debt":
#             "YTD June DT NS TGT",

#         "Liquid":
#             "YTD June LIQ NS TGT",
#     },
# }


# REQUIRED_COLUMNS = sorted(

#     {"Employee Name"}

#     |

#     {
#         column

#         for mode in MODE_COLUMNS.values()

#         for pair in mode.values()

#         for column in pair
#     }
# )


# # ================================================================
# # FY TIMELINE
# # ================================================================

# # April, May and June completed.
# MONTHS_COMPLETED = 3


# # July -> March
# MONTHS_TO_MARCH = 9


# # July -> January
# MONTHS_TO_JAN = 7


# # February + March
# FEB_MAR_MONTHS = 2


# # ================================================================
# # SCENARIOS
# # ================================================================

# SCENARIOS = {

#     "scenario_1": {

#         "label":
#             "Scenario 1",

#         "name":
#             "+20% Run-Rate Push",

#         "milestone":
#             "March",

#         "description":
#             (
#                 "Increase the current monthly run rate "
#                 "by 20% from July onward and see where "
#                 "the business lands by March."
#             ),
#     },


#     "scenario_2": {

#         "label":
#             "Scenario 2",

#         "name":
#             "75% Overall by Jan + 100% Equity",

#         "milestone":
#             "January",

#         "description":
#             (
#                 "By January, Equity reaches 100% of FY "
#                 "target and the portfolio reaches at "
#                 "least 75% overall. Debt and Liquid "
#                 "balance the remainder."
#             ),
#     },


#     "scenario_3": {

#         "label":
#             "Scenario 3",

#         "name":
#             "100% by Jan, Then Feb-Mar Dip",

#         "milestone":
#             "January",

#         "description":
#             (
#                 "Reach 100% by January, then reduce "
#                 "the February-March monthly run rate "
#                 "by the selected dip percentage."
#             ),
#     },


#     "scenario_4": {

#         "label":
#             "Scenario 4",

#         "name":
#             "120% by March",

#         "milestone":
#             "March",

#         "description":
#             (
#                 "Build the monthly requirement needed "
#                 "to close March at 120% of FY target "
#                 "across Equity, Debt and Liquid."
#             ),
#     },


#     "scenario_5": {

#         "label":
#             "Scenario 5",

#         "name":
#             "120% Equity + 100% Overall by March",

#         "milestone":
#             "March",

#         "description":
#             (
#                 "Close Equity at 120% while the complete "
#                 "portfolio closes at least 100% overall "
#                 "by March. Debt and Liquid balance "
#                 "the remainder."
#             ),
#     },
# }


# # ================================================================
# # BASIC HELPERS
# # ================================================================

# def rerun_app() -> None:

#     if hasattr(
#         st,
#         "rerun",
#     ):

#         st.rerun()

#     else:

#         st.experimental_rerun()


# def normalize_column_name(
#     value: object
# ) -> str:

#     return " ".join(

#         str(value)
#         .replace(
#             "\u00a0",
#             " ",
#         )
#         .strip()
#         .split()
#     )


# def clean_numeric(
#     series: pd.Series
# ) -> pd.Series:

#     return pd.to_numeric(
#         series,
#         errors="coerce",
#     ).fillna(
#         0.0
#     )


# def normalize_frame(
#     df: pd.DataFrame
# ) -> pd.DataFrame:

#     out = df.copy()


#     out.columns = [

#         normalize_column_name(
#             column
#         )

#         for column in out.columns
#     ]


#     if (
#         "Employee Name"
#         in out.columns
#     ):

#         names = (
#             out[
#                 "Employee Name"
#             ]
#             .astype(str)
#             .str.strip()
#         )


#         mask = (

#             out[
#                 "Employee Name"
#             ].notna()

#             &

#             names.ne("")

#             &

#             names.str.lower().ne(
#                 "nan"
#             )

#             &

#             names.str.lower().ne(
#                 "total"
#             )

#             &

#             ~names.str.lower().str.startswith(
#                 "grand total"
#             )
#         )


#         out = (
#             out
#             .loc[
#                 mask
#             ]
#             .copy()
#         )


#     return out


# def validate_frame(
#     df: pd.DataFrame
# ) -> Tuple[
#     bool,
#     List[str],
# ]:

#     missing = [

#         column

#         for column
#         in REQUIRED_COLUMNS

#         if column
#         not in df.columns
#     ]


#     return (
#         not missing,
#         missing,
#     )


# # ================================================================
# # LOAD WORKBOOK
# # ================================================================

# def load_workbook(
#     uploaded_file
# ) -> Dict[
#     str,
#     pd.DataFrame,
# ]:

#     xls = pd.ExcelFile(
#         uploaded_file,
#         engine="openpyxl",
#     )


#     missing_sheets = [

#         sheet

#         for sheet
#         in VERTICAL_SHEETS.values()

#         if sheet
#         not in xls.sheet_names
#     ]


#     if missing_sheets:

#         raise ValueError(

#             "Missing required sheet(s): "

#             +

#             ", ".join(
#                 missing_sheets
#             )
#         )


#     frames = {}

#     errors = []


#     for (
#         vertical,
#         sheet,
#     ) in VERTICAL_SHEETS.items():


#         frame = pd.read_excel(
#             xls,
#             sheet_name=sheet,
#         )


#         frame = normalize_frame(
#             frame
#         )


#         valid, missing = (
#             validate_frame(
#                 frame
#             )
#         )


#         if not valid:

#             errors.append(

#                 f"{vertical}: "
#                 +
#                 ", ".join(
#                     missing
#                 )
#             )


#         frames[
#             vertical
#         ] = frame


#     if errors:

#         raise ValueError(

#             "Missing required columns — "

#             +

#             " | ".join(
#                 errors
#             )
#         )


#     return frames


# # ================================================================
# # DISPLAY HELPERS
# # ================================================================

# def fmt_amount(
#     value: float
# ) -> str:

#     if pd.isna(
#         value
#     ):

#         return "—"


#     return (
#         f"{value:,.0f}"
#     )


# def fmt_pct(
#     value: float
# ) -> str:

#     if pd.isna(
#         value
#     ):

#         return "—"


#     return (
#         f"{value * 100:.1f}%"
#     )


# def fmt_delta(
#     value: float
# ) -> str:

#     if pd.isna(
#         value
#     ):

#         return "—"


#     return (
#         f"{value * 100:+.1f}% "
#         f"vs current"
#     )


# def combine_frames(
#     frames:
#         Dict[
#             str,
#             pd.DataFrame,
#         ]
# ) -> pd.DataFrame:

#     return pd.concat(

#         [

#             frames[
#                 vertical
#             ]

#             for vertical
#             in VERTICAL_SHEETS
#         ],

#         ignore_index=True,
#     )


# # ================================================================
# # CURRENT BASELINE CALCULATION
# # ================================================================

# def current_asset_stats(
#     df: pd.DataFrame,
#     mode: str,
# ) -> pd.DataFrame:

#     rows = []


#     for asset in ASSETS:


#         (
#             target_col,
#             actual_col,
#         ) = (
#             MODE_COLUMNS[
#                 mode
#             ][
#                 asset
#             ]
#         )


#         fy_target = float(

#             clean_numeric(
#                 df[
#                     target_col
#                 ]
#             ).sum()
#         )


#         actual = float(

#             clean_numeric(
#                 df[
#                     actual_col
#                 ]
#             ).sum()
#         )


#         ytd_col = (
#             YTD_TARGET_COLUMNS[
#                 mode
#             ][
#                 asset
#             ]
#         )


#         if ytd_col in df.columns:

#             ytd_target = float(

#                 clean_numeric(
#                     df[
#                         ytd_col
#                     ]
#                 ).sum()
#             )

#         else:

#             ytd_target = (

#                 fy_target

#                 *

#                 MONTHS_COMPLETED

#                 /

#                 12.0
#             )


#         run_rate = (

#             actual

#             /

#             MONTHS_COMPLETED
#         )


#         march_projection = (

#             actual

#             +

#             run_rate

#             *

#             MONTHS_TO_MARCH
#         )


#         rows.append(
#             {

#                 "Asset":
#                     asset,

#                 "FY Target":
#                     fy_target,

#                 "YTD Target":
#                     ytd_target,

#                 "YTD Achievement":
#                     actual,

#                 "Target Achieved %":
#                     (
#                         actual
#                         /
#                         ytd_target

#                         if ytd_target > 0

#                         else 0.0
#                     ),

#                 "Current Run Rate":
#                     run_rate,

#                 "Current March Projection":
#                     march_projection,

#                 "Current March Projection %":
#                     (
#                         march_projection
#                         /
#                         fy_target

#                         if fy_target > 0

#                         else 0.0
#                     ),
#             }
#         )


#     return (

#         pd.DataFrame(
#             rows
#         )

#         .set_index(
#             "Asset"
#         )
#     )


# def summarize_current(
#     stats: pd.DataFrame
# ) -> Dict[
#     str,
#     float,
# ]:

#     fy_target = float(

#         stats[
#             "FY Target"
#         ].sum()
#     )


#     ytd_target = float(

#         stats[
#             "YTD Target"
#         ].sum()
#     )


#     actual = float(

#         stats[
#             "YTD Achievement"
#         ].sum()
#     )


#     run_rate = float(

#         stats[
#             "Current Run Rate"
#         ].sum()
#     )


#     march_projection = float(

#         stats[
#             "Current March Projection"
#         ].sum()
#     )


#     return {

#         "FY Target":
#             fy_target,

#         "YTD Target":
#             ytd_target,

#         "YTD Achievement":
#             actual,

#         "Target Achieved %":
#             (
#                 actual
#                 /
#                 ytd_target

#                 if ytd_target > 0

#                 else 0.0
#             ),

#         "Current Run Rate":
#             run_rate,

#         "Current March Projection":
#             march_projection,

#         "Current March Projection %":
#             (
#                 march_projection
#                 /
#                 fy_target

#                 if fy_target > 0

#                 else 0.0
#             ),
#     }


# def build_current_overview(
#     all_frame: pd.DataFrame
# ):

#     stats = {

#         mode:

#             current_asset_stats(
#                 all_frame,
#                 mode,
#             )

#         for mode
#         in MODES
#     }


#     rows = []


#     for mode in MODES:


#         summary = (
#             summarize_current(
#                 stats[
#                     mode
#                 ]
#             )
#         )


#         rows.append(
#             {

#                 "Sales":
#                     (
#                         "Gross Sales"

#                         if mode == "GS"

#                         else
#                         "Net Sales"
#                     ),

#                 "FY Target":
#                     summary[
#                         "FY Target"
#                     ],

#                 "YTD Target":
#                     summary[
#                         "YTD Target"
#                     ],

#                 "YTD Achievement":
#                     summary[
#                         "YTD Achievement"
#                     ],

#                 "Target Achieved %":
#                     summary[
#                         "Target Achieved %"
#                     ],

#                 "Current Run Rate / Month":
#                     summary[
#                         "Current Run Rate"
#                     ],

#                 "Current March Projection":
#                     summary[
#                         "Current March Projection"
#                     ],

#                 "Current March Projection %":
#                     summary[
#                         "Current March Projection %"
#                     ],
#             }
#         )


#     return (
#         pd.DataFrame(
#             rows
#         ),
#         stats,
#     )


# # ================================================================
# # SCENARIO TARGET ALLOCATION
# # ================================================================

# def allocate_non_equity(
#     stats: pd.DataFrame,
#     equity_mult: float,
#     overall_mult: float,
# ) -> pd.Series:


#     equity_target = float(

#         stats.loc[
#             "Equity",
#             "FY Target",
#         ]
#     )


#     debt_target = float(

#         stats.loc[
#             "Debt",
#             "FY Target",
#         ]
#     )


#     liquid_target = float(

#         stats.loc[
#             "Liquid",
#             "FY Target",
#         ]
#     )


#     overall_target_amount = (

#         (
#             equity_target
#             +
#             debt_target
#             +
#             liquid_target
#         )

#         *

#         overall_mult
#     )


#     required_equity = (

#         equity_target

#         *

#         equity_mult
#     )


#     remaining = max(

#         overall_target_amount
#         -
#         required_equity,

#         0.0,
#     )


#     non_equity_base = (

#         debt_target
#         +
#         liquid_target
#     )


#     if non_equity_base > 0:

#         required_debt = (

#             remaining

#             *

#             debt_target

#             /

#             non_equity_base
#         )


#         required_liquid = (

#             remaining

#             *

#             liquid_target

#             /

#             non_equity_base
#         )


#     else:

#         required_debt = 0.0

#         required_liquid = 0.0


#     return pd.Series(
#         {

#             "Equity":
#                 required_equity,

#             "Debt":
#                 required_debt,

#             "Liquid":
#                 required_liquid,
#         }
#     )


# # ================================================================
# # SCENARIO CALCULATION ENGINE
# # ================================================================

# def scenario_stats(
#     current: pd.DataFrame,
#     scenario_key: str,
#     dip_pct: float,
# ) -> pd.DataFrame:


#     out = current.copy()


#     actual = (
#         out[
#             "YTD Achievement"
#         ]
#         .astype(float)
#     )


#     target = (
#         out[
#             "FY Target"
#         ]
#         .astype(float)
#     )


#     current_rr = (
#         out[
#             "Current Run Rate"
#         ]
#         .astype(float)
#     )


#     # ------------------------------------------------------------
#     # SCENARIO 1
#     # +20% current monthly run rate
#     # ------------------------------------------------------------

#     if scenario_key == "scenario_1":


#         scenario_rr = (

#             current_rr

#             *

#             1.20
#         )


#         milestone = (

#             actual

#             +

#             scenario_rr

#             *

#             MONTHS_TO_MARCH
#         )


#         feb_mar_rr = (
#             scenario_rr.copy()
#         )


#         march_projection = (
#             milestone.copy()
#         )


#     # ------------------------------------------------------------
#     # SCENARIO 2
#     # 75% overall by Jan
#     # 100% Equity by Jan
#     # ------------------------------------------------------------

#     elif scenario_key == "scenario_2":


#         january_target = (
#             allocate_non_equity(

#                 out,

#                 equity_mult=1.00,

#                 overall_mult=0.75,
#             )
#         )


#         milestone = (

#             pd.concat(
#                 [
#                     actual,
#                     january_target,
#                 ],
#                 axis=1,
#             )

#             .max(
#                 axis=1
#             )
#         )


#         scenario_rr = (

#             (
#                 milestone
#                 -
#                 actual
#             )
#             .clip(
#                 lower=0
#             )

#             /

#             MONTHS_TO_JAN
#         )


#         # For March projection,
#         # continue January-required pace
#         # through February and March.

#         feb_mar_rr = (
#             scenario_rr.copy()
#         )


#         march_projection = (

#             milestone

#             +

#             feb_mar_rr

#             *

#             FEB_MAR_MONTHS
#         )


#     # ------------------------------------------------------------
#     # SCENARIO 3
#     # 100% by Jan
#     # dip in Feb and March
#     # ------------------------------------------------------------

#     elif scenario_key == "scenario_3":


#         january_target = (
#             target.copy()
#         )


#         milestone = (

#             pd.concat(
#                 [
#                     actual,
#                     january_target,
#                 ],
#                 axis=1,
#             )

#             .max(
#                 axis=1
#             )
#         )


#         scenario_rr = (

#             (
#                 milestone
#                 -
#                 actual
#             )
#             .clip(
#                 lower=0
#             )

#             /

#             MONTHS_TO_JAN
#         )


#         feb_mar_rr = (

#             scenario_rr

#             *

#             (
#                 1.0
#                 -
#                 dip_pct
#             )
#         )


#         march_projection = (

#             milestone

#             +

#             feb_mar_rr

#             *

#             FEB_MAR_MONTHS
#         )


#     # ------------------------------------------------------------
#     # SCENARIO 4
#     # 120% by March
#     # ------------------------------------------------------------

#     elif scenario_key == "scenario_4":


#         march_target = (

#             target

#             *

#             1.20
#         )


#         milestone = (

#             pd.concat(
#                 [
#                     actual,
#                     march_target,
#                 ],
#                 axis=1,
#             )

#             .max(
#                 axis=1
#             )
#         )


#         scenario_rr = (

#             (
#                 milestone
#                 -
#                 actual
#             )
#             .clip(
#                 lower=0
#             )

#             /

#             MONTHS_TO_MARCH
#         )


#         feb_mar_rr = (
#             scenario_rr.copy()
#         )


#         march_projection = (
#             milestone.copy()
#         )


#     # ------------------------------------------------------------
#     # SCENARIO 5
#     # Equity 120%
#     # Overall 100%
#     # ------------------------------------------------------------

#     elif scenario_key == "scenario_5":


#         march_target = (
#             allocate_non_equity(

#                 out,

#                 equity_mult=1.20,

#                 overall_mult=1.00,
#             )
#         )


#         milestone = (

#             pd.concat(
#                 [
#                     actual,
#                     march_target,
#                 ],
#                 axis=1,
#             )

#             .max(
#                 axis=1
#             )
#         )


#         scenario_rr = (

#             (
#                 milestone
#                 -
#                 actual
#             )
#             .clip(
#                 lower=0
#             )

#             /

#             MONTHS_TO_MARCH
#         )


#         feb_mar_rr = (
#             scenario_rr.copy()
#         )


#         march_projection = (
#             milestone.copy()
#         )


#     else:

#         raise ValueError(
#             f"Unknown scenario: {scenario_key}"
#         )


#     out[
#         "Scenario Run Rate"
#     ] = scenario_rr


#     out[
#         "Run Rate Change %"
#     ] = np.where(

#         current_rr > 0,

#         scenario_rr
#         /
#         current_rr
#         -
#         1.0,

#         np.where(

#             scenario_rr > 0,

#             np.nan,

#             0.0,
#         ),
#     )


#     out[
#         "Scenario Milestone %"
#     ] = np.where(

#         target > 0,

#         milestone
#         /
#         target,

#         0.0,
#     )


#     out[
#         "Feb-Mar Run Rate"
#     ] = feb_mar_rr


#     out[
#         "Scenario March Projection"
#     ] = march_projection


#     out[
#         "Scenario March Projection %"
#     ] = np.where(

#         target > 0,

#         march_projection
#         /
#         target,

#         0.0,
#     )


#     return out


# # ================================================================
# # SCENARIO SUMMARY
# # ================================================================

# def summarize_scenario(
#     stats: pd.DataFrame
# ) -> Dict[
#     str,
#     float,
# ]:


#     target = float(

#         stats[
#             "FY Target"
#         ].sum()
#     )


#     milestone_amount = float(

#         (
#             stats[
#                 "Scenario Milestone %"
#             ]

#             *

#             stats[
#                 "FY Target"
#             ]
#         ).sum()
#     )


#     march_projection = float(

#         stats[
#             "Scenario March Projection"
#         ].sum()
#     )


#     return {

#         "Scenario Run Rate":
#             float(

#                 stats[
#                     "Scenario Run Rate"
#                 ].sum()
#             ),

#         "Scenario Milestone %":
#             (
#                 milestone_amount
#                 /
#                 target

#                 if target > 0

#                 else 0.0
#             ),

#         "Scenario March Projection %":
#             (
#                 march_projection
#                 /
#                 target

#                 if target > 0

#                 else 0.0
#             ),
#     }


# # ================================================================
# # BASELINE VS SCENARIO
# # ================================================================

# def build_comparison(
#     mode_stats,
#     scenario_key: str,
#     dip_pct: float,
# ):


#     scenarios = {

#         mode:

#             scenario_stats(

#                 mode_stats[
#                     mode
#                 ],

#                 scenario_key,

#                 dip_pct,
#             )

#         for mode
#         in MODES
#     }


#     rows = []


#     for mode in MODES:


#         current = (
#             summarize_current(

#                 mode_stats[
#                     mode
#                 ]
#             )
#         )


#         scenario = (
#             summarize_scenario(

#                 scenarios[
#                     mode
#                 ]
#             )
#         )


#         current_rr = (
#             current[
#                 "Current Run Rate"
#             ]
#         )


#         scenario_rr = (
#             scenario[
#                 "Scenario Run Rate"
#             ]
#         )


#         if current_rr > 0:

#             rr_change = (

#                 scenario_rr
#                 /
#                 current_rr

#                 -

#                 1.0
#             )

#         else:

#             rr_change = np.nan


#         rows.append(
#             {

#                 "Sales":
#                     (
#                         "Gross Sales"

#                         if mode == "GS"

#                         else
#                         "Net Sales"
#                     ),

#                 "Current Run Rate":
#                     current_rr,

#                 "Scenario Run Rate":
#                     scenario_rr,

#                 "Run Rate Change %":
#                     rr_change,

#                 "Current March Projection %":
#                     current[
#                         "Current March Projection %"
#                     ],

#                 "Scenario Milestone":
#                     SCENARIOS[
#                         scenario_key
#                     ][
#                         "milestone"
#                     ],

#                 "Scenario Milestone %":
#                     scenario[
#                         "Scenario Milestone %"
#                     ],

#                 "Scenario March Projection %":
#                     scenario[
#                         "Scenario March Projection %"
#                     ],

#                 "March Projection Δ pp":
#                     (
#                         scenario[
#                             "Scenario March Projection %"
#                         ]

#                         -

#                         current[
#                             "Current March Projection %"
#                         ]
#                     )

#                     *

#                     100,
#             }
#         )


#     return (
#         pd.DataFrame(
#             rows
#         ),
#         scenarios,
#     )


# # ================================================================
# # RETAIL / DHNI SUMMARY
# # ================================================================

# def build_vertical_summary(
#     frames,
#     scenario_key: str,
#     dip_pct: float,
# ) -> pd.DataFrame:


#     rows = []


#     for vertical in VERTICAL_SHEETS:


#         for mode in MODES:


#             current_stats = (
#                 current_asset_stats(

#                     frames[
#                         vertical
#                     ],

#                     mode,
#                 )
#             )


#             scen_stats = (
#                 scenario_stats(

#                     current_stats,

#                     scenario_key,

#                     dip_pct,
#                 )
#             )


#             current = (
#                 summarize_current(
#                     current_stats
#                 )
#             )


#             scenario = (
#                 summarize_scenario(
#                     scen_stats
#                 )
#             )


#             current_rr = (
#                 current[
#                     "Current Run Rate"
#                 ]
#             )


#             scenario_rr = (
#                 scenario[
#                     "Scenario Run Rate"
#                 ]
#             )


#             if current_rr > 0:

#                 rr_change = (

#                     scenario_rr
#                     /
#                     current_rr

#                     -

#                     1.0
#                 )

#             else:

#                 rr_change = np.nan


#             rows.append(
#                 {

#                     "Vertical":
#                         vertical,

#                     "Sales":
#                         (
#                             "Gross Sales"

#                             if mode == "GS"

#                             else
#                             "Net Sales"
#                         ),

#                     "FY Target":
#                         current[
#                             "FY Target"
#                         ],

#                     "YTD Achievement":
#                         current[
#                             "YTD Achievement"
#                         ],

#                     "Target Achieved %":
#                         current[
#                             "Target Achieved %"
#                         ],

#                     "Current Run Rate":
#                         current_rr,

#                     "Scenario Run Rate":
#                         scenario_rr,

#                     "Run Rate Change %":
#                         rr_change,

#                     "Current March Projection %":
#                         current[
#                             "Current March Projection %"
#                         ],

#                     "Scenario Milestone %":
#                         scenario[
#                             "Scenario Milestone %"
#                         ],

#                     "Scenario March Projection %":
#                         scenario[
#                             "Scenario March Projection %"
#                         ],
#                 }
#             )


#     return pd.DataFrame(
#         rows
#     )


# # ================================================================
# # EQUITY / DEBT / LIQUID BREAKDOWN
# # ================================================================

# def build_asset_breakdown(
#     frames,
#     mode: str,
#     scenario_key: str,
#     dip_pct: float,
# ) -> pd.DataFrame:


#     rows = []


#     for vertical in VERTICAL_SHEETS:


#         current = (
#             current_asset_stats(

#                 frames[
#                     vertical
#                 ],

#                 mode,
#             )
#         )


#         scen = (
#             scenario_stats(

#                 current,

#                 scenario_key,

#                 dip_pct,
#             )
#         )


#         for asset in ASSETS:


#             row = (
#                 scen.loc[
#                     asset
#                 ]
#             )


#             rows.append(
#                 {

#                     "Vertical":
#                         vertical,

#                     "Asset":
#                         asset,

#                     "FY Target":
#                         row[
#                             "FY Target"
#                         ],

#                     "YTD Achievement":
#                         row[
#                             "YTD Achievement"
#                         ],

#                     "Target Achieved %":
#                         row[
#                             "Target Achieved %"
#                         ],

#                     "Current Run Rate":
#                         row[
#                             "Current Run Rate"
#                         ],

#                     "Scenario Run Rate":
#                         row[
#                             "Scenario Run Rate"
#                         ],

#                     "Run Rate Change %":
#                         row[
#                             "Run Rate Change %"
#                         ],

#                     "Current March Projection %":
#                         row[
#                             "Current March Projection %"
#                         ],

#                     "Scenario Milestone %":
#                         row[
#                             "Scenario Milestone %"
#                         ],

#                     "Scenario March Projection %":
#                         row[
#                             "Scenario March Projection %"
#                         ],

#                     "Feb-Mar Run Rate":
#                         row[
#                             "Feb-Mar Run Rate"
#                         ],
#                 }
#             )


#     return pd.DataFrame(
#         rows
#     )


# # ================================================================
# # TABLE FORMATTING
# # ================================================================

# def format_table(
#     df: pd.DataFrame
# ):

#     formatters = {}


#     for column in df.columns:


#         if (
#             "%"
#             in column

#             and

#             "Δ pp"
#             not in column
#         ):

#             formatters[
#                 column
#             ] = (
#                 lambda value:
#                     "—"

#                     if pd.isna(
#                         value
#                     )

#                     else
#                     f"{value * 100:.1f}%"
#             )


#         elif (
#             "Δ pp"
#             in column
#         ):

#             formatters[
#                 column
#             ] = (
#                 lambda value:
#                     "—"

#                     if pd.isna(
#                         value
#                     )

#                     else
#                     f"{value:+.1f} pp"
#             )


#         elif any(

#             keyword
#             in column

#             for keyword in [

#                 "Target",
#                 "Achievement",
#                 "Run Rate",
#                 "Projection",
#             ]
#         ):

#             formatters[
#                 column
#             ] = (
#                 lambda value:
#                     "—"

#                     if pd.isna(
#                         value
#                     )

#                     else
#                     f"{value:,.0f}"
#             )


#     return (
#         df
#         .style
#         .format(
#             formatters
#         )
#     )


# # ================================================================
# # EXPORT
# # ================================================================

# def make_export_excel(
#     current,
#     comparison,
#     vertical,
#     gs_breakdown,
#     ns_breakdown,
#     scenario_key,
#     dip_pct,
# ):


#     output = io.BytesIO()


#     scenario_info = pd.DataFrame(
#         {

#             "Field": [

#                 "Scenario",

#                 "Description",

#                 "Milestone",

#                 "Scenario 3 Feb-Mar Dip",
#             ],

#             "Value": [

#                 (
#                     f"{SCENARIOS[scenario_key]['label']} "
#                     f"— "
#                     f"{SCENARIOS[scenario_key]['name']}"
#                 ),

#                 SCENARIOS[
#                     scenario_key
#                 ][
#                     "description"
#                 ],

#                 SCENARIOS[
#                     scenario_key
#                 ][
#                     "milestone"
#                 ],

#                 (
#                     f"{dip_pct * 100:.0f}%"

#                     if scenario_key
#                     ==
#                     "scenario_3"

#                     else
#                     "Not applicable"
#                 ),
#             ],
#         }
#     )


#     with pd.ExcelWriter(
#         output,
#         engine="openpyxl",
#     ) as writer:


#         scenario_info.to_excel(
#             writer,
#             sheet_name="Scenario Guide",
#             index=False,
#         )


#         current.to_excel(
#             writer,
#             sheet_name="Current Baseline",
#             index=False,
#         )


#         comparison.to_excel(
#             writer,
#             sheet_name="Current vs Scenario",
#             index=False,
#         )


#         vertical.to_excel(
#             writer,
#             sheet_name="Retail-DHNI",
#             index=False,
#         )


#         gs_breakdown.to_excel(
#             writer,
#             sheet_name="GS Breakdown",
#             index=False,
#         )


#         ns_breakdown.to_excel(
#             writer,
#             sheet_name="NS Breakdown",
#             index=False,
#         )


#         for ws in writer.book.worksheets:


#             ws.freeze_panes = "A2"


#             if (
#                 ws.max_row
#                 and
#                 ws.max_column
#             ):

#                 ws.auto_filter.ref = (
#                     ws.dimensions
#                 )


#             for cell in ws[1]:

#                 cell.font = (
#                     cell.font.copy(
#                         bold=True
#                     )
#                 )


#             for cells in ws.columns:


#                 letter = (
#                     cells[
#                         0
#                     ].column_letter
#                 )


#                 width = max(

#                     (

#                         len(
#                             str(
#                                 cell.value
#                                 or
#                                 ""
#                             )
#                         )

#                         for cell
#                         in cells[:120]
#                     ),

#                     default=10,
#                 )


#                 ws.column_dimensions[
#                     letter
#                 ].width = min(

#                     max(
#                         width + 2,
#                         12,
#                     ),

#                     38,
#                 )


#     output.seek(
#         0
#     )


#     return (
#         output.getvalue()
#     )


# # ================================================================
# # UPLOAD SCREEN
# # ================================================================

# if (
#     "dashboard_frames"
#     not in st.session_state
# ):


#     st.title(
#         "Sales Performance Scenario Planner"
#     )


#     st.caption(
#         "Upload the workbook once. "
#         "After validation, only the "
#         "management dashboard is shown."
#     )


#     uploaded_file = st.file_uploader(

#         "Upload Excel workbook",

#         type=[
#             "xlsx",
#             "xlsm",
#         ],

#         help=(
#             "Required sheets: "
#             "RM Retail Sales and RM DHNI."
#         ),
#     )


#     if uploaded_file is not None:


#         try:


#             with st.spinner(
#                 "Loading dashboard…"
#             ):


#                 st.session_state[
#                     "dashboard_frames"
#                 ] = (
#                     load_workbook(
#                         uploaded_file
#                     )
#                 )


#                 st.session_state[
#                     "selected_scenario"
#                 ] = "scenario_1"


#             rerun_app()


#         except Exception as exc:


#             st.error(
#                 f"Could not load this workbook: "
#                 f"{exc}"
#             )


#     st.stop()


# # ================================================================
# # DASHBOARD DATA
# # ================================================================

# frames: Dict[
#     str,
#     pd.DataFrame,
# ] = (
#     st.session_state[
#         "dashboard_frames"
#     ]
# )


# scenario_keys = list(
#     SCENARIOS
# )


# saved_scenario = (
#     st.session_state.get(
#         "selected_scenario",
#         "scenario_1",
#     )
# )


# if (
#     saved_scenario
#     not in scenario_keys
# ):

#     saved_scenario = (
#         "scenario_1"
#     )


# # ================================================================
# # LEFT SIDEBAR
# # SCENARIOS ARE ONLY HERE
# # ================================================================

# with st.sidebar:


#     st.title(
#         "Scenarios"
#     )


#     st.caption(
#         "All scenarios stay here. "
#         "The baseline never moves from "
#         "the top of the main dashboard."
#     )


#     selected_scenario = (
#         st.radio(

#             "Scenario",

#             options=
#                 scenario_keys,

#             index=
#                 scenario_keys.index(
#                     saved_scenario
#                 ),

#             format_func=
#                 lambda key:
#                     (
#                         f"{SCENARIOS[key]['label']} "
#                         f"· "
#                         f"{SCENARIOS[key]['name']}"
#                     ),

#             label_visibility=
#                 "collapsed",
#         )
#     )


#     st.session_state[
#         "selected_scenario"
#     ] = selected_scenario


#     st.divider()


#     st.markdown(
#         f"### "
#         f"{SCENARIOS[selected_scenario]['label']}"
#     )


#     st.markdown(
#         f"**"
#         f"{SCENARIOS[selected_scenario]['name']}"
#         f"**"
#     )


#     st.caption(
#         SCENARIOS[
#             selected_scenario
#         ][
#             "description"
#         ]
#     )


#     # Only Scenario 3 needs a dip control

#     if (
#         selected_scenario
#         ==
#         "scenario_3"
#     ):


#         dip_value = st.slider(

#             "Feb-Mar run-rate dip",

#             min_value=0,

#             max_value=60,

#             value=20,

#             step=5,

#             help=(
#                 "After reaching 100% "
#                 "in January, reduce the "
#                 "February and March monthly "
#                 "pace by this percentage."
#             ),
#         )


#         st.caption(

#             f"Feb-Mar pace = "
#             f"{100 - dip_value}% "
#             f"of the Jan-required pace."
#         )


#     else:

#         dip_value = 20


#     st.divider()


#     if st.button(

#         "Use another workbook",

#         use_container_width=True,
#     ):


#         st.session_state.pop(
#             "dashboard_frames",
#             None,
#         )


#         st.session_state.pop(
#             "selected_scenario",
#             None,
#         )


#         rerun_app()


# # ================================================================
# # RUN CALCULATIONS
# # ================================================================

# dip_pct = (
#     dip_value
#     /
#     100.0
# )


# all_frame = (
#     combine_frames(
#         frames
#     )
# )


# (
#     current_overview,
#     overall_mode_stats,
# ) = (
#     build_current_overview(
#         all_frame
#     )
# )


# comparison, _ = (
#     build_comparison(

#         overall_mode_stats,

#         selected_scenario,

#         dip_pct,
#     )
# )


# vertical_summary = (
#     build_vertical_summary(

#         frames,

#         selected_scenario,

#         dip_pct,
#     )
# )


# gs_breakdown = (
#     build_asset_breakdown(

#         frames,

#         "GS",

#         selected_scenario,

#         dip_pct,
#     )
# )


# ns_breakdown = (
#     build_asset_breakdown(

#         frames,

#         "NS",

#         selected_scenario,

#         dip_pct,
#     )
# )


# # ================================================================
# # COMPACT MAIN HEADER
# # ================================================================

# st.title(
#     "Sales Performance Scenario Planner"
# )


# st.markdown(
#     """
#     <div style="
#         color:#cbd5e1;
#         font-size:0.95rem;
#         margin-bottom:0.75rem;
#     ">
#         Baseline and comparison are intentionally kept together at the top
#         so both are visible in one management view.
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# # ================================================================
# # CURRENT BASELINE
# # ================================================================

# st.markdown(
#     "### Current Baseline"
# )


# current_lookup = (
#     current_overview
#     .set_index(
#         "Sales"
#     )
# )


# gs = (
#     current_lookup
#     .loc[
#         "Gross Sales"
#     ]
# )


# ns = (
#     current_lookup
#     .loc[
#         "Net Sales"
#     ]
# )


# # Only 4 compact baseline cards
# # so the scenario comparison fits below.

# b1, b2, b3, b4 = (
#     st.columns(4)
# )


# b1.metric(

#     "GS Current Run Rate",

#     fmt_amount(
#         gs[
#             "Current Run Rate / Month"
#         ]
#     ),

#     help=(
#         "Average monthly Gross Sales "
#         "based on Apr-Jun actuals."
#     ),
# )


# b2.metric(

#     "NS Current Run Rate",

#     fmt_amount(
#         ns[
#             "Current Run Rate / Month"
#         ]
#     ),

#     help=(
#         "Average monthly Net Sales "
#         "based on Apr-Jun actuals."
#     ),
# )


# b3.metric(

#     "GS Target Achieved",

#     fmt_pct(
#         gs[
#             "Target Achieved %"
#         ]
#     ),

#     help=(
#         "Gross Sales YTD achievement "
#         "divided by YTD June target."
#     ),
# )


# b4.metric(

#     "NS Target Achieved",

#     fmt_pct(
#         ns[
#             "Target Achieved %"
#         ]
#     ),

#     help=(
#         "Net Sales YTD achievement "
#         "divided by YTD June target."
#     ),
# )


# # ================================================================
# # CURRENT VS SCENARIO
# # IMMEDIATELY BELOW BASELINE
# # ================================================================

# st.markdown(
#     "### Current vs Selected Scenario"
# )


# st.info(
#     f"{SCENARIOS[selected_scenario]['label']} — "
#     f"{SCENARIOS[selected_scenario]['name']}\n\n"
#     f"{SCENARIOS[selected_scenario]['description']}"
# )


# cmp_lookup = (
#     comparison
#     .set_index(
#         "Sales"
#     )
# )


# gs_cmp = (
#     cmp_lookup
#     .loc[
#         "Gross Sales"
#     ]
# )


# ns_cmp = (
#     cmp_lookup
#     .loc[
#         "Net Sales"
#     ]
# )


# c1, c2, c3, c4 = (
#     st.columns(4)
# )


# # GS Scenario Run Rate

# c1.metric(

#     "GS Scenario Run Rate",

#     fmt_amount(
#         gs_cmp[
#             "Scenario Run Rate"
#         ]
#     ),

#     delta=
#         fmt_delta(
#             gs_cmp[
#                 "Run Rate Change %"
#             ]
#         ),
# )


# # NS Scenario Run Rate

# c2.metric(

#     "NS Scenario Run Rate",

#     fmt_amount(
#         ns_cmp[
#             "Scenario Run Rate"
#         ]
#     ),

#     delta=
#         fmt_delta(
#             ns_cmp[
#                 "Run Rate Change %"
#             ]
#         ),
# )


# # GS Scenario Achievement

# c3.metric(

#     (
#         f"GS "
#         f"{SCENARIOS[selected_scenario]['milestone']} "
#         f"Achievement"
#     ),

#     fmt_pct(
#         gs_cmp[
#             "Scenario Milestone %"
#         ]
#     ),

#     delta=
#         (
#             (
#                 f"March projection "
#                 f"{fmt_pct(gs_cmp['Scenario March Projection %'])}"
#             )

#             if (
#                 SCENARIOS[
#                     selected_scenario
#                 ][
#                     "milestone"
#                 ]
#                 ==
#                 "January"
#             )

#             else
#             None
#         ),
# )


# # NS Scenario Achievement

# c4.metric(

#     (
#         f"NS "
#         f"{SCENARIOS[selected_scenario]['milestone']} "
#         f"Achievement"
#     ),

#     fmt_pct(
#         ns_cmp[
#             "Scenario Milestone %"
#         ]
#     ),

#     delta=
#         (
#             (
#                 f"March projection "
#                 f"{fmt_pct(ns_cmp['Scenario March Projection %'])}"
#             )

#             if (
#                 SCENARIOS[
#                     selected_scenario
#                 ][
#                     "milestone"
#                 ]
#                 ==
#                 "January"
#             )

#             else
#             None
#         ),
# )


# # ================================================================
# # DETAILED TOP TABLES
# # COLLAPSED SO THEY DO NOT PUSH COMPARISON DOWN
# # ================================================================

# with st.expander(

#     "Detailed baseline and comparison numbers",

#     expanded=False,
# ):


#     st.markdown(
#         "**Current baseline**"
#     )


#     st.dataframe(

#         format_table(
#             current_overview
#         ),

#         use_container_width=True,

#         hide_index=True,

#         height=150,
#     )


#     st.markdown(
#         "**Current vs scenario**"
#     )


#     st.dataframe(

#         format_table(
#             comparison
#         ),

#         use_container_width=True,

#         hide_index=True,

#         height=150,
#     )


# # ================================================================
# # RETAIL VS DHNI
# # ================================================================

# st.divider()


# st.subheader(
#     "Retail vs DHNI"
# )


# st.caption(
#     "The same GS/NS metrics split by vertical, "
#     "so you can see whether the scenario stretch "
#     "is coming from Retail or DHNI."
# )


# st.dataframe(

#     format_table(
#         vertical_summary
#     ),

#     use_container_width=True,

#     hide_index=True,

#     height=260,
# )


# # ================================================================
# # EQUITY / DEBT / LIQUID
# # ================================================================

# st.divider()


# st.subheader(
#     "Equity / Debt / Liquid Breakdown"
# )


# st.caption(
#     "Inside Retail and DHNI, compare the "
#     "current and scenario run rates for "
#     "Equity, Debt and Liquid separately."
# )


# gs_tab, ns_tab = (
#     st.tabs(
#         [
#             "Gross Sales",
#             "Net Sales",
#         ]
#     )
# )


# # ================================================================
# # GS ASSET BREAKDOWN
# # ================================================================

# with gs_tab:


#     display = (
#         gs_breakdown.copy()
#     )


#     if (
#         selected_scenario
#         !=
#         "scenario_3"
#     ):

#         display = (
#             display.drop(
#                 columns=[
#                     "Feb-Mar Run Rate"
#                 ]
#             )
#         )


#     st.dataframe(

#         format_table(
#             display
#         ),

#         use_container_width=True,

#         hide_index=True,

#         height=360,
#     )


# # ================================================================
# # NS ASSET BREAKDOWN
# # ================================================================

# with ns_tab:


#     display = (
#         ns_breakdown.copy()
#     )


#     if (
#         selected_scenario
#         !=
#         "scenario_3"
#     ):

#         display = (
#             display.drop(
#                 columns=[
#                     "Feb-Mar Run Rate"
#                 ]
#             )
#         )


#     st.dataframe(

#         format_table(
#             display
#         ),

#         use_container_width=True,

#         hide_index=True,

#         height=360,
#     )


# # ================================================================
# # EXPORT
# # ================================================================

# export_bytes = (
#     make_export_excel(

#         current_overview,

#         comparison,

#         vertical_summary,

#         gs_breakdown,

#         ns_breakdown,

#         selected_scenario,

#         dip_pct,
#     )
# )


# st.download_button(

#     "Download selected scenario analysis",

#     data=export_bytes,

#     file_name=
#         f"{selected_scenario}_analysis.xlsx",

#     mime=
#         "application/"
#         "vnd.openxmlformats-officedocument."
#         "spreadsheetml.sheet",

#     use_container_width=True,
# )





"""
=============================================================================
 SALES PERFORMANCE, SCENARIO PLANNING & REVENUE IMPACT DASHBOARD
=============================================================================
 Senior-management decision-support application for asset-management sales.

 Run with:
     streamlit run app.py

 Stack: Python | Streamlit | Pandas | NumPy | OpenPyXL
=============================================================================
"""

from __future__ import annotations

import inspect
import io
from html import escape
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import streamlit as st
from openpyxl import load_workbook as openpyxl_load_workbook

# =============================================================================
# 1. APPLICATION CONFIGURATION  (management assumptions only - no business data)
# =============================================================================

APP_TITLE = "Sales Performance Scenario Planner"
APP_SUBTITLE = (
    "Current state → selected management scenario → required future state → revenue impact"
)

# --- Financial-year timeline -------------------------------------------------
MONTHS_COMPLETED = 3        # April, May, June are complete
MONTHS_REMAINING = 9        # July .. March
MONTHS_JUL_JAN = 7          # July .. January
MONTHS_FEB_MAR = 2          # February, March

FUTURE_MONTHS: List[str] = [
    "July", "August", "September", "October",
    "November", "December", "January", "February", "March",
]
MOMENTUM_MONTHS = FUTURE_MONTHS[:MONTHS_JUL_JAN]      # July .. January
LEAKAGE_MONTHS = FUTURE_MONTHS[MONTHS_JUL_JAN:]       # February, March
MONTH_DATES = pd.date_range("2026-07-01", periods=len(FUTURE_MONTHS), freq="MS")

# --- Revenue assumptions (basis points) --------------------------------------
REVENUE_BPS: Dict[str, float] = {"Equity": 60.0, "Debt": 20.0, "Liquid": 10.0}
REVENUE_RATE: Dict[str, float] = {k: v / 10000.0 for k, v in REVENUE_BPS.items()}

ASSETS: List[str] = ["Equity", "Debt", "Liquid"]
SALES_TYPES: List[str] = ["GS", "NS"]
SALES_LABEL: Dict[str, str] = {"GS": "Gross Sales", "NS": "Net Sales"}
VERTICALS: List[str] = ["Retail", "DHNI"]

# --- Scenario assumptions -----------------------------------------------------
S1_RUNRATE_UPLIFT = 0.20            # +20% on current run rate
S2_EQUITY_TARGET = 1.00             # 100% of Equity FY target by January
S2_OVERALL_TARGET = 0.75            # 75% of overall FY target by January
S3_TARGET = 1.00                    # 100% of FY target by January
S3_DEFAULT_DIP = 0.20               # default Feb-Mar run-rate dip
S4_TARGET = 1.20                    # 120% of FY target by March
S5_EQUITY_TARGET = 1.20             # 120% Equity by March
S5_OVERALL_TARGET = 1.00            # 100% overall by March
S6_SEGMENT_TARGETS: Dict[str, float] = {
    "Digital": 1.40,
    "Retail B30": 1.25,
    "Others": 1.15,
}
S7_DEFAULT_JAN_TARGET = 1.00        # January milestone = 100% of FY target
S7_DEFAULT_MAR_TARGET = 1.00        # March outcome = 100% of FY target
S7_DEFAULT_LEAKAGE = 0.20           # Feb-Mar AUM leakage / run-rate pressure

SEGMENT_ORDER: List[str] = ["Digital", "Retail B30", "Others"]

# --- Scenario navigator definitions -------------------------------------------
SCENARIOS: Dict[int, Dict[str, str]] = {
    1: {
        "label": "Scenario 1 · +20% Run-Rate Push",
        "name": "+20% Run-Rate Push",
        "kind": "runrate",
        "explanation": (
            "Increase the current Apr-Jun monthly run rate by 20% from July onward "
            "and measure the resulting March achievement."
        ),
        "milestone": "March 2027 · run rate lifted 20% for the remaining 9 months",
    },
    2: {
        "label": "Scenario 2 · 75% Overall by Jan + 100% Equity",
        "name": "75% Overall by January + 100% Equity",
        "kind": "jan_target",
        "explanation": (
            "Reach 100% of the Equity FY target and 75% of the overall FY target by January. "
            "The residual requirement is allocated to Debt and Liquid in FY-target proportion."
        ),
        "milestone": "January 2027 · Equity 100% of FY target, portfolio 75% of FY target",
    },
    3: {
        "label": "Scenario 3 · 100% by Jan, Then Feb-Mar Dip",
        "name": "100% by January, then Feb-Mar dip",
        "kind": "jan_target",
        "explanation": (
            "Reach 100% of the FY target by January, followed by a configurable "
            "February-March run-rate decline."
        ),
        "milestone": "January 2027 · 100% of FY target, then a reduced Feb-Mar run rate",
    },
    4: {
        "label": "Scenario 4 · 120% by March",
        "name": "120% by March",
        "kind": "march_target",
        "explanation": (
            "Determine the monthly run rate required to finish March at 120% of the FY target."
        ),
        "milestone": "March 2027 · 120% of FY target",
    },
    5: {
        "label": "Scenario 5 · 120% Equity + 100% Overall",
        "name": "120% Equity + 100% Overall by March",
        "kind": "march_target",
        "explanation": (
            "Reach 120% of the Equity FY target and 100% of the overall FY target by March, "
            "with Debt and Liquid balancing the remaining requirement."
        ),
        "milestone": "March 2027 · Equity 120% of FY target, portfolio 100% of FY target",
    },
    6: {
        "label": "Scenario 6 · Digital 140% + B30 125% + Others 115%",
        "name": "Digital 140% + Retail B30 125% + Others 115%",
        "kind": "march_target",
        "explanation": (
            "Model differentiated performance where Digital achieves 140%, Retail B30 achieves "
            "125% and Others achieve 115% of their respective FY targets."
        ),
        "milestone": "March 2027 · differentiated achievement by business segment",
    },
    7: {
        "label": "Scenario 7 · Momentum Build-Up to March 2027",
        "name": "Momentum Build-Up to March 2027",
        "kind": "momentum",
        "explanation": (
            "Build progressive month-on-month momentum from July 2026 to reach the January 2027 "
            "milestone, create sufficient buffer to absorb Feb-Mar AUM leakage, and protect the "
            "March 2027 target."
        ),
        "milestone": "January 2027 milestone → Feb-Mar leakage absorbed → March 2027 target held",
    },
}
SCENARIO_ORDER: List[int] = [1, 2, 3, 4, 5, 6, 7]

# --- Workbook contract --------------------------------------------------------
SHEET_ALIASES: Dict[str, List[str]] = {
    "Retail": ["RM Retail Sales", "RM Retail", "Retail Sales"],
    "DHNI": ["RM DHNI", "DHNI", "RM D-HNI"],
}

# Presentation/dashboard sheet. It is deliberately NOT included in
# SHEET_ALIASES because it is not an employee-level calculation sheet.
FINAL_SHEET_ALIASES: List[str] = ["FINAL", "Final", "Final Dashboard"]

COLUMN_SPEC: Dict[Tuple[str, str], Dict[str, List[str]]] = {
    ("GS", "Equity"): {
        "fy": ["FY 26 TGT EQ"],
        "ytd_tgt": ["YTD June EQ TGT"],
        "ach": ["Equity GS Ach YTD June"],
    },
    ("GS", "Debt"): {
        "fy": ["FY 26 TGT DT"],
        "ytd_tgt": ["YTD June DT TGT"],
        "ach": ["Debt GS Ach"],
    },
    ("GS", "Liquid"): {
        "fy": ["FY 26 TGT LIQ"],
        "ytd_tgt": ["YTD June LIQ TGT"],
        "ach": ["Liquid GS Ach"],
    },
    ("NS", "Equity"): {
        "fy": ["FY 26 TGT EQ NS"],
        "ytd_tgt": ["YTD June EQ NS TGT"],
        "ach": ["Equity NS Ach YTD June"],
    },
    ("NS", "Debt"): {
        "fy": ["FY 26 TGT DT NS"],
        "ytd_tgt": ["YTD June DT NS TGT"],
        "ach": ["Debt NS Ach"],
    },
    ("NS", "Liquid"): {
        "fy": ["FY 26 TGT LIQ NS"],
        "ytd_tgt": ["YTD June LIQ NS TGT"],
        "ach": ["Liquid NS Ach"],
    },
}

META_ALIASES: Dict[str, List[str]] = {
    "Employee Name": ["Employee Name", "Emp Name", "Name"],
    "Emp Code": ["Emp Code", "Employee Code"],
    "ADID": ["ADID", "AD ID"],
    "Status": ["Status", "Employee Status"],
    "Type": ["Type", "Employment Type", "Functional Designation"],
    "ZONE": ["ZONE", "Zone"],
    "REGION": ["REGION", "Region"],
    "EM City": ["EM City", "City", "Location"],
    "MKT TYPE": ["MKT TYPE", "Market Type", "Mkt Type"],
}
META_FIELDS: List[str] = list(META_ALIASES.keys())

# -----------------------------------------------------------------------------
# SEGMENT CLASSIFICATION CONFIGURATION (Scenario 6)
# Edit this block to change how business segments are identified. The scenario
# calculation engine reads the resulting mapping and never needs to change.
# -----------------------------------------------------------------------------
SEGMENT_RULES: Dict[str, Dict[str, Any]] = {
    "Digital": {
        "search_columns": ["MKT TYPE", "Type", "REGION", "ZONE", "EM City", "Status"],
        "keywords": ["digital", "online", "d2c", "e-com", "ecom", "virtual", "vrm",
                     "inside sales", "web"],
    },
    "Retail B30": {
        "search_columns": ["MKT TYPE", "REGION", "Type"],
        "keywords": ["b30"],
    },
}
FALLBACK_SEGMENT = "Others"


# =============================================================================
# 2. GENERIC HELPERS
# =============================================================================

class WorkbookError(Exception):
    """Raised when the uploaded workbook does not satisfy the data contract."""


def normalize_column_name(column: Any) -> str:
    """Collapse non-breaking spaces, repeated spaces and stray padding."""
    return " ".join(str(column).replace("\u00a0", " ").strip().split())


def _norm_key(column: Any) -> str:
    return normalize_column_name(column).casefold()


def _squash_key(column: Any) -> str:
    return "".join(ch for ch in _norm_key(column) if ch.isalnum())


def normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the frame with normalised column labels."""
    out = frame.copy()
    out.columns = [normalize_column_name(c) for c in out.columns]
    return out


def clean_numeric(series: Optional[pd.Series]) -> pd.Series:
    """Coerce a column to numeric, tolerating text-formatted numbers."""
    if series is None:
        return pd.Series(dtype="float64")
    if series.dtype == object:
        series = (
            series.astype(str)
            .str.replace("\u00a0", " ", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
            .replace({"": np.nan, "-": np.nan, "nan": np.nan, "NA": np.nan, "N/A": np.nan})
        )
    return pd.to_numeric(series, errors="coerce")


def as_text(series: pd.Series) -> pd.Series:
    """Coerce any column to clean text, mapping every missing marker to ''."""
    filled = series.where(series.notna(), "")
    return (
        filled.astype(str)
        .str.replace("\u00a0", " ", regex=False)
        .str.strip()
        .replace({"nan": "", "NaN": "", "NaT": "", "None": "", "<NA>": ""})
    )


def text_column(frame: pd.DataFrame, column: str) -> pd.Series:
    """Safe accessor for a metadata column that may be absent."""
    if column not in frame.columns:
        return pd.Series([""] * len(frame), index=frame.index, dtype=object)
    return as_text(frame[column])


def safe_div(numerator: Optional[float], denominator: Optional[float]) -> Optional[float]:
    """Division that never raises and never returns inf/nan."""
    try:
        if numerator is None or denominator is None:
            return None
        n = float(numerator)
        d = float(denominator)
        if not np.isfinite(n) or not np.isfinite(d) or abs(d) < 1e-12:
            return None
        result = n / d
        return result if np.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def _num(value: Any) -> Optional[float]:
    """Normalise a possibly-missing numeric to float or None."""
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if np.isfinite(f) else None


def _z(value: Any) -> float:
    """Numeric value with missing treated as zero (for summation)."""
    v = _num(value)
    return 0.0 if v is None else v


def _ssum(series: pd.Series) -> Optional[float]:
    """Sum that returns None when every entry is missing."""
    total = series.sum(min_count=1)
    return _num(total)


# --- Display formatting -------------------------------------------------------

NA_TEXT = "N/A"


def fmt_cr(value: Any, decimals: int = 0) -> str:
    v = _num(value)
    if v is None:
        return NA_TEXT
    return f"₹ {v:,.{decimals}f} Cr"


def fmt_cr_signed(value: Any, decimals: int = 0) -> str:
    v = _num(value)
    if v is None:
        return NA_TEXT
    return f"₹ {v:+,.{decimals}f} Cr"


def fmt_pct(value: Any, decimals: int = 1) -> str:
    v = _num(value)
    if v is None:
        return NA_TEXT
    return f"{v * 100:,.{decimals}f}%"


def fmt_pct_signed(value: Any, decimals: int = 1) -> str:
    v = _num(value)
    if v is None:
        return NA_TEXT
    return f"{v * 100:+,.{decimals}f}%"


def fmt_pts(value: Any, decimals: int = 1) -> str:
    """Percentage-point delta, e.g. +18.4 pts."""
    v = _num(value)
    if v is None:
        return NA_TEXT
    return f"{v * 100:+,.{decimals}f} pts"


def fmt_num(value: Any, decimals: int = 0) -> str:
    v = _num(value)
    if v is None:
        return NA_TEXT
    return f"{v:,.{decimals}f}"


FORMATTERS = {
    "cr": fmt_cr,
    "cr1": lambda v: fmt_cr(v, 1),
    "cr_signed": fmt_cr_signed,
    "cr1_signed": lambda v: fmt_cr_signed(v, 1),
    "pct": fmt_pct,
    "pct_signed": fmt_pct_signed,
    "pts": fmt_pts,
    "num": fmt_num,
    "txt": lambda v: NA_TEXT if v is None or (isinstance(v, float) and not np.isfinite(v)) else str(v),
}


def format_table(frame: pd.DataFrame, formats: Dict[str, str]) -> pd.DataFrame:
    """Return a display-ready copy of a numeric frame using the given formats."""
    out = pd.DataFrame(index=frame.index)
    for column in frame.columns:
        kind = formats.get(column, "txt")
        formatter = FORMATTERS.get(kind, FORMATTERS["txt"])
        out[column] = [formatter(v) for v in frame[column]]
    return out


# =============================================================================
# 3. WORKBOOK LOADING, VALIDATION & CLEANING
# =============================================================================

def _build_column_index(frame: pd.DataFrame) -> Dict[str, int]:
    """Map normalised column keys to positional index (first occurrence wins)."""
    index: Dict[str, int] = {}
    for position, column in enumerate(frame.columns):
        for key in (_norm_key(column), _squash_key(column)):
            if key and key not in index:
                index[key] = position
    return index


def _resolve_column(index: Dict[str, int], aliases: Sequence[str]) -> Optional[int]:
    for alias in aliases:
        for key in (_norm_key(alias), _squash_key(alias)):
            if key in index:
                return index[key]
    return None


def _expected_header_keys() -> set:
    keys = set()
    for spec in COLUMN_SPEC.values():
        for aliases in spec.values():
            for alias in aliases:
                keys.add(_norm_key(alias))
    for aliases in META_ALIASES.values():
        for alias in aliases:
            keys.add(_norm_key(alias))
    return keys


def _detect_header_row(raw: pd.DataFrame, max_scan: int = 15) -> int:
    """Find the row that actually holds the column headers."""
    expected = _expected_header_keys()
    best_row, best_score = 0, -1
    for row in range(min(max_scan, len(raw))):
        values = {_norm_key(v) for v in raw.iloc[row].tolist() if str(v).strip().lower() != "nan"}
        score = len(values & expected)
        if score > best_score:
            best_row, best_score = row, score
    return best_row if best_score >= 4 else 0


def _match_sheet(available: Sequence[str], aliases: Sequence[str]) -> Optional[str]:
    normalised = {_norm_key(s): s for s in available}
    for alias in aliases:
        key = _norm_key(alias)
        if key in normalised:
            return normalised[key]
    for alias in aliases:
        key = _norm_key(alias)
        for sheet_key, sheet in normalised.items():
            if key in sheet_key:
                return sheet
    return None


def validate_frame(frame: pd.DataFrame, index: Dict[str, int], sheet_label: str) -> List[str]:
    """Return a list of human-readable descriptions of missing required columns."""
    missing: List[str] = []
    for (sales, asset), spec in COLUMN_SPEC.items():
        for role, aliases in spec.items():
            if _resolve_column(index, aliases) is None:
                role_label = {"fy": "FY target", "ytd_tgt": "YTD June target", "ach": "YTD June achievement"}[role]
                missing.append(
                    f"{sheet_label} · {SALES_LABEL[sales]} · {asset} {role_label} "
                    f"(expected column '{aliases[0]}')"
                )
    return missing


def _extract_records(frame: pd.DataFrame, vertical: str) -> pd.DataFrame:
    """Turn one workbook sheet into a tidy per-employee record frame."""
    index = _build_column_index(frame)
    records = pd.DataFrame(index=frame.index)
    records["Vertical"] = vertical

    for field, aliases in META_ALIASES.items():
        position = _resolve_column(index, aliases)
        if position is None:
            records[field] = ""
        else:
            records[field] = as_text(frame.iloc[:, position]).to_numpy()

    for (sales, asset), spec in COLUMN_SPEC.items():
        for role, aliases in spec.items():
            position = _resolve_column(index, aliases)
            series = frame.iloc[:, position] if position is not None else None
            records[f"{sales}_{asset}_{role}"] = clean_numeric(series).to_numpy()

    return records


def _clean_records(records: pd.DataFrame) -> pd.DataFrame:
    """Drop non-employee rows while preserving legitimate negative values."""
    names = text_column(records, "Employee Name").str.casefold()
    invalid = names.isin({"", "nan", "none", "total", "grand total", "sum", "subtotal"})
    numeric_columns = [c for c in records.columns if c.split("_")[0] in SALES_TYPES]
    empty_rows = records[numeric_columns].isna().all(axis=1)
    cleaned = records.loc[~(invalid | empty_rows)].copy()
    cleaned[numeric_columns] = cleaned[numeric_columns].fillna(0.0)
    return cleaned.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_workbook(payload: bytes) -> pd.DataFrame:
    """Read, validate and clean the workbook into a single tidy record frame."""
    try:
        excel = pd.ExcelFile(io.BytesIO(payload), engine="openpyxl")
    except Exception as exc:  # pragma: no cover - defensive
        raise WorkbookError(
            "The file could not be opened as an Excel workbook. "
            "Please upload a valid .xlsx file."
        ) from exc

    available = list(excel.sheet_names)
    resolved: Dict[str, str] = {}
    for vertical, aliases in SHEET_ALIASES.items():
        sheet = _match_sheet(available, aliases)
        if sheet is not None:
            resolved[vertical] = sheet

    missing_sheets = [v for v in SHEET_ALIASES if v not in resolved]
    if missing_sheets:
        wanted = ", ".join(f"'{SHEET_ALIASES[v][0]}'" for v in missing_sheets)
        raise WorkbookError(
            f"The workbook is missing the required calculation sheet(s): {wanted}. "
            "Please upload the standard RM scorecard workbook."
        )

    frames: List[pd.DataFrame] = []
    problems: List[str] = []
    for vertical, sheet in resolved.items():
        raw = pd.read_excel(excel, sheet_name=sheet, header=None, nrows=20)
        header_row = _detect_header_row(raw)
        frame = normalize_frame(pd.read_excel(excel, sheet_name=sheet, header=header_row))
        index = _build_column_index(frame)
        problems.extend(validate_frame(frame, index, vertical))
        if not problems:
            frames.append(_extract_records(frame, vertical))

    if problems:
        raise WorkbookError(
            "The workbook is missing required columns:\n\n- " + "\n- ".join(problems[:12])
            + ("\n- …" if len(problems) > 12 else "")
        )

    records = _clean_records(pd.concat(frames, ignore_index=True))
    if records.empty:
        raise WorkbookError("No employee records were found in the calculation sheets.")
    return records



# =============================================================================
# 3A. FINAL SHEET — MANAGEMENT DASHBOARD VIEW
# =============================================================================

def _find_final_sheet_name(sheet_names: Sequence[str]) -> Optional[str]:
    """Resolve the sixth workbook sheet named FINAL."""
    return _match_sheet(sheet_names, FINAL_SHEET_ALIASES)


def _excel_rgb(color: Any) -> Optional[str]:
    """Convert an openpyxl RGB colour to a CSS hex colour when possible."""
    try:
        if color is None or color.type != "rgb" or not color.rgb:
            return None
        raw = str(color.rgb)
        rgb = raw[-6:]
        if len(rgb) == 6 and all(ch in "0123456789abcdefABCDEF" for ch in rgb):
            return f"#{rgb}"
    except Exception:
        return None
    return None


def _display_excel_value(value: Any, number_format: str = "") -> str:
    """Format Excel values for the FINAL dashboard without exposing formulas."""
    if value is None:
        return ""

    if isinstance(value, (pd.Timestamp,)):
        return value.strftime("%d-%b-%Y")

    # Date/datetime objects from openpyxl.
    if hasattr(value, "strftime") and not isinstance(value, str):
        try:
            return value.strftime("%d-%b-%Y")
        except Exception:
            pass

    if isinstance(value, (int, float, np.integer, np.floating)) and not isinstance(value, bool):
        numeric = float(value)
        if not np.isfinite(numeric):
            return ""

        fmt = str(number_format or "")
        if "%" in fmt:
            # Excel stores percentages as fractions.
            decimals = 0
            if "." in fmt.split("%")[0]:
                decimals = len(fmt.split("%")[0].split(".")[-1].replace("0", "0"))
            decimals = min(max(decimals, 0), 2)
            return f"{numeric * 100:,.{decimals}f}%"

        # Respect accounting-style parentheses when possible.
        negative_parentheses = numeric < 0 and "(" in fmt and ")" in fmt
        abs_value = abs(numeric)

        if abs(abs_value - round(abs_value)) < 1e-9:
            rendered = f"{abs_value:,.0f}"
        else:
            rendered = f"{abs_value:,.2f}".rstrip("0").rstrip(".")

        if numeric < 0:
            return f"({rendered})" if negative_parentheses else f"-{rendered}"
        return rendered

    return str(value)


@st.cache_data(show_spinner=False)
def load_final_sheet_frame(payload: bytes) -> pd.DataFrame:
    """
    Read the FINAL sheet as raw cells for a fallback / inspection table.

    The sheet intentionally has no single header row, so header=None is used.
    """
    excel = pd.ExcelFile(io.BytesIO(payload), engine="openpyxl")
    sheet = _find_final_sheet_name(excel.sheet_names)
    if sheet is None:
        raise WorkbookError(
            "The workbook does not contain the sixth sheet 'FINAL'. "
            "Please upload the workbook that contains Summary, Summary-Achievement, "
            "RM Retail Sales, RM DHNI, VRM and FINAL."
        )

    frame = pd.read_excel(excel, sheet_name=sheet, header=None)
    frame = frame.dropna(axis=0, how="all").dropna(axis=1, how="all")
    return frame.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def build_final_sheet_html(payload: bytes) -> str:
    """
    Render the Excel FINAL sheet into a scrollable HTML table.

    This keeps merged headings and the workbook's basic font/fill/alignment
    styling, while using cached formula results (data_only=True).
    """
    workbook = openpyxl_load_workbook(io.BytesIO(payload), data_only=True)
    sheet_name = _find_final_sheet_name(workbook.sheetnames)
    if sheet_name is None:
        raise WorkbookError(
            "The workbook does not contain the sixth sheet 'FINAL'. "
            "Please upload the workbook that contains the FINAL dashboard sheet."
        )

    ws = workbook[sheet_name]

    # Find the real content boundary from non-empty values rather than Excel's
    # formatted used-range, which can extend thousands of blank rows/columns.
    non_empty = [
        (cell.row, cell.column)
        for row in ws.iter_rows()
        for cell in row
        if cell.value not in (None, "")
    ]
    if not non_empty:
        return "<div class='note'>The FINAL sheet is empty.</div>"

    min_row = min(r for r, _ in non_empty)
    max_row = max(r for r, _ in non_empty)
    min_col = min(c for _, c in non_empty)
    max_col = max(c for _, c in non_empty)

    # Merged-cell lookup.
    merge_anchor: Dict[Tuple[int, int], Tuple[int, int]] = {}
    merge_covered: set = set()
    for merged in ws.merged_cells.ranges:
        # Only consider merged ranges intersecting the content boundary.
        if (
            merged.max_row < min_row or merged.min_row > max_row
            or merged.max_col < min_col or merged.min_col > max_col
        ):
            continue
        anchor = (merged.min_row, merged.min_col)
        merge_anchor[anchor] = (
            merged.max_row - merged.min_row + 1,
            merged.max_col - merged.min_col + 1,
        )
        for rr in range(merged.min_row, merged.max_row + 1):
            for cc in range(merged.min_col, merged.max_col + 1):
                if (rr, cc) != anchor:
                    merge_covered.add((rr, cc))

    html_parts = [
        """
        <div style="
            overflow-x:auto;
            overflow-y:auto;
            max-height:78vh;
            border:1px solid #334155;
            border-radius:12px;
            background:#ffffff;
            padding:4px;
        ">
        <table style="
            border-collapse:collapse;
            width:max-content;
            min-width:100%;
            font-family:Arial, sans-serif;
            font-size:12px;
            color:#0f172a;
        ">
        """
    ]

    for row_idx in range(min_row, max_row + 1):
        row_values = [
            ws.cell(row=row_idx, column=col_idx).value
            for col_idx in range(min_col, max_col + 1)
        ]

        # Keep dashboard spacing, but collapse very large blank areas to a
        # single slim spacer row.
        if all(v in (None, "") for v in row_values):
            html_parts.append(
                "<tr><td colspan='{}' style='height:8px;border:none;background:#fff;'></td></tr>"
                .format(max_col - min_col + 1)
            )
            continue

        html_parts.append("<tr>")
        for col_idx in range(min_col, max_col + 1):
            if (row_idx, col_idx) in merge_covered:
                continue

            cell = ws.cell(row=row_idx, column=col_idx)
            rowspan, colspan = merge_anchor.get((row_idx, col_idx), (1, 1))

            value = _display_excel_value(cell.value, cell.number_format)
            font_color = _excel_rgb(cell.font.color)
            fill_color = _excel_rgb(cell.fill.fgColor)

            styles = [
                "border:1px solid #d1d5db",
                "padding:5px 7px",
                "min-width:78px",
                "white-space:nowrap",
                "vertical-align:middle",
                "background:#ffffff",
            ]

            if fill_color and fill_color.lower() not in {"#000000", "#ffffff"}:
                styles.append(f"background:{fill_color}")
            if font_color:
                styles.append(f"color:{font_color}")
            if cell.font.bold:
                styles.append("font-weight:700")
            if cell.font.italic:
                styles.append("font-style:italic")

            horizontal = getattr(cell.alignment, "horizontal", None)
            if horizontal in {"center", "centerContinuous"}:
                styles.append("text-align:center")
            elif horizontal == "right":
                styles.append("text-align:right")
            else:
                styles.append("text-align:left")

            attrs = []
            if rowspan > 1:
                attrs.append(f"rowspan='{rowspan}'")
            if colspan > 1:
                attrs.append(f"colspan='{colspan}'")

            html_parts.append(
                f"<td {' '.join(attrs)} style=\"{';'.join(styles)}\">"
                f"{escape(value)}"
                "</td>"
            )
        html_parts.append("</tr>")

    html_parts.append("</table></div>")
    return "".join(html_parts)


def render_final_dashboard(payload: bytes) -> None:
    """Display the workbook's sixth FINAL sheet inside the Streamlit app."""
    st.markdown(
        "<div class='app-title'>Sales Target Achievement Dashboard</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='app-sub'>Directly read from the workbook's FINAL sheet — "
        "GS / NS achievement, AUM, run-rate estimates and vertical breakouts.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='app-rule'></div>", unsafe_allow_html=True)

    try:
        html = build_final_sheet_html(payload)
    except WorkbookError as error:
        st.error(str(error))
        return

    st.markdown(
        "<div class='note'>This view is taken from the Excel <b>FINAL</b> sheet. "
        "Use the horizontal scroll inside the dashboard to see all columns.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(html, unsafe_allow_html=True)

    with st.expander("View FINAL sheet as raw data", expanded=False):
        try:
            raw = load_final_sheet_frame(payload)
            st.dataframe(raw, use_container_width=True, hide_index=True, height=620)
        except WorkbookError as error:
            st.error(str(error))

    st.download_button(
        "Download uploaded workbook",
        data=payload,
        file_name="sales_target_dashboard_source.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False,
    )


# =============================================================================
# 4. SEGMENT IDENTIFICATION (Scenario 6)
# =============================================================================

def identify_segments(records: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Suggest a column + values that identify each configured business segment."""
    suggestions: Dict[str, Dict[str, Any]] = {}
    for segment, rule in SEGMENT_RULES.items():
        for column in rule["search_columns"]:
            if column not in records.columns:
                continue
            values = sorted({v for v in text_column(records, column) if v.strip()})
            matches = [
                v for v in values
                if any(keyword in v.casefold() for keyword in rule["keywords"])
            ]
            if matches:
                suggestions[segment] = {"column": column, "values": matches}
                break
    return suggestions


def map_business_segments(
    records: pd.DataFrame,
    mapping: Dict[str, Dict[str, Any]],
) -> pd.DataFrame:
    """Assign every record to Digital / Retail B30 / Others using the mapping."""
    out = records.copy()
    out["Segment"] = FALLBACK_SEGMENT
    # Reverse priority so that the first segment in SEGMENT_ORDER wins.
    for segment in reversed([s for s in SEGMENT_ORDER if s != FALLBACK_SEGMENT]):
        rule = mapping.get(segment)
        if not rule:
            continue
        column, values = rule.get("column"), set(rule.get("values") or [])
        if not column or column not in out.columns or not values:
            continue
        mask = text_column(out, column).isin(values)
        out.loc[mask, "Segment"] = segment
    return out


def segment_diagnostics(records: pd.DataFrame) -> Dict[str, int]:
    counts = records["Segment"].value_counts().to_dict()
    return {segment: int(counts.get(segment, 0)) for segment in SEGMENT_ORDER}


# =============================================================================
# 5. BASE GRID & CURRENT-STATE STATISTICS
# =============================================================================

def build_base_grid(records: pd.DataFrame) -> pd.DataFrame:
    """Aggregate records to the finest analytical grain used by the engine."""
    rows: List[Dict[str, Any]] = []
    grouped = records.groupby(["Vertical", "Segment"], dropna=False)
    for (vertical, segment), block in grouped:
        for sales in SALES_TYPES:
            for asset in ASSETS:
                rows.append({
                    "Vertical": vertical,
                    "Segment": segment,
                    "Sales": sales,
                    "Asset": asset,
                    "fy_target": float(block[f"{sales}_{asset}_fy"].sum()),
                    "ytd_target": float(block[f"{sales}_{asset}_ytd_tgt"].sum()),
                    "ytd_ach": float(block[f"{sales}_{asset}_ach"].sum()),
                })
    return pd.DataFrame(rows)


def filter_grid(
    grid: pd.DataFrame,
    sales: Optional[str] = None,
    asset: Optional[str] = None,
    vertical: Optional[str] = None,
    segment: Optional[str] = None,
) -> pd.DataFrame:
    mask = pd.Series(True, index=grid.index)
    if sales is not None:
        mask &= grid["Sales"] == sales
    if asset is not None:
        mask &= grid["Asset"] == asset
    if vertical is not None:
        mask &= grid["Vertical"] == vertical
    if segment is not None:
        mask &= grid["Segment"] == segment
    return grid.loc[mask]


def current_asset_stats(fy_target: float, ytd_target: float, ytd_ach: float) -> Dict[str, Any]:
    """Baseline statistics for one asset / group. Never scenario dependent."""
    fy_target = _z(fy_target)
    ytd_target = _z(ytd_target)
    ytd_ach = _z(ytd_ach)
    current_rr = ytd_ach / MONTHS_COMPLETED if MONTHS_COMPLETED else None
    current_march = ytd_ach + (current_rr or 0.0) * MONTHS_REMAINING
    return {
        "fy_target": fy_target,
        "ytd_target": ytd_target,
        "ytd_ach": ytd_ach,
        "current_rr": current_rr,
        "ytd_ach_pct": safe_div(ytd_ach, ytd_target),
        "fy_completed_pct": safe_div(ytd_ach, fy_target),
        "current_march": current_march,
        "current_march_pct": safe_div(current_march, fy_target),
    }


def summarize_current(grid: pd.DataFrame, **filters: Any) -> Dict[str, Any]:
    """Baseline statistics for an arbitrary slice of the base grid."""
    subset = filter_grid(grid, **filters)
    return current_asset_stats(
        subset["fy_target"].sum(),
        subset["ytd_target"].sum(),
        subset["ytd_ach"].sum(),
    )


# =============================================================================
# 6. SCENARIO ENGINE - SCENARIOS 1 TO 6
# =============================================================================

def _blank_cell(stats: Dict[str, Any]) -> Dict[str, Any]:
    cell = dict(stats)
    cell.update({
        "scen_rr": None, "rr_change_pct": None, "feb_mar_rr": None,
        "jan_required": None, "jan_amount": None, "jan_pct": None,
        "jan_buffer": None, "jan_buffer_pct": None,
        "march_required": None, "march_amount": None, "march_pct": None,
        "milestone_pct": None, "incremental_sales": None,
        "headroom_amt": None, "headroom_pct": None,
        "momentum_g": None, "feasible": None, "binding": None,
        "trajectory": None, "note": "",
    })
    return cell


def compute_cell(
    fy_target: float,
    ytd_target: float,
    ytd_ach: float,
    kind: str,
    multiplier: Optional[float] = None,
    uplift: Optional[float] = None,
    dip: float = 0.0,
) -> Dict[str, Any]:
    """Scenario mathematics for one asset / group (scenarios 1-6)."""
    stats = current_asset_stats(fy_target, ytd_target, ytd_ach)
    cell = _blank_cell(stats)
    ach = stats["ytd_ach"]
    current_rr = stats["current_rr"] or 0.0

    if kind == "runrate":
        scen_rr = current_rr * (1.0 + (uplift or 0.0))
        jan_amount = ach + scen_rr * MONTHS_JUL_JAN
        cell.update({
            "scen_rr": scen_rr,
            "feb_mar_rr": scen_rr,
            "jan_amount": jan_amount,
            "march_amount": ach + scen_rr * MONTHS_REMAINING,
            "milestone_pct": None,
        })

    elif kind == "jan_target":
        required = max(_z(multiplier) * stats["fy_target"], ach)
        scen_rr = max(required - ach, 0.0) / MONTHS_JUL_JAN
        jan_amount = ach + scen_rr * MONTHS_JUL_JAN
        feb_mar_rr = scen_rr * (1.0 - dip)
        cell.update({
            "scen_rr": scen_rr,
            "feb_mar_rr": feb_mar_rr,
            "jan_required": required,
            "jan_amount": jan_amount,
            "march_amount": jan_amount + feb_mar_rr * MONTHS_FEB_MAR,
            "milestone_pct": multiplier,
        })

    elif kind == "march_target":
        required = max(_z(multiplier) * stats["fy_target"], ach)
        scen_rr = max(required - ach, 0.0) / MONTHS_REMAINING
        cell.update({
            "scen_rr": scen_rr,
            "feb_mar_rr": scen_rr,
            "march_required": required,
            "jan_amount": ach + scen_rr * MONTHS_JUL_JAN,
            "march_amount": ach + scen_rr * MONTHS_REMAINING,
            "milestone_pct": multiplier,
        })

    else:  # pragma: no cover - guarded by the scenario registry
        raise ValueError(f"Unknown scenario kind: {kind}")

    return _finalise_cell(cell)


def _finalise_cell(cell: Dict[str, Any]) -> Dict[str, Any]:
    """Recompute all derived ratios from the absolute amounts in the cell."""
    fy_target = cell.get("fy_target")
    current_rr = _num(cell.get("current_rr"))
    scen_rr = _num(cell.get("scen_rr"))

    cell["ytd_ach_pct"] = safe_div(cell.get("ytd_ach"), cell.get("ytd_target"))
    cell["fy_completed_pct"] = safe_div(cell.get("ytd_ach"), fy_target)
    cell["current_march_pct"] = safe_div(cell.get("current_march"), fy_target)
    cell["jan_pct"] = safe_div(cell.get("jan_amount"), fy_target)
    cell["march_pct"] = safe_div(cell.get("march_amount"), fy_target)

    if current_rr is not None and current_rr > 0 and scen_rr is not None:
        cell["rr_change_pct"] = (scen_rr / current_rr) - 1.0
    else:
        cell["rr_change_pct"] = None

    march_amount = _num(cell.get("march_amount"))
    current_march = _num(cell.get("current_march"))
    if march_amount is not None and current_march is not None:
        cell["incremental_sales"] = march_amount - current_march

    jan_required = _num(cell.get("jan_required"))
    jan_amount = _num(cell.get("jan_amount"))
    if jan_required is not None and jan_amount is not None:
        cell["jan_buffer"] = jan_amount - jan_required
        cell["jan_buffer_pct"] = safe_div(cell["jan_buffer"], jan_required)

    march_required = _num(cell.get("march_required"))
    if march_required is not None and march_amount is not None:
        cell["headroom_amt"] = march_amount - march_required
        march_pct = cell.get("march_pct")
        required_pct = safe_div(march_required, fy_target)
        if march_pct is not None and required_pct is not None:
            cell["headroom_pct"] = march_pct - required_pct
        cell["feasible"] = cell["headroom_amt"] >= -1e-6

    if cell.get("milestone_pct") is None:
        cell["milestone_pct"] = cell.get("march_pct")
    return cell


def scenario_multipliers(grid: pd.DataFrame, scenario_id: int) -> Dict[Tuple[str, str, str], float]:
    """
    Derive the per-asset FY-target multiplier for the selected scenario.

    Key is (sales type, asset, segment); segment is '*' unless the scenario
    differentiates by business segment.
    """
    multipliers: Dict[Tuple[str, str, str], float] = {}

    if scenario_id in (1, 7):
        return multipliers

    if scenario_id == 3:
        for sales in SALES_TYPES:
            for asset in ASSETS:
                multipliers[(sales, asset, "*")] = S3_TARGET
        return multipliers

    if scenario_id == 4:
        for sales in SALES_TYPES:
            for asset in ASSETS:
                multipliers[(sales, asset, "*")] = S4_TARGET
        return multipliers

    if scenario_id == 6:
        for sales in SALES_TYPES:
            for asset in ASSETS:
                for segment in SEGMENT_ORDER:
                    multipliers[(sales, asset, segment)] = S6_SEGMENT_TARGETS.get(segment, 1.0)
        return multipliers

    # Scenarios 2 and 5 balance Debt and Liquid around a fixed Equity ambition.
    equity_mult = S2_EQUITY_TARGET if scenario_id == 2 else S5_EQUITY_TARGET
    overall_mult = S2_OVERALL_TARGET if scenario_id == 2 else S5_OVERALL_TARGET

    for sales in SALES_TYPES:
        targets = {
            asset: float(filter_grid(grid, sales=sales, asset=asset)["fy_target"].sum())
            for asset in ASSETS
        }
        total_target = sum(targets.values())
        required_overall = overall_mult * total_target
        required_equity = equity_mult * targets["Equity"]
        remaining = max(required_overall - required_equity, 0.0)
        denominator = targets["Debt"] + targets["Liquid"]
        share = safe_div(remaining, denominator)
        balance_mult = 0.0 if share is None else share
        multipliers[(sales, "Equity", "*")] = equity_mult
        multipliers[(sales, "Debt", "*")] = balance_mult
        multipliers[(sales, "Liquid", "*")] = balance_mult

    return multipliers


def _multiplier_for(
    multipliers: Dict[Tuple[str, str, str], float],
    sales: str,
    asset: str,
    segment: str,
) -> Optional[float]:
    if (sales, asset, segment) in multipliers:
        return multipliers[(sales, asset, segment)]
    return multipliers.get((sales, asset, "*"))


def apply_scenario_grid(
    grid: pd.DataFrame,
    scenario_id: int,
    params: Dict[str, Any],
    multipliers: Dict[Tuple[str, str, str], float],
) -> pd.DataFrame:
    """Evaluate scenarios 1-6 over every cell of the base grid."""
    kind = SCENARIOS[scenario_id]["kind"]
    dip = float(params.get("dip", 0.0)) if scenario_id == 3 else 0.0
    uplift = S1_RUNRATE_UPLIFT if scenario_id == 1 else None

    results: List[Dict[str, Any]] = []
    for row in grid.to_dict("records"):
        multiplier = _multiplier_for(multipliers, row["Sales"], row["Asset"], row["Segment"])
        cell = compute_cell(
            row["fy_target"], row["ytd_target"], row["ytd_ach"],
            kind=kind, multiplier=multiplier, uplift=uplift, dip=dip,
        )
        cell.update({
            "Vertical": row["Vertical"], "Segment": row["Segment"],
            "Sales": row["Sales"], "Asset": row["Asset"],
        })
        results.append(cell)
    return pd.DataFrame(results)


SUMMABLE_FIELDS = [
    "fy_target", "ytd_target", "ytd_ach", "current_rr", "current_march",
    "scen_rr", "feb_mar_rr", "jan_required", "jan_amount",
    "march_required", "march_amount",
]


def summarize_cells(subset: pd.DataFrame) -> Dict[str, Any]:
    """Aggregate scenario cells additively and rebuild every derived ratio."""
    cell: Dict[str, Any] = {}
    for field in SUMMABLE_FIELDS:
        cell[field] = _ssum(subset[field]) if field in subset.columns else None
    milestones = subset["milestone_pct"].dropna().unique() if "milestone_pct" in subset else []
    cell["milestone_pct"] = float(milestones[0]) if len(milestones) == 1 else None
    cell["note"] = ""
    cell["momentum_g"] = None
    cell["trajectory"] = None
    cell["binding"] = None
    cell["feasible"] = None
    return _finalise_cell(cell)


# --- Named scenario entry points (thin wrappers over the shared engine) -------

def _scenario_frame(grid: pd.DataFrame, scenario_id: int, params: Dict[str, Any]) -> pd.DataFrame:
    return apply_scenario_grid(grid, scenario_id, params, scenario_multipliers(grid, scenario_id))


def calculate_scenario_1(grid: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """+20% run-rate push from July onward."""
    return _scenario_frame(grid, 1, params)


def calculate_scenario_2(grid: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """100% Equity and 75% overall FY target by January."""
    return _scenario_frame(grid, 2, params)


def calculate_scenario_3(grid: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """100% of FY target by January, then a configurable Feb-Mar dip."""
    return _scenario_frame(grid, 3, params)


def calculate_scenario_4(grid: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """120% of FY target by March."""
    return _scenario_frame(grid, 4, params)


def calculate_scenario_5(grid: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """120% Equity and 100% overall FY target by March."""
    return _scenario_frame(grid, 5, params)


def calculate_scenario_6(grid: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    """Digital 140%, Retail B30 125%, Others 115% of their FY targets."""
    return _scenario_frame(grid, 6, params)


SCENARIO_FUNCTIONS = {
    1: calculate_scenario_1,
    2: calculate_scenario_2,
    3: calculate_scenario_3,
    4: calculate_scenario_4,
    5: calculate_scenario_5,
    6: calculate_scenario_6,
}


# =============================================================================
# 7. SCENARIO 7 - MOMENTUM ENGINE
# =============================================================================

def _momentum_sum(growth: float, months: int, tail_factors: Sequence[float]) -> float:
    """Sum of compounding monthly run-rate multiples, including leakage tail."""
    factor = 1.0 + growth
    build = sum(factor ** k for k in range(1, months + 1))
    tail = sum(f * factor ** months for f in tail_factors)
    return build + tail


def solve_momentum_rate(
    current_rr: float,
    required_amount: float,
    months: int = MONTHS_JUL_JAN,
    tail_factors: Sequence[float] = (),
    upper: float = 3.0,
) -> Optional[float]:
    """
    Back-solve the minimum month-on-month growth rate g such that the
    compounding trajectory delivers the required incremental amount.

    Returns 0.0 when no additional momentum is needed and None when the
    requirement cannot be met within the search bounds.
    """
    rr = _num(current_rr)
    need = _num(required_amount)
    if rr is None or need is None or rr <= 0:
        return None
    if need <= 0:
        return 0.0

    def shortfall(growth: float) -> float:
        return rr * _momentum_sum(growth, months, tail_factors) - need

    if shortfall(0.0) >= 0:
        return 0.0
    if shortfall(upper) < 0:
        return None

    low, high = 0.0, upper
    for _ in range(240):
        mid = (low + high) / 2.0
        if shortfall(mid) >= 0:
            high = mid
        else:
            low = mid
    return high


def calculate_momentum_trajectory(
    current_rr: float,
    growth: Optional[float],
    leakage: float,
    flat_rate: Optional[float] = None,
) -> List[float]:
    """Monthly run rates for July → March (momentum build, then leakage)."""
    if growth is None:
        base = _z(flat_rate)
        build = [base] * MONTHS_JUL_JAN
    else:
        rr = _z(current_rr)
        build = [rr * (1.0 + growth) ** k for k in range(1, MONTHS_JUL_JAN + 1)]
    january_rr = build[-1] if build else 0.0
    february_rr = january_rr * (1.0 - leakage)
    march_rr = february_rr * (1.0 - leakage)
    return build + [february_rr, march_rr]


def calculate_leakage_impact(january_rr: float, leakage: float) -> Dict[str, float]:
    """February and March run rates after AUM leakage / run-rate pressure."""
    february_rr = _z(january_rr) * (1.0 - leakage)
    march_rr = february_rr * (1.0 - leakage)
    return {
        "february_rr": february_rr,
        "march_rr": march_rr,
        "feb_mar_sales": february_rr + march_rr,
    }


def calculate_momentum_headroom(
    march_amount: float,
    march_required: float,
    fy_target: float,
    march_target_pct: float,
) -> Dict[str, Optional[float]]:
    """Scenario achievement versus the March ambition, in ₹ and in points."""
    headroom_amt = _z(march_amount) - _z(march_required)
    achieved_pct = safe_div(march_amount, fy_target)
    headroom_pct = None if achieved_pct is None else achieved_pct - march_target_pct
    return {"headroom_amt": headroom_amt, "headroom_pct": headroom_pct}


def calculate_scenario_7(
    fy_target: float,
    ytd_target: float,
    ytd_ach: float,
    params: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Momentum build-up model.

    Solves for the month-on-month growth rate that simultaneously satisfies the
    January milestone and, after Feb-Mar leakage, the March ambition.
    """
    jan_target_pct = float(params.get("jan_target", S7_DEFAULT_JAN_TARGET))
    mar_target_pct = float(params.get("mar_target", S7_DEFAULT_MAR_TARGET))
    leakage = float(params.get("leakage", S7_DEFAULT_LEAKAGE))

    stats = current_asset_stats(fy_target, ytd_target, ytd_ach)
    cell = _blank_cell(stats)
    ach = stats["ytd_ach"]
    current_rr = stats["current_rr"] or 0.0

    jan_required = max(jan_target_pct * stats["fy_target"], ach)
    mar_required = max(mar_target_pct * stats["fy_target"], ach)
    tail = ((1.0 - leakage), (1.0 - leakage) ** 2)

    growth_jan = solve_momentum_rate(current_rr, jan_required - ach, MONTHS_JUL_JAN)
    growth_mar = solve_momentum_rate(current_rr, mar_required - ach, MONTHS_JUL_JAN, tail)

    note = ""
    binding = None
    flat_rate = None

    if current_rr <= 0:
        # Momentum compounding is undefined on a non-positive run rate:
        # fall back to the flat run rate required to hold both milestones.
        flat_jan = max(jan_required - ach, 0.0) / MONTHS_JUL_JAN
        denominator = MONTHS_JUL_JAN + tail[0] + tail[1]
        flat_mar = max(mar_required - ach, 0.0) / denominator
        flat_rate = max(flat_jan, flat_mar)
        growth = None
        binding = "January" if flat_jan >= flat_mar else "March"
        note = (
            "Current run rate is not positive, so compounding momentum cannot be applied. "
            "The flat monthly run rate required to hold the milestones is shown instead."
        )
    elif growth_jan is None and growth_mar is None:
        growth = None
        flat_rate = max(mar_required - ach, 0.0) / (MONTHS_JUL_JAN + tail[0] + tail[1])
        binding = "March"
        note = "The requirement exceeds the momentum search range; a flat required run rate is shown."
    else:
        candidates = [g for g in (growth_jan, growth_mar) if g is not None]
        growth = max(candidates)
        binding = "March" if (growth_mar is not None and growth == growth_mar
                              and (growth_jan is None or growth_mar >= growth_jan)) else "January"

    trajectory = calculate_momentum_trajectory(current_rr, growth, leakage, flat_rate)
    build_phase = trajectory[:MONTHS_JUL_JAN]
    jan_amount = ach + sum(build_phase)
    january_rr = build_phase[-1] if build_phase else 0.0
    leak = calculate_leakage_impact(january_rr, leakage)
    march_amount = jan_amount + leak["feb_mar_sales"]

    headroom = calculate_momentum_headroom(
        march_amount, mar_required, stats["fy_target"], mar_target_pct
    )
    shortfall = max(mar_required - march_amount, 0.0)
    denominator = 1.0 + tail[0] + tail[1]
    additional_jan_rr = shortfall / denominator if denominator else None

    cell.update({
        "scen_rr": january_rr,
        "feb_mar_rr": leak["february_rr"],
        "march_rr": leak["march_rr"],
        "jan_required": jan_required,
        "jan_amount": jan_amount,
        "march_required": mar_required,
        "march_amount": march_amount,
        "milestone_pct": jan_target_pct,
        "march_target_pct": mar_target_pct,
        "momentum_g": growth,
        "flat_rate": flat_rate,
        "leakage": leakage,
        "trajectory": trajectory,
        "binding": binding,
        "note": note,
        "additional_march_sales": shortfall,
        "additional_jan_rr": additional_jan_rr,
        "avg_scen_rr": (sum(trajectory) / len(trajectory)) if trajectory else None,
    })
    cell = _finalise_cell(cell)
    cell["headroom_amt"] = headroom["headroom_amt"]
    cell["headroom_pct"] = headroom["headroom_pct"]
    cell["feasible"] = shortfall <= 1e-6
    # Momentum run rate versus the current flat run rate, measured on the
    # January exit rate (the pace the business must be running at by then).
    cell["rr_change_pct"] = (
        (january_rr / current_rr) - 1.0 if current_rr and current_rr > 0 else None
    )
    return cell


# =============================================================================
# 8. SCENARIO MODEL - ONE INTERFACE FOR EVERY VIEW
# =============================================================================

class ScenarioModel:
    """Evaluates the selected scenario for any slice of the business."""

    def __init__(self, scenario_id: int, grid: pd.DataFrame, params: Dict[str, Any]):
        self.scenario_id = scenario_id
        self.meta = SCENARIOS[scenario_id]
        self.grid = grid
        self.params = params
        self.multipliers = scenario_multipliers(grid, scenario_id)
        self._cache: Dict[Tuple, Dict[str, Any]] = {}
        if scenario_id == 7:
            self.scenario_grid = None
        else:
            self.scenario_grid = SCENARIO_FUNCTIONS[scenario_id](grid, params)

    # -- core accessor --------------------------------------------------------
    def cell(
        self,
        sales: str,
        asset: Optional[str] = None,
        vertical: Optional[str] = None,
        segment: Optional[str] = None,
    ) -> Dict[str, Any]:
        key = (sales, asset, vertical, segment)
        if key in self._cache:
            return self._cache[key]

        if self.scenario_id == 7:
            subset = filter_grid(self.grid, sales=sales, asset=asset,
                                 vertical=vertical, segment=segment)
            cell = calculate_scenario_7(
                subset["fy_target"].sum(),
                subset["ytd_target"].sum(),
                subset["ytd_ach"].sum(),
                self.params,
            )
        else:
            frame = self.scenario_grid
            mask = frame["Sales"] == sales
            if asset is not None:
                mask &= frame["Asset"] == asset
            if vertical is not None:
                mask &= frame["Vertical"] == vertical
            if segment is not None:
                mask &= frame["Segment"] == segment
            cell = summarize_cells(frame.loc[mask])

        self._cache[key] = cell
        return cell

    # -- convenience views ----------------------------------------------------
    def assets(self, sales: str, **filters: Any) -> Dict[str, Dict[str, Any]]:
        return {asset: self.cell(sales, asset=asset, **filters) for asset in ASSETS}

    def baseline(self, sales: str, **filters: Any) -> Dict[str, Any]:
        return summarize_current(self.grid, sales=sales, **filters)

    def implied_milestones(self, sales: str) -> Dict[str, Optional[float]]:
        return {
            asset: _multiplier_for(self.multipliers, sales, asset, "*")
            for asset in ASSETS
        }

    def available_segments(self) -> List[str]:
        present = set(self.grid["Segment"].unique())
        return [s for s in SEGMENT_ORDER if s in present]

    def available_verticals(self) -> List[str]:
        present = set(self.grid["Vertical"].unique())
        return [v for v in VERTICALS if v in present]


# =============================================================================
# 9. REVENUE ENGINE
# =============================================================================

def calculate_revenue(cells_by_asset: Dict[str, Dict[str, Any]], field: str) -> Dict[str, Any]:
    """Asset-class revenue from a set of scenario cells. No blended rate."""
    by_asset: Dict[str, Optional[float]] = {}
    sales_by_asset: Dict[str, Optional[float]] = {}
    total = 0.0
    for asset in ASSETS:
        amount = _num(cells_by_asset.get(asset, {}).get(field))
        sales_by_asset[asset] = amount
        revenue = None if amount is None else amount * REVENUE_RATE[asset]
        by_asset[asset] = revenue
        total += 0.0 if revenue is None else revenue
    return {"by_asset": by_asset, "sales_by_asset": sales_by_asset, "total": total}


def calculate_baseline_revenue(cells_by_asset: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Baseline revenue on the current-run-rate March projection (scenario independent)."""
    return calculate_revenue(cells_by_asset, "current_march")


def calculate_incremental_revenue(
    scenario_revenue: Dict[str, Any],
    baseline_revenue: Dict[str, Any],
) -> Dict[str, Any]:
    incremental = {
        asset: (
            None
            if scenario_revenue["by_asset"].get(asset) is None
            or baseline_revenue["by_asset"].get(asset) is None
            else scenario_revenue["by_asset"][asset] - baseline_revenue["by_asset"][asset]
        )
        for asset in ASSETS
    }
    total = scenario_revenue["total"] - baseline_revenue["total"]
    uplift = safe_div(scenario_revenue["total"], baseline_revenue["total"])
    return {
        "by_asset": incremental,
        "total": total,
        "uplift_pct": None if uplift is None else uplift - 1.0,
        "contribution": {
            asset: safe_div(scenario_revenue["by_asset"].get(asset), scenario_revenue["total"])
            for asset in ASSETS
        },
    }


def revenue_bundle(model: ScenarioModel, basis: str, **filters: Any) -> Dict[str, Any]:
    """Baseline / scenario / incremental revenue for any slice of the business."""
    cells = model.assets(basis, **filters)
    baseline = calculate_baseline_revenue(cells)
    scenario = calculate_revenue(cells, "march_amount")
    january = calculate_revenue(cells, "jan_amount")
    incremental = calculate_incremental_revenue(scenario, baseline)
    return {
        "cells": cells,
        "baseline": baseline,
        "scenario": scenario,
        "january": january,
        "incremental": incremental,
    }


# =============================================================================
# 10. TABLE BUILDERS
# =============================================================================

def build_current_overview(model: ScenarioModel) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Baseline table - identical for every scenario."""
    rows = []
    for sales in SALES_TYPES:
        base = model.baseline(sales)
        rows.append({
            "Sales": SALES_LABEL[sales],
            "FY Target": base["fy_target"],
            "YTD June Target": base["ytd_target"],
            "YTD June Achievement": base["ytd_ach"],
            "Target Achieved %": base["ytd_ach_pct"],
            "FY Target Completed %": base["fy_completed_pct"],
            "Current Run Rate": base["current_rr"],
            "Current March Projection": base["current_march"],
            "Current March Projection %": base["current_march_pct"],
        })
    formats = {
        "Sales": "txt", "FY Target": "cr", "YTD June Target": "cr",
        "YTD June Achievement": "cr", "Target Achieved %": "pct",
        "FY Target Completed %": "pct", "Current Run Rate": "cr",
        "Current March Projection": "cr", "Current March Projection %": "pct",
    }
    return pd.DataFrame(rows), formats


def summarize_scenario(model: ScenarioModel, sales: str) -> Dict[str, Any]:
    """Headline current-versus-scenario numbers for one sales basis."""
    cell = model.cell(sales)
    return {
        "Sales": SALES_LABEL[sales],
        "Current Run Rate": cell["current_rr"],
        "Scenario Run Rate": cell["scen_rr"],
        "Run Rate Change %": cell["rr_change_pct"],
        "Jan Achievement": cell["jan_amount"],
        "Jan Achievement %": cell["jan_pct"],
        "Feb-Mar Run Rate": cell["feb_mar_rr"],
        "Current March Projection %": cell["current_march_pct"],
        "Scenario March Achievement": cell["march_amount"],
        "Scenario March Achievement %": cell["march_pct"],
        "Incremental Sales": cell["incremental_sales"],
    }


def build_comparison(model: ScenarioModel) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Current versus selected scenario, for Gross Sales and Net Sales."""
    rows = [summarize_scenario(model, sales) for sales in SALES_TYPES]
    formats = {
        "Sales": "txt", "Current Run Rate": "cr", "Scenario Run Rate": "cr",
        "Run Rate Change %": "pct_signed", "Jan Achievement": "cr",
        "Jan Achievement %": "pct", "Feb-Mar Run Rate": "cr",
        "Current March Projection %": "pct", "Scenario March Achievement": "cr",
        "Scenario March Achievement %": "pct", "Incremental Sales": "cr_signed",
    }
    return pd.DataFrame(rows), formats


def build_revenue_impact(model: ScenarioModel, basis: str) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Revenue by asset class - never a blended rate."""
    bundle = revenue_bundle(model, basis)
    rows = []
    for asset in ASSETS:
        rows.append({
            "Asset Class": asset,
            "Scenario Sales": bundle["scenario"]["sales_by_asset"][asset],
            "Revenue Rate": f"{REVENUE_BPS[asset]:.0f} bps",
            "Scenario Revenue": bundle["scenario"]["by_asset"][asset],
            "Baseline Revenue": bundle["baseline"]["by_asset"][asset],
            "Incremental Revenue": bundle["incremental"]["by_asset"][asset],
            "Revenue Contribution %": bundle["incremental"]["contribution"][asset],
        })
    rows.append({
        "Asset Class": "Total",
        "Scenario Sales": sum(_z(v) for v in bundle["scenario"]["sales_by_asset"].values()),
        "Revenue Rate": "—",
        "Scenario Revenue": bundle["scenario"]["total"],
        "Baseline Revenue": bundle["baseline"]["total"],
        "Incremental Revenue": bundle["incremental"]["total"],
        "Revenue Contribution %": 1.0 if bundle["scenario"]["total"] else None,
    })
    formats = {
        "Asset Class": "txt", "Scenario Sales": "cr", "Revenue Rate": "txt",
        "Scenario Revenue": "cr1", "Baseline Revenue": "cr1",
        "Incremental Revenue": "cr1_signed", "Revenue Contribution %": "pct",
    }
    return pd.DataFrame(rows), formats


def build_vertical_summary(model: ScenarioModel) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Retail versus DHNI, for Gross Sales and Net Sales."""
    rows = []
    for vertical in model.available_verticals():
        for sales in SALES_TYPES:
            cell = model.cell(sales, vertical=vertical)
            bundle = revenue_bundle(model, sales, vertical=vertical)
            rows.append({
                "Vertical": vertical,
                "Sales": SALES_LABEL[sales],
                "FY Target": cell["fy_target"],
                "YTD Achievement": cell["ytd_ach"],
                "Target Achieved %": cell["ytd_ach_pct"],
                "Current Run Rate": cell["current_rr"],
                "Scenario Run Rate": cell["scen_rr"],
                "Run Rate Change %": cell["rr_change_pct"],
                "Current March Projection %": cell["current_march_pct"],
                "Scenario Milestone %": cell["milestone_pct"],
                "Scenario March Projection %": cell["march_pct"],
                "Scenario Revenue": bundle["scenario"]["total"],
                "Incremental Revenue": bundle["incremental"]["total"],
            })
    formats = {
        "Vertical": "txt", "Sales": "txt", "FY Target": "cr", "YTD Achievement": "cr",
        "Target Achieved %": "pct", "Current Run Rate": "cr", "Scenario Run Rate": "cr",
        "Run Rate Change %": "pct_signed", "Current March Projection %": "pct",
        "Scenario Milestone %": "pct", "Scenario March Projection %": "pct",
        "Scenario Revenue": "cr1", "Incremental Revenue": "cr1_signed",
    }
    return pd.DataFrame(rows), formats


def build_asset_breakdown(model: ScenarioModel, sales: str) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Equity / Debt / Liquid split within each vertical."""
    rows = []
    include_dip = model.scenario_id in (3, 7)
    for vertical in model.available_verticals():
        for asset in ASSETS:
            cell = model.cell(sales, asset=asset, vertical=vertical)
            revenue = _z(cell["march_amount"]) * REVENUE_RATE[asset]
            baseline_revenue = _z(cell["current_march"]) * REVENUE_RATE[asset]
            row = {
                "Vertical": vertical,
                "Asset": asset,
                "FY Target": cell["fy_target"],
                "YTD Achievement": cell["ytd_ach"],
                "Target Achieved %": cell["ytd_ach_pct"],
                "Current Run Rate": cell["current_rr"],
                "Scenario Run Rate": cell["scen_rr"],
                "Run Rate Change %": cell["rr_change_pct"],
            }
            if include_dip:
                row["Feb-Mar Run Rate"] = cell["feb_mar_rr"]
            row.update({
                "Current March Projection %": cell["current_march_pct"],
                "Scenario Milestone %": cell["milestone_pct"],
                "Scenario March Projection %": cell["march_pct"],
                "Scenario Revenue": revenue,
                "Incremental Revenue": revenue - baseline_revenue,
            })
            rows.append(row)
    formats = {
        "Vertical": "txt", "Asset": "txt", "FY Target": "cr", "YTD Achievement": "cr",
        "Target Achieved %": "pct", "Current Run Rate": "cr", "Scenario Run Rate": "cr",
        "Run Rate Change %": "pct_signed", "Feb-Mar Run Rate": "cr",
        "Current March Projection %": "pct", "Scenario Milestone %": "pct",
        "Scenario March Projection %": "pct", "Scenario Revenue": "cr1",
        "Incremental Revenue": "cr1_signed",
    }
    return pd.DataFrame(rows), formats


def build_segment_scenario_analysis(
    model: ScenarioModel, sales: str
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Scenario 6 - differentiated performance by business segment."""
    rows = []
    for segment in model.available_segments():
        cell = model.cell(sales, segment=segment)
        rows.append({
            "Segment": segment,
            "FY Target": cell["fy_target"],
            "YTD Achievement": cell["ytd_ach"],
            "Current Run Rate": cell["current_rr"],
            "Current March Projection": cell["current_march"],
            "Scenario Achievement %": cell["milestone_pct"],
            "Scenario Target Amount": cell["march_required"],
            "Scenario Required Run Rate": cell["scen_rr"],
            "Run Rate Uplift %": cell["rr_change_pct"],
            "Incremental Amount": cell["incremental_sales"],
        })
    overall = model.cell(sales)
    rows.append({
        "Segment": "Overall",
        "FY Target": overall["fy_target"],
        "YTD Achievement": overall["ytd_ach"],
        "Current Run Rate": overall["current_rr"],
        "Current March Projection": overall["current_march"],
        "Scenario Achievement %": overall["march_pct"],
        "Scenario Target Amount": overall["march_required"],
        "Scenario Required Run Rate": overall["scen_rr"],
        "Run Rate Uplift %": overall["rr_change_pct"],
        "Incremental Amount": overall["incremental_sales"],
    })
    formats = {
        "Segment": "txt", "FY Target": "cr", "YTD Achievement": "cr",
        "Current Run Rate": "cr", "Current March Projection": "cr",
        "Scenario Achievement %": "pct", "Scenario Target Amount": "cr",
        "Scenario Required Run Rate": "cr", "Run Rate Uplift %": "pct_signed",
        "Incremental Amount": "cr_signed",
    }
    return pd.DataFrame(rows), formats


def build_momentum_analysis(cell: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Scenario 7 - month-by-month momentum trajectory."""
    trajectory = cell.get("trajectory") or []
    current_rr = _num(cell.get("current_rr"))
    growth = cell.get("momentum_g")
    leakage = _z(cell.get("leakage"))
    fy_target = cell.get("fy_target")
    cumulative = _z(cell.get("ytd_ach"))

    rows = []
    previous = current_rr
    for position, month in enumerate(FUTURE_MONTHS):
        run_rate = trajectory[position] if position < len(trajectory) else None
        cumulative += _z(run_rate)
        if position < MONTHS_JUL_JAN:
            mom = growth if growth is not None else safe_div(run_rate, previous)
            if growth is None and mom is not None:
                mom = mom - 1.0
            phase = "Momentum build-up"
        else:
            mom = -leakage
            phase = "Feb-Mar leakage"
        rows.append({
            "Month": month,
            "Phase": phase,
            "Current Run Rate": current_rr,
            "Required Scenario Run Rate": run_rate,
            "MoM Growth": mom,
            "Cumulative Achievement": cumulative,
            "Achievement %": safe_div(cumulative, fy_target),
        })
        previous = run_rate
    formats = {
        "Month": "txt", "Phase": "txt", "Current Run Rate": "cr",
        "Required Scenario Run Rate": "cr", "MoM Growth": "pct_signed",
        "Cumulative Achievement": "cr", "Achievement %": "pct",
    }
    return pd.DataFrame(rows), formats


def build_momentum_by_group(
    model: ScenarioModel, sales: str, dimension: str
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Scenario 7 applied independently to asset classes or to verticals."""
    if dimension == "asset":
        keys = [("Asset", asset, {"asset": asset}) for asset in ASSETS]
        first_column = "Asset"
    else:
        keys = [("Vertical", v, {"vertical": v}) for v in model.available_verticals()]
        first_column = "Vertical"

    rows = []
    for _, name, filters in keys:
        cell = model.cell(sales, **filters)
        rows.append({
            first_column: name,
            "Current Run Rate": cell["current_rr"],
            "Required MoM Momentum": cell["momentum_g"],
            "January Achievement": cell["jan_amount"],
            "January Achievement %": cell["jan_pct"],
            "Feb-Mar Leakage": cell.get("leakage"),
            "March Achievement": cell["march_amount"],
            "March Achievement %": cell["march_pct"],
            "Headroom / Shortfall": cell["headroom_amt"],
        })
    formats = {
        first_column: "txt", "Current Run Rate": "cr",
        "Required MoM Momentum": "pct_signed", "January Achievement": "cr",
        "January Achievement %": "pct", "Feb-Mar Leakage": "pct",
        "March Achievement": "cr", "March Achievement %": "pct",
        "Headroom / Shortfall": "cr_signed",
    }
    return pd.DataFrame(rows), formats


def build_monthly_revenue(model: ScenarioModel, basis: str) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Scenario 7 - monthly revenue implied by the momentum trajectory."""
    trajectories = {
        asset: (model.cell(basis, asset=asset).get("trajectory") or [])
        for asset in ASSETS
    }
    rows = []
    for position, month in enumerate(FUTURE_MONTHS):
        row = {"Month": month}
        total = 0.0
        for asset in ASSETS:
            series = trajectories[asset]
            sales_amount = series[position] if position < len(series) else 0.0
            revenue = _z(sales_amount) * REVENUE_RATE[asset]
            row[f"{asset} Revenue"] = revenue
            total += revenue
        row["Total Revenue"] = total
        rows.append(row)
    formats = {"Month": "txt", "Total Revenue": "cr1"}
    for asset in ASSETS:
        formats[f"{asset} Revenue"] = "cr1"
    return pd.DataFrame(rows), formats


def build_leakage_sensitivity(
    model: ScenarioModel, basis: str
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """Scenario 7 - how the March outcome moves with the leakage assumption."""
    subset = filter_grid(model.grid, sales=basis)
    fy_target = subset["fy_target"].sum()
    ytd_target = subset["ytd_target"].sum()
    ytd_ach = subset["ytd_ach"].sum()
    rows = []
    for leakage in (0.0, 0.10, 0.20, 0.30):
        params = dict(model.params)
        params["leakage"] = leakage
        cell = calculate_scenario_7(fy_target, ytd_target, ytd_ach, params)
        rows.append({
            "Feb-Mar Leakage": leakage,
            "Required MoM Momentum": cell["momentum_g"],
            "January Achievement %": cell["jan_pct"],
            "March Achievement %": cell["march_pct"],
            "Headroom / Shortfall": cell["headroom_amt"],
        })
    formats = {
        "Feb-Mar Leakage": "pct", "Required MoM Momentum": "pct_signed",
        "January Achievement %": "pct", "March Achievement %": "pct",
        "Headroom / Shortfall": "cr_signed",
    }
    return pd.DataFrame(rows), formats


def build_scenario_guide(model: ScenarioModel, basis: str) -> pd.DataFrame:
    rows = []
    for scenario_id in SCENARIO_ORDER:
        meta = SCENARIOS[scenario_id]
        rows.append({
            "Scenario": meta["label"],
            "Description": meta["explanation"],
            "Milestone": meta["milestone"],
            "Selected": "Yes" if scenario_id == model.scenario_id else "",
        })
    rows.append({
        "Scenario": "Revenue methodology",
        "Description": (
            "Revenue is estimated at asset-class level using 60 bps for Equity, 20 bps for Debt "
            f"and 10 bps for Liquid, applied to {SALES_LABEL[basis]} only so that Gross Sales and "
            "Net Sales revenue are never double counted."
        ),
        "Milestone": "",
        "Selected": "",
    })
    rows.append({
        "Scenario": "Timeline assumption",
        "Description": (
            "April, May and June are complete. Three months completed, nine months remaining "
            "(July-January is seven months, February-March is two months). The current run rate "
            "is YTD achievement divided by three."
        ),
        "Milestone": "",
        "Selected": "",
    })
    if model.scenario_id == 3:
        rows.append({
            "Scenario": "Scenario 3 setting",
            "Description": f"Feb-Mar run-rate dip: {fmt_pct(model.params.get('dip', S3_DEFAULT_DIP))}",
            "Milestone": "", "Selected": "",
        })
    if model.scenario_id == 7:
        rows.append({
            "Scenario": "Scenario 7 settings",
            "Description": (
                f"January target: {fmt_pct(model.params.get('jan_target', S7_DEFAULT_JAN_TARGET))} · "
                f"March target: {fmt_pct(model.params.get('mar_target', S7_DEFAULT_MAR_TARGET))} · "
                f"Feb-Mar leakage: {fmt_pct(model.params.get('leakage', S7_DEFAULT_LEAKAGE))}"
            ),
            "Milestone": "", "Selected": "",
        })
    return pd.DataFrame(rows)


# =============================================================================
# 11. EXCEL EXPORT
# =============================================================================

def _round_frame(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for column in out.columns:
        if pd.api.types.is_numeric_dtype(out[column]):
            out[column] = out[column].astype(float).round(4)
    return out


def make_export_excel(model: ScenarioModel, basis: str) -> bytes:
    """Build the management export workbook for the selected scenario."""
    sheets: List[Tuple[str, pd.DataFrame]] = []
    sheets.append(("Scenario Guide", build_scenario_guide(model, basis)))
    sheets.append(("Current Baseline", build_current_overview(model)[0]))
    sheets.append(("Current vs Scenario", build_comparison(model)[0]))
    sheets.append(("Revenue Impact", build_revenue_impact(model, basis)[0]))
    sheets.append(("Retail-DHNI Summary", build_vertical_summary(model)[0]))
    sheets.append(("Gross Sales Breakdown", build_asset_breakdown(model, "GS")[0]))
    sheets.append(("Net Sales Breakdown", build_asset_breakdown(model, "NS")[0]))

    segment_model = model if model.scenario_id == 6 else ScenarioModel(6, model.grid, model.params)
    segment_frames = []
    for sales in SALES_TYPES:
        frame = build_segment_scenario_analysis(segment_model, sales)[0]
        frame.insert(0, "Sales", SALES_LABEL[sales])
        segment_frames.append(frame)
    sheets.append(("Scenario 6 Segments", pd.concat(segment_frames, ignore_index=True)))

    momentum_model = model if model.scenario_id == 7 else ScenarioModel(7, model.grid, model.params)
    momentum_frames = []
    for sales in SALES_TYPES:
        overall = momentum_model.cell(sales)
        frame = build_momentum_analysis(overall)[0]
        frame.insert(0, "Sales", SALES_LABEL[sales])
        momentum_frames.append(frame)
    for sales in SALES_TYPES:
        for dimension in ("asset", "vertical"):
            frame = build_momentum_by_group(momentum_model, sales, dimension)[0]
            frame.insert(0, "Sales", SALES_LABEL[sales])
            momentum_frames.append(frame)
    sheets.append(("Scenario 7 Momentum", pd.concat(momentum_frames, ignore_index=True)))
    sheets.append(("S7 Monthly Revenue", build_monthly_revenue(momentum_model, basis)[0]))

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for name, frame in sheets:
            _round_frame(frame).to_excel(writer, sheet_name=name[:31], index=False)
        _style_workbook(writer)
    return buffer.getvalue()


def _style_workbook(writer: Any) -> None:
    """Bold headers, frozen top row and sensible column widths."""
    try:
        from openpyxl.styles import Alignment, Font, PatternFill
    except Exception:  # pragma: no cover - openpyxl always present in the stack
        return
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="1F2937")
    for worksheet in writer.book.worksheets:
        worksheet.freeze_panes = "A2"
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        for column_cells in worksheet.columns:
            longest = 0
            letter = column_cells[0].column_letter
            for cell in column_cells:
                value = "" if cell.value is None else str(cell.value)
                longest = max(longest, min(len(value), 60))
            worksheet.column_dimensions[letter].width = max(12, min(longest + 3, 62))


# =============================================================================
# 12. PRESENTATION LAYER - THEME
# =============================================================================

CUSTOM_CSS = """
<style>
.stApp, [data-testid="stAppViewContainer"] { background-color: #07111F; }
[data-testid="stHeader"] { background: transparent; }
.block-container, [data-testid="stMainBlockContainer"] {
    padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1600px;
}

.stApp, .stApp p, .stApp span, .stApp li, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: #F8FAFC; }

.app-title { font-size: 1.65rem; font-weight: 700; color: #F8FAFC; margin: 0 0 2px 0; letter-spacing: -0.01em; }
.app-sub { color: #94A3B8; font-size: 0.86rem; margin: 0 0 2px 0; }
.app-rule { height: 1px; background: #334155; margin: 12px 0 4px 0; }

.section-label {
    font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase;
    color: #94A3B8; font-weight: 700; margin: 18px 0 8px 0;
    border-left: 3px solid #3B82F6; padding-left: 10px;
}
.callout {
    background: #111827; border: 1px solid #334155; border-left: 3px solid #3B82F6;
    border-radius: 8px; padding: 12px 16px; color: #E2E8F0; font-size: 0.88rem;
    line-height: 1.55; margin: 4px 0 10px 0;
}
.callout-warn { border-left-color: #F59E0B; }
.callout-ok { border-left-color: #22C55E; }
.tag-ok { color: #22C55E; font-weight: 700; }
.tag-warn { color: #F59E0B; font-weight: 700; }
.note { color: #94A3B8; font-size: 0.78rem; margin: 2px 0 10px 0; }

[data-testid="stMetric"], [data-testid="metric-container"] {
    background: #111827; border: 1px solid #334155; border-radius: 10px;
    padding: 14px 16px 12px 16px; min-height: 108px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.35);
}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div {
    color: #94A3B8 !important; font-size: 0.72rem !important;
    letter-spacing: 0.07em; text-transform: uppercase; font-weight: 600;
}
[data-testid="stMetricValue"] { color: #F8FAFC !important; font-size: 1.42rem !important; font-weight: 700; }
[data-testid="stMetricDelta"] { font-size: 0.76rem !important; }

[data-testid="stDataFrame"] { border: 1px solid #334155; border-radius: 8px; }
[data-testid="stVegaLiteChart"] text { fill: #CBD5E1 !important; }
[data-testid="stVegaLiteChart"] .role-axis-grid line { stroke: #1E293B !important; }
[data-testid="stVegaLiteChart"] .role-axis line,
[data-testid="stVegaLiteChart"] .role-axis path { stroke: #334155 !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #334155; }
.stTabs [data-baseweb="tab"] { color: #94A3B8; }
.stTabs [aria-selected="true"] { color: #F8FAFC; }
[data-testid="stExpander"] {
    border: 1px solid #334155 !important; border-radius: 8px; background: #0B1626;
}

[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
    background: #F8FAFC !important; border-right: 1px solid #CBD5E1;
}
[data-testid="stSidebar"] * { color: #0F172A !important; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] small { color: #475569 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] input { background: #FFFFFF !important; }
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
}
.sidebar-title {
    font-size: 0.74rem; letter-spacing: 0.16em; text-transform: uppercase;
    font-weight: 700; color: #0F172A; margin-bottom: 6px;
}
.sidebar-card {
    background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 3px solid #3B82F6;
    border-radius: 8px; padding: 10px 12px; margin: 4px 0 12px 0;
}
.sidebar-card .s-name { font-weight: 700; font-size: 0.88rem; color: #0F172A; }
.sidebar-card .s-body { font-size: 0.78rem; color: #475569; line-height: 1.5; margin-top: 4px; }
.sidebar-card .s-milestone { font-size: 0.75rem; color: #0F172A; margin-top: 6px; font-weight: 600; }

</style>
"""


def rerun() -> None:
    handler = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
    if handler is not None:
        handler()


def _dataframe_kwargs() -> Dict[str, Any]:
    try:
        parameters = inspect.signature(st.dataframe).parameters
    except (TypeError, ValueError):
        return {}
    if "width" in parameters and parameters["width"].default == "stretch":
        return {}
    if "use_container_width" in parameters:
        return {"use_container_width": True}
    return {}


def show_table(frame: pd.DataFrame, formats: Optional[Dict[str, str]] = None) -> None:
    display = format_table(frame, formats) if formats else frame
    try:
        st.dataframe(display, hide_index=True, **_dataframe_kwargs())
    except TypeError:  # pragma: no cover - very old Streamlit
        st.dataframe(display)


def section(title: str) -> None:
    st.markdown(f"<div class='section-label'>{title}</div>", unsafe_allow_html=True)


def callout(text: str, tone: str = "") -> None:
    css = "callout" + (f" callout-{tone}" if tone else "")
    st.markdown(f"<div class='{css}'>{text}</div>", unsafe_allow_html=True)


def kpi_row(items: Sequence[Tuple]) -> None:
    if not items:
        return
    columns = st.columns(len(items))
    for column, item in zip(columns, items):
        label, value = item[0], item[1]
        delta = item[2] if len(item) > 2 else None
        delta_color = item[3] if len(item) > 3 else "normal"
        with column:
            if delta is None:
                st.metric(label, value)
            else:
                st.metric(label, value, delta, delta_color=delta_color)


# =============================================================================
# 13. UPLOAD GATE
# =============================================================================

def render_upload_screen() -> None:
    _, middle, _ = st.columns([1, 2, 1])
    with middle:
        _render_upload_body()


def _render_upload_body() -> None:
    st.markdown(f"<div class='app-title'>{APP_TITLE}</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='app-sub'>Upload the RM scorecard workbook to open the dashboard. "
        "Nothing is stored beyond this session.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='app-rule'></div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Workbook", type=["xlsx", "xlsm"], label_visibility="collapsed",
    )
    if uploaded is not None:
        payload = uploaded.getvalue()
        try:
            load_workbook(payload)
        except WorkbookError as error:
            st.error(str(error))
        except Exception:  # pragma: no cover - defensive, never show a traceback
            st.error(
                "The workbook could not be read. Please check that it is a valid Excel file "
                "containing the RM Retail Sales and RM DHNI sheets."
            )
        else:
            st.session_state["workbook"] = payload
            rerun()


# =============================================================================
# 14. SIDEBAR
# =============================================================================

def render_sidebar(records: pd.DataFrame) -> Tuple[int, Dict[str, Any], str, Dict[str, Any]]:
    sidebar = st.sidebar
    sidebar.markdown("<div class='sidebar-title'>Scenario Navigator</div>", unsafe_allow_html=True)

    labels = [SCENARIOS[i]["label"] for i in SCENARIO_ORDER]
    selected_label = sidebar.radio(
        "Scenario", labels, index=0, key="scenario_choice", label_visibility="collapsed",
    )
    scenario_id = SCENARIO_ORDER[labels.index(selected_label)]
    meta = SCENARIOS[scenario_id]
    sidebar.markdown(
        "<div class='sidebar-card'>"
        f"<div class='s-name'>Scenario {scenario_id} · {meta['name']}</div>"
        f"<div class='s-body'>{meta['explanation']}</div>"
        f"<div class='s-milestone'>Target milestone: {meta['milestone']}</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    params: Dict[str, Any] = {
        "dip": S3_DEFAULT_DIP,
        "jan_target": S7_DEFAULT_JAN_TARGET,
        "mar_target": S7_DEFAULT_MAR_TARGET,
        "leakage": S7_DEFAULT_LEAKAGE,
    }

    if scenario_id == 3:
        sidebar.markdown("<div class='sidebar-title'>Scenario controls</div>", unsafe_allow_html=True)
        params["dip"] = sidebar.slider(
            "Feb-Mar Run-Rate Dip", min_value=0, max_value=60,
            value=int(S3_DEFAULT_DIP * 100), step=5, format="%d%%", key="s3_dip",
        ) / 100.0

    if scenario_id == 7:
        sidebar.markdown("<div class='sidebar-title'>Scenario controls</div>", unsafe_allow_html=True)
        params["jan_target"] = sidebar.slider(
            "January Achievement Target", min_value=90, max_value=120,
            value=int(S7_DEFAULT_JAN_TARGET * 100), step=1, format="%d%%", key="s7_jan",
        ) / 100.0
        params["mar_target"] = sidebar.slider(
            "March Achievement Target", min_value=90, max_value=120,
            value=int(S7_DEFAULT_MAR_TARGET * 100), step=1, format="%d%%", key="s7_mar",
        ) / 100.0
        params["leakage"] = sidebar.slider(
            "Feb-Mar AUM Leakage", min_value=0, max_value=30,
            value=int(S7_DEFAULT_LEAKAGE * 100), step=1, format="%d%%", key="s7_leak",
        ) / 100.0

    mapping = render_segment_controls(records)

    with sidebar.expander("Assumptions", expanded=False):
        basis_label = st.radio(
            "Revenue basis", [SALES_LABEL["GS"], SALES_LABEL["NS"]], index=0, key="revenue_basis",
            help="Revenue is computed on one sales basis only so that Gross Sales and "
                 "Net Sales revenue are never double counted.",
        )
        st.caption(
            "Revenue rates: Equity 60 bps · Debt 20 bps · Liquid 10 bps. "
            "Timeline: April-June complete, 9 months remaining, "
            "July-January 7 months, February-March 2 months."
        )
    basis = "GS" if basis_label == SALES_LABEL["GS"] else "NS"

    sidebar.markdown("<div class='app-rule'></div>", unsafe_allow_html=True)
    if sidebar.button("Use another workbook"):
        reset_workbook()

    return scenario_id, params, basis, mapping


def render_segment_controls(records: pd.DataFrame) -> Dict[str, Any]:
    """Configurable segment classification for Scenario 6."""
    suggestions = identify_segments(records)
    mapping: Dict[str, Any] = dict(st.session_state.get("segment_mapping") or suggestions)

    usable_columns = [
        field for field in META_FIELDS
        if field in records.columns and text_column(records, field).ne("").any()
    ]

    with st.sidebar.expander("Segment mapping (Scenario 6)", expanded=False):
        st.caption(
            "Digital, Retail B30 and Others are derived from workbook metadata. "
            "Adjust the classification here; every other record falls into Others."
        )
        for segment in ("Digital", "Retail B30"):
            options = ["(not mapped)"] + usable_columns
            current = mapping.get(segment, {}).get("column", "(not mapped)")
            index = options.index(current) if current in options else 0
            column = st.selectbox(
                f"{segment} identified by", options, index=index, key=f"seg_col_{segment}",
            )
            if column == "(not mapped)":
                mapping.pop(segment, None)
                continue
            values = sorted({v for v in text_column(records, column) if v.strip()})
            preset = [v for v in mapping.get(segment, {}).get("values", []) if v in values]
            chosen = st.multiselect(
                f"{segment} values", values, default=preset,
                key=f"seg_vals_{segment}_{column}",
            )
            if chosen:
                mapping[segment] = {"column": column, "values": list(chosen)}
            else:
                mapping.pop(segment, None)

    st.session_state["segment_mapping"] = mapping
    return mapping


# =============================================================================
# 15. DASHBOARD SECTIONS
# =============================================================================

def render_baseline(model: ScenarioModel) -> None:
    section("Current Baseline")
    cards = []
    for sales in SALES_TYPES:
        base = model.baseline(sales)
        cards.append((
            f"{sales} Current Run Rate", fmt_cr(base["current_rr"]),
            f"{fmt_pct(base['fy_completed_pct'])} of FY target booked", "off",
        ))
    for sales in SALES_TYPES:
        base = model.baseline(sales)
        delta = None if base["ytd_ach_pct"] is None else fmt_pts(base["ytd_ach_pct"] - 1.0)
        cards.append((f"{sales} Target Achieved %", fmt_pct(base["ytd_ach_pct"]), delta))
    for sales in SALES_TYPES:
        base = model.baseline(sales)
        delta = None if base["current_march_pct"] is None else fmt_pts(base["current_march_pct"] - 1.0)
        cards.append((f"{sales} March Projection %", fmt_pct(base["current_march_pct"]), delta))
    kpi_row(cards)
    st.markdown(
        "<div class='note'>Baseline is the Apr-Jun run rate carried forward for nine months. "
        "It never changes with the selected scenario.</div>",
        unsafe_allow_html=True,
    )


def scenario_cards(model: ScenarioModel, basis: str) -> List[Tuple]:
    kind = model.meta["kind"]
    cards: List[Tuple] = []

    if model.scenario_id == 6:
        for segment in model.available_segments():
            cell = model.cell(basis, segment=segment)
            delta = (
                None if cell["march_pct"] is None or cell["current_march_pct"] is None
                else fmt_pts(cell["march_pct"] - cell["current_march_pct"])
            )
            cards.append((f"{segment} Achievement", fmt_pct(cell["march_pct"]), delta))
        overall = model.cell(basis)
        cards.append((
            "Overall Achievement", fmt_pct(overall["march_pct"]),
            None if overall["march_pct"] is None or overall["current_march_pct"] is None
            else fmt_pts(overall["march_pct"] - overall["current_march_pct"]),
        ))
        cards.append((
            "Scenario March Projection", fmt_cr(overall["march_amount"]),
            fmt_cr_signed(overall["incremental_sales"]),
        ))
        return cards

    if model.scenario_id == 7:
        cell = model.cell(basis)
        momentum = cell["momentum_g"]
        cards.append((
            "Required MoM Momentum",
            fmt_pct(momentum) if momentum is not None else NA_TEXT,
            f"binding: {cell['binding']} milestone" if cell.get("binding") else None, "off",
        ))
        cards.append((
            "January Achievement", fmt_pct(cell["jan_pct"]),
            fmt_cr_signed(cell["jan_buffer"]) + " buffer" if cell["jan_buffer"] is not None else None,
        ))
        cards.append(("Feb-Mar Leakage", fmt_pct(cell.get("leakage")), None))
        cards.append((
            "March Achievement", fmt_pct(cell["march_pct"]),
            None if cell["march_pct"] is None or cell["current_march_pct"] is None
            else fmt_pts(cell["march_pct"] - cell["current_march_pct"]),
        ))
        cards.append((
            "March Headroom / Shortfall", fmt_cr_signed(cell["headroom_amt"]),
            fmt_pts(cell["headroom_pct"]) if cell["headroom_pct"] is not None else None,
        ))
        cards.append((
            "January Exit Run Rate", fmt_cr(cell["scen_rr"]),
            fmt_pct_signed(cell["rr_change_pct"]) if cell["rr_change_pct"] is not None else None,
        ))
        return cards

    for sales in SALES_TYPES:
        cell = model.cell(sales)
        label = "Scenario Run Rate" if kind == "runrate" else "Required Run Rate"
        cards.append((
            f"{sales} {label}", fmt_cr(cell["scen_rr"]),
            fmt_pct_signed(cell["rr_change_pct"]) if cell["rr_change_pct"] is not None else None,
        ))

    if kind == "jan_target":
        for sales in SALES_TYPES:
            cell = model.cell(sales)
            cards.append((
                f"{sales} January Achievement", fmt_pct(cell["jan_pct"]),
                fmt_cr(cell["jan_amount"]), "off",
            ))
    for sales in SALES_TYPES:
        cell = model.cell(sales)
        delta = (
            None if cell["march_pct"] is None or cell["current_march_pct"] is None
            else fmt_pts(cell["march_pct"] - cell["current_march_pct"])
        )
        cards.append((f"{sales} March Achievement", fmt_pct(cell["march_pct"]), delta))
    return cards


def render_comparison(model: ScenarioModel, basis: str) -> None:
    section(f"Current vs Scenario {model.scenario_id} · {model.meta['name']}")
    cards = scenario_cards(model, basis)
    if len(cards) <= 6:
        kpi_row(cards)
    else:
        kpi_row(cards[:4])
        kpi_row(cards[4:8])

    if model.scenario_id in (2, 5):
        implied = model.implied_milestones(basis)
        st.markdown(
            "<div class='note'>Equity carries the fixed ambition; Debt and Liquid share the "
            f"residual requirement in FY-target proportion — implied milestone of "
            f"{fmt_pct(implied['Debt'])} of FY target for both ({SALES_LABEL[basis]}).</div>",
            unsafe_allow_html=True,
        )
    if model.scenario_id == 3:
        st.markdown(
            f"<div class='note'>February-March run rate is set at "
            f"{fmt_pct(1 - model.params['dip'])} of the July-January required run rate.</div>",
            unsafe_allow_html=True,
        )
    if model.scenario_id == 2:
        st.markdown(
            "<div class='note'>February-March is assumed to continue at the July-January "
            "required run rate.</div>",
            unsafe_allow_html=True,
        )


def render_revenue_kpis(model: ScenarioModel, basis: str) -> Dict[str, Any]:
    section("Revenue / Earnings Impact")
    bundle = revenue_bundle(model, basis)
    baseline_total = bundle["baseline"]["total"]
    scenario_total = bundle["scenario"]["total"]
    incremental = bundle["incremental"]
    kpi_row([
        ("Baseline Revenue", fmt_cr(baseline_total, 1), "current run rate", "off"),
        ("Scenario Revenue", fmt_cr(scenario_total, 1), fmt_cr_signed(incremental["total"], 1)),
        ("Incremental Revenue", fmt_cr_signed(incremental["total"], 1),
         fmt_pct_signed(incremental["uplift_pct"]) if incremental["uplift_pct"] is not None else None),
        ("Revenue Uplift %",
         fmt_pct(incremental["uplift_pct"]) if incremental["uplift_pct"] is not None else NA_TEXT,
         f"on {SALES_LABEL[basis]}", "off"),
    ])
    st.markdown(
        f"<div class='note'>Revenue is calculated at asset-class level (Equity 60 bps, Debt 20 bps, "
        f"Liquid 10 bps) on {SALES_LABEL[basis]} only — no blended rate, no double counting.</div>",
        unsafe_allow_html=True,
    )
    return bundle


def render_detail_expander(model: ScenarioModel) -> None:
    with st.expander("Detailed baseline and comparison numbers", expanded=False):
        st.markdown("**Current baseline**")
        frame, formats = build_current_overview(model)
        show_table(frame, formats)
        st.markdown("**Current vs selected scenario**")
        frame, formats = build_comparison(model)
        show_table(frame, formats)


def render_vertical_section(model: ScenarioModel) -> None:
    section("Retail vs DHNI")
    frame, formats = build_vertical_summary(model)
    show_table(frame, formats)
    st.markdown(
        "<div class='note'>Revenue on each row is calculated on that row's own sales basis; "
        "Gross Sales and Net Sales revenue are alternative views and are never added together.</div>",
        unsafe_allow_html=True,
    )


def render_asset_section(model: ScenarioModel) -> None:
    section("Equity / Debt / Liquid Breakdown")
    tabs = st.tabs([SALES_LABEL["GS"], SALES_LABEL["NS"]])
    for tab, sales in zip(tabs, SALES_TYPES):
        with tab:
            frame, formats = build_asset_breakdown(model, sales)
            show_table(frame, formats)


def render_segment_section(model: ScenarioModel, basis: str, counts: Dict[str, int]) -> None:
    section("Scenario 6 · Segment Analysis")
    unmapped = [s for s in ("Digital", "Retail B30") if counts.get(s, 0) == 0]
    if unmapped:
        missing = " and ".join(unmapped)
        callout(
            f"<b>Segment validation:</b> no records could be reliably classified as {missing} "
            "from the workbook metadata (MKT TYPE, Type, ZONE, REGION, EM City). "
            "Those records have <b>not</b> been reallocated — they remain in Others, and the "
            f"{missing} scenario uplift is therefore not applied. Use "
            "<i>Segment mapping (Scenario 6)</i> in the sidebar to point the classification at "
            "the correct column and values.",
            tone="warn",
        )

    present = " · ".join(
        f"{segment} {S6_SEGMENT_TARGETS[segment]:.0%} of FY target ({counts.get(segment, 0)} RMs)"
        for segment in SEGMENT_ORDER
    )
    st.markdown(f"<div class='note'>Scenario assumption — {present}.</div>", unsafe_allow_html=True)

    tabs = st.tabs([SALES_LABEL["GS"], SALES_LABEL["NS"]])
    for tab, sales in zip(tabs, SALES_TYPES):
        with tab:
            frame, formats = build_segment_scenario_analysis(model, sales)
            show_table(frame, formats)

    overall = model.cell(basis)
    lines = []
    for segment in model.available_segments():
        cell = model.cell(basis, segment=segment)
        uplift = (
            fmt_pct_signed(cell["rr_change_pct"]) if cell["rr_change_pct"] is not None else NA_TEXT
        )
        lines.append(
            f"<b>{segment}</b> moves from {fmt_pct(cell['current_march_pct'])} to "
            f"{fmt_pct(cell['march_pct'])} of FY target, needing {fmt_cr(cell['scen_rr'])} per month "
            f"({uplift} run-rate uplift)"
        )
    callout(
        f"On {SALES_LABEL[basis]}: " + "; ".join(lines) + ". Overall March achievement moves from "
        f"{fmt_pct(overall['current_march_pct'])} to {fmt_pct(overall['march_pct'])}, an improvement "
        f"of {fmt_cr_signed(overall['incremental_sales'])}."
    )


def render_momentum_section(model: ScenarioModel, basis: str) -> None:
    section("Scenario 7 · Momentum Analysis")
    cell = model.cell(basis)
    momentum = cell["momentum_g"]

    kpi_row([
        ("Current Run Rate", fmt_cr(cell["current_rr"]), f"Apr-Jun, {SALES_LABEL[basis]}", "off"),
        ("Required MoM Momentum", fmt_pct(momentum) if momentum is not None else NA_TEXT,
         f"binding: {cell['binding']}" if cell.get("binding") else None, "off"),
        ("January Target", fmt_cr(cell["jan_required"]),
         fmt_pct(model.params["jan_target"]) + " of FY target", "off"),
        ("January Scenario Achievement", fmt_cr(cell["jan_amount"]), fmt_pct(cell["jan_pct"]), "off"),
    ])
    kpi_row([
        ("January Buffer", fmt_cr_signed(cell["jan_buffer"]),
         fmt_pct_signed(cell["jan_buffer_pct"]) if cell["jan_buffer_pct"] is not None else None),
        ("Feb-Mar Leakage", fmt_pct(cell.get("leakage")),
         f"Feb {fmt_cr(cell['feb_mar_rr'])} · Mar {fmt_cr(cell.get('march_rr'))}", "off"),
        ("March Scenario Achievement", fmt_cr(cell["march_amount"]), fmt_pct(cell["march_pct"]), "off"),
        ("March Headroom / Shortfall", fmt_cr_signed(cell["headroom_amt"]),
         fmt_pts(cell["headroom_pct"]) if cell["headroom_pct"] is not None else None),
    ])

    if cell["feasible"]:
        callout(
            "<span class='tag-ok'>✓ TARGET ACHIEVABLE</span> — the momentum trajectory reaches the "
            f"January milestone and still clears the March ambition after "
            f"{fmt_pct(cell.get('leakage'))} Feb-Mar leakage.",
            tone="ok",
        )
    else:
        callout(
            "<span class='tag-warn'>⚠ ADDITIONAL MOMENTUM REQUIRED</span> — additional March sales "
            f"required: {fmt_cr(cell.get('additional_march_sales'))}; additional January run rate "
            f"required: {fmt_cr(cell.get('additional_jan_rr'))} per month.",
            tone="warn",
        )
    if cell.get("note"):
        st.markdown(f"<div class='note'>{cell['note']}</div>", unsafe_allow_html=True)

    momentum_text = fmt_pct(momentum) if momentum is not None else "a flat required"
    outcome = (
        f"{fmt_pct(cell['headroom_pct'])} headroom" if _z(cell["headroom_amt"]) >= 0
        else f"a {fmt_cr(abs(_z(cell['headroom_amt'])))} shortfall"
    )
    callout(
        f"<b>Momentum required:</b> the business needs to build approximately {momentum_text} "
        f"month-on-month momentum from July through January — lifting the monthly run rate from "
        f"{fmt_cr(cell['current_rr'])} to {fmt_cr(cell['scen_rr'])} by January — to reach the "
        f"{fmt_pct(model.params['jan_target'])} January milestone. With an assumed "
        f"{fmt_pct(cell.get('leakage'))} February-March leakage, the trajectory delivers "
        f"{fmt_pct(cell['march_pct'])} achievement by March against a "
        f"{fmt_pct(model.params['mar_target'])} ambition, creating {outcome}. "
        f"January buffer created before leakage: {fmt_cr_signed(cell['jan_buffer'])}."
    )

    st.markdown("**Monthly momentum trajectory**")
    frame, formats = build_momentum_analysis(cell)
    show_table(frame, formats)

    trajectory = cell.get("trajectory") or []
    if trajectory:
        chart = pd.DataFrame(
            {
                "Current run-rate trajectory": [_z(cell["current_rr"])] * len(trajectory),
                "Required momentum trajectory": trajectory,
            },
            index=MONTH_DATES[: len(trajectory)],
        )
        st.line_chart(chart)
        st.markdown(
            f"<div class='note'>January 2027 milestone: {fmt_cr(cell['jan_required'])} cumulative "
            f"({fmt_pct(model.params['jan_target'])} of FY target) — reached at a monthly run rate of "
            f"{fmt_cr(cell['scen_rr'])}, after which February and March step down by "
            f"{fmt_pct(cell.get('leakage'))} each.</div>",
            unsafe_allow_html=True,
        )

    tabs = st.tabs(["Asset class", "Retail vs DHNI", "Leakage sensitivity", "Monthly revenue"])
    with tabs[0]:
        for sales in SALES_TYPES:
            st.markdown(f"**{SALES_LABEL[sales]}**")
            frame, formats = build_momentum_by_group(model, sales, "asset")
            show_table(frame, formats)
    with tabs[1]:
        for sales in SALES_TYPES:
            st.markdown(f"**{SALES_LABEL[sales]}**")
            frame, formats = build_momentum_by_group(model, sales, "vertical")
            show_table(frame, formats)
    with tabs[2]:
        frame, formats = build_leakage_sensitivity(model, basis)
        show_table(frame, formats)
        st.markdown(
            "<div class='note'>Momentum is re-solved at each leakage assumption, so the required "
            "July-January build changes with the February-March pressure.</div>",
            unsafe_allow_html=True,
        )
    with tabs[3]:
        frame, formats = build_monthly_revenue(model, basis)
        show_table(frame, formats)
        january_revenue = calculate_revenue(model.assets(basis), "jan_amount")
        march_revenue = calculate_revenue(model.assets(basis), "march_amount")
        baseline = calculate_baseline_revenue(model.assets(basis))
        st.markdown(
            f"<div class='note'>January scenario revenue {fmt_cr(january_revenue['total'], 1)} · "
            f"March scenario revenue {fmt_cr(march_revenue['total'], 1)} · baseline "
            f"{fmt_cr(baseline['total'], 1)} · incremental "
            f"{fmt_cr_signed(march_revenue['total'] - baseline['total'], 1)}.</div>",
            unsafe_allow_html=True,
        )


def render_revenue_detail(model: ScenarioModel, basis: str, bundle: Dict[str, Any]) -> None:
    section("Revenue by Asset Class")
    frame, formats = build_revenue_impact(model, basis)
    show_table(frame, formats)

    incremental = bundle["incremental"]
    parts = " + ".join(
        f"{asset} {fmt_cr_signed(incremental['by_asset'][asset], 1)}" for asset in ASSETS
    )
    contribution = " · ".join(
        f"{asset} {fmt_pct(incremental['contribution'][asset])}" for asset in ASSETS
    )
    callout(
        f"<b>Revenue bridge:</b> current run-rate revenue {fmt_cr(bundle['baseline']['total'], 1)} "
        f"+ {parts} = scenario revenue {fmt_cr(bundle['scenario']['total'], 1)}.<br>"
        f"<b>Scenario revenue contribution:</b> {contribution}."
    )


def render_export(model: ScenarioModel, basis: str) -> None:
    section("Export")
    try:
        payload = make_export_excel(model, basis)
    except Exception:  # pragma: no cover - defensive
        st.warning("The export could not be generated for the current selection.")
        return
    st.download_button(
        "Download Selected Scenario Analysis",
        data=payload,
        file_name=f"scenario_{model.scenario_id}_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.markdown(
        "<div class='note'>The workbook contains the scenario guide, baseline, comparison, revenue "
        "impact, Retail-DHNI summary, Gross and Net Sales breakdowns, Scenario 6 segment analysis, "
        "Scenario 7 momentum analysis and Scenario 7 monthly revenue.</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# 16. APPLICATION ENTRY POINT
# =============================================================================

def render_dashboard(records: pd.DataFrame) -> None:
    scenario_id, params, basis, mapping = render_sidebar(records)
    records = map_business_segments(records, mapping)
    segment_counts = segment_diagnostics(records)
    grid = build_base_grid(records)
    model = ScenarioModel(scenario_id, grid, params)

    st.markdown(f"<div class='app-title'>{APP_TITLE}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='app-sub'>{APP_SUBTITLE}</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-rule'></div>", unsafe_allow_html=True)

    render_baseline(model)
    render_comparison(model, basis)
    bundle = render_revenue_kpis(model, basis)
    render_detail_expander(model)

    render_vertical_section(model)
    render_asset_section(model)

    if scenario_id == 6:
        render_segment_section(model, basis, segment_counts)
    if scenario_id == 7:
        render_momentum_section(model, basis)

    render_revenue_detail(model, basis, bundle)
    render_export(model, basis)


def reset_workbook() -> None:
    for key in ("workbook", "segment_mapping", "application_view"):
        st.session_state.pop(key, None)
    rerun()


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE, page_icon="▮", layout="wide", initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if "workbook" not in st.session_state:
        render_upload_screen()
        return

    try:
        records = load_workbook(st.session_state["workbook"])
    except WorkbookError as error:
        st.error(str(error))
        if st.button("Use another workbook"):
            reset_workbook()
        return
    except Exception:  # never surface a raw traceback to management
        st.error(
            "The workbook could not be read. Please upload the standard RM scorecard workbook "
            "containing the RM Retail Sales and RM DHNI sheets."
        )
        if st.button("Use another workbook"):
            reset_workbook()
        return

    st.sidebar.markdown(
        "<div class='sidebar-title'>Application View</div>",
        unsafe_allow_html=True,
    )
    application_view = st.sidebar.radio(
        "Application View",
        ["Scenario Planner", "FINAL Dashboard"],
        key="application_view",
        label_visibility="collapsed",
    )
    st.sidebar.markdown("<div class='app-rule'></div>", unsafe_allow_html=True)

    if application_view == "FINAL Dashboard":
        try:
            render_final_dashboard(st.session_state["workbook"])
        except Exception:  # never surface a raw traceback to management
            st.error(
                "The FINAL dashboard could not be prepared from the uploaded workbook. "
                "Please confirm that the workbook contains a sheet named 'FINAL'."
            )
        if st.sidebar.button("Use another workbook", key="final_use_another_workbook"):
            reset_workbook()
        return

    try:
        render_dashboard(records)
    except Exception:  # never surface a raw traceback to management
        st.error(
            "This view could not be prepared from the uploaded workbook. Please select another "
            "scenario, or upload a workbook that matches the standard RM scorecard format."
        )


if __name__ == "__main__":
    main()
