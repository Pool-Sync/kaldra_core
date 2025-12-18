"""
Stream Comparator for KALDRA v3.3 Phase 2.

Compares narrative evolution across different streams (e.g., NYT vs Twitter).
Measures divergence in archetypes, polarities, and overall narrative direction.
"""
from dataclasses import dataclass
from typing import List, Dict, Tuple
import math

from src.story.multi_stream_buffer import StreamWindow
from src.common.unified_signal import StoryEvent


@dataclass
class StreamComparisonResult:
    """
    Result of comparing two narrative streams.
    
    Attributes:
        stream_a: First stream ID
        stream_b: Second stream ID
        archetype_divergence: Divergence in archetypal patterns [0,1]
        polarity_divergence: Divergence in polarity patterns [0,1]
        stage_divergence: Divergence in story stages [0,1] (FUTURE)
        overall_divergence: Weighted overall divergence [0,1]
        notes: Additional context or warnings
    """
    stream_a: str
    stream_b: str
    archetype_divergence: float
    polarity_divergence: float
    stage_divergence: float  # Reserved for future StoryArc integration
    overall_divergence: float
    notes: Dict[str, str]


class StreamComparator:
    """
    Compares narrative evolution across multiple streams.
    
    Calculates divergence metrics for:
    - Archetypal patterns (delta12, delta144)
    - Polarity scores
    - Story stages (FUTURE: when StoryArc is integrated)
    
    Example:
        >>> comparator = StreamComparator()
        >>> windows = buffer.get_all_windows(size=50)
        >>> results = comparator.compare_windows(windows)
        >>> for result in results:
        ...     print(f"{result.stream_a} vs {result.stream_b}: {result.overall_divergence:.2f}")
    """
    
    def compare_windows(self, windows: List[StreamWindow]) -> List[StreamComparisonResult]:
        """
        Compare all pairs of stream windows.
        
        Args:
            windows: List of StreamWindow objects to compare
        
        Returns:
            List of StreamComparisonResult for each pair
        """
        results = []
        
        # Compare all pairs
        for i in range(len(windows)):
            for j in range(i + 1, len(windows)):
                result = self._compare_pair(windows[i], windows[j])
                results.append(result)
        
        return results
    
    def _compare_pair(
        self,
        window_a: StreamWindow,
        window_b: StreamWindow
    ) -> StreamComparisonResult:
        """
        Compare two stream windows.
        
        Args:
            window_a: First stream window
            window_b: Second stream window
        
        Returns:
            StreamComparisonResult with divergence metrics
        """
        notes = {}
        
        # Handle empty windows
        if not window_a.events and not window_b.events:
            notes["warning"] = "Both streams are empty"
            return StreamComparisonResult(
                stream_a=window_a.stream_id,
                stream_b=window_b.stream_id,
                archetype_divergence=0.0,
                polarity_divergence=0.0,
                stage_divergence=0.0,
                overall_divergence=0.0,
                notes=notes
            )
        
        if not window_a.events:
            notes["warning"] = f"Stream {window_a.stream_id} is empty"
            return StreamComparisonResult(
                stream_a=window_a.stream_id,
                stream_b=window_b.stream_id,
                archetype_divergence=1.0,
                polarity_divergence=1.0,
                stage_divergence=1.0,
                overall_divergence=1.0,
                notes=notes
            )
        
        if not window_b.events:
            notes["warning"] = f"Stream {window_b.stream_id} is empty"
            return StreamComparisonResult(
                stream_a=window_a.stream_id,
                stream_b=window_b.stream_id,
                archetype_divergence=1.0,
                polarity_divergence=1.0,
                stage_divergence=1.0,
                overall_divergence=1.0,
                notes=notes
            )
        
        # Aggregate profiles
        arch_a = self._aggregate_archetype_profile(window_a.events)
        arch_b = self._aggregate_archetype_profile(window_b.events)
        
        pol_a = self._aggregate_polarity_profile(window_a.events)
        pol_b = self._aggregate_polarity_profile(window_b.events)
        
        # Calculate divergences
        arch_div = self._cosine_divergence(arch_a, arch_b)
        pol_div = self._cosine_divergence(pol_a, pol_b)
        
        # Stage divergence is reserved for future StoryArc integration
        stage_div = 0.0
        notes["stage_divergence"] = "Not yet implemented (requires StoryArc)"
        
        # Overall divergence (weighted average)
        # Currently: 50% archetype + 50% polarity
        # FUTURE: Add stage divergence weight
        overall_div = 0.5 * arch_div + 0.5 * pol_div
        
        return StreamComparisonResult(
            stream_a=window_a.stream_id,
            stream_b=window_b.stream_id,
            archetype_divergence=arch_div,
            polarity_divergence=pol_div,
            stage_divergence=stage_div,
            overall_divergence=overall_div,
            notes=notes
        )
    
    def _aggregate_archetype_profile(
        self,
        events: List[StoryEvent]
    ) -> Dict[str, float]:
        """
        Aggregate archetypal profile from events.
        
        Averages delta12 scores and delta144_state frequencies.
        
        Args:
            events: List of StoryEvents
        
        Returns:
            Dictionary of archetype -> average score
        """
        profile = {}
        count = 0
        
        for event in events:
            # Aggregate delta12 scores
            if event.delta12:
                for archetype, score in event.delta12.items():
                    profile[archetype] = profile.get(archetype, 0.0) + score
                count += 1
            
            # Aggregate delta144_state as a categorical feature
            if event.delta144_state:
                key = f"delta144:{event.delta144_state}"
                profile[key] = profile.get(key, 0.0) + 1.0
        
        # Average
        if count > 0:
            for key in profile:
                profile[key] /= count
        
        return profile
    
    def _aggregate_polarity_profile(
        self,
        events: List[StoryEvent]
    ) -> Dict[str, float]:
        """
        Aggregate polarity profile from events.
        
        Averages polarity scores across all events.
        
        Args:
            events: List of StoryEvents
        
        Returns:
            Dictionary of polarity -> average score
        """
        profile = {}
        count = 0
        
        for event in events:
            if event.polarity_scores:
                for polarity, score in event.polarity_scores.items():
                    profile[polarity] = profile.get(polarity, 0.0) + score
                count += 1
        
        # Average
        if count > 0:
            for key in profile:
                profile[key] /= count
        
        return profile
    
    def _cosine_divergence(
        self,
        vec_a: Dict[str, float],
        vec_b: Dict[str, float]
    ) -> float:
        """
        Calculate cosine divergence between two vectors.
        
        Divergence = 1 - cosine_similarity
        Range: [0, 1] where 0 = identical, 1 = completely different
        
        Args:
            vec_a: First vector (key -> value)
            vec_b: Second vector (key -> value)
        
        Returns:
            Divergence score [0, 1]
        """
        # Handle empty vectors
        if not vec_a and not vec_b:
            return 0.0
        if not vec_a or not vec_b:
            return 1.0
        
        # Get all keys
        all_keys = set(vec_a.keys()) | set(vec_b.keys())
        
        # Build aligned vectors
        a = [vec_a.get(k, 0.0) for k in all_keys]
        b = [vec_b.get(k, 0.0) for k in all_keys]
        
        # Compute dot product
        dot = sum(ai * bi for ai, bi in zip(a, b))
        
        # Compute magnitudes
        mag_a = math.sqrt(sum(ai * ai for ai in a))
        mag_b = math.sqrt(sum(bi * bi for bi in b))
        
        # Handle zero magnitude
        if mag_a == 0.0 or mag_b == 0.0:
            return 1.0
        
        # Cosine similarity
        similarity = dot / (mag_a * mag_b)
        
        # Clamp to [0, 1] and return divergence
        similarity = max(0.0, min(1.0, similarity))
        divergence = 1.0 - similarity
        
        return divergence
