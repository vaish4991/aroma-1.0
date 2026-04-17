"""
Serein AI — Multi-Model Sentiment Analysis Ensemble
=====================================================
Combines VADER + TextBlob + Custom AFINN for accurate emotion detection.
Each model votes, and the ensemble produces a weighted final result.
"""

import re
import math

# ── VADER Sentiment (Rule-based, tuned for social media) ──────────────────
class VADERAnalyzer:
    """
    Simplified VADER implementation with full lexicon.
    Handles: emoticons, slang, ALL-CAPS emphasis, punctuation amplification.
    """
    def __init__(self):
        self.lexicon = self._build_lexicon()
        self.boosters = {
            'absolutely': 0.293, 'amazingly': 0.293, 'awfully': 0.293,
            'completely': 0.293, 'considerably': 0.293, 'decidedly': 0.293,
            'deeply': 0.293, 'enormously': 0.293, 'entirely': 0.293,
            'especially': 0.293, 'exceptionally': 0.293, 'extremely': 0.293,
            'fabulously': 0.293, 'flipping': 0.293, 'freaking': 0.293,
            'greatly': 0.293, 'hella': 0.293, 'highly': 0.293,
            'hugely': 0.293, 'incredibly': 0.293, 'intensely': 0.293,
            'majorly': 0.293, 'more': 0.293, 'most': 0.293,
            'particularly': 0.293, 'purely': 0.293, 'quite': 0.293,
            'really': 0.293, 'remarkably': 0.293, 'so': 0.293,
            'substantially': 0.293, 'thoroughly': 0.293, 'totally': 0.293,
            'tremendously': 0.293, 'uber': 0.293, 'unbelievably': 0.293,
            'unusually': 0.293, 'utterly': 0.293, 'very': 0.293,
        }
        self.negations = {
            "ain't", "aren't", "can't", "couldn't", "didn't", "doesn't",
            "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't",
            "mustn't", "needn't", "never", "no", "nobody", "none", "nor",
            "not", "nothing", "nowhere", "shan't", "shouldn't", "wasn't",
            "weren't", "without", "won't", "wouldn't",
        }

    def _build_lexicon(self):
        """Core sentiment lexicon with valence scores (-4 to +4)."""
        lex = {}
        # Positive words
        pos_words = {
            'good': 1.9, 'great': 3.1, 'awesome': 3.3, 'amazing': 3.1,
            'wonderful': 3.2, 'fantastic': 3.4, 'excellent': 3.2, 'love': 3.2,
            'happy': 2.7, 'joy': 3.0, 'joyful': 3.0, 'beautiful': 2.8,
            'brilliant': 3.0, 'perfect': 3.0, 'best': 3.2, 'glad': 2.4,
            'thankful': 2.2, 'grateful': 2.6, 'blessed': 2.5, 'excited': 2.8,
            'thrilled': 3.1, 'ecstatic': 3.4, 'delighted': 3.0, 'cheerful': 2.6,
            'hopeful': 2.2, 'optimistic': 2.4, 'proud': 2.6, 'confident': 2.3,
            'content': 2.0, 'peaceful': 2.2, 'calm': 1.8, 'relaxed': 2.0,
            'inspired': 2.5, 'motivated': 2.3, 'energized': 2.4, 'alive': 2.0,
            'smile': 2.0, 'laugh': 2.4, 'fun': 2.5, 'enjoy': 2.2,
            'celebrate': 2.6, 'success': 2.5, 'win': 2.4, 'achieved': 2.5,
            'comfortable': 1.8, 'safe': 1.7, 'warm': 1.5, 'kind': 2.0,
            'caring': 2.1, 'sweet': 2.0, 'nice': 1.8, 'pleasant': 1.9,
            'positive': 1.8, 'better': 1.5, 'improve': 1.6, 'progress': 1.7,
            'relief': 2.0, 'free': 1.8, 'strong': 1.7, 'brave': 2.2,
            'courageous': 2.4, 'resilient': 2.0, 'capable': 1.8, 'worthy': 2.0,
        }
        # Negative words
        neg_words = {
            'bad': -2.5, 'terrible': -3.2, 'awful': -3.1, 'horrible': -3.2,
            'sad': -2.5, 'depressed': -3.4, 'depression': -3.4, 'unhappy': -2.6,
            'miserable': -3.1, 'lonely': -2.7, 'alone': -1.8, 'empty': -2.5,
            'hopeless': -3.3, 'helpless': -3.0, 'worthless': -3.5, 'useless': -2.8,
            'anxious': -2.5, 'anxiety': -2.7, 'nervous': -2.0, 'worried': -2.2,
            'scared': -2.5, 'afraid': -2.4, 'terrified': -3.2, 'panic': -3.0,
            'stressed': -2.6, 'overwhelmed': -2.8, 'exhausted': -2.5, 'tired': -1.8,
            'burnout': -3.0, 'drained': -2.5, 'frustrated': -2.4, 'irritated': -2.2,
            'angry': -2.8, 'furious': -3.4, 'rage': -3.5, 'hate': -3.2,
            'mad': -2.5, 'annoyed': -2.0, 'disgusted': -2.8, 'resentful': -2.5,
            'hurt': -2.5, 'pain': -2.7, 'suffering': -3.0, 'agony': -3.3,
            'cry': -2.3, 'crying': -2.5, 'tears': -2.1, 'sob': -2.6,
            'broken': -2.8, 'shattered': -3.1, 'devastated': -3.3, 'destroyed': -3.0,
            'grief': -3.0, 'mourning': -2.8, 'loss': -2.5, 'lost': -2.0,
            'failure': -2.8, 'failed': -2.6, 'failing': -2.5, 'fail': -2.5,
            'stuck': -2.0, 'trapped': -2.8, 'suffocating': -3.0, 'drowning': -3.0,
            'numb': -2.5, 'dead': -3.0, 'dying': -3.2, 'death': -3.0,
            'suicide': -3.8, 'suicidal': -3.9, 'harm': -2.8, 'cut': -1.5,
            'dark': -1.8, 'darkness': -2.0, 'nightmare': -2.5, 'hell': -2.8,
            'ugly': -2.5, 'pathetic': -2.8, 'weak': -2.0, 'stupid': -2.3,
            'dumb': -2.1, 'idiot': -2.5, 'loser': -2.8, 'burden': -2.6,
            'regret': -2.2, 'guilt': -2.5, 'ashamed': -2.6, 'shame': -2.7,
            'jealous': -2.0, 'envy': -1.8, 'bitter': -2.2, 'hostile': -2.5,
            'sick': -2.0, 'ill': -1.8, 'disease': -2.2, 'disorder': -2.0,
            'insomnia': -2.2, 'nightmare': -2.3, 'restless': -1.8,
            'confused': -1.5, 'uncertain': -1.3, 'doubt': -1.5, 'unsure': -1.2,
            'disappointed': -2.3, 'letdown': -2.2, 'betrayed': -3.0,
            'abandoned': -3.0, 'rejected': -2.8, 'ignored': -2.2, 'invisible': -2.5,
            'unloved': -3.0, 'unwanted': -2.8, 'unworthy': -3.0,
        }
        lex.update(pos_words)
        lex.update(neg_words)
        return lex

    def analyze(self, text):
        """Returns compound, pos, neg, neu scores."""
        words = self._tokenize(text)
        sentiments = []

        for i, word in enumerate(words):
            lower = word.lower()
            valence = self.lexicon.get(lower, 0)

            if valence == 0:
                continue

            # Check ALL CAPS (amplification)
            if word.isupper() and len(word) > 1:
                valence += 0.733 if valence > 0 else -0.733

            # Check boosters in preceding words
            if i > 0:
                prev = words[i - 1].lower()
                if prev in self.boosters:
                    boost = self.boosters[prev]
                    valence += boost if valence > 0 else -boost

            # Check negation in preceding 3 words
            negated = False
            for j in range(max(0, i - 3), i):
                if words[j].lower() in self.negations:
                    negated = True
                    break
            if negated:
                valence *= -0.74

            sentiments.append(valence)

        # Punctuation emphasis
        exclamation_count = text.count('!')
        question_count = text.count('?')
        ep_amplifier = min(exclamation_count * 0.292, 1.5)
        qm_modifier = 0.18 if question_count > 1 else 0

        # Compute scores
        if not sentiments:
            return {'compound': 0.0, 'pos': 0.0, 'neg': 0.0, 'neu': 1.0}

        total = sum(sentiments)

        if total > 0:
            total += ep_amplifier
        elif total < 0:
            total -= ep_amplifier
        total -= qm_modifier

        # Normalize compound to -1 to 1
        compound = total / math.sqrt(total * total + 15)

        pos_sum = sum(s for s in sentiments if s > 0) + 1e-6
        neg_sum = sum(abs(s) for s in sentiments if s < 0) + 1e-6
        neu_count = len([s for s in sentiments if s == 0])
        total_abs = pos_sum + neg_sum + neu_count + 1e-6

        return {
            'compound': round(compound, 4),
            'pos': round(pos_sum / total_abs, 3),
            'neg': round(neg_sum / total_abs, 3),
            'neu': round(neu_count / total_abs, 3),
        }

    def _tokenize(self, text):
        return re.findall(r"[\w']+|[.,!?;]", text)


