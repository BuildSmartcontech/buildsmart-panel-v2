# panels/dueno/pedidos_web_acciones.py
# ============================================
# ACCIONES DE PEDIDOS WEB - Panel Dueno
# ============================================
# V1.3: Usa el modelo por defecto y extrae imagenes del usuario
# ============================================

import datetime

def generar_web_para_pedido(sb, pedido):
    print(f"=== GENERANDO WEB PARA PEDIDO: {pedido.get('id')} ===")
    
    try:
        from utils.web_generator import generar_web
        from utils.web_storage import guardar_web, generar_uuid
        from utils.web_publisher import publicar_web
        
        datos_negocio = pedido.get("datos_negocio") or {}
        if not datos_negocio:
            return {"exito": False, "mensaje": "No hay datos de negocio en este pedido."}
            
        # El generador usara el modelo por defecto (nemotron-3-super-120b)
        resultado_gen = generar_web(
            datos_negocio=datos_negocio, 
            opciones={"tipo_pagina": "Landing Page", "diseno": "Moderno"}
        )
        
        if not resultado_gen.get("exito"):
            return {"exito": False, "mensaje": f"Error de IA: {resultado_gen.get('error')}"}
            
        html = resultado_gen["html"]
        
        web_id = generar_uuid()
        usuario_id = pedido.get("email", "usuario_default")
        
        guardado = guardar_web(
            usuario_id=usuario_id, 
            web_id=web_id, 
            html=html, 
            datos_extra={"pedido_id": pedido.get("id")}
        )
        
        if not guardado.get("exito"):
            return {"exito": False, "mensaje": f"Error guardando web: {guardado.get('error')}"}
            
        resultado_pub = publicar_web(usuario_id, web_id)
        url_publica = resultado_pub.get("url_publica", "")
        
        if not url_publica:
             return {"exito": False, "mensaje": f"Error publicando: {resultado_pub.get('error')}"}

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
        }
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"exito": False, "mensaje": f"Error inesperado: {str(e)}"}