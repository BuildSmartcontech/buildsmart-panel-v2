# panels/dueno/pedidos_web_acciones.py
# ============================================
# ACCIONES DE PEDIDOS WEB - Panel Dueno
# ============================================
# V2.2: Envia email automatico cuando la web se publica en Netlify.
# ============================================

import datetime

def _enviar_email_web_lista(pedido, url_publica):
    """Envia el correo de confirmacion al cliente cuando la web esta online."""
    try:
        from utils.email_sender import email_sender
        if not email_sender.disponible:
            print("[EMAIL] Omitido: email_sender no configurado.")
            return

        email = pedido.get("email", "")
        nombre = pedido.get("nombre_cliente", "Cliente")
        
        if not email:
            return

        asunto = f"Tu web esta lista - SAMU IA - Hola {nombre}"
        
        contenido = f"""Hola {nombre},

¡Buenas noticias! Tu pagina web ya esta publicada y lista para recibir visitas.

Puedes verla y compartirla aqui:
{url_publica}

Recuerda que tienes acceso a tu panel de cliente para hacer cambios usando el enlace que te enviamos anteriormente.

Cualquier consulta, responde a este email.

Saludos,
El equipo de SAMU IA
"""

        resultado = email_sender.enviar_correo(email, asunto, contenido)
        print(f"[EMAIL] Notificacion web lista enviada a {email}: {resultado}")
    except Exception as e:
        print(f"[EMAIL] Error enviando notificacion de web lista: {e}")

def generar_web_para_pedido(sb, pedido, publicar=True):
    print(f"=== GENERANDO WEB PARA PEDIDO: {pedido.get('id')} ===")
    
    try:
        from utils.web_generator import generar_web
        from utils.web_storage import guardar_web, generar_uuid
        
        datos_negocio = pedido.get("datos_negocio") or {}
        if not datos_negocio:
            return {"exito": False, "mensaje": "No hay datos de negocio en este pedido."}
            
        # DIAGNOSTICO SUPABASE: Verificamos si el logo viene en el JSON
        logo_db = datos_negocio.get("logo_b64")
        print(f"[SUPABASE CHECK] Logo en la base de datos: {'SI' if logo_db else 'NO'}")
        if not logo_db:
            print("[SUPABASE CHECK] ALERTA: El pedido no tiene logo. El usuario no lo subio o se perdio al guardar.")
            
        resultado_gen = generar_web(datos_negocio=datos_negocio)
        
        if not resultado_gen.get("exito"):
            return {"exito": False, "mensaje": f"Error de IA: {resultado_gen.get('error')}"}
            
        html = resultado_gen["html"]
        
        web_id = generar_uuid()
        usuario_id = pedido.get("email", "usuario_default")
        
        guardado = guardar_web(usuario_id=usuario_id, web_id=web_id, html=html, datos_extra={"pedido_id": pedido.get("id")})
        if not guardado.get("exito"):
            return {"exito": False, "mensaje": f"Error guardando web: {guardado.get('error')}"}

        if publicar:
            from utils.web_publisher import publicar_web
            resultado_pub = publicar_web(usuario_id, web_id)
            url_publica = resultado_pub.get("url_publica", "")
            
            if not url_publica:
                 return {"exito": False, "mensaje": f"Error publicando: {resultado_pub.get('error')}"}

            # 1. Actualizamos la base de datos
            sb.update(
                "pedidos_web",
                {"estado": "entregado", "web_id": web_id, "web_url": url_publica, "updated_at": datetime.datetime.now().isoformat(), "entregado_at": datetime.datetime.now().isoformat()},
                "id", pedido.get("id")
            )

            # 2. Enviamos el correo al cliente
            _enviar_email_web_lista(pedido, url_publica)

            return {"exito": True, "mensaje": "Web generada, publicada y correo enviado.", "url_publica": url_publica, "web_id": web_id, "html": html}
        
        else:
            return {"exito": True, "mensaje": "Web generada en modo VISTA PREVIA. No publicada.", "html": html, "web_id": web_id}
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"exito": False, "mensaje": f"Error inesperado: {str(e)}"}