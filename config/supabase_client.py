# supabase_client.py
# ============================================
# CREDENCIALES DE SUPABASE
# ============================================

class SupabaseConfig:
    def __init__(self, url, key):
        self.url = url
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

# ==========================================
# PEGA TUS DATOS DE SUPABASE AQUÍ ABAJO
# ==========================================
supabase = SupabaseConfig(
    url="https://gbjsjbiyoyjzodznrjjj.supabase.co",
    key="sb_secret_rRf3LEd9__R5rsP5T2d9yg_r-gwKnb2"
)
