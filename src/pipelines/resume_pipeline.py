from langgraph.graph import StateGraph, END

from src.agents.resolver import (
    ResumeState,
    jd_analyzer_agent,
    resume_analyzer_agent,
    resume_tuning_agent,
)

graph = StateGraph(ResumeState)

graph.add_node("jd_analyzer", jd_analyzer_agent)
graph.add_node("resume_analyzer", resume_analyzer_agent)
graph.add_node("resume_tuning", resume_tuning_agent)

graph.set_entry_point("jd_analyzer")
graph.add_edge("jd_analyzer", "resume_analyzer")
graph.add_edge("resume_analyzer", "resume_tuning")
graph.add_edge("resume_tuning", END)

app = graph.compile()

jd = """Job Description Full Stack AI Engineer (Immediate Joiner)

Position: Full Stack AI Engineer (2 Openings)
Location: Pune / Hybrid (Preferred)
Experience: 14 Years (Exceptional freshers with strong projects are welcome)
Joining: Immediate (Within 7 Days)


About the Role

We are looking for talented Full Stack AI Engineers to join our growing engineering team. You'll work on building scalable software products, developing AI-powered solutions, designing robust backend systems, and delivering production-ready features in a fast-paced environment.

If you enjoy solving complex problems, building products from the ground up, and working with the latest AI technologies, we'd love to hear from you.


Responsibilities

Design, develop, and maintain full-stack web applications.
Build scalable frontend and backend systems.
Develop AI-powered features using modern LLMs and AI frameworks.
Design secure REST APIs and database architecture.
Integrate third-party APIs and cloud services.
Optimize application performance, scalability, and reliability.
Collaborate with cross-functional teams to deliver high-quality software.
Write clean, maintainable, and production-ready code.
Participate in code reviews, testing, and technical discussions.

Required Skills

Frontend

React.js / Next.js
TypeScript / JavaScript
HTML5, CSS3
Tailwind CSS
Backend

Node.js
Express.js / NestJS
REST APIs
Authentication & Authorization
PostgreSQL / MySQL / MongoDB

AI & Machine Learning

OpenAI APIs or similar LLMs
LangChain / AI Agents
Prompt Engineering
RAG concepts
Vector Databases
Python for AI development

DevOps & Tools

Git & GitHub
Docker
Linux
CI/CD fundamentals
AWS, Azure, or GCP

Good to Have

FastAPI
Redis
WebSockets
Kubernetes
n8n
MCP
LangGraph, CrewAI, AutoGen, Dify
Strong system design knowledge

What We're Looking For

Strong problem-solving skills
Ability to work independently
Ownership mindset
Fast learner with attention to detail
Passion for AI, software engineering, and product development
Excellent communication and collaboration skills

Qualifications

B.E./B.Tech/M.Tech in Computer Science, IT, AI/ML, Electronics, or a related field.
Strong GitHub profile and hands-on projects preferred.

Role: Full Stack Developer
Industry Type: Auto Components
Department: Engineering - Software & QA
Employment Type: Full Time, Permanent
Role Category: Software Development
Education
UG: B.Tech / B.E. in Computer Science and Engineering (CSE), Artificial Intelligence And Data Science, Artificial Intelligence And Machine Learning
PG: M.Tech in Artificial Intelligence and Machine Learning
Key Skills
Skills highlighted with ‘‘ are preferred keyskills
RAG conceptsGithubAzure CertifiedFullstack DevelopmentVector Database
LangchainStrong system design knowledgeCi/CdDockerMySQLJavascriptReact.jsAWSPythonCSSn8nLLMsPostgresqlRest APIsRedisNode.jsPrompt EngineeringGITLinuxGCPMongoDBNextjsKubernetes"""

