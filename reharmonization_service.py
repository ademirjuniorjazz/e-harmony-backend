
from typing import List, Dict, Optional, Any
from ..core.music_theory_engine import MusicTheoryEngine, Chord
from ..knowledge_base.ian_guest_kb import IanGuestKnowledgeBase

class ReharmonizationService:
    def __init__(self):
        self.theory_engine = MusicTheoryEngine()
        self.knowledge_base = IanGuestKnowledgeBase()

    def suggest_reharmonizations(self, chord_symbols: List[str], key: str = "C", 
                               style: str = "jazz") -> Dict[str, Any]:
        """Sugere rearmonizações baseadas no estilo e metodologia Ian Guest"""

        original_analysis = self.theory_engine.analyze_chord_progression(chord_symbols, key)
        suggestions = []

        for i, chord_data in enumerate(original_analysis):
            chord_suggestions = self._get_chord_substitutions(
                chord_data["chord"], key, style, i, len(chord_symbols)
            )

            if chord_suggestions:
                suggestions.append({
                    "position": i,
                    "original_chord": chord_symbols[i],
                    "substitutions": chord_suggestions,
                    "guest_theory": self._get_guest_theory_explanation(chord_data, style)
                })

        return {
            "original_progression": chord_symbols,
            "key": key,
            "style": style,
            "reharmonization_suggestions": suggestions,
            "complete_alternatives": self._generate_complete_alternatives(chord_symbols, key, style)
        }

    def _get_chord_substitutions(self, chord: Chord, key: str, style: str, 
                               position: int, total_chords: int) -> List[Dict]:
        """Obtém substituições específicas para um acorde"""
        substitutions = []

        # Substitutos tritonais (Volume 2 Ian Guest)
        if chord.quality.value == "dominant7":
            tritone_sub = self._get_tritone_substitution(chord)
            substitutions.append({
                "chord": tritone_sub,
                "type": "tritone_substitution",
                "explanation": "Substituto tritonal - mantém tensão dominante com movimento cromático",
                "volume_reference": "Ian Guest Vol. 2 p.46-60"
            })

        # Empréstimo modal
        modal_substitutes = self._get_modal_borrowing_options(chord, key)
        substitutions.extend(modal_substitutes)

        # Dominantes secundários
        if position < total_chords - 1:  # Não é o último acorde
            secondary_dom = self._get_secondary_dominant_options(chord, key)
            substitutions.extend(secondary_dom)

        return substitutions

    def _get_tritone_substitution(self, chord: Chord) -> str:
        """Calcula substituto tritonal"""
        root_index = self.theory_engine.chromatic_notes.index(chord.root)
        tritone_index = (root_index + 6) % 12
        tritone_root = self.theory_engine.chromatic_notes[tritone_index]
        return f"{tritone_root}7"

    def _get_modal_borrowing_options(self, chord: Chord, key: str) -> List[Dict]:
        """Opções de empréstimo modal"""
        options = []

        if chord.quality.value == "major":
            # Empréstimo do menor
            minor_version = f"{chord.root}m"
            options.append({
                "chord": minor_version,
                "type": "modal_borrowing", 
                "explanation": f"Empréstimo do modo menor de {key}",
                "volume_reference": "Ian Guest Vol. 2 p.10-25"
            })

        return options

    def _get_secondary_dominant_options(self, chord: Chord, key: str) -> List[Dict]:
        """Opções de dominantes secundários"""
        options = []

        # V/V, V/vi, V/ii etc.
        if chord.quality.value in ["major", "minor"]:
            dom_root_index = (self.theory_engine.chromatic_notes.index(chord.root) + 7) % 12
            dom_root = self.theory_engine.chromatic_notes[dom_root_index]
            secondary_dom = f"{dom_root}7"

            options.append({
                "chord": secondary_dom,
                "type": "secondary_dominant",
                "explanation": f"Dominante secundário que resolve em {chord.root}",
                "volume_reference": "Ian Guest Vol. 2 p.26-45"
            })

        return options

    def _generate_complete_alternatives(self, chord_symbols: List[str], 
                                      key: str, style: str) -> List[Dict]:
        """Gera progressões alternativas completas"""
        alternatives = []

        # Versão com substitutos tritonais
        tritone_version = []
        for chord in chord_symbols:
            parsed = self.theory_engine.parse_chord(chord)
            if parsed.quality.value == "dominant7":
                tritone_version.append(self._get_tritone_substitution(parsed))
            else:
                tritone_version.append(chord)

        if tritone_version != chord_symbols:
            alternatives.append({
                "name": "Versão com Substitutos Tritonais",
                "progression": tritone_version,
                "style": "jazz_sophisticated",
                "difficulty": "intermediário"
            })

        # Versão com dominantes secundários
        secondary_version = self._add_secondary_dominants(chord_symbols, key)
        if secondary_version != chord_symbols:
            alternatives.append({
                "name": "Versão com Dominantes Secundários", 
                "progression": secondary_version,
                "style": "jazz_traditional",
                "difficulty": "intermediário"
            })

        return alternatives

    def _add_secondary_dominants(self, chord_symbols: List[str], key: str) -> List[str]:
        """Adiciona dominantes secundários onde apropriado"""
        result = []

        for i, chord in enumerate(chord_symbols):
            if i < len(chord_symbols) - 1:  # Não é o último
                next_chord = self.theory_engine.parse_chord(chord_symbols[i + 1])

                # Inserir V/next_chord antes do próximo acorde
                if next_chord.quality.value in ["major", "minor"]:
                    dom_root_index = (self.theory_engine.chromatic_notes.index(next_chord.root) + 7) % 12
                    dom_root = self.theory_engine.chromatic_notes[dom_root_index]
                    result.extend([chord, f"{dom_root}7"])
                else:
                    result.append(chord)
            else:
                result.append(chord)

        return result

    def _get_guest_theory_explanation(self, chord_data: Dict, style: str) -> Dict:
        """Explicação teórica baseada no método Ian Guest"""
        return {
            "function_analysis": f"Função: {chord_data['function']}",
            "guest_approach": self._get_guest_approach_for_function(chord_data['function']),
            "practice_tips": [
                "Pratique a progressão original primeiro",
                "Adicione substituições uma por vez",
                "Ouça o efeito de cada substituição"
            ]
        }

    def _get_guest_approach_for_function(self, function: str) -> str:
        """Abordagem pedagógica do Ian Guest por função"""
        approaches = {
            "T": "Função tônica - centro de repouso. Substitutos devem manter estabilidade.",
            "D": "Função dominante - tensão que pede resolução. Substitutos devem manter direcionamento.", 
            "S": "Função subdominante - preparação. Boa para experimentar coloridos."
        }
        return approaches.get(function, "Analise a função harmônica antes de substituir")
