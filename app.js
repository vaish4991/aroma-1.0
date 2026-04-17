/**
 * EMORA AI — Main Application Controller
 * Integrates: Emotion Recognition, NLP, Voice Input, Webcam,
 * Wearables Simulation, Crisis Protocol, Memory Engine, Analytics
 */

// ── STATE ──────────────────────────────────────────────────────────────────
const STORAGE_KEY = 'emora-ai-state-v2';
const appState = {
  mode: 'companion',
  messages: [],
  sessionCount: 1,
  profile: {
    name: '',
    interests: [],
    lifeEvents: [],
    recentMood: 'calm',
    emotionHistory: [],
    riskScore: 0,
    engagementScore: 100
  },
  currentEmotion: { dominant: 'neutral', confidence: 70, isCrisis: false, riskScore: 0 },
  emotionBars: { joy: 60, calm: 45, stress: 20, sadness: 10, anxiety: 15 },
  moodChartData: [],
  webcamActive: false,
  voiceActive: false
};

// ── DOM REFS ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const chatLog      = $('chatLog');
const chatInput    = $('chatInput');
const sendBtn      = $('sendBtn');
const typingInd    = $('typingIndicator');
const nlpInd       = $('nlpIndicator');
const voiceBtn     = $('voiceBtn');
const voiceVis     = $('voiceVisualizer');
const camToggleBtn = $('camToggleBtn');
const webcamFeed   = $('webcamFeed');
const crisisOverlay = $('crisisOverlay');
const mindfulOverlay = $('mindfulOverlay');
const modeGrid     = $('modeGrid');
const suggestions  = $('suggestions');
const charCount    = $('charCount');
const statusText   = $('statusText');

// ── INIT ───────────────────────────────────────────────────────────────────
function init() {
  loadState();
  bindEvents();
  initWearablesSimulation();
  initHeartCanvas();
  initMoodChart();
  populateAmbientParticles();
  syncModeUI();
  updateMemoryUI();

  // Initialise AI engine with saved conversation history
  if (window.AIEngine) {
    AIEngine.init(appState.messages);
    // Show live AI status badge using getStatus()
    const status = AIEngine.getStatus();
    const sub    = document.querySelector('.header-sub');
    if (sub) {
      const badge = document.createElement('span');
      badge.style.cssText = `margin-left:8px;font-size:9px;color:${status.color};font-weight:700;vertical-align:middle;`;
      badge.textContent   = status.label;
      badge.id            = 'aiModeBadge';
      badge.title         = 'AI stack: ' + status.label;
      sub.appendChild(badge);
    }
  }

  if (appState.messages.length === 0) {
    setTimeout(() => addAIMessage(getWelcomeMessage()), 800);
  } else {
    renderAllMessages();
    updateMemoryUI();
  }

  // Auto-grow textarea
  chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 160) + 'px';
    charCount.textContent = `${chatInput.value.length}/2000`;
  });
}

function getWelcomeMessage() {
  // Use companion name if configured
  let compName = 'Emora', compStyle = '';
  try {
    const c = JSON.parse(localStorage.getItem('emora_companion') || '{}');
    if (c.name)  compName  = c.name;
    if (c.style) compStyle = ` — your ${c.style.toLowerCase()} companion`;
  } catch {}

  // Greet user by name if known
  let greeting = 'Hey there 🌟';
  try {
    const s = JSON.parse(localStorage.getItem('emora_session') || '{}');
    const fn = (s.name || '').split(' ')[0].split('@')[0];
    if (fn && fn.length > 1) greeting = `Hey ${fn} 🌟`;
  } catch {}

  const aiStack = window.AIEngine?.isUsingGPT() ? 'GPT-4o + 4-model BERT Ensemble' : 'multimodal emotion analysis';

  return `${greeting} I'm **${compName}**${compStyle} — your AI emotional companion.\n\nI'm here to listen, understand, and support you — without judgment, without rushing. I use **${aiStack}** to understand exactly how you're feeling and respond with real empathy — not scripted lines.\n\nTalk to me about *anything* — anxiety, stress, relationships, loneliness, big wins, or just a feeling you can't quite name.\n\n**What's on your mind today?** I'm fully here — just for you. 💙`;
}

