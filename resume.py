import streamlit as st
import time
from src.pipelines.resume_pipeline import app as resume_app, ResumeState

st.set_page_config(page_title="AI Resume Tuner", page_icon="🧠", layout="wide")

st.markdown(
    """
<style>
    .main { background-color: #0f1117; }
    .stTextArea textarea { font-family: monospace; font-size: 13px; }
    .agent-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #444;
    }
    .agent-card.active { border-left-color: #f0a500; }
    .agent-card.done { border-left-color: #00c48c; }
    .agent-card.idle { border-left-color: #333; opacity: 0.5; }
    .agent-title { font-weight: 700; font-size: 15px; color: #fff; margin-bottom: 4px; }
    .agent-desc { font-size: 13px; color: #aaa; }
    .agent-status { font-size: 12px; margin-top: 6px; }
    .status-idle { color: #555; }
    .status-active { color: #f0a500; }
    .status-done { color: #00c48c; }
    .result-box {
        background: #1a1d27;
        border: 1px solid #2e3250;
        border-radius: 10px;
        padding: 18px;
        font-size: 13px;
        color: #dde;
        white-space: pre-wrap;
        font-family: monospace;
        max-height: 340px;
        overflow-y: auto;
    }
    .latex-box {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px;
        font-size: 12.5px;
        color: #c9d1d9;
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        max-height: 500px;
        overflow-y: auto;
    }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #fff;
        margin: 24px 0 12px 0;
    }
    .pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
    }
    .pill-blue { background: #1a3a5c; color: #58a6ff; }
    .pill-green { background: #1a3a2a; color: #00c48c; }
    .pill-yellow { background: #3a2a00; color: #f0a500; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("## 🧠 AI Resume Tuner")
st.markdown(
    "Paste your **Job Description** and **Resume**, and let the multi-agent system tailor your resume to the JD."
)
st.divider()

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("#### 📋 Job Description")
    jd = st.text_area(
        label="jd",
        placeholder="Paste the full job description here...",
        height=280,
        label_visibility="collapsed",
        key="jd_input",
    )

with col_right:
    st.markdown("#### 📄 Your Resume")
    resume = st.text_area(
        label="resume",
        placeholder="Paste your resume content here (plain text or LaTeX)...",
        height=280,
        label_visibility="collapsed",
        key="resume_input",
    )

st.markdown("")
run_btn = st.button("🚀 Tune My Resume", use_container_width=True, type="primary")

if run_btn:
    if not jd.strip() or not resume.strip():
        st.warning("Please provide both Job Description and Resume.")
    else:
        st.divider()
        st.markdown("### ⚙️ Agent Pipeline")

        agents = [
            {
                "id": "jd_analyzer",
                "title": "Agent 1 — JD Analyzer",
                "desc": "Reads the job description and extracts key skills, technologies, and requirements.",
                "icon": "🔍",
            },
            {
                "id": "resume_analyzer",
                "title": "Agent 2 — Resume Matcher",
                "desc": "Compares your resume against the JD analysis and identifies gaps and matches.",
                "icon": "🧩",
            },
            {
                "id": "resume_tuner",
                "title": "Agent 3 — Resume Tuner",
                "desc": "Rewrites your resume in LaTeX to align closely with the job description.",
                "icon": "✍️",
            },
        ]

        placeholders = []
        for agent in agents:
            ph = st.empty()
            ph.markdown(
                f"""
            <div class="agent-card idle">
                <div class="agent-title">{agent['icon']} {agent['title']}</div>
                <div class="agent-desc">{agent['desc']}</div>
                <div class="agent-status status-idle">⏳ Waiting...</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            placeholders.append(ph)

        def set_active(i):
            placeholders[i].markdown(
                f"""
            <div class="agent-card active">
                <div class="agent-title">{agents[i]['icon']} {agents[i]['title']}</div>
                <div class="agent-desc">{agents[i]['desc']}</div>
                <div class="agent-status status-active">🔄 Running...</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        def set_done(i, note=""):
            placeholders[i].markdown(
                f"""
            <div class="agent-card done">
                <div class="agent-title">{agents[i]['icon']} {agents[i]['title']}</div>
                <div class="agent-desc">{agents[i]['desc']}</div>
                <div class="agent-status status-done">✅ Done {f'— {note}' if note else ''}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # --- Run agents step by step with visual feedback ---

        from src.agents.resolver import (
            jd_analyzer_agent,
            resume_analyzer_agent,
            resume_tuning_agent,
        )

        state = ResumeState(
            jd=jd,
            jd_desc="",
            resume=resume,
            resolution="",
            final_response="",
        )

        # Agent 1
        set_active(0)
        time.sleep(0.3)
        state = jd_analyzer_agent(state)
        set_done(0, "JD parsed")

        # Agent 2
        set_active(1)
        time.sleep(0.3)
        state = resume_analyzer_agent(state)
        set_done(1, "Gaps identified")

        # Agent 3
        set_active(2)
        time.sleep(0.3)
        state = resume_tuning_agent(state)
        set_done(2, "Resume rewritten")

        st.divider()

        # --- Results ---
        st.markdown("### 📊 Results")

        tab1, tab2, tab3 = st.tabs(
            ["🔍 JD Analysis", "🧩 Resume Match", "✍️ Tuned Resume (LaTeX)"]
        )

        with tab1:
            st.markdown(
                '<div class="result-box">'
                + state["jd_desc"].replace("<", "&lt;").replace(">", "&gt;")
                + "</div>",
                unsafe_allow_html=True,
            )

        with tab2:
            st.markdown(
                '<div class="result-box">'
                + state["resolution"].replace("<", "&lt;").replace(">", "&gt;")
                + "</div>",
                unsafe_allow_html=True,
            )

        with tab3:
            latex = state["final_response"]
            st.markdown(
                '<div class="latex-box">'
                + latex.replace("<", "&lt;").replace(">", "&gt;")
                + "</div>",
                unsafe_allow_html=True,
            )
            st.download_button(
                label="⬇️ Download LaTeX",
                data=latex,
                file_name="tuned_resume.tex",
                mime="text/plain",
                use_container_width=True,
            )
