
from typing import List, Dict, Optional, Any
from ..core.music_theory_engine import MusicTheoryEngine, Chord
from ..knowledge_base.ian_guest_kb import IanGuestKnowledgeBase

class ImprovisationConsultantService:
    def __init__(self):
        self.theory_engine = MusicTheoryEngine()
        self.knowledge_base = IanGuestKnowledgeBase()

    def get_improvisation_guide(self, chord_symbols: List[str], key: str = "C") -> Dict[str, Any]:
        """Guia completo para improvisação sobre progressão"""

        analysis = self.theory_engine.analyze_chord_progression(chord_symbols, key)

        return {
            "progression": chord_symbols,
            "key": key,
            "chord_scale_mapping": self._map_chord_to_scales(analysis),
            "target_notes": self._identify_target_notes(analysis),
            "approach_strategies": self._suggest_approach_strategies(analysis),
            "practice_exercises": self._generate_practice_exercises(analysis),
            "guest_methodology": self._apply_guest_methodology(analysis)
        }

    def _map_chord_to_scales(self, analysis: List[Dict]) -> List[Dict]:
        """Mapeia cada acorde às escalas recomendadas"""
        mapping = []

        for chord_data in analysis:
            chord = chord_data["chord"]
            scales = chord_data["scales_recommended"]

            chord_mapping = {
                "chord": chord_data["chord_symbol"],
                "primary_scale": scales[0] if scales else "chromatic",
                "alternative_scales": scales[1:] if len(scales) > 1 else [],
                "scale_notes": self._get_scale_notes(chord.root, scales[0] if scales else "chromatic"),
                "avoid_notes": self._get_avoid_notes(chord),
                "strong_notes": self._get_strong_notes(chord)
            }

            mapping.append(chord_mapping)

        return mapping

    def _get_scale_notes(self, root: str, mode: str) -> List[str]:
        """Retorna notas da escala"""
        root_index = self.theory_engine.chromatic_notes.index(root)
        mode_intervals = self.theory_engine.modes.get(mode, [0, 2, 4, 5, 7, 9, 11])

        notes = []
        for interval in mode_intervals:
            note_index = (root_index + interval) % 12
            notes.append(self.theory_engine.chromatic_notes[note_index])

        return notes

    def _get_avoid_notes(self, chord: Chord) -> List[str]:
        """Notas a evitar na improvisação"""
        avoid_notes = []

        # Regras básicas de avoid notes
        if chord.quality.value == "major7":
            # Evitar 4ª justa em acordes maiores
            root_index = self.theory_engine.chromatic_notes.index(chord.root)
            avoid_index = (root_index + 5) % 12
            avoid_notes.append(self.theory_engine.chromatic_notes[avoid_index])

        return avoid_notes

    def _get_strong_notes(self, chord: Chord) -> List[str]:
        """Notas fortes para improvisação"""
        strong_notes = [chord.root]  # Fundamental sempre forte

        # Terça e sétima são características
        root_index = self.theory_engine.chromatic_notes.index(chord.root)

        if chord.quality.value in ["major", "major7"]:
            third_index = (root_index + 4) % 12
            strong_notes.append(self.theory_engine.chromatic_notes[third_index])
        elif chord.quality.value in ["minor", "minor7"]:
            third_index = (root_index + 3) % 12
            strong_notes.append(self.theory_engine.chromatic_notes[third_index])

        if "7" in chord.quality.value:
            if chord.quality.value == "major7":
                seventh_index = (root_index + 11) % 12
            else:
                seventh_index = (root_index + 10) % 12
            strong_notes.append(self.theory_engine.chromatic_notes[seventh_index])

        return strong_notes

    def _identify_target_notes(self, analysis: List[Dict]) -> List[Dict]:
        """Identifica target notes para cada acorde"""
        targets = []

        for i, chord_data in enumerate(analysis):
            chord = chord_data["chord"]
            strong_notes = self._get_strong_notes(chord)

            # Target notes são geralmente 3ª e 7ª
            target_info = {
                "chord": chord_data["chord_symbol"],
                "primary_targets": strong_notes[1:],  # Exclui fundamental
                "approach_notes": self._get_approach_notes(strong_notes),
                "resolution_notes": self._get_resolution_notes(analysis, i)
            }

            targets.append(target_info)

        return targets

    def _get_approach_notes(self, target_notes: List[str]) -> List[Dict]:
        """Notas de aproximação para os targets"""
        approaches = []

        for target in target_notes:
            target_index = self.theory_engine.chromatic_notes.index(target)

            # Aproximação cromática
            approaches.append({
                "target": target,
                "chromatic_below": self.theory_engine.chromatic_notes[(target_index - 1) % 12],
                "chromatic_above": self.theory_engine.chromatic_notes[(target_index + 1) % 12],
                "diatonic_approaches": self._get_diatonic_approaches(target)
            })

        return approaches

    def _get_diatonic_approaches(self, target_note: str) -> List[str]:
        """Aproximações diatônicas"""
        # Simplificado - retorna aproximações por graus da escala
        target_index = self.theory_engine.chromatic_notes.index(target_note)

        return [
            self.theory_engine.chromatic_notes[(target_index - 2) % 12],  # Segunda abaixo
            self.theory_engine.chromatic_notes[(target_index + 2) % 12]   # Segunda acima
        ]

    def _get_resolution_notes(self, analysis: List[Dict], current_index: int) -> List[str]:
        """Notas de resolução para o próximo acorde"""
        if current_index < len(analysis) - 1:
            next_chord = analysis[current_index + 1]["chord"]
            return self._get_strong_notes(next_chord)
        return []

    def _suggest_approach_strategies(self, analysis: List[Dict]) -> List[Dict]:
        """Estratégias de aproximação melódica"""
        strategies = []

        # Análise do contexto harmônico
        has_ii_v_i = self._detect_ii_v_i(analysis)
        is_modal = self._detect_modal_context(analysis)

        if has_ii_v_i:
            strategies.append({
                "name": "ii-V-I Licks",
                "description": "Use frases características sobre ii-V-I",
                "techniques": [
                    "Conectar as 3ªs dos acordes",
                    "Usar escala bebop sobre V7",
                    "Resolver na 3ª ou 5ª do I"
                ]
            })

        if is_modal:
            strategies.append({
                "name": "Abordagem Modal",
                "description": "Explore as características modais",
                "techniques": [
                    "Enfatize notas características do modo",
                    "Use pedais harmônicos",
                    "Evite resolução tonal forte"
                ]
            })

        # Estratégias gerais
        strategies.append({
            "name": "Chord Tones",
            "description": "Construa frases usando notas dos acordes",
            "techniques": [
                "Comece e termine em chord tones",
                "Use passing tones entre chord tones",
                "Varie o ritmo harmônico"
            ]
        })

        return strategies

    def _detect_ii_v_i(self, analysis: List[Dict]) -> bool:
        """Detecta progressões ii-V-I"""
        if len(analysis) < 3:
            return False

        for i in range(len(analysis) - 2):
            functions = [
                analysis[i]["function"],
                analysis[i+1]["function"], 
                analysis[i+2]["function"]
            ]

            if functions == ["S", "D", "T"]:
                return True

        return False

    def _detect_modal_context(self, analysis: List[Dict]) -> bool:
        """Detecta contexto modal"""
        # Simplificado - detecta acordes não-funcionais
        non_functional = sum(1 for chord in analysis if chord["function"] == "sub")
        return non_functional > len(analysis) * 0.3

    def _generate_practice_exercises(self, analysis: List[Dict]) -> List[Dict]:
        """Gera exercícios de prática"""
        exercises = []

        # Exercício 1: Chord Tones
        exercises.append({
            "name": "Arpejos dos Acordes",
            "description": "Toque os arpejos de cada acorde da progressão",
            "steps": [
                "Toque fundamental-3ª-5ª-7ª de cada acorde",
                "Pratique em diferentes oitavas",
                "Varie as articulações"
            ],
            "guest_reference": "Volume 1 - Inversões e Arpejos"
        })

        # Exercício 2: Target Notes
        exercises.append({
            "name": "Conexão de Target Notes",
            "description": "Conecte 3ªs e 7ªs entre acordes",
            "steps": [
                "Identifique 3ª e 7ª de cada acorde",
                "Crie linhas melódicas conectando essas notas",
                "Use aproximações cromáticas"
            ],
            "guest_reference": "Volume 2 - Condução Melódica"
        })

        # Exercício 3: Escalas
        exercises.append({
            "name": "Prática de Escalas",
            "description": "Pratique as escalas recomendadas",
            "steps": [
                "Toque cada escala sobre seu respectivo acorde",
                "Crie padrões melódicos",
                "Improvise usando apenas notas da escala"
            ],
            "guest_reference": "Volume 3 - Modalismo e Escalas"
        })

        return exercises

    def _apply_guest_methodology(self, analysis: List[Dict]) -> Dict:
        """Aplica metodologia específica do Ian Guest"""
        return {
            "pedagogical_approach": [
                "Comece com chord tones (notas dos acordes)",
                "Adicione passing tones gradualmente", 
                "Desenvolva vocabulário através de transcrições",
                "Pratique em todas as tonalidades"
            ],
            "guest_principles": [
                "Harmonia como base da improvisação",
                "Importância da escuta ativa",
                "Desenvolvimento gradual de complexidade",
                "Aplicação prática em repertório"
            ],
            "volume_references": {
                "chord_tones": "Volume 1 - Acordes e Inversões",
                "scales": "Volume 3 - Modalismo",
                "substitutions": "Volume 2 - Acordes de Empréstimo"
            }
        }
