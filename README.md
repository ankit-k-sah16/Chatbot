# 🤖 LangGraph + LangChain Stateful AI Chatbot

A **stateful conversational AI chatbot** built with **LangGraph, LangChain, Groq Cloud, and Streamlit**.

This project goes beyond a basic LLM chatbot by implementing **thread-based conversations, real-time response streaming, conversation state management, checkpointing, and persistent chat history using SQLite3**.

The chatbot uses **Groq Cloud** to access the `openai/gpt-oss-120b` model and provides an interactive **Streamlit** interface for chatting and managing previous conversations.

---

## ✨ Features

### 💬 Conversational AI
- Powered by the `openai/gpt-oss-120b` model through Groq Cloud.
- Maintains context across messages within a conversation.
- Supports natural multi-turn conversations.

### 🧵 Thread-Based Conversations
- Every conversation is assigned a unique `thread_id`.
- Different conversations are isolated from one another.
- Users can create multiple independent chat sessions.

### ⚡ Real-Time Streaming
- LLM responses are streamed to the UI instead of waiting for the entire response.
- Provides a more responsive and interactive chatbot experience.

### 🧠 LangGraph State Management
- Uses `StateGraph` to define the chatbot workflow.
- Conversation messages are maintained as part of the graph state.
- LangGraph manages the flow between the chatbot's nodes.

### 💾 Persistent Conversation History
- SQLite3 is used to store conversation information.
- Previous conversations can be retrieved after restarting the application.
- Users can select an earlier conversation and continue chatting from where they left off.

### 🔄 Conversation Checkpointing
- LangGraph checkpointing is used to persist graph state associated with conversation threads.
- Each thread maintains its own conversation state.
- The `thread_id` acts as the identifier used to retrieve and continue a conversation. LangGraph's persistence model organizes checkpoints by threads for this purpose. citeturn0search4turn0search8

### 🎨 Streamlit Interface
- Interactive chat interface.
- Sidebar for previous conversations.
- New Chat functionality.
- Chat messages displayed using Streamlit's chat components.
- Streaming assistant responses.

### 🔐 Secure API Key Management
- Groq API credentials are not hardcoded into the application.
- Local development can use environment variables / `.env`.
- Streamlit Community Cloud can use its built-in Secrets management. Streamlit recommends keeping credentials outside the repository. citeturn0search0turn0search7

---

# 🏗️ Architecture

The high-level flow of the application is:

```text
                    ┌──────────────────────┐
                    │      User            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    └──────────┬───────────┘
                               │
                         thread_id
                               │
                               ▼
                    ┌──────────────────────┐
                    │     LangGraph        │
                    │     StateGraph       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Chat Node        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      LangChain       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Groq Cloud      │
                    │ openai/gpt-oss-120b  │
                    └──────────┬───────────┘
                               │
                        Streaming Response
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    └──────────────────────┘

                               │
                               ▼
                    ┌──────────────────────┐
                    │      SQLite3         │
                    │ Persistent History   │
                    └──────────────────────┘
```

---

# 🧠 How Conversation Memory Works

The chatbot uses **thread IDs** to separate individual conversations.

For example:

```text
Thread 1
├── User: Hello
├── AI: Hi! How can I help?
├── User: Explain LangGraph
└── AI: LangGraph is...

Thread 2
├── User: What is Python?
└── AI: Python is...
```

Each conversation receives its own unique `thread_id`.

When the user switches to an earlier conversation, the application retrieves the associated messages and restores them to the Streamlit interface.

LangGraph's persistence system uses a thread identifier to organize and retrieve checkpointed state. citeturn0search8

---

# 💾 SQLite Persistence

The project initially used an in-memory checkpointing approach during development.

The application was later extended with **SQLite3 persistence** so that conversation information can survive application restarts and be retrieved from previous sessions.

The persistence layer allows the application to:

```text
Create Chat
     ↓
Generate thread_id
     ↓
Store conversation
     ↓
Save to SQLite
     ↓
Application restart
     ↓
Load previous threads
     ↓
Resume conversation
```

