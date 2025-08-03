
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

# Imports dos serviços
from app.services.harmony_analyzer import HarmonyAnalyzerService
from app.services.exercise_corrector import ExerciseCorrectorService
from app.services.reharmonization_service import ReharmonizationService
from app.services.improvisation_consultant import ImprovisationConsultantService
from app.services.ai_chat_service import AIHarmonyAssistant

# Modelos Pydantic para requests/responses
class ProgressionAnalysisRequest(BaseModel):
    chord_symbols: List[str]
    key: str = "C"
    context: str = "tonal"

class ExerciseCorrectionRequest(BaseModel):
    exercise_type: str
    user_answer: str
    level: int = 1
    exercise_data: Optional[Dict] = None

class ReharmonizationRequest(BaseModel):
    chord_symbols: List[str]
    key: str = "C"
    style: str = "jazz"

class ImprovisationRequest(BaseModel):
    chord_symbols: List[str]
    key: str = "C"

class ChatMessage(BaseModel):
    message: str
    user_context: Optional[Dict] = None

class ChordAnalysisRequest(BaseModel):
    chord_symbol: str
    key: str = "C"

# Inicializar FastAPI app
app = FastAPI(
    title="E-harmony API",
    description="API para análise harmônica baseada na metodologia Ian Guest e Berklee College of Music",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
harmony_analyzer = HarmonyAnalyzerService()
exercise_corrector = ExerciseCorrectorService()
reharmonization_service = ReharmonizationService()
improvisation_consultant = ImprovisationConsultantService()
ai_assistant = AIHarmonyAssistant()

# Health check
@app.get("/")
async def root():
    return {
        "message": "E-harmony API - Mestre de Harmonia Musical",
        "version": "1.0.0",
        "status": "running",
        "methodology": "Ian Guest + Berklee College of Music"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": "all_operational"}

# ========== HARMONY ANALYSIS ENDPOINTS ==========
@app.post("/api/v1/analyze/progression")
async def analyze_progression(request: ProgressionAnalysisRequest):
    """Analisa progressão harmônica completa"""
    try:
        result = harmony_analyzer.analyze_progression(
            request.chord_symbols, 
            request.key, 
            request.context
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/analyze/chord")
async def analyze_chord(request: ChordAnalysisRequest):
    """Análise detalhada de um acorde específico"""
    try:
        result = harmony_analyzer.get_chord_detail(
            request.chord_symbol, 
            request.key
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== EXERCISE CORRECTION ENDPOINTS ==========
@app.post("/api/v1/exercises/correct")
async def correct_exercise(request: ExerciseCorrectionRequest):
    """Corrige exercício do usuário"""
    try:
        result = exercise_corrector.correct_exercise(
            request.exercise_type,
            request.user_answer,
            request.exercise_data,
            request.level
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/exercises/generate/{category}")
async def generate_exercise(category: str, level: int = 1, key: str = "C"):
    """Gera novo exercício"""
    try:
        result = exercise_corrector.generate_exercise(category, level, key)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== REHARMONIZATION ENDPOINTS ==========
@app.post("/api/v1/reharmonize")
async def suggest_reharmonizations(request: ReharmonizationRequest):
    """Sugere rearmonizações"""
    try:
        result = reharmonization_service.suggest_reharmonizations(
            request.chord_symbols,
            request.key,
            request.style
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== IMPROVISATION CONSULTANT ENDPOINTS ==========
@app.post("/api/v1/improvisation/guide")
async def get_improvisation_guide(request: ImprovisationRequest):
    """Guia de improvisação para progressão"""
    try:
        result = improvisation_consultant.get_improvisation_guide(
            request.chord_symbols,
            request.key
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== AI CHAT ENDPOINTS (PREMIUM) ==========
@app.post("/api/v1/chat/message")
async def chat_with_assistant(request: ChatMessage):
    """Chat com assistente de harmonia (Premium)"""
    try:
        result = ai_assistant.process_chat_message(
            request.message,
            request.user_context
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/chat/tip")
async def get_random_tip():
    """Dica aleatória do método Ian Guest"""
    try:
        tip = ai_assistant.get_random_tip()
        return {"success": True, "data": {"tip": tip}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/chat/exercises/{level}")
async def suggest_exercises(level: str):
    """Sugere exercícios por nível"""
    try:
        exercises = ai_assistant.suggest_exercises_for_level(level)
        return {"success": True, "data": {"exercises": exercises}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========== KNOWLEDGE BASE ENDPOINTS ==========
@app.get("/api/v1/knowledge/concepts")
async def get_concepts():
    """Lista conceitos disponíveis"""
    try:
        concepts = list(harmony_analyzer.knowledge_base.concepts.keys())
        return {"success": True, "data": {"concepts": concepts}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/knowledge/concept/{concept_name}")
async def get_concept_explanation(concept_name: str):
    """Explicação de conceito específico"""
    try:
        concept = harmony_analyzer.knowledge_base.get_concept_explanation(concept_name)
        if not concept:
            raise HTTPException(status_code=404, detail="Conceito não encontrado")

        return {"success": True, "data": {
            "concept": concept.concept,
            "explanation": concept.explanation,
            "volume": concept.volume,
            "examples": concept.examples,
            "related_concepts": concept.related_concepts
        }}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/knowledge/progressions")
async def get_common_progressions():
    """Progressões comuns da música popular"""
    try:
        progressions = harmony_analyzer.knowledge_base.progressions
        return {"success": True, "data": {"progressions": progressions}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para testar todas as funcionalidades
@app.post("/api/v1/demo/full-analysis")
async def full_demo_analysis():
    """Demo completo das funcionalidades"""
    try:
        # Progressão exemplo: ii-V-I em C
        demo_chords = ["Dm7", "G7", "CM7"]

        # Análise harmônica
        harmony_analysis = harmony_analyzer.analyze_progression(demo_chords, "C")

        # Sugestões de rearmonização
        reharmonization = reharmonization_service.suggest_reharmonizations(demo_chords, "C")

        # Guia de improvisação
        improvisation = improvisation_consultant.get_improvisation_guide(demo_chords, "C")

        # Exercício exemplo
        exercise = exercise_corrector.generate_exercise("campo_harmonico", 1, "C")

        return {
            "success": True,
            "data": {
                "demo_progression": demo_chords,
                "harmony_analysis": harmony_analysis,
                "reharmonization_suggestions": reharmonization,
                "improvisation_guide": improvisation,
                "sample_exercise": exercise,
                "message": "E-harmony funcionando completamente! Todas as funcionalidades implementadas."
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no demo: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
