# -*- coding: utf-8 -*-
"""
Local Agent - Agente locale usando Ollama + Llama3
"""

import requests
import json

class LocalAgent:
    def __init__(self, model_name="llama3"):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = model_name
        
    def test_connection(self):
        """Testa la connessione a Ollama"""
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": self.model_name, "prompt": "Test", "stream": False}
            )
            if response.status_code == 200:
                print("✅ Ollama (locale): OK")
                return True
            else:
                print("❌ Ollama non risponde - assicurati che sia avviato")
                return False
        except Exception as e:
            print(f"❌ Errore Ollama: {e}")
            return False
    
    def generate_response(self, prompt, context=""):
        """Genera una risposta usando l'agente locale"""
        try:
            full_prompt = f"""Sei TimeMind, un coach personale per la produttività e la gestione del tempo.
            
{context}

Domanda dell'utente: {prompt}

Rispondi in modo utile e pratico, usando un tono amichevole ma professionale."""

            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'Errore nella risposta')
            else:
                return f"Errore connessione Ollama: {response.status_code}"
                
        except Exception as e:
            return f"Errore agente locale: {e}"
    
    def set_model(self, model_name):
        """Cambia il modello utilizzato"""
        self.model_name = model_name
        return f"Modello cambiato a: {model_name}"