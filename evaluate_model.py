"""
EMORA AI — Model Evaluation & Benchmark
=========================================
Tests both trained models on real-world examples.
Measures: Accuracy, F1, confusion matrix, empathy quality.

Usage:
  python evaluate_model.py \
    --emotion_model yourname/emora-emotion-classifier \
    --empathy_model yourname/emora-empathy-responder
"""

import argparse
import json
import torch
import numpy as np
from transformers import pipeline
from sklearn.metrics import classification_report, confusion_matrix

# ── TEST CASES ────────────────────────────────────────────────────────────────
EMOTION_TEST = [
    # (text, expected_emotion)
    ("I'm so happy today, got promoted!",                          "happiness"),
    ("I feel so alone, nobody cares about me",                     "loneliness"),
    ("I'm really anxious about my exam tomorrow",                  "anxiety"),
    ("Everything is falling apart, I can't go on",                 "crisis"),
    ("I'm so grateful for my friends, they make life beautiful",   "gratitude"),
    ("My boss is driving me crazy, I'm so stressed and burnt out", "stress"),
    ("I've been crying all day, I feel so sad and empty",          "sadness"),
    ("I'm furious at what they did, this is so unfair",            "anger"),
    ("Just a regular Tuesday, nothing special",                    "neutral"),
    ("I want to hurt myself, I don't see any way out",             "crisis"),
    ("I'm overwhelmed with deadlines, no time to breathe",         "stress"),
    ("Feeling lonely even in a crowd, nobody really knows me",     "loneliness"),
    ("My anxiety is through the roof, I can't stop worrying",      "anxiety"),
    ("I got into my dream university! I'm so excited!",            "happiness"),
    ("Thank you so much for being there for me",                   "gratitude"),
]

EMPATHY_TEST = [
    "I've been feeling really down lately",
    "I'm so scared about my health results",
    "Nobody understands what I'm going through",
    "I just had the best day of my life",
    "I'm exhausted and can't keep going like this",
]

LABEL_NAMES = [
    "neutral","happiness","sadness","anger",
    "anxiety","stress","loneliness","gratitude","crisis"
]


def evaluate_emotion_model(model_name):
    print(f"\n{'='*60}")
    print(f"🧠 EMOTION CLASSIFIER EVALUATION")
    print(f"   Model: {model_name}")
    print(f"{'='*60}\n")

    try:
        classifier = pipeline(
            "text-classification",
            model=model_name,
            device=0 if torch.cuda.is_available() else -1,
        )
    except Exception as e:
        print(f"❌ Could not load emotion model: {e}")
        return

    texts    = [t for t, _ in EMOTION_TEST]
    expected = [e for _, e in EMOTION_TEST]
    predicted = []

    print(f"{'Input':<50} {'Expected':<12} {'Predicted':<12} {'✓'}")
    print("-" * 80)

    correct = 0
    for text, exp in EMOTION_TEST:
        result = classifier(text, truncation=True, max_length=128)[0]
        pred   = result["label"].lower()
        score  = result["score"]
        ok     = "✅" if pred == exp else "❌"
        if pred == exp: correct += 1
        print(f"{text[:48]:<50} {exp:<12} {pred:<12} {ok} ({score:.2f})")
        predicted.append(pred)

    accuracy = correct / len(EMOTION_TEST)
    print(f"\n📊 Accuracy: {accuracy:.1%} ({correct}/{len(EMOTION_TEST)})")

    # Detailed report
    print("\n📈 Classification Report:")
    print(classification_report(expected, predicted, zero_division=0))


def evaluate_empathy_model(model_name):
    print(f"\n{'='*60}")
    print(f"💬 EMPATHY RESPONSE EVALUATION")
    print(f"   Model: {model_name}")
    print(f"{'='*60}\n")

    try:
        responder = pipeline(
            "text2text-generation",
            model=model_name,
            device=0 if torch.cuda.is_available() else -1,
        )
    except Exception as e:
        print(f"❌ Could not load empathy model: {e}")
        return

    QUALITIES = ["Empathetic?", "Human-like?", "Relevant?"]

    for text in EMPATHY_TEST:
        result = responder(text, max_new_tokens=120, num_beams=4, early_stopping=True)[0]
        response = result["generated_text"]
        print(f"\n👤 User: {text}")
        print(f"🤖 Emora: {response}")
        # Word count quality check
        words = len(response.split())
        print(f"   [Words: {words} | {'Good length ✅' if 20 <= words <= 150 else '⚠️ Too short/long'}]")

    print("\n⚠️  Manual quality review recommended for empathy responses.")
    print("    Rate each response on: empathy, naturalness, relevance (1-5)")


def run_inference_speed_test(model_name):
    print(f"\n{'='*60}")
    print(f"⚡ INFERENCE SPEED TEST")
    print(f"{'='*60}")
    import time
    try:
        clf = pipeline("text-classification", model=model_name, device=-1)
        texts = ["I feel anxious"] * 10
        start = time.time()
        for t in texts:
            clf(t)
        elapsed = (time.time() - start) / len(texts)
        print(f"  Average inference time: {elapsed*1000:.1f}ms per sample")
        if elapsed < 0.1:
            print("  ✅ Production-ready speed")
        elif elapsed < 0.5:
            print("  ⚠️  Acceptable for low-traffic (consider ONNX export for speed)")
        else:
            print("  ❌ Too slow — use distilled model or ONNX")
    except Exception as e:
        print(f"  ❌ Speed test failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Emora AI Models")
    parser.add_argument("--emotion_model", type=str,
                        default="j-hartmann/emotion-english-distilroberta-base",
                        help="HuggingFace emotion model name")
    parser.add_argument("--empathy_model", type=str,
                        default="facebook/blenderbot-400M-distill",
                        help="HuggingFace empathy response model name")
    args = parser.parse_args()

    evaluate_emotion_model(args.emotion_model)
    evaluate_empathy_model(args.empathy_model)
    run_inference_speed_test(args.emotion_model)

    print(f"\n{'='*60}")
    print("✅ Evaluation complete!")
    print(f"{'='*60}\n")
