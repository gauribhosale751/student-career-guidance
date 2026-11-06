import os
from typing import Dict, List

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="AI Student Career Guidance Assistant",
    page_icon="🎓",
    layout="wide",
)

# Curated starter knowledge base. These are broad role profiles, not job guarantees.
CAREER_KNOWLEDGE: Dict[str, dict] = {
    "Finance": {
        "roles": [
            {
                "title": "Financial Analyst",
                "responsibilities": "Analyse financial statements, build forecasts, compare performance and prepare reports.",
                "skills": ["Excel", "financial accounting", "financial modelling", "分析", "communication"],
                "qualifications": "Commerce, finance, economics or a related degree is commonly relevant.",
                "certifications": ["NISM certifications relevant to the chosen finance segment", "CFA Program (long-term, eligibility and costs apply)"],
                "projects": ["Build a three-year financial analysis of a listed company using public annual reports."]
            },
            {
                "title": "Accounts Executive",
                "responsibilities": "Maintain ledgers, process invoices, reconcile accounts and support month-end closing.",
                "skills": ["Accounting", "GST basics", "Tally or comparable accounting software", "Excel", "attention to detail"],
                "qualifications": "B.Com or a related accounting qualification is commonly relevant.",
                "certifications": ["Tally education resources/certification where available", "GST practitioner learning through official GST resources"],
                "projects": ["Create a sample company ledger, sales register and bank reconciliation."]
            },
            {
                "title": "Business / Credit Analyst",
                "responsibilities": "Review business performance, assess credit information and prepare decision-support reports.",
                "skills": ["Excel", "financial statement analysis", "business writing", "statistics", "presentation"],
                "qualifications": "Commerce, economics, finance or business qualifications are useful.",
                "certifications": ["NISM modules relevant to the target role", "A recognised introductory financial analysis course"],
                "projects": ["Prepare a mock credit note using a fictional small-business case."]
            },
        ],
        "skill_topics": ["Advanced Excel", "accounting fundamentals", "financial statement analysis", "basic statistics", "presentation and business writing"],
    },
    "Mechanical Engineering": {
        "roles": [
            {
                "title": "Automotive Design / CAD Engineer",
                "responsibilities": "Create and revise component designs, 3D models and engineering drawings.",
                "skills": ["Engineering drawing", "CAD (e.g. SolidWorks/CATIA)", "GD&T", "materials", "problem solving"],
                "qualifications": "Diploma or degree in Mechanical/Automobile Engineering is commonly relevant.",
                "certifications": ["Vendor training/certification for the CAD tool used", "NPTEL courses in CAD, design or manufacturing when available"],
                "projects": ["Model a simple bracket or gearbox component and create a dimensioned drawing."]
            },
            {
                "title": "Quality Engineer",
                "responsibilities": "Monitor product quality, investigate defects and support corrective/preventive actions.",
                "skills": ["Quality tools", "7 QC tools", "measurement", "root-cause analysis", "Excel"],
                "qualifications": "Mechanical, Production or Automobile Engineering is commonly relevant.",
                "certifications": ["Introductory Six Sigma training", "Relevant quality-management training"],
                "projects": ["Create a process flow, check sheet and Pareto analysis for a sample manufacturing defect."]
            },
            {
                "title": "Production / Manufacturing Engineer",
                "responsibilities": "Improve production processes, reduce waste and support safe, efficient manufacturing.",
                "skills": ["Manufacturing processes", "lean basics", "time study", "CAD basics", "communication"],
                "qualifications": "Mechanical, Manufacturing or Production Engineering is commonly relevant.",
                "certifications": ["NPTEL manufacturing/production courses when available", "Lean or Six Sigma introductory training"],
                "projects": ["Map a small assembly process and propose a measurable cycle-time improvement."]
            },
        ],
        "skill_topics": ["CAD", "engineering drawing and GD&T", "manufacturing processes", "quality tools", "lean manufacturing"],
    },
    "Computer Science / IT": {
        "roles": [
            {
                "title": "AI / Machine Learning Engineer (entry pathway)",
                "responsibilities": "Prepare data, train and evaluate models, integrate model outputs into software and document results.",
                "skills": ["Python", "statistics", "linear algebra basics", "machine learning", "SQL", "Git"],
                "qualifications": "Computer Science, IT, mathematics or a related degree is helpful; a strong portfolio also matters.",
                "certifications": ["NPTEL AI/ML courses when available", "Microsoft Learn AI learning paths"],
                "projects": ["Build and evaluate a small classification model; document data, metrics and limitations."]
            },
            {
                "title": "Software Developer",
                "responsibilities": "Design, build, test and maintain software applications and APIs.",
                "skills": ["One programming language", "data structures", "Git", "SQL", "testing", "problem solving"],
                "qualifications": "Computer Science/IT degree or equivalent demonstrable skills.",
                "certifications": ["Microsoft Learn role-based learning (where relevant)", "A structured programming course with assessed projects"],
                "projects": ["Build a CRUD application with authentication, tests and a clear README."]
            },
            {
                "title": "Data Analyst",
                "responsibilities": "Clean data, analyse trends, create dashboards and communicate evidence-based findings.",
                "skills": ["SQL", "Excel", "Python or R", "statistics", "Power BI or Tableau", "storytelling"],
                "qualifications": "Computer Science, IT, mathematics, statistics, economics or related backgrounds are useful.",
                "certifications": ["Google Data Analytics Certificate (check current availability and fees)", "Microsoft Learn Power BI learning paths"],
                "projects": ["Analyse a public dataset and publish a dashboard with a short insight report."]
            },
        ],
        "skill_topics": ["Python", "SQL", "statistics", "Git/GitHub", "data structures", "machine learning fundamentals", "communication"],
    },
    "Business / Management": {
        "roles": [
            {
                "title": "Business Analyst",
                "responsibilities": "Understand business needs, document requirements, analyse processes and support solution delivery.",
                "skills": ["Excel", "SQL basics", "requirements gathering", "process mapping", "presentation"],
                "qualifications": "MBA or a degree in business, commerce, engineering or a related discipline can be relevant.",
                "certifications": ["Entry-level business analysis training", "Microsoft Learn data and Power BI paths"],
                "projects": ["Create a requirements document and process map for a fictional online store."]
            },
            {
                "title": "Data / Business Analytics Associate",
                "responsibilities": "Turn business data into reports, dashboards and recommendations for stakeholders.",
                "skills": ["Excel", "SQL", "Power BI/Tableau", "statistics", "business understanding"],
                "qualifications": "Business, management, commerce, economics, engineering or quantitative degrees are useful.",
                "certifications": ["Google Data Analytics Certificate (check current availability and fees)", "Microsoft Learn Power BI learning paths"],
                "projects": ["Create a sales dashboard and explain three decisions supported by the data."]
            },
            {
                "title": "Marketing / Growth Analyst",
                "responsibilities": "Measure campaign performance, research customers and recommend ways to improve acquisition and retention.",
                "skills": ["Market research", "Excel", "analytics", "digital marketing", "communication"],
                "qualifications": "MBA/marketing, business, commerce or related backgrounds can be relevant.",
                "certifications": ["Google Skillshop training", "HubSpot Academy courses"],
                "projects": ["Design a sample campaign measurement plan with KPIs and a mock results dashboard."]
            },
        ],
        "skill_topics": ["Excel", "business communication", "data interpretation", "SQL", "Power BI", "presentation", "process analysis"],
    },
    "Other / Not sure": {
        "roles": [
            {
                "title": "Project Coordinator",
                "responsibilities": "Track tasks, timelines, risks and communication across a project team.",
                "skills": ["Planning", "communication", "Excel", "documentation", "teamwork"],
                "qualifications": "Requirements vary by industry; relevant education and evidence of coordination skills help.",
                "certifications": ["Introductory project management courses from recognised providers"],
                "projects": ["Create a project plan with milestones, risks and a weekly status report."]
            },
            {
                "title": "Customer Success Associate",
                "responsibilities": "Help customers use a product, resolve issues and improve customer outcomes.",
                "skills": ["Communication", "problem solving", "product knowledge", "CRM basics", "empathy"],
                "qualifications": "Requirements vary; domain knowledge and communication skills are valuable.",
                "certifications": ["HubSpot Academy customer service resources"],
                "projects": ["Write a sample onboarding guide and customer issue-resolution workflow."]
            },
            {
                "title": "Operations Analyst",
                "responsibilities": "Review operational data and processes to improve cost, quality and service.",
                "skills": ["Excel", "process mapping", "basic statistics", "reporting", "problem solving"],
                "qualifications": "Business, engineering, commerce or related qualifications can be relevant.",
                "certifications": ["Introductory Lean/Six Sigma training", "Microsoft Learn data skills"],
                "projects": ["Analyse a sample workflow and propose improvements with measurable KPIs."]
            },
        ],
        "skill_topics": ["Excel", "communication", "problem solving", "data interpretation", "project planning"],
    },
}

