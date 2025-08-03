
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class ExerciseTemplate:
    level: int
    category: str
    description: str
    example: str
    solution: str
    feedback_points: List[str]

@dataclass
class ConceptExplanation:
    concept: str
    volume: int
    page_reference: str
    explanation: str
    examples: List[str]
    related_concepts: List[str]

class IanGuestKnowledgeBase:
    def __init__(self):
        self.concepts = self._init_concepts()
        self.exercises = self._init_exercises()
        self.progressions = self._init_common_progressions()
        self.pedagogical_sequence = self._init_pedagogical_sequence()

    def _init_concepts(self) -> Dict[str, ConceptExplanation]:
        """Base de conceitos dos 3 volumes do Ian Guest"""
        return {
            # VOLUME 1 - Conceitos Fundamentais
            "intervalos": ConceptExplanation(
                concept="Intervalos",
                volume=1,
                page_reference="p. 15-25",
                explanation="Distância entre duas notas musicais. Base fundamental para compreensão harmônica.",
                examples=["C-E = 3ª maior", "C-Eb = 3ª menor", "C-F = 4ª justa"],
                related_concepts=["escalas", "acordes", "tensões"]
            ),

            "escalas_diatonicas": ConceptExplanation(
                concept="Escalas Diatônicas",
                volume=1,
                page_reference="p. 26-40",
                explanation="Sistema de 7 notas que forma a base da harmonia tonal ocidental.",
                examples=["C maior: C-D-E-F-G-A-B", "A menor: A-B-C-D-E-F-G"],
                related_concepts=["intervalos", "modos", "campo_harmonico"]
            ),

            "acordes_triade": ConceptExplanation(
                concept="Acordes Tríade",
                volume=1,
                page_reference="p. 41-55",
                explanation="Acordes formados por 3 notas: fundamental, terça e quinta.",
                examples=["C = C-E-G", "Dm = D-F-A", "G7 = G-B-D-F"],
                related_concepts=["intervalos", "inversões", "campo_harmonico"]
            ),

            "campo_harmonico": ConceptExplanation(
                concept="Campo Harmônico",
                volume=1,
                page_reference="p. 56-70",
                explanation="Conjunto de acordes formados a partir de uma escala diatônica.",
                examples=["C maior: C - Dm - Em - F - G - Am - Bº"],
                related_concepts=["escalas_diatonicas", "funções_harmonicas", "progressões"]
            ),

            # VOLUME 2 - Conceitos Avançados
            "acordes_emprestimo": ConceptExplanation(
                concept="Acordes de Empréstimo Modal",
                volume=2,
                page_reference="p. 10-25",
                explanation="Acordes provenientes de outros modos da mesma tônica.",
                examples=["Em C maior: Fm (do modo menor)", "Bb (do modo mixolídio)"],
                related_concepts=["modos", "intercâmbio_modal", "rearmonização"]
            ),

            "dominantes_secundarios": ConceptExplanation(
                concept="Dominantes Secundários",
                volume=2,
                page_reference="p. 26-45",
                explanation="Acordes dominantes que resolvem em graus diferentes da tônica.",
                examples=["V/vi = E7 → Am", "V/ii = A7 → Dm", "V/V = D7 → G7"],
                related_concepts=["dominantes", "modulação", "tonicização"]
            ),

            "substitutos_dominante": ConceptExplanation(
                concept="Substitutos de Dominante",
                volume=2,
                page_reference="p. 46-60",
                explanation="Acordes que podem substituir a função dominante.",
                examples=["SubV7: Db7 → C", "bIIM7: DbM7 → C"],
                related_concepts=["trítono", "resolução", "jazz_harmony"]
            ),

            # VOLUME 3 - Modalismo
            "modos_gregos": ConceptExplanation(
                concept="Modos Gregos",
                volume=3,
                page_reference="p. 5-30",
                explanation="Sete modos derivados da escala diatônica, cada um com característica única.",
                examples=["Dórico: som menor com 6ª maior", "Mixolídio: som maior com 7ª menor"],
                related_concepts=["escalas_diatonicas", "harmonia_modal", "improvisação"]
            ),

            "harmonia_modal": ConceptExplanation(
                concept="Harmonia Modal",
                volume=3,
                page_reference="p. 31-55",
                explanation="Sistema harmônico baseado em modos, sem função tonal tradicional.",
                examples=["Progressão dórica: Dm - C - Dm", "Mixolídia: G - F - G"],
                related_concepts=["modos_gregos", "acordes_modais", "música_brasileira"]
            ),

            "fusao_modal": ConceptExplanation(
                concept="Fusão de Modos",
                volume=3,
                page_reference="p. 56-75",
                explanation="Combinação de diferentes modos numa mesma progressão.",
                examples=["C jônio → C lídio", "Am eólio → Am dórico"],
                related_concepts=["modos_gregos", "modulação_modal", "arranjo"]
            )
        }

    def _init_exercises(self) -> Dict[str, List[ExerciseTemplate]]:
        """Exercícios baseados na metodologia Ian Guest"""
        return {
            "nivel_1_basico": [
                ExerciseTemplate(
                    level=1,
                    category="identificação_intervalos",
                    description="Identifique os intervalos entre as notas",
                    example="C - E = ?",
                    solution="3ª maior",
                    feedback_points=[
                        "C para E = 2 tons = 3ª maior",
                        "Intervalo consonante e estável",
                        "Base do acorde maior"
                    ]
                ),
                ExerciseTemplate(
                    level=1,
                    category="formação_acordes",
                    description="Forme a tríade solicitada",
                    example="Forme Dm",
                    solution="D - F - A",
                    feedback_points=[
                        "Fundamental: D",
                        "Terça menor: F",
                        "Quinta justa: A",
                        "Acorde menor = 3ª menor + 5ª justa"
                    ]
                ),
                ExerciseTemplate(
                    level=1,
                    category="campo_harmonico",
                    description="Complete o campo harmônico",
                    example="Campo harmônico de G maior",
                    solution="G - Am - Bm - C - D - Em - F#º",
                    feedback_points=[
                        "Escala: G-A-B-C-D-E-F#",
                        "Tríades formadas sobre cada grau",
                        "Padrão: M-m-m-M-M-m-º"
                    ]
                )
            ],

            "nivel_2_intermediario": [
                ExerciseTemplate(
                    level=2,
                    category="emprestimo_modal",
                    description="Identifique o acorde de empréstimo",
                    example="Em C maior: C - Fm - G - C",
                    solution="Fm é empréstimo do modo menor",
                    feedback_points=[
                        "Fm não pertence ao campo de C maior",
                        "Vem do campo de C menor",
                        "Cria contraste modal interessante"
                    ]
                ),
                ExerciseTemplate(
                    level=2,
                    category="dominantes_secundarios",
                    description="Insira dominante secundário",
                    example="C - Am - Dm - G - C",
                    solution="C - A7 - Dm - G - C",
                    feedback_points=[
                        "A7 = V/ii (dominante de Dm)",
                        "Cria tensão direcionada",
                        "Intensifica resolução em Dm"
                    ]
                )
            ],

            "nivel_3_avancado": [
                ExerciseTemplate(
                    level=3,
                    category="rearmonizacao",
                    description="Rearmonize usando substitutos",
                    example="C - Am - Dm - G7 - C",
                    solution="C - Am - Dm - Db7 - C",
                    feedback_points=[
                        "Db7 = substituto tritonal de G7",
                        "Movimento cromático no baixo",
                        "Sofisticação harmônica"
                    ]
                ),
                ExerciseTemplate(
                    level=3,
                    category="harmonia_modal",
                    description="Analise a progressão modal",
                    example="Em - D - Em (modo dórico)",
                    solution="i - bVII - i em E dórico",
                    feedback_points=[
                        "Centro modal: Em",
                        "D maior caracteriza dórico",
                        "Som menor com 6ª maior"
                    ]
                )
            ]
        }

    def _init_common_progressions(self) -> Dict[str, Dict]:
        """Progressões comuns da música popular"""
        return {
            "ii_V_I": {
                "description": "Progressão fundamental do jazz",
                "example": "Dm7 - G7 - CM7",
                "analysis": "ii7 - V7 - IM7",
                "variations": ["Dm7 - Db7 - CM7", "D7alt - G7alt - CM7"],
                "style": "jazz_bossa_nova"
            },

            "vi_IV_I_V": {
                "description": "Progressão pop clássica",
                "example": "Am - F - C - G",
                "analysis": "vi - IV - I - V",
                "variations": ["Am7 - FM7 - CM7 - G7", "A7 - F - C - G"],
                "style": "pop_rock"
            },

            "I_vi_ii_V": {
                "description": "Turnaround clássico",
                "example": "C - Am - Dm - G",
                "analysis": "I - vi - ii - V",
                "variations": ["C6 - A7 - Dm7 - G7", "CM7 - Am7 - Dm7 - G7"],
                "style": "jazz_standards"
            }
        }

    def _init_pedagogical_sequence(self) -> List[str]:
        """Sequência pedagógica recomendada por Ian Guest"""
        return [
            "intervalos",
            "escalas_diatonicas", 
            "acordes_triade",
            "campo_harmonico",
            "inversões",
            "acordes_setima",
            "funções_harmonicas",
            "progressões_basicas",
            "emprestimo_modal",
            "dominantes_secundarios",
            "substitutos_dominante",
            "modos_gregos",
            "harmonia_modal",
            "fusao_modal",
            "rearmonização_avancada"
        ]

    def get_exercise_by_level(self, level: int, category: str = None) -> List[ExerciseTemplate]:
        """Retorna exercícios por nível"""
        level_map = {
            1: "nivel_1_basico",
            2: "nivel_2_intermediario", 
            3: "nivel_3_avancado"
        }

        exercises = self.exercises.get(level_map.get(level, "nivel_1_basico"), [])

        if category:
            exercises = [ex for ex in exercises if ex.category == category]

        return exercises

    def get_concept_explanation(self, concept: str) -> ConceptExplanation:
        """Retorna explicação de conceito"""
        return self.concepts.get(concept)

    def get_related_concepts(self, concept: str) -> List[ConceptExplanation]:
        """Retorna conceitos relacionados"""
        base_concept = self.concepts.get(concept)
        if not base_concept:
            return []

        related = []
        for related_name in base_concept.related_concepts:
            related_concept = self.concepts.get(related_name)
            if related_concept:
                related.append(related_concept)

        return related

    def validate_exercise_answer(self, exercise: ExerciseTemplate, user_answer: str) -> Dict:
        """Valida resposta do usuário"""
        is_correct = user_answer.lower().strip() == exercise.solution.lower().strip()

        feedback = {
            "is_correct": is_correct,
            "expected_answer": exercise.solution,
            "feedback_points": exercise.feedback_points,
            "encouragement": self._get_encouragement(is_correct),
            "next_steps": self._get_next_steps(exercise, is_correct)
        }

        return feedback

    def _get_encouragement(self, is_correct: bool) -> str:
        """Feedback motivacional"""
        if is_correct:
            return "Excelente! Você demonstrou boa compreensão do conceito."
        else:
            return "Não desanime! Esse é um conceito importante que requer prática."

    def _get_next_steps(self, exercise: ExerciseTemplate, is_correct: bool) -> List[str]:
        """Sugestões de próximos passos"""
        if is_correct:
            return [
                "Tente exercícios mais avançados desta categoria",
                "Explore conceitos relacionados",
                "Aplique em repertório musical"
            ]
        else:
            return [
                "Revise os conceitos fundamentais",
                "Pratique exercícios similares",
                "Consulte a explicação teórica"
            ]
