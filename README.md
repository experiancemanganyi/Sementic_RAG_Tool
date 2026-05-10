================================================================================
                    RAG DOCUMENT QUESTION & ANSWER SYSTEM
================================================================================

A powerful Retrieval-Augmented Generation (RAG) system that allows you to chat 
with your PDF documents. Ask questions in natural language and get accurate 
answers with source citations pointing to specific documents and page numbers.

================================================================================
                                FEATURES
================================================================================

✓ PDF Processing - Automatically reads and chunks PDF documents
✓ Semantic Search - Uses OpenAI embeddings for intelligent document retrieval
✓ Source Attribution - Every answer includes document name and page number
✓ Interactive Web UI - Clean Streamlit interface for easy interaction
✓ REST API - FastAPI endpoint for programmatic access and webhook integration
✓ Remote Access - Share via ngrok tunnel (works from anywhere, any network)
✓ Local Storage - No database needed, everything runs locally
✓ Cross-Platform - Works on Windows, Mac, and Linux

================================================================================
                              TECH STACK
================================================================================

- Python 3.8+
- FastAPI - REST API framework
- Streamlit - Web user interface
- OpenAI GPT - Language model for answers
- OpenAI Embeddings - Vector search
- PyPDF - PDF text extraction
- ngrok - Public URL tunneling

================================================================================
                            QUICK START GUIDE
================================================================================

STEP 1: INSTALL DEPENDENCIES
-------------------------------------------------------------------------------
pip install fastapi uvicorn streamlit openai pypdf python-dotenv numpy pyngrok

STEP 2: SETUP OPENAI API KEY
-------------------------------------------------------------------------------
Create a file named .env in the project folder with:
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

STEP 3: ADD YOUR PDF DOCUMENTS
-------------------------------------------------------------------------------
Create a folder named "data" and put all your PDF files inside it

STEP 4: PROCESS THE PDFs
-------------------------------------------------------------------------------
python local_rag.py

This reads all PDFs, splits them into chunks, generates embeddings, and saves 
everything to rag_data.pkl (only needed once, or when you add new PDFs)

STEP 5: RUN THE APPLICATION
-------------------------------------------------------------------------------
python tunnel.py

This starts both the API server and ngrok tunnel simultaneously.

================================================================================
                          WAYS TO USE THE SYSTEM
================================================================================

METHOD 1: WEB INTERFACE (Streamlit)
-------------------------------------------------------------------------------
Command: streamlit run app.py
Access: http://localhost:8501

Provides a chat-like interface where you can type questions and see answers
with sources displayed in an expandable format.

METHOD 2: REST API (FastAPI)
-------------------------------------------------------------------------------
Command: uvicorn api:app --host 0.0.0.0 --port 8000
Access: http://localhost:8000/docs (interactive documentation)

Useful for integrating with other applications, webhooks, or automation.

METHOD 3: PUBLIC ACCESS (ngrok)
-------------------------------------------------------------------------------
Command: python tunnel.py
Access: https://your-url.ngrok-free.dev/my_rag

Share this URL with anyone - they can access your RAG system from anywhere,
even on different networks or countries!

================================================================================
                              API DOCUMENTATION
================================================================================

ENDPOINT
-------------------------------------------------------------------------------
POST /my_rag

REQUEST HEADERS
-------------------------------------------------------------------------------
Content-Type: application/json

REQUEST BODY
-------------------------------------------------------------------------------
{
    "question": "What is this document about?"
}

RESPONSE EXAMPLE
-------------------------------------------------------------------------------
{
    "question": "What is this document about?",
    "answer": "The document discusses the fundamentals of machine learning...",
    "sources": [
        {
            "source": "machine_learning.pdf",
            "page": 5,
            "content": "Machine learning is a subset of artificial intelligence..."
        },
        {
            "source": "ai_basics.pdf",
            "page": 12,
            "content": "Neural networks are inspired by the human brain..."
        }
    ]
}

STATUS CODES
-------------------------------------------------------------------------------
200 - Success
500 - Server error (check API key or document loading)

================================================================================
                          TESTING THE API
================================================================================

