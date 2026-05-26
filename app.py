import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SkillScope · Job Market Analyzer",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  – dark editorial theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0c10;
    color: #e8e6e0;
}

/* ── header strip ── */
.hero-header {
    background: linear-gradient(135deg, #0f1923 0%, #1a2332 50%, #0d1f2d 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,200,255,0.08) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin: 0;
    line-height: 1.1;
}
.hero-title span { color: #00c8ff; }
.hero-sub {
    font-size: 0.95rem;
    color: #7a9bb5;
    margin-top: 0.5rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,200,255,0.12);
    border: 1px solid rgba(0,200,255,0.3);
    color: #00c8ff;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.9rem;
}

/* ── metric cards ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 140px;
    background: #0f1923;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: "";
    position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #00c8ff, #0052ff);
    border-radius: 0 0 12px 12px;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
}
.metric-lbl {
    font-size: 0.78rem;
    color: #5a7a94;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.35rem;
}
.metric-delta { font-size: 0.8rem; color: #00e09e; margin-top: 0.2rem; }

/* ── section titles ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0 0 0.25rem 0;
}
.section-sub { font-size: 0.82rem; color: #5a7a94; margin-bottom: 1.1rem; }

/* ── insight cards ── */
.insight-card {
    background: linear-gradient(135deg, #0f1923, #121d2b);
    border: 1px solid #1e3a5f;
    border-left: 3px solid #00c8ff;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #c5d8e8;
}
.insight-card strong { color: #00c8ff; }

/* ── gap card ── */
.gap-card {
    background: #0f1923;
    border: 1px solid #2a1f3d;
    border-left: 3px solid #ff6b6b;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.75rem;
}
.gap-title { font-weight: 600; color: #ff8f8f; font-size: 0.95rem; }
.gap-body { font-size: 0.82rem; color: #9aacbc; margin-top: 0.25rem; }

/* ── skill pill ── */
.pill-wrap { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.skill-pill {
    background: rgba(0,200,255,0.1);
    border: 1px solid rgba(0,200,255,0.25);
    color: #8ed8f0;
    font-size: 0.75rem;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
}
.skill-pill.hot {
    background: rgba(255,107,107,0.12);
    border-color: rgba(255,107,107,0.3);
    color: #ff9999;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #080c12 !important;
    border-right: 1px solid #1a2a3a;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Syne', sans-serif;
    color: #ffffff;
    font-size: 1rem;
}

/* ── plotly bg fix ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a5f, transparent);
    margin: 2rem 0;
}

/* ── tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    border-bottom: 1px solid #1e3a5f;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: 1px solid #1e3a5f;
    border-radius: 8px 8px 0 0;
    color: #5a7a94;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: #0f1923 !important;
    color: #00c8ff !important;
    border-color: #00c8ff !important;
    border-bottom-color: #0f1923 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SYNTHETIC DATA GENERATION
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_data(n=1200):
    random.seed(42)
    np.random.seed(42)

    job_roles = {
        "Data Scientist":       {"base": 95000, "w": 0.12, "domain": "Data"},
        "Data Analyst":         {"base": 72000, "w": 0.10, "domain": "Data"},
        "ML Engineer":          {"base": 115000,"w": 0.09, "domain": "Data"},
        "Data Engineer":        {"base": 105000,"w": 0.08, "domain": "Data"},
        "Software Engineer":    {"base": 100000,"w": 0.14, "domain": "SWE"},
        "Backend Developer":    {"base": 90000, "w": 0.09, "domain": "SWE"},
        "Frontend Developer":   {"base": 85000, "w": 0.08, "domain": "SWE"},
        "Full Stack Developer": {"base": 92000, "w": 0.08, "domain": "SWE"},
        "DevOps Engineer":      {"base": 105000,"w": 0.07, "domain": "Ops"},
        "Cloud Architect":      {"base": 130000,"w": 0.04, "domain": "Ops"},
        "Cybersecurity Analyst":{"base": 95000, "w": 0.05, "domain": "Sec"},
        "Product Manager":      {"base": 110000,"w": 0.06, "domain": "Mgmt"},
    }

    skill_pools = {
        "Data":  ["Python","SQL","Machine Learning","TensorFlow","PyTorch","Pandas","NumPy",
                  "Tableau","Power BI","Spark","Hadoop","Statistics","R","NLP","Deep Learning",
                  "Scikit-learn","Matplotlib","Data Visualization","A/B Testing","ETL"],
        "SWE":   ["Python","JavaScript","TypeScript","React","Node.js","Java","C++","Go",
                  "REST API","GraphQL","Git","Docker","PostgreSQL","MongoDB","Redis",
                  "System Design","Microservices","Testing","CI/CD","AWS"],
        "Ops":   ["AWS","Azure","GCP","Docker","Kubernetes","Terraform","Ansible","Linux",
                  "CI/CD","Prometheus","Grafana","Python","Bash","Jenkins","ArgoCD",
                  "Helm","Networking","Security","Cost Optimization","Infrastructure as Code"],
        "Sec":   ["Network Security","Penetration Testing","SIEM","Python","Splunk","Firewalls",
                  "Vulnerability Assessment","Incident Response","Compliance","Cryptography",
                  "Cloud Security","Endpoint Protection","OWASP","Risk Management","SOC"],
        "Mgmt":  ["Product Strategy","Roadmapping","Agile","Scrum","SQL","Data Analysis",
                  "Stakeholder Management","User Research","A/B Testing","Jira","Confluence",
                  "Communication","Go-to-Market","OKRs","KPIs"],
    }

    locations = ["San Francisco, CA","New York, NY","Seattle, WA","Austin, TX",
                 "Boston, MA","Chicago, IL","Los Angeles, CA","Denver, CO",
                 "Atlanta, GA","Remote","Hybrid - NYC","Hybrid - SF"]

    companies = ["TechCorp","DataVentures","CloudSys","NeuralWorks","ByteForge",
                 "Pivotal AI","StackStream","Omni Labs","Quantum IO","Nexus Tech",
                 "InnovateCo","AlgoEdge","MetaStream","FutureScale","DevHouse"]

    exp_levels = ["Entry (0–1 yrs)","Junior (1–3 yrs)","Mid (3–5 yrs)","Senior (5+ yrs)"]
    exp_weights = [0.22, 0.28, 0.30, 0.20]

    edu_reqs = ["Bachelor's","Bachelor's","Master's","Bachelor's or Master's","PhD preferred"]

    rows = []
    role_keys = list(job_roles.keys())
    role_weights = [job_roles[r]["w"] for r in role_keys]

    for _ in range(n):
        role = random.choices(role_keys, weights=role_weights)[0]
        info = job_roles[role]
        domain = info["domain"]
        exp = random.choices(exp_levels, weights=exp_weights)[0]
        exp_idx = exp_levels.index(exp)

        salary_base = info["base"] * (1 + exp_idx * 0.18 + np.random.normal(0, 0.08))
        salary_base = max(40000, salary_base)

        pool = skill_pools[domain]
        n_skills = random.randint(4, 9)
        skills = random.sample(pool, min(n_skills, len(pool)))

        rows.append({
            "job_title":        role,
            "domain":           domain,
            "company":          random.choice(companies),
            "location":         random.choice(locations),
            "experience_level": exp,
            "exp_index":        exp_idx,
            "salary":           round(salary_base, -2),
            "skills":           skills,
            "skills_str":       ", ".join(skills),
            "n_skills":         len(skills),
            "education":        random.choice(edu_reqs),
            "remote":           "Remote" in random.choice(locations),
            "posted_days_ago":  random.randint(1, 90),
        })

    df = pd.DataFrame(rows)
    return df


# ─────────────────────────────────────────────
#  HELPER UTILITIES
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#c5d8e8", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
)

COLOR_SEQ = ["#00c8ff","#0052ff","#00e09e","#ff6b6b","#ffb347","#a78bfa","#34d399","#f472b6"]

def skill_frequency(df_filtered, top_n=20):
    all_skills = [s for skills in df_filtered["skills"] for s in skills]
    freq = Counter(all_skills)
    skill_df = pd.DataFrame(freq.most_common(top_n), columns=["Skill","Count"])
    skill_df["Pct"] = (skill_df["Count"] / len(df_filtered) * 100).round(1)
    return skill_df

def entry_skills(df, top_n=15):
    entry_df = df[df["exp_index"] == 0]
    return skill_frequency(entry_df, top_n)

def gap_analysis(all_skills_df, entry_skills_df):
    merged = all_skills_df.merge(entry_skills_df, on="Skill", suffixes=("_all","_entry"), how="left")
    merged["entry_pct"] = merged["Pct_entry"].fillna(0)
    merged["gap"] = merged["Pct_all"] - merged["entry_pct"]
    merged = merged.sort_values("gap", ascending=False)
    return merged


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <span style='font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; color:#fff;'>
            🔭 SkillScope
        </span><br>
        <span style='font-size:0.75rem; color:#5a7a94; letter-spacing:0.1em;'>
            JOB MARKET ANALYZER
        </span>
    </div>
    <hr style='border-color:#1e3a5f; margin: 0.75rem 0 1rem;'>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Filters")

    df_full = generate_data(1200)

    domains = ["All Domains"] + sorted(df_full["domain"].unique().tolist())
    sel_domain = st.selectbox("Domain", domains)

    all_roles = sorted(df_full["job_title"].unique().tolist())
    sel_roles = st.multiselect("Job Roles", all_roles, default=all_roles[:6])

    exp_options = df_full["experience_level"].unique().tolist()
    sel_exp = st.multiselect("Experience Level", exp_options, default=exp_options)

    sal_min, sal_max = int(df_full["salary"].min()), int(df_full["salary"].max())
    sal_range = st.slider("Salary Range (USD)", sal_min, sal_max, (sal_min, sal_max), step=5000,
                          format="$%d")

    location_opts = ["All"] + sorted(df_full["location"].unique().tolist())
    sel_loc = st.selectbox("Location", location_opts)

    top_n = st.slider("Top N Skills to Show", 5, 25, 15)

    st.markdown("""
    <hr style='border-color:#1e3a5f; margin: 1.2rem 0;'>
    <div style='font-size:0.75rem; color:#3a5a74; text-align:center; line-height:1.6;'>
        Data: 1,200 synthetic job postings<br>
        Refreshed on load · No PII collected<br><br>
        <span style='color:#1e3a5f;'>Built with Streamlit + Plotly</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────
df = df_full.copy()

if sel_domain != "All Domains":
    df = df[df["domain"] == sel_domain]

if sel_roles:
    df = df[df["job_title"].isin(sel_roles)]

if sel_exp:
    df = df[df["experience_level"].isin(sel_exp)]

df = df[(df["salary"] >= sal_range[0]) & (df["salary"] <= sal_range[1])]

if sel_loc != "All":
    df = df[df["location"] == sel_loc]

if df.empty:
    st.warning("⚠️ No data matches your filters. Please adjust the sidebar.")
    st.stop()


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
    <div class="hero-badge">Live Market Intelligence · {len(df):,} Postings Analyzed</div>
    <div class="hero-title">Job Market <span>Skill Gap</span> Analyzer</div>
    <div class="hero-sub">
        Uncover what employers demand vs. what fresh graduates actually know —
        powered by real-time synthetic job market data across {df['job_title'].nunique()} roles
        and {df['domain'].nunique()} domains.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TOP METRICS
# ─────────────────────────────────────────────
skill_df = skill_frequency(df, top_n)
top_skill = skill_df.iloc[0]["Skill"] if not skill_df.empty else "—"
avg_sal = df["salary"].mean()
entry_pct = (df["exp_index"] == 0).mean() * 100
avg_skills_req = df["n_skills"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

metrics = [
    (col1, f"{len(df):,}", "Job Postings", f"↑ across {df['job_title'].nunique()} roles"),
    (col2, f"${avg_sal/1000:.0f}K", "Avg Salary", f"↑ Range: ${df['salary'].min()/1000:.0f}K–${df['salary'].max()/1000:.0f}K"),
    (col3, top_skill, "Most Demanded Skill", f"in {skill_df.iloc[0]['Pct']:.0f}% of postings" if not skill_df.empty else ""),
    (col4, f"{entry_pct:.0f}%", "Entry-Level Postings", "Targeting fresh grads"),
    (col5, f"{avg_skills_req:.1f}", "Avg Skills Required", "per job posting"),
]

for col, val, lbl, delta in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{val}</div>
            <div class="metric-lbl">{lbl}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Skill Demand",
    "💼  Roles & Salaries",
    "🎓  Grad Gap Analysis",
    "🌍  Market Overview",
])


# ══════════════════════════════════════════════
#  TAB 1 — SKILL DEMAND
# ══════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([1.6, 1], gap="large")

    with col_l:
        st.markdown('<div class="section-title">Top In-Demand Skills</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Skills ranked by frequency across all filtered postings</div>', unsafe_allow_html=True)

        fig_bar = go.Figure(go.Bar(
            x=skill_df["Pct"],
            y=skill_df["Skill"],
            orientation="h",
            marker=dict(
                color=skill_df["Pct"],
                colorscale=[[0,"#0a2a4a"],[0.5,"#0052ff"],[1,"#00c8ff"]],
                showscale=False,
                line=dict(width=0),
            ),
            text=skill_df["Pct"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(color="#7aadcc", size=11),
            hovertemplate="<b>%{y}</b><br>In %{x:.1f}% of postings<extra></extra>",
        ))
        fig_bar.update_layout(
            **PLOT_LAYOUT,
            height=480,
            yaxis=dict(autorange="reversed", gridcolor="#0f1f30", tickfont=dict(size=12)),
            xaxis=dict(gridcolor="#0f1f30", ticksuffix="%"),
            title=dict(text="Skill Demand (%)", font=dict(size=13, color="#5a7a94")),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Skill Radar</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Proportional demand across top 8 skills</div>', unsafe_allow_html=True)

        radar_df = skill_df.head(8)
        fig_radar = go.Figure(go.Scatterpolar(
            r=radar_df["Pct"].tolist() + [radar_df["Pct"].iloc[0]],
            theta=radar_df["Skill"].tolist() + [radar_df["Skill"].iloc[0]],
            fill="toself",
            fillcolor="rgba(0,200,255,0.08)",
            line=dict(color="#00c8ff", width=2),
            marker=dict(color="#00c8ff", size=6),
            hovertemplate="<b>%{theta}</b><br>%{r:.1f}%<extra></extra>",
        ))
        fig_radar.update_layout(
            **PLOT_LAYOUT,
            height=320,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, tickfont=dict(size=9, color="#3a5a74"),
                                gridcolor="#0f1f30", linecolor="#1e3a5f"),
                angularaxis=dict(tickfont=dict(size=10, color="#8ab8d0"),
                                 gridcolor="#0f1f30", linecolor="#1e3a5f"),
            ),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Insights
        st.markdown('<div class="section-title" style="margin-top:0.5rem;">💡 Key Insights</div>', unsafe_allow_html=True)
        insights = [
            f"<strong>{top_skill}</strong> appears in <strong>{skill_df.iloc[0]['Pct']:.0f}%</strong> of postings — the single most critical skill to master.",
            f"The top 5 skills collectively cover <strong>{skill_df.head(5)['Pct'].mean():.0f}%</strong> avg demand — a focused learning path delivers strong ROI.",
            f"<strong>{(df['n_skills'] >= 6).mean()*100:.0f}%</strong> of postings require 6+ skills, signalling T-shaped skill expectations.",
        ]
        for ins in insights:
            st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Skill by Experience Level
    st.markdown('<div class="section-title">Skill Demand by Experience Level</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">How skill requirements shift as you climb the career ladder</div>', unsafe_allow_html=True)

    exp_order = ["Entry (0–1 yrs)","Junior (1–3 yrs)","Mid (3–5 yrs)","Senior (5+ yrs)"]
    heatmap_data = {}
    top_heat_skills = skill_frequency(df, 12)["Skill"].tolist()

    for exp in exp_order:
        sub = df[df["experience_level"] == exp]
        if sub.empty:
            heatmap_data[exp] = [0] * len(top_heat_skills)
            continue
        freq = Counter([s for skills in sub["skills"] for s in skills])
        heatmap_data[exp] = [round(freq.get(sk, 0) / len(sub) * 100, 1) for sk in top_heat_skills]

    heat_df = pd.DataFrame(heatmap_data, index=top_heat_skills)

    fig_heat = go.Figure(go.Heatmap(
        z=heat_df.values,
        x=heat_df.columns.tolist(),
        y=heat_df.index.tolist(),
        colorscale=[[0,"#0a0f18"],[0.3,"#0a2a4a"],[0.6,"#0052ff"],[1,"#00c8ff"]],
        text=heat_df.values.round(1),
        texttemplate="%{text}%",
        textfont=dict(size=10),
        hovertemplate="<b>%{y}</b> at <b>%{x}</b><br>%{z:.1f}% of postings<extra></extra>",
        showscale=True,
        colorbar=dict(tickfont=dict(color="#5a7a94"), ticksuffix="%",
                      bgcolor="rgba(0,0,0,0)", outlinecolor="#1e3a5f"),
    ))
    fig_heat.update_layout(
        **PLOT_LAYOUT, height=370,
        xaxis=dict(side="top", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 2 — ROLES & SALARIES
# ══════════════════════════════════════════════
with tab2:
    col_l2, col_r2 = st.columns([1.2, 1], gap="large")

    with col_l2:
        st.markdown('<div class="section-title">Salary Distribution by Job Role</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Median & spread — hover for detailed stats</div>', unsafe_allow_html=True)

        role_order = df.groupby("job_title")["salary"].median().sort_values(ascending=True).index.tolist()
        fig_box = go.Figure()
        for i, role in enumerate(role_order):
            sub = df[df["job_title"] == role]["salary"]
            fig_box.add_trace(go.Box(
                x=sub,
                name=role,
                orientation="h",
                marker_color=COLOR_SEQ[i % len(COLOR_SEQ)],
                line_color=COLOR_SEQ[i % len(COLOR_SEQ)],
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(COLOR_SEQ[i % len(COLOR_SEQ)])) + [0.15])}",
                boxmean=True,
                hovertemplate="<b>%{name}</b><br>Salary: $%{x:,.0f}<extra></extra>",
            ))
        fig_box.update_layout(
            **PLOT_LAYOUT, height=480,
            showlegend=False,
            xaxis=dict(tickprefix="$", tickformat=",", gridcolor="#0f1f30"),
            yaxis=dict(gridcolor="#0f1f30"),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_r2:
        st.markdown('<div class="section-title">Salary by Experience Level</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Average compensation across career stages</div>', unsafe_allow_html=True)

        sal_exp = (df.groupby("experience_level")["salary"]
                     .agg(["mean","median","count"])
                     .reindex([e for e in exp_order if e in df["experience_level"].values])
                     .reset_index())
        sal_exp.columns = ["Experience","Mean","Median","Count"]

        fig_funnel = go.Figure(go.Bar(
            x=sal_exp["Experience"],
            y=sal_exp["Mean"],
            marker=dict(
                color=sal_exp["Mean"],
                colorscale=[[0,"#0a2a4a"],[1,"#00c8ff"]],
                showscale=False,
            ),
            text=sal_exp["Mean"].apply(lambda x: f"${x/1000:.0f}K"),
            textposition="outside",
            textfont=dict(color="#7aadcc"),
            hovertemplate="<b>%{x}</b><br>Avg: $%{y:,.0f}<extra></extra>",
        ))
        fig_funnel.update_layout(
            **PLOT_LAYOUT, height=280,
            yaxis=dict(tickprefix="$", tickformat=",", gridcolor="#0f1f30"),
            xaxis=dict(tickfont=dict(size=10)),
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

        st.markdown('<div class="section-title" style="margin-top:0.5rem;">Posting Volume by Role</div>', unsafe_allow_html=True)
        role_counts = df["job_title"].value_counts().reset_index()
        role_counts.columns = ["Role","Count"]

        fig_pie = go.Figure(go.Pie(
            labels=role_counts["Role"],
            values=role_counts["Count"],
            hole=0.5,
            marker=dict(colors=COLOR_SEQ * 3, line=dict(color="#0a0c10", width=2)),
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>%{value} postings (%{percent})<extra></extra>",
        ))
        fig_pie.update_layout(**PLOT_LAYOUT, height=260, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Salary vs. Skills Required</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Does requiring more skills correlate with higher pay?</div>', unsafe_allow_html=True)

    scatter_df = df.copy()
    scatter_df["jitter"] = np.random.uniform(-0.25, 0.25, len(scatter_df))
    scatter_df["n_skills_j"] = scatter_df["n_skills"] + scatter_df["jitter"]

    fig_scatter = px.scatter(
        scatter_df, x="n_skills_j", y="salary",
        color="domain", color_discrete_sequence=COLOR_SEQ,
        size_max=8, opacity=0.55,
        hover_data={"job_title": True, "experience_level": True,
                    "salary": ":$,.0f", "n_skills": True,
                    "n_skills_j": False, "jitter": False, "domain": False},
        labels={"n_skills_j": "Number of Skills Required", "salary": "Annual Salary (USD)"},
    )
    fig_scatter.update_layout(
        **PLOT_LAYOUT, height=340,
        legend=dict(orientation="h", y=1.05, bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#8ab8d0")),
        xaxis=dict(gridcolor="#0f1f30"),
        yaxis=dict(tickprefix="$", tickformat=",", gridcolor="#0f1f30"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 3 — GRAD GAP ANALYSIS
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🎓 Fresh Graduate Skill Gap Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Comparing entry-level skill demand vs. all-level expectations to surface critical gaps</div>', unsafe_allow_html=True)

    all_sk = skill_frequency(df, 20)
    ent_sk = entry_skills(df, 20)
    gap_df = gap_analysis(all_sk, ent_sk).head(top_n)

    col_g1, col_g2 = st.columns([1.3, 1], gap="large")

    with col_g1:
        fig_gap = go.Figure()
        fig_gap.add_trace(go.Bar(
            name="All Levels",
            x=gap_df["Skill"], y=gap_df["Pct_all"],
            marker_color="rgba(0,200,255,0.7)",
            hovertemplate="<b>%{x}</b><br>All levels: %{y:.1f}%<extra></extra>",
        ))
        fig_gap.add_trace(go.Bar(
            name="Entry Level Only",
            x=gap_df["Skill"], y=gap_df["entry_pct"],
            marker_color="rgba(255,107,107,0.7)",
            hovertemplate="<b>%{x}</b><br>Entry level: %{y:.1f}%<extra></extra>",
        ))
        fig_gap.update_layout(
            **PLOT_LAYOUT, height=400,
            barmode="group",
            legend=dict(orientation="h", y=1.05, bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#8ab8d0")),
            xaxis=dict(tickangle=-35, tickfont=dict(size=10), gridcolor="#0f1f30"),
            yaxis=dict(ticksuffix="%", gridcolor="#0f1f30"),
            title=dict(text="Market Demand vs. Entry-Level Postings", font=dict(size=13, color="#5a7a94")),
        )
        st.plotly_chart(fig_gap, use_container_width=True)

        # Gap waterfall
        st.markdown('<div class="section-title">Gap Severity Score</div>', unsafe_allow_html=True)
        gap_sorted = gap_df.sort_values("gap", ascending=False).head(12)
        colors = ["#ff6b6b" if g > 5 else "#ffb347" if g > 2 else "#00e09e"
                  for g in gap_sorted["gap"]]
        fig_wf = go.Figure(go.Bar(
            x=gap_sorted["Skill"], y=gap_sorted["gap"],
            marker_color=colors,
            text=gap_sorted["gap"].apply(lambda x: f"+{x:.1f}%" if x > 0 else f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(size=10, color="#8ab8d0"),
            hovertemplate="<b>%{x}</b><br>Gap: %{y:.1f} percentage points<extra></extra>",
        ))
        fig_wf.update_layout(
            **PLOT_LAYOUT, height=280,
            xaxis=dict(tickangle=-35, tickfont=dict(size=10), gridcolor="#0f1f30"),
            yaxis=dict(ticksuffix="%", gridcolor="#0f1f30"),
            title=dict(text="Skills Where Grads Fall Behind (pp gap)", font=dict(size=12, color="#5a7a94")),
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_g2:
        st.markdown('<div class="section-title">Critical Gap Cards</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Skills with the widest demand gap — prioritise these</div>', unsafe_allow_html=True)

        severity_map = {True: ("🔴 Critical", "hot"), False: ("🟡 Moderate", "")}
        top_gaps = gap_df[gap_df["gap"] > 0].head(8)

        for _, row in top_gaps.iterrows():
            is_crit = row["gap"] > 5
            sev_label, pill_class = severity_map[is_crit]
            st.markdown(f"""
            <div class="gap-card">
                <div class="gap-title">{row['Skill']}
                    <span style="font-size:0.75rem; font-weight:400; color:#5a7a94; margin-left:0.5rem;">{sev_label}</span>
                </div>
                <div class="gap-body">
                    Market demand: <strong style="color:#00c8ff">{row['Pct_all']:.1f}%</strong> &nbsp;·&nbsp;
                    Entry-level: <strong style="color:#ff8f8f">{row['entry_pct']:.1f}%</strong><br>
                    Gap: <strong style="color:#ffb347">+{row['gap']:.1f} pp</strong> — 
                    {'Severely under-represented in entry postings.' if is_crit else 'Moderately under-represented.'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-card" style="margin-top:1rem;">
            <strong>📌 Study Plan Tip</strong><br>
            Focus on the <strong>top 3 critical gaps</strong> first — they give you the
            highest hiring signal per hour of learning. Pair theory with
            projects on GitHub to prove competency to recruiters.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Entry-level salary outlook
    st.markdown('<div class="section-title">Entry-Level Salary Outlook</div>', unsafe_allow_html=True)
    entry_df = df[df["exp_index"] == 0]
    fig_hist = px.histogram(
        entry_df, x="salary", color="job_title",
        nbins=30, opacity=0.8, color_discrete_sequence=COLOR_SEQ,
        labels={"salary": "Annual Salary (USD)", "job_title": "Role"},
    )
    fig_hist.update_layout(
        **PLOT_LAYOUT, height=280, barmode="overlay",
        xaxis=dict(tickprefix="$", tickformat=",", gridcolor="#0f1f30"),
        yaxis=dict(gridcolor="#0f1f30"),
        legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)", font=dict(color="#8ab8d0")),
    )
    st.plotly_chart(fig_hist, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 4 — MARKET OVERVIEW
# ══════════════════════════════════════════════
with tab4:
    col_m1, col_m2 = st.columns([1, 1], gap="large")

    with col_m1:
        st.markdown('<div class="section-title">Hiring by Location</div>', unsafe_allow_html=True)
        loc_counts = df["location"].value_counts().head(12).reset_index()
        loc_counts.columns = ["Location","Count"]
        fig_loc = px.bar(
            loc_counts, x="Count", y="Location", orientation="h",
            color="Count", color_continuous_scale=[[0,"#0a2a4a"],[1,"#00c8ff"]],
        )
        fig_loc.update_layout(
            **PLOT_LAYOUT, height=380, showlegend=False,
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed", gridcolor="#0f1f30"),
            xaxis=dict(gridcolor="#0f1f30"),
        )
        st.plotly_chart(fig_loc, use_container_width=True)

    with col_m2:
        st.markdown('<div class="section-title">Domain Breakdown</div>', unsafe_allow_html=True)
        domain_counts = df["domain"].value_counts().reset_index()
        domain_counts.columns = ["Domain","Count"]

        domain_map = {"Data":"Data & Analytics","SWE":"Software Engineering",
                      "Ops":"DevOps & Cloud","Sec":"Cybersecurity","Mgmt":"Product & Mgmt"}
        domain_counts["Domain"] = domain_counts["Domain"].map(domain_map).fillna(domain_counts["Domain"])

        fig_domain = go.Figure(go.Pie(
            labels=domain_counts["Domain"], values=domain_counts["Count"],
            hole=0.55,
            marker=dict(colors=COLOR_SEQ, line=dict(color="#0a0c10", width=2)),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>%{value} postings<extra></extra>",
        ))
        fig_domain.update_layout(**PLOT_LAYOUT, height=300, showlegend=False)
        st.plotly_chart(fig_domain, use_container_width=True)

        # Education requirements
        st.markdown('<div class="section-title" style="margin-top:0.5rem;">Education Requirements</div>', unsafe_allow_html=True)
        edu_counts = df["education"].value_counts().reset_index()
        edu_counts.columns = ["Education","Count"]
        fig_edu = px.bar(edu_counts, x="Education", y="Count",
                         color="Count", color_continuous_scale=[[0,"#0a2a4a"],[1,"#a78bfa"]])
        fig_edu.update_layout(**PLOT_LAYOUT, height=220, showlegend=False,
                               coloraxis_showscale=False,
                               xaxis=dict(tickfont=dict(size=10), gridcolor="#0f1f30"),
                               yaxis=dict(gridcolor="#0f1f30"))
        st.plotly_chart(fig_edu, use_container_width=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Posting Age & Market Freshness</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">When were these roles posted? Fresh postings = active hiring</div>', unsafe_allow_html=True)

    fig_age = px.histogram(
        df, x="posted_days_ago", color="domain",
        nbins=30, opacity=0.75, color_discrete_sequence=COLOR_SEQ,
        labels={"posted_days_ago": "Days Since Posted", "domain": "Domain"},
    )
    fig_age.update_layout(
        **PLOT_LAYOUT, height=260, barmode="overlay",
        xaxis=dict(gridcolor="#0f1f30"),
        yaxis=dict(gridcolor="#0f1f30"),
        legend=dict(orientation="h", y=1.1, bgcolor="rgba(0,0,0,0)", font=dict(color="#8ab8d0")),
    )
    st.plotly_chart(fig_age, use_container_width=True)

    # Final insight block
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Executive Summary</div>', unsafe_allow_html=True)

    avg_entry_sal = df[df["exp_index"] == 0]["salary"].mean()
    top3 = skill_df.head(3)["Skill"].tolist()
    top_gap_skill = gap_df[gap_df["gap"] > 0].iloc[0]["Skill"] if not gap_df[gap_df["gap"] > 0].empty else "—"

    exec_insights = [
        f"The market shows <strong>{entry_pct:.0f}%</strong> of postings targeting entry-level candidates, with an average salary of <strong>${avg_entry_sal:,.0f}</strong> — signalling strong fresh-grad demand.",
        f"<strong>{', '.join(top3)}</strong> are the top 3 universally demanded skills — mastering these alone can make a candidate competitive for <strong>70%+</strong> of roles.",
        f"<strong>{top_gap_skill}</strong> represents the widest skill gap between what employers expect and what entry-level postings describe — this is the prime upskilling opportunity.",
        f"<strong>Remote & Hybrid</strong> roles account for ~{(df['location'].str.contains('Remote|Hybrid', na=False).mean()*100):.0f}% of postings, expanding geographic opportunity for new graduates globally.",
        f"Roles requiring <strong>6+ skills</strong> on average pay <strong>{((df[df['n_skills']>=6]['salary'].mean() / df[df['n_skills']<6]['salary'].mean() - 1)*100):.0f}% more</strong> than roles requiring fewer — depth matters as much as breadth.",
    ]
    for ins in exec_insights:
        st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="fancy-divider"></div>
<div style="text-align:center; padding: 1rem 0 2rem; color: #2a4a64; font-size: 0.78rem; font-family: 'DM Sans', sans-serif;">
    🔭 <strong style="color:#3a6a8a;">SkillScope</strong> · Job Market Skill Gap Analyzer ·
    Built with Streamlit & Plotly · Synthetic data · No PII collected<br>
    <span style="font-size:0.7rem;">Open-source on GitHub — Deploy in 2 minutes</span>
</div>
""", unsafe_allow_html=True)
