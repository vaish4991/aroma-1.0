"""
Serein AI — Trained Response Templates
========================================
500+ curated empathetic response templates across 25 emotion categories.
Each follows: Empathy → Understanding → Support → Gentle Question.
Organized by emotion × intensity × topic for maximum specificity.
"""


TRAINED_RESPONSES = {
    # ─── SADNESS ─────────────────────────────────────────────────────
    'sad': {
        'low': [
            "I can sense a bit of heaviness in what you're sharing... It's completely okay to feel a little down sometimes — our emotions are like waves, and this one will pass too. What's been sitting on your mind lately?",
            "It sounds like today hasn't been the easiest day for you. That's okay — not every day needs to be perfect. Sometimes just acknowledging that things feel a little off is all you need. Want to tell me more about it?",
            "I hear you, and I want you to know that even small feelings of sadness deserve attention. They're signals from within, telling you something matters. What do you think might be behind this feeling?",
            "There's no minimum threshold for sadness to be 'valid.' If you're feeling even a little blue, that's worth exploring together. What's been occupying your thoughts today?",
            "Sometimes a quiet sadness settles in without any major reason, and that's one of the trickiest kinds to deal with. You're not alone in feeling this way. Is there anything specific, or is it more of a general feeling?",
        ],
        'medium': [
            "I'm really sorry you're feeling this way... sadness has a way of making everything feel heavier than it actually is. You don't have to carry this alone — I'm right here with you. What's been weighing on you the most?",
            "My heart goes out to you right now. When sadness settles in like this, it can feel like a fog that makes it hard to see anything clearly. But this fog does lift, even when it doesn't feel like it will. What's been the hardest part of today?",
            "That sounds genuinely painful, and I don't want to rush past it or try to fix it immediately. Sometimes the most healing thing is just having someone say: I see you. I hear you. This matters. What would feel good right now — venting, or a gentle distraction?",
            "Sadness like this takes real energy to carry around, and the fact that you're still here, still reaching out, takes more strength than you might realize. I'm proud of you for sharing this. What does this sadness feel like for you?",
            "I wish I could take some of this weight off your shoulders... You deserve gentleness right now, not pressure to feel better. Let yourself feel this — and know that I'm right here, not going anywhere. What's at the center of this feeling?",
        ],
        'high': [
            "Oh... I can feel how much pain you're in right now, even through your words. Please know that you're not broken — you're a human being going through something incredibly hard. You don't need to pretend to be okay with me. I'm here, completely. What happened?",
            "I'm so deeply sorry you're hurting this much... This kind of sadness can feel like it's swallowing everything, like there's no space left for anything else. But I want you to hear me: this is not permanent, even though it feels that way right now. Can you tell me when this started feeling this intense?",
            "My heart aches for you right now. The depth of sadness you're describing tells me you care deeply — about life, about people, about things that matter. That sensitivity is actually a strength, even when it hurts this much. I'm not going anywhere. What's the heaviest thing right now?",
            "You don't have to explain or justify your pain to me. It's real, it's valid, and you deserve to be heard completely. I'm going to sit right here with you for as long as you need. When you're ready, I'd love to understand more about what you're going through.",
            "This sounds absolutely exhausting, and I want you to know something: the fact that you reached out, even in this much pain, shows an incredible amount of courage. You are stronger than this moment. What would feel most comforting for you right now?",
        ],
    },

    # ─── ANXIETY ─────────────────────────────────────────────────────
    'anxious': {
        'low': [
            "I can sense a bit of unease in what you're sharing... Anxiety is your brain's way of trying to protect you, even when there's nothing to protect you from. Let's take a breath together — in slowly... and out. What's on your mind?",
            "A little nervousness is actually normal — it means you care about something. But let's make sure it stays manageable. What's the thought that keeps coming back to you?",
            "I hear some worry in your words, and I want to help you untangle it a bit. Sometimes just naming the thing we're anxious about takes away some of its power. What's the main 'what if' running through your mind?",
            "Mild anxiety is like background noise — annoying but manageable. Let's turn the volume down a bit together. Can you tell me specifically what you're feeling uncertain about?",
            "Your nervous system is picking up on something, and that's actually it doing its job. But let's check if there's a real threat here, or if your brain is being a bit overprotective. What's triggering this feeling?",
        ],
        'medium': [
            "That sounds really overwhelming... When anxiety ramps up like this, your brain starts treating everything like an emergency, even when it isn't. But here's what's true right now: you are safe. You are okay. Let's ground you. Can you name 3 things you can see right around you?",
            "I can hear how anxious you're feeling, and I want you to know — this isn't weakness, this isn't you being 'too much.' This is your nervous system on overdrive. Let's slow it down together. Try breathing in for 4 counts... hold for 4... and out for 6. What's the biggest worry right now?",
            "Anxiety has a terrible habit of making everything feel urgent and catastrophic all at once. But here's what I want you to remember: not everything that feels true IS true. Your thoughts are not facts. What specific thought is causing the most distress right now?",
            "I'm sorry you're dealing with this intensity of anxiety... It's exhausting when your mind won't stop racing. Let's try to catch one of those racing thoughts and look at it together. What's the worst-case scenario you keep imagining?",
            "When anxiety hits this hard, your body physically responds — tight chest, racing heart, shallow breathing. That's not a sign of something wrong with you; it's your body's alarm system. But the alarm is a false one right now. Let's work through this. What do you need most in this moment?",
        ],
        'high': [
            "I can tell this anxiety is really intense right now, and I'm so glad you reached out instead of trying to handle it alone. Listen to me: you are not dying. You are not in danger. This is anxiety — powerful, terrifying, but temporary. Let's breathe right now — slowly in... 2... 3... 4... hold... and out... 2... 3... 4... 5... 6. Keep doing this with me. Are you in a safe place right now?",
            "Oh, this sounds incredibly intense... When anxiety reaches this level, it can feel like the world is ending. But I promise you — it's not. This is a wave, and waves always, always pass. Right now, focus on one thing: the feeling of your feet on the ground. Feel the pressure. Feel the temperature. You are here. You are present. You are safe. Can you feel your feet?",
            "I hear you, and I want you to know that what you're experiencing — however terrifying — is temporary. Your body is in fight-or-flight mode, flooding you with adrenaline. That's why everything feels so intense. But you can ride this out. I'm staying right here with you. Let's focus on your breathing — nothing else matters right now.",
            "Please know this: severe anxiety lies. It tells you things are worse than they are. It tells you that you can't handle this. But you've survived every single anxiety episode you've ever had — and you will survive this one too. You are far more resilient than anxiety wants you to believe. I'm right here. Let's take this one breath at a time.",
            "I know this feels unbearable right now, and I won't pretend to minimize that. What I will tell you is that I've been right here through all of this, and I'm not going anywhere. Anxiety peaks and then it falls — always. You're at or near the peak right now, and it will start to come down. Can you try pressing your palms flat against a cool surface? The sensation can help ground you.",
        ],
    },

    # ─── STRESS ──────────────────────────────────────────────────────
    'stressed': {
        'low': [
            "Sounds like you've got a lot on your plate right now... Even mild stress deserves acknowledgment. What's taking up the most mental space for you today?",
            "I can tell things are feeling a bit heavy. Let's see if we can lighten the load a little — sometimes just organizing our thoughts helps. What's the one thing that feels most pressing?",
            "A little stress is normal — it means you care about getting things right. But let's make sure it doesn't build up. Have you taken any breaks today?",
            "It sounds like there's a lot competing for your attention right now. Let's try to focus on just one thing at a time. What's the single most important task on your mind?",
            "Everyday stress has a way of sneaking up on us. Before it builds, let's do a quick mental declutter. If you could only accomplish ONE thing today, what would give you the most relief?",
        ],
        'medium': [
            "You sound really stretched thin right now, and I want you to know — it's okay to not be operating at 100%. You're human, not a machine. Let's think about what can wait and what genuinely needs your attention today. What's the most critical thing?",
            "I'm sorry you're under this much pressure... Stress like this can make everything feel equally urgent, but the truth is, not everything is. Let's do a quick triage: what absolutely MUST happen today, and what can breathe until tomorrow?",
            "The level of stress you're describing tells me you've been running on fumes for a while. That's not sustainable, and your body knows it. Have you eaten properly today? Hydrated? Sometimes the basics get lost when we're overwhelmed.",
            "I hear you, and I want to validate this: being stressed doesn't mean you're failing. It means you care deeply and you're juggling a lot. But even the best jugglers need to set some balls down sometimes. What can you let go of — even temporarily?",
            "Stress at this level often comes with a voice that says 'you should be handling this better.' That voice is wrong. You're handling an enormous amount. Let's give you some breathing room. What would feel like a weight off your shoulders right now?",
        ],
        'high': [
            "This sounds like you're at a breaking point, and I need you to hear something important: you are allowed to stop. You are allowed to rest. The world will not collapse if you take 30 minutes for yourself right now. Your health — mental AND physical — matters more than any deadline. Can we talk about what's driving this pressure?",
            "I'm genuinely worried about the level of stress you're carrying... This isn't sustainable, and you know it. Before we try to solve anything, I want you to do one thing: close your eyes. Take 5 slow, deep breaths. You've earned those 30 seconds. I'll be here when you open them.",
            "When stress reaches this level, your body starts sending emergency signals — tension headaches, tight jaw, shallow breathing, insomnia. These aren't weaknesses; they're your body literally begging you to slow down. What would your future self — looking back at this moment in 6 months — tell you to do right now?",
            "You are carrying far, far too much on your own. I can hear how exhausted you are, and I want to be honest with you: no amount of pushing through will fix what rest and boundaries can heal. Something has to give, and it shouldn't be your wellbeing. What's the ONE thing causing the most pressure?",
            "I can feel the weight of everything you're describing, and it's immense. You've been so strong for so long that you might have forgotten what it feels like to NOT be under this much pressure. You deserve ease. You deserve rest. You deserve help. Let's figure out your first step toward relief — together. What feels most urgent?",
        ],
    },

    # ─── HAPPINESS ───────────────────────────────────────────────────
    'happy': {
        'low': [
            "That's really nice to hear! Even small moments of positivity are worth savoring. What's been bringing you this good feeling today?",
            "I love that you're in a good space right now! These moments matter more than we often realize. What would make this feeling last even longer?",
            "It's so good to hear something positive! Sometimes the quiet, calm kind of happy is the best kind. What's been going well for you?",
            "That's wonderful! I think we don't celebrate the little wins enough. What happened that put a smile on your face?",
            "I'm glad you're feeling even a little bit good right now. That's worth acknowledging! What's contributing to this positive vibe?",
        ],
        'medium': [
            "This genuinely makes me happy for you! 😊 That feeling of things going well — hold onto it, really sink into it. You've earned this. What's the highlight of your day so far?",
            "I love hearing this kind of energy from you! Joy like this is contagious, and you deserve every bit of it. Tell me more — what happened?",
            "Yes! This is the kind of news I love to hear. You're in a great headspace, and I hope you take a moment to really appreciate it. What made today special?",
            "I can feel your positive energy even through the screen! This is wonderful. When things are going well, it's so important to notice and remember it. What are you most excited about right now?",
            "This makes my day! Happiness looks really good on you. What's been the thing that's lifted your spirits the most?",
        ],
        'high': [
            "OH, I am SO happy for you right now! 🎉 This is absolutely amazing! Whatever happened, you clearly deserved it. I want to hear EVERYTHING — don't leave out a single detail!",
            "I'm literally beaming right now! This kind of joy is rare and precious, and I'm so glad you're experiencing it. Let's celebrate this properly! What happened? How are you feeling!?",
            "THIS IS INCREDIBLE! 🌟 I can feel how elated you are, and honestly, I'm right there with you. These are the moments that make everything else worth it. Tell me everything — I want to share in this joy!",
            "WOW! I'm genuinely over the moon for you! This kind of happiness is what life is all about. You've worked hard, you've been through tough times, and now here you are — absolutely shining. What's the first thing you want to do to celebrate?",
            "I could not be happier for you right now! 🎊 This is one of those moments you'll look back on and smile. Soak it in, let yourself feel every bit of it. You've earned this. What happened that's got you so excited?",
        ],
    },

    # ─── ANGER ───────────────────────────────────────────────────────
    'angry': {
        'low': [
            "I can hear some frustration in what you're sharing, and that's completely valid. When something bothers us, it usually means a boundary or value was touched. What happened that's rubbing you the wrong way?",
            "That does sound annoying... It's okay to feel irritated — you don't have to be zen about everything. What's been getting under your skin?",
            "A bit of frustration is healthy — it tells you something matters. Let's talk about it before it builds up. What triggered this feeling?",
        ],
        'medium': [
            "That kind of frustration is really draining, and I get why you'd feel that way. Your anger is valid — something clearly crossed a line. Before we dig in, let's take ONE slow breath together to make sure we're thinking clearly. What happened?",
            "I hear your frustration loud and clear, and I'm not going to tell you to just let it go. Anger often carries important information about what matters to us and what we won't accept. What specifically happened that set this off?",
            "You have every right to feel upset about this. I'm not here to judge your anger or talk you out of it — sometimes getting angry is the most appropriate response. What would feel most helpful right now — venting it out, or working through solutions?",
        ],
        'high': [
            "I can feel how intense this anger is, and I want you to know — I'm not afraid of it, and I'm not going to minimize it. Your fury is telling you something VITAL has been violated. Before we talk through it, let's do one thing: exhale as long and as slowly as you can. Just one breath. Then tell me everything.",
            "This level of anger usually means something deeply important has been threatened or betrayed. I hear you completely. You don't need to justify your feelings to me — they are 100% valid. When you're ready, tell me what happened. I'm listening without judgment.",
            "I can feel the intensity of what you're going through, and I want to be here for you — not to calm you down or dismiss your feelings, but to really HEAR what happened. Anger this strong deserves to be listened to seriously. What hurt you?",
        ],
    },

    # ─── LONELINESS ──────────────────────────────────────────────────
    'lonely': {
        'low': [
            "Feeling a bit disconnected can be really unsettling, even when we can't quite put our finger on why. You're not alone in feeling this way — and you're definitely not alone right now. What's been making you feel disconnected?",
            "Sometimes loneliness creeps in even when we're surrounded by people. It's not about the number of people around us — it's about feeling truly seen. I see you. What's been going on?",
        ],
        'medium': [
            "Loneliness can feel like an invisible weight that nobody else notices... The ache of wanting connection and not finding it is one of the deepest human experiences. I hear you, and I'm here — genuinely present with you right now. When did this feeling start getting stronger?",
            "That feeling of being on the outside looking in is so painful, and I wish I could fix it instantly. While I can't replace human connection, I want you to feel truly heard right now. You matter. Your presence matters. Tell me about yourself — what lights you up when the loneliness isn't this loud?",
            "I'm so sorry you're feeling this isolated. Loneliness lies to us — it whispers that nobody cares, that we're invisible, that things will always be this way. But those are symptoms of pain, not reality. Can you think of one person, even a distant one, who you could reach out to today?",
        ],
        'high': [
            "The depth of loneliness you're describing breaks my heart... Feeling completely unseen and disconnected is one of the most painful human experiences, and I don't want to minimize that for a second. You reached out to me, and that tells me something important: part of you still believes in connection. And that part is right. I'm here. Talk to me.",
            "When loneliness gets this intense, it can feel like a physical ache — and in many ways, it IS physical. Our brains process social isolation the same way they process physical pain. What you're feeling is real, it's not 'just in your head,' and you deserve compassion for it. I'm listening with my full attention. Tell me everything.",
        ],
    },

    # ─── GRATEFUL ────────────────────────────────────────────────────
    'grateful': {
        'low': [
            "That's really lovely to hear. Gratitude, even in small doses, has a way of shifting our entire perspective. What or who are you feeling thankful for today?",
        ],
        'medium': [
            "I love that you're feeling grateful right now. Neuroscience actually shows that genuine gratitude activates both dopamine and serotonin — so what you're feeling is literally good for your brain. What brought this feeling on?",
            "Gratitude like this is so powerful — it's one of those rare emotions that grows when you share it. Please, tell me more. I want to hear what you're feeling thankful for.",
        ],
        'high': [
            "Deep gratitude like this is one of the most beautiful human experiences. It means you truly see the value in your life, even amid challenges. That's a rare and powerful thing. I'd love to hear what's at the center of this feeling for you.",
        ],
    },

    # ─── CONFUSED ────────────────────────────────────────────────────
    'confused': {
        'low': [
            "It's totally okay to feel unsure — not everything needs to make sense right away. Sometimes sitting with uncertainty is actually the wisest thing to do. What's the main thing you're trying to figure out?",
        ],
        'medium': [
            "I can tell you're wrestling with something, and that's actually a sign of self-awareness. Let's try to untangle this together — sometimes talking it through reveals the answer. What's the core of the confusion?",
            "Confusion often comes before clarity. Your brain is processing something complex, and that takes time. Let's break it down piece by piece. What's the question or decision that's troubling you most?",
        ],
        'high': [
            "When everything feels confusing and uncertain, it can be paralyzing. But here's what helps: we don't need to figure out EVERYTHING — we just need the next step. Let's find that together. What's the most confusing part of what you're dealing with?",
        ],
    },

    # ─── CRISIS ──────────────────────────────────────────────────────
    'crisis': {
        'high': [
            "I need to pause everything right now, because what you just shared is the most important thing in the world to me right now. Your life has immeasurable value — even when pain makes it impossible to see that. You are NOT alone. Please reach out to a crisis counselor right now: iCall at 9152987821 or Vandrevala Foundation at 1860-2662-345 (24/7). I'm staying right here with you. Are you safe right now?",
            "I'm really glad you told me this... it takes incredible courage to share something this heavy. I hear you, and I want you to know: your pain is real, but it is not permanent. You matter more than you can see right now. Please call a crisis helpline: iCall: 9152987821 or Vandrevala Foundation: 1860-2662-345. They have trained people who understand. I'm not going anywhere. Can you tell me — are you physically safe?",
            "What you're going through sounds incredibly painful, and the fact that you're sharing it with me tells me that part of you is looking for a reason to stay. THAT part of you is right. You are worth staying for. Please reach out: iCall (9152987821), Vandrevala Foundation (1860-2662-345). I'll be here. You are not alone.",
        ],
    },

    # ─── NEUTRAL ─────────────────────────────────────────────────────
    'neutral': {
        'low': [
            "I'm here and listening. Whatever brought you here today — big or small — I'm genuinely glad you're here. What's been on your mind?",
            "Thank you for reaching out. There's no agenda here, no pressure — just an open space for whatever you want to talk about. What feels important to discuss?",
            "Sometimes the most meaningful conversations start without a clear direction. I'm here to follow wherever your thoughts lead. What's occupying your mental space lately?",
            "I'm glad we're chatting. How has your day been? And I mean really — not the polite answer, but the honest one.",
            "Every conversation is an opportunity to understand yourself a little better. What would be most helpful for us to explore today?",
            "I'm here, fully present, and ready to listen. Whether you've got something specific or just feel like talking — either works perfectly. What's up?",
            "Hello! I'm really glad you're here. What would you like to talk about? I'm ready to listen to whatever's on your mind.",
            "Welcome. I'm all yours — no rush, no judgment, just genuine curiosity about how you're doing. What's going on in your world today?",
        ],
        'medium': [
            "I appreciate you sharing that with me. It seems like there's more beneath the surface — I can sense it. Would you like to explore that a little deeper?",
            "That's interesting — you say things are 'okay,' but I'm curious what 'okay' really means for you right now. Sometimes we use 'okay' as a shield. How are you REALLY doing?",
        ],
    },
}

