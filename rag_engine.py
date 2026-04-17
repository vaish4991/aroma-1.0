"""
Serein AI — RAG (Retrieval-Augmented Generation) Engine
=========================================================
Searches the knowledge base using TF-IDF similarity to find
the most relevant entries before calling GPT-4o.

Pipeline:
1. User message → TF-IDF vectorize
2. Search KB for top-5 similar entries
3. High match (>0.45): use KB response directly
4. Medium match (0.2-0.45): include as context for GPT-4o
5. Low match (<0.2): pure GPT-4o with enriched prompt
"""

import json
import os
import re
import math
from collections import Counter


class RAGEngine:
    """Retrieval-Augmented Generation engine using TF-IDF similarity."""

    def __init__(self, kb_path=None):
        if kb_path is None:
            kb_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'data', 'knowledge_base.json'
            )

        self.kb_path = kb_path
        self.entries = []
        self.tfidf_matrix = []
        self.vocabulary = {}
        self.idf = {}
        self.loaded = False

        self._load_and_index()

    def _load_and_index(self):
        """Load knowledge base and build TF-IDF index."""
        if not os.path.exists(self.kb_path):
            print(f"[RAG] Knowledge base not found at {self.kb_path}")
            print("[RAG] Running knowledge base builder...")
            try:
                from train.build_knowledge_base import build_knowledge_base
                build_knowledge_base()
            except Exception as e:
                print(f"[RAG] Could not build KB: {e}")
                return

        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            self.entries = kb.get('entries', [])
            if not self.entries:
                print("[RAG] Knowledge base is empty")
                return
            self._build_tfidf_index()
            self.loaded = True
            print(f"[RAG] Loaded {len(self.entries)} KB entries, TF-IDF index built")
        except Exception as e:
            print(f"[RAG] Error loading KB: {e}")

    def _tokenize(self, text):
        """Simple tokenizer: lowercase, remove punctuation, split."""
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        # Remove common stop words
        stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'you', 'your', 'he', 'she',
            'it', 'they', 'the', 'a', 'an', 'is', 'am', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'shall',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
            'and', 'but', 'or', 'if', 'then', 'than', 'that', 'this',
            'so', 'just', 'very', 'really', 'about', 'also', 'some',
        }
        return [t for t in tokens if t not in stop_words and len(t) > 1]

    def _build_tfidf_index(self):
        """Build TF-IDF vectors for all KB entries."""
        # Step 1: Build vocabulary and document frequencies
        doc_freq = Counter()
        all_docs = []

        for entry in self.entries:
            tokens = self._tokenize(entry['q'])
            all_docs.append(tokens)
            unique = set(tokens)
            for token in unique:
                doc_freq[token] += 1

        n_docs = len(all_docs)

        # Build vocabulary (map word → index)
        self.vocabulary = {}
        idx = 0
        for word, freq in doc_freq.items():
            if freq >= 1:  # Keep all words since KB is small
                self.vocabulary[word] = idx
                idx += 1

        # Compute IDF
        self.idf = {}
        for word, freq in doc_freq.items():
            if word in self.vocabulary:
                self.idf[word] = math.log((n_docs + 1) / (freq + 1)) + 1

        # Step 2: Build TF-IDF vectors for each document
        self.tfidf_matrix = []
        for tokens in all_docs:
            vec = self._compute_tfidf(tokens)
            self.tfidf_matrix.append(vec)

    def _compute_tfidf(self, tokens):
        """Compute TF-IDF vector for a list of tokens."""
        tf = Counter(tokens)
        n = len(tokens) if tokens else 1
        vec = {}
        for word, count in tf.items():
            if word in self.vocabulary:
                tf_val = count / n
                idf_val = self.idf.get(word, 1)
                vec[self.vocabulary[word]] = tf_val * idf_val
        return vec

    def _cosine_similarity(self, vec1, vec2):
        """Compute cosine similarity between two sparse vectors."""
        if not vec1 or not vec2:
            return 0.0

        common_keys = set(vec1.keys()) & set(vec2.keys())
        if not common_keys:
            return 0.0

        dot = sum(vec1[k] * vec2[k] for k in common_keys)
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot / (norm1 * norm2)

    def search(self, query, top_k=5):
        """
        Search the knowledge base for entries similar to the query.
        Returns list of (entry, similarity_score) tuples.
        """
        if not self.loaded or not self.entries:
            return []

        query_tokens = self._tokenize(query)
        query_vec = self._compute_tfidf(query_tokens)

        if not query_vec:
            return []

        # Compute similarity with all entries
        similarities = []
        for i, entry_vec in enumerate(self.tfidf_matrix):
            sim = self._cosine_similarity(query_vec, entry_vec)
            if sim > 0.05:  # Filter out very low matches
                similarities.append((self.entries[i], sim))

        # Sort by similarity, descending
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def get_best_response(self, query, emotion=None):
        """
        Get the best response from the KB.
        Returns: (response, confidence, source) or (None, 0, None) if no good match.
        """
        results = self.search(query, top_k=5)

        if not results:
            return None, 0.0, None

        best_entry, best_score = results[0]

        # If emotion matches, boost the score
        if emotion and best_entry.get('emotion') == emotion:
            best_score *= 1.2

        return best_entry.get('a'), best_score, best_entry.get('source')

    def get_context_for_gpt(self, query, top_k=3):
        """
        Get relevant KB entries as context for GPT-4o.
        Returns formatted context string.
        """
        results = self.search(query, top_k=top_k)

        if not results:
            return ""

        context_parts = []
        for entry, score in results:
            if score > 0.15:
                context_parts.append(
                    f"[Similar question (relevance: {score:.0%}): \"{entry['q']}\"]\n"
                    f"[Expert response: \"{entry['a'][:200]}...\"]\n"
                    f"[Emotion: {entry.get('emotion', 'neutral')}]"
                )

        if not context_parts:
            return ""

        return (
            "RELEVANT CONTEXT FROM KNOWLEDGE BASE (use these as reference for your response):\n\n"
            + "\n\n".join(context_parts)
        )

    def get_retrieval_tier(self, query, emotion=None):
        """
        Determine which retrieval tier to use.
        Returns: ('direct', response) | ('augmented', context) | ('pure', None)
        """
        results = self.search(query, top_k=5)

        if not results:
            return 'pure', None

        best_entry, best_score = results[0]

        # Tier 1: Direct KB response (high confidence match)
        if best_score > 0.45:
            return 'direct', best_entry.get('a')

        # Tier 2: Augmented — use KB as context for GPT
        if best_score > 0.15:
            context = self.get_context_for_gpt(query)
            return 'augmented', context

        # Tier 3: Pure GPT-4o
        return 'pure', None
