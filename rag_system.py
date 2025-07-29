# -*- coding: utf-8 -*-
"""
RAG System - Sistema di Retrieval-Augmented Generation usando ChromaDB
"""

import os
import chromadb
from chromadb.config import Settings
from remote_agent import RemoteAgent

class RAGSystem:
    def __init__(self, persist_directory="./timemind_chroma"):
        self.persist_directory = persist_directory
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.knowledge_collection = self.chroma_client.get_or_create_collection("knowledge_base")
        
        # Usa RemoteAgent per generare embedding
        self.remote_agent = RemoteAgent()
        
        # Carica knowledge base se non già fatto
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Carica file dalla cartella knowledge_base nel vector DB"""
        kb_path = "./knowledge_base"
        
        if not os.path.exists(kb_path):
            os.makedirs(kb_path)
            self._create_sample_files(kb_path)
        
        # Carica tutti i file .txt nella knowledge base
        for filename in os.listdir(kb_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(kb_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.add_document(content, filename)
    
    def _create_sample_files(self, kb_path):
        """Crea file di esempio nella knowledge base"""
        # File Pomodoro
        with open(os.path.join(kb_path, "pomodoro_technique.txt"), "w", encoding="utf-8") as f:
            f.write("""
            Tecnica Pomodoro:
            1. Scegli un'attività da svolgere
            2. Imposta un timer per 25 minuti
            3. Lavora sull'attività fino al suono del timer
            4. Fai una pausa di 5 minuti
            5. Ogni 4 pomodori, fai una pausa più lunga (15-30 minuti)
            
            Benefici: migliora la concentrazione, riduce la procrastinazione, 
            aumenta la produttività.
            """)
        
        # File Time Blocking
        with open(os.path.join(kb_path, "time_blocking.txt"), "w", encoding="utf-8") as f:
            f.write("""
            Time Blocking:
            Tecnica di pianificazione dove dividi la giornata in blocchi di tempo
            dedicati a specifiche attività.
            
            Come applicarla:
            - Identifica le tue attività principali
            - Assegna blocchi di tempo specifici nel calendario
            - Rispetta i blocchi programmati
            - Lascia buffer tra le attività
            
            Vantaggi: maggiore focus, meno multitasking, migliore gestione del tempo.
            """)
        
        # File Eisenhower Matrix
        with open(os.path.join(kb_path, "eisenhower_matrix.txt"), "w", encoding="utf-8") as f:
            f.write("""
            Matrice di Eisenhower:
            Metodo per prioritizzare task basato su urgenza e importanza.
            
            Quadranti:
            1. Urgente + Importante: Fai subito
            2. Non urgente + Importante: Programma
            3. Urgente + Non importante: Delega
            4. Non urgente + Non importante: Elimina
            
            Aiuta a concentrarsi su ciò che conta davvero.
            """)
    
    def add_document(self, text, doc_id, metadata=None):
        """Aggiunge un documento alla knowledge base"""
        try:
            # Genera embedding usando RemoteAgent
            embedding = self.remote_agent.generate_embedding(text, "RETRIEVAL_DOCUMENT")
            
            if embedding:
                # Prepara metadata
                if metadata is None:
                    metadata = {"source": "knowledge_base", "doc_id": doc_id}
                
                # Memorizza nel vector DB
                self.knowledge_collection.upsert(
                    embeddings=[embedding],
                    documents=[text],
                    ids=[doc_id],
                    metadatas=[metadata]
                )
                
                return f"✅ Documento '{doc_id}' aggiunto alla knowledge base"
            else:
                return f"❌ Errore generazione embedding per '{doc_id}'"
            
        except Exception as e:
            return f"⚠️ Errore caricamento documento '{doc_id}': {e}"
    
    def search_documents(self, query, n_results=2):
        """Cerca documenti rilevanti nella knowledge base"""
        try:
            # Genera embedding per la query
            query_embedding = self.remote_agent.generate_embedding(query, "RETRIEVAL_QUERY")
            
            if not query_embedding:
                return None
            
            # Cerca documenti rilevanti
            results = self.knowledge_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'distances', 'metadatas']
            )
            
            if results['documents'][0]:
                return {
                    'documents': results['documents'][0],
                    'distances': results['distances'][0] if results['distances'] else [],
                    'metadatas': results['metadatas'][0] if results['metadatas'] else []
                }
            return None
            
        except Exception as e:
            print(f"⚠️ Errore ricerca documenti: {e}")
            return None
    
    def get_context_for_query(self, query, n_results=2):
        """Ottiene contesto rilevante per una query"""
        search_results = self.search_documents(query, n_results)
        
        if search_results and search_results['documents']:
            return "\n".join(search_results['documents'])
        return None
    
    def get_collection_stats(self):
        """Restituisce statistiche sulla collection"""
        try:
            count = self.knowledge_collection.count()
            return f"📊 Knowledge base: {count} documenti indicizzati"
        except Exception as e:
            return f"❌ Errore statistiche: {e}"
    
    def delete_document(self, doc_id):
        """Elimina un documento dalla knowledge base"""
        try:
            self.knowledge_collection.delete(ids=[doc_id])
            return f"✅ Documento '{doc_id}' eliminato dalla knowledge base"
        except Exception as e:
            return f"❌ Errore eliminazione documento '{doc_id}': {e}"
    
    def reset_knowledge_base(self):
        """Resetta completamente la knowledge base"""
        try:
            self.chroma_client.delete_collection("knowledge_base")
            self.knowledge_collection = self.chroma_client.get_or_create_collection("knowledge_base")
            return "✅ Knowledge base resettata"
        except Exception as e:
            return f"❌ Errore reset knowledge base: {e}"