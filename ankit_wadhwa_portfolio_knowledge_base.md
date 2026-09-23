# Ankit Wadhwa — Portfolio Knowledge Base

> This document is a structured knowledge base about Ankit Wadhwa, intended to be chunked and embedded for a Retrieval-Augmented Generation (RAG) chatbot on his portfolio website. Each section below is written to stand on its own as a retrievable chunk.

---

## Basic Profile

Ankit Wadhwa is an AI Engineer specializing in GenAI and Agentic Systems, based in Yamuna Nagar, Haryana, India, and currently located in Noida for his ongoing job search. He has 4+ years of professional experience as a System Engineer at Tata Consultancy Services (TCS). He is transitioning his career focus toward AI Engineer, Generative AI Developer, and Full-Stack Developer roles.

**Contact Information**
- Phone: +91-7015269163
- Email: ankitwadhwa615@gmail.com
- LinkedIn: linkedin.com/in/ankitwadhwa16

## Professional Summary

Ankit Wadhwa is an AI Engineer who has architected multi-agent orchestration systems with LangGraph, built production RAG pipelines with semantic retrieval over ChromaDB, and shipped secure FastAPI backends with JWT authentication — backed by 4+ years of production delivery experience at Tata Consultancy Services. He is hands-on across the agentic stack: LLM orchestration, vector search, conversational memory, multimodal input, and deployment. He is a Smart India Hackathon 2022 winner and holds the Microsoft Certified: Azure AI Fundamentals certification.

## Technical Skills

- **LLMs & Agent Frameworks:** LangChain, LangGraph (state graphs, conditional routing), Deep Agents, multi-agent orchestration, prompt engineering
- **RAG & Vector Search:** RAG pipelines, ChromaDB, HuggingFace sentence-transformer embeddings (bge-small-en-v1.5), semantic search, conversational memory
- **LLM APIs & Search:** Groq API, Tavily, DuckDuckGo Search, OpenAI/Anthropic/Gemini-style API integration, multimodal (vision) model integration
- **Backend & Auth:** FastAPI, REST APIs, JWT authentication, Streamlit, Firebase
- **Mobile:** Flutter (Riverpod, Provider, BLoC, GetX), Material 3, cross-platform app development
- **NLP & ML:** spaCy, NLTK, TF-IDF, HuggingFace Transformers, NumPy, Pandas, Scikit-learn
- **Cloud & DevOps:** Microsoft Azure (AI Fundamentals Certified), Docker, Podman, Git, Postman
- **Languages:** Python, Dart

## Professional Experience

### System Engineer — Tata Consultancy Services (July 2022 – Present)

- **AI-Assisted Automation & Reporting:** Designed and deployed a Python automation pipeline (Streamlit, REST APIs, smtplib) extracting, processing, and reporting defect/incident data from Rally and Pulse, cutting manual tracking effort by ~40% and improving incident response speed by ~25%.
- **NLP Text Processing:** Applied spaCy and TF-IDF preprocessing to structure unstructured incident/defect text into standardized report fields — foundational work later extended into personal RAG/embedding projects.
- **Reporting Automation:** Built a monthly PowerPoint automation tool using the KIRO AI coding assistant and python-pptx, auto-generating status decks and saving ~6 hours per month.
- **Cross-Platform App (GE HealthCare client):** Built a Flutter cross-platform application with Firebase and REST API integration serving 2,000+ field engineers; led incident tracking and defect monitoring for a live production system.

---

## GenAI / Agentic AI Projects

### Project 1: Ankit's Agent — Deep Agentic Research & Coding Assistant

**One-line pitch:** A portfolio-grade AI assistant combining a Flutter client, a FastAPI service, and a LangGraph/Deep Agents orchestration layer, enabling users to research topics, analyze uploaded documents and images, ask coding questions, and hold authenticated multi-turn conversations.

**Live Demo:** https://ankit-s-deep-agent.web.app/
**GitHub Repo:** https://github.com/ankitwadhwa615/Deep-Agentic-Research-and-Coding-Assistant