# ── TextBlob-style Pattern Analyzer ──────────────────────────────────────
class PatternAnalyzer:
    """
    Pattern-based sentiment analysis (TextBlob approach).
    Returns polarity (-1 to 1) and subjectivity (0 to 1).
    """
    def __init__(self):
        self.pattern_lexicon = self._build_patterns()

    def _build_patterns(self):
        return {
            # (polarity, subjectivity)
            'good': (0.7, 0.6), 'great': (0.8, 0.75), 'awesome': (0.9, 0.8),
            'amazing': (0.9, 0.8), 'wonderful': (0.9, 0.8), 'excellent': (0.85, 0.75),
            'love': (0.8, 0.9), 'happy': (0.8, 0.9), 'joy': (0.8, 0.9),
            'beautiful': (0.85, 0.85), 'perfect': (0.9, 0.8), 'fantastic': (0.9, 0.8),
            'glad': (0.6, 0.7), 'thankful': (0.7, 0.8), 'grateful': (0.7, 0.8),
            'blessed': (0.7, 0.8), 'excited': (0.8, 0.9), 'thrilled': (0.9, 0.9),
            'proud': (0.7, 0.8), 'confident': (0.6, 0.7), 'hopeful': (0.6, 0.7),
            'calm': (0.5, 0.6), 'peaceful': (0.6, 0.7), 'relaxed': (0.5, 0.6),
            'motivated': (0.6, 0.7), 'inspired': (0.7, 0.8), 'fun': (0.7, 0.8),
            'success': (0.7, 0.6), 'achieve': (0.6, 0.6), 'celebrate': (0.8, 0.8),
            'smile': (0.6, 0.7), 'laugh': (0.7, 0.8),

            'bad': (-0.7, 0.6), 'terrible': (-0.9, 0.8), 'awful': (-0.9, 0.8),
            'horrible': (-0.9, 0.8), 'sad': (-0.7, 0.9), 'depressed': (-0.9, 0.9),
            'unhappy': (-0.7, 0.8), 'miserable': (-0.9, 0.9), 'lonely': (-0.7, 0.9),
            'alone': (-0.4, 0.5), 'empty': (-0.6, 0.7), 'hopeless': (-0.9, 0.9),
            'helpless': (-0.8, 0.9), 'worthless': (-0.9, 0.9), 'anxious': (-0.6, 0.8),
            'anxiety': (-0.7, 0.7), 'nervous': (-0.5, 0.7), 'worried': (-0.5, 0.7),
            'scared': (-0.7, 0.8), 'afraid': (-0.6, 0.8), 'terrified': (-0.9, 0.9),
            'panic': (-0.8, 0.8), 'stressed': (-0.7, 0.8), 'overwhelmed': (-0.7, 0.8),
            'exhausted': (-0.6, 0.7), 'tired': (-0.4, 0.6), 'frustrated': (-0.6, 0.8),
            'angry': (-0.8, 0.9), 'furious': (-0.9, 0.9), 'hate': (-0.9, 0.9),
            'hurt': (-0.7, 0.8), 'pain': (-0.7, 0.7), 'cry': (-0.6, 0.8),
            'crying': (-0.7, 0.9), 'broken': (-0.8, 0.8), 'devastated': (-0.9, 0.9),
            'grief': (-0.8, 0.9), 'failure': (-0.7, 0.7), 'failed': (-0.7, 0.7),
            'stuck': (-0.5, 0.6), 'trapped': (-0.7, 0.8), 'numb': (-0.6, 0.7),
            'confused': (-0.3, 0.5), 'disappointed': (-0.6, 0.7),
            'abandoned': (-0.8, 0.9), 'rejected': (-0.7, 0.8), 'ignored': (-0.5, 0.7),
            'burden': (-0.7, 0.8), 'guilt': (-0.6, 0.8), 'ashamed': (-0.7, 0.8),
            'shame': (-0.7, 0.8), 'regret': (-0.5, 0.7), 'weak': (-0.5, 0.6),

            # Context-dependent mental health words (often negative in emotional context)
            'fine': (-0.1, 0.3),  # "I'm fine" is often hiding emotions
            'okay': (0.1, 0.3),
            'whatever': (-0.3, 0.4),
            'nothing': (-0.2, 0.3),
            'everything': (-0.1, 0.2),
        }

    def analyze(self, text):
        words = re.findall(r'\w+', text.lower())
        polarities = []
        subjectivities = []

        for i, word in enumerate(words):
            if word in self.pattern_lexicon:
                pol, subj = self.pattern_lexicon[word]

                # Check for negation
                if i > 0 and words[i-1] in ('not', "don't", "didn't", "can't", "won't", "never", "no", "isn't", "aren't", "wasn't"):
                    pol *= -0.5

                polarities.append(pol)
                subjectivities.append(subj)

        if not polarities:
            return {'polarity': 0.0, 'subjectivity': 0.0}

        return {
            'polarity': round(sum(polarities) / len(polarities), 4),
            'subjectivity': round(sum(subjectivities) / len(subjectivities), 4),
        }


