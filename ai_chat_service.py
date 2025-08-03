
from typing import List, Dict, Optional, Any
import json
from ..core.music_theory_engine import MusicTheoryEngine
from ..knowledge_base.ian_guest_kb import IanGuestKnowledgeBase
from ..services.harmony_analyzer import HarmonyAnalyzerService
from ..services.exercise_corrector import ExerciseCorrectorService

class AIHarmonyAssistant:
    def __init__(self):
        self.theory_engine = MusicTheoryEngine()
        self.knowledge_base = IanGuestKnowledgeBase()
        self.harmony_analyzer = HarmonyAnalyzerService()
        self.exercise_corrector = ExerciseCorrectorService()

        # Base de conhecimento para chat
        self.chat_knowledge = self._init_chat_knowledge_base()

    def process_chat_message(self, message: str, user_context: Dict = None) -> Dict[str, Any]:
        """Processa mensagem do usuário e retorna resposta inteligente"""

        # Análise da intenção do usuário
        intent = self._analyze_user_intent(message)

        # Processamento específico por tipo de pergunta
        if intent["type"] == "harmony_analysis":
            return self._handle_harmony_question(message, intent)
        elif intent["type"] == "exercise_help":
            return self._handle_exercise_question(message, intent)
        elif intent["type"] == "concept_explanation":
            return self._handle_concept_question(message, intent)
        elif intent["type"] == "practice_advice":
            return self._handle_practice_question(message, intent)
        elif intent["type"] == "general_theory":
            return self._handle_theory_question(message, intent)
        else:
            return self._handle_general_question(message, intent)

    def _init_chat_knowledge_base(self) -> Dict:
        """Inicializa base de conhecimento para chat"""
        return {
            "greeting_responses": [
                "Olá! Sou seu assistente de harmonia baseado na metodologia Ian Guest. Como posso ajudar?",
                "Oi! Estou aqui para esclarecer suas dúvidas sobre harmonia. Qual é sua pergunta?",
                "Bem-vindo ao plantão de dúvidas! Sou especialista no método Ian Guest. No que posso auxiliar?"
            ],

            "common_questions": {
                "como formar acordes": {
                    "response": "Para formar acordes, comece com a tríade básica: fundamental + 3ª + 5ª. No método Ian Guest (Volume 1), aprendemos que um acorde maior tem 3ª maior, e menor tem 3ª menor.",
                    "follow_up": ["Quer que eu analise um acorde específico?", "Precisa de ajuda com inversões?"]
                },

                "o que são tensões": {
                    "response": "Tensões são notas adicionadas aos acordes básicos (9ª, 11ª, 13ª). Ian Guest explica no Volume 1 que elas dão 'cor' aos acordes sem alterar sua função básica.",
                    "follow_up": ["Quer saber quais tensões usar em cada acorde?", "Precisa de exemplos práticos?"]
                },

                "como analisar progressões": {
                    "response": "Análise harmônica segue passos: 1) Identifique a tonalidade, 2) Determine os graus, 3) Classifique as funções (T-S-D). Ian Guest enfatiza entender FUNÇÃO antes de decorar cifras.",
                    "follow_up": ["Tem alguma progressão específica para analisar?", "Quer revisar funções harmônicas?"]
                }
            },

            "ian_guest_quotes": [
                ""A harmonia é a base de tudo na música popular" - Ian Guest",
                ""Primeiro entenda a função, depois aprenda a cifra" - Ian Guest", 
                ""Pratique sempre com musicalidade, nunca mecanicamente" - Ian Guest"
            ]
        }

    def _analyze_user_intent(self, message: str) -> Dict:
        """Analisa intenção do usuário na mensagem"""
        message_lower = message.lower()

        # Keywords para identificar tipos de pergunta
        keywords_map = {
            "harmony_analysis": ["analise", "progressão", "acorde", "campo harmônico", "função"],
            "exercise_help": ["exercício", "correção", "resposta", "como resolver", "ajuda"],
            "concept_explanation": ["o que é", "explique", "conceito", "definição", "teoria"],
            "practice_advice": ["como praticar", "estudar", "dica", "método", "técnica"],
            "general_theory": ["intervalo", "escala", "modo", "tensão", "substituição"]
        }

        # Detectar acordes na mensagem
        chords_found = self._extract_chords_from_message(message)

        # Classificar intenção
        intent_scores = {}
        for intent_type, keywords in keywords_map.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent_type] = score

        # Determinar intenção principal
        if intent_scores:
            main_intent = max(intent_scores, key=intent_scores.get)
        else:
            main_intent = "general_question"

        return {
            "type": main_intent,
            "confidence": intent_scores.get(main_intent, 0),
            "chords_mentioned": chords_found,
            "message_length": len(message.split())
        }

    def _extract_chords_from_message(self, message: str) -> List[str]:
        """Extrai acordes mencionados na mensagem"""
        import re

        # Pattern para acordes comuns
        chord_pattern = r'\b([A-G][#b]?(?:m|maj|dim|aug)?(?:7|9|11|13)?(?:/[A-G][#b]?)?)\b'
        potential_chords = re.findall(chord_pattern, message)

        valid_chords = []
        for chord in potential_chords:
            try:
                # Tentar parsear para validar
                self.theory_engine.parse_chord(chord)
                valid_chords.append(chord)
            except:
                continue

        return valid_chords

    def _handle_harmony_question(self, message: str, intent: Dict) -> Dict:
        """Lida com perguntas sobre análise harmônica"""
        chords = intent["chords_mentioned"]

        if chords:
            # Fazer análise automática
            try:
                analysis = self.harmony_analyzer.analyze_progression(chords)

                response_text = f"Análise da progressão {' - '.join(chords)}:\n\n"

                for i, chord_data in enumerate(analysis["analysis"]):
                    chord_symbol = chords[i]
                    roman = chord_data["roman_numeral"]
                    function = chord_data["function"]

                    response_text += f"• {chord_symbol}: {roman} (função {function})\n"

                response_text += f"\nTonalidade sugerida: {analysis['key']}"
                response_text += f"\nNível: {analysis['pedagogical_notes'][0] if analysis['pedagogical_notes'] else 'Básico'}"

                return {
                    "response": response_text,
                    "type": "harmony_analysis",
                    "analysis_data": analysis,
                    "follow_up_suggestions": [
                        "Quer sugestões de rearmonização?",
                        "Precisa de ajuda com escalas para improvisação?",
                        "Tem dúvidas sobre algum acorde específico?"
                    ]
                }

            except Exception as e:
                return {
                    "response": f"Detectei os acordes {', '.join(chords)}, mas preciso de mais contexto. Pode especificar a tonalidade ou me dar mais detalhes sobre sua dúvida?",
                    "type": "clarification_needed",
                    "error": str(e)
                }
        else:
            return {
                "response": "Para análise harmônica, preciso que você me informe os acordes! Exemplo: 'Analise a progressão C - Am - F - G'. Posso ajudar com funções, graus romanos e sugestões de estudo.",
                "type": "instruction",
                "follow_up_suggestions": [
                    "Me diga os acordes da progressão",
                    "Quer revisar como identificar graus?",
                    "Precisa de ajuda com campo harmônico?"
                ]
            }

    def _handle_exercise_question(self, message: str, intent: Dict) -> Dict:
        """Lida com perguntas sobre exercícios"""
        return {
            "response": "Estou aqui para ajudar com exercícios! Posso corrigir respostas, explicar conceitos ou gerar novos exercícios. Me diga: qual tipo de exercício (intervalos, acordes, campo harmônico) e seu nível (1-3)?",
            "type": "exercise_help",
            "follow_up_suggestions": [
                "Exercícios de intervalos (nível básico)",
                "Formação de acordes (nível intermediário)", 
                "Campo harmônico (nível avançado)",
                "Correção de exercício específico"
            ]
        }

    def _handle_concept_question(self, message: str, intent: Dict) -> Dict:
        """Lida com perguntas conceituais"""
        message_lower = message.lower()

        # Mapear conceitos comuns
        concept_responses = {
            "tensão": {
                "explanation": "Tensões são notas que adicionamos aos acordes básicos para criar 'cor' harmônica. São a 9ª, 11ª e 13ª. Ian Guest ensina que devemos dominar o acorde básico antes de adicionar tensões.",
                "volume": "Volume 1 - p. 86-95",
                "example": "Em C7: tensões disponíveis são D(9ª), F(11ª) e A(13ª)"
            },
            "função harmônica": {
                "explanation": "Funções harmônicas são T (tônica/repouso), S (subdominante/preparação) e D (dominante/tensão). Ian Guest sempre ensina: entenda a FUNÇÃO antes de decorar a cifra!",
                "volume": "Volume 1 - p. 96-110",
                "example": "Em C maior: C=T, F=S, G=D"
            },
            "substituto tritonal": {
                "explanation": "Substituto tritonal substitui um dominante por outro dominante a um trítono de distância. Mantém a tensão mas cria movimento cromático no baixo.",
                "volume": "Volume 2 - p. 46-60", 
                "example": "G7 → C pode ser Db7 → C"
            }
        }

        # Procurar conceito mencionado
        for concept, data in concept_responses.items():
            if concept in message_lower:
                return {
                    "response": f"{data['explanation']}\n\nReferência: {data['volume']}\nExemplo: {data['example']}",
                    "type": "concept_explanation",
                    "concept": concept,
                    "follow_up_suggestions": [
                        f"Quer exercícios sobre {concept}?",
                        "Precisa de mais exemplos?",
                        "Tem outras dúvidas conceituais?"
                    ]
                }

        # Resposta genérica se não encontrar conceito específico
        return {
            "response": "Posso explicar vários conceitos! Alguns dos mais importantes: tensões, funções harmônicas, substitutos, modos, empréstimo modal. Sobre qual conceito específico você quer saber?",
            "type": "concept_help",
            "follow_up_suggestions": [
                "Tensões disponíveis",
                "Funções harmônicas (T-S-D)",
                "Substitutos tritonais",
                "Modos gregos"
            ]
        }

    def _handle_practice_question(self, message: str, intent: Dict) -> Dict:
        """Lida com perguntas sobre prática"""
        practice_advice = {
            "geral": [
                "Ian Guest sempre diz: 'Pratique com musicalidade, nunca mecanicamente'",
                "Comece sempre pelo básico: tríades antes de acordes com 7ª",
                "Pratique em todas as tonalidades, mas devagar",
                "Escute muito - a harmonia deve ser ouvida, não só tocada"
            ],

            "acordes": [
                "Sequência Ian Guest: 1) Tríade básica, 2) Inversões, 3) Sétima, 4) Tensões",
                "Pratique as 4 inversões de cada acorde de 7ª",
                "Use metrônomo sempre, mesmo para estudar harmonia",
                "Aplique em repertório - escolha uma música simples"
            ],

            "progressões": [
                "Analise antes de tocar - identifique as funções",
                "Pratique ii-V-I em todas as tonalidades",
                "Comece devagar, focando na condução de vozes",
                "Experimente diferentes ritmos sobre a mesma progressão"
            ]
        }

        # Determinar tipo de prática
        message_lower = message.lower()
        if "acorde" in message_lower:
            advice_type = "acordes"
        elif "progressão" in message_lower:
            advice_type = "progressões"
        else:
            advice_type = "geral"

        selected_advice = practice_advice[advice_type]

        return {
            "response": f"Dicas de prática ({advice_type}):\n\n" + "\n".join(f"• {tip}" for tip in selected_advice),
            "type": "practice_advice",
            "follow_up_suggestions": [
                "Quer um plano de estudos específico?",
                "Precisa de exercícios práticos?",
                "Tem dúvidas sobre repertório?"
            ]
        }

    def _handle_theory_question(self, message: str, intent: Dict) -> Dict:
        """Lida com perguntas teóricas gerais"""
        return {
            "response": "Sou especialista em teoria harmônica baseada no método Ian Guest! Posso ajudar com: intervalos, escalas, acordes, funções harmônicas, modos, tensões, substitutos e muito mais. Qual tópico específico te interessa?",
            "type": "theory_help",
            "follow_up_suggestions": [
                "Como formar acordes",
                "Análise de progressões",
                "Tensões disponíveis",
                "Substitutos harmônicos"
            ]
        }

    def _handle_general_question(self, message: str, intent: Dict) -> Dict:
        """Lida com perguntas gerais"""
        # Respostas para saudações
        greetings = ["oi", "olá", "hello", "bom dia", "boa tarde", "boa noite"]
        if any(greeting in message.lower() for greeting in greetings):
            import random
            greeting_response = random.choice(self.chat_knowledge["greeting_responses"])
            return {
                "response": greeting_response,
                "type": "greeting",
                "follow_up_suggestions": [
                    "Analisar uma progressão harmônica",
                    "Corrigir um exercício",
                    "Tirar dúvidas sobre conceitos",
                    "Dicas de prática"
                ]
            }

        # Resposta genérica
        return {
            "response": "Estou aqui para ajudar com harmonia! Posso analisar progressões, corrigir exercícios, explicar conceitos e dar dicas de prática. Baseio minhas respostas na metodologia Ian Guest e princípios da Berklee. Como posso ajudar?",
            "type": "general_help",
            "follow_up_suggestions": [
                "Me conte sua dúvida específica",
                "Quer analisar uma progressão?",
                "Precisa de ajuda com exercícios?",
                "Tem dúvidas conceituais?"
            ]
        }

    def get_random_tip(self) -> str:
        """Retorna dica aleatória baseada no método Ian Guest"""
        import random

        tips = [
            "Dica do Ian Guest: 'Sempre pratique as inversões - elas são fundamentais para uma boa condução de vozes'",
            "Lembre-se: função harmônica é mais importante que a cifra. Entenda T-S-D primeiro!",
            "Ian Guest recomenda: pratique ii-V-I em todas as tonalidades - é a base do jazz e bossa nova",
            "Para tensões: comece pela 9ª (é a mais suave), depois 13ª, e por último 11ª",
            "Estude com repertório! Escolha uma música simples e aplique os conceitos teóricos"
        ]

        return random.choice(tips)

    def suggest_exercises_for_level(self, user_level: str) -> List[Dict]:
        """Sugere exercícios baseados no nível do usuário"""
        level_map = {"básico": 1, "intermediário": 2, "avançado": 3}
        level_num = level_map.get(user_level.lower(), 1)

        exercise_categories = [
            "identificação_intervalos",
            "formação_acordes", 
            "campo_harmonico",
            "emprestimo_modal",
            "dominantes_secundarios",
            "rearmonizacao"
        ]

        suggestions = []
        for category in exercise_categories[:level_num + 1]:  # Limita por nível
            exercise = self.exercise_corrector.generate_exercise(category, level_num)
            if not exercise.get("error"):
                suggestions.append({
                    "category": category,
                    "description": exercise["description"],
                    "level": level_num
                })

        return suggestions
