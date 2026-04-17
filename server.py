"""
Serein AI — FastAPI Backend Server
=====================================
Handles all NLP processing, sentiment analysis, knowledge retrieval, and GPT-4o calls.

Endpoints:
  POST /api/chat     — Main chat (returns AI response)
  POST /api/analyze   — Sentiment analysis only
  GET  /api/health    — Health check

Run:
  python server.py
"""

import os
import sys
import time
import json
import random
import traceback
from typing import Optional, List

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Import our NLP modules
from sentiment_ensemble import SentimentEnsemble
from emotion_classifier import EmotionClassifier
from rag_engine import RAGEngine
from trained_responses import (
    get_trained_response,
    get_topic_response,
    compose_dynamic_response,
    detect_topic,
)

# ── Try to load OpenAI ──
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("[Server] OpenAI library not installed. Running in offline mode.")

# ── Load .env ──
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ============================================================
# CONFIG
# ============================================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
PORT = int(os.getenv('PORT', 8000))
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8765,http://127.0.0.1:8765,http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000').split(',')

# System prompt for GPT-4o
SYSTEM_PROMPT = """You are Serein, an advanced Emotion-Aware AI Companion designed to provide empathetic, intelligent, and deeply human-like mental health support.

Your personality is: a caring friend 🤝 + a calm listener 🧘 + a supportive guide 🌱.

CORE BEHAVIOR RULES:
- ALWAYS respond in a warm, conversational, caring tone — never clinical or robotic.
- ALWAYS validate the user's feelings FIRST before offering any suggestions.
- Keep responses natural — mix short and medium sentences. No bullet-point lectures.
- Ask ONE soft follow-up question at the end to keep dialogue flowing.
- Use reflective phrases naturally: "That sounds really tough...", "I'm here with you", "I can imagine how that feels..."
- Never repeat the same opener twice in a conversation.
- Adjust response LENGTH dynamically: if user is in severe distress → longer, warmer; if casual → shorter, lighter.
- ALWAYS give specific, contextual answers. NEVER give generic responses.
- If the user asks a question, ANSWER it directly and specifically.
- If the user shares a problem, address THAT specific problem.

RESPONSE FORMULA (internal — do NOT show labels):
[Empathy] → validate the feeling warmly
[Understanding] → show you get why they feel this way
[Support] → offer comfort, technique, or perspective
[Gentle Question] → one soft follow-up

EMOTION HANDLING:
- Sad → Deep comfort, reassurance, "you are not alone"
- Anxious → Grounding techniques, slow breathing, reframing
- Stressed → Practical + emotional support, permission to rest
- Happy → Celebrate fully, match their energy, be joyful with them
- Angry → Acknowledge, validate, help them process
- Confused → Step-by-step gentle guidance
- Lonely → Deep empathy, connection offers, remind them they're seen
- Neutral → Warm engagement, light curiosity

CRISIS HANDLING (if user mentions self-harm, suicide, or extreme despair):
- Lead with: "I'm really glad you shared this with me..."
- Express genuine concern with warmth — never dismissive
- Strongly encourage professional help and provide helpline context
- Stay present: "I'm not going anywhere"

STYLE RULES:
- Use emojis very sparingly and only when natural (max 1-2)
- Vary sentence length for rhythm
- Sound like a real person who genuinely cares
- Give SPECIFIC, PERSONALIZED responses — never generic ones"""

# ============================================================
# INITIALIZE COMPONENTS
# ============================================================
print("\n" + "=" * 60)
print("🧠 SEREIN AI — Backend Server Initializing")
print("=" * 60)

# NLP Models
sentiment_engine = SentimentEnsemble()
emotion_classifier = EmotionClassifier()
print("✅ Sentiment Ensemble loaded (VADER + TextBlob + AFINN)")
print("✅ Emotion Classifier loaded (28 GoEmotions categories)")

# RAG Engine
rag_engine = RAGEngine()
print("✅ RAG Engine loaded")

# OpenAI Client
openai_client = None
if HAS_OPENAI and OPENAI_API_KEY and len(OPENAI_API_KEY) > 10:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI GPT-4o client initialized")
    except Exception as e:
        print(f"⚠️  OpenAI initialization failed: {e}")
