from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from transformers import pipeline
import re, os, json

# 1. Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Function to create vector DB from a single document
def create_vectorstore_from_text(document_text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(document_text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# 3. Function to use similarity search to get relevant chunks and extract info via LLM
llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=256)

def extract_fields_with_llm(document_text: str) -> dict:
    try:
        # Use full document if short, else do similarity search
        use_full_text = len(document_text) < 2000
        if use_full_text:
            combined_context = document_text
        else:
            vectorstore = create_vectorstore_from_text(document_text)
            query = "What is the national ID and action mentioned in the legal document?"
            top_docs = vectorstore.similarity_search(query, k=3)
            combined_context = "\n".join([doc.page_content for doc in top_docs])

        # New prompt to enforce strict JSON output
        prompt = f"""
Extract the following information from the legal court document below:
- National ID (must be exactly a 10-digit number found in the text)
- Action (must be either "freeze_funds" or "release_funds", based on phrases like 'freeze all associated bank accounts' or 'release funds')

Respond **only** in a single-line JSON like this:
{{"national_id": "", "action": "freeze_funds"}}

Document:
{combined_context}
"""

        result = llm_pipeline(prompt)[0]['generated_text']
        # print("LLM Output:", result)

        # Extract JSON-like content
        json_match = re.search(r'"national_id"\s*:\s*"\d{10}".*?"action"\s*:\s*"[a-zA-Z_]+"', result, re.DOTALL)
        if json_match:
            json_str = "{" + json_match.group() + "}"
            data = json.loads(json_str)
            return {
                "national_id": data.get("national_id", ""),
                "action": data.get("action", "")
            }

        # Fallback regex if LLM failed to return expected format
        national_id_match = re.search(r'\b\d{10}\b', combined_context)
        action_match = re.search(r'(freeze all associated bank accounts|release all associated bank accounts|immediately frozen|immediately released)', combined_context, re.IGNORECASE)

        action_map = {
            "freeze all associated bank accounts": "freeze_funds",
            "release all associated bank accounts": "release_funds",
            "immediately frozen":"freeze_funds",
            "immediately released":"release_funds"
        }

        national_id = national_id_match.group(0) if national_id_match else ""
        action_phrase = action_match.group(0).lower() if action_match else ""
        action = action_map.get(action_phrase, "")

        return {
            "national_id": national_id,
            "action": action
        }

    except Exception as e:
        print("Extraction failed:", e)

    return {
        "national_id": "",
        "action": ""
    }
















