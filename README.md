# 🔐 LLM-Powered JSON-LD Anomaly Detection for Cybersecurity

This project is a research-driven application that uses a Large Language Model (LLM) to detect anomalies in structured forensic data formats (like JSON-LD) commonly found in cybersecurity investigations.

Built with **FastAPI**, **FAISS**, **Sentence Transformers**, and run locally using **Mistral via Ollama**, this system offers an explainable, efficient, and scalable way to analyze thousands of log records and pinpoint unusual patterns without relying on predefined rules.

---

## 📌 Key Features

* ✅ **Upload and analyze JSON-LD files**
* ✅ **LLM-based anomaly detection using Mistral (Ollama)**
* ✅ **Automatic record compression and pattern grouping**
* ✅ **RAG (Retrieval-Augmented Generation)** using FAISS + LangChain
* ✅ **Strict response formatting** (Anomaly Detected: True/False + Description)
* ✅ Runs 100% **locally**, no external LLM calls

---

## 🧠 Use Case

Forensic analysts and cyber researchers often deal with thousands of structured records like MFT, USNJRNL, or EventLogs in UCO-based JSON-LD formats. This system:

* Groups repetitive records (e.g., same timestamp/event type)
* Compresses content into semantic summaries
* Sends it to an LLM with forensic case patterns retrieved from a knowledge base
* Gets back structured, explainable anomaly decisions

---

## 📁 Project Structure

```
rag-anomaly-detector/
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── routers/
│   │   └── analyze.py        # File upload + trigger analysis
│   ├── services/
│   │   ├── parser_service.py # JSON-LD parsing and compression
│   │   ├── rag_service.py    # FAISS retrieval + Mistral prompt
│   │   └── embedding_service.py # Document embedding for KB
│   ├── models/               # (Optional Pydantic schemas)
│   └── utils/                # File handlers, helpers
├── vectorstore/              # Saved FAISS index
├── documents/                # USECASE 1 & 2 .docx files
├── uploads/                  # Uploaded user files
├── embed_docs.py             # One-time KB embedding
├── requirements.txt
├── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourname/rag-anomaly-detector.git
cd rag-anomaly-detector
```

### 2. Set up a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# or
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 3. Pull Mistral via Ollama

```bash
ollama pull mistral
```

### 4. Run document embedding

```bash
python embed_docs.py
```

### 5. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to test the API.

---

## 📥 How It Works

1. User uploads a `.jsonld` file via `/api/analyze`
2. The file is parsed and grouped by `(timestamp, eventType)`
3. Repetitive records are collapsed to semantic summaries
4. Relevant forensic patterns are retrieved from embedded case documents using FAISS
5. A structured prompt is sent to Mistral
6. Mistral responds using a strict format:

   ```
   Anomaly Detected : True
   Description: ...
   ```
7. Response is returned via API

---

## 📌 Prompt Format Used

```
You are a digital forensic analyst.

Here is forensic event data extracted from a JSON-LD file uploaded by the user:
---
<compressed_record_summary>
---

Here are known forensic patterns from previous cases this is a knowledge-base for you.
As this is a knowledge-base use these only as general references, not as facts in your explanation:
---
<retrieved_context_from_FAISS>
---

Now, can you identify any anomalies in the json-ld file uploaded by the user?
If yes, explain clearly, and do not mention anything from the knowledge-base. Stick to inferencing.

Output format:
Anomaly Detected : True/False
Description: ...
```

---

## ⚠️ Limitations

* Only supports `.jsonld` files for now
* Requires manual embedding of new knowledge base documents
* Model context window limit (\~8K for Mistral)

---

## 🔮 Future Improvements

* GUI with Streamlit for interactive uploads
* CSV/Docx support
* Anomaly explanation with source facet IDs
* Run on high-context models (Claude, GPT-4 Turbo)
* Add rule-based validation layer pre-LLM

---

## 👨‍💻 Author

**Aldric Pinto**
