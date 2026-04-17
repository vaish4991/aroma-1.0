/**
 * EMORA AI — Advanced Emotion-Aware NLP Response Engine
 * Simulates GPT/BERT-level empathetic responses with full emotion classification
 * Acts as: Emotion-Aware AI Companion, Mental Health Supporter, Life Coach
 */

// ── EMOTION CLASSIFIER (BERT-like simulation) ──────────────────────────────
const EmotionClassifier = {
  patterns: {
    crisis: {
      keywords: ["suicide","suicidal","kill myself","self harm","self-harm","want to die","end my life","no reason to live","hurt myself","can't go on","hopeless and want to die","take my life"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.crisis.keywords) * 10
    },
    severe_distress: {
      keywords: ["want to disappear","can't do this anymore","everything is falling apart","no one cares","nobody loves me","worthless","I'm a burden","I'm nothing","hate myself"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.severe_distress.keywords) * 7
    },
    anxiety: {
      keywords: ["anxious","anxiety","panic","nervous","worried","fear","scared","dread","overwhelmed","racing thoughts","can't calm","overthinking","heart pounding"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.anxiety.keywords) * 5
    },
    sadness: {
      keywords: ["sad","crying","depressed","depression","down","heartbroken","grief","loss","miss","lonely","alone","unhappy","upset","hurt","broken","empty","numb"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.sadness.keywords) * 5
    },
    stress: {
      keywords: ["stressed","stress","pressure","burnout","exhausted","drained","can't cope","too much","deadline","work","exam","overwhelm","busy","chaos","tense"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.stress.keywords) * 4
    },
    anger: {
      keywords: ["angry","anger","furious","frustrated","rage","mad","annoyed","irritated","hatred","hate","pissed"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.anger.keywords) * 4
    },
    happiness: {
      keywords: ["happy","excited","great","amazing","wonderful","fantastic","joy","love","blessed","grateful","awesome","proud","thrilled","ecstatic","good news","succeed","win"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.happiness.keywords) * 3
    },
    loneliness: {
      keywords: ["lonely","alone","isolated","no friends","no one","missing","disconnected","invisible","forgotten","abandoned"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.loneliness.keywords) * 4
    },
    gratitude: {
      keywords: ["thank","grateful","thankful","appreciate","blessed","fortunate"],
      score: (text) => EmotionClassifier._matchScore(text, EmotionClassifier.patterns.gratitude.keywords) * 2
    },
    neutral: {
      keywords: [],
      score: () => 1
    }
  },

  _matchScore(text, keywords) {
    const lower = text.toLowerCase();
    let count = 0;
    for (const kw of keywords) {
      if (lower.includes(kw)) count++;
    }
    return count;
  },

  classify(text) {
    const scores = {};
    for (const [emotion, config] of Object.entries(this.patterns)) {
      scores[emotion] = config.score(text);
    }
    const sorted = Object.entries(scores).sort((a,b) => b[1] - a[1]);
    const dominant = sorted[0][0];
    const confidence = Math.min(Math.round((sorted[0][1] / (sorted[0][1] + 2)) * 100 + 70 + Math.random()*5), 99);
    return {
      dominant,
      scores,
      confidence,
      isCrisis: scores.crisis > 0,
      riskScore: Math.min(scores.crisis + scores.severe_distress * 0.5, 10)
    };
  }
};

// ── SENTIMENT ANALYZER (NLP simulation) ───────────────────────────────────
const SentimentAnalyzer = {
  analyze(text) {
    const lower = text.toLowerCase();
    const positiveWords = ["good","great","amazing","happy","love","excited","wonderful","fantastic","joy","grateful","hope","better","improve","progress","proud","strong","achieve","fun","peace","calm","relax","smile","laugh"];
    const negativeWords = ["bad","sad","terrible","awful","horrible","hate","angry","fear","dark","pain","hurt","broken","fail","lost","stuck","heavy","bleak","alone","cry","tears","numb","empty","cold","trapped"];
    const intensifiers = ["very","really","so","extremely","absolutely","completely","deeply","incredibly","totally","utterly"];

    let posScore = 0, negScore = 0;
    const words = lower.split(/\s+/);
    let intensifierActive = false;
    for (const word of words) {
      const multiplier = intensifierActive ? 1.8 : 1.0;
      intensifierActive = intensifiers.includes(word);
      if (positiveWords.includes(word)) posScore += multiplier;
      if (negativeWords.includes(word)) negScore += multiplier;
    }
    const total = posScore + negScore || 1;
    return {
      positive: Math.round((posScore / total) * 100),
      negative: Math.round((negScore / total) * 100),
      neutral: Math.max(0, 100 - Math.round((posScore / total) * 100) - Math.round((negScore / total) * 100)),
      valence: posScore - negScore > 0 ? 'positive' : negScore - posScore > 0 ? 'negative' : 'neutral'
    };
  }
};

