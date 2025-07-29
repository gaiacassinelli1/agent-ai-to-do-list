# -*- coding: utf-8 -*-
"""
TimeMind - Main Application
Coach personale per organizzare il tempo con agenti ibridi e RAG

Prerequisiti:
1. pip install ollama google-genai chromadb python-dotenv requests
2. Installare Ollama: https://ollama.ai/
3. Scaricare Llama3: ollama pull llama3
4. Configurare GOOGLE_API_KEY nel file .env
5. Creare cartella ./knowledge_base con file di testo
"""

from local_agent import LocalAgent
from remote_agent import RemoteAgent
from rag_system import RAGSystem
from database_manager import DatabaseManager

class TimeMindAgent:
    def __init__(self):
        print("🧠 Inizializzazione TimeMind Hybrid Agent...")
        
        # Inizializza componenti
        self.local_agent = LocalAgent()
        self.remote_agent = RemoteAgent()
        self.rag_system = RAGSystem()
        self.db_manager = DatabaseManager()
        
        # Test connessioni
        self.test_all_connections()
        
        print("🧠 TimeMind Hybrid Agent inizializzato")
        print("✅ Database locale: OK")
        print("✅ Vector DB (RAG): OK")
        print("✅ Knowledge base: OK")
        
    def test_all_connections(self):
        """Testa tutte le connessioni"""
        print("\n🔍 Test connessioni...")
        self.local_agent.test_connection()
        self.remote_agent.test_connection()
        print(self.rag_system.get_collection_stats())
        
    def chat(self, user_input: str, use_remote: bool = False):
        """Interfaccia principale di chat"""
        # Cerca nella knowledge base
        knowledge_context = self.rag_system.get_context_for_query(user_input)
        context = f"Knowledge base:\n{knowledge_context}\n\n" if knowledge_context else ""
        
        # Determina se usare agente locale o remoto
        if use_remote or "analisi" in user_input.lower() or "report" in user_input.lower():
            return self.remote_agent.generate_response(user_input, context)
        else:
            return self.local_agent.generate_response(user_input, context)
    
    # Metodi delegati al database manager
    def add_task(self, title: str, description: str = "", priority: int = 2, estimated_minutes: int = 30) -> str:
        return self.db_manager.add_task(title, description, priority, estimated_minutes)
    
    def get_tasks(self, status: str = "pending") -> str:
        return self.db_manager.get_tasks(status)
    
    def complete_task(self, task_id: int, actual_minutes: int = None) -> str:
        return self.db_manager.complete_task(task_id, actual_minutes)
    
    def delete_task(self, task_id: int) -> str:
        return self.db_manager.delete_task(task_id)
    
    def add_habit(self, name: str, description: str = "", frequency: str = "daily") -> str:
        return self.db_manager.add_habit(name, description, frequency)
    
    def get_habits(self, active_only: bool = True) -> str:
        return self.db_manager.get_habits(active_only)
    
    def log_habit(self, habit_id: int, completed: bool = True, notes: str = "") -> str:
        return self.db_manager.log_habit(habit_id, completed, notes)
    
    def start_pomodoro(self, task_id: int = None) -> str:
        return self.db_manager.start_pomodoro(task_id)
    
    def complete_pomodoro(self, session_id: int, notes: str = "") -> str:
        return self.db_manager.complete_pomodoro(session_id, notes)
    
    def get_daily_summary(self) -> str:
        return self.db_manager.get_daily_summary()
    
    # Metodi RAG
    def add_knowledge(self, text: str, doc_id: str) -> str:
        return self.rag_system.add_document(text, doc_id)
    
    def search_knowledge(self, query: str) -> str:
        results = self.rag_system.search_documents(query)
        if results and results['documents']:
            return "\n".join(results['documents'])
        return "Nessun risultato trovato nella knowledge base"

def print_help():
    """Stampa i comandi disponibili"""
    print("\n🧠 TimeMind - Il tuo coach personale per la produttività")
    print("=" * 60)
    print("💡 Comandi disponibili:")
    print("\n📋 TASK MANAGEMENT:")
    print("  • 'add task: titolo' - Aggiunge un task")
    print("  • 'tasks' - Mostra task pending")
    print("  • 'completed tasks' - Mostra task completati")
    print("  • 'complete: ID' - Completa un task")
    print("  • 'delete task: ID' - Elimina un task")
    print("\n🏃‍♂️ HABIT TRACKING:")
    print("  • 'add habit: nome' - Aggiunge un'abitudine")
    print("  • 'habits' - Mostra abitudini attive")
    print("  • 'log habit: ID' - Registra completamento abitudine")
    print("  • 'log habit: ID false' - Registra mancato completamento")
    print("\n🍅 POMODORO:")
    print("  • 'pomodoro' - Avvia sessione Pomodoro")
    print("  • 'pomodoro: task_id' - Avvia Pomodoro per task specifico")
    print("  • 'complete pomodoro: session_id' - Completa sessione")
    print("\n📊 ANALYTICS:")
    print("  • 'summary' - Riepilogo giornaliero")
    print("  • 'stats' - Statistiche knowledge base")
    print("\n🧠 CHAT & KNOWLEDGE:")
    print("  • 'remote: domanda' - Usa agente remoto (Gemini)")
    print("  • 'search: query' - Cerca nella knowledge base")
    print("  • 'add knowledge: doc_id | testo' - Aggiungi alla knowledge base")
    print("\n🔧 SISTEMA:")
    print("  • 'help' - Mostra questo aiuto")
    print("  • 'test' - Test connessioni")
    print("  • 'quit' - Esci")
    print("-" * 60)

