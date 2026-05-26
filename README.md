# 🔭 SkillScope — Job Market Skill Gap Analyzer

> **A polished, interactive Streamlit dashboard** that analyzes 1,200 synthetic job postings to reveal which skills employers demand most — and where fresh graduates fall short.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 CLICK TO VIEW Live Demo

**→ [View]([https://your-app-name.streamlit.app](https://job-market-analyzer-csl5t7bcappqw6gn4ja3bge.streamlit.app/))**

*(Replace with your Streamlit Community Cloud URL after deployment)*

---

## 📸 Features

| Feature | Description |
|---|---|
| 📊 **Skill Demand Dashboard** | Top N skills ranked by frequency with radar chart & heatmap by experience |
| 💼 **Roles & Salaries** | Box plots, bar charts, and scatter analysis per role and domain |
| 🎓 **Grad Gap Analysis** | Side-by-side comparison of all-level vs. entry-level skill demand |
| 🌍 **Market Overview** | Location heatmap, domain pie, education requirements, posting freshness |
| 🎛️ **Interactive Filters** | Domain, role, experience, salary range, location — all real-time |
| 💡 **Business Insights** | Auto-generated executive summary with data-driven takeaways |

---

## 🚀 Deploy in 2 Minutes (Streamlit Community Cloud)

### Step 1 — Fork & push to GitHub
```bash
git clone https://github.com/YOUR_USERNAME/job-market-analyzer
cd job-market-analyzer
# (make any changes you want)
git add . && git commit -m "Initial deploy" && git push
```

### Step 2 — Deploy on Streamlit Community Cloud (free)
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **"New app"**
3. Select your repo, branch `main`, and set **Main file path** to `app.py`
4. Click **"Deploy"** — live in ~60 seconds ✅

### Step 3 — Share your URL
Copy the generated URL like `https://your-app.streamlit.app` and share anywhere.

---

## 💻 Run Locally

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/job-market-analyzer
cd job-market-analyzer

# Install deps
pip install -r requirements.txt

# Run
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## 🗂️ Project Structure

```
job-market-analyzer/
├── app.py                  # Main Streamlit application (all-in-one)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Dark theme + server config
└── README.md               # This file
```

---

## 🧪 Tech Stack

- **[Streamlit](https://streamlit.io)** — Web app framework
- **[Plotly](https://plotly.com/python/)** — Interactive charts (bar, box, scatter, radar, heatmap, pie)
- **[Pandas](https://pandas.pydata.org)** + **[NumPy](https://numpy.org)** — Data manipulation
- **[Matplotlib](https://matplotlib.org)** + **[Seaborn](https://seaborn.pydata.org)** — Statistical support

---

## 📊 Dataset

All 1,200 job postings are **synthetically generated inside the app** using realistic distributions:

- **12 job roles** across 5 domains (Data, SWE, DevOps, Security, Product)
- **15 companies**, 12 locations, 4 experience levels
- **Salary ranges** calibrated to real 2024 US market data
- **Skill pools** per domain reflecting actual hiring patterns
- Seeded for reproducibility (`random.seed(42)`)

---

## 🎓 Use Cases

- 📁 **GitHub Portfolio** — Deploy and link on your resume
- 🎤 **Interview Prep** — Demonstrates end-to-end data project skills
- 🏫 **Bootcamp / Capstone** — Ready-made project with business value
- 🔍 **Career Research** — Understand what skills to learn next

---

## 🛠️ Customization Ideas

- Swap synthetic data with **real data** from LinkedIn Jobs API or RapidAPI
- Add a **resume upload** feature to auto-match user skills vs. market demand
- Integrate with **Google Sheets** as a live data source
- Add a **skill recommendation engine** using cosine similarity

---

## 📄 License

MIT — free to use, fork, and modify.

---

<div align="center">
  <strong>Built with ❤️ using Streamlit</strong><br>
  Star ⭐ the repo if you find it useful!
</div>
