
from typing import List, Dict, Optional, Any
from ..core.music_theory_engine import MusicTheoryEngine, Chord, Function
from ..knowledge_base.ian_guest_kb import IanGuestKnowledgeBase

class HarmonyAnalyzerService:
    def __init__(self):
        self.theory_engine = MusicTheoryEngine()
        self.knowledge_base = IanGuestKnowledgeBase()

    def analyze_progression(self, 
                          chord_symbols: List[str], 
                          key: str = "C",
                          context: str = "tonal") -> Dict[str, Any]:
        """Análise completa de progressão harmônica"""

        # Análise básica usando theory engine
        basic_analysis = self.theory_engine.analyze_chord_progression(chord_symbols, key)

        # Enriquecimento com conhecimento Ian Guest
        enhanced_analysis = self._enhance_with_guest_knowledge(basic_analysis, context)

        # Sugestões de melhoria
        suggestions = self._generate_suggestions(chord_symbols, key, context)

        # Validação de condução de vozes
        voice_leading = self.theory_engine.validate_voice_leading(chord_symbols)

        return {
            "progression": chord_symbols,
            "key": key,
            "context": context,
            "analysis": enhanced_analysis,
            "suggestions": suggestions,
            "voice_leading": voice_leading,
            "pedagogical_notes": self._get_pedagogical_notes(enhanced_analysis),
            "related_concepts": self._get_related_concepts(enhanced_analysis)
        }

    def _enhance_with_guest_knowledge(self, basic_analysis: List[Dict], context: str) -> List[Dict]:
        """Enriquece análise com conhecimento pedagógico Ian Guest"""
        enhanced = []

        for chord_analysis in basic_analysis:
            chord_data = chord_analysis.copy()

            # Adicionar informações pedagógicas
            chord_data["guest_analysis"] = self._get_guest_perspective(chord_analysis)

            # Informações sobre tensões (Ian Guest Vol. 1-2)
            chord_data["tension_theory"] = self._explain_tensions(chord_analysis)

            # Context específico (modal vs tonal)
            chord_data["context_notes"] = self._get_context_specific_notes(chord_analysis, context)

            enhanced.append(chord_data)

        return enhanced

    def _get_guest_perspective(self, chord_analysis: Dict) -> Dict:
        """Perspectiva pedagógica do Ian Guest sobre o acorde"""
        chord = chord_analysis["chord"]
        function = chord_analysis["function"]

        guest_notes = {
            "volume_reference": self._get_volume_reference(chord),
            "pedagogical_approach": self._get_pedagogical_approach(chord),
            "common_usage": self._get_common_usage(chord, function),
            "student_challenges": self._get_student_challenges(chord)
        }

        return guest_notes

    def _get_volume_reference(self, chord: Chord) -> str:
        """Referência ao volume do Ian Guest onde o conceito é abordado"""
        if chord.quality.value in ["major", "minor", "diminished"]:
            return "Volume 1 - Acordes Tríade (p. 41-55)"
        elif "7" in chord.quality.value:
            return "Volume 1 - Acordes de Sétima (p. 71-85)"
        elif chord.function == Function.SUBSTITUTE:
            return "Volume 2 - Substitutos (p. 46-60)"
        else:
            return "Volume 1 - Conceitos Fundamentais"

    def _get_pedagogical_approach(self, chord: Chord) -> str:
        """Abordagem pedagógica recomendada pelo Ian Guest"""
        approaches = {
            "major": "Comece com tríade, depois adicione sétima maior para jazz/bossa nova",
            "minor": "Base: 3ª menor. Experimente com sétima menor para cor jazzística",
            "dominant7": "Acorde essencial! Memorize as 4 inversões e pratique resoluções",
            "half_diminished": "Comum no ii grau menor. Pratique com escala lócria"
        }

        return approaches.get(chord.quality.value, "Pratique em diferentes inversões")

    def _explain_tensions(self, chord_analysis: Dict) -> Dict:
        """Explicação detalhada das tensões disponíveis"""
        tensions = chord_analysis.get("tensions_available", [])

        tension_explanations = {}
        for tension in tensions:
            if tension == "9":
                tension_explanations[tension] = "9ª: Adiciona cor sem alterar função. Evite com 4ª no baixo."
            elif tension == "11":
                tension_explanations[tension] = "11ª: Cuidado em acordes maiores (choque com 3ª). Ótima em menores."
            elif tension == "13":
                tension_explanations[tension] = "13ª: Substitui ou completa 6ª. Cor sofisticada."
            elif tension == "#11":
                tension_explanations[tension] = "#11: Som lídio. Muito usada em acordes maiores."
            elif tension == "b13":
                tension_explanations[tension] = "b13: Tensão alterada. Comum em dominantes."

        return {
            "available_tensions": tensions,
            "explanations": tension_explanations,
            "usage_tips": self._get_tension_usage_tips(chord_analysis["chord"])
        }

    def _get_tension_usage_tips(self, chord: Chord) -> List[str]:
        """Dicas de uso das tensões baseadas no Ian Guest"""
        tips = []

        if chord.quality.value == "major7":
            tips.extend([
                "Use 9ª para suavizar o som",
                "#11 cria sonoridade lídica interessante",
                "Evite 11ª natural (choque com 3ª maior)"
            ])
        elif chord.quality.value == "minor7":
            tips.extend([
                "11ª natural soa excelente",
                "9ª adiciona cor dórica",
                "13ª pode substituir 6ª"
            ])
        elif chord.quality.value == "dominant7":
            tips.extend([
                "Todas as tensões são válidas",
                "b13 e #11 para som alterado",
                "9ª é a mais suave para começar"
            ])

        return tips

    def _generate_suggestions(self, chord_symbols: List[str], key: str, context: str) -> Dict:
        """Gera sugestões de melhoria baseadas na metodologia Ian Guest"""
        suggestions = {
            "harmonic_enrichment": [],
            "voice_leading_improvements": [],
            "style_suggestions": [],
            "pedagogical_exercises": []
        }

        # Análise da progressão para sugestões
        analysis = self.theory_engine.analyze_chord_progression(chord_symbols, key)

        # Sugestões de enriquecimento harmônico
        for i, chord_data in enumerate(analysis):
            chord_symbol = chord_symbols[i]

            # Sugestões de substitutos
            substitutes = self.theory_engine.suggest_chord_substitutions(
                chord_data["chord"], key
            )

            if substitutes:
                suggestions["harmonic_enrichment"].append({
                    "original": chord_symbol,
                    "substitutes": substitutes,
                    "explanation": f"Alternativas para {chord_symbol} baseadas no Volume 2 do Ian Guest"
                })

        # Sugestões de estilo
        if self._is_jazz_progression(analysis):
            suggestions["style_suggestions"].append(
                "Esta progressão tem características jazzísticas. Considere usar acordes com 7ª."
            )

        if self._has_modal_characteristics(analysis):
            suggestions["style_suggestions"].append(
                "Progressão com características modais. Veja Volume 3 do Ian Guest sobre modalismo."
            )

        # Exercícios pedagógicos recomendados
        suggestions["pedagogical_exercises"] = self._recommend_exercises(analysis)

        return suggestions

    def _is_jazz_progression(self, analysis: List[Dict]) -> bool:
        """Detecta se a progressão tem características jazzísticas"""
        functions = [chord["function"] for chord in analysis]

        # Procura por ii-V-I
        for i in range(len(functions) - 2):
            if (functions[i] == "S" and 
                functions[i+1] == "D" and 
                functions[i+2] == "T"):
                return True

        return False

    def _has_modal_characteristics(self, analysis: List[Dict]) -> bool:
        """Detecta características modais"""
        # Simplificado: busca por acordes que não são do campo harmônico tradicional
        return any(chord["function"] == "sub" for chord in analysis)

    def _recommend_exercises(self, analysis: List[Dict]) -> List[str]:
        """Recomenda exercícios baseados na análise"""
        exercises = []

        # Verifica quais conceitos estão presentes
        has_seventh_chords = any("7" in chord["chord_symbol"] for chord in analysis)
        has_secondary_dominants = any(chord["function"] == "V/x" for chord in analysis)

        if has_seventh_chords:
            exercises.append("Pratique as inversões dos acordes de 7ª presentes")

        if has_secondary_dominants:
            exercises.append("Estude dominantes secundários no Volume 2 do Ian Guest")

        exercises.append("Toque a progressão em diferentes tonalidades")
        exercises.append("Experimente diferentes ritmos e estilos")

        return exercises

    def _get_pedagogical_notes(self, analysis: List[Dict]) -> List[str]:
        """Notas pedagógicas gerais sobre a progressão"""
        notes = []

        # Análise de dificuldade
        difficulty_factors = self._assess_difficulty(analysis)
        notes.append(f"Nível de dificuldade: {difficulty_factors['level']}")

        # Conceitos importantes
        concepts = set()
        for chord_data in analysis:
            concepts.add(chord_data["chord"].quality.value)

        notes.append(f"Conceitos envolvidos: {', '.join(concepts)}")

        return notes

    def _assess_difficulty(self, analysis: List[Dict]) -> Dict:
        """Avalia nível de dificuldade da progressão"""
        difficulty_points = 0

        for chord_data in analysis:
            chord = chord_data["chord"]

            # Pontos por tipo de acorde
            if "7" in chord.quality.value:
                difficulty_points += 1
            if chord.extensions:
                difficulty_points += len(chord.extensions)
            if chord.function == Function.SUBSTITUTE:
                difficulty_points += 2

        if difficulty_points <= 2:
            return {"level": "Básico", "points": difficulty_points}
        elif difficulty_points <= 5:
            return {"level": "Intermediário", "points": difficulty_points}
        else:
            return {"level": "Avançado", "points": difficulty_points}

    def _get_related_concepts(self, analysis: List[Dict]) -> List[str]:
        """Conceitos relacionados para estudo complementar"""
        concepts = set()

        for chord_data in analysis:
            quality = chord_data["chord"].quality.value

            if quality == "dominant7":
                concepts.add("resolução_de_dominantes")
                concepts.add("escalas_dominantes")
            elif "minor" in quality:
                concepts.add("modos_menores")
                concepts.add("escalas_menores")
            elif quality == "major7":
                concepts.add("modos_maiores")
                concepts.add("tensões_maiores")

        return list(concepts)

    def get_chord_detail(self, chord_symbol: str, key: str = "C") -> Dict:
        """Análise detalhada de um acorde específico"""
        chord = self.theory_engine.parse_chord(chord_symbol)

        detail = {
            "chord_symbol": chord_symbol,
            "parsed_chord": chord,
            "notes": self._get_chord_notes(chord),
            "inversions": self._get_inversions(chord),
            "available_tensions": self.theory_engine._get_available_tensions(chord, key),
            "recommended_scales": self.theory_engine._recommend_scales(chord, key),
            "guest_pedagogy": self._get_guest_pedagogy_for_chord(chord),
            "practice_suggestions": self._get_practice_suggestions(chord)
        }

        return detail

    def _get_chord_notes(self, chord: Chord) -> List[str]:
        """Retorna as notas do acorde"""
        root_index = self.theory_engine.chromatic_notes.index(chord.root)
        notes = [chord.root]

        # Mapeamento básico de intervalos por qualidade
        intervals_map = {
            "major": [4, 7],
            "minor": [3, 7],
            "diminished": [3, 6],
            "augmented": [4, 8],
            "major7": [4, 7, 11],
            "minor7": [3, 7, 10],
            "dominant7": [4, 7, 10],
            "half_diminished": [3, 6, 10],
            "diminished7": [3, 6, 9]
        }

        intervals = intervals_map.get(chord.quality.value, [4, 7])

        for interval in intervals:
            note_index = (root_index + interval) % 12
            notes.append(self.theory_engine.chromatic_notes[note_index])

        return notes

    def _get_inversions(self, chord: Chord) -> List[str]:
        """Gera as inversões do acorde"""
        notes = self._get_chord_notes(chord)
        inversions = []

        for i in range(len(notes)):
            inversion_notes = notes[i:] + notes[:i]
            bass_note = inversion_notes[0]

            if i == 0:
                inversions.append(f"{chord.root}{chord.quality.value}")
            else:
                inversions.append(f"{chord.root}{chord.quality.value}/{bass_note}")

        return inversions

    def _get_guest_pedagogy_for_chord(self, chord: Chord) -> Dict:
        """Pedagogia específica do Ian Guest para o acorde"""
        return {
            "volume_reference": self._get_volume_reference(chord),
            "practice_order": self._get_practice_order(chord),
            "common_mistakes": self._get_common_mistakes(chord),
            "musical_examples": self._get_musical_examples(chord)
        }

    def _get_practice_order(self, chord: Chord) -> List[str]:
        """Ordem de prática recomendada pelo Ian Guest"""
        base_order = [
            "1. Aprenda a tríade básica",
            "2. Pratique as inversões",
            "3. Adicione a sétima",
            "4. Experimente tensões"
        ]

        if chord.quality.value == "dominant7":
            base_order.append("5. Pratique resoluções em diferentes tonalidades")

        return base_order

    def _get_common_mistakes(self, chord: Chord) -> List[str]:
        """Erros comuns identificados pelo Ian Guest"""
        mistakes = []

        if chord.quality.value == "major7":
            mistakes.extend([
                "Confundir com acorde dominante",
                "Usar 11ª natural (choque com 3ª maior)"
            ])
        elif chord.quality.value == "minor7":
            mistakes.extend([
                "Tocar muito pesado",
                "Não explorar a 11ª natural"
            ])

        return mistakes

    def _get_musical_examples(self, chord: Chord) -> List[str]:
        """Exemplos musicais do repertório popular brasileiro"""
        examples = {
            "major7": ["Girl from Ipanema", "Corcovado"],
            "minor7": ["So What", "Autumn Leaves"],
            "dominant7": ["Blue Bossa", "All Blues"]
        }

        return examples.get(chord.quality.value, ["Pratique em standards de jazz"])

    def _get_practice_suggestions(self, chord: Chord) -> List[str]:
        """Sugestões práticas de estudo"""
        return [
            f"Pratique {chord.root}{chord.quality.value} em todas as inversões",
            "Toque em diferentes ritmos (bossa nova, jazz, pop)",
            "Combine com outros acordes da mesma família",
            "Improvise melodias usando as tensões disponíveis"
        ]
