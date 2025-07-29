# TimeMind 🧠

**Your personal productivity coach powered by hybrid artificial intelligence**

TimeMind is an advanced productivity application that combines local and remote AI agents to help you organize time, manage tasks, track habits, and improve your daily efficiency.

## ✨ Key Features

### 🤖 Hybrid AI Architecture
- **Local Agent**: Ollama + Llama3 for fast responses and privacy
- **Remote Agent**: Google Gemini for deep analysis and advanced capabilities
- **RAG System**: ChromaDB for personalized knowledge base

### 📋 Complete Task Management
- Create and organize tasks with priorities
- Time estimation and actual time tracking
- Customizable status (pending, completed)
- Task deletion and editing

### 🏃‍♂️ Habit Tracking
- Daily/weekly habit tracking
- Completion logging with notes
- Progress statistics
- Active/inactive habit management

### 🍅 Integrated Pomodoro Timer
- 25-minute Pomodoro sessions
- Direct task linking
- Productivity tracking
- Post-session notes

### 📊 Analytics and Reports
- Automatic daily summaries
- Completed task statistics
- Habit analysis
- Pomodoro performance

### 🔍 Intelligent Knowledge Base
- RAG system with semantic search
- Automatic embeddings with Gemini
- Expandable knowledge base
- Contextual search

## 🚀 Installation and Setup

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - [Download here](https://ollama.ai/)
3. **Google AI API Key** - [Get it here](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/timemind.git
cd timemind
```

2. **Install dependencies**
```bash
pip install ollama google-genai chromadb python-dotenv requests
```

3. **Setup Ollama**
```bash
# Install and start Ollama
ollama pull llama3
ollama serve
```

4. **API Configuration**
```bash
cp .env.example .env
# Modify .env with your API key
```

5. **Start TimeMind**
```bash
python timemind_main.py
```

## 📖 Usage Guide

### Task Management Commands
```bash
# Add a task
add task: Complete presentation

# View pending tasks
tasks

# View completed tasks
completed tasks

# Complete a task
complete: 1

# Delete a task
delete task: 2
```

### Habit Tracking Commands
```bash
# Add a habit
add habit: Read 30 minutes

# View habits
habits

# Log completion
log habit: 1

# Log non-completion
log habit: 1 false
```

### Pomodoro Commands
```bash
# Start generic session
pomodoro

# Start session for specific task
pomodoro: 1

# Complete session
complete pomodoro: 1
```

### Analytics Commands
```bash
# Daily summary
summary

# Knowledge base statistics
stats
```

### Knowledge Base Commands
```bash
# Search in knowledge base
search: pomodoro technique

# Add document
add knowledge: productivity_tips | Productivity tips content...

# Chat with remote agent
remote: Analyze my weekly productivity
```

## 🏗️ System Architecture

```
TimeMind/
├── timemind_main.py        # Main application
├── local_agent.py         # Local agent (Ollama)
├── remote_agent.py        # Remote agent (Gemini)
├── rag_system.py          # RAG system (ChromaDB)
├── database_manager.py    # SQLite database management
├── knowledge_base/        # Knowledge base folder
├── timemind_chroma/       # Vector database
├── timemind.db           # SQLite database
└── .env                  # API configuration
```

### Main Components

**TimeMindAgent**: Main orchestrator that coordinates all components

**LocalAgent**: Handles quick responses using Ollama and Llama3 locally

**RemoteAgent**: Provides advanced analysis through Google Gemini

**RAGSystem**: Retrieval system for personalized knowledge base

**DatabaseManager**: Persistent management of tasks, habits, Pomodoro sessions

## 🗄️ Database Schema

### Tasks
- `id`, `title`, `description`, `priority`, `status`
- `created_at`, `completed_at`, `estimated_minutes`, `actual_minutes`

### Habits
- `id`, `name`, `description`, `target_frequency`, `active`

### Habit Logs
- `id`, `habit_id`, `date`, `completed`, `notes`

### Pomodoro Sessions
- `id`, `task_id`, `start_time`, `end_time`, `duration_minutes`, `completed`

### Daily Reflections
- `id`, `date`, `morning_plan`, `evening_reflection`, `mood_score`

## 🔧 Advanced Configuration

### Custom Models

```python
# Change local model
agent.local_agent.set_model("llama3:70b")

# Change remote model
agent.remote_agent.set_model("gemini-pro")
```

### Custom Knowledge Base

1. Add `.txt` files to the `knowledge_base/` folder
2. The system will automatically index them
3. Use `search: query` to search content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Roadmap

- [ ] Web interface with FastAPI
- [ ] Calendar integration
- [ ] Data export/import
- [ ] Desktop notifications
- [ ] Advanced analytics with charts
- [ ] Slack/Discord integration
- [ ] Mobile app
- [ ] Cloud synchronization

## 🐛 Troubleshooting

### Common Issues

**Ollama not responding**
```bash
# Verify Ollama is running
ollama serve

# Check installed models
ollama list
```

**Gemini API error**
```bash
# Check API key in .env file
cat .env

# Test connection
python -c "from remote_agent import RemoteAgent; RemoteAgent().test_connection()"
```

**Corrupted database**
```bash
# Delete and recreate database
rm timemind.db
python timemind_main.py
```

## 📄 License

This project is distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local AI
- [Google Gemini](https://gemini.google.com/) for cloud AI
- [ChromaDB](https://www.trychroma.com/) for vector database
- Open source community for inspiration and support

---

**Built with ❤️ to improve everyone's productivity**
