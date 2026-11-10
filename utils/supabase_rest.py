# utils/supabase_rest.py
# ============================================
# Cliente REST minimal estilo SDK oficial
# ============================================
# V1.5: Agrega metodos gte y lte para filtros de fecha.
# ============================================

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

MAX_REINTENTOS = 3
TIEMPO_ESPERA_BASE = 2

class _Query:
    def __init__(self, session, url, headers, tabla):
        self.session = session
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

    # NUEVOS MÉTODOS PARA LA PESTAÑA ARM
    def gte(self, col, val):
        self._filters.append((col, f"gte.{val}"))
        return self

    def lte(self, col, val):
        self._filters.append((col, f"lte.{val}"))
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

        for intento in range(MAX_REINTENTOS):
            try:
                r = self.session.get(self.url, headers=headers, params=params, timeout=30)
                if r.status_code == 200:
                    return _Response(r.json())
                elif r.status_code >= 500:
                    print(f"[SUPABASE REST] Error {r.status_code}, reintentando...")
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                    continue
                else:
                    return _Response([], error=f"HTTP {r.status_code}: {r.text[:200]}")
            except requests.exceptions.RequestException as e:
                print(f"[SUPABASE REST] Excepción: {e}, reintentando...")
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                else:
                    return _Response([], error=str(e))

        return _Response([], error="Falló después de múltiples reintentos")

class _Response:
    def __init__(self, data, error=None):
        self.data = data if data is not None else []
        self.error = error

class SupabaseREST:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "").rstrip("/")
        self.key = os.getenv("SUPABASE_KEY", "")
        self.disponible = bool(self.url and self.key)

        self.headers = {
            "apikey": self.key,
            "Content-Type": "application/json",
        }

        if self.key.startswith("eyJ"):
            self.headers["Authorization"] = f"Bearer {self.key}"

        self.session = requests.Session()

    def table(self, nombre):
        if not self.disponible:
            raise RuntimeError("SupabaseREST: faltan SUPABASE_URL o SUPABASE_KEY en .env")
        return _Query(self.session, self.url, self.headers, nombre)

    def insert(self, tabla, data):
        url = f"{self.url}/rest/v1/{tabla}"
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"
        for intento in range(MAX_REINTENTOS):
            try:
                r = self.session.post(url, headers=headers, json=data, timeout=30)
                if r.status_code in (200, 201):
                    return _Response(r.json())
                elif r.status_code >= 500:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                    continue
                else:
                    return _Response([], error=r.text)
            except requests.exceptions.RequestException as e:
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                else:
                    return _Response([], error=str(e))
        return _Response([], error="Falló después de múltiples reintentos")

    def update(self, tabla, data, col, val):
        url = f"{self.url}/rest/v1/{tabla}"
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"
        params = {col: f"eq.{val}"}
        for intento in range(MAX_REINTENTOS):
            try:
                r = self.session.patch(url, headers=headers, params=params, json=data, timeout=30)
                if r.status_code in (200, 204):
                    return _Response(r.json())
                elif r.status_code >= 500:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                    continue
                else:
                    return _Response([], error=r.text)
            except requests.exceptions.RequestException as e:
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                else:
                    return _Response([], error=str(e))
        return _Response([], error="Falló después de múltiples reintentos")

    def delete(self, tabla, col, val):
        url = f"{self.url}/rest/v1/{tabla}"
        headers = dict(self.headers)
        headers["Prefer"] = "return=representation"
        params = {col: f"eq.{val}"}
        for intento in range(MAX_REINTENTOS):
            try:
                r = self.session.delete(url, headers=headers, params=params, timeout=30)
                if r.status_code in (200, 204):
                    return _Response(r.json())
                elif r.status_code >= 500:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                    continue
                else:
                    return _Response([], error=r.text)
            except requests.exceptions.RequestException as e:
                if intento < MAX_REINTENTOS - 1:
                    time.sleep(TIEMPO_ESPERA_BASE * (intento + 1))
                else:
                    return _Response([], error=str(e))
        return _Response([], error="Falló después de múltiples reintentos")

supabase_rest = SupabaseREST()