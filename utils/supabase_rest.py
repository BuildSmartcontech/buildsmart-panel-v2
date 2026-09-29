# utils/supabase_rest.py
# ============================================
# Cliente REST minimal estilo SDK oficial
# ============================================
# V1.1: Agrega metodo delete()
# V1.0: Cliente inicial (select, insert, update)
# ============================================

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class _Query:
    """Query builder minimal estilo SDK oficial."""

    def __init__(self, url, headers, tabla):
        self.url = f"{url}/rest/v1/{tabla}"
        self.headers = headers
        self._select = "*"
        self._filters = []
        self._order = None
        self._limit = None

    def select(self, cols="*"):
        self._select = cols
        return self

    def eq(self, col, val):
        self._filters.append((col, f"eq.{val}"))
        return self

    def order(self, col, desc=False):
        self._order = f"{col}.{'desc' if desc else 'asc'}"
        return self

    def limit(self, n):
        self._limit = n
        return self

    def execute(self):
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"

        params = {"select": self._select}
        for col, expr in self._filters:
            params[col] = expr
        if self._order:
            params["order"] = self._order
        if self._limit:
            params["limit"] = self._limit

        try:
            r = requests.get(self.url, headers=headers, params=params, timeout=15)
            if r.status_code == 200:
                return _Response(r.json())
            return _Response([], error=f"HTTP {r.status_code}: {r.text[:200]}")
        except Exception as e:
            return _Response([], error=str(e))


class _Response:
    def __init__(self, data, error=None):
        self.data = data if data is not None else []
        self.error = error


class SupabaseREST:
    """Cliente REST minimal estilo SDK oficial."""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.headers = {
            "apikey": self.key or "",
            "Authorization": f"Bearer {self.key or ''}",
            "Content-Type": "application/json",
        }
        self.disponible = bool(self.url and self.key)

    def table(self, nombre):
        if not self.disponible:
            raise RuntimeError("SupabaseREST: faltan SUPABASE_URL o SUPABASE_KEY en .env")
        return _Query(self.url, self.headers, nombre)

    def insert(self, tabla, data):
        """Insert directo (por si lo necesitas después)."""
        url = f"{self.url}/rest/v1/{tabla}"
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"
        try:
            r = requests.post(url, headers=headers, json=data, timeout=15)
            return _Response(r.json() if r.status_code in (200, 201) else [], error=None if r.status_code in (200, 201) else r.text)
        except Exception as e:
            return _Response([], error=str(e))

    def update(self, tabla, data, col, val):
        """Update simple: update(tabla, {campo: valor}, col_filtro, valor_filtro)."""
        url = f"{self.url}/rest/v1/{tabla}"
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"
        params = {col: f"eq.{val}"}
        try:
            r = requests.patch(url, headers=headers, params=params, json=data, timeout=15)
            return _Response(r.json() if r.status_code in (200, 204) else [], error=None if r.status_code in (200, 204) else r.text)
        except Exception as e:
            return _Response([], error=str(e))

    def delete(self, tabla, col, val):
        """Delete simple: delete(tabla, col_filtro, valor_filtro)."""
        url = f"{self.url}/rest/v1/{tabla}"
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"
        params = {col: f"eq.{val}"}
        try:
            r = requests.delete(url, headers=headers, params=params, timeout=15)
            return _Response(r.json() if r.status_code in (200, 204) else [], error=None if r.status_code in (200, 204) else r.text)
        except Exception as e:
            return _Response([], error=str(e))


# Singleton listo para importar
supabase_rest = SupabaseREST()


if __name__ == "__main__":
    print("Test SupabaseREST")
    if supabase_rest.disponible:
        r = supabase_rest.table("config_global").select("*").execute()
        print(f"config_global: {len(r.data)} filas")
        if r.error:
            print(f"Error: {r.error}")
    else:
        print("Faltan credenciales en .env")