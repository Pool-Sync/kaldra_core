"""
KALDRA Supabase Client (REST)
Versão: v1
Funções básicas para leitura/escrita usando a REST API do Supabase.
"""

import os
import urllib.request
import urllib.error
import json
from typing import Any, Dict, List, Optional


class SupabaseClient:
    """
    Cliente REST simples para o Supabase.
    Usa SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY do .env.
    """

    def __init__(self) -> None:
        self.url = os.getenv("SUPABASE_URL")
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not self.url or not self.service_key:
            raise RuntimeError("Supabase env vars missing.")

    def _make_request(
        self,
        path: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        params: Optional[str] = None,
    ) -> Dict[str, Any]:

        endpoint = self.url.rstrip("/") + path
        if params:
            endpoint += f"?{params}"

        req = urllib.request.Request(endpoint, method=method)
        req.add_header("apikey", self.service_key)
        req.add_header("Authorization", f"Bearer {self.service_key}")
        req.add_header("Content-Type", "application/json")

        if data is not None:
            req.data = json.dumps(data).encode("utf-8")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode("utf-8") or "{}"
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return {"raw": raw}

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            return {"error": e.code, "message": err_body}

        except Exception as e:
            return {"error": "network", "message": str(e)}

    # ---------- Public API ----------

    def fetch(self, table: str, params: str = "select=*") -> Dict[str, Any]:
        return self._make_request(f"/rest/v1/{table}", "GET", None, params)

    def insert(self, table: str, data: Dict) -> Dict[str, Any]:
        return self._make_request(f"/rest/v1/{table}", "POST", data)

    def upsert(self, table: str, data: Dict) -> Dict[str, Any]:
        return self._make_request(f"/rest/v1/{table}", "POST", data, "on_conflict=id")

    def delete(self, table: str, match: Dict) -> Dict[str, Any]:
        params = "&".join(f"{k}=eq.{v}" for k, v in match.items())
        return self._make_request(f"/rest/v1/{table}", "DELETE", None, params)