// ── EVENT BINDING ──────────────────────────────────────────────────────────
function bindEvents() {
  const onIfExists = (id, event, handler) => {
    const el = $(id);
    if (el) el.addEventListener(event, handler);
  };

  // Send
  sendBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  });

  // Suggestions
  document.querySelectorAll('.suggestion-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      chatInput.value = btn.dataset.text;
      chatInput.dispatchEvent(new Event('input'));
      handleSend();
    });
  });

  // Mode buttons
  modeGrid.addEventListener('click', e => {
    const btn = e.target.closest('[data-mode]');
    if (!btn) return;
    appState.mode = btn.dataset.mode;
    syncModeUI();
    persistState();
    if (appState.mode === 'mindful') {
      setTimeout(() => addAIMessage(`🧘 Mindfulness mode activated. I'll approach our conversation with extra presence, gentleness, and somatic awareness. Every response will include grounding techniques.\n\nWould you like to start with a breathing exercise, or shall we talk first?`), 200);
    } else {
      const modeMessages = {
        companion: `Companion mode on 🫂 Think of me as your trusted friend who happens to understand psychology really well. No formality, just honest support.`,
        therapist: `Therapist mode on 🧠 I'll guide our conversation with evidence-based techniques — CBT, DBT, acceptance-based approaches. This is a safe, structured space.`,
        coach: `Life Coach mode on 💪 Let's focus on action, growth, and forward momentum. What goal or challenge shall we dig into?`
      };
      setTimeout(() => addAIMessage(modeMessages[appState.mode]), 200);
    }
  });

  // Voice
  voiceBtn.addEventListener('click', handleVoiceInput);

  // Webcam
  camToggleBtn.addEventListener('click', toggleWebcam);

  // Crisis
  onIfExists('crisisClose', 'click', () => {
    crisisOverlay.classList.add('hidden');
    addAIMessage(`I'm relieved you're safe. I'm right here with you — and that conversation isn't over. Whenever you're ready to keep talking, I'm listening. You don't have to carry this alone. 💙`);
  });

  // Mindfulness
  onIfExists('mindfulBtn', 'click', () => {
    mindfulOverlay.classList.remove('hidden');
  });
  onIfExists('mindfulClose', 'click', () => {
    mindfulOverlay.classList.add('hidden');
    stopBreathing();
  });
  onIfExists('startBreathe', 'click', startBreathingExercise);

  // Journal
  onIfExists('journalBtn', 'click', () => {
    const prompts = ResponseEngine.journalPrompts;
    const prompt = prompts[Math.floor(Math.random() * prompts.length)];
    addAIMessage(prompt);
    chatLog.scrollTop = chatLog.scrollHeight;
  });

  // Reset
  onIfExists('resetBtn', 'click', () => {
    if (confirm('Reset this session? All memory will be cleared.')) {
      localStorage.removeItem(STORAGE_KEY);
      window.location.reload();
    }
  });

  // Banner close
  onIfExists('bannerClose', 'click', () => {
    const banner = $('techBanner');
    if (banner) banner.style.display = 'none';
  });

  // Sidebar toggle (mobile)
  onIfExists('sidebarToggle', 'click', () => {
    document.querySelector('.sidebar').classList.toggle('open');
  });
}

