# panels/dueno/pedidos_web_acciones.py
# ============================================
# ACCIONES DE PEDIDOS WEB - Panel Dueno
# ============================================
# V1.1: Acepta modelo_ia para la generacion con OpenRouter
# ============================================

import datetime

def generar_web_para_pedido(sb, pedido, modelo_ia="openrouter/free"):
    """
    Genera la web de un pedido.
    """
    print(f"=== GENERANDO WEB PARA PEDIDO: {pedido.get('id')} ===")
    
    try:
        from utils.web_generator import generar_web
        from utils.web_storage import guardar_web, generar_uuid
        from utils.web_publisher import publicar_web
        
        # 1. Extraer datos del pedido
        datos_negocio = pedido.get("datos_negocio") or {}
        if not datos_negocio:
            return {"exito": False, "mensaje": "No hay datos de negocio en este pedido."}
            
        # 2. Generar HTML
        # Llamamos a generar_web con el modelo seleccionado
        resultado_gen = generar_web(
            datos_negocio=datos_negocio, 
            opciones={"tipo_pagina": "Landing Page", "diseno": "Moderno"},
            modelo_ia=modelo_ia
        )
        
        if not resultado_gen.get("exito"):
            return {"exito": False, "mensaje": f"Error de IA: {resultado_gen.get('error')}"}
            
        html = resultado_gen["html"]
        
        # 3. Guardar en almacenamiento local/Supabase
        web_id = generar_uuid()
        usuario_id = pedido.get("email", "usuario_default") # Usamos email como ID de carpeta
        
        guardado = guardar_web(
            usuario_id=usuario_id, 
            web_id=web_id, 
            html=html, 
            datos_extra={"pedido_id": pedido.get("id")}
        )
        
        if not guardado.get("exito"):
            return {"exito": False, "mensaje": f"Error guardando web: {guardado.get('error')}"}
            
        # 4. Publicar en Netlify
        resultado_pub = publicar_web(usuario_id, web_id)
        url_publica = resultado_pub.get("url_publica", "")
        
        if not url_publica:
             return {"exito": False, "mensaje": f"Error publicando: {resultado_pub.get('error')}"}

        # 5. Actualizar el pedido en la base de datos
        sb.update(
            "pedidos_web",
            {
                "estado": "entregado",
                "web_id": web_id,
                "web_url": url_publica,
                "updated_at": datetime.datetime.now().isoformat(),
                "entregado_at": datetime.datetime.now().isoformat()
            },
            "id",
            pedido.get("id")
        )
        
        return {
            "exito": True, 
            "mensaje": "Web generada y publicada con exito.",
            "url_publica": url_publica,
            "web_id": web_id,
            "email_enviado": False, # Aquí iría la lógica de email
            "email_mensaje": "Funcion de email pendiente."
        }
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"exito": False, "mensaje": f"Error inesperado: {str(e)}"}