LEARNING_RESOURCES = [
    ("NPTEL", "IITs/IISc courses; learning is generally free, while certification exams may have fees.", "https://www.nptel.ac.in/"),
    ("SWAYAM", "Government-supported online courses; check each course page for schedule and certificate conditions.", "https://swayam.gov.in/"),
    ("Microsoft Learn", "Free, self-paced technical learning paths; some external certification exams are paid.", "https://learn.microsoft.com/training/"),
    ("Google Career Certificates", "Professional certificate programmes; check current India pricing, enrolment and availability.", "https://grow.google/intl/en_in/certificates/"),
    ("Coursera", "Courses and professional certificates; pricing, audit access and financial aid vary by course.", "https://www.coursera.org/"),
    ("edX", "University and professional courses; audit and certificate options vary.", "https://www.edx.org/"),
    ("HubSpot Academy", "Free courses and certifications in marketing, sales and customer service.", "https://academy.hubspot.com/"),
    ("Google Skillshop", "Training for Google products and advertising tools; availability varies by topic.", "https://skillshop.withgoogle.com/"),
]

JOB_RESOURCES = [
    ("National Career Service (Government of India)", "https://www.ncs.gov.in/"),
    ("LinkedIn Jobs", "https://www.linkedin.com/jobs/"),
    ("Naukri", "https://www.naukri.com/"),
    ("Indeed India", "https://in.indeed.com/"),
]

