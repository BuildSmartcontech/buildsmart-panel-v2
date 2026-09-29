import sys, os
sys.path.insert(0, os.path.abspath("."))

from utils.web_generator import generar_web

print("=" * 70)
print("TEST GENERACION REAL - BLOQUE 3")
print("=" * 70)

datos = {
    "nombre": "Panaderia Premium Los Tres Amigos",
    "sector": "alimentos",
    "descripcion": "Panaderia artesanal con masa madre y reposteria premium",
    "publico_objetivo": "familias y oficinas del sector",
    "diferenciadores": "masa madre, ingredientes locales",
    "direccion": "Calle 123 #45-67",
    "ciudad": "Bogota",
    "pais": "Colombia",
    "horarios": "Lun-Vie 8am-6pm, Sab 9am-1pm",
    "instagram": "panaderialos3amigos",
    "facebook": "panaderialos3amigos",
    "tiktok": "panaderialos3",
    "anio_fundacion": "2018",
    "email_contacto": "info@panaderialos3amigos.com",
    "whatsapp_negocio": "+573001234567",
}

print(f"\nDatos de entrada:")
for k, v in datos.items():
    print(f"  {k}: {v}")

print("\nIniciando generacion (puede tardar 30-60s)...")
resultado = generar_web(datos, con_imagenes=True)

print("\n" + "=" * 70)
if resultado["exito"]:
    html = resultado["html"]
    print("GENERACION EXITOSA")
    print(f"  HTML: {len(html)} caracteres")
    print(f"  Fuente IA: {resultado.get('fuente')}")
    print()
    print("VERIFICACION DE SECCIONES DINAMICAS:")
    print(f"  Ubicacion (seccion):    {'SI' if 'ubicacion' in html.lower() else 'NO'}")
    print(f"  Google Maps iframe:     {'SI' if 'google.com/maps' in html else 'NO'}")
    print(f"  Horarios:               {'SI' if 'horario' in html.lower() else 'NO'}")
    print(f"  Instagram (link):       {'SI' if 'instagram.com' in html.lower() else 'NO'}")
    print(f"  Facebook (link):        {'SI' if 'facebook.com' in html.lower() else 'NO'}")
    print(f"  TikTok (link):          {'SI' if 'tiktok.com' in html.lower() else 'NO'}")
    print(f"  WhatsApp (link):        {'SI' if 'wa.me' in html else 'NO'}")
    print(f"  Anio 2018:              {'SI' if '2018' in html else 'NO'}")
    print(f"  Email contacto:         {'SI' if 'info@panaderialos3amigos.com' in html else 'NO'}")
    
    # Guardar el HTML para inspeccion visual
    with open("test_bloque3.html", "w", encoding="utf-8") as f:
        f.write(html)
    print()
    print("HTML guardado en: test_bloque3.html")
    print("Abri este archivo en el navegador para ver el resultado visual.")
else:
    print(f"GENERACION FALLIDA: {resultado.get('error')}")
print("=" * 70)
