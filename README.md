Court Order Automation using GenAI and LangGraph

This project automates the manual process of interpreting and executing court orders received as scanned PDFs. It uses OCR, LLMs, retrieval-augmented generation (RAG), and LangGraph to extract actionable insights and perform validations before executing placeholder actions.

Features:

Accepts scanned court order PDFs.

Extracts National ID and Action using OCR and LLM.

Validates National ID against a customer database (customers.csv).

Validates Action against an allowed list (actions.csv).

Executes a dummy function if both fields are valid.

Exposes a FastAPI backend with:

"/" : HTML UI to upload a PDF

"/process_doc" : API endpoint to process the document

Provides a simple web interface to upload documents and view the result.

Tech Stack:

FastAPI – REST API server

LangGraph – Agentic framework for GenAI workflows

LangChain – LLM-based document parsing and retrieval

FAISS – Vector store for semantic document search

Tesseract OCR (via pytesseract) – Extracts text from scanned PDFs

PyMuPDF – PDF parsing

Open-source embedding model – Used for RAG over court documents