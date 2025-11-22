import torch
import torch.nn as nn
import torch.nn.functional as F

class KaldraKindraCulturalMod(nn.Module):
    """
    Camada de modulação cultural 3×48 sobre distribuição Δ144.

    Esta camada aplica um viés cultural dinâmico sobre as probabilidades dos arquétipos,
    baseado em um vetor de contexto (embedding).

    A modulação ocorre em 3 planos (3, 6, 9), cada um com 48 vetores Kindra,
    que são projetados para o espaço de 144 estados.

    Inputs:
      - archetype_probs: tensor (..., 144) - Probabilidades base dos estados
      - context_vec: tensor (..., d_ctx) - Vetor de contexto (embedding)
    """

    def __init__(self, d_ctx: int = 256):
        super().__init__()
        self.ctx_norm = nn.LayerNorm(d_ctx)

        # Projeção do contexto para os 48 vetores de cada plano
        self.W = nn.ModuleDict({
            p: nn.Linear(d_ctx, 48)
            for p in ["3", "6", "9"]
        })
        
        # Matriz de mapeamento 48 (Kindras) → 144 (Estados Δ144)
        # Inicializada com valores pequenos para começar com modulação suave
        self.M = nn.ParameterDict({
            p: nn.Parameter(torch.randn(48, 144) * 0.01)
            for p in ["3", "6", "9"]
        })
        
        # Pesos globais de cada plano (lambda_p), aprendíveis
        # Inicializados para resultar em ~0.5 após sigmoide
        self.lambda_raw = nn.Parameter(torch.zeros(3))

    def lambdas(self) -> torch.Tensor:
        """Retorna os pesos λ_p de cada plano no intervalo (0, 1)."""
        return torch.sigmoid(self.lambda_raw)

    def forward(
        self,
        archetype_probs: torch.Tensor,
        context_vec: torch.Tensor,
        apply_softmax: bool = True,
    ) -> torch.Tensor:
        """
        Aplica a modulação cultural.
        """
        x = self.ctx_norm(context_vec)
        gains = []
        lambdas = self.lambdas()

        # Itera sobre os planos 3, 6, 9
        for i, p in enumerate(["3", "6", "9"]):
            # 1. Ativação dos 48 Kindras do plano p a partir do contexto
            c_p = torch.sigmoid(self.W[p](x))            # (..., 48)
            
            # 2. Projeção dos Kindras para o espaço de 144 estados
            # c_p @ M[p] -> (..., 48) x (48, 144) -> (..., 144)
            g_p = torch.sigmoid(c_p @ self.M[p])         # (..., 144)
            
            # 3. Aplica peso do plano
            gains.append(lambdas[i] * g_p)

        # Soma os ganhos de todos os planos
        # gain_total será um fator multiplicativo >= 1.0 (base)
        # Somamos 1.0 para que se gains forem zero, a modulação seja neutra (identidade)
        gain_total = 1.0 + sum(gains)
        
        # Modula as probabilidades originais
        modulated = archetype_probs * gain_total

        if apply_softmax:
            return F.softmax(modulated, dim=-1)
        
        return modulated