def build_prompt(profile: dict, career_data: dict) -> str:
    return f"""
You are a careful, practical career guidance assistant for students in India.
Give educational guidance, not a guarantee of employment or admission.

STUDENT PROFILE
Qualification: {profile['qualification']}
Department / field: {profile['department']}
Year / experience: {profile['year']}
Current skills: {profile['skills'] or 'Not specified'}
Interests: {profile['interests']}
Preferred industry: {profile['industry']}
Career goal: {profile['goal']}
Location preference: {profile['location'] or 'Not specified'}

CURATED KNOWLEDGE BASE FOR THE SELECTED FIELD
{career_data}

Create a personalised plan with these exact sections:
1. Profile summary
2. Three recommended career roles (ranked). For each: responsibilities, why it fits this profile,
   typical entry requirements, and realistic first steps.
3. Skill-gap analysis. Separate skills the student already has from skills to develop.
   Do not claim a skill is present unless the student listed it.
4. Learning roadmap in stages: 0-1 month, 2-3 months, 4-6 months.
   Include topics, weekly practice, and one portfolio project per stage.
5. Certifications. Suggest only relevant options and clearly say to verify current eligibility,
   price, exam format and availability on the provider's official site.
6. Job-search strategy for India: search terms, entry-level titles, portfolio/resume advice,
   networking and scam precautions. Do not invent live vacancies, salaries or placement guarantees.
7. Next 3 actions the student can start this week.

Be encouraging but realistic. Explain uncertainty where information is missing.
Use concise headings, tables where useful, and concrete examples.
Do not invent course URLs, job openings, placement statistics or certification requirements.
"""

def generate_plan(profile: dict, career_data: dict) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an evidence-conscious student career counsellor. Never fabricate facts, vacancies, links or credentials."
            },
            {"role": "user", "content": build_prompt(profile, career_data)},
        ],
        temperature=0.35,
        max_tokens=3000,
    )
    return response.choices[0].message.content or "The model returned an empty response."

