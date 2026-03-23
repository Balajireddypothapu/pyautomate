"""
PyAutomate — Python Automation Toolkit
A collection of automation scripts for file management, data processing,
and system monitoring with a web-based dashboard.
"""

from flask import Flask, render_template, jsonify, request
import os
import json
import csv
import hashlib
import re
from datetime import datetime, timedelta
from collections import Counter
import random
import io

app = Flask(__name__)

# ─── File Analyzer Module ────────────────────────────────────────

class FileAnalyzer:
    """Analyze directory structure and file statistics."""
    
    CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".pptx"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs", ".ts", ".jsx", ".tsx"],
        "Data": [".json", ".csv", ".xml", ".yaml", ".yml", ".sql", ".db", ".sqlite"],
        "Media": [".mp3", ".mp4", ".wav", ".avi", ".mkv", ".mov", ".flac"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    }
    
    @staticmethod
    def analyze_directory(path):
        """Analyze a directory and return statistics."""
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0,
            "categories": {cat: {"count": 0, "size": 0} for cat in FileAnalyzer.CATEGORIES},
            "other": {"count": 0, "size": 0},
            "extensions": Counter(),
            "largest_files": [],
            "recent_files": [],
        }
        
        all_files = []
        
        for root, dirs, files in os.walk(path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            stats["total_dirs"] += len(dirs)
            
            for fname in files:
                if fname.startswith("."):
                    continue
                    
                filepath = os.path.join(root, fname)
                try:
                    size = os.path.getsize(filepath)
                    mtime = os.path.getmtime(filepath)
                except OSError:
                    continue
                
                stats["total_files"] += 1
                stats["total_size"] += size
                
                ext = os.path.splitext(fname)[1].lower()
                stats["extensions"][ext] += 1
                
                # Categorize
                categorized = False
                for cat, exts in FileAnalyzer.CATEGORIES.items():
                    if ext in exts:
                        stats["categories"][cat]["count"] += 1
                        stats["categories"][cat]["size"] += size
                        categorized = True
                        break
                
                if not categorized:
                    stats["other"]["count"] += 1
                    stats["other"]["size"] += size
                
                all_files.append({
                    "name": fname,
                    "path": os.path.relpath(filepath, path),
                    "size": size,
                    "modified": datetime.fromtimestamp(mtime).isoformat(),
                    "extension": ext,
                })
        
        # Sort for largest and most recent
        stats["largest_files"] = sorted(all_files, key=lambda x: x["size"], reverse=True)[:10]
        stats["recent_files"] = sorted(all_files, key=lambda x: x["modified"], reverse=True)[:10]
        stats["extensions"] = dict(stats["extensions"].most_common(15))
        
        return stats


# ─── Text Processor Module ───────────────────────────────────────

class TextProcessor:
    """Text analysis and processing utilities."""
    
    @staticmethod
    def analyze_text(text):
        """Analyze text content and return statistics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Word frequency
        word_freq = Counter(w.lower().strip('.,!?;:"\'-()[]{}') for w in words)
        
        # Character frequency
        char_freq = Counter(c.lower() for c in text if c.isalpha())
        
        # Readability (Flesch-Kincaid approximation)
        syllables = sum(TextProcessor._count_syllables(w) for w in words)
        if len(words) > 0 and len(sentences) > 0:
            fk_grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
        else:
            fk_grade = 0
        
        return {
            "characters": len(text),
            "characters_no_spaces": len(text.replace(" ", "").replace("\n", "")),
            "words": len(words),
            "sentences": len(sentences),
            "paragraphs": len(paragraphs),
            "avg_word_length": round(sum(len(w) for w in words) / max(len(words), 1), 1),
            "avg_sentence_length": round(len(words) / max(len(sentences), 1), 1),
            "unique_words": len(set(w.lower() for w in words)),
            "vocabulary_richness": round(len(set(w.lower() for w in words)) / max(len(words), 1) * 100, 1),
            "readability_grade": round(max(fk_grade, 0), 1),
            "top_words": dict(word_freq.most_common(20)),
            "reading_time_min": round(len(words) / 200, 1),
        }
    
    @staticmethod
    def _count_syllables(word):
        """Estimate syllable count."""
        word = word.lower().strip('.,!?;:"\'-()[]{}')
        if len(word) <= 3:
            return 1
        count = len(re.findall(r'[aeiouy]+', word))
        if word.endswith('e'):
            count -= 1
        return max(count, 1)


# ─── Password Generator Module ───────────────────────────────────

class PasswordGenerator:
    """Generate secure passwords with customizable rules."""
    
    LOWER = "abcdefghijklmnopqrstuvwxyz"
    UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS = "0123456789"
    SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    @staticmethod
    def generate(length=16, use_upper=True, use_digits=True, use_symbols=True, count=1):
        """Generate secure passwords."""
        charset = PasswordGenerator.LOWER
        if use_upper:
            charset += PasswordGenerator.UPPER
        if use_digits:
            charset += PasswordGenerator.DIGITS
        if use_symbols:
            charset += PasswordGenerator.SYMBOLS
        
        passwords = []
        for _ in range(count):
            pwd = ''.join(random.SystemRandom().choice(charset) for _ in range(length))
            strength = PasswordGenerator._check_strength(pwd)
            passwords.append({"password": pwd, "strength": strength})
        
        return passwords
    
    @staticmethod
    def _check_strength(pwd):
        """Evaluate password strength."""
        score = 0
        if len(pwd) >= 8: score += 1
        if len(pwd) >= 12: score += 1
        if len(pwd) >= 16: score += 1
        if re.search(r'[a-z]', pwd): score += 1
        if re.search(r'[A-Z]', pwd): score += 1
        if re.search(r'[0-9]', pwd): score += 1
        if re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]', pwd): score += 1
        
        if score <= 3: return {"label": "Weak", "color": "#f44336", "score": score}
        if score <= 5: return {"label": "Moderate", "color": "#ff9800", "score": score}
        return {"label": "Strong", "color": "#4caf50", "score": score}


# ─── System Monitor Module ────────────────────────────────────────

class SystemMonitor:
    """Monitor system resources (simulated for portability)."""
    
    @staticmethod
    def get_stats():
        """Get system statistics."""
        random.seed(int(datetime.now().timestamp()) // 5)  # Update every 5 seconds
        
        return {
            "cpu_percent": round(random.uniform(5, 75), 1),
            "memory": {
                "total_gb": 16.0,
                "used_gb": round(random.uniform(6, 12), 1),
                "percent": round(random.uniform(40, 80), 1),
            },
            "disk": {
                "total_gb": 512,
                "used_gb": round(random.uniform(150, 350), 1),
                "percent": round(random.uniform(30, 70), 1),
            },
            "network": {
                "bytes_sent_mb": round(random.uniform(100, 5000), 1),
                "bytes_recv_mb": round(random.uniform(500, 15000), 1),
            },
            "uptime_hours": round(random.uniform(1, 720), 1),
            "processes": random.randint(150, 400),
            "timestamp": datetime.now().isoformat(),
        }


# ─── Resume Analyzer Module ──────────────────────────────────────

class ResumeAnalyzer:
    """Analyze resumes against job descriptions for keywords."""
    
    @staticmethod
    def analyze(resume_text, job_desc):
        """Find common keywords and identifies missing ones."""
        def get_keywords(text):
            # Simple keyword extraction (words > 3 chars, lowercase)
            words = re.findall(r'\b[a-z]{4,}\b', text.lower())
            # Filter out common stop words (simplified list)
            stops = {'with', 'from', 'that', 'this', 'your', 'have', 'been', 'which', 'about', 'their'}
            return set(w for w in words if w not in stops)

        resume_keys = get_keywords(resume_text)
        job_keys = get_keywords(job_desc)
        
        found = resume_keys.intersection(job_keys)
        missing = job_keys.difference(resume_keys)
        
        # Sort and limit
        found = sorted(list(found))[:20]
        missing = sorted(list(missing))[:20]
        
        match_score = round(len(resume_keys.intersection(job_keys)) / max(len(job_keys), 1) * 100)
        
        return {
            "match_score": match_score,
            "found_keywords": found,
            "missing_keywords": missing,
            "resume_count": len(resume_keys),
            "job_count": len(job_keys)
        }

# ─── Routes ──────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    data = request.json
    resume = data.get("resume", "")
    job_desc = data.get("job_desc", "")
    if not resume.strip() or not job_desc.strip():
        return jsonify({"error": "Both resume and job description are required"}), 400
    result = ResumeAnalyzer.analyze(resume, job_desc)
    return jsonify(result)


@app.route("/api/analyze-dir", methods=["POST"])
def analyze_dir():
    data = request.json
    path = data.get("path", os.path.expanduser("~"))
    if not os.path.isdir(path):
        return jsonify({"error": f"Path '{path}' is not a valid directory"}), 400
    result = FileAnalyzer.analyze_directory(path)
    return jsonify(result)


@app.route("/api/analyze-text", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400
    result = TextProcessor.analyze_text(text)
    return jsonify(result)


@app.route("/api/generate-password", methods=["POST"])
def generate_password():
    data = request.json or {}
    passwords = PasswordGenerator.generate(
        length=data.get("length", 16),
        use_upper=data.get("uppercase", True),
        use_digits=data.get("digits", True),
        use_symbols=data.get("symbols", True),
        count=data.get("count", 5),
    )
    return jsonify({"passwords": passwords})


@app.route("/api/system-stats")
def system_stats():
    return jsonify(SystemMonitor.get_stats())


@app.route("/api/hash", methods=["POST"])
def compute_hash():
    data = request.json
    text = data.get("text", "")
    return jsonify({
        "md5": hashlib.md5(text.encode()).hexdigest(),
        "sha1": hashlib.sha1(text.encode()).hexdigest(),
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "sha512": hashlib.sha512(text.encode()).hexdigest(),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5002)