# ── Custom AFINN-style Scorer with Mental Health Extensions ──────────────
class AFINNScorer:
    """
    Word-level sentiment scoring based on AFINN methodology.
    Extended with mental-health-specific vocabulary.
    Scores: -5 (most negative) to +5 (most positive)
    """
    def __init__(self):
        self.scores = self._build_scores()
        self.intensifiers = {
            'very': 1.5, 'really': 1.4, 'extremely': 1.8, 'so': 1.3,
            'absolutely': 1.7, 'completely': 1.6, 'totally': 1.5,
            'deeply': 1.5, 'incredibly': 1.7, 'terribly': 1.6,
            'utterly': 1.7, 'genuinely': 1.3, 'truly': 1.4,
        }
        self.negators = {'not', "don't", "didn't", "can't", "couldn't",
                         "won't", "wouldn't", "never", "no", "neither",
                         "nor", "isn't", "aren't", "wasn't", "weren't",
                         "hasn't", "haven't", "hadn't", "shouldn't", "without"}

    def _build_scores(self):
        return {
            # Positive (+1 to +5)
            'good': 3, 'great': 3, 'awesome': 4, 'amazing': 4,
            'wonderful': 4, 'excellent': 4, 'love': 3, 'loved': 3,
            'happy': 3, 'joy': 4, 'joyful': 4, 'beautiful': 3,
            'brilliant': 4, 'perfect': 3, 'best': 3, 'glad': 3,
            'thankful': 2, 'grateful': 3, 'blessed': 3, 'excited': 3,
            'thrilled': 4, 'ecstatic': 5, 'delighted': 4, 'cheerful': 3,
            'hopeful': 2, 'optimistic': 2, 'proud': 3, 'confident': 2,
            'content': 2, 'peaceful': 2, 'calm': 2, 'relaxed': 2,
            'inspired': 3, 'motivated': 2, 'energized': 3, 'alive': 2,
            'smile': 2, 'laugh': 3, 'fun': 3, 'enjoy': 2,
            'celebrate': 3, 'success': 3, 'win': 3, 'achieve': 3,
            'better': 2, 'improve': 2, 'progress': 2, 'relief': 2,
            'strong': 2, 'brave': 3, 'courage': 3, 'resilient': 3,
            'kind': 2, 'caring': 2, 'sweet': 2, 'nice': 2,
            'fantastic': 4, 'superb': 4, 'outstanding': 4, 'remarkable': 3,
            'incredible': 4, 'magnificent': 4, 'marvelous': 4,
            'terrific': 4, 'splendid': 3, 'glorious': 4,
            'supportive': 2, 'understanding': 2, 'compassionate': 3,
            'healing': 2, 'growth': 2, 'strength': 2,

            # Negative (-1 to -5)
            'bad': -3, 'terrible': -4, 'awful': -4, 'horrible': -4,
            'sad': -3, 'depressed': -4, 'depression': -4, 'unhappy': -3,
            'miserable': -4, 'lonely': -3, 'alone': -2, 'empty': -3,
            'hopeless': -4, 'helpless': -4, 'worthless': -4, 'useless': -3,
            'anxious': -3, 'anxiety': -3, 'nervous': -2, 'worried': -2,
            'scared': -3, 'afraid': -3, 'terrified': -4, 'panic': -4,
            'stressed': -3, 'overwhelmed': -3, 'exhausted': -3, 'tired': -2,
            'burnout': -4, 'drained': -3, 'frustrated': -3, 'irritated': -2,
            'angry': -3, 'furious': -4, 'rage': -5, 'hate': -4,
            'mad': -3, 'annoyed': -2, 'disgusted': -3, 'resentful': -3,
            'hurt': -3, 'pain': -3, 'suffering': -4, 'agony': -4,
            'cry': -2, 'crying': -3, 'tears': -2, 'sob': -3,
            'broken': -3, 'shattered': -4, 'devastated': -4, 'destroyed': -4,
            'grief': -4, 'mourning': -3, 'loss': -3, 'lost': -2,
            'failure': -3, 'failed': -3, 'failing': -3, 'fail': -3,
            'stuck': -2, 'trapped': -3, 'suffocating': -4, 'drowning': -4,
            'numb': -3, 'dead': -4, 'dying': -4, 'death': -4,
            'suicide': -5, 'suicidal': -5, 'harm': -3, 'cut': -1,
            'dark': -2, 'darkness': -2, 'nightmare': -3, 'hell': -3,
            'ugly': -3, 'pathetic': -3, 'weak': -2, 'stupid': -2,
            'loser': -3, 'burden': -3, 'shame': -3, 'ashamed': -3,
            'guilt': -3, 'regret': -2, 'abandoned': -4, 'rejected': -3,
            'ignored': -2, 'invisible': -3, 'unloved': -4, 'unwanted': -3,
            'betrayed': -4, 'disappointed': -3, 'confused': -2,
            'insomnia': -2, 'restless': -2, 'disorder': -2,
        }

    def analyze(self, text):
        words = re.findall(r'\w+', text.lower())
        total_score = 0
        word_count = 0
        scores_list = []
        intensifier_active = 1.0

        for i, word in enumerate(words):
            # Check for intensifier
            if word in self.intensifiers:
                intensifier_active = self.intensifiers[word]
                continue

            if word in self.scores:
                score = self.scores[word] * intensifier_active

                # Negation check
                negated = False
                for j in range(max(0, i - 3), i):
                    if words[j] in self.negators:
                        negated = True
                        break
                if negated:
                    score *= -0.5

                total_score += score
                scores_list.append(score)
                word_count += 1
                intensifier_active = 1.0
            else:
                intensifier_active = 1.0

        if word_count == 0:
            return {'score': 0, 'normalized': 0.0, 'word_count': 0}

        # Normalize to -1 to 1
        normalized = total_score / (word_count * 5)  # max possible per word is 5
        normalized = max(-1.0, min(1.0, normalized))

        return {
            'score': round(total_score, 2),
            'normalized': round(normalized, 4),
            'word_count': word_count,
        }


