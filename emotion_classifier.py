"""
Serein AI — Fine-Grained Emotion Classifier
=============================================
GoEmotions-inspired 28-category emotion classification.
Uses weighted keyword matching, phrase detection, and contextual analysis.
"""

import re
from collections import Counter


class EmotionClassifier:
    """
    Classifies text into 28 fine-grained emotion categories (GoEmotions taxonomy).
    Uses multi-signal detection: keywords, phrases, patterns, context.
    """

    # GoEmotions-based taxonomy with weighted keywords and phrases
    EMOTION_TAXONOMY = {
        'admiration': {
            'keywords': ['admire', 'impressed', 'amazing', 'incredible', 'inspiring', 'respect', 'brilliant', 'outstanding', 'remarkable', 'extraordinary'],
            'phrases': ['so talented', 'really impressive', 'blown away', 'in awe', 'look up to'],
            'weight': 1.0,
        },
        'amusement': {
            'keywords': ['funny', 'hilarious', 'laughing', 'lol', 'haha', 'humor', 'comedy', 'joke', 'lmao', 'rofl'],
            'phrases': ['made me laugh', 'so funny', 'cracking up', 'died laughing'],
            'weight': 1.0,
        },
        'anger': {
            'keywords': ['angry', 'furious', 'rage', 'mad', 'livid', 'pissed', 'outraged', 'infuriated', 'enraged', 'fuming', 'hostile', 'hateful'],
            'phrases': ['so angry', 'makes me mad', 'drives me crazy', 'fed up with', 'sick and tired', 'can\'t stand', 'blood boiling'],
            'weight': 1.5,
        },
        'annoyance': {
            'keywords': ['annoyed', 'annoying', 'irritated', 'irritating', 'bothered', 'pestering', 'nagging', 'ugh', 'grrr'],
            'phrases': ['getting on my nerves', 'driving me nuts', 'so annoying', 'can\'t deal'],
            'weight': 1.0,
        },
        'approval': {
            'keywords': ['agree', 'approve', 'support', 'endorse', 'correct', 'right', 'exactly', 'absolutely', 'definitely'],
            'phrases': ['well done', 'good job', 'nice work', 'i agree', 'you\'re right'],
            'weight': 0.8,
        },
        'caring': {
            'keywords': ['care', 'caring', 'concerned', 'worry', 'protect', 'nurture', 'comfort', 'support'],
            'phrases': ['i care about', 'are you okay', 'how are you', 'take care', 'be careful', 'worried about you'],
            'weight': 1.0,
        },
        'confusion': {
            'keywords': ['confused', 'confusing', 'puzzled', 'baffled', 'perplexed', 'bewildered', 'lost', 'unsure', 'uncertain'],
            'phrases': ['don\'t understand', 'makes no sense', 'i\'m lost', 'what do you mean', 'not sure what', 'hard to understand'],
            'weight': 1.0,
        },
        'curiosity': {
            'keywords': ['curious', 'wondering', 'interested', 'intrigued', 'fascinated', 'question'],
            'phrases': ['i wonder', 'tell me more', 'how does', 'what is', 'why does', 'i want to know'],
            'weight': 0.8,
        },
        'desire': {
            'keywords': ['want', 'wish', 'crave', 'desire', 'longing', 'yearning', 'need', 'dream'],
            'phrases': ['i wish', 'i want', 'if only', 'i dream of', 'i long for', 'i need'],
            'weight': 0.9,
        },
        'disappointment': {
            'keywords': ['disappointed', 'disappointing', 'letdown', 'underwhelming', 'bummer', 'sucks'],
            'phrases': ['let me down', 'expected more', 'not what i hoped', 'fell short', 'what a waste'],
            'weight': 1.2,
        },
        'disapproval': {
            'keywords': ['disagree', 'disapprove', 'wrong', 'unacceptable', 'inappropriate', 'terrible'],
            'phrases': ['that\'s wrong', 'not okay', 'shouldn\'t have', 'don\'t think so', 'not right'],
            'weight': 1.0,
        },
        'disgust': {
            'keywords': ['disgusted', 'disgusting', 'gross', 'revolting', 'repulsive', 'nauseating', 'vile', 'sick'],
            'phrases': ['makes me sick', 'so gross', 'can\'t stomach'],
            'weight': 1.2,
        },
        'embarrassment': {
            'keywords': ['embarrassed', 'embarrassing', 'humiliated', 'mortified', 'awkward', 'cringe'],
            'phrases': ['so embarrassing', 'wanted to disappear', 'died of embarrassment', 'so awkward'],
            'weight': 1.1,
        },
        'excitement': {
            'keywords': ['excited', 'exciting', 'thrilled', 'pumped', 'hyped', 'stoked', 'ecstatic', 'elated', 'exhilarated'],
            'phrases': ['can\'t wait', 'so excited', 'looking forward', 'this is amazing', 'hell yeah'],
            'weight': 1.2,
        },
        'fear': {
            'keywords': ['scared', 'frightened', 'terrified', 'afraid', 'fearful', 'petrified', 'horrified', 'phobia'],
            'phrases': ['i\'m scared', 'freaking out', 'scares me', 'frightened of', 'terrified of', 'give me chills'],
            'weight': 1.5,
        },
        'gratitude': {
            'keywords': ['grateful', 'thankful', 'appreciate', 'thanks', 'thank', 'blessing', 'blessed'],
            'phrases': ['thank you', 'so grateful', 'really appreciate', 'means a lot', 'couldn\'t have done it without'],
            'weight': 1.0,
        },
        'grief': {
            'keywords': ['grief', 'grieving', 'mourning', 'bereaved', 'loss', 'passed away', 'died'],
            'phrases': ['lost someone', 'passed away', 'miss them', 'can\'t believe they\'re gone', 'life without'],
            'weight': 1.8,
        },
        'joy': {
            'keywords': ['happy', 'joyful', 'cheerful', 'delighted', 'blissful', 'merry', 'jubilant', 'overjoyed'],
            'phrases': ['so happy', 'best day', 'feeling great', 'on top of the world', 'couldn\'t be happier', 'made my day'],
            'weight': 1.2,
        },
        'love': {
            'keywords': ['love', 'adore', 'cherish', 'affection', 'devoted', 'soulmate', 'darling', 'sweetheart'],
            'phrases': ['i love', 'in love', 'love you', 'mean everything', 'my heart', 'forever yours'],
            'weight': 1.3,
        },
        'nervousness': {
            'keywords': ['nervous', 'anxious', 'jittery', 'restless', 'uneasy', 'apprehensive', 'tense', 'edgy'],
            'phrases': ['butterflies in my stomach', 'can\'t sit still', 'on edge', 'feeling jittery', 'heart racing'],
            'weight': 1.3,
        },
        'optimism': {
            'keywords': ['optimistic', 'hopeful', 'promising', 'bright', 'positive', 'encouraged', 'upbeat'],
            'phrases': ['things will get better', 'looking up', 'good feeling about', 'bright side', 'silver lining'],
            'weight': 1.0,
        },
        'pride': {
            'keywords': ['proud', 'pride', 'accomplished', 'achievement', 'triumph', 'victorious'],
            'phrases': ['so proud', 'did it', 'made it', 'pulled it off', 'achieved my goal'],
            'weight': 1.1,
        },
        'realization': {
            'keywords': ['realize', 'realized', 'understand', 'epiphany', 'revelation', 'clarity', 'insight'],
            'phrases': ['just realized', 'it hit me', 'now i see', 'makes sense now', 'opened my eyes'],
            'weight': 0.9,
        },
        'relief': {
            'keywords': ['relieved', 'relief', 'phew', 'finally', 'weight off', 'exhale'],
            'phrases': ['such a relief', 'finally over', 'weight off my shoulders', 'can breathe again', 'dodged a bullet'],
            'weight': 1.1,
        },
        'remorse': {
            'keywords': ['sorry', 'regret', 'remorse', 'apologize', 'guilt', 'guilty', 'ashamed'],
            'phrases': ['i\'m sorry', 'feel bad about', 'wish i hadn\'t', 'my fault', 'i regret', 'should have'],
            'weight': 1.2,
        },
        'sadness': {
            'keywords': ['sad', 'depressed', 'depression', 'unhappy', 'miserable', 'gloomy', 'heartbroken', 'sorrowful', 'melancholy', 'downcast', 'dejected', 'despondent', 'blue', 'down'],
            'phrases': ['feeling down', 'so sad', 'really upset', 'can\'t stop crying', 'heart hurts', 'feeling blue', 'empty inside', 'nothing matters'],
            'weight': 1.5,
        },
        'surprise': {
            'keywords': ['surprised', 'shocking', 'unexpected', 'astonished', 'stunned', 'wow', 'speechless', 'unbelievable'],
            'phrases': ['didn\'t expect', 'caught off guard', 'out of nowhere', 'can\'t believe', 'jaw dropped'],
            'weight': 0.9,
        },
        'neutral': {
            'keywords': [],
            'phrases': [],
            'weight': 0.3,
        },
    }

    # Crisis patterns (highest priority)
    CRISIS_PATTERNS = [
        'want to die', 'kill myself', 'end my life', 'suicide', 'suicidal',
        'want to end it', 'no reason to live', 'worthless', 'better off dead',
        'self harm', 'self-harm', 'cut myself', 'hurt myself',
        "don't want to be here", 'take my own life', 'not worth living',
        'give up on life', 'disappear forever', 'wish i was dead',
        "can't go on", "can't do this anymore", 'want to disappear',
        'nobody would miss me', 'world is better without me',
    ]

    # Simplified emotion groups for the chatbot's response system
    EMOTION_GROUPS = {
        'happy': ['admiration', 'amusement', 'approval', 'excitement', 'gratitude', 'joy', 'love', 'optimism', 'pride', 'relief'],
        'sad': ['disappointment', 'grief', 'remorse', 'sadness'],
        'anxious': ['fear', 'nervousness'],
        'stressed': ['annoyance'],
        'angry': ['anger', 'disapproval', 'disgust'],
        'confused': ['confusion', 'realization', 'surprise'],
        'lonely': [],
        'neutral': ['caring', 'curiosity', 'desire', 'embarrassment', 'neutral'],
    }

    def __init__(self):
        self.history = []

    def classify(self, text):
        """
        Classify text into emotions.
        Returns: dominant emotion, all scores, simplified group, crisis flag.
        """
        text_lower = text.lower().strip()

        # Crisis check first
        is_crisis = any(pattern in text_lower for pattern in self.CRISIS_PATTERNS)
        if is_crisis:
            return {
                'dominant': 'crisis',
                'simplified': 'crisis',
                'scores': {'crisis': 10},
                'confidence': 0.99,
                'is_crisis': True,
                'top_3': [('crisis', 10)],
            }

        # Score all emotions
        scores = {}
        for emotion, config in self.EMOTION_TAXONOMY.items():
            score = 0

            # Keyword matches
            for kw in config['keywords']:
                if kw in text_lower:
                    score += 2 * config['weight']

            # Phrase matches (higher weight)
            for phrase in config['phrases']:
                if phrase in text_lower:
                    score += 3 * config['weight']

            scores[emotion] = round(score, 2)

        # If nothing matched, set neutral
        if max(scores.values()) == 0:
            scores['neutral'] = 1

        # Sort and get top emotions
        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant = sorted_emotions[0][0]
        top_3 = sorted_emotions[:3]

        # Compute confidence
        top_score = sorted_emotions[0][1]
        second_score = sorted_emotions[1][1] if len(sorted_emotions) > 1 else 0
        if top_score > 0:
            confidence = min(0.99, 0.5 + (top_score - second_score) / (top_score + 1) * 0.5)
        else:
            confidence = 0.3

        # Map to simplified group
        simplified = 'neutral'
        for group, emotions in self.EMOTION_GROUPS.items():
            if dominant in emotions:
                simplified = group
                break

        # Check for loneliness specifically
        lonely_words = ['lonely', 'alone', 'isolated', 'abandoned', 'rejected', 'invisible', 'forgotten', 'disconnected', 'no friends', 'nobody']
        if any(w in text_lower for w in lonely_words):
            simplified = 'lonely'

        # Track history
        self.history.append({
            'emotion': dominant,
            'simplified': simplified,
            'confidence': confidence,
        })
        if len(self.history) > 50:
            self.history.pop(0)

        return {
            'dominant': dominant,
            'simplified': simplified,
            'scores': {k: v for k, v in sorted_emotions if v > 0},
            'confidence': round(confidence, 3),
            'is_crisis': False,
            'top_3': [(e, s) for e, s in top_3 if s > 0],
        }

    def get_emotion_trend(self):
        """Analyze emotion trend over conversation."""
        if len(self.history) < 3:
            return 'stable'

        recent = [h['simplified'] for h in self.history[-5:]]
        counter = Counter(recent)
        most_common = counter.most_common(1)[0]

        neg_emotions = {'sad', 'anxious', 'stressed', 'angry', 'lonely', 'crisis'}
        pos_emotions = {'happy', 'grateful'}

        neg_count = sum(1 for e in recent if e in neg_emotions)
        pos_count = sum(1 for e in recent if e in pos_emotions)

        if neg_count > len(recent) * 0.6:
            return 'declining'
        elif pos_count > len(recent) * 0.6:
            return 'improving'
        return 'stable'
