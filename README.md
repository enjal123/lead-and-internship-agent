# 🚀 AI Outreach & Internship Discovery Agent


An AI-powered, multi-agent automation system that streamlines two traditionally time-consuming workflows:

1. **Business Lead Generation** – Discover local businesses with outdated websites, analyze their online presence using AI, score them as potential clients, and generate personalized cold outreach emails.
2. **Internship Discovery** – Search for relevant internship opportunities, evaluate how well they match a candidate's background, and automatically tailor resumes for high-quality applications.

The entire system is designed to run **locally**, leveraging a locally hosted LLM through **Ollama** and free web search providers. No paid AI or search APIs are required.

<img width="1080" height="409" alt="Screenshot 2026-07-22 172237" src="https://github.com/user-attachments/assets/3928bba3-db9a-4d4e-a302-2fcf4036b190" />

<img width="1127" height="421" alt="Screenshot 2026-07-22 172308" src="https://github.com/user-attachments/assets/6aa5d9eb-d0e1-43ec-8b3e-3b3709ac7350" />


---

## ✨ Features

### 🏢 Business Lead Generation

- Automatically discovers local businesses using free web search.
- Analyzes company websites for:
  - Outdated design
  - Missing mobile responsiveness
  - Poor user experience
  - SEO issues
- Uses AI to determine whether a business is a strong potential client.
- Assigns lead scores based on website quality and business potential.
- Extracts publicly available contact information.
- Generates personalized cold outreach emails for each qualified lead.
- Queues outreach emails for later review or immediate sending.

---

### 💼 Internship Discovery

- Searches the web for internship opportunities.
- Evaluates internship relevance using AI.
- Compares postings against a candidate's:
  - Skills
  - Experience
  - Education
  - Career interests
- Scores internship fit.
- Automatically tailors resumes for strong matches.
- Stores all opportunities in a searchable local database.


<img width="1061" height="363" alt="Screenshot 2026-07-23 125711" src="https://github.com/user-attachments/assets/75b96912-8186-4ae4-a60a-db79e58ae90b" />
<img width="795" height="379" alt="Screenshot 2026-07-22 172258" src="https://github.com/user-attachments/assets/092f6283-1128-4d8d-aaf7-a46eba1d0dbd" />

---

### 🤖 Multi-Agent AI Architecture

The system is composed of specialized AI agents, each responsible for a single task, including:

- Business analysis
- Lead qualification
- Internship evaluation
- Resume tailoring
- Email generation
- Embedding generation
- Long-term memory retrieval

Each agent follows the Unix philosophy of doing one job well, making the system modular, maintainable, and easy to extend.

---

### 🧠 Local AI

Unlike many AI automation tools, this project runs entirely on your own machine.

- Local LLM powered by **Ollama**
- No OpenAI API key required
- No usage costs
- Private by default
- Faster iteration and experimentation

---

### 🗄️ Persistent Storage

All generated data is stored locally using SQLite, including:

- Business leads
- Internship listings
- AI analyses
- Lead scores
- Resume versions
- Outreach emails

This allows pipelines to be rerun without duplicating existing entries.

---

## 🏗️ Architecture

```
main.py                  CLI entry point
view_results.py          Display stored database results

agents/                  Single-purpose AI agents
ai/                      LLM client, prompts, embeddings, classifiers
browser/                 Web search, scraping, contact extraction
database/                SQLite schema and queries
emailer/                 SMTP email queue and delivery
memory/                  Chroma vector database
orchestrators/           Pipeline orchestration
resume/                  Resume tailoring
tasks/                   Maintenance jobs
tests/                   Automated test suite
```

---

## ⚙️ Tech Stack

### Programming Language

- Python

### AI

- Ollama
- Llama 3
- Local LLM inference

### Database

- SQLite
- ChromaDB (Vector Memory)

### Search & Scraping

- DuckDuckGo Lite
- DuckDuckGo HTML
- Bing HTML
- BeautifulSoup
- Requests

### Email

- SMTP
- Gmail App Passwords

### Testing

- Pytest

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/enjal123/lead-and-internship-agent.git

cd lead-and-internship-agent
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Ollama

Download Ollama from:

https://ollama.com

Then pull a local model:

```bash
ollama pull llama3
```

Start the local inference server:

```bash
ollama serve
```

---

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update the required variables, including your email credentials.

> **Note:** For Gmail, use a 16-character **App Password**, not your account password.

---

### 5. Add Your Resume

Place your master resume inside:

```
resume/master_resume.txt
```

The AI will automatically generate tailored versions for qualified internship opportunities.

---

## 💻 Usage

### Find Business Leads

```bash
python main.py businesses --query "restaurants Sonoma County" --max 15
```

---

### Find Internship Opportunities

```bash
python main.py internships --query "backend engineering internship 2027"
```

---

### Generate Outreach Emails

Queue emails:

```bash
python main.py outreach
```

Send emails immediately:

```bash
python main.py outreach --send
```

---

### Run Everything

```bash
python main.py all
```

---

### View Saved Results

```bash
python view_results.py
```

---

## 📂 Project Workflow

### Business Pipeline

```
Search Businesses
        │
        ▼
Scrape Website
        │
        ▼
AI Website Analysis
        │
        ▼
Lead Scoring
        │
        ▼
Extract Contact Info
        │
        ▼
Generate Outreach Email
        │
        ▼
Save to Database
```

---

### Internship Pipeline

```
Search Internships
        │
        ▼
Extract Posting
        │
        ▼
AI Fit Analysis
        │
        ▼
Resume Tailoring
        │
        ▼
Save to Database
```

---

## 🎯 Design Decisions

- ✅ Completely free to run
- ✅ No paid AI APIs required
- ✅ Local LLM inference through Ollama
- ✅ Duplicate-safe database
- ✅ Modular multi-agent architecture
- ✅ Persistent long-term vector memory
- ✅ Resume customization for every internship
- ✅ Personalized outreach generation
- ✅ Easily extensible with new agents

---

## 📌 Known Limitations

- Free search providers may occasionally throttle or soft-block automated requests.
- Company names are not always extracted from internship listings depending on the source.
- Ollama must be running locally for AI functionality.
- Requires strong operating system. 
- Search quality depends on publicly available web data.

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🔮 Future Improvements

- Web dashboard
- Docker deployment
- Multi-user authentication
- CRM integration
- LinkedIn lead discovery
- AI follow-up email generation
- Calendar scheduling
- Analytics dashboard
- Resume quality scoring
- Automated interview preparation
- Cloud deployment support

---

## 🤝 Contributing

Contributions, bug reports, feature requests, and pull requests are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Enjal Parajuli**

Incoming EECS Student at UC Berkeley

GitHub: https://github.com/enjal123

---

⭐ If you found this project useful, consider giving it a star. It helps others discover the project and supports future development.