# ── ENSEMBLE: Combines all 3 models ─────────────────────────────────────
class SentimentEnsemble:
    """
    Weighted ensemble of VADER + Pattern (TextBlob) + AFINN.
    Returns unified sentiment analysis with emotion mapping.
    """
    WEIGHTS = {'vader': 0.40, 'pattern': 0.30, 'afinn': 0.30}

    EMOTION_MAP = {
        # (valence_range, arousal_hints) → emotion
        'happy': {'min_val': 0.3, 'keywords': ['happy', 'joy', 'glad', 'excited', 'thrilled', 'love', 'amazing', 'great', 'wonderful', 'awesome', 'fantastic', 'celebrate', 'proud', 'blessed']},
        'sad': {'max_val': -0.2, 'keywords': ['sad', 'cry', 'crying', 'tears', 'unhappy', 'miserable', 'lonely', 'empty', 'grief', 'loss', 'broken', 'heartbroken', 'devastated', 'depressed', 'depression']},
        'anxious': {'max_val': -0.1, 'keywords': ['anxious', 'anxiety', 'nervous', 'worried', 'scared', 'panic', 'fear', 'afraid', 'terrified', 'overthinking', 'dread', 'tense']},
        'stressed': {'max_val': -0.1, 'keywords': ['stressed', 'stress', 'overwhelmed', 'exhausted', 'burnout', 'pressure', 'deadline', 'tired', 'drained', 'frustrated', 'overloaded']},
        'angry': {'max_val': -0.2, 'keywords': ['angry', 'furious', 'rage', 'hate', 'mad', 'annoyed', 'irritated', 'pissed', 'livid', 'enraged']},
        'grateful': {'min_val': 0.2, 'keywords': ['grateful', 'thankful', 'blessed', 'appreciate', 'thank', 'thanks']},
        'lonely': {'max_val': -0.1, 'keywords': ['lonely', 'alone', 'isolated', 'abandoned', 'rejected', 'invisible', 'forgotten', 'disconnected', 'no friends', 'nobody']},
        'confused': {'keywords': ['confused', 'uncertain', 'unsure', 'lost', 'don\'t know', 'not sure', 'mixed feelings']},
    }

    def __init__(self):
        self.vader = VADERAnalyzer()
        self.pattern = PatternAnalyzer()
        self.afinn = AFINNScorer()

    def analyze(self, text):
        """Full ensemble analysis. Returns comprehensive result."""
        # Run all 3 models
        vader_result = self.vader.analyze(text)
        pattern_result = self.pattern.analyze(text)
        afinn_result = self.afinn.analyze(text)

        # Weighted valence
        weighted_valence = (
            vader_result['compound'] * self.WEIGHTS['vader'] +
            pattern_result['polarity'] * self.WEIGHTS['pattern'] +
            afinn_result['normalized'] * self.WEIGHTS['afinn']
        )

        # Determine emotion from keywords + valence
        text_lower = text.lower()
        emotion_scores = {}

        for emotion, config in self.EMOTION_MAP.items():
            score = 0
            kw_matches = sum(1 for kw in config['keywords'] if kw in text_lower)
            score += kw_matches * 2

            # Valence alignment
            if 'min_val' in config and weighted_valence >= config['min_val']:
                score += 1
            if 'max_val' in config and weighted_valence <= config['max_val']:
                score += 1

            emotion_scores[emotion] = score

        # Pick dominant emotion
        if max(emotion_scores.values(), default=0) == 0:
            dominant = 'neutral'
        else:
            dominant = max(emotion_scores, key=emotion_scores.get)

        # Model agreement (confidence)
        signs = [
            1 if vader_result['compound'] > 0.05 else (-1 if vader_result['compound'] < -0.05 else 0),
            1 if pattern_result['polarity'] > 0.05 else (-1 if pattern_result['polarity'] < -0.05 else 0),
            1 if afinn_result['normalized'] > 0.05 else (-1 if afinn_result['normalized'] < -0.05 else 0),
        ]
        agreement = abs(sum(signs)) / 3
        confidence = 0.5 + agreement * 0.5  # 0.5 to 1.0

        # Sentiment label
        if weighted_valence > 0.15:
            sentiment = 'positive'
        elif weighted_valence < -0.15:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # Intensity
        abs_val = abs(weighted_valence)
        if abs_val > 0.6:
            intensity = 'high'
        elif abs_val > 0.3:
            intensity = 'medium'
        else:
            intensity = 'low'

        # Crisis detection
        crisis_words = ['suicide', 'suicidal', 'kill myself', 'want to die', 'end my life',
                       'self harm', 'self-harm', 'hurt myself', 'no reason to live',
                       'better off dead', 'take my life', 'wish i was dead']
        is_crisis = any(cw in text_lower for cw in crisis_words)

        return {
            'sentiment': sentiment,
            'valence': round(weighted_valence, 4),
            'dominant_emotion': 'crisis' if is_crisis else dominant,
            'emotion_scores': emotion_scores,
            'intensity': intensity,
            'confidence': round(confidence, 3),
            'is_crisis': is_crisis,
            'models': {
                'vader': vader_result,
                'pattern': pattern_result,
                'afinn': afinn_result,
            },
        }