Using PowerShell (Windows):
-------------------------------------------------------------------------------
$body = @{question="What is RAG?"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/my_rag" -Method POST -Body $body -ContentType "application/json"

Using curl (Mac/Linux/Windows):
-------------------------------------------------------------------------------
curl -X POST http://localhost:8000/my_rag -H "Content-Type: application/json" -d "{\"question\": \"test\"}"

Using Python:
-------------------------------------------------------------------------------
import requests
response = requests.post("http://localhost:8000/my_rag", json={"question": "Hello"})
print(response.json())

Using Browser:
-------------------------------------------------------------------------------
Open http://localhost:8000/docs for interactive API testing

================================================================================
                          REMOTE ACCESS WITH NGROK
================================================================================

When you run python tunnel.py, you get a public URL like:
https://yachty-carmelita-hydromechanical.ngrok-free.dev/my_rag

HOW IT WORKS:
-------------------------------------------------------------------------------
ngrok creates a secure tunnel from the public internet to your local computer.
Requests to the public URL are forwarded to your local API on port 8080.

SHARING WITH OTHERS:
-------------------------------------------------------------------------------
Simply give them the public URL. They can:
- Send POST requests with questions
- Access /docs for interactive documentation
- Use from any network (different WiFi, cellular, different country)

LIMITATIONS (Free ngrok tier):
-------------------------------------------------------------------------------
- 40 connections per minute
- 1 GB bandwidth per month
- Random subdomain each restart (URL changes)
- Sufficient for testing and demos

For production: Upgrade ngrok or deploy to cloud (Render, Railway, AWS)

================================================================================
                              PROJECT STRUCTURE
================================================================================

RAG_Tool/
│
├── api.py              # FastAPI REST API endpoints
├── app.py              # Streamlit web interface
├── brain.py            # Core RAG logic (original)
├── local_rag.py        # PDF ingestion & embedding generator
├── local_brain.py      # Local vector search & answer generation
├── tunnel.py           # Combined API server + ngrok tunnel
├── rag.py              # Supabase connector (optional, for cloud storage)
├── chunk.py            # PDF chunking utility
├── query_RAG.py        # Command-line query tool
│
├── data/               # 📁 Place your PDF files here
│   └── your_document.pdf
│
├── .env                # 🔐 API keys (create this file)
├── requirements.txt    # Python dependencies
└── rag_data.pkl        # Generated file (embeddings storage)

================================================================================
                              FILE DESCRIPTIONS
================================================================================

api.py
    Contains FastAPI app with /my_rag endpoint. Handles HTTP requests and
    returns JSON responses with answers and sources.

app.py
    Streamlit web application. Provides chat interface, displays answers,
    and shows expandable source citations.

local_rag.py
    Run this first! Reads PDFs from "data" folder, chunks them into 500-character
    pieces with 50-character overlap, generates embeddings using OpenAI, and
    saves everything to rag_data.pkl.

local_brain.py
    Loads rag_data.pkl, handles similarity search using cosine similarity,
    builds context from relevant chunks, and calls OpenAI to generate answers.

tunnel.py
    Combines uvicorn API server and ngrok tunnel. Run this for external access.
    Starts API on port 8080 and creates public ngrok URL.

rag.py
    Optional Supabase connector. Use if you want cloud vector storage instead
    of local pickle file.

================================================================================
                              COMMAND REFERENCE
================================================================================

TASK                                COMMAND
-------------------------------------------------------------------------------
Install dependencies                pip install -r requirements.txt
Process PDFs (first time)           python local_rag.py
Reprocess PDFs (after adding new)   python local_rag.py
Run API only                        uvicorn api:app --host 0.0.0.0 --port 8000
Run API with auto-reload            uvicorn api:app --host 0.0.0.0 --port 8000 --reload
Run Streamlit UI                    streamlit run app.py
Run API + ngrok tunnel              python tunnel.py
Test API locally                    curl http://localhost:8000/docs
Check your IP address               ipconfig (Windows) or ifconfig (Mac/Linux)
Add Windows firewall rule           netsh advfirewall firewall add rule name="RAG_API" dir=in action=allow protocol=TCP localport=8000

================================================================================
                          TROUBLESHOOTING GUIDE
================================================================================

PROBLEM: ModuleNotFoundError: No module named 'xxx'
SOLUTION: pip install the missing module

PROBLEM: OpenAI API error - Invalid API key
SOLUTION: Check your .env file has correct OPENAI_API_KEY (no quotes, no spaces)

PROBLEM: No PDFs found
SOLUTION: Create "data" folder and add PDF files before running local_rag.py

PROBLEM: Other computer cannot connect (same network)
SOLUTION: 
  1. Add Windows firewall rule (see command reference above)
  2. Make sure API is running with --host 0.0.0.0
  3. Verify both computers on same WiFi/router

PROBLEM: Other computer cannot connect (different network)
SOLUTION: Use ngrok tunnel - run python tunnel.py and share the public URL

PROBLEM: ngrok authentication failed
SOLUTION: 
  1. Sign up for free account at https://ngrok.com
  2. Get your token from dashboard
  3. Add token to tunnel.py

PROBLEM: Answers are not accurate
SOLUTION: 
  1. Ensure PDFs are text-based (not scanned images)
  2. For scanned PDFs, install: pip install pytesseract pillow
  3. Try smaller chunk size in local_rag.py (change size=300)

PROBLEM: API is slow
SOLUTION: 
  1. Use smaller PDFs or fewer documents
  2. Reduce chunk count by increasing chunk size (size=1000)
  3. Use gpt-3.5-turbo instead of gpt-4

================================================================================
                                USE CASES
================================================================================

RESEARCH PAPERS
    Upload academic papers and ask questions about methodology, results, or
    conclusions. Get answers with exact page references.

LEGAL DOCUMENTS
    Quickly find specific clauses, definitions, or requirements in contracts,
    agreements, or legal briefs.

TECHNICAL MANUALS
    Ask questions about product specifications, troubleshooting steps, or
    installation procedures from documentation.

COMPANY POLICIES
    Chat with HR documents, employee handbooks, or policy manuals to quickly
    find information about benefits, procedures, or rules.

BOOKS AND TEXTBOOKS
    Upload entire books and ask questions about specific chapters, concepts,
    or characters.

CUSTOMER SUPPORT
    Answer customer questions from product documentation, FAQ documents, or
    knowledge bases.

================================================================================
                              HOW IT WORKS
================================================================================

1. PDF INGESTION (local_rag.py)
   - Reads all PDF files from the "data" folder
   - Extracts text from each page
   - Splits text into overlapping chunks (500 chars with 50 overlap)
   - Generates vector embeddings for each chunk using OpenAI
   - Saves chunks and embeddings to rag_data.pkl

2. QUESTION ANSWERING (local_brain.py)
   - User submits a question
   - Question is converted to embedding vector
   - System finds most similar document chunks using cosine similarity
   - Top 5 relevant chunks are retrieved
   - Chunks are compiled into context prompt
   - OpenAI generates answer based ONLY on provided context
   - Answer and sources are returned to user

3. API SERVER (api.py)
   - Listens for HTTP POST requests at /my_rag
   - Extracts question from request body
   - Calls ask() function from brain
   - Returns JSON response with answer and sources

4. NGROK TUNNEL (tunnel.py)
   - Starts FastAPI server on port 8080
   - Creates secure tunnel to public internet
   - Forwards all requests to local server
   - Provides public HTTPS URL

================================================================================
                            PERFORMANCE TIPS
================================================================================

✓ Keep PDFs under 50MB for best performance
✓ Use text-based PDFs (not scanned images)
✓ Process PDFs once, then reuse rag_data.pkl
✓ Restart API after adding new PDFs (re-run local_rag.py)
✓ For production, consider using vector database (Supabase, Pinecone)
✓ Use gpt-3.5-turbo for faster responses (gpt-4 is slower)

================================================================================
                                LICENSE
================================================================================

MIT License - Free for personal and commercial use

================================================================================
                                CONTACT
================================================================================

For issues or questions, please open an issue on GitHub or contact the maintainer.

================================================================================
                                ACKNOWLEDGMENTS
================================================================================

- OpenAI for embeddings and GPT models
- FastAPI for the excellent web framework
- Streamlit for the amazing UI library
- ngrok for public URL tunneling

================================================================================
                                  NOTES
================================================================================

• The first run of local_rag.py may take several minutes depending on PDF size
• API keys are stored in .env - never share this file or commit to GitHub
• Add .env to .gitignore to prevent accidental exposure
• Free ngrok URLs change each restart - upgrade for fixed subdomain
• For 24/7 operation, consider deploying to cloud platform (Render, Railway)

========================================================================================
                            END OF README
================================================================================