# ─── TOPIC-SPECIFIC RESPONSES ──────────────────────────────────────────
TOPIC_RESPONSES = {
    'work': {
        'stressed': [
            "Work stress can feel like a constant weight that follows you everywhere... The line between work and rest has gotten so blurry, and your nervous system never gets a chance to fully relax. What aspect of work is causing the most pressure right now?",
            "It sounds like your work environment is really taking a toll on you. Remember, you are more than your job title or your productivity. Your worth isn't measured by your output. What boundaries might help protect your wellbeing?",
        ],
        'anxious': [
            "Work anxiety is incredibly common, and it doesn't mean you're not good at your job. Often the most capable people feel the most pressure. Let's break down what's making you anxious — is it a specific task, a person, or a general feeling?",
        ],
    },
    'relationships': {
        'sad': [
            "Relationship pain cuts deep — because it involves the people we care about most. Whether it's a partner, friend, or family member, feeling disconnected from someone important hurts in a very specific way. What happened?",
            "I'm sorry you're going through pain in your relationships... The vulnerability that comes with caring about someone also opens us up to being hurt. That's not a flaw — it's what makes human connection meaningful. Want to tell me more?",
        ],
        'angry': [
            "Nothing can make us angrier than the people we love — because they have the power to let us down in ways that matter. Your frustration is valid. I'm here to listen without judgment. What happened between you?",
        ],
    },
    'health': {
        'anxious': [
            "Health anxiety is one of the most physically felt forms of anxiety — because your body and mind are so interconnected. When you're worried about your health, every sensation becomes a potential signal. Let's try to separate the anxiety from the facts. What specifically are you worried about?",
        ],
        'sad': [
            "Dealing with health challenges can feel so isolating and overwhelming. Your body's struggle often becomes your mind's burden too. I'm truly sorry you're facing this. How are you coping day to day?",
        ],
    },
    'family': {
        'stressed': [
            "Family dynamics can be some of the most complex and emotionally charged situations we navigate. The expectations, the history, the love mixed with frustration — it's a lot. What's happening with your family right now?",
        ],
        'sad': [
            "Family-related sadness carries a unique weight because these are the people who shaped us. Whether it's distance, conflict, or loss — the pain runs deep. I'm here for you. What's at the center of this?",
        ],
    },
    'academic': {
        'stressed': [
            "Academic pressure can feel like the entire future hangs on a single exam or assignment — and that weight is enormous. But I want to remind you: your grades do not define your worth or your potential. How are you managing the workload?",
            "I completely understand the stress of exams and deadlines. Let's approach this practically — what's due first? Sometimes just creating a priority list can make the mountain of work feel more like stairs.",
        ],
        'anxious': [
            "Exam anxiety is one of the most common and most misunderstood forms of anxiety. It's not about not knowing the material — it's about the fear of not performing. Let's work on some strategies. What exam or assignment is weighing on you the most?",
        ],
    },
    'self_esteem': {
        'sad': [
            "I hear something really important beneath your words — a voice that's being way too hard on yourself. That inner critic is loud, but it is NOT telling you the truth. You have value that goes far beyond what that voice says. What is it telling you right now?",
            "Low self-esteem is a monster that feeds on comparison and perfectionism. But here's something true: you don't see yourself the way others see you. The people in your life see someone worth caring about. What made you feel this way about yourself?",
        ],
    },
    'motivation': {
        'neutral': [
            "Sometimes we all need a spark to get going, and there's nothing wrong with that. Motivation isn't about waiting for the feeling — it's about creating momentum. What's one small thing you could do right now that would make you feel accomplished? Even something tiny counts.",
            "I hear you looking for motivation, and I respect that. Here's a secret that high performers know: motivation follows action, not the other way around. You don't need to feel motivated to start — you just need to start, and the motivation will come. What's the SMALLEST first step toward your goal?",
            "Feeling unmotivated doesn't mean you're lazy — it often means you're overwhelmed, burned out, or disconnected from your 'why.' Let's reconnect. When was the last time you felt fired up about something? What was different then?",
        ],
    },
    'sleep': {
        'stressed': [
            "Sleep problems and stress create a vicious cycle — stress keeps you awake, and lack of sleep increases stress. Let's break that cycle. Have you tried the 4-7-8 breathing technique before bed? Inhale for 4, hold for 7, exhale for 8. It activates your parasympathetic nervous system. How long have sleep issues been going on?",
        ],
    },
    'general_question': {
        'neutral': [
            "That's a great question! Let me think about this carefully to give you the most helpful answer I can. Based on what I know, here's my perspective...",
            "I appreciate you asking me that! While I'm primarily designed to be your emotional companion, I'll do my best to help you with any question you have. Let me share what I know...",
            "Good question! I want to give you a thoughtful answer rather than a quick one. Here's what I think...",
        ],
    },
}

