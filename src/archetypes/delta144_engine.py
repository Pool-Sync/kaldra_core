"""
KALDRA — Delta144 Engine
========================

Motor Δ144 (Delta-144) — Arquétipos × Estados

Responsabilidades:
- Carregar os 12 arquétipos (archetypes.core.json)
- Carregar os 144 estados (delta144_states.json)
- Carregar os Modifiers (archetype_modifiers.core.json)
- v2.7: Carregar as 48 Polarities (polarities.json)
- Inferir o estado Δ144 mais provável a partir de:
    - embedding semântico (v2.3+)
    - scores de plano TW (3/6/9)
    - scores de perfil (EXPANSIVE/CONTRACTIVE/TRANSCENDENT)
    - modifiers dinâmicos ativos
e traduz isso para um estado Δ144 + modifiers.

v2.7: Agora com auto-inferência de modifiers via embeddings.
"""

import json
import numpy as np
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from src.core.embedding_generator import EmbeddingGenerator, EmbeddingConfig
from src.config import (
    ARCHETYPES_12_FILE,
    DELTA144_STATES_FILE,
    MODIFIERS_FILE,
    POLARITIES_FILE,
    KALDRA_EMBEDDINGS_MODE,
    KALDRA_EMBEDDINGS_API_KEY,
    KALDRA_EMBEDDINGS_MODEL,
)
from .delta12_vector import Delta12Vector


# ---------------------------------------------------------------------------
# Dataclasses básicas
# ---------------------------------------------------------------------------


@dataclass
class Archetype:
    id: str
    label: str
    essence: str
    light: str
    shadow: str
    drives: List[str]
    journey_role: str
    stoic_axis: str
    description: str


@dataclass
class ArchetypeState:
    """
    Representa uma célula da matriz Δ144 (arquetipo × estado).
    """
    id: str
    archetype_id: str
    row: int
    col: int
    label: str
    profile: str  # "EXPANSIVE" | "CONTRACTIVE" | "TRANSCENDENT"
    tw_plane_default: str  # "3", "6", "9"
    description: str
    default_modifiers: List[str] = field(default_factory=list)
    allowed_modifiers: List[str] = field(default_factory=list)


@dataclass
class Modifier:
    """
    Modifier (qualificador dinâmico) que pode ser aplicado a um estado Δ144.
    """
    id: str
    label: str
    category: str
    description: str
    tw_alignment: List[str]


@dataclass
class Polarity:
    """
    Polarity (tensão dimensional) que estrutura a experiência.
    
    Polaridades representam tensões fundamentais como:
    - LIGHT ↔ SHADOW
    - ORDER ↔ CHAOS
    - EXPANSION ↔ CONTRACTION
    
    v2.7: Polarities são usadas para modular Δ12, TW369, e análise narrativa.
    """
    id: str
    label: str
    description: str
    dimension: str  # e.g., "existential", "structure", "energy"
    tw_alignment: List[str]  # TW planes this polarity aligns with (3/6/9)


