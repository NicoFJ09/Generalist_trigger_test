# **Generalist_trigger_test Development Workflow**

---

## 1. **Project Bootstrap & Environment Setup**

- **Initialize the repo & environment:**  
  - Create repo/branch, add requirements, `.env` template, and skeleton structure.
- **Install/test dependencies:**  
  - Ensure `langgraph`, `composio`, `fastapi`, `uvicorn`, `rich`, and `python-dotenv` are all installed and import successfully.
- **Commit:**  
  - `chore: project scaffolding, requirements, deps verified`

---

## 2. **MCP/Email Authentication & Context Initialization**

- **Goal:**  
  - Authenticate with Composio MCP, connect to email provider, and initialize session/context storage.
- **Implementation Steps:**
  1. Implement MCP client setup (`composio` connection code).
  2. Set up context/memory store (even basic Python dict/JSON as placeholder).
  3. Validate authentication by printing a "logged in" and blank context at launch.
- **Testing:**  
  - Run with test keys, check email provider is linked, context/memory object is initialized.
- **Commit:**  
  - `feat: MCP authentication and context initialization`

---

## 3. **Inbox Fetching & Console Summarization**

- **Goal:**  
  - Fetch unread emails, show them in a readable Rich-styled console list.
- **Implementation Steps:**
  1. Implement inbox-fetch via MCP’s provided tool.
  2. Parse results, format to a neat table/list in the console using Rich.
  3. Add command-line prompt to refresh/fetch inbox on demand.
- **Testing:**  
  - Run fetch, confirm emails are shown and info is clear.
- **Commit:**  
  - `feat: fetch and summarize unread emails in terminal`

---

## 4. **Email Selection & Draft Proposal**

- **Goal:**  
  - Allow user to select emails, trigger AI draft for reply.
- **Implementation Steps:**
  1. Build CLI prompt for user to select emails (by number, etc).
  2. Use LangGraph to generate a draft reply for each selection (pass in email body/context).
  3. Display draft in the terminal.
- **Testing:**  
  - Pick emails, confirm AI produces sensible, context-aware drafts.
- **Commit:**  
  - `feat: user selects emails, agent drafts replies with AI`

---

## 5. **Draft Editing, Approval & Sending**

- **Goal:**  
  - Let user edit proposals, approve or discard. Send finalized replies via MCP.
- **Implementation Steps:**
  1. Prompt user (Y/N) to edit each draft (inline or with $EDITOR if time).
  2. Prompt user (Y/N) to send.
  3. Call MCP/send tool to dispatch reply.
  4. Update context/memory with sent thread/response.
- **Testing:**  
  - Run end-to-end: select email, see/edit draft, send, confirm delivery.
- **Commit:**  
  - `feat: interactive draft editing and sending via MCP`

---

## 6. **Webhook Trigger Integration for Automation**

- **Goal:**  
  - Enable auto-mode (agent listens for new emails/triggers and responds with minimal/no user input).
- **Implementation Steps:**
  1. Add FastAPI app in `triggers/trigger_manager.py` with endpoint to receive new email events.
  2. On trigger, fetch new email, pass to LangGraph, auto-draft, auto-send.
  3. Log all actions to console and memory/context.
- **Testing:**  
  - Use Composio to simulate trigger; check full automation works (email received → reply sent).
- **Commit:**  
  - `feat: FastAPI webhook trigger for full automation`

---

## 7. **User/Agent Settings, Command Improvements, Error Handling**

- Expose switch for manual/full-auto, user settings (reply style, triggers), CLI help.
- Add error handling/logging (auth failures, no new emails, network issues).
- Add `.env` loading via `python-dotenv`.
- **Commit:**  
  - `feat: settings, error handling, and workflow polish`
