import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("LEADS EN crm_leads (ultimos 10)")
print("=" * 70)

try:
    from utils.supabase_rest import supabase_rest
except ImportError as e:
    print(f"ERROR importando supabase_rest: {e}")
    print("Buscando alternativas...")
    try:
        from utils.supabase_client import supabase
        print("Usando supabase_client.supabase")

        # Query manual
        url = supabase.url + "/rest/v1/crm_leads?select=*&order=created_at.desc&limit=10"
        import requests
        r = requests.get(url, headers=supabase.headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            print(f"\nTotal: {len(data)}\n")
            for lead in data:
                print(f"ID:       {str(lead.get('id'))[:8]}...")
                print(f"  Nombre:   {lead.get('nombre')}")
                print(f"  Email:    {lead.get('email')}")
                print(f"  Telefono: {lead.get('telefono')}")
                print(f"  Mensaje:  {(lead.get('mensaje') or '')[:60]}")
                print(f"  Estado:   {lead.get('estado')}")
                print(f"  Pedido:   {lead.get('pedido_id')}")
                print(f"  Fecha:    {lead.get('created_at')}")
                print()
        else:
            print(f"Error HTTP {r.status_code}: {r.text[:300]}")
    except Exception as e2:
        print(f"ERROR alternativo: {e2}")
        sys.exit(1)
    sys.exit(0)

r = supabase_rest.table("crm_leads").select("*").order("created_at", desc=True).limit(10).execute()

if not r.data:
    print("No hay leads en la tabla crm_leads")
else:
    print(f"Total: {len(r.data)}\n")
    for lead in r.data:
        print(f"ID:       {str(lead.get('id'))[:8]}...")
        print(f"  Nombre:   {lead.get('nombre')}")
        print(f"  Email:    {lead.get('email')}")
        print(f"  Telefono: {lead.get('telefono')}")
        print(f"  Mensaje:  {(lead.get('mensaje') or '')[:60]}")
        print(f"  Estado:   {lead.get('estado')}")
        print(f"  Pedido:   {lead.get('pedido_id')}")
        print(f"  Fecha:    {lead.get('created_at')}")
        print()
print("=" * 70)
