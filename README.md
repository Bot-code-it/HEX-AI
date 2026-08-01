# HEX-AI
---

# Python Chatbot (Powered by Groq)

A lightweight, lightning-fast Python chatbot CLI powered by the **Groq API**. Built for simplicity, speed, and easy customization!

---

## ✨ Features

* **⚡ Blazing Fast:** Leverages Groq’s high-speed LPU infrastructure for near-instant responses.
* **🎯 Realtime information:** Can reply to any realtime query.
* **⚙️ Easily Configurable:** Simple setup and very-lightwieght.

---

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have Python 3.8+ installed and a Groq API key (you can get one at [console.groq.com](https://console.groq.com/keys)).

### 2. Installation

**Clone this repository and install requirements:**

```bash
git clone https://github.com/Bot-code-it/HEX-AI.git
```
```bash
python -r requirements.txt
```

### 3. Setup API key and Instructions

1. Copy your Groq API key from [console.groq.com](https://console.groq.com/keys), and paste it in the ```data/api.key``` file.

2. Write the instructions for AI in ```data/instructions.txt``` file or you can skip this step as basic instructions are already written in the file.

### 4. Run HEX-AI

Start chatting right from your terminal:

```bash
python main.py

```

---

## 🛠️ Tech Stack

* **Language:** Python
* **LLM Engine:** Groq API (`gpt-oss-20b`)
* **Dependencies:** `requests`, `pylatexenc`, `pyperclip` & `iso3166`