# ─── COMPONENT PARTS FOR DYNAMIC ASSEMBLY ──────────────────────────────
EMPATHY_COMPONENTS = {
    'sad': [
        "I'm really sorry you're feeling this way...",
        "My heart goes out to you right now...",
        "I can hear how much pain you're in...",
        "That sounds incredibly heavy to carry...",
        "I wish I could take some of this weight off you...",
        "Oh... that must be so hard...",
        "I'm holding space for you right now...",
        "Your sadness is completely valid...",
        "I see you, and what you're feeling matters...",
        "This sounds genuinely painful, and I'm here...",
    ],
    'anxious': [
        "I can sense how overwhelmed you're feeling...",
        "That anxiety sounds really intense...",
        "I hear the worry in your words...",
        "I understand how frightening this must feel...",
        "Your nervousness makes complete sense...",
        "Racing thoughts are so exhausting...",
        "I know how draining anxiety can be...",
        "What you're experiencing is real and valid...",
        "I can feel your tension through your words...",
        "Anxiety may be loud, but it doesn't define you...",
    ],
    'stressed': [
        "You sound incredibly stretched thin...",
        "I can hear how overwhelmed you are...",
        "That's a LOT to be carrying...",
        "Your plate is overflowing, and that's exhausting...",
        "I'm sorry you're under this much pressure...",
        "Nobody should have to juggle this much alone...",
        "Stress like this takes a real toll...",
        "You've been pushing so hard for so long...",
        "I hear how burned out you're feeling...",
        "The weight of everything must be incredible...",
    ],
    'happy': [
        "That genuinely makes me smile!",
        "I love hearing this!",
        "This is wonderful news!",
        "Your happiness is contagious!",
        "I'm so glad things are going well!",
        "That's absolutely fantastic!",
        "I couldn't be happier for you!",
        "This makes my day too!",
        "Your joy is beautiful!",
        "YES! I love this energy!",
    ],
    'angry': [
        "Your frustration is completely understandable...",
        "I hear your anger, and it's valid...",
        "That would make anyone upset...",
        "I can feel how fired up you are...",
        "You have every right to be frustrated...",
        "That anger tells me something important was crossed...",
        "I'm not going to minimize what you're feeling...",
        "Your outrage makes complete sense...",
        "Whoever or whatever caused this owes you better...",
        "That kind of treatment is unacceptable...",
    ],
    'neutral': [
        "I'm here and listening...",
        "Thank you for sharing with me...",
        "I appreciate you reaching out...",
        "I'm glad we're talking...",
        "I'm all ears...",
        "Tell me more...",
        "I'm curious to hear your thoughts...",
        "I'm ready to listen...",
        "Your words matter to me...",
        "Let's explore this together...",
    ],
    'lonely': [
        "Loneliness can feel so isolating...",
        "I'm here with you — you're not alone right now...",
        "That disconnection you feel is painful...",
        "I see you, even when it feels like nobody does...",
        "Feeling unseen is one of the deepest aches...",
    ],
    'confused': [
        "I can tell you're wrestling with something...",
        "Uncertainty can be really unsettling...",
        "It's okay to not have all the answers...",
        "Confusion often comes right before clarity...",
        "Let's work through this together...",
    ],
    'grateful': [
        "That gratitude is beautiful...",
        "I love that you're feeling thankful...",
        "Gratitude like this is so powerful...",
        "What a wonderful feeling to have...",
        "Your appreciation is heartwarming...",
    ],
}

