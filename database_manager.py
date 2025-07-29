# -*- coding: utf-8 -*-
"""
Database Manager - Gestione del database SQLite per TimeMind
"""

import sqlite3
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path="./timemind.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inizializza il database SQLite locale"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabella task/todo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 2,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                estimated_minutes INTEGER,
                actual_minutes INTEGER
            )
        """)
        
        # Tabella abitudini
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                target_frequency TEXT DEFAULT 'daily',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabella tracciamento abitudini
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date DATE,
                completed BOOLEAN,
                notes TEXT,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        """)
        
        # Tabella riflessioni giornaliere
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                morning_plan TEXT,
                evening_reflection TEXT,
                mood_score INTEGER,
                productivity_score INTEGER,
                lessons_learned TEXT,
                tomorrow_focus TEXT
            )
        """)
        
        # Tabella sessioni Pomodoro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pomodoro_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_minutes INTEGER,
                completed BOOLEAN,
                notes TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
    # === TASK MANAGEMENT ===
    
    def add_task(self, title: str, description: str = "", priority: int = 2, estimated_minutes: int = 30) -> str:
        """Aggiunge un nuovo task alla lista"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, estimated_minutes) 
            VALUES (?, ?, ?, ?)
        """, (title, description, priority, estimated_minutes))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return f"✅ Task aggiunto: '{title}' (ID: {task_id}, Priorità: {priority}, Stima: {estimated_minutes}min)"
    
    def get_tasks(self, status: str = "pending") -> str:
        """Recupera i task con status specificato"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, priority, estimated_minutes, created_at
            FROM tasks WHERE status = ? ORDER BY priority DESC, created_at ASC
        """, (status,))
        
        tasks = cursor.fetchall()
        conn.close()
        
        if not tasks:
            return f"📝 Nessun task con status '{status}'"
        
        result = f"📋 Task ({status}):\n"
        for task in tasks:
            result += f"• ID {task[0]}: {task[1]} (P{task[2]}, ~{task[4]}min)\n"
        
        return result
    
    def complete_task(self, task_id: int, actual_minutes: int = None) -> str:
        """Completa un task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP, actual_minutes = ?
            WHERE id = ?
        """, (actual_minutes, task_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return f"✅ Task {task_id} completato! Tempo effettivo: {actual_minutes}min"
        else:
            conn.close()
            return f"❌ Task {task_id} non trovato"
    
    def delete_task(self, task_id: int) -> str:
        """Elimina un task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return f"✅ Task {task_id} eliminato"
        else:
            conn.close()
            return f"❌ Task {task_id} non trovato"
    
    # === HABIT MANAGEMENT ===
    
    def add_habit(self, name: str, description: str = "", frequency: str = "daily") -> str:
        """Aggiunge una nuova abitudine da tracciare"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO habits (name, description, target_frequency) 
            VALUES (?, ?, ?)
        """, (name, description, frequency))
        
        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return f"🏃‍♂️ Abitudine aggiunta: '{name}' (ID: {habit_id}, Frequenza: {frequency})"
    
    def get_habits(self, active_only: bool = True) -> str:
        """Recupera le abitudini"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute("""
                SELECT id, name, description, target_frequency 
                FROM habits WHERE active = 1 ORDER BY created_at ASC
            """)
        else:
            cursor.execute("""
                SELECT id, name, description, target_frequency, active 
                FROM habits ORDER BY created_at ASC
            """)
        
        habits = cursor.fetchall()
        conn.close()
        
        if not habits:
            return "🏃‍♂️ Nessuna abitudine configurata"
        
        result = "🏃‍♂️ Abitudini:\n"
        for habit in habits:
            status = "" if active_only else f" ({'Attiva' if habit[4] else 'Disattiva'})"
            result += f"• ID {habit[0]}: {habit[1]} ({habit[3]}){status}\n"
        
        return result
    
    def log_habit(self, habit_id: int, completed: bool = True, notes: str = "") -> str:
        """Registra il completamento di un'abitudine per oggi"""
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Controlla se già registrato oggi
        cursor.execute("""
            SELECT id FROM habit_logs WHERE habit_id = ? AND date = ?
        """, (habit_id, today))
        
        if cursor.fetchone():
            # Aggiorna esistente
            cursor.execute("""
                UPDATE habit_logs SET completed = ?, notes = ?
                WHERE habit_id = ? AND date = ?
            """, (completed, notes, habit_id, today))
        else:
            # Crea nuovo
            cursor.execute("""
                INSERT INTO habit_logs (habit_id, date, completed, notes)
                VALUES (?, ?, ?, ?)
            """, (habit_id, today, completed, notes))
        
        conn.commit()
        conn.close()
        
        status = "✅ Completata" if completed else "❌ Non completata"
        return f"{status} abitudine {habit_id} per oggi"
    
    # === POMODORO MANAGEMENT ===
    
    def start_pomodoro(self, task_id: int = None) -> str:
        """Avvia una sessione Pomodoro"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_time = datetime.now()
        
        cursor.execute("""
            INSERT INTO pomodoro_sessions (task_id, start_time, duration_minutes, completed)
            VALUES (?, ?, 25, 0)
        """, (task_id, start_time))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return f"🍅 Pomodoro avviato (ID: {session_id}) - Focus per 25 minuti!"
    
    def complete_pomodoro(self, session_id: int, notes: str = "") -> str:
        """Completa una sessione Pomodoro"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        end_time = datetime.now()
        
        cursor.execute("""
            UPDATE pomodoro_sessions 
            SET completed = 1, end_time = ?, notes = ?
            WHERE id = ?
        """, (end_time, notes, session_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return f"✅ Pomodoro {session_id} completato!"
        else:
            conn.close()
            return f"❌ Sessione Pomodoro {session_id} non trovata"
    
    # === DAILY SUMMARY ===
    
    def get_daily_summary(self) -> str:
        """Genera un riepilogo della giornata"""
        today = datetime.now().date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Task completati oggi
        cursor.execute("""
            SELECT COUNT(*) FROM tasks 
            WHERE status = 'completed' AND DATE(completed_at) = ?
        """, (today,))
        completed_tasks = cursor.fetchone()[0]
        
        # Task pending
        cursor.execute("""
            SELECT COUNT(*) FROM tasks WHERE status = 'pending'
        """, ())
        pending_tasks = cursor.fetchone()[0]
        
        # Abitudini completate oggi
        cursor.execute("""
            SELECT COUNT(*) FROM habit_logs 
            WHERE date = ? AND completed = 1
        """, (today,))
        habits_done = cursor.fetchone()[0]
        
        # Sessioni Pomodoro
        cursor.execute("""
            SELECT COUNT(*) FROM pomodoro_sessions 
            WHERE DATE(start_time) = ? AND completed = 1
        """, (today,))
        pomodoros = cursor.fetchone()[0]
        
        conn.close()
        
        return f"""📊 Riepilogo di oggi:
• ✅ Task completati: {completed_tasks}
• 📝 Task rimanenti: {pending_tasks}
• 🏃‍♂️ Abitudini completate: {habits_done}
• 🍅 Sessioni Pomodoro: {pomodoros}"""