This makes the chatbot closer to a real-world conversational application rather than a simple stateless LLM interface.

---

# ⚡ Streaming

The chatbot uses LangGraph's streaming capabilities to display responses as they are generated.

Conceptually:

```python
for message_chunk, metadata in chatbot.stream(
    input_data,
    config=config,
    stream_mode="messages"
):
    # Display generated content
```

Instead of:

```text
User → Wait → Complete response
```

the experience becomes:

```text
User
 ↓
LLM starts generating
 ↓
Token/message chunks
 ↓
Streamlit displays chunks
 ↓
Complete response
```

This creates a much more responsive user experience.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **LangChain** | LLM application framework and model integration |
| **LangGraph** | Stateful graph-based workflow orchestration |
| **Groq Cloud** | LLM inference |
| **GPT-OSS 120B** | Language model |
| **Streamlit** | Frontend / user interface |
| **SQLite3** | Persistent conversation storage |
| **python-dotenv** | Local environment variable management |

---

# 📂 Project Structure

A typical project structure looks like:

```text
LangGraph_Chatbot/
│
├── backend1.py
│
├── streamlit_frontend_threading.py
│
├── chatbot.db
│
├── requirements.txt
│
├── .env
│
├── .gitignore
│
└── README.md
```

> Your exact filenames may differ depending on your implementation.

### `backend1.py`

Contains the chatbot backend, including:

- LangGraph `StateGraph`
- Chat state definition
- Chat node
- Groq LLM configuration
- Checkpointer
- Graph compilation

### `streamlit_frontend_threading.py`

Contains the Streamlit application:

- Chat interface
- Thread management
- Previous conversations
- New Chat functionality
- Conversation loading
- Streaming responses

### `chatbot.db`

SQLite database used for persistent conversation storage.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repository>.git
```

Navigate into the project:

```bash
cd LangGraph_Chatbot
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

# 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, the main dependencies are:

```text
streamlit
langchain
langchain-groq
langgraph
python-dotenv
```

SQLite3 is included with standard Python installations, so it generally does not need to be installed separately.

---

# 🔑 4. Configure the Groq API Key

Create a `.env` file for local development:

```env
GROQ_API_KEY=your_groq_api_key
```

Then load it in Python:

```python
from dotenv import load_dotenv

load_dotenv()
```

The API key should **never be committed to GitHub**.

Add the following to `.gitignore`:

```text
.env
.streamlit/secrets.toml
```

For Streamlit Community Cloud, configure the secret through the app's Secrets settings instead of committing credentials to the repository. citeturn0search7turn0search6

---

# ▶️ 5. Run the Application

Start the Streamlit application:

```bash
streamlit run streamlit_frontend_threading.py
```

The application should open in your browser.

---

# ☁️ Deployment

This project can be deployed using **Streamlit Community Cloud**.

Basic deployment workflow:

```text
GitHub Repository
       ↓
Connect Repository
       ↓
Select Streamlit Entry File
       ↓
Configure Dependencies
       ↓
Add GROQ_API_KEY Secret
       ↓
Deploy
```

For Community Cloud, add your Groq API key through the application's Secrets settings rather than committing it to GitHub. Streamlit provides a dedicated secrets-management mechanism for deployed apps. citeturn0search7

Example secret:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

---

# 🔐 Security

Never commit API keys or other credentials to the repository.

### `.gitignore`

Your `.gitignore` should include:

```text
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
venv/
.env
```

If an API key is accidentally exposed publicly, revoke it and generate a new one.

---

# 🧩 Core LangGraph Workflow

The chatbot workflow is conceptually:

```text
START
  │
  ▼
Chat Node
  │
  ▼
LLM
  │
  ▼
END
```

The graph state contains the conversation messages.

A simplified state definition:

```python
class ChatbotState(TypedDict):
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]
```

The `add_messages` reducer allows messages returned by the chatbot node to be incorporated into the existing message state.

The graph is then compiled with a checkpointer:

```python
graph = StateGraph(ChatbotState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(
    checkpointer=checkpoint
)
```

`StateGraph` is designed around nodes that read and write shared graph state, and the compiled graph supports execution and streaming methods. citeturn0search11

