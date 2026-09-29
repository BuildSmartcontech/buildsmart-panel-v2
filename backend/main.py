# backend/main.py - FastAPI Backend para SAMU IA con Orquestador LangGraph
# ============================================
# VERSIÓN 7.9 - CON RUTAS DE WEBS GENERADAS
# ============================================

import sys
import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import httpx
from dotenv import load_dotenv

# ========== AGREGAR RUTA DEL PROYECTO AL PATH ==========
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

app = FastAPI(title="SAMU IA API", version="7.9")

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== MODELOS ==========
class ChatRequest(BaseModel):
    mensaje: str
    sistema: Optional[str] = "Eres un asistente útil y profesional."
    negocio_id: Optional[str] = None
    modelo: Optional[str] = None

class ChatResponse(BaseModel):
    respuesta: str
    modelo_usado: str
    fuente: str
    pdf_url: Optional[str] = None
    resumen_ejecutivo: Optional[str] = None

# ========== RUTAS ==========
@app.get("/")
async def root():
    return {
        "mensaje": "SAMU IA API",
        "version": "7.9",
        "status": "online"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ========== RUTAS DE WEBS GENERADAS ==========

@app.get("/web/{web_id}")
async def servir_web(web_id: str):
    """
    Sirve una web generada por su ID.
    Busca el HTML en data/webs_generadas/*/{web_id}/index.html
    """
    import glob
    
    # Buscar la carpeta de la web en data/webs_generadas/
    patron = os.path.join("data", "webs_generadas", "*", web_id, "index.html")
    rutas = glob.glob(patron)
    
    if not rutas:
        # Si no encuentra, intentar buscar en el respaldo
        return HTMLResponse(
            content=f"""
            <html>
            <head><title>Web no encontrada</title></head>
            <body style="font-family: sans-serif; padding: 40px; text-align: center;">
                <h1>❌ Web no encontrada</h1>
                <p>La web con ID <code>{web_id}</code> no existe o fue eliminada.</p>
                <p><a href="/">Volver al inicio</a></p>
            </body>
            </html>
            """,
            status_code=404
        )
    
    ruta_html = rutas[0]
    
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            html = f.read()
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
            <head><title>Error</title></head>
            <body style="font-family: sans-serif; padding: 40px; text-align: center;">
                <h1>❌ Error al cargar la web</h1>
                <p>{str(e)}</p>
            </body>
            </html>
            """,
            status_code=500
        )

@app.get("/api/webs/{usuario_id}")
async def listar_webs_usuario(usuario_id: str):
    """
    Lista las webs generadas de un usuario.
    Retorna un JSON con la lista de webs.
    """
    carpeta = os.path.join("data", "webs_generadas", usuario_id)
    
    if not os.path.exists(carpeta):
        return {"exito": True, "webs": [], "total": 0}
    
    webs = []
    for web_id in os.listdir(carpeta):
        ruta_web = os.path.join(carpeta, web_id)
        ruta_html = os.path.join(ruta_web, "index.html")
        
        if os.path.exists(ruta_html):
            webs.append({
                "web_id": web_id,
                "url": f"http://localhost:8000/web/{web_id}",
                "tamano": os.path.getsize(ruta_html),
                "fecha_modificacion": os.path.getmtime(ruta_html)
            })
    
    return {
        "exito": True,
        "usuario_id": usuario_id,
        "webs": webs,
        "total": len(webs)
    }

@app.get("/api/webs")
async def listar_todas_las_webs():
    """
    Lista TODAS las webs generadas (para admin).
    """
    base = os.path.join("data", "webs_generadas")
    
    if not os.path.exists(base):
        return {"exito": True, "webs": [], "total": 0}
    
    webs = []
    for usuario_id in os.listdir(base):
        carpeta_usuario = os.path.join(base, usuario_id)
        if not os.path.isdir(carpeta_usuario):
            continue
        
        for web_id in os.listdir(carpeta_usuario):
            ruta_web = os.path.join(carpeta_usuario, web_id)
            ruta_html = os.path.join(ruta_web, "index.html")
            
            if os.path.exists(ruta_html):
                webs.append({
                    "usuario_id": usuario_id,
                    "web_id": web_id,
                    "url": f"http://localhost:8000/web/{web_id}",
                    "tamano": os.path.getsize(ruta_html)
                })
    
    return {
        "exito": True,
        "webs": webs,
        "total": len(webs)
    }

# ========== CHAT ==========

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal con orquestador LangGraph"""
    try:
        from backend.orquestador import ejecutar_orquestador
        
        resultado = ejecutar_orquestador(request.mensaje, request.negocio_id)
        
        if resultado and resultado.get("resultado"):
            return ChatResponse(
                respuesta=resultado["resultado"],
                modelo_usado="openrouter",
                fuente="nube",
                pdf_url=resultado.get("pdf_url"),
                resumen_ejecutivo=resultado.get("resumen_ejecutivo")
            )
        else:
            from backend.gateway import gateway
            respuesta, fuente = gateway.chat(request.mensaje, request.sistema)
            return ChatResponse(
                respuesta=respuesta,
                modelo_usado=fuente,
                fuente=fuente
            )
            
    except ImportError as e:
        print(f"⚠️ Orquestador no disponible: {e}")
        try:
            from backend.gateway import gateway
            respuesta, fuente = gateway.chat(request.mensaje, request.sistema)
            return ChatResponse(
                respuesta=respuesta,
                modelo_usado=fuente,
                fuente=fuente
            )
        except Exception as e2:
            raise HTTPException(status_code=503, detail=f"Error en gateway: {str(e2)}")
            
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== FUNCIONES DE CHAT (FALLBACK) ==========
async def chat_ollama(mensaje: str, sistema: str) -> str:
    """Chat con Ollama local"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": f"{sistema}\n\nUsuario: {mensaje}\n\nAsistente:",
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get('response', '')
            raise Exception(f"Ollama error: {response.status_code}")
    except Exception as e:
        raise Exception(f"Ollama falló: {str(e)}")

async def chat_deepseek(mensaje: str, sistema: str) -> str:
    """Chat con DeepSeek API"""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise Exception("DeepSeek API Key no configurada")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        raise Exception(f"DeepSeek error: {response.status_code}")

async def chat_openrouter(mensaje: str, sistema: str) -> str:
    """Chat con OpenRouter API"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise Exception("OpenRouter API Key no configurada")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "nvidia/nemotron-3-super-120b-a12b:free",
                "messages": [
                    {"role": "system", "content": sistema},
                    {"role": "user", "content": mensaje}
                ],
                "temperature": 0.7,
                "max_tokens": 8000
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        raise Exception(f"OpenRouter error: {response.status_code}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)