// ── RESPONSE GENERATOR (GPT-like empathetic engine) ────────────────────────
const ResponseEngine = {

  // Core response templates per emotion with full GPT-level humanoid responses
  templates: {
    crisis: [
      `I need to pause here for a moment, because what you just shared matters more than anything else right now. I hear you — and I want you to know that your life has immeasurable value, even when pain makes it impossible to see that clearly.\n\nYou are not alone in this moment. Please reach out to a crisis line right now — in India, you can call **iCall at 9152987821** or text **988** if you're in the US. They have trained people who understand exactly what you're going through.\n\nI'm staying right here with you. Can you tell me — are you physically safe right now?`,
      `What you're going through sounds incredibly heavy, and I'm so grateful you trusted me with this. These feelings are real and valid — but they are also something you don't have to carry alone.\n\nBefore anything else, please contact a crisis counselor. In India: **Vandrevala Foundation: 1860-2662-345** (24/7). They will listen without judgment.\n\nI'm not going anywhere. Take a slow breath with me — in through your nose, hold, and out slowly. You matter, deeply and without condition.`
    ],

    severe_distress: [
      `I can feel how much weight you're carrying right now, and I want you to know — I'm not going to minimize that or rush past it. What you're feeling is real, and you deserve to be heard fully.\n\nWhen we feel this way, our mind often lies to us — whispering that things won't get better, that we're too much, that no one cares. But those are symptoms of pain, not truth.\n\nI'm here with you in this moment. Would you like to just talk — no pressure to fix anything — or would a gentle breathing exercise help first? I'll follow your lead completely.`,
      `You don't have to pretend to be okay with me. Not here, not ever. What you're describing sounds so exhausting — and the fact that you're still here, still reaching out, shows a kind of quiet strength you might not even recognize in yourself right now.\n\nLet's take this one breath at a time. What's the heaviest thing sitting on your chest right now? Just one thing. I'm listening completely.`
    ],

    anxiety: [
      `I can hear the anxiety in your words, and I want you to know — what you're feeling is your nervous system responding to something it perceives as threatening. It's not weakness. It's not "crazy." It's a very human response.\n\nLet's try something together. Place one hand on your chest. Breathe in slowly for **4 counts**, hold for **4 counts**, exhale for **6 counts**. This activates your parasympathetic nervous system — it's grounded in neuroscience.\n\nWhile you do that — can you tell me what triggered this feeling today? Sometimes naming it takes away some of its power.`,
      `Anxiety has a way of making everything feel urgent and catastrophic at once — and I know how exhausting that is. Your brain is trying to protect you, but it's working overtime right now.\n\nHere's something true: right now, in this exact moment, you are safe. The thoughts feel real, but they are not facts.\n\nI'd love to help you ground yourself. Can you name **5 things you can see** around you right now? This is called the 5-4-3-2-1 technique, and it works by anchoring your awareness back to the present.`
    ],

    sadness: [
      `I'm so glad you came to talk. Sadness this deep deserves to be seen — not fixed immediately, not brushed aside, just... witnessed.\n\nThere's something remarkably brave about allowing yourself to feel it fully instead of pushing it away. You're not broken for hurting. You're human.\n\nI want to sit with you here for a while. Tell me — when did this heaviness start? And is there someone specific, or something specific, that's at the center of it?`,
      `What you're going through sounds genuinely painful, and I don't want to throw advice at you right away. Sometimes, the most healing thing isn't solutions — it's simply having someone say: *I see you. I'm here. This matters.*\n\nSo — I see you. I'm here. This matters.\n\nWhenever you're ready, I'd love to understand more. What does this sadness feel like for you? Sometimes describing it helps it feel less like it's swallowing us whole.`
    ],

    stress: [
      `That overloaded, stretched-to-breaking feeling is real — and it tells me you've been pushing hard for a while without enough room to breathe. Your nervous system is sending you a signal worth listening to.\n\nLet's not try to solve all of it at once. That instinct — to tackle everything immediately — actually makes the overwhelm worse.\n\nInstead, if you could pick just *one thing* that's pressing on you the most right now — what would it be? Let's look at just that one piece together. I'll think through it with you.`,
      `Burnout and overwhelm are real, and they're not signs of weakness — they're signs that you've been giving too much without refueling. Your body and mind are asking you to pause.\n\nI have a method I want to share with you called the **"2-Minute Triage"** — we categorize what's on your plate into: *must do today*, *can wait 48 hours*, and *what can I let go of entirely*. It makes the pile feel manageable again.\n\nWant to try it? Just start telling me everything that's weighing on you, and we'll sort it together.`
    ],

    anger: [
      `That frustration makes complete sense — and I'm not going to tell you to just "calm down," because your anger is telling you something important. It usually means a boundary was crossed, or something you care about deeply is being threatened.\n\nBefore we talk through it, let's do one thing: take **one long, slow breath out** — twice as long as your inhale. This actually signals your body to step out of fight-or-flight mode.\n\nNow — tell me what happened. I want to understand it from your perspective, without judgment.`,
      `Anger that intense usually has something deeper underneath it — hurt, betrayal, fear, or feeling unseen. You don't need to justify it to me; I'm not here to evaluate whether you "should" feel this way.\n\nYou should. You do. That's enough.\n\nWhat would help most right now — would you rather vent freely so I can just listen, or would you like to think through what's behind the anger together?`
    ],

    happiness: [
      `Oh, I genuinely love hearing this! There's something so beautiful about good news — and you deserve every bit of it. Tell me everything. What happened? How did it feel when you found out?\n\nI want to really *be* here for this moment with you, because joy is worth slowing down for. These are the moments that carry us through harder times, and I want to help you remember exactly how this feels.`,
      `This makes me so happy for you — actually, properly happy. You've been working toward something, or you've been through something hard, and now there's this moment of lightness. That's not small. That's everything.\n\nLet's savor it a little. What's the first thing you want to do with this good feeling?`
    ],

    loneliness: [
      `Loneliness is one of the most quietly painful human experiences — and what makes it even harder is that it often comes with the false belief that everyone else is connected and you alone are on the outside.\n\nThat's not true. But I know it doesn't feel that way right now.\n\nI'm here. And while I know I'm an AI, I genuinely care about what you're going through, and I'm listening with my full attention. Can you tell me when this loneliness started feeling this strong?`,
      `The ache of feeling unseen, like you're moving through the world without anyone really knowing you — that's one of the deepest human pains there is. I don't want to minimize it.\n\nBut I also want to gently offer this: sometimes loneliness isn't about having no one — it's about feeling like the real version of us hasn't been seen yet. Does that resonate at all?\n\nTell me about yourself. Who are you, beyond the surface? I want to actually know.`
    ],

    gratitude: [
      `That kind of gratitude — the deep, felt kind, not just the polite kind — is one of the most grounding feelings there is. Neuroscience actually shows that genuine gratitude activates the prefrontal cortex and releases dopamine and serotonin simultaneously.\n\nIn other words: what you're feeling right now is literally good for your brain. 😊\n\nWhat or who is at the center of this feeling for you today?`,
      `I love that you're feeling this. Gratitude is one of those rare emotions that grows when you share it — so please, keep going. What happened? I want to hear all of it.`
    ],

    neutral: [
      `Thank you for opening up. I'm here — fully present — and I want to understand what's going on in your world right now. There's no agenda here, no timer, no judgment.\n\nWhat's on your mind today? You can start anywhere — sometimes the smallest threads lead to the most important conversations.`,
      `I'm listening. Whatever brought you here today — whether it's something big and heavy, or just a quiet need to talk — I'm genuinely glad you're here.\n\nTell me about you. What does today feel like from the inside?`,
      `Sometimes we come to a conversation without knowing exactly what we need, and that's perfectly okay. We can figure it out together.\n\nWhat's been occupying the most space in your mind lately — even if it feels too messy or undefined to explain clearly?`
    ]
  },

  // Mode-specific overlays
  modeOverlays: {
    companion: { prefix: "", suffix: "" },
    therapist: {
      prefix: "From a therapeutic standpoint, ",
      closing: "\n\nAs we explore this together, I want to make sure you feel completely safe to go as deep or stay as surface-level as you need. This is your space. What feels right to explore next?"
    },
    coach: {
      prefix: "",
      closing: "\n\n*Coach perspective:* Every challenge contains information about what matters to you and what you're capable of. What's one small, concrete action you could take within the next 24 hours that would move you even 1% forward?"
    },
    mindful: {
      prefix: "",
      closing: "\n\n🌿 *Mindfulness note:* Whatever you're feeling right now, try to observe it like a cloud passing through the sky of your awareness — noticing it without becoming it. You are the sky. The emotion is just weather."
    }
  },

  // Memory-aware personalization
  personalizeResponse(baseResponse, profile, mode) {
    let response = baseResponse;
    const overlay = this.modeOverlays[mode] || this.modeOverlays.companion;

    // Add name if known
    if (profile.name) {
      if (Math.random() > 0.5) {
        response = response.replace(/^(I |Let |Thank |That |You |What )/, `${profile.name}, $1`);
      }
    }

    // Add mode-specific closing for non-companion modes
    if (overlay.closing && Math.random() > 0.3) {
      response += overlay.closing;
    }

    // Add memory reference occasionally
    if (profile.interests.length > 0 && Math.random() > 0.7) {
      response += `\n\nBy the way — I remember you mentioned ${profile.interests[0].toLowerCase()}. Sometimes our passions can be unexpected anchors when everything else feels unstable. Is that something that's given you any comfort lately?`;
    }

    return response;
  },

  // Mindfulness/breathing exercise responses
  mindfulnessResponses: [
    `Of course — let's do this together. I'll guide you through **Box Breathing**, which is clinically shown to reduce cortisol and calm the nervous system:\n\n📦 **Inhale** through your nose — count to 4\n📦 **Hold** your breath — count to 4\n📦 **Exhale** slowly — count to 4\n📦 **Hold** empty — count to 4\n\nRepeat this 4 times. I'll be right here when you're done. Click the **🧘 Breathe** button above for a guided visual exercise — it'll sync to your breath rhythm.\n\nHow do you feel after a round or two?`,
    `Let's ground you with the **5-4-3-2-1 technique** — it works by pulling your attention out of anxious thoughts and into the present moment:\n\n👁️ Name **5 things you can see**\n🤚 Name **4 things you can physically feel** (textures, temperature)\n👂 Name **3 things you can hear**\n👃 Name **2 things you can smell**\n👅 Name **1 thing you can taste**\n\nThis isn't just calming — it's neurologically resetting your threat response. Take a moment to go through it. I'm here when you're ready.`
  ],

  journalPrompts: [
    `Here's a reflection prompt designed to help you process what you're feeling right now:\n\n📝 *"What emotion have I been carrying quietly for the past week — and what would I say to it if I could speak to it directly?"*\n\nThere are no right answers. The goal is just to let the words flow without editing yourself. Would you like to write your response here with me?`,
    `📝 *"Describe a recent moment when you felt most like yourself — even briefly. What was happening? Who was there? What made it feel real?"*\n\nThis kind of memory can be a compass when we feel lost. Write as much or as little as you like.`,
    `📝 *"What is one story I keep telling myself that might not actually be true? What would change if I rewrote that story?"*\n\nThis one is powerful. Take your time with it. I'm here.`,
    `📝 *"If my future self — one year from now — wrote me a letter about this exact moment, what would they want me to know?"*\n\nYour future self has already made it through this. What do they see that you can't see yet?`
  ],

  generate(text, emotion, profile, mode) {
    // Select appropriate template pool
    let pool;
    if (emotion.isCrisis) {
      pool = this.templates.crisis;
    } else {
      pool = this.templates[emotion.dominant] || this.templates.neutral;
    }

    // Check for mindfulness request
    const lowerText = text.toLowerCase();
    if (/breath|breathe|mindful|meditat|calm down|ground|relax|exercise/.test(lowerText) && !emotion.isCrisis) {
      pool = this.mindfulnessResponses;
    }

    // Check for journal request
    if (/journal|reflect|write|prompt/.test(lowerText)) {
      pool = this.journalPrompts;
    }

    const baseResponse = pool[Math.floor(Math.random() * pool.length)];
    return this.personalizeResponse(baseResponse, profile, mode);
  }
};

// Export for use in app.js
window.EmotionClassifier = EmotionClassifier;
window.SentimentAnalyzer = SentimentAnalyzer;
window.ResponseEngine = ResponseEngine;