**What it demonstrates:**
- Designing and integrating LLM-powered product experiences
- Building tool-using, delegation-first agent workflows
- Connecting multimodal model inputs with file and image upload pipelines
- Building secure authenticated APIs and persistent conversation storage
- Shipping a cross-platform Flutter interface with responsive state handling
- Diagnosing and improving real-world streaming, validation, and browser issues

**Core Features:**
- Email/password registration and login with JWT authentication, plus token refresh with server-side rotated refresh tokens (stored only as keyed hashes)
- Inline form validation and disabled states for invalid auth input
- Password-change endpoint plus a password-reset API endpoint
- Persistent user sessions using Flutter `shared_preferences`
- New conversations, saved sessions, and message history
- Research, coding, review, and general-purpose specialist agents with delegation status updates during execution
- Server-Sent Events (SSE) streaming responses with live delegation status in the Flutter client, plus a non-streaming JSON chat endpoint for integrations
- Upload support for UTF-8 text-based files, PDFs, and images, with image previews in chat and direct vision-model analysis
- Lightweight Markdown-style rendering for headings, bold, italics, bullets, and dividers
- SQLite persistence for users, sessions, messages, and uploads
- CORS configuration for web deployments

**Architecture:**
```
Flutter Client (auth/chat/splash screens, Riverpod state, API client, multi-platform file selection)
        ↓
FastAPI Backend (auth routes, chat routes, upload route, SQLite DB, CORS + bearer-token security)
        ↓
Agent Runtime (LangGraph checkpointed execution, Deep Agents orchestration,
               researcher/coder/reviewer subagents, vision-capable model path)
```

**Technology Stack:**
- *Frontend:* Flutter, Dart, Flutter Riverpod, `http`, `shared_preferences`, `file_picker`, `image_picker`, Firebase Core/Hosting, Material 3
- *Backend:* Python 3, FastAPI, Uvicorn, Pydantic, SQLite, JWT bearer auth, PBKDF2-SHA256 password hashing with per-password salts, multipart upload handling, CORS middleware
- *AI/Agent Layer:* LangChain, LangGraph, Deep Agents, Groq-hosted chat models, Tavily web search, specialist subagents for research/coding/review, vision-capable model input for image analysis

**API Surface:** `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/me`, `/auth/password` (PATCH), `/auth/forgot-password`, `/upload`, `/chat/sessions`, `/chat/sessions/{id}/history`, `/chat/sessions/{id}` (DELETE), `/chat`, `/chat/stream`, `/health`.

**Security Notes:** Passwords are stored as hashes, never plaintext. Authenticated resources are scoped to the current user. Upload ownership is verified before a file is used in a chat request. The current password-reset flow updates a password directly after email lookup and its UI trigger is disabled — a production deployment would replace it with a time-limited, email-delivered reset token.

**Design Notes:** The Flutter client uses SSE for incremental responses; `/chat` provides an equivalent non-streaming JSON response. Uploaded images are sent to the vision-capable model as multimodal content. PDFs are text-extracted with `pypdf`; text files are decoded as UTF-8. Conversation checkpoints use an in-memory LangGraph saver, while durable conversation history is stored in SQLite.

---

### Project 2: India Education & Training Schemes Assistant (RAG Chatbot)

**One-line pitch:** A portfolio-ready Retrieval-Augmented Generation (RAG) application for exploring Indian government education and training schemes in plain English. It retrieves relevant records from a local, source-derived knowledge base before asking an LLM to compose an answer, and exposes the retrieved records in the interface for review.

**Live Demo:** https://indian-education-scheme-assistant-rag.streamlit.app/
**GitHub Repo:** https://github.com/ankitwadhwa615/Indian_Education_Scheme_Assistant_RAG