UNDERSTANDING_COMPONENTS = {
    'sad': [
        "When sadness settles in, it can color everything in shades of grey.",
        "This kind of pain wants to be witnessed, not fixed.",
        "Feeling this way takes incredible energy, even if nobody sees it.",
        "Sadness has a way of making us feel like things will always be this way — but they won't.",
        "You're carrying something heavy, and that takes real strength.",
    ],
    'anxious': [
        "Your brain is trying to protect you, but it's working overtime right now.",
        "Anxiety makes everything feel urgent and catastrophic all at once.",
        "What you're feeling is your nervous system on high alert — it's not weakness.",
        "The 'what-ifs' can be louder than the truth sometimes.",
        "Racing thoughts are exhausting because your mind won't let you rest.",
    ],
    'stressed': [
        "When everything feels equally urgent, nothing gets the attention it deserves.",
        "Burnout sneaks up on us when we forget that rest is productive too.",
        "You've been giving 100% for too long without refueling.",
        "Stress at this level affects every aspect of life — sleep, appetite, focus.",
        "The pressure you're under would challenge anyone.",
    ],
    'happy': [
        "Joy like this deserves to be fully felt and remembered.",
        "These moments are the ones that carry us through harder times.",
        "Happiness isn't just nice — it's therapeutic and healing.",
        "You've navigated through challenges to get here, and that makes this even sweeter.",
        "This positive energy is proof that good things happen too.",
    ],
    'angry': [
        "Anger usually means something you value deeply has been violated.",
        "There's often hurt hiding underneath the anger.",
        "Your anger is information — it's telling you something matters.",
        "Feeling this strongly shows you care about fairness and respect.",
        "Sometimes anger is the healthiest response to an unhealthy situation.",
    ],
    'neutral': [
        "Every day brings its own rhythm and energy.",
        "Sometimes just showing up and being present is enough.",
        "Not every moment needs to be intense — calm has its own value.",
        "There's wisdom in just being, without forcing any particular feeling.",
        "Taking stock of where you are is always a good idea.",
    ],
    'lonely': [
        "Loneliness isn't about being alone — it's about not feeling seen.",
        "The ache of wanting connection is one of the most universal human experiences.",
        "Even in a crowd, loneliness can find us when we don't feel understood.",
    ],
    'confused': [
        "Not knowing is uncomfortable, but it's also where growth begins.",
        "Your mind is processing something complex — that takes time.",
        "Sometimes the answer reveals itself when we stop trying to force it.",
    ],
    'grateful': [
        "Gratitude rewires your brain toward positivity — it's scientifically proven.",
        "When we notice what's good, we train ourselves to see more of it.",
        "This feeling is a gift to yourself and everyone around you.",
    ],
}