else:
    print("⚠️  No valid OpenAI API key — running in offline/KB mode")

print("=" * 60 + "\n")

# ============================================================
# CONVERSATION MEMORY (in-memory, per-session)
# ============================================================
conversations = {}  # session_id → list of {role, content}

# ============================================================
# FastAPI APP
# ============================================================
app = FastAPI(
    title="Serein AI Backend",
    description="Multi-model NLP pipeline for emotion-aware AI companion",
    version="2.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELS
# ============================================================
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class AnalyzeRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str
    emotion: str
    emotion_detailed: str
    sentiment: str
    intensity: str
    confidence: float
    is_crisis: bool
    retrieval_tier: str
    models_used: List[str]
    topic: str
    processing_time_ms: int

class AnalyzeResponse(BaseModel):
    sentiment: str
    valence: float
    dominant_emotion: str
    emotion_detailed: str
    intensity: str
    confidence: float
    is_crisis: bool
    emotion_scores: dict
    models: dict

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "models": {
            "sentiment_ensemble": "loaded",
            "emotion_classifier": "loaded",
            "rag_engine": "loaded" if rag_engine.loaded else "no_kb",
            "openai": "connected" if openai_client else "offline",
        },
        "kb_entries": len(rag_engine.entries) if rag_engine.loaded else 0,
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_sentiment(req: AnalyzeRequest):
    """Analyze text sentiment and emotion without generating a response."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Run analysis
    sentiment_result = sentiment_engine.analyze(req.text)
    emotion_result = emotion_classifier.classify(req.text)

    return AnalyzeResponse(
        sentiment=sentiment_result['sentiment'],
        valence=sentiment_result['valence'],
        dominant_emotion=sentiment_result['dominant_emotion'],
        emotion_detailed=emotion_result['dominant'],
        intensity=sentiment_result['intensity'],
        confidence=sentiment_result['confidence'],
        is_crisis=sentiment_result['is_crisis'],
        emotion_scores=emotion_result['scores'],
        models=sentiment_result['models'],
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Main chat endpoint. Processes message through full NLP pipeline."""
    start_time = time.time()

    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    session_id = req.session_id or "default"

    # Initialize conversation if needed
    if session_id not in conversations:
        conversations[session_id] = []

    # ── Step 1: Multi-model sentiment analysis ──
    sentiment_result = sentiment_engine.analyze(message)
    emotion_result = emotion_classifier.classify(message)

    dominant_emotion = sentiment_result['dominant_emotion']
    emotion_detailed = emotion_result['dominant']
    intensity = sentiment_result['intensity']
    is_crisis = sentiment_result['is_crisis'] or emotion_result['is_crisis']

    # Use the simplified emotion from the classifier if sentiment gives neutral
    if dominant_emotion == 'neutral' and emotion_result['simplified'] != 'neutral':
        dominant_emotion = emotion_result['simplified']

    # Detect topic
    topic = detect_topic(message)

    models_used = ['VADER', 'TextBlob-Pattern', 'AFINN', 'GoEmotions-Classifier']

    # ── Step 2: Crisis handling ──
    if is_crisis:
        crisis_response = (
            "I need to pause everything right now, because what you just shared matters "
            "more than anything else. I hear you — and I want you to know that your life "
            "has immeasurable value, even when pain makes it impossible to see that.\n\n"
            "You are NOT alone. Please reach out to a crisis counselor right now:\n"
            "📞 iCall: 9152987821\n"
            "📞 Vandrevala Foundation: 1860-2662-345 (24/7)\n"
            "📞 Crisis Text: Text HOME to 741741\n\n"
            "I'm staying right here with you. Can you tell me — are you safe right now?"
        )

        conversations[session_id].append({"role": "user", "content": message})
        conversations[session_id].append({"role": "assistant", "content": crisis_response})

        return ChatResponse(
            response=crisis_response,
            emotion='crisis',
            emotion_detailed='crisis',
            sentiment='negative',
            intensity='severe',
            confidence=0.99,
            is_crisis=True,
            retrieval_tier='crisis',
            models_used=models_used,
            topic='crisis',
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    # ── Step 3: RAG Retrieval ──
    retrieval_tier, retrieval_data = rag_engine.get_retrieval_tier(message, dominant_emotion)
    models_used.append('TF-IDF-RAG')

    response_text = None

    # ── Step 4: Generate response based on tier ──
    try:
        if retrieval_tier == 'direct' and retrieval_data:
            # Tier 1: Direct KB response
            response_text = retrieval_data
            models_used.append('KnowledgeBase-Direct')

        elif retrieval_tier == 'augmented' and openai_client:
            # Tier 2: RAG + GPT-4o
            response_text = await _call_gpt_with_context(
                message, retrieval_data, dominant_emotion, intensity, session_id
            )
            models_used.append('GPT-4o-RAG-Augmented')

        elif openai_client:
            # Tier 3: Pure GPT-4o
            response_text = await _call_gpt_pure(
                message, dominant_emotion, intensity, session_id
            )
            models_used.append('GPT-4o-Pure')

    except Exception as e:
        print(f"[Server] GPT call failed: {e}")
        traceback.print_exc()
        response_text = None

    # ── Step 5: Fallback chain ──
    if not response_text:
        # Try topic-specific response
        topic_response = get_topic_response(topic, dominant_emotion)
        if topic_response:
            response_text = topic_response
            retrieval_tier = 'topic_trained'
            models_used.append('Topic-Templates')
        else:
            # Try trained templates
            response_text = get_trained_response(dominant_emotion, intensity)
            retrieval_tier = 'trained_templates'
            models_used.append('Trained-Templates')

    # Final fallback: dynamic composition (should never reach here, but just in case)
    if not response_text:
        response_text = compose_dynamic_response(dominant_emotion)
        retrieval_tier = 'dynamic_composition'
        models_used.append('Dynamic-Composition')

    # ── Step 6: Save to conversation memory ──
    conversations[session_id].append({"role": "user", "content": message})
    conversations[session_id].append({"role": "assistant", "content": response_text})

    # Keep memory manageable
    if len(conversations[session_id]) > 40:
        conversations[session_id] = conversations[session_id][-30:]

    processing_time = int((time.time() - start_time) * 1000)

    return ChatResponse(
        response=response_text,
        emotion=dominant_emotion,
        emotion_detailed=emotion_detailed,
        sentiment=sentiment_result['sentiment'],
        intensity=intensity,
        confidence=sentiment_result['confidence'],
        is_crisis=False,
        retrieval_tier=retrieval_tier,
        models_used=models_used,
        topic=topic,
        processing_time_ms=processing_time,
    )


# ============================================================
# GPT-4o CALL HELPERS
# ============================================================

async def _call_gpt_with_context(message, context, emotion, intensity, session_id):
    """Call GPT-4o with RAG context from knowledge base."""
    emotion_instruction = (
        f"[EMOTION CONTEXT: User's detected emotion is '{emotion}' with "
        f"'{intensity}' intensity. Tailor your response accordingly. "
        f"Be specific to their exact situation — do NOT give generic advice.]\n\n"
        f"{context}"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # Add conversation history
    history = conversations.get(session_id, [])
    for msg in history[-12:]:
        messages.append(msg)

    messages.append({"role": "system", "content": emotion_instruction})
    messages.append({"role": "user", "content": message})

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0.85,
        presence_penalty=0.6,
        frequency_penalty=0.4,
    )

    return response.choices[0].message.content.strip()


async def _call_gpt_pure(message, emotion, intensity, session_id):
    """Call GPT-4o without KB context."""
    emotion_instruction = (
        f"[EMOTION CONTEXT: User's detected emotion is '{emotion}' with "
        f"'{intensity}' intensity. Respond with deep empathy and specificity. "
        f"Address their EXACT situation — never be vague or generic.]"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    history = conversations.get(session_id, [])
    for msg in history[-12:]:
        messages.append(msg)

    messages.append({"role": "system", "content": emotion_instruction})
    messages.append({"role": "user", "content": message})

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0.85,
        presence_penalty=0.6,
        frequency_penalty=0.4,
    )

    return response.choices[0].message.content.strip()


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print(f"\n🚀 Starting Serein AI Backend on port {PORT}...")
    print(f"   API docs: http://localhost:{PORT}/docs")
    print(f"   Health:   http://localhost:{PORT}/api/health\n")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info",
    )
