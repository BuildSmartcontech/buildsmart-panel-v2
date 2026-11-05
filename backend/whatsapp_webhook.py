# backend/whatsapp_webhook.py
# ============================================
# WEBHOOK DE WHATSAPP META API - ARM PLUS
# ============================================
# V2.0: Validación de firma X-Hub-Signature-256 (Security Shield)
# ============================================

from fastapi import FastAPI, Request, HTTPException, Header
import os
import hmac
import hashlib
from utils.plan_controller import verificar_acceso_arm
from utils.odoo_service import crear_lead_odoo
from utils.security import sanitizar_input_ia # <-- IMPORTACIÓN DE SEGURIDAD

try:
    from utils.supabase_rest import supabase_rest
except ImportError:
    supabase_rest = None

try:
    from backend.gateway import gateway 
except ImportError:
    gateway = None

app = FastAPI()

@app.get("/webhook/whatsapp")
async def verify_token(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == os.getenv("META_VERIFY_TOKEN"):
        return int(params.get("hub.challenge"))
    raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/webhook/whatsapp")
async def receive_message(request: Request, x_hub_signature_256: str = Header(None)):
    # 1. VALIDAR FIRMA DE META (Evita que envíen mensajes falsos)
    app_secret = os.getenv("META_APP_SECRET")
    if app_secret:
        if not x_hub_signature_256:
            raise HTTPException(status_code=403, detail="Missing signature")
        
        body_bytes = await request.body()
        expected_signature = "sha256=" + hmac.new(
            app_secret.encode(), body_bytes, hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(x_hub_signature_256, expected_signature):
            raise HTTPException(status_code=403, detail="Invalid signature")

    body = await request.json()
    
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        if "messages" not in entry:
            return {"status": "ok"}
            
        mensaje = entry["messages"][0]
        cliente_id = entry["metadata"]["phone_number_id"]
        telefono_remitente = mensaje["from"]
        texto_original = mensaje["text"]["body"]
        
        # 2. SANITIZAR EL MENSAJE (Evita Prompt Injection)
        texto = sanitizar_input_ia(texto_original)
        
        # 3. VALIDAR PLAN Y LÍMITES
        tiene_acceso, mensaje_error = verificar_acceso_arm(cliente_id)
        
        if not tiene_acceso:
            print(f"[ARM BLOCK] Bloqueado para {cliente_id}: {mensaje_error}")
            return {"status": "blocked", "reason": mensaje_error}
            
        # 4. ORQUESTADOR IA
        if gateway:
            prompt = f"Califica este lead: {texto}. Devuelve un resumen corto y la intención de compra."
            respuesta_ia, fuente = gateway.chat_inteligente(prompt, "Eres un calificador de leads.")
        else:
            respuesta_ia = "Lead interesado."
            
        # 5. SINCRONIZAR ODOO
        crear_lead_odoo(
            nombre=f"Cliente WA {telefono_remitente[-4:]}", 
            telefono=telefono_remitente, 
            descripcion=f"Mensaje: {texto}\nAnálisis IA: {respuesta_ia}"
        )
        
        # 6. REGISTRAR EN SUPABASE
        if supabase_rest and supabase_rest.disponible:
            try:
                supabase_rest.table("arm_logs").insert({
                    "cliente_id": cliente_id,
                    "telefono": telefono_remitente,
                    "tipo": "whatsapp",
                    "tokens_usados": 50,
                    "resumen": respuesta_ia
                }).execute()
            except Exception as e:
                print(f"[DB ERROR] No se pudo registrar log: {e}")
        
        print(f"[ARM OK] Lead procesado para {telefono_remitente}")
        return {"status": "ok"}
    except Exception as e:
        print(f"[WEBHOOK ERROR] {e}")
        return {"status": "error"}