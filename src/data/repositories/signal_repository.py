"""
KALDRA Signal Repository v1

Responsável por todas as operações de leitura/escrita na tabela `signals`
usando o SupabaseClient.
"""

from typing import Any, Dict, List, Optional
from src.infrastructure.supabase_client import SupabaseClient


class SignalRepository:
    """
    Interface de alto nível para a tabela `signals`.
    Toda a pipeline deve usar este repositório, não o cliente direto.
    """

    def __init__(self, client: Optional[SupabaseClient] = None) -> None:
        self.client = client or SupabaseClient()
        self.table = "signals"

    # ---------- Leitura ----------

    def list_signals(
        self,
        domain: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Lista sinais com filtros opcionais.
        
        Args:
            domain: Filtrar por domínio (alpha, geo, product, safeguard)
            limit: Número máximo de resultados
        
        Returns:
            Lista de sinais ou dict com erro
        """
        params = f"select=*&limit={limit}"
        if domain:
            params += f"&domain=eq.{domain}"

        return self.client.fetch(self.table, params)

    def get_signal_by_id(self, signal_id: str) -> Dict[str, Any]:
        """
        Busca um sinal específico por ID.
        
        Args:
            signal_id: UUID do sinal
        
        Returns:
            Sinal ou dict com erro
        """
        params = f"select=*&id=eq.{signal_id}"
        return self.client.fetch(self.table, params)

    # ---------- Escrita ----------

    def create_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo sinal.
        
        Espera um dict com os campos principais:
        - id (uuid) — opcional, pode ser gerado pelo banco
        - domain (required)
        - title (required)
        - summary
        - importance
        - confidence
        - raw_payload (jsonb)
        
        Args:
            data: Dados do sinal
        
        Returns:
            Sinal criado ou dict com erro
        """
        return self.client.insert(self.table, data)

    def upsert_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insere ou atualiza um sinal.
        
        Args:
            data: Dados do sinal (deve incluir id para atualização)
        
        Returns:
            Sinal upsertado ou dict com erro
        """
        return self.client.upsert(self.table, data)

    def delete_signal(self, signal_id: str) -> Dict[str, Any]:
        """
        Deleta um sinal por ID.
        
        Args:
            signal_id: UUID do sinal
        
        Returns:
            Resposta de sucesso ou dict com erro
        """
        return self.client.delete(self.table, {"id": signal_id})
