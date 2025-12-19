"""
Polarity Mapping Module (v2.7)
==============================

Responsável por mapear saídas dos Meta-Engines (Nietzsche, Aurelius, Campbell)
para scores de Polaridade (46 tensões dimensionais).

Mappings:
- Nietzsche (12 eixos) → Polarities de Will, Power, Chaos
- Aurelius (12 eixos) → Polarities de Affect, Control, Duty
- Campbell (12 estágios) → Polarities de Journey, Transformation
"""

from typing import Dict, Any, List, Optional

# Mapeamento de eixos Nietzsche para Polarities
# Eixo (0-1) -> Polarity ID (e direção: +1 ou -1)
# Mapeamento de eixos Nietzsche para Polarities
# Eixo (0-1) -> Polarity ID (e direção: +1 ou -1)
NIETZSCHE_MAPPING = {
    "will_to_power": ("POL_DOMINANCE_SERVICE", 1.0),      # High Will -> Dominance
    "amor_fati": ("POL_RESENTMENT_AFFIRMATION", 1.0),     # High Amor Fati -> Affirmation
    "dionysian_force": ("POL_ORDER_CHAOS", -1.0),         # High Dionysian -> Chaos (low Order)
    "apollonian_order": ("POL_ORDER_CHAOS", 1.0),         # High Apollonian -> Order
    "free_spirit": ("POL_AUTONOMY_DEPENDENCE", 1.0),      # Free Spirit -> Autonomy
    "eternal_return_acceptance": ("POL_METANOIA_STAGNATION", 1.0), # Affirmation of return -> Metanoia
    "active_nihilism": ("POL_CREATION_DESTRUCTION", -1.0), # Active Nihilism -> Destruction
    "passive_nihilism": ("POL_MEANING_VOID", -1.0),       # Passive Nihilism -> Void
    "transvaluation": ("POL_CREATION_DESTRUCTION", 1.0),  # Transvaluation -> Creation
    "resentment": ("POL_RESENTMENT_AFFIRMATION", -1.0),   # High Resentment -> Resentment
}

# Mapeamento de eixos Aurelius para Polarities
AURELIUS_MAPPING = {
    "serenity": ("POL_CALM_ANXIETY", 1.0),                # High Serenity -> Calm
    "emotional_regulation": ("POL_OPENNESS_REPRESSION", -1.0), # High Reg -> Repression/Control? Or Calm? Let's map to CONTROL_SURRENDER
    "control_dichotomy": ("POL_CONTROL_SURRENDER", 1.0),  # Focus on what you control -> Control
    "logos_alignment": ("POL_RATIONAL_MYTHIC", 1.0),      # High Logos -> Rational
    "memento_mori": ("POL_METANOIA_STAGNATION", 1.0),     # Awareness of death -> Urgency/Metanoia
    "civic_duty": ("POL_DUTY_EVASION", 1.0),              # High Duty -> Duty
    "inner_citadel": ("POL_AUTONOMY_DEPENDENCE", 1.0),    # Inner strength -> Autonomy
    "present_moment": ("POL_ANALYSIS_INTUITION", -1.0),   # Presence -> Intuition/Direct experience? Or maybe just CALM
}