// ── SEND / PROCESS ─────────────────────────────────────────────────────────
async function handleSend() {
  const text = chatInput.value.trim();
  if (!text) return;

  chatInput.value = '';
  chatInput.style.height = 'auto';
  charCount.textContent = '0/2000';
  suggestions.style.display = 'none';

  // Add user message
  addUserMessage(text);

  // Extract memory from text
  extractMemory(text);

  // Classify emotion
  const emotion = EmotionClassifier.classify(text);
  const sentiment = SentimentAnalyzer.analyze(text);
  appState.currentEmotion = emotion;

  // Update emotion UI
  updateEmotionBars(emotion);
  updateAnalytics(emotion, sentiment);
  updateAvatarEmotion(emotion.dominant);

  // Update profile
  appState.profile.riskScore = emotion.riskScore;
  updateMemoryUI();
  persistState();

  // Crisis check
  if (emotion.isCrisis) {
    crisisOverlay.classList.remove('hidden');
    appState.profile.riskScore = 10;
    $('memRisk').textContent = '⚠️ HIGH';
    $('memRisk').className = 'mem-val risk';
    updateMemoryUI();
  }

  // Show NLP processing animation
  await showNLPProcessing();

  // Show typing indicator
  typingInd.classList.remove('hidden');
  chatLog.scrollTop = chatLog.scrollHeight;

  // Get companion persona for system prompt injection
  let companion = {};
  try { companion = JSON.parse(localStorage.getItem('emora_companion') || '{}'); } catch {}

  let response;
  let finalEmotion = emotion;
  try {
    if (window.AIEngine) {
      // GPT-4o + BERT Ensemble — both run in parallel inside AIEngine.process
      const result = await AIEngine.process(text, appState.profile, appState.mode, emotion, companion);
      response     = sanitizeAIResponse(result?.text);
      finalEmotion = result.emotion || emotion;

      // Re-update emotion UI with more accurate BERT ensemble results
      if (finalEmotion.source === 'bert-ensemble') {
        updateEmotionBars(finalEmotion);
        updateAvatarEmotion(finalEmotion.dominant);
        appState.currentEmotion = finalEmotion;

        // Crisis re-check with BERT result (may catch what keyword check missed)
        if (finalEmotion.isCrisis && !crisisOverlay.classList.contains('shown')) {
          crisisOverlay.classList.remove('hidden');
          crisisOverlay.classList.add('shown');
          appState.profile.riskScore = 10;
          $('memRisk').textContent = '⚠️ HIGH';
          $('memRisk').className   = 'mem-val risk';
          updateMemoryUI();
        }
      }

      // Update analytics with BERT sentiment
      if (result.bert) {
        const merged = { ...sentiment, ...result.bert };
        updateAnalytics(finalEmotion, merged);
      }
    } else {
      await sleep(1200 + Math.random() * 800);
      response = sanitizeAIResponse(ResponseEngine.generate(text, emotion, appState.profile, appState.mode));
    }
  } catch (err) {
    console.error('[Emora] AI error:', err);
    response = sanitizeAIResponse(ResponseEngine.generate(text, emotion, appState.profile, appState.mode));
  }

  typingInd.classList.add('hidden');
  addAIMessage(sanitizeAIResponse(response), finalEmotion);

  // Track mood point
  appState.moodChartData.push({
    time: Date.now(),
    emotion: emotion.dominant,
    score: getEmotionScore(emotion.dominant)
  });
  drawMoodChart();
  persistState();
}

// ── NLP ANIMATION ──────────────────────────────────────────────────────────
async function showNLPProcessing() {
  nlpInd.classList.remove('hidden');
  const steps = ['nlpStep1','nlpStep2','nlpStep3','nlpStep4'];

  for (let i = 0; i < steps.length; i++) {
    steps.forEach((s, idx) => {
      const el = $(s);
      el.classList.toggle('active', idx === i);
      el.classList.toggle('done', idx < i);
    });
    await sleep(280);
  }

  steps.forEach(s => {
    $(s).classList.remove('active');
    $(s).classList.add('done');
  });
  await sleep(150);
  nlpInd.classList.add('hidden');
  steps.forEach(s => {
    $(s).classList.remove('done', 'active');
  });
}

// ── MESSAGE RENDERING ──────────────────────────────────────────────────────
function addUserMessage(text) {
  appState.messages.push({ role: 'user', text, time: Date.now() });
  renderMessage({ role: 'user', text, time: Date.now() });
}

function addAIMessage(text, emotion = null) {
  const msg = { role: 'ai', text, time: Date.now(), emotion: emotion?.dominant };
  appState.messages.push(msg);
  streamMessage(msg);
}

function renderAllMessages() {
  chatLog.innerHTML = '';
  appState.messages.forEach(msg => renderMessage(msg, false));
}

