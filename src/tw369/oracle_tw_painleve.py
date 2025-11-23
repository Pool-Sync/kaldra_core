"""
TW-Painlevé Oracle Module
=========================
Detector de anomalias baseado na distribuição de Tracy-Widom e equações de Painlevé II.

Este módulo analisa janelas de sinais (matrizes de covariância de Wishart) para detectar
transições de fase críticas no sistema KALDRA.
"""

from dataclasses import dataclass
import numpy as np
from typing import Tuple, Optional

@dataclass
class TWConfig:
    """Configuração para o Oracle TW-Painlevé."""
    window_size: int = 100
    alpha: float = 0.99  # Nível de significância (99%)
    min_samples: int = 30

@dataclass
class TWStats:
    """Estatísticas retornadas pelo Oracle."""
    lambda_max: float
    threshold: float
    num_eigenvalues: int

class TWPainleveOracle:
    """
    Oráculo que monitora o maior autovalor (lambda_max) da matriz de covariância
    de uma janela de sinais. Se lambda_max exceder o limiar previsto pela
    distribuição de Tracy-Widom (TW1), dispara um alerta de anomalia/transição.
    """

    def __init__(self, config: Optional[TWConfig] = None):
        self.config = config or TWConfig()

    def compute_covariance(self, window: np.ndarray) -> np.ndarray:
        """
        Calcula a matriz de covariância empírica.
        window: shape (T, m) onde T é tempo/amostras e m é dimensão/features.
        Retorna matriz (m, m).
        """
        # Centralizar dados
        centered = window - np.mean(window, axis=0)
        # Covariância (normalizada por T-1)
        cov = np.cov(centered, rowvar=False)
        return cov

    def tracy_widom_threshold(self, m: int, alpha: float) -> Tuple[float, float]:
        """
        Retorna (mu_m, sigma_m) aproximados e calcula o threshold crítico.
        
        Baseado na teoria de Matrizes Aleatórias (RMT):
        Para matrizes de Wishart (ruído branco), o maior autovalor flutua
        conforme a distribuição Tracy-Widom (beta=1 para GOE, mas usamos aproximação geral).
        
        Aproximação simplificada para threshold:
        mu_approx = (sqrt(m) + sqrt(T))^2  (limite de Marchenko-Pastur soft edge)
        sigma_approx = mu_approx * (1/sqrt(m) + 1/sqrt(T))^(1/3) ... (heurística simples aqui)
        
        NOTA: Esta é uma heurística para detecção de sinal vs ruído.
        """
        # Heurística simples baseada em Marchenko-Pastur edge para matrizes quadradas/retangulares
        # Assumindo T ~= window_size da config para normalização
        T = self.config.window_size
        ratio = m / T
        
        # Limite superior de Marchenko-Pastur (MP) para lambda_max teórico de ruído
        lambda_plus = (1 + np.sqrt(ratio)) ** 2
        
        # Scaling factor para TW (sigma)
        # sigma_m ~ lambda_plus * m^(-2/3) (ordem de grandeza)
        sigma_m = lambda_plus * (m ** (-2/3))
        
        # Quantil para alpha=0.99 na TW1 é aprox 2.02
        # (Valores tabelados: 95% ~ 0.98, 99% ~ 2.02)
        z_alpha = 2.02 if alpha >= 0.99 else 0.98
        
        threshold = lambda_plus + (sigma_m * z_alpha)
        
        return lambda_plus, threshold

    def painleve_filter(self, eigenvalues: np.ndarray) -> np.ndarray:
        """
        Aplica filtro baseado na solução de Painlevé II (Hastings-McLeod).
        
        Nesta versão (Stub Funcional):
        Aplica uma correção não-linear aos autovalores próximos da borda (edge)
        para simular o "soft edge" da distribuição de Tracy-Widom.
        
        A correção empurra autovalores extremos levemente em direção ao centro,
        reduzindo falsos positivos de ruído.
        """
        if len(eigenvalues) == 0:
            return eigenvalues
            
        # Ordena para garantir que tratamos o maior (lambda_max) corretamente
        sorted_eigs = np.sort(eigenvalues)
        lambda_max = sorted_eigs[-1]
        
        # Heurística de correção de borda (Painlevé II approximation stub)
        # q(s) ~ Ai(s) para s -> +inf
        # Aplicamos um damping suave baseado na magnitude
        
        # Se lambda_max for muito grande, o filtro atenua levemente (supressão de ruído)
        # Se for pequeno, mantém.
        
        # Fator de correção simulado:
        correction = 1.0
        if lambda_max > 2.0: # Assumindo dados normalizados
             correction = 0.98 # 2% damping na cauda extrema
             
        filtered = sorted_eigs * correction
        
        return filtered

    def detect(self, window: np.ndarray) -> Tuple[bool, TWStats]:
        """
        Recebe janela de sinais (T, m).
        1. Calcula C = cov(window)
        2. Obtém autovalores e pega lambda_max
        3. Estima threshold TW
        4. Retorna (trigger, stats)
        """
        T, m = window.shape
        
        if T < self.config.min_samples:
            # Janela muito pequena, não confiável
            return False, TWStats(0.0, 0.0, m)

        # 1. Covariância
        cov = self.compute_covariance(window)
        
        # 2. Autovalores (apenas parte real, assumindo simetria/hermitiana)
        eigenvalues = np.linalg.eigvalsh(cov)
        # Aplica filtro (placeholder)
        eigenvalues = self.painleve_filter(eigenvalues)
        
        lambda_max = float(np.max(eigenvalues))
        
        # 3. Threshold
        # Normalizamos lambda_max pela variância do ruído se soubéssemos sigma^2,
        # aqui assumimos dados padronizados ou comparamos com MP teórico relativo.
        # Para simplificar o uso prático sem calibração de ruído:
        # Usamos a heurística implementada em tracy_widom_threshold.
        _, threshold = self.tracy_widom_threshold(m, self.config.alpha)
        
        # Ajuste de escala: se a janela não for normalizada (var=1), o threshold MP
        # precisa escalar com a variância média dos dados.
        # Estimativa robusta de sigma^2 local: mediana dos autovalores ou traço/m
        sigma_sq_est = np.mean(np.diag(cov)) # traço/m = variância média
        threshold_scaled = threshold * sigma_sq_est

        stats = TWStats(
            lambda_max=float(lambda_max),
            threshold=float(threshold),
            num_eigenvalues=len(eigenvalues),
        )
        
        return bool(lambda_max > threshold), stats
