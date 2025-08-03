
from typing import List, Dict, Optional, Any
from ..core.music_theory_engine import MusicTheoryEngine
from ..knowledge_base.ian_guest_kb import IanGuestKnowledgeBase, ExerciseTemplate

class ExerciseCorrectorService:
    def __init__(self):
        self.theory_engine = MusicTheoryEngine()
        self.knowledge_base = IanGuestKnowledgeBase()

    def correct_exercise(self, exercise_type: str, user_answer: str, 
                        exercise_data: Dict = None, level: int = 1) -> Dict[str, Any]:
        """Corrige exercício do usuário com feedback pedagógico"""

        # Obter template do exercício ou usar dados fornecidos
        if exercise_data:
            exercise_template = self._create_exercise_from_data(exercise_data)
        else:
            exercise_template = self._get_exercise_template(exercise_type, level)

        if not exercise_template:
            return self._create_error_response("Tipo de exercício não encontrado")

        # Validar resposta
        validation_result = self._validate_answer(exercise_template, user_answer)

        # Gerar feedback detalhado
        feedback = self._generate_detailed_feedback(
            exercise_template, user_answer, validation_result
        )

        # Sugerir próximos passos
        next_steps = self._suggest_next_steps(exercise_template, validation_result)

        return {
            "exercise": {
                "type": exercise_type,
                "level": level,
                "description": exercise_template.description,
                "example": exercise_template.example
            },
            "user_answer": user_answer,
            "correct_answer": exercise_template.solution,
            "is_correct": validation_result["is_correct"],
            "score": validation_result["score"],
            "feedback": feedback,
            "next_steps": next_steps,
            "guest_pedagogy": self._get_guest_pedagogical_notes(exercise_template)
        }

    def _get_exercise_template(self, exercise_type: str, level: int) -> Optional[ExerciseTemplate]:
        """Obtém template de exercício da base de conhecimento"""
        exercises = self.knowledge_base.get_exercise_by_level(level, exercise_type)
        if exercises:
            return exercises[0]  # Retorna primeiro exercício do tipo
        return None

    def _create_exercise_from_data(self, exercise_data: Dict) -> ExerciseTemplate:
        """Cria exercício a partir de dados fornecidos"""
        return ExerciseTemplate(
            level=exercise_data.get("level", 1),
            category=exercise_data.get("category", "geral"),
            description=exercise_data.get("description", ""),
            example=exercise_data.get("example", ""),
            solution=exercise_data.get("solution", ""),
            feedback_points=exercise_data.get("feedback_points", [])
        )

    def _validate_answer(self, exercise: ExerciseTemplate, user_answer: str) -> Dict:
        """Valida resposta com diferentes níveis de tolerância"""

        # Normalizar respostas
        normalized_user = self._normalize_answer(user_answer)
        normalized_correct = self._normalize_answer(exercise.solution)

        # Validação por categoria
        if exercise.category == "identificação_intervalos":
            return self._validate_interval_answer(normalized_user, normalized_correct)
        elif exercise.category == "formação_acordes":
            return self._validate_chord_formation(normalized_user, normalized_correct)
        elif exercise.category == "campo_harmonico":
            return self._validate_harmonic_field(normalized_user, normalized_correct)
        elif exercise.category == "emprestimo_modal":
            return self._validate_modal_borrowing(normalized_user, normalized_correct)
        elif exercise.category == "dominantes_secundarios":
            return self._validate_secondary_dominants(normalized_user, normalized_correct)
        elif exercise.category == "rearmonizacao":
            return self._validate_reharmonization(normalized_user, normalized_correct)
        elif exercise.category == "harmonia_modal":
            return self._validate_modal_harmony(normalized_user, normalized_correct)
        else:
            return self._validate_generic(normalized_user, normalized_correct)

    def _normalize_answer(self, answer: str) -> str:
        """Normaliza resposta para comparação"""
        return answer.lower().strip().replace(" ", "")

    def _validate_interval_answer(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação específica para intervalos"""
        # Mapeamento de alternativas válidas
        interval_alternatives = {
            "3ªmaior": ["3maior", "tercamaior", "terçamaior", "3m", "3ªm"],
            "3ªmenor": ["3menor", "tercamenor", "terçamenor", "3m", "3ªm"],
            "5ªjusta": ["5justa", "quintajusta", "5j", "5ªj"],
            "4ªjusta": ["4justa", "quartajusta", "4j", "4ªj"]
        }

        # Verificar se a resposta do usuário está nas alternativas válidas
        for correct, alternatives in interval_alternatives.items():
            if correct_answer == correct.lower().replace("ª", ""):
                if user_answer in [alt.lower() for alt in alternatives]:
                    return {"is_correct": True, "score": 100}

        # Verificação direta
        is_correct = user_answer == correct_answer
        score = 100 if is_correct else self._calculate_partial_score(user_answer, correct_answer)

        return {"is_correct": is_correct, "score": score}

    def _validate_chord_formation(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação para formação de acordes"""
        # Separar notas da resposta
        user_notes = self._extract_notes_from_answer(user_answer)
        correct_notes = self._extract_notes_from_answer(correct_answer)

        # Verificar se as notas estão corretas (ordem não importa)
        user_set = set(user_notes)
        correct_set = set(correct_notes)

        if user_set == correct_set:
            return {"is_correct": True, "score": 100}

        # Calcular pontuação parcial baseada nas notas corretas
        correct_count = len(user_set.intersection(correct_set))
        total_count = len(correct_set)
        score = int((correct_count / total_count) * 100) if total_count > 0 else 0

        return {"is_correct": False, "score": score}

    def _extract_notes_from_answer(self, answer: str) -> List[str]:
        """Extrai notas de uma resposta de acorde"""
        # Remove espaços e separa por hífen ou vírgula
        notes = answer.replace(" ", "").replace("-", ",").split(",")
        return [note.strip() for note in notes if note.strip()]

    def _validate_harmonic_field(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação para campo harmônico"""
        user_chords = self._extract_chords_from_field(user_answer)
        correct_chords = self._extract_chords_from_field(correct_answer)

        # Verificar ordem e correção
        if len(user_chords) != len(correct_chords):
            return {"is_correct": False, "score": 0}

        correct_count = 0
        for i, (user_chord, correct_chord) in enumerate(zip(user_chords, correct_chords)):
            if self._normalize_chord_symbol(user_chord) == self._normalize_chord_symbol(correct_chord):
                correct_count += 1

        score = int((correct_count / len(correct_chords)) * 100)
        is_correct = score == 100

        return {"is_correct": is_correct, "score": score}

    def _extract_chords_from_field(self, field_answer: str) -> List[str]:
        """Extrai acordes de um campo harmônico"""
        return [chord.strip() for chord in field_answer.split("-") if chord.strip()]

    def _normalize_chord_symbol(self, chord: str) -> str:
        """Normaliza símbolo de acorde"""
        return chord.lower().replace("°", "dim").replace("ø", "m7b5")

    def _validate_modal_borrowing(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação para empréstimo modal"""
        # Verificação se identifica o acorde e sua origem
        keywords_user = set(user_answer.split())
        keywords_correct = set(correct_answer.split())

        # Pontuação baseada em palavras-chave importantes
        important_keywords = ["empréstimo", "menor", "maior", "modal", "modo"]
        user_important = keywords_user.intersection(important_keywords)
        correct_important = keywords_correct.intersection(important_keywords)

        if user_important == correct_important and len(user_important) > 0:
            return {"is_correct": True, "score": 100}

        # Pontuação parcial
        score = int((len(user_important) / max(len(correct_important), 1)) * 100)
        return {"is_correct": False, "score": score}

    def _validate_secondary_dominants(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação para dominantes secundários"""
        # Extrair acordes da progressão
        user_progression = self._extract_chords_from_field(user_answer)
        correct_progression = self._extract_chords_from_field(correct_answer)

        if len(user_progression) != len(correct_progression):
            return {"is_correct": False, "score": 0}

        # Verificar se inseriu dominante secundário no local correto
        correct_count = 0
        for i, (user_chord, correct_chord) in enumerate(zip(user_progression, correct_progression)):
            if self._is_equivalent_chord(user_chord, correct_chord):
                correct_count += 1

        score = int((correct_count / len(correct_progression)) * 100)
        return {"is_correct": score == 100, "score": score}

    def _is_equivalent_chord(self, chord1: str, chord2: str) -> bool:
        """Verifica se dois acordes são equivalentes"""
        try:
            parsed1 = self.theory_engine.parse_chord(chord1)
            parsed2 = self.theory_engine.parse_chord(chord2)

            return (parsed1.root == parsed2.root and 
                   parsed1.quality == parsed2.quality)
        except:
            return self._normalize_chord_symbol(chord1) == self._normalize_chord_symbol(chord2)

    def _validate_reharmonization(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação para rearmonização"""
        # Para rearmonização, várias respostas podem estar corretas
        # Verificar se a substituição faz sentido teoricamente

        user_progression = self._extract_chords_from_field(user_answer)
        correct_progression = self._extract_chords_from_field(correct_answer)

        # Análise mais sofisticada - verificar se a função harmônica é preservada
        try:
            user_analysis = self.theory_engine.analyze_chord_progression(user_progression)
            correct_analysis = self.theory_engine.analyze_chord_progression(correct_progression)

            # Comparar funções harmônicas
            user_functions = [chord["function"] for chord in user_analysis]
            correct_functions = [chord["function"] for chord in correct_analysis]

            if user_functions == correct_functions:
                return {"is_correct": True, "score": 100}
        except:
            pass

        # Fallback para comparação direta
        return self._validate_generic(user_answer, correct_answer)

    def _validate_modal_harmony(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação para harmonia modal"""
        # Verificar se identifica o centro modal e a análise
        user_parts = user_answer.split()
        correct_parts = correct_answer.split()

        # Procurar por elementos chave
        modal_keywords = ["dórico", "dor", "mixolídio", "mix", "lídio", "lid"]
        roman_numerals = ["i", "ii", "iii", "iv", "v", "vi", "vii", "bvii"]

        user_modal = any(keyword in user_answer.lower() for keyword in modal_keywords)
        correct_modal = any(keyword in correct_answer.lower() for keyword in modal_keywords)

        user_roman = any(numeral in user_answer.lower() for numeral in roman_numerals)
        correct_roman = any(numeral in correct_answer.lower() for numeral in roman_numerals)

        score = 0
        if user_modal and correct_modal:
            score += 50
        if user_roman and correct_roman:
            score += 50

        return {"is_correct": score == 100, "score": score}

    def _validate_generic(self, user_answer: str, correct_answer: str) -> Dict:
        """Validação genérica para outros tipos"""
        is_correct = user_answer == correct_answer
        score = 100 if is_correct else self._calculate_partial_score(user_answer, correct_answer)
        return {"is_correct": is_correct, "score": score}

    def _calculate_partial_score(self, user_answer: str, correct_answer: str) -> int:
        """Calcula pontuação parcial baseada em similaridade"""
        if not user_answer or not correct_answer:
            return 0

        # Algoritmo simples de similaridade
        longer = max(len(user_answer), len(correct_answer))
        if longer == 0:
            return 100

        # Contagem de caracteres em comum
        common_chars = sum(1 for i, char in enumerate(user_answer) 
                          if i < len(correct_answer) and char == correct_answer[i])

        return int((common_chars / longer) * 100)

    def _generate_detailed_feedback(self, exercise: ExerciseTemplate, 
                                  user_answer: str, validation: Dict) -> Dict:
        """Gera feedback pedagógico detalhado"""
        feedback = {
            "score_feedback": self._get_score_feedback(validation["score"]),
            "specific_feedback": [],
            "encouragement": self._get_encouragement_message(validation["score"]),
            "concept_review": [],
            "practice_tips": exercise.feedback_points.copy()
        }

        # Feedback específico por categoria
        if exercise.category == "identificação_intervalos":
            feedback["specific_feedback"] = self._get_interval_feedback(
                user_answer, exercise.solution, validation
            )
        elif exercise.category == "formação_acordes":
            feedback["specific_feedback"] = self._get_chord_feedback(
                user_answer, exercise.solution, validation
            )
        elif exercise.category == "campo_harmonico":
            feedback["specific_feedback"] = self._get_field_feedback(
                user_answer, exercise.solution, validation
            )

        return feedback

    def _get_score_feedback(self, score: int) -> str:
        """Feedback baseado na pontuação"""
        if score >= 90:
            return "Excelente! Demonstrou domínio completo do conceito."
        elif score >= 70:
            return "Bom trabalho! Alguns pequenos ajustes podem melhorar sua resposta."
        elif score >= 50:
            return "No caminho certo! Continue praticando para consolidar o conhecimento."
        else:
            return "Precisa revisar os conceitos fundamentais. Não desanime!"

    def _get_encouragement_message(self, score: int) -> str:
        """Mensagem motivacional baseada no método Ian Guest"""
        messages = {
            90: "Parabéns! Você está aplicando bem a metodologia do Ian Guest.",
            70: "Muito bem! Continue praticando com a sistematização do método.",
            50: "Está progredindo! A persistência é fundamental no aprendizado musical.",
            0: "Todo músico passa por dificuldades. Continue estudando com paciência."
        }

        for threshold in sorted(messages.keys(), reverse=True):
            if score >= threshold:
                return messages[threshold]

        return messages[0]

    def _get_interval_feedback(self, user_answer: str, correct_answer: str, validation: Dict) -> List[str]:
        """Feedback específico para intervalos"""
        feedback = []

        if not validation["is_correct"]:
            feedback.append(f"A resposta correta é: {correct_answer}")
            feedback.append("Lembre-se: conte os semitons entre as notas")
            feedback.append("Revise a tabela de intervalos no Volume 1 do Ian Guest")

        return feedback

    def _get_chord_feedback(self, user_answer: str, correct_answer: str, validation: Dict) -> List[str]:
        """Feedback específico para formação de acordes"""
        feedback = []

        if validation["score"] < 100:
            feedback.append(f"Formação correta: {correct_answer}")

            if validation["score"] > 0:
                feedback.append("Você acertou algumas notas, mas revise a formação completa")
            else:
                feedback.append("Revise como formar tríades: fundamental + 3ª + 5ª")

            feedback.append("Pratique a formação em diferentes tonalidades")

        return feedback

    def _get_field_feedback(self, user_answer: str, correct_answer: str, validation: Dict) -> List[str]:
        """Feedback específico para campo harmônico"""
        feedback = []

        if validation["score"] < 100:
            feedback.append(f"Campo harmônico correto: {correct_answer}")
            feedback.append("Lembre-se do padrão: I-ii-iii-IV-V-vi-vii°")
            feedback.append("Cada grau tem sua qualidade específica (maior/menor/diminuto)")

        return feedback

    def _suggest_next_steps(self, exercise: ExerciseTemplate, validation: Dict) -> List[str]:
        """Sugere próximos passos baseados no desempenho"""
        next_steps = []

        if validation["is_correct"]:
            next_steps.extend([
                f"Tente exercícios de nível {exercise.level + 1}",
                f"Pratique {exercise.category} em diferentes contextos",
                "Aplique o conceito em repertório musical"
            ])
        else:
            next_steps.extend([
                "Revise a teoria antes de tentar novamente",
                f"Pratique exercícios similares de {exercise.category}",
                "Consulte as referências do Ian Guest mencionadas"
            ])

        return next_steps

    def _get_guest_pedagogical_notes(self, exercise: ExerciseTemplate) -> Dict:
        """Notas pedagógicas específicas do método Ian Guest"""
        return {
            "methodology_notes": self._get_methodology_notes(exercise.category),
            "common_student_errors": self._get_common_errors(exercise.category),
            "practice_sequence": self._get_practice_sequence(exercise.category),
            "musical_applications": self._get_musical_applications(exercise.category)
        }

    def _get_methodology_notes(self, category: str) -> List[str]:
        """Notas metodológicas por categoria"""
        notes_map = {
            "identificação_intervalos": [
                "Ian Guest enfatiza a importância de 'ouvir' os intervalos",
                "Pratique cantando antes de tocar no instrumento",
                "Associe cada intervalo a uma música conhecida"
            ],
            "formação_acordes": [
                "Método Guest: sempre partir da tríade básica",
                "Memorizar os intervalos componentes",
                "Praticar em todas as inversões"
            ],
            "campo_harmonico": [
                "Base fundamental da harmonia tonal",
                "Ian Guest recomenda decorar em todas as tonalidades",
                "Entender as funções antes das cifras"
            ]
        }

        return notes_map.get(category, ["Continue seguindo a metodologia sistemática"])

    def _get_common_errors(self, category: str) -> List[str]:
        """Erros comuns identificados pelo Ian Guest"""
        errors_map = {
            "identificação_intervalos": [
                "Contar as teclas ao invés dos semitons",
                "Confundir 4ª justa com 5ª diminuta"
            ],
            "formação_acordes": [
                "Esquecer da qualidade da 3ª",
                "Confundir maior com dominante"
            ],
            "campo_harmonico": [
                "Não lembrar do vii° diminuto",
                "Confundir as qualidades dos graus"
            ]
        }

        return errors_map.get(category, [])

    def _get_practice_sequence(self, category: str) -> List[str]:
        """Sequência de prática recomendada"""
        sequence_map = {
            "identificação_intervalos": [
                "1. Decorar intervalos básicos",
                "2. Praticar intervalos compostos", 
                "3. Aplicar em contexto harmônico"
            ],
            "formação_acordes": [
                "1. Tríades maiores e menores",
                "2. Acordes diminutos e aumentados",
                "3. Acordes de sétima",
                "4. Tensões e extensões"
            ]
        }

        return sequence_map.get(category, ["Siga a progressão natural do método"])

    def _get_musical_applications(self, category: str) -> List[str]:
        """Aplicações musicais do conceito"""
        applications_map = {
            "identificação_intervalos": [
                "Análise melódica",
                "Construção de acordes",
                "Improvisação"
            ],
            "formação_acordes": [
                "Acompanhamento",
                "Arranjo",
                "Composição"
            ],
            "campo_harmonico": [
                "Análise de repertório",
                "Substituições harmônicas",
                "Modulação"
            ]
        }

        return applications_map.get(category, ["Aplicação geral em música popular"])

    def _create_error_response(self, message: str) -> Dict:
        """Cria resposta de erro padronizada"""
        return {
            "error": True,
            "message": message,
            "is_correct": False,
            "score": 0,
            "feedback": {"score_feedback": "Erro no processamento do exercício"}
        }

    def generate_exercise(self, category: str, level: int = 1, key: str = "C") -> Dict:
        """Gera novo exercício baseado nos parâmetros"""
        exercises = self.knowledge_base.get_exercise_by_level(level, category)

        if not exercises:
            return self._create_error_response("Categoria de exercício não encontrada")

        # Selecionar exercício aleatório da categoria
        import random
        exercise_template = random.choice(exercises)

        # Adaptar para tonalidade especificada se necessário
        adapted_exercise = self._adapt_exercise_to_key(exercise_template, key)

        return {
            "exercise_id": f"{category}_{level}_{key}",
            "category": category,
            "level": level,
            "key": key,
            "description": adapted_exercise.description,
            "example": adapted_exercise.example,
            "expected_answer": adapted_exercise.solution,
            "feedback_points": adapted_exercise.feedback_points,
            "guest_notes": self._get_guest_pedagogical_notes(adapted_exercise)
        }

    def _adapt_exercise_to_key(self, exercise: ExerciseTemplate, target_key: str) -> ExerciseTemplate:
        """Adapta exercício para uma tonalidade específica"""
        # Implementação simplificada - pode ser expandida
        if target_key == "C":
            return exercise

        # Aqui implementaríamos transposição real
        # Por agora, retorna o exercício original
        return exercise
