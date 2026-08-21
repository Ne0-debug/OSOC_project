# Rights Navigator — RTI/Complaint Drafting Agent

**OOSC 4.0 Hackathon — Problem Statement 3: AI for Civic and Legal Empowerment**

## Problem & Solution

Filing an RTI (Right to Information) request or a tenant deposit complaint in India requires
navigating dense legal language and knowing exactly what a valid application needs — most
people don't know where to start, what to ask for, or how to word it correctly. **Rights
Navigator** is a conversational assistant that explains your rights in plain language (with
citations back to the actual legal text, so answers are trustworthy) and drafts a ready-to-file
document for you — either an RTI application under the RTI Act, 2005, or a tenant security
deposit complaint under the Model Tenancy Act, 2021.

**Scope for this prototype:** Delhi, two domains — RTI requests for public records, and tenant
deposit disputes.

## Team

| Name | Role |
|---|---|
| _[Name — A]_ | Domain & Product |
| _[Name — B]_ | Backend / AI |
| _[Name — C]_ | Frontend / Deploy |

## Architecture

- **Frontend:** Next.js + TypeScript + Tailwind, deployed on Vercel.
- **Backend:** FastAPI (Python), deployed on _[Render/Railway — fill in]_.
- **LLM:** Google Gemini (`gemini-3.6-flash`) via the `google.generativeai` SDK.
  > Note: the original project plan specified the Anthropic API — the team switched to
  > Gemini during Day 1 backend scaffolding. Functionality (retrieval, generation, structured
  > field extraction) is equivalent either way; this is noted here for transparency.
- **Retrieval:** No vector database — the source corpus (RTI Act + Model Tenancy Act excerpts)
  is small enough that a lightweight keyword-overlap scorer selects the most relevant chunks
  at query time, which are then passed directly into the LLM prompt as context. This was a
  deliberate scope decision, not a shortcut — it keeps the system simple and fully explainable
  for a small, fixed corpus.
- **Citations:** Every `/ask` response includes the source filename(s) it drew from, so answers
  are traceable back to the actual legal text rather than an unverifiable LLM guess.
- **Document generation:** Conversational input is passed to the LLM to extract structured
  fields (name, address, department, deposit amount, etc.), which are then used to fill a
  `.docx` template via `python-docx`. Missing fields are detected before generation and the API
  asks for the missing information instead of producing an incomplete document.

```
[Architecture diagram — insert Excalidraw export here, per Task 4.1]
```

## Setup & Run

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\Activate        # Windows PowerShell
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with:

```
GEMINI_API_KEY=your_key_here
```

Run the server:

```bash
uvicorn main:app --reload
```

The backend runs at `http://127.0.0.1:8000`. Key endpoints:
- `POST /ask` — `{ "query": "..." }` → cited answer from source text
- `POST /generate-document` — `{ "conversation": "...", "document_type": "rti" | "tenancy_complaint" }` → downloadable `.docx`, or a `needs_more_info` response if details are missing

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:3000` by default.

## Live Prototype

- **Live app:** _[Vercel URL — fill in]_
- **Backend API:** _[hosted backend URL — fill in]_

## Scope & Scalability

This prototype covers one state (Delhi) and two legal domains (RTI, tenant deposits). Adding a
third domain or a new state would **not** require rebuilding the system — it would mean:
1. Adding new cleaned, topic-labeled `.md` source files under `backend/docs_temp/chunks/`.
2. Defining a new required-fields schema (matching the pattern of `RTI_FIELDS` /
   `TENANCY_FIELDS` in `main.py`) and a corresponding `.docx` builder function.
3. No changes needed to the retrieval, citation, or extraction logic — those are domain-agnostic.

State-specific legal variations (e.g. state-level tenancy rules) would follow the same pattern:
new source files scoped to that state, without touching the core pipeline.

## Screenshots

_[Insert screenshots or a short GIF of the core ask → explain → draft → download flow here]_

## Known Limitations / Tech Debt

- `google.generativeai` (the Gemini SDK used here) is deprecated in favor of `google.genai`.
  Not migrated mid-hackathon — functional, but should be updated post-submission.
- Retrieval uses keyword overlap, not semantic search — sufficient for this small, fixed
  corpus, but would need a proper vector index if the corpus grows significantly.
- The required-fields schema (`RTI_FIELDS`, `TENANCY_FIELDS` in `main.py`) is a reasonable
  default written during development; not yet formally reconciled against a separately
  authored domain schema.

## Submission

- **Prototype:** _[live link]_
- **Repo:** _[GitHub link]_
- **Demo video:** _[link, ≤10 min]_
