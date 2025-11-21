"""
KALDRA — Delta144 Engine
========================

Motor de inferência da matriz arquetípica Δ144.

Responsabilidades principais:
- Carregar os 12 arquétipos (archetypes_12.core.json)
- Carregar os 144 estados (delta144_states.core.json)
- Carregar os Modifiers (archetype_modifiers.core.json)
- Oferecer uma API simples para inferir:
    - estado arquetípico dominante de um arquétipo
    - modifiers dinâmicos ativos
    - snapshot dos sinais usados

Este módulo **não** sabe nada de embeddings ou NLP diretamente.
Ele espera receber já os sinais numéricos agregados (ex.: saídos de TW369, Kindras, etc.)
e traduz isso para um estado Δ144 + modifiers.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import json
import math


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
    id: str
    label: str
    category: str
    description: str


@dataclass
class StateInferenceResult:
    """
    Resultado final da inferência de estado Δ144.
    """
    archetype: Archetype
    state: ArchetypeState
    active_modifiers: List[Modifier]
    scores: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "archetype": asdict(self.archetype),
            "state": asdict(self.state),
            "active_modifiers": [asdict(m) for m in self.active_modifiers],
            "scores": self.scores,
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
    data = _load_json(path)
    result: Dict[str, Modifier] = {}
    for raw in data:
        m = Modifier(
            id=raw["id"],
            label=raw["label"],
            category=raw.get("category", ""),
            description=raw.get("description", ""),
        )
        result[m.id] = m
    return result


# ---------------------------------------------------------------------------
# Núcleo do motor Δ144
# ---------------------------------------------------------------------------


class Delta144Engine:
    """
    Motor arquetípico da Δ144.

    Não faz parsing de texto nem cálculo de TW369 diretamente.
    Recebe **sinais já agregados** e devolve um estado Δ144 coerente.

    Exemplo de uso:

        base_dir = Path("kaldra/core/archetypes")
        engine = Delta144Engine.from_default_files(base_dir)

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
    ) -> None:
        self.archetypes = archetypes
        self.states = states
        self.modifiers = modifiers

        # índice rápido: arquétipo → lista de estados
        self._states_by_archetype: Dict[str, List[ArchetypeState]] = {}
        for s in self.states.values():
            self._states_by_archetype.setdefault(s.archetype_id, []).append(s)

    # ---------------------------------------------------------------------
    # Fábricas / loading
    # ---------------------------------------------------------------------

    @classmethod
    def from_default_files(cls, base_dir: Path) -> "Delta144Engine":
        """
        Carrega a engine a partir dos arquivos padrão:

        - archetypes_12.core.json
        - delta144_states.core.json
        - archetype_modifiers.core.json

        Espera-se que estes arquivos estejam em `base_dir`.
        """
        archetypes_path = base_dir / "archetypes_12.core.json"
        states_path = base_dir / "delta144_states.core.json"
        modifiers_path = base_dir / "archetype_modifiers.core.json"

        archetypes = load_archetypes(archetypes_path)
        states = load_states(states_path)
        modifiers = load_modifiers(modifiers_path)

        return cls(archetypes=archetypes, states=states, modifiers=modifiers)

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

    # ---------------------------------------------------------------------
    # Inferência de estado Δ144
    # ---------------------------------------------------------------------

    def infer_state(
        self,
        archetype_id: str,
        plane_scores: Dict[str, float],
        profile_scores: Dict[str, float],
        modifier_scores: Optional[Dict[str, float]] = None,
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
        """

        if modifier_scores is None:
            modifier_scores = {}

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

    python -m kaldra.core.archetypes.delta144_engine

    (assumindo que este arquivo está em kaldra/core/archetypes/
     e que os JSONs padrão existem no mesmo diretório.)
    """
    base = Path(__file__).resolve().parent
    engine = Delta144Engine.from_default_files(base)

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