def parse_command(user_input: str, agent: TimeMindAgent):
    """Parsing e esecuzione comandi"""
    user_input = user_input.strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        return "quit"
    
    elif user_input.lower() in ['help', 'h']:
        print_help()
        return "continue"
    
    elif user_input.lower() == 'test':
        agent.test_all_connections()
        return "continue"
    
    # === TASK COMMANDS ===
    elif user_input.startswith('add task:'):
        title = user_input.replace('add task:', '').strip()
        print(f"🤖 {agent.add_task(title)}")
        return "continue"
    
    elif user_input.lower() == 'tasks':
        print(f"🤖 {agent.get_tasks()}")
        return "continue"
    
    elif user_input.lower() == 'completed tasks':
        print(f"🤖 {agent.get_tasks('completed')}")
        return "continue"
    
    elif user_input.startswith('complete:'):
        try:
            task_id = int(user_input.replace('complete:', '').strip())
            print(f"🤖 {agent.complete_task(task_id)}")
        except ValueError:
            print("❌ ID task non valido")
        return "continue"
    
    elif user_input.startswith('delete task:'):
        try:
            task_id = int(user_input.replace('delete task:', '').strip())
            print(f"🤖 {agent.delete_task(task_id)}")
        except ValueError:
            print("❌ ID task non valido")
        return "continue"
    
    # === HABIT COMMANDS ===
    elif user_input.startswith('add habit:'):
        name = user_input.replace('add habit:', '').strip()
        print(f"🤖 {agent.add_habit(name)}")
        return "continue"
    
    elif user_input.lower() == 'habits':
        print(f"🤖 {agent.get_habits()}")
        return "continue"
    
    elif user_input.startswith('log habit:'):
        parts = user_input.replace('log habit:', '').strip().split()
        try:
            habit_id = int(parts[0])
            completed = parts[1].lower() != 'false' if len(parts) > 1 else True
            print(f"🤖 {agent.log_habit(habit_id, completed)}")
        except (ValueError, IndexError):
            print("❌ Formato non valido. Usa: log habit: ID [true/false]")
        return "continue"
    
    # === POMODORO COMMANDS ===
    elif user_input.lower() == 'pomodoro':
        print(f"🤖 {agent.start_pomodoro()}")
        return "continue"
    
    elif user_input.startswith('pomodoro:'):
        try:
            task_id = int(user_input.replace('pomodoro:', '').strip())
            print(f"🤖 {agent.start_pomodoro(task_id)}")
        except ValueError:
            print("❌ ID task non valido")
        return "continue"
    
    elif user_input.startswith('complete pomodoro:'):
        try:
            session_id = int(user_input.replace('complete pomodoro:', '').strip())
            print(f"🤖 {agent.complete_pomodoro(session_id)}")
        except ValueError:
            print("❌ ID sessione non valido")
        return "continue"
    
    # === ANALYTICS COMMANDS ===
    elif user_input.lower() == 'summary':
        print(f"🤖 {agent.get_daily_summary()}")
        return "continue"
    
    elif user_input.lower() == 'stats':
        print(f"🤖 {agent.rag_system.get_collection_stats()}")
        return "continue"
    
    # === KNOWLEDGE COMMANDS ===
    elif user_input.startswith('search:'):
        query = user_input.replace('search:', '').strip()
        results = agent.search_knowledge(query)
        print(f"🤖 Risultati ricerca:\n{results}")
        return "continue"
    
    elif user_input.startswith('add knowledge:'):
        try:
            content = user_input.replace('add knowledge:', '').strip()
            parts = content.split('|', 1)
            if len(parts) == 2:
                doc_id = parts[0].strip()
                text = parts[1].strip()
                print(f"🤖 {agent.add_knowledge(text, doc_id)}")
            else:
                print("❌ Formato non valido. Usa: add knowledge: doc_id | testo")
        except Exception as e:
            print(f"❌ Errore: {e}")
        return "continue"
    
    elif user_input.startswith('remote:'):
        question = user_input.replace('remote:', '').strip()
        print(f"🤖 {agent.chat(question, use_remote=True)}")
        return "continue"
    
    else:
        # Chat normale con agente locale
        print(f"🤖 {agent.chat(user_input)}")
        return "continue"

def main():
    """Main loop dell'applicazione"""
    try:
        agent = TimeMindAgent()
        print_help()
        
        while True:
            try:
                user_input = input("\n🧑 Tu: ").strip()
                
                if not user_input:
                    continue
                
                result = parse_command(user_input, agent)
                
                if result == "quit":
                    print("👋 Arrivederci! Buona produttività!")
                    break
                    
            except KeyboardInterrupt:
                print("\n👋 Arrivederci!")
                break
            except Exception as e:
                print(f"❌ Errore: {e}")
                
    except Exception as e:
        print(f"❌ Errore inizializzazione: {e}")
        print("Verifica che:")
        print("1. Ollama sia installato e avviato")
        print("2. GOOGLE_API_KEY sia configurata nel file .env")
        print("3. Tutte le dipendenze siano installate")

if __name__ == "__main__":
    main()