**Highlights:**
- Answers questions on scheme benefits, eligibility, beneficiaries, and application pathways
- Indexes 693 scheme-detail records from an included JSON dataset
- Uses `BAAI/bge-small-en-v1.5` embeddings with local ChromaDB persistence
- Uses Groq-hosted generation (configurable model via `GROQ_MODEL`)
- Supports multiple in-browser chat threads and preserves recent turn context for follow-ups
- Shows retrieved scheme records and chunks for transparency
- Hides model reasoning so users receive only the final response

**Architecture:**
```
Government scheme JSON → normalize + chunk → BGE embeddings → Chroma vector store
                                                           ↓ top 5 chunks
Streamlit chat UI → LangChain grounded prompt → Groq LLM → Answer + sources
```

**Tech Stack:** Streamlit (UI), LangChain (RAG orchestration), ChromaDB (vector store), HuggingFace `BAAI/bge-small-en-v1.5` (embeddings), Groq via `langchain-groq` (LLM inference), myScheme API export script (dataset acquisition).

**Design Choices:**
- Local ChromaDB for simple setup with no managed vector infrastructure
- Metadata-rich documents preserving scheme name, category, beneficiaries, ministry, and agency for better retrieval context
- Lazy initialization of model clients only after the first query
- A grounding-first prompt instructing the model not to invent scheme facts beyond retrieved context
- Bounded chat context including the latest eight messages for follow-ups without unbounded prompt growth

**Limitations & Next Steps:** The data is a point-in-time export, not a live policy feed. A reranker and similarity threshold would improve ambiguous queries. English is the primary supported language. A labelled evaluation set for retrieval recall and groundedness is a planned next improvement.

**Data Note:** The dataset is derived from publicly available Indian government scheme information via myScheme, for educational and portfolio demonstration purposes. This is an informational prototype — scheme rules, dates, and eligibility can change, and users should confirm important decisions on official government portals.

---

### Project 3: Agentic Research Assistant

**One-line pitch:** An autonomous, portfolio-ready AI research assistant that turns a question into a structured research workflow — classifying the request, breaking complex topics into focused sub-questions, searching the web, synthesizing an evidence-aware answer, and critiquing the result before returning it to the user.

**Live Demo:** https://ankitwadhwa-agentic-research-assistant.streamlit.app/
**GitHub Repo:** https://github.com/ankitwadhwa615/Agentic-Research-Assistant

**Why it's notable:** Most chat interfaces produce a single response in one step. This project demonstrates an agentic alternative: a stateful workflow where specialized stages plan, research, write, evaluate, and — when needed — revise the answer. The interface surfaces that process through live pipeline status, progress, iteration count, and response-time metrics.

**Highlights:**
- Intent-aware routing for greetings, lightweight chat, and research questions
- Query decomposition converting complex questions into focused research tasks
- Multi-step web research using DuckDuckGo Search
- Evidence-aware answer synthesis with safeguards against unsupported claims
- A critic stage that requests revision only for substantial issues
- Conditional LangGraph routing with a capped refinement loop (max 3 iterations)
- Streamlit chat interface with conversation history and expandable research plans/critiques
- Optional voice input, transcribed through Groq Whisper (`whisper-large-v3-turbo`)

**How it works:**
```
User question → Intent router
  → Greeting → Greeting response
  → Chat → Chat response
  → Research → Research planner → Web search → Answer synthesis → Quality critique
       → Good enough → Final answer
       → Substantial issue (within iteration limit) → back to Web search
```

**Tech Stack:** Streamlit (UI), LangGraph (agent orchestration), LangChain + `langchain-groq` (LLM integration), Groq-hosted `openai/gpt-oss-120b` and `openai/gpt-oss-20b` (models), DuckDuckGo Search via LangChain Community (web research), Groq Whisper (speech-to-text), `python-dotenv` (configuration).

**Portfolio Talking Points:**
- *Agent design:* Uses an explicit graph instead of a single LLM call, making each stage understandable and extensible
- *Quality control:* The critique node distinguishes substantial content problems from cosmetic improvements and routes only justified revisions back through the workflow
- *State management:* A typed shared state carries the query, research plan, search results, draft, critique, intent, and iteration count through the graph
- *Product thinking:* The UI surfaces the agent's plan, progress, quality review, and timing rather than hiding the reasoning workflow behind a loading spinner
- *Practical multimodality:* Voice questions can be transcribed with Whisper before entering the same research pipeline

