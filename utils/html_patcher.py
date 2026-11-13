# utils/html_patcher.py
# ============================================
# APLICADOR DE CAMBIOS AL HTML - V5.0 (EJECUTOR DOM)
# ============================================

import re
from bs4 import BeautifulSoup
from utils.image_fetcher import obtener_urls_imagenes_negocio

def _limpiar_html_residual(html_code: str) -> str:
    if "</footer>" in html_code:
        partes = html_code.split("</footer>")
        return partes[0] + "</footer>\n</body>\n</html>"
    return html_code

def _reparar_imagenes_rotas(html_completo):
    soup = BeautifulSoup(html_completo, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if "{{" in src or not src or (src.startswith("http") and "images.unsplash.com" not in src):
            if "base64" in src:
                continue
            alt_texto = img.get('alt', 'negocio')
            imagenes = obtener_urls_imagenes_negocio({"sector": alt_texto}, cantidad=1)
            if imagenes:
                img['src'] = imagenes[0]['url_regular']
            else:
                img['src'] = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop"
    return str(soup)

def aplicar_cambios(html, operaciones):
    if not html or not operaciones:
        return {"exito": False, "html_nuevo": html, "error": "Sin cambios"}

    html = _limpiar_html_residual(html)
    soup = BeautifulSoup(html, 'html.parser')
    cambios_reales = 0
    explicacion = ""

    for op in operaciones:
        selector = op.get("selector", "")
        accion = op.get("accion", "")
        valor = op.get("valor", "")
        
        if not selector or not accion:
            continue
            
        elementos = soup.select(selector)
        if not elementos:
            continue

        if accion == "cambiar_texto":
            for el in elementos:
                el.string = valor
                cambios_reales += 1
                break
                
        elif accion == "cambiar_atributo":
            atributo = op.get("atributo", "")
            if atributo:
                for el in elementos:
                    el[atributo] = valor
                    cambios_reales += 1
                    break
                    
        elif accion == "insertar_html":
            for el in elementos:
                fragmento = BeautifulSoup(valor, 'html.parser')
                el.append(fragmento)
                cambios_reales += 1
                break
                
        elif accion == "mover":
            destino = op.get("destino", "")
            # Buscar el elemento ancla de destino
            if destino.startswith("despues_de_"):
                ancla_destino_sel = destino.replace("despues_de_", "")
                ancla_destino = soup.select_one(ancla_destino_sel)
                if ancla_destino:
                    for el in elementos:
                        ancla_destino.insert_after(el.extract())
                        cambios_reales += 1
                        break
            elif destino.startswith("antes_de_"):
                ancla_destino_sel = destino.replace("antes_de_", "")
                ancla_destino = soup.select_one(ancla_destino_sel)
                if ancla_destino:
                    for el in elementos:
                        ancla_destino.insert_before(el.extract())
                        cambios_reales += 1
                        break
                        
        elif accion == "cambiar_css":
            for el in elementos:
                estilo_actual = el.get('style', '')
                el['style'] = estilo_actual + "; " + valor
                cambios_reales += 1
                break
                
        elif accion == "eliminar":
            for el in elementos:
                el.decompose()
                cambios_reales += 1
                break

    html_final = str(soup)

    if cambios_reales == 0:
        return {
            "exito": False, 
            "html_nuevo": html, 
            "error": "La IA no encontró el elemento exacto para aplicar el cambio."
        }

    html_final = _reparar_imagenes_rotas(html_final)

    return {
        "exito": True,
        "html_nuevo": html_final,
        "cambios_aplicados": cambios_reales,
        "cambios_totales": len(operaciones),
        "aplicados": [{"descripcion": explicacion or "Cambios aplicados", "detalle": ""}],
        "fallidos": []
    }