resume = r"""\documentclass[letterpaper,10.5pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.55in}
\addtolength{\textwidth}{1.1in}
\addtolength{\topmargin}{-0.4in}
\addtolength{\textheight}{1.5in}

\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-5pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\small{#1}
}

\newcommand{\resumeSubheading}[4]{
  \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small #3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-4pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=*, itemsep=-2pt, topsep=0pt]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-4pt}}

\begin{document}

% HEADER
\begin{center}
    \textbf{\Huge \scshape Abhinav Maurya} \\ \vspace{3pt}
    \textbf{\large Backend Engineer (Node.js / AWS)} \\ \vspace{4pt}
    \small
    07052314766 $|$
    \href{mailto:abhinavmaurya476@gmail.com}{abhinavmaurya476@gmail.com} $|$
    \href{https://linkedin.com/in/abhinav28}{LINKEDIN} $|$
    \href{https://abhinav-sde.vercel.app/}{PORTFOLIO} $|$
    \href{https://github.com/abhinav2-3}{GITHUB}
\end{center}

% SUMMARY — 3 lines max, front-loaded with strongest signals
\section{Summary}
Backend Engineer with 1.5+ years shipping production APIs and owning backend infrastructure at a live B2C startup. Cut API response times by 60\% and independently built Avira.ai, a real-time AI interview platform on Google Gemini 2.5. I own things end-to-end - from schema design to AWS deployment.

% TECHNICAL SKILLS
\section{Technical Skills}
\begin{itemize}[leftmargin=0.15in, label={}, itemsep=-1pt]
\small{
  \item{\textbf{Languages:} TypeScript, JavaScript, SQL}
  \item{\textbf{Backend:} Node.js, Express.js, REST API Design, JWT/OAuth2, Webhook Handling, Cron Jobs, OpenAI APIs, Google Gemini API}
  \item{\textbf{Databases:} PostgreSQL, MongoDB, Redis}
  \item{\textbf{Cloud \& DevOps:} AWS (EC2, S3, Lambda, SAM), Docker, GitHub Actions (CI/CD), Nginx}
  \item{\textbf{Tools:} Git, Postman, Sentry}
}
\end{itemize}

% EXPERIENCE
\section{Experience}
\resumeSubHeadingListStart

\resumeSubheading
{Backend Engineer}{Dec 2024 -- Present}
{FitnEarn}{Remote, India}
\resumeItemListStart
  \resumeItem{Owned backend for a live B2C fitness platform - designed data models, built REST APIs, and deployed to AWS lambda/S3 across web, Android, and admin dashboard}
  \resumeItem{Optimized MongoDB queries and indexes across 5+ high-traffic endpoints, cutting average API response time by \textbf{60\%}}
  \resumeItem{Architected and shipped 5+ production modules end-to-end, coordinating releases across frontend, design, and QA teams}
  \resumeItem{Handled deployment, uptime monitoring, and environment config on AWS EC2 --- zero production outages during owned modules}
\resumeItemListEnd

\resumeSubheading
{Backend Developer Intern}{Jul 2024 -- Oct 2024}
{Rablo}{Lucknow, India}
\resumeItemListStart
  \resumeItem{Built Node.js/Express backend for an online tutoring platform, handling concurrent session booking and user lifecycle flows}
  \resumeItem{Integrated Razorpay payment gateway with webhook handling, covering the full transaction lifecycle from initiation to confirmation}
  \resumeItem{Implemented tutor onboarding from signup to first session - verification, scheduling, and completion tracking}
\resumeItemListEnd

\resumeSubHeadingListEnd

% PROJECTS
\section{Projects}
\resumeSubHeadingListStart

\resumeSubheading
{Avira.ai --- AI Interview Platform $|$ \href{https://avira-interview-ai.vercel.app/}{Live Demo} $|$ \href{https://github.com/abhinav2-3/Avira-Interview-AI}{GitHub}}{}
{Next.js, TypeScript, Node.js, Google Gemini 2.5, MongoDB, Three.js}{}
\resumeItemListStart
  \resumeItem{Built a voice-based AI interview platform using Gemini 2.5 audio model --- handles real-time conversation, adaptive questioning, and full session persistence via MongoDB}
  \resumeItem{Designed the backend API layer for session lifecycle, scoring logic, and resume/JD-aware question generation from scratch}
  \resumeItem{Shipped end-to-end solo - frontend, backend, AI integration, and 3D holographic UI using Three.js}
\resumeItemListEnd

\resumeSubheading
{MonStack CLI --- npm Package $|$ \href{https://github.com/abhinav2-3/monstack-cli}{GitHub}}{}
{Node.js, TypeScript, npm}{}
\resumeItemListStart
  \resumeItem{Built and published a CLI tool that scaffolds a production Node.js/Express backend - routes, controllers, middleware, Docker - with one command}
  \resumeItem{Saves 30--45 min of setup per project; built as a modular monorepo to support multiple frameworks and databases as plugins}
\resumeItemListEnd

\resumeSubheading
{Digital Wallet App $|$ \href{https://paytm-user-app-wine.vercel.app/}{Live Demo}}{}
{Next.js, Node.js, PostgreSQL, Redis, TypeScript}{}
\resumeItemListStart
  \resumeItem{Designed ACID-compliant PostgreSQL schema for P2P transfers and integrated Redis caching, cutting query response time by \textbf{75\%}}
  \resumeItem{Built JWT auth, RBAC, and a RESTful API layer handling wallet operations, balance management, and transaction history}
\resumeItemListEnd

\resumeSubHeadingListEnd
% EDUCATION
\section{Education}
\resumeSubHeadingListStart
\resumeSubheading
{Ambalika Institute of Management and Technology}{Lucknow, India}
{Bachelor of Computer Applications --- Computer Science}{Aug 2022 -- Jul 2025}
\resumeSubHeadingListEnd

\end{document}\documentclass[letterpaper,10.5pt]{article}"""


# result: ResumeState = app.invoke(
#     ResumeState(
#         jd=jd,
#         jd_desc="",
#         resume=resume,
#         resolution="",
#         final_response="",
#     )
# )

# print("======================== JD =========================")
# print("jd:", result["jd"])
# print("===================== JD DESC =======================")
# print("jd_desc:", result["jd_desc"])
# print("===================== RESOLUTION ====================")
# print("Resolution:", result["resolution"])
# print("==================== FINAL RESPONSE =================")
# print("Final Response:", result["final_response"])
