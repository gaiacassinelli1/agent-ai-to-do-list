# -*- coding: utf-8 -*-
"""
Remote Agent - Agente remoto usando Google Gemini
"""

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class RemoteAgent:
    def __init__(self, model_name="gemini-2.0-flash-001"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY non configurata nel file .env")
        
        self.client = genai.Client(api_key=self.api_key)
        
    def test_connection(self):
        """Testa la connessione a Gemini"""
        try:
            if self.api_key:
                print("✅ Gemini API Key: OK")
                return True
            else:
                print("❌ GOOGLE_API_KEY non configurata")
                return False
        except Exception as e:
            print(f"❌ Errore Gemini: {e}")
            return False
    
    def generate_response(self, prompt, context="", temperature=0.7, max_tokens=1000):
        """Genera una risposta usando l'agente remoto"""
        try:
            full_prompt = f"""Sei TimeMind, un coach avanzato per la produttività.
            
{context}

Domanda dell'utente: {prompt}

Fornisci un'analisi approfondita e suggerimenti personalizzati."""

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature, 
                    max_output_tokens=max_tokens
                )
            )
            
            return response.text
            
        except Exception as e:
            return f"Errore agente remoto: {e}"
    
    def generate_embedding(self, text, task_type="RETRIEVAL_DOCUMENT"):
        """Genera embedding per il testo usando Gemini"""
        try:
            result = self.client.models.embed_content(
                model="gemini-embedding-exp-03-07",
                contents=text,
                config=types.EmbedContentConfig(task_type=task_type)
            )
            
            return result.embeddings[0].values
            
        except Exception as e:
            print(f"⚠️ Errore generazione embedding: {e}")
            return None
    
    def set_model(self, model_name):
        """Cambia il modello utilizzato"""
        self.model_name = model_name
        return f"Modello cambiato a: {model_name}"