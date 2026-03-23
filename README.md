# ⚡ PyAutomate — Python Automation Toolkit

A powerful Python automation toolkit with text analysis, password generation, hash computation, and system monitoring — all accessible through a sleek web dashboard.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

## ✨ Features

### 📝 Text Analyzer
- Word count, character count, sentence & paragraph analysis
- Vocabulary richness and readability grade (Flesch-Kincaid)
- Top word frequency with visual word cloud
- Reading time estimation

### 🔐 Password Generator
- Customizable length (4–64 characters)
- Toggle uppercase, digits, and symbols
- Batch generation (up to 20 at once)
- Real-time strength evaluation with color-coded indicators
- One-click copy to clipboard

### 🔒 Hash Generator
- MD5, SHA-1, SHA-256, SHA-512 hashing
- Instant computation for any text input

### 📊 System Monitor
- CPU, memory, and disk usage with live meters
- Process count and network statistics
- Color-coded alerts for high resource usage

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Frontend** | HTML, CSS, JavaScript |
| **Security** | hashlib, secrets (SystemRandom) |
| **Design** | Dark purple theme, tabbed interface |

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/Balajireddypothapu/pyautomate.git
cd pyautomate

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Open **http://localhost:5002** in your browser.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze-text` | Analyze text (word count, readability, etc.) |
| `POST` | `/api/generate-password` | Generate secure passwords |
| `POST` | `/api/hash` | Compute MD5, SHA-1, SHA-256, SHA-512 |
| `GET` | `/api/system-stats` | Get system resource statistics |
| `POST` | `/api/analyze-dir` | Analyze directory structure |

## 📸 Screenshots

> Screenshots will be added after deployment.

## 📜 License

MIT License