# Mapeamento de estágios Campbell para Polarities
# Estágio -> {Polarity ID: Score}
CAMPBELL_MAPPING = {
    "call_to_adventure": {"POL_CALL_REFUSAL": 0.8, "POL_STABILITY_VOLATILITY": 0.7},
    "refusal_of_call": {"POL_CALL_REFUSAL": 0.2, "POL_COURAGE_FEAR": 0.2},
    "supernatural_aid": {"POL_AUTONOMY_DEPENDENCE": 0.3, "POL_RATIONAL_MYTHIC": 0.2},
    "crossing_threshold": {"POL_STABILITY_VOLATILITY": 0.8, "POL_TEST_RETREAT": 0.7},
    "belly_of_whale": {"POL_DESCENT_ASCENT": 0.1, "POL_METANOIA_STAGNATION": 0.8}, # Descent
    "road_of_trials": {"POL_TEST_RETREAT": 0.8, "POL_COURAGE_FEAR": 0.7},
    "meeting_goddess": {"POL_INDIVIDUAL_COLLECTIVE": 0.7, "POL_CREATION_DESTRUCTION": 0.8},
    "woman_as_temptress": {"POL_DUTY_EVASION": 0.3, "POL_CONTROL_SURRENDER": 0.4},
    "atonement_father": {"POL_HIERARCHY_NETWORK": 0.8, "POL_RESPONSIBILITY_GUILT": 0.8},
    "apotheosis": {"POL_DESCENT_ASCENT": 0.9, "POL_LIGHT_SHADOW": 0.9}, # Ascent
    "ultimate_boon": {"POL_MEANING_VOID": 0.9, "POL_CREATION_DESTRUCTION": 0.9},
    "refusal_return": {"POL_DUTY_EVASION": 0.2, "POL_INDIVIDUAL_COLLECTIVE": 0.2},
    "magic_flight": {"POL_STABILITY_VOLATILITY": 0.9, "POL_COURAGE_FEAR": 0.8},
    "rescue_without": {"POL_AUTONOMY_DEPENDENCE": 0.2, "POL_INDIVIDUAL_COLLECTIVE": 0.8},
    "crossing_return": {"POL_STABILITY_VOLATILITY": 0.6, "POL_TEST_RETREAT": 0.6},
    "master_two_worlds": {"POL_RATIONAL_MYTHIC": 0.5, "POL_LIGHT_SHADOW": 0.5}, # Balance
    "freedom_to_live": {"POL_HOPE_DESPAIR": 0.9, "POL_CONTROL_SURRENDER": 0.5},
}


def extract_polarity_scores(meta_results: Dict[str, Any]) -> Dict[str, float]:
    """
    Extrai scores de polaridade a partir dos resultados dos Meta-Engines.
    
    Args:
        meta_results: Dict contendo saídas de 'nietzsche', 'aurelius', 'campbell'
        
    Returns:
        Dict mapeando polarity_id -> score (0.0 a 1.0)
    """
    polarity_scores: Dict[str, List[float]] = {}
    
    # 1. Processa Nietzsche
    if "nietzsche" in meta_results:
        nietzsche_data = meta_results["nietzsche"]
        # Assume que nietzsche_data tem um campo 'scores' ou é o próprio dict de scores
        # Ajustar conforme estrutura real do MetaSignal
        scores = nietzsche_data.get("scores", {}) if isinstance(nietzsche_data, dict) else {}
        
        for axis, (pol_id, direction) in NIETZSCHE_MAPPING.items():
            if axis in scores:
                val = scores[axis]
                # Normaliza: se direction=1, val=val. Se direction=-1, val=1-val
                normalized = val if direction > 0 else (1.0 - val)
                polarity_scores.setdefault(pol_id, []).append(normalized)

    # 2. Processa Aurelius
    if "aurelius" in meta_results:
        aurelius_data = meta_results["aurelius"]
        scores = aurelius_data.get("scores", {}) if isinstance(aurelius_data, dict) else {}
        
        for axis, (pol_id, direction) in AURELIUS_MAPPING.items():
            if axis in scores:
                val = scores[axis]
                normalized = val if direction > 0 else (1.0 - val)
                polarity_scores.setdefault(pol_id, []).append(normalized)

    # 3. Processa Campbell
    if "campbell" in meta_results:
        campbell_data = meta_results["campbell"]
        # Assume que campbell_data tem 'stage'
        stage = campbell_data.get("stage") if isinstance(campbell_data, dict) else None
        
        if stage and stage in CAMPBELL_MAPPING:
            mapping = CAMPBELL_MAPPING[stage]
            for pol_id, val in mapping.items():
                polarity_scores.setdefault(pol_id, []).append(val)

    # 4. Agrega scores (média)
    final_scores: Dict[str, float] = {}
    for pol_id, values in polarity_scores.items():
        if values:
            final_scores[pol_id] = sum(values) / len(values)
            
    return final_scores