**Limitations:** Search results are public-web results from DuckDuckGo; important claims should be verified against primary sources. The assistant is designed for research assistance, not professional legal, medical, financial, or other high-stakes advice. The refinement loop is deliberately capped to control latency and API usage. Voice input depends on browser and Streamlit audio-input support.

---

## Certifications & Achievements

- Microsoft Certified: Azure AI Fundamentals
- Winner, Smart India Hackathon 2022

## Education

**B.Tech, Computer Science and Engineering**
Seth Jai Parkash Mukand Lal Institute of Engineering and Technology | 2018 – 2022

---

## Job Search & Availability

- **Notice Period:** Official notice period is 90 days; able to join within 30 days. Notice period is negotiable, and a notice period buyout is also possible.
- **Preferred Locations:** Delhi NCR, Bangalore, Hyderabad, and Pune. Currently based in Noida.
- **Compensation:** Ankit prefers to discuss current compensation directly. Expected CTC is ₹15–16 LPA, negotiable depending on role, scope, and location.
- **Role Focus:** AI Engineer, Generative AI Developer, and Full-Stack Developer roles, particularly those involving LLM orchestration, RAG systems, and agentic workflows.

## Frequently Asked Questions (Recruiter-Style)

**Why are you looking to move on from Tata Consultancy Services?**
My role at TCS has been broader, support-oriented engineering work — automation, incident/defect tracking, and cross-platform app delivery — which gave me a strong production engineering foundation, but I want a role that's centered specifically on AI/GenAI development day-to-day. Over the past period I've built that focus myself through the LangGraph/agentic and RAG projects in this portfolio, and I'm now looking for a role where that becomes my core job rather than a side pursuit.

**You don't have a large-scale production machine learning project on your resume — how do you address that?**
My applied AI experience is concentrated in RAG and agentic systems rather than classical ML model training — building multi-agent orchestration with LangGraph, production-grade retrieval pipelines with ChromaDB and HuggingFace embeddings, and grounded LLM applications end-to-end (backend, auth, deployment, and frontend). I see this as directly relevant applied AI experience for GenAI/agentic-focused roles, even though it isn't a traditional supervised-learning ML project. I'm happy to go deeper on the retrieval, orchestration, and evaluation design decisions behind any of these projects.

**What's your notice period and when can you join?**
Official notice period is 90 days, but I can join within 30 days. It's negotiable, and a notice period buyout is also possible.

**What's your current and expected compensation?**
Ankit prefers to discuss current compensation directly. Please contact him for those details. Expected CTC is ₹15–16 LPA, negotiable depending on role, scope, and location.

**Are you open to relocation, and what locations do you prefer?**
Yes — I'm willing to relocate to any of my preferred locations: Delhi NCR, Bangalore, Hyderabad, or Pune. I'm currently based in Noida.

**What's your work mode preference — onsite, hybrid, or remote?**
I'm open to any of the three, depending on the role.

**What's the best way to reach you?**
Phone or WhatsApp at +91-7015269163 is the fastest way to reach me; my email is ankitwadhwa615@gmail.com.

---

## Links & Logistics

- **GitHub Profile:** https://github.com/ankitwadhwa615
- **LinkedIn:** linkedin.com/in/ankitwadhwa16
- **Work Mode Preference:** Open to onsite, hybrid, or remote roles
- **Relocation:** Willing to relocate to any of the preferred locations (Delhi NCR, Bangalore, Hyderabad, Pune)
- **Best Way for Recruiters to Reach Out:** Phone or WhatsApp at +91-7015269163

---

*This document consolidates information from Ankit Wadhwa's resume and the READMEs of his three flagship GenAI/agentic projects, plus current job-search details, for use as a knowledge base in a portfolio RAG chatbot.*
