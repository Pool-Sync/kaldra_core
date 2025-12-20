"""
Testa a conexão entre o KALDRA Core e o Supabase.

Uso:
    python -m src.scripts.test_supabase_connection
"""

import json
import os
import sys
import urllib.error
import urllib.request


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"[ERRO] Variável de ambiente não encontrada: {name}")
        sys.exit(1)
    return value


def main() -> None:
    supabase_url = get_env("SUPABASE_URL")
    # Preferimos a service role key se existir, senão cai na anon
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or get_env("SUPABASE_ANON_KEY")

    # Monta endpoint simples na tabela signals
    endpoint = supabase_url.rstrip("/") + "/rest/v1/signals?select=count&limit=1"

    print("🔌 Testando conexão com Supabase...")
    print(f"→ URL: {endpoint}")

    req = urllib.request.Request(endpoint)
    req.add_header("apikey", service_key)
    req.add_header("Authorization", f"Bearer {service_key}")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8") or "{}"
            print(f"✅ Resposta HTTP: {status}")

            try:
                data = json.loads(body)
                print("📦 Corpo (parse JSON ok):", data)
            except json.JSONDecodeError:
                print("ℹ️ Corpo (texto bruto):", body)

            if 200 <= status < 300:
                print("\n🎉 CONEXÃO SUPABASE OK — KALDRA conseguiu falar com o banco.")
                sys.exit(0)
            else:
                print("\n⚠️ Conseguiu conectar, mas recebeu status inesperado.")
                sys.exit(1)

    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTPError ao conectar: {e.code} {e.reason}")
        try:
            err_body = e.read().decode("utf-8")
            print("Corpo do erro:", err_body)
        except Exception:
            pass
        sys.exit(1)

    except urllib.error.URLError as e:
        print(f"\n❌ URLError ao conectar: {e.reason}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