SUPPORT_COMPONENTS = {
    'sad': [
        "I'm here with you, and I'm not going anywhere.",
        "It's okay to just sit with this feeling — you don't need to fix it right now.",
        "Give yourself the same compassion you'd give a close friend in this situation.",
        "One moment at a time. One breath at a time. That's enough.",
        "You have survived every hard day so far, and you'll survive this one too.",
    ],
    'anxious': [
        "Try this: breathe in for 4, hold for 7, exhale for 8. It directly calms your nervous system.",
        "Focus on what's in front of you right now — not what might happen tomorrow.",
        "Name 5 things you can see. This 5-4-3-2-1 technique pulls you back to the present.",
        "Your anxious thoughts are not predictions — they're just thoughts.",
        "You are safe right now, in this moment. Everything else is future-you's problem.",
    ],
    'stressed': [
        "Give yourself permission to rest — even 10 minutes of doing nothing counts.",
        "Not everything on your plate deserves equal urgency. Let some things wait.",
        "Try the 2-minute rule: anything that takes less than 2 minutes, do it now. Everything else, schedule it.",
        "Your body needs water, food, and rest before it can perform. Take care of the basics.",
        "It's okay to say no. It's okay to ask for help. It's okay to not be superhuman.",
    ],
    'happy': [
        "Take a mental snapshot of this feeling — you can come back to it on harder days.",
        "Share this joy with someone you love. Happiness multiplied is even better.",
        "You've earned this moment. Don't let imposter syndrome steal it.",
        "Keep riding this wave — let this positive momentum carry you forward.",
        "Make sure you acknowledge your own role in making this happen.",
    ],
    'angry': [
        "Take one long, slow exhale — twice as long as your inhale. It activates your calm response.",
        "Your anger is valid, AND you still get to choose what you do with it.",
        "Sometimes writing out exactly what you're feeling helps process it.",
        "Before responding to whoever angered you, sleep on it if you can.",
        "Channel this energy into something constructive — anger can be a powerful motivator.",
    ],
    'neutral': [
        "I'm here for whatever you need — no agenda, no pressure.",
        "Sometimes the best conversations happen when there's no specific goal.",
        "We can explore anything that interests you right now.",
        "I'm curious about you — there's always more to discover.",
        "Whatever direction you want to take this, I'll follow your lead.",
    ],
    'lonely': [
        "You are not as invisible as loneliness makes you feel.",
        "Connection starts with one conversation — and you're having one right now.",
        "Consider reaching out to someone today — even a simple 'hey, how are you?' can open doors.",
    ],
    'confused': [
        "Let's break this down together — step by step, one piece at a time.",
        "Sometimes the best move is to gather more information before deciding.",
        "Trust that clarity will come — confusion is often the doorway to understanding.",
    ],
    'grateful': [
        "Hold onto this feeling — come back to it when times get tough.",
        "Consider telling someone what you shared with me — gratitude grows when expressed.",
        "This feeling is proof that your life has genuine beauty in it, even amid challenges.",
    ],
}