function renderMessage(msg, scroll = true) {
  const row = document.createElement('div');
  row.className = `message-row ${msg.role}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = msg.role === 'ai' ? '🤖' : '👤';

  const content = document.createElement('div');
  content.className = 'msg-content';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = formatMessageText(msg.text);

  const meta = document.createElement('div');
  meta.className = 'msg-meta';

  const time = document.createElement('span');
  time.className = 'msg-time';
  time.textContent = formatTime(msg.time);
  meta.appendChild(time);

  if (msg.role === 'ai' && msg.emotion && msg.emotion !== 'neutral') {
    const tag = document.createElement('span');
    tag.className = 'msg-emotion-tag';
    tag.textContent = `${getEmotionEmoji(msg.emotion)} ${capitalize(msg.emotion)} detected`;
    meta.appendChild(tag);
  }

  content.appendChild(bubble);
  content.appendChild(meta);
  row.appendChild(avatar);
  row.appendChild(content);
  chatLog.appendChild(row);

  if (scroll) chatLog.scrollTop = chatLog.scrollHeight;
}

// Stream text character by character (ChatGPT-like)
function streamMessage(msg) {
  const row = document.createElement('div');
  row.className = `message-row ai`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = '🤖';

  const content = document.createElement('div');
  content.className = 'msg-content';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';

  const cursor = document.createElement('span');
  cursor.className = 'stream-cursor';

  const meta = document.createElement('div');
  meta.className = 'msg-meta';

  const time = document.createElement('span');
  time.className = 'msg-time';
  time.textContent = formatTime(msg.time);

  content.appendChild(bubble);
  content.appendChild(meta);
  row.appendChild(avatar);
  row.appendChild(content);
  chatLog.appendChild(row);

  // Stream character by character
  const fullText = sanitizeAIResponse(msg?.text);
  let i = 0;
  const speed = Math.max(8, Math.min(20, 2000 / fullText.length)); // adaptive speed

  bubble.innerHTML = '';
  bubble.appendChild(cursor);

  function streamNext() {
    if (i < fullText.length) {
      cursor.remove();
      bubble.innerHTML = formatMessageText(fullText.slice(0, i + 1));
      bubble.appendChild(cursor);
      i++;
      chatLog.scrollTop = chatLog.scrollHeight;
      setTimeout(streamNext, speed);
    } else {
      cursor.remove();
      bubble.innerHTML = formatMessageText(fullText);

      // Add meta
      meta.appendChild(time);
      if (msg.emotion && msg.emotion !== 'neutral') {
        const tag = document.createElement('span');
        tag.className = 'msg-emotion-tag';
        tag.textContent = `${getEmotionEmoji(msg.emotion)} ${capitalize(msg.emotion)} detected`;
        meta.appendChild(tag);
      }
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  }

  streamNext();
}

// Format **bold**, *italic*, line breaks
function formatMessageText(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n\n/g, '</p><p style="margin-top:10px">')
    .replace(/\n/g, '<br>');
}

// ── EMOTION BARS UPDATE ────────────────────────────────────────────────────
function updateEmotionBars(emotion) {
  const emotionMap = {
    happiness: { joy: 90, calm: 50, stress: 10, sadness: 5, anxiety: 8 },
    sadness:   { joy: 15, calm: 20, stress: 30, sadness: 85, anxiety: 35 },
    anxiety:   { joy: 20, calm: 15, stress: 70, sadness: 40, anxiety: 90 },
    stress:    { joy: 25, calm: 20, stress: 85, sadness: 35, anxiety: 65 },
    anger:     { joy: 10, calm: 10, stress: 80, sadness: 25, anxiety: 45 },
    loneliness:{ joy: 20, calm: 30, stress: 40, sadness: 70, anxiety: 50 },
    neutral:   { joy: 60, calm: 60, stress: 20, sadness: 10, anxiety: 15 },
    gratitude: { joy: 80, calm: 70, stress: 10, sadness: 5, anxiety: 5 },
    crisis:    { joy: 5,  calm: 5,  stress: 90, sadness: 95, anxiety: 90 },
    severe_distress: { joy: 10, calm: 10, stress: 80, sadness: 90, anxiety: 80 }
  };

  const bars = emotionMap[emotion.dominant] || emotionMap.neutral;

  Object.entries(bars).forEach(([key, pct]) => {
    const variance = Math.floor((Math.random() - 0.5) * 15);
    const finalPct = Math.max(3, Math.min(97, pct + variance));
    const bar = $(`bar${capitalize(key)}`);
    const pctEl = $(`pct${capitalize(key)}`);
    if (bar) { bar.style.width = finalPct + '%'; }
    if (pctEl) { pctEl.textContent = finalPct + '%'; }
  });

  appState.emotionBars = bars;

  // Update emotion badge
  const badge = $('emotionBadge');
  if (badge) {
    badge.textContent = `${getEmotionEmoji(emotion.dominant)} ${capitalize(emotion.dominant)}`;
  }
}

// ── ANALYTICS UPDATE (safe for pages without analytics panel) ──────────────
function updateAnalytics(emotion, sentiment) {
  const dominantEl = $('dominantEmo');
  const riskScoreEl = $('riskScore');
  const engagementEl = $('engagementScore');
  const confidenceEl = $('nlpConfidence');

  if (dominantEl) dominantEl.textContent = capitalize(emotion?.dominant || 'neutral');
  if (riskScoreEl) {
    const risk = Number(emotion?.riskScore || 0);
    riskScoreEl.textContent = `${Math.min(10, Math.max(0, Math.round(risk)))}/10`;
    riskScoreEl.className = risk >= 7 ? 'risk' : risk >= 3 ? '' : 'safe';
  }
  if (engagementEl) {
    const negative = Number(sentiment?.negative || 0);
    engagementEl.textContent = negative >= 70 ? 'Low' : negative >= 45 ? 'Medium' : 'High';
  }
  if (confidenceEl) confidenceEl.textContent = `${Math.min(99, Math.max(1, Number(emotion?.confidence || 70)))}%`;
}

function updateAvatarEmotion(dominant) {
  const mouth = $('avMouth');
  if (!mouth) return;
  if (['happiness','gratitude'].includes(dominant)) {
    mouth.style.borderRadius = '0 0 20px 20px';
    mouth.style.borderTop = 'none';
    mouth.style.borderBottom = '2px solid white';
    mouth.style.top = 'auto';
    mouth.style.bottom = '14px';
  } else if (['sadness','crisis','severe_distress'].includes(dominant)) {
    mouth.style.borderRadius = '20px 20px 0 0';
    mouth.style.borderBottom = 'none';
    mouth.style.borderTop = '2px solid white';
    mouth.style.bottom = '10px';
  } else {
    mouth.style.borderRadius = '0 0 20px 20px';
    mouth.style.borderTop = 'none';
    mouth.style.borderBottom = '2px solid white';
    mouth.style.bottom = '14px';
  }

  // Update status text
  const statusMessages = {
    happiness: 'Sharing your joy 🌟',
    sadness: 'Holding space gently 💙',
    anxiety: 'Calming with you 🌿',
    stress: 'Grounding together 🧘',
    anger: 'Listening without judgment 🤝',
    loneliness: 'Here with you 🫂',
    crisis: 'Prioritizing your safety 🆘',
    neutral: 'Present and listening 💫',
    gratitude: 'Feeling this with you ✨'
  };
  statusText.textContent = statusMessages[dominant] || 'Listening with empathy';
}

// ── MEMORY EXTRACTION ──────────────────────────────────────────────────────
function extractMemory(text) {
  const clean = text.trim();

  const nameMatch = clean.match(/(?:i am|i'm|my name is|call me|i go by)\s+([A-Z][a-z]+|[a-z]{2,20})/i);
  if (nameMatch) appState.profile.name = capitalize(nameMatch[1]);

  const interestMatch = clean.match(/(?:i love|i like|i enjoy|i'm into|passionate about)\s+([^.!?]+)/i);
  if (interestMatch) {
    const interests = interestMatch[1].split(/,|and/).map(s => s.trim()).filter(s => s.length > 1).slice(0,3);
    interests.forEach(interest => {
      if (!appState.profile.interests.includes(interest)) {
        appState.profile.interests.push(capitalize(interest));
      }
    });
    appState.profile.interests = appState.profile.interests.slice(0,5);
  }

  const eventCues = /(birthday|exam|job|breakup|wedding|graduation|promotion|loss|death|baby|divorce|moving)/i;
  if (eventCues.test(clean)) {
    const event = clean.slice(0, 100);
    if (!appState.profile.lifeEvents.includes(event)) {
      appState.profile.lifeEvents.unshift(event);
      appState.profile.lifeEvents = appState.profile.lifeEvents.slice(0, 5);
    }
  }

  updateMemoryUI();
}

function updateMemoryUI() {
  const p = appState.profile;
  $('memName').textContent = p.name || 'Learning...';
  $('memMood').textContent = capitalize(appState.currentEmotion.dominant);
  $('memInterests').textContent = p.interests.slice(0,2).join(', ') || '—';
  $('memSessions').textContent = appState.sessionCount;

  const risk = appState.currentEmotion.riskScore;
  const riskEl = $('memRisk');
  if (risk >= 7) { riskEl.textContent = '⚠️ HIGH'; riskEl.className = 'mem-val risk'; }
  else if (risk >= 3) { riskEl.textContent = '⚡ MODERATE'; riskEl.className = 'mem-val'; riskEl.style.color = '#f59e0b'; }
  else { riskEl.textContent = 'Safe ✓'; riskEl.className = 'mem-val safe'; }
}



// ── VOICE INPUT ────────────────────────────────────────────────────────────
let recognition = null;

function handleVoiceInput() {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    addSystemToast('⚠️ Voice input requires Chrome or Edge browser');
    return;
  }

  if (appState.voiceActive) {
    stopVoice();
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onstart = () => {
    appState.voiceActive = true;
    voiceBtn.classList.add('recording');
    voiceVis.classList.remove('hidden');
    chatInput.placeholder = '🎤 Listening... speak now';
  };

  recognition.onresult = e => {
    const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
    chatInput.value = transcript;
    chatInput.dispatchEvent(new Event('input'));
  };

  recognition.onend = () => {
    stopVoice();
    if (chatInput.value.trim()) {
      setTimeout(handleSend, 500);
    }
  };

  recognition.onerror = () => { stopVoice(); };
  recognition.start();
}

function stopVoice() {
  appState.voiceActive = false;
  voiceBtn.classList.remove('recording');
  voiceVis.classList.add('hidden');
  chatInput.placeholder = "Tell me what's on your mind... I'm here to listen 💙";
  if (recognition) { try { recognition.stop(); } catch(e){} }
}

// ── WEBCAM / FACIAL EMOTION ────────────────────────────────────────────────
const faceEmotions = ['Happy 😊','Calm 😌','Surprised 😮','Neutral 😐','Thoughtful 🤔','Worried 😟','Sad 😔'];
let faceScanInterval = null;

function toggleWebcam() {
  if (appState.webcamActive) {
    appState.webcamActive = false;
    camToggleBtn.textContent = '🎥 Enable Camera';
    camToggleBtn.classList.remove('active');
    webcamFeed.classList.add('hidden');
    webcamFeed.srcObject = null;
    $('camPlaceholder').style.display = '';
    $('faceDetectionOverlay').style.display = 'none';
    $('detectedFaceEmotion').classList.add('hidden');
    if (faceScanInterval) clearInterval(faceScanInterval);
    $('wearablesTechItem').classList.add('active');
  } else {
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      .then(stream => {
        appState.webcamActive = true;
        webcamFeed.srcObject = stream;
        webcamFeed.classList.remove('hidden');
        camToggleBtn.textContent = '🚫 Disable Camera';
        camToggleBtn.classList.add('active');
        $('camPlaceholder').style.display = 'none';
        $('faceDetectionOverlay').style.display = '';
        $('detectedFaceEmotion').classList.remove('hidden');
        startFaceEmotionSimulation();
      })
      .catch(() => {
        addSystemToast('Camera access denied. Using text + voice analysis instead.');
      });
  }
}

function startFaceEmotionSimulation() {
  const faceBox = $('faceBox');
  const faceLabel = $('faceLabel');
  const faceEmotionText = $('faceEmotionText');

  // Simulate face detection box
  faceBox.style.cssText = `top:15%;left:25%;width:50%;height:65%;`;

  faceScanInterval = setInterval(() => {
    const detectedEmotion = faceEmotions[Math.floor(Math.random() * faceEmotions.length)];
    faceLabel.textContent = detectedEmotion;
    faceEmotionText.textContent = detectedEmotion;

    // Slightly move detection box
    const jitter = () => Math.floor((Math.random()-0.5)*4);
    faceBox.style.top = `${15+jitter()}%`;
    faceBox.style.left = `${22+jitter()}%`;
  }, 2000);
}

// ── WEARABLES SIMULATION ───────────────────────────────────────────────────
function initWearablesSimulation() {
  let bpm = 72;
  setInterval(() => {
    // Simulate heart rate based on emotion
    const emotion = appState.currentEmotion.dominant;
    const baseBPM = { happiness: 78, sadness: 62, anxiety: 98, stress: 92, anger: 105, neutral: 72, crisis: 115, gratitude: 70, loneliness: 65 };
    const target = baseBPM[emotion] || 72;
    bpm = bpm + (target - bpm) * 0.1 + (Math.random()-0.5)*3;
    bpm = Math.max(55, Math.min(120, bpm));
    $('heartRate').textContent = Math.round(bpm);

    // Stress level
    const stressEl = $('stressLevel');
    if (bpm > 95) { stressEl.textContent = 'High'; stressEl.style.color = '#ef4444'; }
    else if (bpm > 82) { stressEl.textContent = 'Moderate'; stressEl.style.color = '#f59e0b'; }
    else { stressEl.textContent = 'Low'; stressEl.style.color = '#10b981'; }

    // HRV
    const hrv = Math.round(80 - (bpm-60) * 0.6 + (Math.random()-0.5)*5);
    $('hrvScore').textContent = Math.max(20, hrv);

    // Sleep (static-ish)
    $('sleepScore').textContent = (6.5 + Math.random()*2).toFixed(1);
  }, 1500);
}

// ── HEART WAVE CANVAS ──────────────────────────────────────────────────────
function initHeartCanvas() {
  const canvas = $('heartCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let offset = 0;

  function drawWave() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 1.5;
    ctx.shadowBlur = 8;
    ctx.shadowColor = '#ef4444';

    for (let x = 0; x < canvas.width; x++) {
      const t = (x + offset) / 20;
      // ECG-like pattern
      let y;
      const phase = t % (2 * Math.PI);
      if (phase < 0.5) y = canvas.height/2;
      else if (phase < 0.7) y = canvas.height/2 - 12;
      else if (phase < 0.8) y = canvas.height/2 + 6;
      else if (phase < 1.0) y = canvas.height/2 - 18;
      else if (phase < 1.1) y = canvas.height/2 + 3;
      else y = canvas.height/2 + Math.sin(phase*0.5)*3;

      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();
    offset += 2;
    requestAnimationFrame(drawWave);
  }
  drawWave();
}

// ── MOOD CHART ─────────────────────────────────────────────────────────────
function initMoodChart() {
  appState.moodChartData = [
    { score: 5 }, { score: 4 }, { score: 6 }, { score: 5 }, { score: 7 }
  ];
  drawMoodChart();
}

function drawMoodChart() {
  const canvas = $('moodChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const data = appState.moodChartData.slice(-12);
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  if (data.length < 2) return;

  const scores = data.map(d => d.score !== undefined ? d.score : getEmotionScore(d.emotion));
  const min = Math.min(...scores) - 0.5;
  const max = Math.max(...scores) + 0.5;
  const range = max - min || 1;

  const toX = i => (i / (data.length-1)) * W;
  const toY = s => H - ((s - min) / range) * (H-10) - 5;

  // Grid lines
  ctx.strokeStyle = 'rgba(255,255,255,0.05)';
  ctx.lineWidth = 1;
  [0.25, 0.5, 0.75].forEach(r => {
    ctx.beginPath(); ctx.moveTo(0, H*r); ctx.lineTo(W, H*r); ctx.stroke();
  });

  // Gradient fill
  const grad = ctx.createLinearGradient(0,0,0,H);
  grad.addColorStop(0, 'rgba(139,92,246,0.4)');
  grad.addColorStop(1, 'rgba(139,92,246,0)');
  ctx.beginPath();
  scores.forEach((s,i) => i===0 ? ctx.moveTo(toX(i), toY(s)) : ctx.lineTo(toX(i), toY(s)));
  ctx.lineTo(toX(scores.length-1), H);
  ctx.lineTo(0, H);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  // Line
  ctx.beginPath();
  ctx.strokeStyle = '#8b5cf6';
  ctx.lineWidth = 2;
  ctx.lineJoin = 'round';
  scores.forEach((s,i) => i===0 ? ctx.moveTo(toX(i), toY(s)) : ctx.lineTo(toX(i), toY(s)));
  ctx.stroke();

  // Dots
  scores.forEach((s,i) => {
    ctx.beginPath();
    ctx.arc(toX(i), toY(s), 3, 0, Math.PI*2);
    ctx.fillStyle = '#a78bfa';
    ctx.fill();
  });
}

function getEmotionScore(emotion) {
  const scoreMap = { happiness: 8, gratitude: 8, neutral: 5, calm: 6, loneliness: 3, sadness: 2, anxiety: 3, stress: 3, anger: 2, crisis: 1, severe_distress: 1 };
  return scoreMap[emotion] || 5;
}

// ── BREATHING EXERCISE ─────────────────────────────────────────────────────
let breathingTimer = null;
let breathPhase = 0;

function startBreathingExercise() {
  const circle = $('breatheCircle');
  const text = $('breatheText');
  const phases = [
    { label: 'Breathe In', duration: 4000, class: 'expand' },
    { label: 'Hold', duration: 4000, class: '' },
    { label: 'Breathe Out', duration: 4000, class: 'shrink' },
    { label: 'Hold', duration: 4000, class: '' }
  ];

  $('startBreathe').textContent = '⏹ Stop';
  $('startBreathe').onclick = stopBreathing;

  function runPhase() {
    const phase = phases[breathPhase % phases.length];
    text.textContent = phase.label;
    circle.className = 'breathe-circle ' + (phase.class || '');
    breathingTimer = setTimeout(() => {
      breathPhase++;
      runPhase();
    }, phase.duration);
  }
  runPhase();
}

function stopBreathing() {
  if (breathingTimer) clearTimeout(breathingTimer);
  const circle = $('breatheCircle');
  circle.className = 'breathe-circle';
  $('breatheText').textContent = 'Breathe In';
  $('startBreathe').textContent = '▶ Start Exercise';
  $('startBreathe').onclick = startBreathingExercise;
}

// ── MODE UI ────────────────────────────────────────────────────────────────
function syncModeUI() {
  document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === appState.mode);
  });
}

// ── AMBIENT PARTICLES ──────────────────────────────────────────────────────
function populateAmbientParticles() {
  const container = $('ambientBg');
  for (let i = 0; i < 30; i++) {
    const particle = document.createElement('div');
    const size = Math.random() * 4 + 1;
    particle.style.cssText = `
      position:absolute;
      width:${size}px; height:${size}px;
      border-radius:50%;
      background:rgba(${Math.random()>0.5?'139,92,246':'6,182,212'},${Math.random()*0.3+0.05});
      left:${Math.random()*100}%;
      top:${Math.random()*100}%;
      animation: float${Math.ceil(Math.random()*3)} ${8+Math.random()*12}s ease-in-out ${Math.random()*8}s infinite;
      pointer-events:none;
    `;
    container.appendChild(particle);
  }

  // CSS for particles
  const style = document.createElement('style');
  style.textContent = `
    @keyframes float1 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(30px,-30px)} }
    @keyframes float2 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-20px,40px)} }
    @keyframes float3 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(40px,20px)} }
  `;
  document.head.appendChild(style);
}

// ── TOAST ──────────────────────────────────────────────────────────────────
function addSystemToast(message) {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position:fixed; bottom:100px; left:50%; transform:translateX(-50%);
    background:rgba(30,20,60,0.95); border:1px solid rgba(139,92,246,0.3);
    color:#e2e8f0; padding:10px 20px; border-radius:99px; font-size:13px;
    z-index:999; backdrop-filter:blur(12px); transition:opacity 0.3s;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ── STATE PERSISTENCE ──────────────────────────────────────────────────────
function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    if (saved) {
      Object.assign(appState, saved);
      appState.sessionCount = (saved.sessionCount || 0) + 1;
    }
  } catch(e) {}
}

function persistState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
  } catch(e) {}
}

// ── UTILS ──────────────────────────────────────────────────────────────────
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function capitalize(str) { return str ? str.charAt(0).toUpperCase() + str.slice(1) : ''; }
function formatTime(ts) {
  const d = ts ? new Date(ts) : new Date();
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
}
function getEmotionEmoji(emotion) {
  const map = { happiness:'😊', sadness:'💙', anxiety:'😰', stress:'😤', anger:'😠', loneliness:'🫂', neutral:'😌', gratitude:'🙏', crisis:'🆘', severe_distress:'💔' };
  return map[emotion] || '🤖';
}

function sanitizeAIResponse(text) {
  if (typeof text === 'string' && text.trim()) return text;
  return "I'm here with you. I didn't catch that fully - could you share it one more time?";
}

// ── START ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', init);