@dataclass
class StateInferenceResult:
    """
    Resultado final da inferência de estado Δ144.
    """
    archetype: Archetype
    state: ArchetypeState
    active_modifiers: List[Modifier]
    scores: Dict[str, Any]
    probs: Optional[List[float]] = None  # Vetor de probabilidades (144)
    polarity_scores: Dict[str, float] = field(default_factory=dict)  # v2.7

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization."""
        return {
            "archetype": {
                "id": self.archetype.id,
                "label": self.archetype.label,
                "essence": self.archetype.essence,
            },
            "state": {
                "id": self.state.id,
                "label": self.state.label,
                "profile": self.state.profile,
                "description": self.state.description,
            },
            "active_modifiers": [asdict(m) for m in self.active_modifiers],
            "scores": self.scores,
            "probs": self.probs,
            "polarity_scores": self.polarity_scores,  # v2.7
        }


# ---------------------------------------------------------------------------
# Funções utilitárias de carregamento
# ---------------------------------------------------------------------------


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_archetypes(path: Path) -> Dict[str, Archetype]:
    data = _load_json(path)
    result: Dict[str, Archetype] = {}
    for raw in data:
        a = Archetype(
            id=raw["id"],
            label=raw["label"],
            essence=raw.get("essence", ""),
            light=raw.get("light", ""),
            shadow=raw.get("shadow", ""),
            drives=raw.get("drives", []),
            journey_role=raw.get("journey_role", ""),
            stoic_axis=raw.get("stoic_axis", ""),
            description=raw.get("description", ""),
        )
        result[a.id] = a
    return result


def load_states(path: Path) -> Dict[str, ArchetypeState]:
    data = _load_json(path)
    result: Dict[str, ArchetypeState] = {}
    for raw in data:
        s = ArchetypeState(
            id=raw["id"],
            archetype_id=raw["archetype_id"],
            row=int(raw["row"]),
            col=int(raw["col"]),
            label=raw["label"],
            profile=raw["profile"],
            tw_plane_default=str(raw["tw_plane_default"]),
            description=raw.get("description", ""),
            default_modifiers=raw.get("default_modifiers", []),
            allowed_modifiers=raw.get("allowed_modifiers", []),
        )
        result[s.id] = s
    return result


def load_modifiers(path: Path) -> Dict[str, Modifier]:
    """
    Carrega modifiers do arquivo JSON.
    """
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    modifiers = {}
    for item in data:
        mid = item["id"]
        modifiers[mid] = Modifier(
            id=mid,
            label=item["label"],
            category=item["category"],
            description=item["description"],
            tw_alignment=item.get("tw_alignment", []),
        )
    return modifiers


def load_polarities(path: Path) -> Dict[str, Polarity]:
    """
    Carrega polarities do arquivo JSON.
    
    v2.7: Polarities são tensões dimensionais fundamentais que modulam
    Δ12, TW369, e análise narrativa.
    
    Args:
        path: Caminho para polarities.json
        
    Returns:
        Dict mapeando polarity_id -> Polarity
    """
    if not path.exists():
        # Safe fallback: se arquivo não existe, retorna dict vazio
        return {}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        polarities = {}
        for item in data:
            pol_id = item["id"]
            polarities[pol_id] = Polarity(
                id=pol_id,
                label=item["label"],
                description=item["description"],
                dimension=item["dimension"],
                tw_alignment=item.get("tw_alignment", []),
            )
        
        return polarities
    
    except Exception as e:
        # Log warning but don't crash
        print(f"Warning: Failed to load polarities from {path}: {e}")
        return {}


# ---------------------------------------------------------------------------
# Núcleo do motor Δ144
# ---------------------------------------------------------------------------


class Delta144Engine:
    """
    Motor arquetípico da Δ144.

    Não faz parsing de texto nem cálculo de TW369 diretamente.
    Recebe **sinais já agregados** e devolve um estado Δ144 coerente.

    Exemplo de uso:

        engine = Delta144Engine.from_default_files()

        result = engine.infer_state(
            archetype_id="A07_RULER",
            plane_scores={"3": 0.2, "6": 0.6, "9": 0.2},
            profile_scores={"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2},
            modifier_scores={"MOD_SHADOW": 0.8, "MOD_DEFENSIVE": 0.6}
        )

        print(result.to_dict())
    """

    def __init__(
        self,
        archetypes: Dict[str, Archetype],
        states: Dict[str, ArchetypeState],
        modifiers: Dict[str, Modifier],
        polarities: Dict[str, Polarity],
        embedding_generator: Optional[EmbeddingGenerator] = None,
        d_ctx: int = 256,
    ) -> None:
        """
        Inicializa o motor Δ144.
        
        Args:
            archetypes: Mapa de arquétipos (12)
            states: Mapa de estados Δ144 (144)
            modifiers: Mapa de modifiers (59)
            polarities: Mapa de polarities (46) - v2.7
            embedding_generator: Gerador de embeddings (opcional)
            d_ctx: Dimensão do contexto (default 256)
        """
        self.archetypes = archetypes
        self.states = states
        self.modifiers = modifiers
        self.polarities = polarities  # v2.7: Polarities integration
        self.d_ctx = d_ctx
        
        # Configura embedding generator (default: legacy)
        if embedding_generator is None:
            config = EmbeddingConfig(
                provider=KALDRA_EMBEDDINGS_MODE.lower(), # "legacy" or "real" (mapped to openai/st in factory)
                model_name=KALDRA_EMBEDDINGS_MODEL,
                api_key=KALDRA_EMBEDDINGS_API_KEY,
                dim=d_ctx
            )
            # Map "real" to "openai" for now if configured, else "sentence-transformers" could be default
            # But for safety, let's stick to explicit providers in config.
            # If KALDRA_EMBEDDINGS_MODE is "REAL", we assume OpenAI for this sprint.
            if config.provider == "real":
                config.provider = "openai"
            
            self.embedding_generator = EmbeddingGenerator(config=config)
        else:
            self.embedding_generator = embedding_generator

        # índice rápido: arquétipo → lista de estados
        self._states_by_archetype: Dict[str, List[ArchetypeState]] = {}
        for s in self.states.values():
            self._states_by_archetype.setdefault(s.archetype_id, []).append(s)
            
        # Inicializa embeddings dos estados
        self._state_embeddings: Dict[str, np.ndarray] = {}
        self._init_state_embeddings()
        
        # v2.7: Inicializa embeddings dos modifiers para auto-inference
        self._modifier_embeddings: Dict[str, np.ndarray] = {}
        self._init_modifier_embeddings()

    def _init_state_embeddings(self):
        """
        Gera embeddings de referência para cada um dos 144 estados.
        Usa o EmbeddingGenerator configurado (Legacy ou Real).
        """
        for state in self.states.values():
            # Cria texto representativo do estado
            text = f"{state.label}: {state.description}"
            embedding = self.embedding_generator.encode(text)[0]
            self._state_embeddings[state.id] = embedding
    
    def _init_modifier_embeddings(self):
        """
        v2.7: Gera embeddings de referência para cada modifier.
        
        Usado para auto-inferência de modifier scores via cosine similarity.
        """
        for modifier in self.modifiers.values():
            # Cria texto representativo do modifier
            text = f"{modifier.label}: {modifier.description}"
            embedding = self.embedding_generator.encode(text)[0]
            self._modifier_embeddings[modifier.id] = embedding

    # ---------------------------------------------------------------------
    # Fábricas / loading
    # ---------------------------------------------------------------------

    @classmethod
    def from_default_files(cls, d_ctx: int = 256) -> "Delta144Engine":
        """
        Carrega a engine a partir dos arquivos padrão definidos em src/config.py.
        """
        archetypes = load_archetypes(ARCHETYPES_12_FILE)
        states = load_states(DELTA144_STATES_FILE)
        modifiers = load_modifiers(MODIFIERS_FILE)

        return cls(archetypes=archetypes, states=states, modifiers=modifiers, d_ctx=d_ctx)

    @classmethod
    def from_schema(cls, d_ctx: int = 256) -> "Delta144Engine":
        """
        Carrega motor a partir dos schemas padrão.
        
        v2.7: Agora carrega polarities além de archetypes, states, e modifiers.
        """
        archetypes = load_archetypes(ARCHETYPES_12_FILE)
        states = load_states(DELTA144_STATES_FILE)
        modifiers = load_modifiers(MODIFIERS_FILE)
        polarities = load_polarities(POLARITIES_FILE)  # v2.7

        return cls(
            archetypes=archetypes,
            states=states,
            modifiers=modifiers,
            polarities=polarities,  # v2.7
            d_ctx=d_ctx
        )

    # ---------------------------------------------------------------------
    # Getters básicos
    # ---------------------------------------------------------------------

    def get_archetype(self, archetype_id: str) -> Archetype:
        return self.archetypes[archetype_id]

    def get_state(self, state_id: str) -> ArchetypeState:
        return self.states[state_id]

    def list_states_for_archetype(self, archetype_id: str) -> List[ArchetypeState]:
        return sorted(
            self._states_by_archetype.get(archetype_id, []),
            key=lambda s: (s.row, s.col),
        )

    def compute_delta12(
        self,
        plane_scores: Optional[Dict[str, float]] = None,
        profile_scores: Optional[Dict[str, float]] = None,
        modifier_scores: Optional[Dict[str, float]] = None
    ) -> Delta12Vector:
        """
        Compute Delta12 vector (base archetypal probabilities) from input signals.
        
        This projects Kindra/TW369 signals onto the 12-dimensional archetype space.
        
        Args:
            plane_scores: TW369 plane scores (3, 6, 9)
            profile_scores: Profile scores (EXPANSIVE, CONTRACTIVE, TRANSCENDENT)
            modifier_scores: Modifier activation scores
            
        Returns:
            Delta12Vector with normalized archetype probabilities
        """
        # Initialize archetype scores
        archetype_scores = {arch_id: 0.0 for arch_id in self.archetypes.keys()}
        
        # Simple heuristic mapping (can be refined with learned weights)
        if plane_scores:
            # Plane 3 (Action) favors: WARRIOR, REBEL, CREATOR, SEEKER
            plane_3_weight = plane_scores.get("3", 0.0)
            archetype_scores["A03_WARRIOR"] += plane_3_weight * 0.3
            archetype_scores["A08_REBEL"] += plane_3_weight * 0.25
            archetype_scores["A12_CREATOR"] += plane_3_weight * 0.25
            archetype_scores["A05_SEEKER"] += plane_3_weight * 0.2
            
            # Plane 6 (Structure) favors: RULER, CAREGIVER, LOVER
            plane_6_weight = plane_scores.get("6", 0.0)
            archetype_scores["A07_RULER"] += plane_6_weight * 0.4
            archetype_scores["A04_CAREGIVER"] += plane_6_weight * 0.3
            archetype_scores["A06_LOVER"] += plane_6_weight * 0.3
            
            # Plane 9 (Metanoia) favors: SAGE, MAGICIAN, JESTER
            plane_9_weight = plane_scores.get("9", 0.0)
            archetype_scores["A10_SAGE"] += plane_9_weight * 0.4
            archetype_scores["A09_MAGICIAN"] += plane_9_weight * 0.35
            archetype_scores["A11_JESTER"] += plane_9_weight * 0.25
        
        if profile_scores:
            # EXPANSIVE favors: CREATOR, SEEKER, REBEL
            exp_weight = profile_scores.get("EXPANSIVE", 0.0)
            archetype_scores["A12_CREATOR"] += exp_weight * 0.2
            archetype_scores["A05_SEEKER"] += exp_weight * 0.15
            archetype_scores["A08_REBEL"] += exp_weight * 0.15
            
            # CONTRACTIVE favors: RULER, CAREGIVER, INNOCENT
            con_weight = profile_scores.get("CONTRACTIVE", 0.0)
            archetype_scores["A07_RULER"] += con_weight * 0.2
            archetype_scores["A04_CAREGIVER"] += con_weight * 0.15
            archetype_scores["A01_INNOCENT"] += con_weight * 0.1
            
            # TRANSCENDENT favors: SAGE, MAGICIAN
            trans_weight = profile_scores.get("TRANSCENDENT", 0.0)
            archetype_scores["A10_SAGE"] += trans_weight * 0.2
            archetype_scores["A09_MAGICIAN"] += trans_weight * 0.2
        
        # Ensure all archetypes have at least a small base probability
        for arch_id in archetype_scores:
            archetype_scores[arch_id] += 0.01
        
        # Create and normalize Delta12Vector
        delta12 = Delta12Vector(values=archetype_scores)
        delta12.normalize()
        
        return delta12

    # ---------------------------------------------------------------------
    # Inferência de estado Δ144
    # ---------------------------------------------------------------------

    def infer_from_vector(
        self,
        vector: np.ndarray,
        tau_modifiers: Optional[Dict[str, float]] = None
    ) -> StateInferenceResult:
        """
        Realiza inferência semântica comparando o vetor de entrada com os
        embeddings de referência dos 144 estados.
        """
        # Normaliza vetor de entrada
        norm = np.linalg.norm(vector)
        if norm > 0:
            query_vec = vector / norm
        else:
            query_vec = vector

        # Calcula similaridade (dot product) com todos os estados
        scores = []
        state_ids = []
        
        # Ordenar estados para consistência
        sorted_states = sorted(self.states.values(), key=lambda s: s.id)
        
        for s in sorted_states:
            ref_vec = self._state_embeddings.get(s.id)
            if ref_vec is None:
                sim = 0.0
            else:
                sim = float(np.dot(query_vec, ref_vec))
            scores.append(sim)
            state_ids.append(s.id)
            
        scores_np = np.array(scores)
        
        # Softmax com temperatura para gerar probabilidades
        # v2.8: Modulate temperature with Tau smoothing
        base_temp = 0.1
        if tau_modifiers:
            smoothing = tau_modifiers.get("archetype_smoothing", 1.0)
            # Lower smoothing (high risk) -> Higher temperature (flatter distribution)
            # If smoothing = 1.0 -> temp = 0.1
            # If smoothing = 0.5 -> temp = 0.2
            # If smoothing = 0.1 -> temp = 1.0
            temperature = base_temp / max(0.1, smoothing)
        else:
            temperature = base_temp
        exp_scores = np.exp(scores_np / temperature)
        probs = exp_scores / exp_scores.sum()
        
        # Escolhe o vencedor
        winner_idx = int(np.argmax(probs))
        winner_state_id = state_ids[winner_idx]
        winner_state = self.states[winner_state_id]
        winner_archetype = self.archetypes[winner_state.archetype_id]
        
        # Scores detalhados para debug/trace
        scores_dict = {
            "plane_scores": {"3": 0.33, "6": 0.33, "9": 0.33}, # Placeholder, poderia ser derivado
            "profile_scores": {"EXPANSIVE": 0.33, "CONTRACTIVE": 0.33, "TRANSCENDENT": 0.33},
            "chosen_state_score": float(probs[winner_idx]),
            "similarity": float(scores_np[winner_idx])
        }
        
        # v2.7: Auto-infer modifier scores from embedding
        modifier_scores = self.infer_modifier_scores_from_embedding(vector, top_k=10)
        active_modifiers = self._infer_modifiers(
            winner_state,
            modifier_scores,
            max_modifiers=4,
            threshold=0.35
        )
        
        return StateInferenceResult(
            archetype=winner_archetype,
            state=winner_state,
            active_modifiers=active_modifiers,  # v2.7: Now populated automatically
            scores=scores_dict,
            probs=probs.tolist()
        )

    def infer_state(
        self,
        archetype_id: str,
        plane_scores: Dict[str, float],
        profile_scores: Dict[str, float],
        modifier_scores: Optional[Dict[str, float]] = None,
        polarity_scores: Optional[Dict[str, float]] = None,  # v2.7
        tau_modifiers: Optional[Dict[str, float]] = None,    # v2.8
    ) -> StateInferenceResult:
        """
        Infere um estado Δ144 para um arquétipo específico.

        Parâmetros
        ----------
        archetype_id:
            ID do arquétipo (ex.: "A07_RULER").

        plane_scores:
            Peso relativo de cada plano TW369:
                {"3": ..., "6": ..., "9": ...}
            Ex.: saída normalizada do TW369 Engine.

        profile_scores:
            Peso relativo de cada perfil de estado:
                {"EXPANSIVE": x, "CONTRACTIVE": y, "TRANSCENDENT": z}
            Ex.: derivado de sinais de expansão, retração, metanoia.

        modifier_scores:
            Opcional. Dicionário:
                {"MOD_WOUNDED": 0.8, "MOD_DEFENSIVE": 0.6, ...}
            Estes valores podem vir do Bias Engine, Kindras, TW369, etc.
            
        polarity_scores:
            Opcional (v2.7). Dicionário:
                {"POL_LIGHT_SHADOW": 0.8, ...}
            Scores de polaridade extraídos de Meta-Engines.
        """

        if modifier_scores is None:
            modifier_scores = {}
            
        if polarity_scores is None:
            polarity_scores = {}

        archetype = self.get_archetype(archetype_id)
        candidate_states = self.list_states_for_archetype(archetype_id)

        # 1) Normaliza scores
        plane_scores_norm = self._normalize_scores(plane_scores, default_key="3")
        profile_scores_norm = self._normalize_scores(
            profile_scores, default_key="EXPANSIVE"
        )

        # 2) Escolhe o profile dominante (EXPANSIVE / CONTRACTIVE / TRANSCENDENT)
        dominant_profile = max(profile_scores_norm.items(), key=lambda kv: kv[1])[0]

        # 3) Filtra estados pelo profile dominante
        profile_filtered = [s for s in candidate_states if s.profile == dominant_profile]
        if not profile_filtered:
            # fallback: se algo estranho acontecer, usa todos
            profile_filtered = candidate_states

        # 4) Scora cada estado com base:
        #    - aderência ao TW-plane dominante
        #    - coerência combinada com os demais planos
        #    - posição (col) pode ser usada como leve ruído/ordem
        scored: List[Tuple[ArchetypeState, float]] = []
        for s in profile_filtered:
            score = self._score_state(s, plane_scores_norm, profile_scores_norm)
            scored.append((s, score))

        scored.sort(key=lambda t: t[1], reverse=True)
        best_state, best_score = scored[0]

        # 5) Inferir modifiers dinâmicos
        active_modifiers = self._infer_modifiers(best_state, modifier_scores)

        # 6) Montar resultado
        scores_snapshot = {
            "plane_scores": plane_scores_norm,
            "profile_scores": profile_scores_norm,
            "chosen_profile": dominant_profile,
            "state_scores": [
                {"state_id": s.id, "score": sc} for (s, sc) in scored
            ],
            "chosen_state_score": best_score,
            "raw_modifier_scores": modifier_scores,
        }

        return StateInferenceResult(
            archetype=archetype,
            state=best_state,
            active_modifiers=active_modifiers,
            scores=scores_snapshot,
            polarity_scores=polarity_scores,  # v2.7
        )

    # ---------------------------------------------------------------------
    # Internals: scoring
    # ---------------------------------------------------------------------

    @staticmethod
    def _normalize_scores(
        scores: Dict[str, float],
        default_key: Optional[str] = None,
    ) -> Dict[str, float]:
        if not scores:
            if default_key is None:
                return {}
            return {default_key: 1.0}

        total = sum(max(v, 0.0) for v in scores.values())
        if total <= 0:
            # tudo zero ou negativo → fallback
            if default_key is not None:
                return {default_key: 1.0}
            return {k: 0.0 for k in scores.keys()}

        return {k: max(v, 0.0) / total for k, v in scores.items()}

    def _score_state(
        self,
        state: ArchetypeState,
        plane_scores: Dict[str, float],
        profile_scores: Dict[str, float],
    ) -> float:
        """
        Heurística simples de score para um estado:

        - peso principal: aderência ao tw_plane_default do estado
        - reforço: saldo do profile dominante (já filtrado antes)
        - leve ruído ordenado pela coluna (para desempate estável)
        """
        # aderência ao plano default
        plane_weight = plane_scores.get(state.tw_plane_default, 0.0)

        # profile já foi usado para filtrar, mas podemos reforçar ligeiramente
        profile_weight = profile_scores.get(state.profile, 0.0)

        # pequeno bônus pela posição na matriz (coluna) para estabilidade
        col_bonus = 0.01 * (state.col / 12.0)

        return plane_weight * 0.7 + profile_weight * 0.25 + col_bonus

    # ---------------------------------------------------------------------
    # Internals: modifiers
    # ---------------------------------------------------------------------

    # Internals: modifiers

    def infer_modifier_scores_from_embedding(
        self,
        embedding: np.ndarray,
        top_k: int = 10
    ) -> Dict[str, float]:
        """
        v2.7: Infere modifier scores a partir de um embedding via cosine similarity.
        
        Args:
            embedding: Embedding do texto de entrada
            top_k: Número máximo de modifiers a retornar
            
        Returns:
            Dict mapeando modifier_id -> score (0-1)
        """
        if not self._modifier_embeddings:
            # Se não há embeddings de modifiers, retorna vazio
            return {}
        
        scores = {}
        
        for modifier_id, mod_embedding in self._modifier_embeddings.items():
            # Cosine similarity
            similarity = np.dot(embedding, mod_embedding) / (
                np.linalg.norm(embedding) * np.linalg.norm(mod_embedding) + 1e-10
            )
            
            # Normaliza para [0, 1]
            score = (similarity + 1.0) / 2.0
            scores[modifier_id] = float(score)
        
        # Retorna top_k modifiers com maiores scores
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_scores[:top_k])

    def _infer_modifiers(
        self,
        state: ArchetypeState,
        modifier_scores: Dict[str, float],
        max_modifiers: int = 4,
        threshold: float = 0.35,
    ) -> List[Modifier]:
        """
        Ativa modifiers dinâmicos para um estado específico.

        Regras:
        - Só considera modifiers presentes em `state.allowed_modifiers`
          ou `state.default_modifiers`.
        - Se `modifier_scores` estiver vazio, retorna apenas os defaults.
        - Caso contrário:
            - começa pelos defaults
            - adiciona modifiers com score acima do threshold, ordenados.
        """
        allowed_set = set(state.allowed_modifiers) | set(state.default_modifiers)
        if not allowed_set:
            # nenhum explicitamente definido → retorna vazio
            return []

        # Se não há scores externos, devolve apenas os defaults.
        if not modifier_scores:
            return [
                self.modifiers[mid]
                for mid in state.default_modifiers
                if mid in self.modifiers
            ]

        # Cria lista de (modifier_id, score)
        scored_mods: List[Tuple[str, float]] = []
        for mid in allowed_set:
            score = modifier_scores.get(mid, 0.0)
            scored_mods.append((mid, score))

        # Ordena por score desc
        scored_mods.sort(key=lambda t: t[1], reverse=True)

        active_ids: List[str] = []

        # 1) Garante que defaults entrem se tiverem score razoável ou se não houver nada melhor
        for mid in state.default_modifiers:
            if mid in self.modifiers:
                active_ids.append(mid)

        # 2) Adiciona outros modifiers acima de threshold até o limite
        for mid, sc in scored_mods:
            if mid in active_ids:
                continue
            if sc < threshold:
                continue
            active_ids.append(mid)
            if len(active_ids) >= max_modifiers:
                break

        # Remove duplicatas mantendo ordem
        dedup: List[str] = []
        for mid in active_ids:
            if mid not in dedup:
                dedup.append(mid)

        return [self.modifiers[mid] for mid in dedup if mid in self.modifiers]


# ---------------------------------------------------------------------------
# Pequeno helper para debug manual
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Uso rápido de linha de comando:

    python -m src.archetypes.delta144_engine

    (assumindo que este arquivo está em src/archetypes/
     e que os JSONs padrão existem em schema/archetypes/)
    """
    engine = Delta144Engine.from_default_files()

    # Exemplo: inferir estado para o Governante
    result = engine.infer_state(
        archetype_id="A07_RULER",
        plane_scores={"3": 0.2, "6": 0.6, "9": 0.2},
        profile_scores={"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2},
        modifier_scores={
            "MOD_DEFENSIVE": 0.8,
            "MOD_SHADOW": 0.4,
            "MOD_INSTITUTIONAL": 0.6,
        },
    )

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

