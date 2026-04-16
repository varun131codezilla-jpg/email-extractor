# Lead Enrichment Engine

A high-fidelity AI-driven email extraction and enrichment tool.

This project implements a robust 3-tier cascade logic to confidently deduce professional email addresses from just a Name and Domain.

## 🌟 Features

- **Tier 1 (Exact Match):** Uses the Serper.dev API to search for explicit matches of the lead's email somewhere online.
- **Tier 2 (Format Deduction):** If an exact match can't be found, smartly scrapes for other employees at the company to deduce standard corporate email nomenclature (e.g. `first.last` vs `f.last`).
- **Tier 3 (Permutations):** Falls back to mathematically generating the 5 most common corporate email formats if all other intelligence fails.
- **Sleek UI:** Uses a premium dark-mode, glassmorphism web UI powered by Flask.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- [Serper API Key](https://serper.dev/) for Google Search integration.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LeadEnrichmentEngine.git
   cd LeadEnrichmentEngine
   ```

2. **Create a virtual environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask-cors requests python-dotenv
   ```

4. **Add Environment Variables**
   Create a `.env` file in the root directory and add your Serper API Key:
   ```txt
   SERPER_API_KEY=your_serper_api_key_here
   ```

## 💻 Usage

To start the Lead Enrichment Engine web application:

```bash
python app.py
```

Then, open your web browser to [http://127.0.0.1:5000](http://127.0.0.1:5000). Enter the First Name, Last Name, and Domain of the lead to extract their intelligence.
