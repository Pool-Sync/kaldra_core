"""
Teste rápido do SignalRepository com Supabase real.

Uso:
    python3 -m src.scripts.test_signal_repository
"""

import uuid
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.repositories.signal_repository import SignalRepository


def main() -> None:
    print("🔧 Testando SignalRepository v1...")
    
    try:
        repo = SignalRepository()
        print("✅ Repository initialized")
        
        # 1) Listar sinais existentes (deve vir vazio no começo)
        print("\n📊 Listando sinais existentes...")
        res = repo.list_signals(limit=5)
        
        if "error" in res:
            print(f"❌ Erro ao listar: {res}")
        elif isinstance(res, list):
            print(f"✅ Listagem OK - {len(res)} sinais encontrados")
            for signal in res[:3]:  # Show first 3
                print(f"  • {signal.get('title', 'N/A')}")
        else:
            print(f"ℹ️ Resposta: {res}")
        
        # 2) Criar um sinal de teste
        test_id = str(uuid.uuid4())
        print(f"\n➕ Criando sinal de teste (ID: {test_id[:8]}...)...")
        
        create_res = repo.create_signal({
            "id": test_id,
            "domain": "alpha",
            "title": "Signal de teste local",
            "summary": "Gerado pelo test_signal_repository.py",
            "importance": 0.5,
            "raw_payload": {"source": "local_test"}
        })
        
        if "error" in create_res:
            print(f"❌ Erro ao criar: {create_res}")
        else:
            print(f"✅ Sinal criado com sucesso")
            if isinstance(create_res, list) and len(create_res) > 0:
                print(f"  • Title: {create_res[0].get('title', 'N/A')}")
        
        # 3) Buscar pelo ID
        print(f"\n🔍 Buscando sinal pelo ID...")
        get_res = repo.get_signal_by_id(test_id)
        
        if "error" in get_res:
            print(f"❌ Erro ao buscar: {get_res}")
        elif isinstance(get_res, list):
            if len(get_res) > 0:
                print(f"✅ Sinal encontrado")
                print(f"  • Title: {get_res[0].get('title', 'N/A')}")
                print(f"  • Domain: {get_res[0].get('domain', 'N/A')}")
            else:
                print("⚠️ Nenhum sinal encontrado com esse ID")
        
        # 4) Deletar o sinal
        print(f"\n🗑️ Deletando sinal de teste...")
        del_res = repo.delete_signal(test_id)
        
        if "error" in del_res:
            print(f"❌ Erro ao deletar: {del_res}")
        else:
            print(f"✅ Sinal deletado com sucesso")
        
        print("\n🎉 Teste SignalRepository concluído.")
        
    except RuntimeError as e:
        print(f"\n❌ Erro de inicialização: {e}")
        print("Verifique se o .env está configurado corretamente")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