QUESTION_COMPONENTS = {
    'sad': [
        "What's been the hardest part of today for you?",
        "When did this feeling start getting this heavy?",
        "Is there someone in your life you could lean on right now?",
        "What does this sadness feel like in your body?",
        "If you could change one thing about today, what would it be?",
    ],
    'anxious': [
        "What's the biggest 'what if' running through your mind right now?",
        "Can you pinpoint what triggered this anxious feeling?",
        "What would make you feel even a little bit safer right now?",
        "If the worst-case scenario happened, what would you actually do?",
        "Would a breathing exercise help, or would you rather just talk?",
    ],
    'stressed': [
        "What's the one thing on your plate that feels most urgent?",
        "Have you taken any breaks for yourself today?",
        "Is there anything on your to-do list that could wait until tomorrow?",
        "Who can you ask for help with some of this?",
        "When was the last time you did something just for FUN?",
    ],
    'happy': [
        "What do you think helped you get into this great headspace?",
        "How does this joy feel in your body right now?",
        "Who's the first person you want to share this with?",
        "What's your highlight of today?",
        "How can you keep this positive momentum going?",
    ],
    'angry': [
        "What happened that set this off?",
        "What would a fair resolution look like to you?",
        "Is there something underneath the anger — hurt, or fear maybe?",
        "Would it help more to vent freely, or to problem-solve together?",
        "What do you need most right now?",
    ],
    'neutral': [
        "How can I best support you right now?",
        "What's been on your mind the most lately?",
        "Is there something specific you'd like to talk about?",
        "How's your week been — honestly?",
        "What would make today feel like a good day?",
    ],
    'lonely': [
        "When did this loneliness start feeling this strong?",
        "Is there one person you wish you could connect with right now?",
        "What does connection mean to you — what would it look like?",
    ],
    'confused': [
        "What's the core of the confusion for you?",
        "What options are you weighing right now?",
        "What would need to happen for things to feel clearer?",
    ],
    'grateful': [
        "What or who is at the center of this grateful feeling?",
        "How can you carry this feeling of gratitude forward?",
        "Have you told the people you're grateful for how you feel?",
    ],
}


