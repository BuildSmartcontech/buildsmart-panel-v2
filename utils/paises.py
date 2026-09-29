# utils/paises.py
# ============================================
# LISTA GLOBAL DE PAISES - SAMU IA
# ============================================
# V1.0: Paises con prefijos telefonicos internacionales
#       Prioridad LATAM, luego Norteamerica, Europa, resto.
# ============================================

PAISES = [
    # ==========================================
    # LATINOAMERICA (prioridad)
    # ==========================================
    {"codigo": "CO", "nombre": "Colombia",               "prefijo": "+57"},
    {"codigo": "MX", "nombre": "Mexico",                 "prefijo": "+52"},
    {"codigo": "AR", "nombre": "Argentina",              "prefijo": "+54"},
    {"codigo": "CL", "nombre": "Chile",                  "prefijo": "+56"},
    {"codigo": "PE", "nombre": "Peru",                   "prefijo": "+51"},
    {"codigo": "EC", "nombre": "Ecuador",                "prefijo": "+593"},
    {"codigo": "VE", "nombre": "Venezuela",              "prefijo": "+58"},
    {"codigo": "BO", "nombre": "Bolivia",                "prefijo": "+591"},
    {"codigo": "PY", "nombre": "Paraguay",               "prefijo": "+595"},
    {"codigo": "UY", "nombre": "Uruguay",                "prefijo": "+598"},
    {"codigo": "BR", "nombre": "Brasil",                 "prefijo": "+55"},
    {"codigo": "CR", "nombre": "Costa Rica",             "prefijo": "+506"},
    {"codigo": "PA", "nombre": "Panama",                 "prefijo": "+507"},
    {"codigo": "GT", "nombre": "Guatemala",              "prefijo": "+502"},
    {"codigo": "SV", "nombre": "El Salvador",            "prefijo": "+503"},
    {"codigo": "HN", "nombre": "Honduras",               "prefijo": "+504"},
    {"codigo": "NI", "nombre": "Nicaragua",              "prefijo": "+505"},
    {"codigo": "DO", "nombre": "Republica Dominicana",   "prefijo": "+1"},
    {"codigo": "CU", "nombre": "Cuba",                   "prefijo": "+53"},
    {"codigo": "PR", "nombre": "Puerto Rico",            "prefijo": "+1"},
    # ==========================================
    # NORTEAMERICA
    # ==========================================
    {"codigo": "US", "nombre": "Estados Unidos",         "prefijo": "+1"},
    {"codigo": "CA", "nombre": "Canada",                 "prefijo": "+1"},
    # ==========================================
    # EUROPA
    # ==========================================
    {"codigo": "ES", "nombre": "Espana",                 "prefijo": "+34"},
    {"codigo": "PT", "nombre": "Portugal",               "prefijo": "+351"},
    {"codigo": "FR", "nombre": "Francia",                "prefijo": "+33"},
    {"codigo": "IT", "nombre": "Italia",                 "prefijo": "+39"},
    {"codigo": "DE", "nombre": "Alemania",               "prefijo": "+49"},
    {"codigo": "GB", "nombre": "Reino Unido",            "prefijo": "+44"},
    # ==========================================
    # OTROS
    # ==========================================
    {"codigo": "XX", "nombre": "Otro pais",              "prefijo": "+"},
]


PAISES_DEFAULT = "Colombia"


def obtener_prefijo(nombre_pais):
    """Devuelve el prefijo telefonico de un pais."""
    if not nombre_pais:
        return "+"
    for p in PAISES:
        if p["nombre"] == nombre_pais:
            return p["prefijo"]
    return "+"


def obtener_nombres():
    """Devuelve solo la lista de nombres (para selectbox)."""
    return [p["nombre"] for p in PAISES]


if __name__ == "__main__":
    print("=" * 60)
    print("TEST PAISES")
    print("=" * 60)
    print(f"Total: {len(PAISES)}")
    print()
    for p in PAISES[:5]:
        print(f"  {p['codigo']} | {p['nombre']:25} | {p['prefijo']}")
    print(f"  ... y {len(PAISES) - 5} mas")
    print()
    print("Test obtener_prefijo:")
    for test in ["Colombia", "Mexico", "Espana", "Argentina", "Otro pais", "NoExiste"]:
        print(f"  {test:15} -> {obtener_prefijo(test)}")
    print("=" * 60)