---

# 🧵 Thread Configuration

Each conversation receives a unique thread ID:

```python
config = {
    "configurable": {
        "thread_id": thread_id
    }
}
```

The thread ID allows LangGraph's persistence system to associate graph state with a specific conversation. citeturn0search4

This enables the application to maintain separate conversations:

```text
thread_001 → Conversation A

thread_002 → Conversation B

thread_003 → Conversation C
```

---

# 📸 Screenshots

Add screenshots of your application here.

Example:

```markdown
## 📸 Screenshots

### Chat Interface

![Chat Interface](screenshots/chat-interface.png)

### Previous Conversations

![Previous Conversations](screenshots/previous-conversations.png)
```

Recommended screenshots:

- Main chatbot interface
- Streaming response
- Previous conversation sidebar
- Multiple thread conversations
- Resuming an earlier conversation

---

# 🌟 Key Learning Outcomes

Building this project helped me understand several important concepts in modern LLM application development:

- Building conversational applications with LangChain
- Designing stateful workflows using LangGraph
- Working with `StateGraph`
- Managing conversation state
- Understanding thread-based persistence
- Implementing streaming LLM responses
- Integrating Groq Cloud models
- Building interactive AI applications with Streamlit
- Persisting application data with SQLite3
- Managing API credentials securely
- Deploying LLM applications using Streamlit Community Cloud

---

# 🔮 Future Improvements

Some planned improvements for the project include:

- [ ] RAG-based document question answering
- [ ] Tool calling
- [ ] Web search integration
- [ ] Agentic workflows
- [ ] Multiple AI agents
- [ ] File/document uploads
- [ ] User authentication
- [ ] Long-term user memory
- [ ] Improved database architecture
- [ ] Conversation search
- [ ] Message editing/deletion
- [ ] LangSmith tracing and observability
- [ ] Production-grade persistent checkpointing

---

# 🎯 Project Goals

The primary goal of this project is to understand how to build **stateful and persistent LLM applications** rather than simple prompt-and-response interfaces.

The project is also part of my ongoing exploration of:

```text
LLMs
 ↓
LangChain
 ↓
LangGraph
 ↓
Stateful Applications
 ↓
RAG
 ↓
Tool Calling
 ↓
AI Agents
 ↓
Multi-Agent Systems
```

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If you'd like to contribute:

```bash
git clone https://github.com/ankit-k-sah16/Chatbot
cd LangGraph_Chatbot
```

Create a new branch:

```bash
git checkout -b feature/your-feature
```

Commit your changes:

```bash
git add .
git commit -m "Add new feature"
```

Push the branch:

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📄 License

This project is available under the **MIT License**.

See the `LICENSE` file for more information.

---

# 👨‍💻 Author

**Ankit**

AI & ML Enthusiast

Interested in:

- Generative AI
- LLM Applications
- LangChain
- LangGraph
- RAG
- Agentic AI
- Machine Learning
- Data Science

---

# ⭐ Support

If you found this project interesting or useful, consider giving the repository a ⭐ on GitHub!

It helps support the project and motivates me to keep building and learning. 🚀

---

## 🔗 Project Links

**GitHub:**  
`https://github.com/ankit-k-sah16/Chatbot`

**Live Demo:**  
`<your-streamlit-community-cloud-url>`

**LinkedIn:**  
`<your-linkedin-profile>`

---
<img width="1920" height="1080" alt="Screenshot 2026-09-05 014201" src="https://github.com/user-attachments/assets/4d4b635e-c5a4-44a5-8a3e-4fa931abf6f3" />
<img width="1920" height="1080" alt="Screenshot 2026-09-10 000640" src="https://github.com/user-attachments/assets/b2b9569b-272e-4f81-ac62-8eaef8af6205" />

## 🏷️ Tags

`#Python` `#LangChain` `#LangGraph` `#GenerativeAI` `#LLM` `#AI` `#ArtificialIntelligence` `#AgenticAI` `#Streamlit` `#Groq` `#SQLite` `#MachineLearning` `#AIEngineering`