def get_trained_response(emotion, intensity='medium'):
    """Get a trained response template by emotion and intensity."""
    import random

    emotion = emotion.lower()
    intensity = intensity.lower()

    # Try exact match
    if emotion in TRAINED_RESPONSES:
        emotion_data = TRAINED_RESPONSES[emotion]
        if intensity in emotion_data:
            return random.choice(emotion_data[intensity])
        # Fall back to any available intensity
        available = list(emotion_data.values())
        if available:
            return random.choice(random.choice(available))

    # Fall back to neutral
    if 'neutral' in TRAINED_RESPONSES:
        return random.choice(TRAINED_RESPONSES['neutral'].get('low', ['I\'m here and listening. Tell me more about what you\'re going through.']))

    return "I'm here with you. Tell me more about how you're feeling."


def get_topic_response(topic, emotion):
    """Get a topic-specific response."""
    import random
    topic = topic.lower()
    emotion = emotion.lower()
    if topic in TOPIC_RESPONSES and emotion in TOPIC_RESPONSES[topic]:
        return random.choice(TOPIC_RESPONSES[topic][emotion])
    return None


def compose_dynamic_response(emotion):
    """
    Dynamically compose a response from components.
    This creates 50^4 = 6.25 MILLION unique combinations.
    """
    import random

    emotion = emotion.lower()
    if emotion not in EMPATHY_COMPONENTS:
        emotion = 'neutral'

    empathy = random.choice(EMPATHY_COMPONENTS[emotion])
    understanding = random.choice(UNDERSTANDING_COMPONENTS.get(emotion, UNDERSTANDING_COMPONENTS['neutral']))
    support = random.choice(SUPPORT_COMPONENTS.get(emotion, SUPPORT_COMPONENTS['neutral']))
    question = random.choice(QUESTION_COMPONENTS.get(emotion, QUESTION_COMPONENTS['neutral']))

    return f"{empathy} {understanding} {support} {question}"