st.title("🎓 AI Student Career Guidance Assistant")
st.write("Create a practical career plan based on your education, skills, interests and goals.")
st.info("Your details are used to generate guidance in this session. Do not enter passwords, government ID numbers or other sensitive personal information.")

with st.form("career_profile_form"):
    st.subheader("1. Student profile")
    c1, c2 = st.columns(2)
    with c1:
        qualification = st.selectbox(
            "Current qualification",
            ["12th / Higher Secondary", "Diploma", "B.Com", "BBA", "BCA", "B.Sc", "B.E. / B.Tech",
             "MBA", "MCA", "M.Sc", "Other"],
        )
        department = st.selectbox(
            "Department / field",
            ["Finance", "Mechanical Engineering", "Computer Science / IT",
             "Business / Management", "Electrical / Electronics", "Science / Mathematics",
             "Arts / Humanities", "Other / Not sure"],
        )
        year = st.selectbox("Current year / experience", [
            "First year", "Second year", "Third year", "Final year", "Recent graduate",
            "0-2 years work experience", "3+ years work experience"
        ])
    with c2:
        industry = st.selectbox(
            "Preferred industry",
            ["Information Technology", "Finance / Banking", "Automobile / Manufacturing",
             "Business / Consulting", "Healthcare", "Education", "Government / Public sector",
             "Marketing / Media", "Open to suggestions"],
        )
        goal = st.selectbox(
            "Career goal",
            ["Get an internship", "Get an entry-level job", "Prepare for higher studies",
             "Prepare for government exams", "Change career direction", "Explore career options"],
        )
        location = st.text_input("Preferred work location (optional)", placeholder="e.g. Pune, Mumbai, Remote")

    skills = st.text_area(
        "Your current skills (comma-separated)",
        placeholder="e.g. Python, Excel, communication, teamwork",
        help="List only skills you currently have. You can leave this blank.",
    )
    interests = st.text_area(
        "Your interests",
        placeholder="e.g. building apps, analysing financial data, designing vehicles, working with people",
    )
    submitted = st.form_submit_button("🚀 Generate Career Plan", type="primary", use_container_width=True)

if submitted:
    if not interests.strip():
        st.error("Please enter at least one interest so the recommendations have a useful starting point.")
    else:
        profile = {
            "qualification": qualification,
            "department": department,
            "year": year,
            "skills": skills.strip(),
            "interests": interests.strip(),
            "industry": industry,
            "goal": goal,
            "location": location.strip(),
        }
        career_data = CAREER_KNOWLEDGE.get(department, CAREER_KNOWLEDGE["Other / Not sure"])
        with st.spinner("Analysing your profile and preparing your career plan..."):
            try:
                plan = generate_plan(profile, career_data)
                st.session_state["career_plan"] = plan
                st.session_state["career_profile"] = profile
            except Exception as exc:
                st.error(f"Could not generate the plan: {exc}")
                st.caption("Check your API key, internet connection, Groq model name and installed packages.")

if "career_plan" in st.session_state:
    st.divider()
    st.header("2. Your personalised career plan")
    st.markdown(st.session_state["career_plan"])
    st.download_button(
        "⬇️ Download career plan",
        data=st.session_state["career_plan"],
        file_name="student_career_plan.md",
        mime="text/markdown",
    )

st.divider()
st.header("3. Learning resources")
st.caption("These are official platform homepages, not a claim that a specific course is currently open. Check the provider page for current course availability, fees and eligibility.")
for name, description, url in LEARNING_RESOURCES:
    st.markdown(f"- **[{name}]({url})** — {description}")

st.header("4. Job-search resources")
st.caption("These links open job-search portals. This app does not claim that any particular vacancy is live.")
for name, url in JOB_RESOURCES:
    st.markdown(f"- [{name}]({url})")

with st.expander("About this project / limitations"):
    st.write(
        "This is an educational prototype. Recommendations are generated by an LLM and should be "
        "checked against course providers, employers and a qualified career counsellor. The curated "
        "knowledge base is a starter dataset, not an exhaustive labour-market database. No live job "
        "vacancies, salary estimates or placement guarantees are retrieved."
    )
