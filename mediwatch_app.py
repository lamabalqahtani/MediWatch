

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from pathlib import Path
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu

# ==========================================
# 1. PAGE CONFIGURATION & LOCALIZATION
# ==========================================
st.set_page_config(
    page_title="MediWatch | ICU Command Center",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "acknowledged_patients" not in st.session_state:
    st.session_state.acknowledged_patients = set()

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Patients"

# ==========================================
# 2. FUTURISTIC COMMAND CENTER CSS
# ==========================================
st.markdown("""
    <style>
    .main { background-color: #040814; }
    .stApp { background-color: #040814; color: #F8FAFC; }
    
    [data-testid="stSidebar"] {
        background-color: #070D1D;
        color: #F8FAFC;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border-color: #3B82F6 !important;
        border-radius: 8px;
    }
    [data-testid="stSidebar"] .stSelectbox svg {
        fill: #FFFFFF !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {
        color: #F8FAFC;
    }
    
    .icu-pod {
        background: linear-gradient(135deg, #0D1B2A 0%, #1B263B 100%);
        border: 1px solid #284B63;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .pod-normal { border-left: 5px solid #10B981; }
    .pod-warning { border-left: 5px solid #F59E0B; }
    .pod-danger { border-left: 5px solid #EF4444; background: linear-gradient(135deg, #1A0F14 0%, #2D1519 100%); }
    .pod-acked { border-left: 5px solid #3B82F6; opacity: 0.85; }

    input, textarea {
        background-color: #0B132B !important;
        color: #FFFFFF !important;
        border-color: #1D3557 !important;
        border-radius: 8px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #0B132B;
        border-radius: 8px;
        color: #FFFFFF;
        padding: 10px 24px;
        border: 1px solid #1D3557;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        border-color: #3B82F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style='padding: 12px 0;'>
            <h2 style='margin:0; font-size: 24px; font-weight: 700; color: #38BDF8;'>🩺 MediWatch</h2>
            <p style='margin:0; font-size: 13px; opacity: 0.8; color: #94A3B8;'>نظام القيادة والسيطرة للعناية المركزة</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    lang = st.selectbox("🌐 Language / اللغة", ["العربية", "English"])
    st.divider()

# ==========================================
# 3. LOCALIZATION DICTIONARY
# ==========================================
if lang == "العربية":
    txt = {
        "title": "🏥 لوحة قيادة العناية المركزة الحية",
        "caption": "متابعة مركزة لأسرّة المرضى مع التحديث اللحظي للعلامات الحيوية ونظام الإنذار المبكر.",
        "total_p": "إجمالي الأسرة",
        "norm_p": "🟢 مستقر",
        "acked_p": "🔵 تم التدخل",
        "low_p": "🟡 تحت الملاحظة",
        "high_p": "🔴 حالات حرجة",
        "search": "🔍 بحث سريع برقم السرير أو معرّف المريض (مثال: Bed-01 أو P0001):",
        "tab_all": "جميع الأسرة",
        "tab_danger": "🔴 الحالات الحرجة",
        "tab_warning": "🟡 تحت الملاحظة",
        "tab_acked": "🔵 تم التعامل",
        "alerts_title": "🚨 مركز الإنذار المبكر والتدخل السريع",
        "alerts_caption": "متابعة فورية للتنبيهات الحرجة.",
        "no_alerts": "✨ ممتاز! جميع المؤشرات ضمن النطاق الآمن.",
        "trends_title": "📈 لوحة التحليل العميق والمؤشرات",
        "trends_caption": "استعراض تفصيلي لتطور العلامات الحيوية للمريض.",
        "history_title": "🕒 السجلات والتقارير التاريخية",
        "history_caption": "الأرشيف الكامل للقراءات التاريخية.",
        "ack_btn": "✅ اعتماد التدخل الطبي",
        "reset_ack": "🔄 إعادة تعيين الأرشيف (إظهار التنبيهات مجدداً)",
        "search_hist": "🔍 بحث في السجل:",
        "select_patient": "اختر المريض للتحليل:"
    }
else:
    txt = {
        "title": "🏥 Live ICU Command Center",
        "caption": "Focused patient bed monitoring with real-time vital signs and early warning system.",
        "total_p": "Total Beds",
        "norm_p": "🟢 Stable",
        "acked_p": "🔵 Intervened",
        "low_p": "🟡 Observation",
        "high_p": "🔴 Critical",
        "search": "🔍 Quick search by Bed or Patient ID:",
        "tab_all": "All Beds",
        "tab_danger": "🔴 Critical",
        "tab_warning": "🟡 Observation",
        "tab_acked": "🔵 Acknowledged",
        "alerts_title": "🚨 Early Warning & Rapid Response",
        "alerts_caption": "Immediate tracking of critical alerts.",
        "no_alerts": "✨ Excellent! All vitals are within safe ranges.",
        "trends_title": "📈 Advanced Analytics Dashboard",
        "trends_caption": "Detailed review of patient vital sign progression.",
        "history_title": "🕒 Clinical Archive & Reports",
        "history_caption": "Complete archive of historical readings.",
        "ack_btn": "✅ Acknowledge Intervention",
        "reset_ack": "🔄 Reset Archive",
        "search_hist": "🔍 Search history:",
        "select_patient": "Select patient for analysis:"
    }

# ==========================================
# 4. DATA LOADING
# ==========================================
@st.cache_data
def load_mediwatch_data():
    BASE_DIR = Path(__file__).resolve().parent
    CSV_PATH = BASE_DIR / "demo_readings.csv"
    df = pd.read_csv(CSV_PATH)
    selected_patients = (
        df["patient_id"]
        .drop_duplicates()
        .sample(n=min(45, df["patient_id"].nunique()), random_state=42)
    )
    df = df[df["patient_id"].isin(selected_patients)].copy()
    df = df.sort_values(["patient_id", "hour_from_admission"]).copy()
    return df

df_all = load_mediwatch_data()

unique_pids = df_all["patient_id"].unique()
bed_mapping = {p_id: f"Bed-{(i+1):02d}" for i, p_id in enumerate(unique_pids)}
df_all["bed_no"] = df_all["patient_id"].map(bed_mapping)
df_all["display_id"] = df_all["patient_id"].apply(lambda x: f"P{int(x):04d}" if str(x).isdigit() else f"P-{x}")
df_all["bp_combined"] = df_all["systolic_bp"].astype(str) + " / " + df_all["diastolic_bp"].astype(str)

# ==========================================
# 5. CLINICAL RULE ENGINE
# ==========================================
def evaluate_vitals(row):
    risk_levels = []
    reasons = []

    t = row["temperature_c"]
    if 38.5 <= t <= 39.5 or t < 35.0:
        risk_levels.append("Red")
        reasons.append(f"حرارة حرجة ({t}°C)")
    elif (37.5 <= t < 38.5) or (35.0 <= t < 36.0):
        risk_levels.append("Orange")
        reasons.append(f"ارتفاع/انخفاض طفيف بالحرارة ({t}°C)")

    hr = row["heart_rate"]
    if hr > 120 or hr < 50:
        risk_levels.append("Red")
        reasons.append(f"نبض قلب حرِج ({hr} bpm)")
    elif (110 <= hr <= 120) or (50 <= hr < 60):
        risk_levels.append("Orange")
        reasons.append(f"نبض قلب غير مستقر ({hr} bpm)")

    rr = row["respiratory_rate"]
    if rr > 25 or rr < 10:
        risk_levels.append("Red")
        reasons.append(f"معدل تنفس حرِج ({rr})")
    elif 21 <= rr <= 25:
        risk_levels.append("Orange")
        reasons.append(f"معدل تنفس مرتفع ({rr})")

    sbp = row["systolic_bp"]
    if sbp < 90:
        risk_levels.append("Red")
        reasons.append(f"ضغط دم انقباضي حرِج ({sbp})")
    elif sbp < 100:
        risk_levels.append("Orange")
        reasons.append(f"ضغط دم انقباضي منخفض ({sbp})")

    spo2 = row["spo2_pct"]
    if spo2 < 90:
        risk_levels.append("Red")
        reasons.append(f"تشبع الأكسجين حرِج ({spo2}%)")
    elif 90 <= spo2 <= 94:
        risk_levels.append("Orange")
        reasons.append(f"تشبع أكسجين منخفض ({spo2}%)")

    if "Red" in risk_levels:
        return pd.Series(["High Risk", ", ".join(reasons)])
    elif "Orange" in risk_levels:
        return pd.Series(["Low Risk", ", ".join(reasons)])
    else:
        return pd.Series(["Normal", "قراءات مستقرة وآمنة"])

# ==========================================
# 6. REAL-TIME CLOCK & NAVIGATION (FIXED STATE)
# ==========================================
available_hours = sorted(df_all["hour_from_admission"].unique())
if "sim_hour_idx" not in st.session_state:
    st.session_state.sim_hour_idx = 0

count = st_autorefresh(interval=60 * 1000, key="global_realtime_clock")
if count > 0 and "last_count" in st.session_state and count != st.session_state.last_count:
    st.session_state.sim_hour_idx = (st.session_state.sim_hour_idx + 1) % len(available_hours)
st.session_state.last_count = count

current_hour = available_hours[st.session_state.sim_hour_idx]

current_slice = df_all[df_all["hour_from_admission"] <= current_hour]
df_current = current_slice.sort_values("hour_from_admission").groupby("patient_id").tail(1).copy()
df_current[["Risk_Level", "Alert_Reason"]] = df_current.apply(evaluate_vitals, axis=1)
df_current["Original_Risk"] = df_current["Risk_Level"]

active_alerts_count = len(df_current[
    (df_current["Original_Risk"].isin(["High Risk", "Low Risk"])) & 
    (~df_current["patient_id"].isin(st.session_state.acknowledged_patients))
])

with st.sidebar:
    if lang == "العربية":
        page_options = ["Patients", "Alerts", "Trends", "History"]
        display_names = [
            "المرضى (Patients)", 
            f"التنبيهات (Alerts) ({active_alerts_count})" if active_alerts_count > 0 else "التنبيهات (Alerts)", 
            "المؤشرات (Trends)", 
            "السجل (History)"
        ]
    else:
        page_options = ["Patients", "Alerts", "Trends", "History"]
        display_names = [
            "Patients", 
            f"Alerts ({active_alerts_count})" if active_alerts_count > 0 else "Alerts", 
            "Trends", 
            "History"
        ]

    curr_selection = st.session_state.active_nav
    default_idx = page_options.index(curr_selection) if curr_selection in page_options else 0

    selected_display = option_menu(
        menu_title=None,
        options=display_names,
        icons=["people", "exclamation-triangle", "graph-up", "clock-history"],
        menu_icon="cast",
        default_index=default_idx,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#38BDF8", "font-size": "16px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0px",
                "color": "#F8FAFC",
                "--hover-color": "#1E293B",
            },
            "nav-link-selected": {"background-color": "#2563EB", "color": "white", "font-weight": "bold"},
        }
    )

    idx_selected = display_names.index(selected_display)
    current_page = page_options[idx_selected]
    st.session_state.active_nav = current_page  # تثبيت الصفحة الحالية في الذاكرة

# ==========================================
# 7. PAGE 1: 🖥️ Patients
# ==========================================
if current_page == "Patients":
    st.markdown(f"""
        <div style='margin-bottom: 20px;'>
            <h1 style='margin:0; font-size: 28px; font-weight: 800; color: #F8FAFC;'>{txt['title']}</h1>
            <p style='margin:4px 0 0 0; color: #94A3B8; font-size: 14px;'>{txt['caption']}</p>
        </div>
    """, unsafe_allow_html=True)

    total_p = len(df_current)
    acked_p = len(df_current[df_current["patient_id"].isin(st.session_state.acknowledged_patients) & (df_current["Original_Risk"].isin(["High Risk", "Low Risk"]))])
    high_p = len(df_current[(df_current["Original_Risk"] == "High Risk") & (~df_current["patient_id"].isin(st.session_state.acknowledged_patients))])
    low_p = len(df_current[(df_current["Original_Risk"] == "Low Risk") & (~df_current["patient_id"].isin(st.session_state.acknowledged_patients))])
    norm_p = total_p - (high_p + low_p + acked_p)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric(txt["total_p"], f"{total_p}")
    m2.metric(txt["norm_p"], norm_p)
    m3.metric(txt["acked_p"], acked_p)
    m4.metric(txt["low_p"], low_p)
    m5.metric(txt["high_p"], high_p)

    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    search_q = st.text_input(txt["search"], "")

    view_df = df_current.sort_values("bed_no").copy()
    if search_q:
        view_df = view_df[
            view_df["display_id"].str.contains(search_q, case=False) | 
            view_df["bed_no"].str.contains(search_q, case=False)
        ]

    tab_all, tab_danger, tab_warning, tab_acked = st.tabs([
        txt["tab_all"], txt["tab_danger"], txt["tab_warning"], txt["tab_acked"]
    ])

    def render_icu_pods(subset_df):
        if subset_df.empty:
            st.info("لا توجد حالات ضمن هذه الفئة حالياً." if lang=="العربية" else "No cases found.")
            return
        cols = st.columns(3)
        for idx, row in subset_df.reset_index(drop=True).iterrows():
            is_acked = row["patient_id"] in st.session_state.acknowledged_patients

            if is_acked:
                pod_class = "pod-acked"
                badge = "🔵 تم التدخل" if lang=="العربية" else "🔵 Ack"
            elif row["Original_Risk"] == "High Risk":
                pod_class = "pod-danger"
                badge = "🔴 خطر حرِج" if lang=="العربية" else "🔴 Critical"
            elif row["Original_Risk"] == "Low Risk":
                pod_class = "pod-warning"
                badge = "🟡 ملاحظة" if lang=="العربية" else "🟡 Observation"
            else:
                pod_class = "pod-normal"
                badge = "🟢 مستقر" if lang=="العربية" else "🟢 Stable"
            
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="icu-pod {pod_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 16px; font-weight: 700; color: #38BDF8;">🛏️ {row['bed_no']}</span>
                        <span style="font-size: 12px; font-weight: bold; background: rgba(255,255,255,0.08); padding: 3px 10px; border-radius: 6px;">{row['display_id']} | {badge}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin: 6px 0; opacity: 0.9;">
                        <span>❤️ HR: <b>{row['heart_rate']} bpm</b></span>
                        <span>🩸 SpO₂: <b>{row['spo2_pct']}%</b></span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; margin: 6px 0; opacity: 0.9;">
                        <span>🫁 Resp: <b>{row['respiratory_rate']}</b></span>
                        <span>🌡️ Temp: <b>{row['temperature_c']}°C</b></span>
                    </div>
                    <div style="font-size: 13px; margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 6px; color: #94A3B8;">
                        BP: <b style="color: #F8FAFC;">{row['systolic_bp']}/{row['diastolic_bp']} mmHg</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_all:
        render_icu_pods(view_df)
    with tab_danger:
        render_icu_pods(view_df[(view_df["Original_Risk"] == "High Risk") & (~view_df["patient_id"].isin(st.session_state.acknowledged_patients))])
    with tab_warning:
        render_icu_pods(view_df[(view_df["Original_Risk"] == "Low Risk") & (~view_df["patient_id"].isin(st.session_state.acknowledged_patients))])
    with tab_acked:
        render_icu_pods(view_df[view_df["patient_id"].isin(st.session_state.acknowledged_patients) & (view_df["Original_Risk"].isin(["High Risk", "Low Risk"]))])

# ==========================================
# 8. PAGE 2: 🚨 Alerts
# ==========================================
elif current_page == "Alerts":
    st.title(txt["alerts_title"])
    st.caption(txt["alerts_caption"])

    active_alerts = df_current[
        (df_current["Original_Risk"].isin(["High Risk", "Low Risk"])) & 
        (~df_current["patient_id"].isin(st.session_state.acknowledged_patients))
    ]

    if active_alerts.empty:
        st.success(txt["no_alerts"])
    else:
        for _, row in active_alerts.iterrows():
            card_style = "pod-danger" if row["Original_Risk"] == "High Risk" else "pod-warning"
            level_text = "🔴 حرِج جداً (High Risk)" if row["Original_Risk"] == "High Risk" else "🟡 تحت الملاحظة (Low Risk)"
            
            with st.container():
                st.markdown(f"""
                <div class="icu-pod {card_style}">
                    <h3 style="margin:0 0 8px 0; color: #F8FAFC;">{level_text} — السرير {row['bed_no']} ({row['display_id']})</h3>
                    <p style="margin:4px 0;"><b>السبب / Reason:</b> {row['Alert_Reason']}</p>
                    <small style="color: #94A3B8;">HR: {row['heart_rate']} | SpO2: {row['spo2_pct']}% | Temp: {row['temperature_c']}°C | BP: {row['systolic_bp']}/{row['diastolic_bp']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"{txt['ack_btn']} ({row['bed_no']})", key=f"ack_{row['patient_id']}"):
                    st.session_state.acknowledged_patients.add(row["patient_id"])
                    st.rerun()
                st.write("---")

    if st.session_state.acknowledged_patients:
        if st.button(txt["reset_ack"]):
            st.session_state.acknowledged_patients.clear()
            st.rerun()

# ==========================================
# 9. PAGE 3: 📈 Trends
# ==========================================
elif current_page == "Trends":
    st.title(txt["trends_title"])
    st.caption(txt["trends_caption"])

    selected_pid = st.selectbox(
        txt["select_patient"],
        df_all["patient_id"].unique(),
        format_func=lambda x: f"Patient P{int(x):04d}" if str(x).isdigit() else f"Patient {x}"
    )

    p_data = df_all[(df_all["patient_id"] == selected_pid) & (df_all["hour_from_admission"] <= current_hour)].copy()

    if p_data.empty:
        st.warning("لا توجد بيانات كافية.")
    else:
        p_data[["Risk_Level", "Alert_Reason"]] = p_data.apply(evaluate_vitals, axis=1)
        latest = p_data.iloc[-1]
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("العمر / Age", f"{latest['age']}")
        col_b.metric("السرير / Bed", f"{latest['bed_no']}")
        col_c.metric("الحالة / Status", latest['Risk_Level'])

        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            fig_hr = px.line(p_data, x="hour_from_admission", y="heart_rate", markers=True, title="Heart Rate Trend (HR)", template="plotly_dark")
            st.plotly_chart(fig_hr, use_container_width=True)
            
            fig_temp = px.line(p_data, x="hour_from_admission", y="temperature_c", markers=True, title="Temperature Trend (°C)", template="plotly_dark")
            st.plotly_chart(fig_temp, use_container_width=True)

        with c2:
            fig_spo2 = px.line(p_data, x="hour_from_admission", y="spo2_pct", markers=True, title="Oxygen Saturation (SpO₂)", template="plotly_dark")
            st.plotly_chart(fig_spo2, use_container_width=True)
            
            fig_bp = px.line(p_data, x="hour_from_admission", y=["systolic_bp", "diastolic_bp"], markers=True, title="Blood Pressure Trend (BP)", template="plotly_dark")
            st.plotly_chart(fig_bp, use_container_width=True)

# ==========================================
# 10. PAGE 4: 🕒 History
# ==========================================
elif current_page == "History":
    st.title(txt["history_title"])
    st.caption(txt["history_caption"])

    search_h = st.text_input(txt["search_hist"], "")
    hist_df = df_all[df_all["hour_from_admission"] <= current_hour].copy()
    
    if search_h:
        hist_df = hist_df[
            hist_df["display_id"].str.contains(search_h, case=False) | 
            hist_df["bed_no"].str.contains(search_h, case=False)
        ]

    display_history = hist_df[[
        "display_id", "bed_no", "hour_from_admission", 
        "heart_rate", "spo2_pct", "respiratory_rate", 
        "temperature_c", "bp_combined"
    ]].copy()

    if lang == "العربية":
        display_history.columns = [
            "معرّف المريض", "رقم السرير", "ساعة التنويم", 
            "نبض القلب (HR)", "الأكسجين (SpO₂ %)", "معدل التنفس", 
            "درجة الحرارة (°C)", "ضغط الدم (BP)"
        ]
    else:
        display_history.columns = [
            "Patient ID", "Bed No", "Admission Hour", 
            "Heart Rate (HR)", "SpO₂ (%)", "Respiratory Rate", 
            "Temperature (°C)", "Blood Pressure (BP)"
        ]

    st.dataframe(
        display_history.head(200), 
        use_container_width=True, 
        hide_index=True
    )

st.divider()
st.caption("MediWatch | Real-Time Clinical Rule-Based Monitoring | Command Center v3.1")