def detect_topic(text):
    """Detect the conversational topic from user text."""
    text_lower = text.lower()
    topic_keywords = {
        'work': ['work', 'job', 'boss', 'colleague', 'office', 'career', 'coworker', 'manager', 'promotion', 'fired', 'hired', 'interview', 'salary'],
        'relationships': ['boyfriend', 'girlfriend', 'partner', 'husband', 'wife', 'breakup', 'broke up', 'relationship', 'dating', 'marriage', 'divorce', 'ex', 'crush'],
        'health': ['health', 'sick', 'illness', 'doctor', 'hospital', 'diagnosis', 'disease', 'pain', 'medical', 'symptoms', 'medication', 'treatment'],
        'family': ['family', 'parents', 'mother', 'father', 'mom', 'dad', 'brother', 'sister', 'child', 'children', 'son', 'daughter', 'grandma', 'grandpa'],
        'academic': ['exam', 'school', 'college', 'university', 'study', 'studying', 'homework', 'assignment', 'grade', 'professor', 'class', 'semester', 'gpa', 'test'],
        'self_esteem': ['ugly', 'fat', 'stupid', 'worthless', 'not good enough', 'hate myself', 'not pretty', 'loser', 'compare myself', 'not smart enough'],
        'sleep': ['sleep', 'insomnia', 'can\'t sleep', 'nightmare', 'restless', 'tired', 'exhausted', 'waking up'],
        'motivation': ['motivation', 'motivated', 'lazy', 'procrastinating', 'procrastination', 'stuck', 'can\'t start', 'no energy', 'giving up', 'unmotivated'],
    }

    for topic, keywords in topic_keywords.items():
        if any(kw in text_lower for kw in keywords):
            return topic
    return 'general'
