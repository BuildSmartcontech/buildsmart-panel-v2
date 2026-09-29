# utils/web_templates.py
# ============================================
# TEMPLATES BASE PARA GENERACION DE WEBS
# ============================================
# Este archivo contiene los templates HTML base que se le pasan
# a la IA como referencia para que genere webs profesionales.
# ============================================

import datetime


# ============================================
# TEMPLATE: LANDING PAGE MODERNA
# ============================================

TEMPLATE_LANDING_MODERNA = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="__DESCRIPCION_SEO__">
    <title>__TITULO__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --color-primario: __COLOR_PRIMARIO__;
            --color-secundario: __COLOR_SECUNDARIO__;
            --color-texto: #1a1a1a;
            --color-fondo: #ffffff;
            --color-gris: #f5f5f5;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, sans-serif;
            color: var(--color-texto);
            background: var(--color-fondo);
            line-height: 1.6;
        }
        
        header {
            background: var(--color-primario);
            color: white;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        nav {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            text-decoration: none;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: opacity 0.3s;
        }
        
        .nav-links a:hover { opacity: 0.8; }
        
        .hero {
            background: linear-gradient(135deg, var(--color-primario), var(--color-secundario));
            color: white;
            padding: 6rem 2rem;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            opacity: 0.95;
        }
        
        .btn {
            display: inline-block;
            background: white;
            color: var(--color-primario);
            padding: 1rem 2.5rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            transition: transform 0.3s, box-shadow 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        section {
            padding: 5rem 2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-title {
            font-size: 2.2rem;
            margin-bottom: 1rem;
            text-align: center;
            color: var(--color-primario);
        }
        
        .section-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 3rem;
            font-size: 1.1rem;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .card {
            background: var(--color-gris);
            padding: 2rem;
            border-radius: 12px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }
        
        .card h3 {
            color: var(--color-primario);
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        
        .card p {
            color: #555;
            line-height: 1.7;
        }
        
        footer {
            background: var(--color-primario);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }
        
        footer p {
            opacity: 0.8;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .hero p { font-size: 1.1rem; }
            .nav-links { display: none; }
            .section-title { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="#" class="logo">__NOMBRE_NEGOCIO__</a>
            <ul class="nav-links">
                <li><a href="#servicios">Servicios</a></li>
                <li><a href="#nosotros">Nosotros</a></li>
                <li><a href="#contacto">Contacto</a></li>
            </ul>
        </nav>
    </header>
    
    <section class="hero">
        <h1>__TITULO_HERO__</h1>
        <p>__SUBTITULO_HERO__</p>
        <a href="#contacto" class="btn">__CTA_TEXTO__</a>
    </section>
    
    <section id="servicios">
        <div class="container">
            <h2 class="section-title">Nuestros Servicios</h2>
            <p class="section-subtitle">__SUBTITULO_SERVICIOS__</p>
            <div class="grid">
                __TARJETAS_SERVICIOS__
            </div>
        </div>
    </section>
    
    <section id="nosotros" style="background: var(--color-gris);">
        <div class="container">
            <h2 class="section-title">Sobre Nosotros</h2>
            <p class="section-subtitle">__TEXTO_NOSOTROS__</p>
        </div>
    </section>
    
    <section id="contacto">
        <div class="container">
            <h2 class="section-title">Contactanos</h2>
            <p class="section-subtitle">__TEXTO_CONTACTO__</p>
            <div style="text-align: center; margin-top: 2rem;">
                <a href="mailto:__EMAIL__" class="btn" style="background: var(--color-primario); color: white;">Enviar Mensaje</a>
            </div>
        </div>
    </section>
    
    <footer>
        <p><strong>__NOMBRE_NEGOCIO__</strong></p>
        <p>__DIRECCION__</p>
        <p>__TELEFONO__ | __EMAIL__</p>
        <p style="margin-top: 1rem; font-size: 0.9rem;">© __ANO__ __NOMBRE_NEGOCIO__. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
"""


# ============================================
# TEMPLATE: SITIO CORPORATIVO
# ============================================

TEMPLATE_CORPORATIVO = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="__DESCRIPCION_SEO__">
    <title>__TITULO__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --color-primario: __COLOR_PRIMARIO__;
            --color-secundario: __COLOR_SECUNDARIO__;
            --color-texto: #2c3e50;
            --color-fondo: #ffffff;
            --color-gris: #ecf0f1;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, sans-serif;
            color: var(--color-texto);
            background: var(--color-fondo);
            line-height: 1.6;
        }
        
        header {
            background: white;
            border-bottom: 1px solid #e0e0e0;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        nav {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--color-primario);
            text-decoration: none;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }
        
        .nav-links a {
            color: var(--color-texto);
            text-decoration: none;
            font-weight: 500;
        }
        
        .hero {
            background: linear-gradient(135deg, var(--color-primario), var(--color-secundario));
            color: white;
            padding: 5rem 2rem;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 2.8rem;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.2rem;
            opacity: 0.95;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        
        .section-title {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: var(--color-primario);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .card {
            background: white;
            padding: 2rem;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            transition: box-shadow 0.3s;
        }
        
        .card:hover {
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .card h3 {
            color: var(--color-primario);
            margin-bottom: 1rem;
        }
        
        footer {
            background: var(--color-texto);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="#" class="logo">__NOMBRE_NEGOCIO__</a>
            <ul class="nav-links">
                <li><a href="#servicios">Servicios</a></li>
                <li><a href="#nosotros">Nosotros</a></li>
                <li><a href="#contacto">Contacto</a></li>
            </ul>
        </nav>
    </header>
    
    <section class="hero">
        <h1>__TITULO_HERO__</h1>
        <p>__SUBTITULO_HERO__</p>
    </section>
    
    <div class="container">
        <h2 class="section-title">Nuestros Servicios</h2>
        <div class="grid">
            __TARJETAS_SERVICIOS__
        </div>
    </div>
    
    <div class="container" style="background: var(--color-gris);">
        <h2 class="section-title">Sobre Nosotros</h2>
        <p>__TEXTO_NOSOTROS__</p>
    </div>
    
    <div class="container">
        <h2 class="section-title">Contacto</h2>
        <p>__TEXTO_CONTACTO__</p>
        <p style="margin-top: 1rem;"><strong>Email:</strong> __EMAIL__</p>
        <p><strong>Telefono:</strong> __TELEFONO__</p>
        <p><strong>Direccion:</strong> __DIRECCION__</p>
    </div>
    
    <footer>
        <p><strong>__NOMBRE_NEGOCIO__</strong></p>
        <p>© __ANO__ Todos los derechos reservados.</p>
    </footer>
</body>
</html>
"""


# ============================================
# TEMPLATE: PORTAFOLIO
# ============================================

TEMPLATE_PORTAFOLIO = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="__DESCRIPCION_SEO__">
    <title>__TITULO__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --color-primario: __COLOR_PRIMARIO__;
            --color-secundario: __COLOR_SECUNDARIO__;
            --color-texto: #1a1a1a;
            --color-fondo: #fafafa;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, sans-serif;
            color: var(--color-texto);
            background: var(--color-fondo);
            line-height: 1.6;
        }
        
        header {
            padding: 2rem;
            text-align: center;
            background: white;
            border-bottom: 1px solid #e0e0e0;
        }
        
        header h1 {
            font-size: 2.5rem;
            color: var(--color-primario);
            margin-bottom: 0.5rem;
        }
        
        header p {
            color: #666;
            font-size: 1.1rem;
        }
        
        .galeria {
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
        }
        
        .proyecto {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        
        .proyecto:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        
        .proyecto-img {
            height: 220px;
            background: linear-gradient(135deg, var(--color-primario), var(--color-secundario));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
        }
        
        .proyecto-info {
            padding: 1.5rem;
        }
        
        .proyecto-info h3 {
            color: var(--color-primario);
            margin-bottom: 0.5rem;
        }
        
        .proyecto-info p {
            color: #666;
            font-size: 0.95rem;
        }
        
        footer {
            background: var(--color-primario);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            margin-top: 3rem;
        }
        
        @media (max-width: 768px) {
            header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <header>
        <h1>__NOMBRE_NEGOCIO__</h1>
        <p>__SUBTITULO_HERO__</p>
    </header>
    
    <div class="galeria">
        __PROYECTOS__
    </div>
    
    <footer>
        <p><strong>__NOMBRE_NEGOCIO__</strong></p>
        <p>__EMAIL__ | __TELEFONO__</p>
        <p>© __ANO__</p>
    </footer>
</body>
</html>
"""


# ============================================
# TEMPLATE: BLOG
# ============================================

TEMPLATE_BLOG = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="__DESCRIPCION_SEO__">
    <title>__TITULO__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --color-primario: __COLOR_PRIMARIO__;
            --color-secundario: __COLOR_SECUNDARIO__;
            --color-texto: #2c3e50;
        }
        
        body {
            font-family: Georgia, serif;
            color: var(--color-texto);
            background: #fafafa;
            line-height: 1.8;
        }
        
        header {
            background: var(--color-primario);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        header p {
            opacity: 0.9;
        }
        
        .articulos {
            max-width: 800px;
            margin: 3rem auto;
            padding: 0 2rem;
        }
        
        .articulo {
            background: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .articulo h2 {
            color: var(--color-primario);
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }
        
        .articulo .fecha {
            color: #999;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .articulo p {
            color: #444;
        }
        
        footer {
            background: var(--color-texto);
            color: white;
            padding: 2rem;
            text-align: center;
            margin-top: 3rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>__NOMBRE_NEGOCIO__</h1>
        <p>__SUBTITULO_HERO__</p>
    </header>
    
    <div class="articulos">
        __ARTICULOS__
    </div>
    
    <footer>
        <p>© __ANO__ __NOMBRE_NEGOCIO__</p>
    </footer>
</body>
</html>
"""


# ============================================
# FUNCION: OBTENER TEMPLATE SEGUN TIPO
# ============================================

def obtener_template(tipo_pagina):
    """Obtiene el template base según el tipo de página"""
    
    templates = {
        "Landing Page": TEMPLATE_LANDING_MODERNA,
        "Sitio Corporativo": TEMPLATE_CORPORATIVO,
        "Portafolio": TEMPLATE_PORTAFOLIO,
        "Blog": TEMPLATE_BLOG,
    }
    
    return templates.get(tipo_pagina, TEMPLATE_LANDING_MODERNA)


# ============================================
# FUNCION: GENERAR TARJETAS DE SERVICIOS
# ============================================

def generar_tarjetas_servicios(servicios):
    """Genera el HTML de las tarjetas de servicios"""
    
    if not servicios:
        servicios = ["Servicio 1", "Servicio 2", "Servicio 3"]
    
    html = ""
    for servicio in servicios:
        html += (
            '<div class="card">\n'
            '    <h3>' + str(servicio) + '</h3>\n'
            '    <p>Descripcion del servicio ' + str(servicio) + '.</p>\n'
            '</div>\n'
        )
    
    return html


# ============================================
# FUNCION: GENERAR PROYECTOS
# ============================================

def generar_proyectos(proyectos):
    """Genera el HTML de los proyectos del portafolio"""
    
    if not proyectos:
        proyectos = ["Proyecto 1", "Proyecto 2", "Proyecto 3"]
    
    html = ""
    for proyecto in proyectos:
        html += (
            '<div class="proyecto">\n'
            '    <div class="proyecto-img">&#128193;</div>\n'
            '    <div class="proyecto-info">\n'
            '        <h3>' + str(proyecto) + '</h3>\n'
            '        <p>Descripcion del proyecto.</p>\n'
            '    </div>\n'
            '</div>\n'
        )
    
    return html


# ============================================
# FUNCION: GENERAR ARTICULOS
# ============================================

def generar_articulos(articulos):
    """Genera el HTML de los artículos del blog"""
    
    if not articulos:
        articulos = ["Articulo 1", "Articulo 2", "Articulo 3"]
    
    html = ""
    for articulo in articulos:
        html += (
            '<article class="articulo">\n'
            '    <h2>' + str(articulo) + '</h2>\n'
            '    <p class="fecha">' + datetime.datetime.now().strftime("%d/%m/%Y") + '</p>\n'
            '    <p>Contenido del articulo.</p>\n'
            '</article>\n'
        )
    
    return html


# ============================================
# FUNCION: RENDERIZAR TEMPLATE (CON REPLACE)
# ============================================

def renderizar_template(tipo_pagina, datos):
    """
    Renderiza el template con los datos proporcionados.
    Usa .replace() en vez de .format() para evitar conflictos con CSS.
    """
    
    template = obtener_template(tipo_pagina)
    
    # Valores por defecto
    valores = {
        "__NOMBRE_NEGOCIO__": datos.get("nombre_negocio", "Mi Negocio"),
        "__TITULO__": datos.get("titulo", "Mi Negocio"),
        "__DESCRIPCION_SEO__": datos.get("descripcion_seo", "Descripcion"),
        "__TITULO_HERO__": datos.get("titulo_hero", "Bienvenido"),
        "__SUBTITULO_HERO__": datos.get("subtitulo_hero", "Descripcion breve"),
        "__CTA_TEXTO__": datos.get("cta_texto", "Contactanos"),
        "__SUBTITULO_SERVICIOS__": datos.get("subtitulo_servicios", "Lo que ofrecemos"),
        "__TARJETAS_SERVICIOS__": generar_tarjetas_servicios(datos.get("servicios")),
        "__TEXTO_NOSOTROS__": datos.get("texto_nosotros", "Nuestra historia"),
        "__TEXTO_CONTACTO__": datos.get("texto_contacto", "Contactanos para mas informacion"),
        "__PROYECTOS__": generar_proyectos(datos.get("proyectos")),
        "__ARTICULOS__": generar_articulos(datos.get("articulos")),
        "__EMAIL__": datos.get("email", "contacto@negocio.com"),
        "__TELEFONO__": datos.get("telefono", "+57 300 000 0000"),
        "__DIRECCION__": datos.get("direccion", "Bogota, Colombia"),
        "__COLOR_PRIMARIO__": datos.get("color_primario", "#0f3460"),
        "__COLOR_SECUNDARIO__": datos.get("color_secundario", "#f39c12"),
        "__ANO__": str(datetime.datetime.now().year),
    }
    
    # Reemplazar cada marcador
    html = template
    for marcador, valor in valores.items():
        html = html.replace(marcador, str(valor))
    
    return html


# ============================================
# PRUEBA
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROBANDO TEMPLATES BASE")
    print("=" * 60)
    
    for tipo in ["Landing Page", "Sitio Corporativo", "Portafolio", "Blog"]:
        datos = {
            "nombre_negocio": "Construcciones ABC",
            "titulo": "Construcciones ABC - Especialistas en Obra Civil",
            "descripcion_seo": "30 anos de experiencia en construccion",
            "titulo_hero": "Construimos tu hogar sonado",
            "subtitulo_hero": "30 anos de experiencia en Bogota",
            "servicios": ["Obra Civil", "Reformas", "Diseno"],
            "proyectos": ["Casa Moderna", "Edificio Centro", "Reforma Oficina"],
            "articulos": ["Tendencias 2026", "Como elegir contratista", "Presupuesto"],
        }
        
        html = renderizar_template(tipo, datos)
        print("\n" + tipo + ": " + str(len(html)) + " caracteres")
        print("Primeras 100 letras: " + html[:100])
    
    print("\n" + "=" * 60)
    print("Templates funcionando correctamente")