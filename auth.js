/**
 * EMORA AI — Auth Controller (auth.js)
 * Supports: Firebase (when configured) + Local Demo Mode (always works)
 * Features: Email/Password, Google OAuth, GitHub OAuth, Password Reset,
 *           Password Strength Meter, Tab Slider, Enter Key, Toast Notices
 */

// ── GLOBALS ────────────────────────────────────────────────────
const AUTH           = window._firebaseAuth   || null;
const GOOGLE_PROV    = window._googleProvider || null;
const GITHUB_PROV    = window._githubProvider || null;
const APP_PAGE       = 'index.html';
const USERS_KEY      = 'emora_users';
const SESSION_KEY    = 'emora_session';
const HAS_USER_KEY   = 'emora_has_user';
const DEMO_MODE      = !AUTH;

// ── ON LOAD ────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  // Small delay for cinematic loader feel
  setTimeout(() => {
    if (DEMO_MODE) {
      hideDemoBanner(false); // show banner
      revealShell();
      const hasUser = localStorage.getItem(HAS_USER_KEY);
      hasUser ? showLogin() : showSignup();
    } else {
      // Real Firebase — check persisted session
      AUTH.onAuthStateChanged(user => {
        if (user) {
          redirectToApp();
        } else {
          revealShell();
          const hasUser = localStorage.getItem(HAS_USER_KEY);
          hasUser ? showLogin() : showSignup();
        }
      });
    }

    initTabSlider();
    bindPasswordStrength();
    bindEnterKey();
  }, 1200);
});

function revealShell() {
  const loader = document.getElementById('initLoader');
  const shell  = document.getElementById('authShell');
  loader.classList.add('hidden');
  setTimeout(() => shell.classList.remove('hidden'), 100);
}

function hideDemoBanner(hide = true) {
  const el = document.getElementById('demoBanner');
  if (!el) return;
  if (hide) {
    el.classList.add('hidden');
  } else {
    el.classList.remove('hidden');
  }
}

// ── SIGN UP ────────────────────────────────────────────────────
async function handleSignup() {
  const name   = val('su-name');
  const email  = val('su-email');
  const pass   = val('su-pass');
  const conf   = val('su-conf');
  const agreed = document.getElementById('su-agree').checked;
  const errEl  = document.getElementById('su-error');

  clearMsg(errEl);

  if (name.length < 2)        return showErr(errEl, '👤 Please enter your full name (min 2 chars).');
  if (!validEmail(email))     return showErr(errEl, '📧 Please enter a valid email address.');
  if (pass.length < 6)        return showErr(errEl, '🔒 Password must be at least 6 characters.');
  if (pass !== conf)          return showErr(errEl, '🔒 Passwords do not match — please re-enter.');
  if (!agreed)                return showErr(errEl, '☑️ Please agree to the Privacy Policy & Terms.');

  setBtnLoading('signupBtn', 'su-spin', true);

  if (DEMO_MODE) {
    await sleep(900);
    const users = getUsers();
    if (users[email]) {
      setBtnLoading('signupBtn', 'su-spin', false);
      return showErr(errEl, '📧 This email is already registered. Please sign in.');
    }
    users[email] = { name, email, pass: btoa(pass), created: Date.now() };
    saveUsers(users);
    localStorage.setItem(HAS_USER_KEY, '1');
    saveSession({ name, email });
    showSuccess(`Welcome, ${firstName(name)}! 🎉`, 'Your account is ready. Taking you to Emora...');
  } else {
    try {
      const cred = await AUTH.createUserWithEmailAndPassword(email, pass);
      await cred.user.updateProfile({ displayName: name });
      await cred.user.sendEmailVerification().catch(() => {});
      localStorage.setItem(HAS_USER_KEY, '1');
      showSuccess(`Welcome, ${firstName(name)}! 🎉`, 'Your account is ready. Taking you to Emora...');
    } catch (err) {
      setBtnLoading('signupBtn', 'su-spin', false);
      showErr(errEl, firebaseMsg(err.code));
    }
  }
}

// ── LOGIN ──────────────────────────────────────────────────────
async function handleLogin() {
  const email  = val('li-email');
  const pass   = val('li-pass');
  const errEl  = document.getElementById('li-error');
  const sucEl  = document.getElementById('li-success');

  clearMsg(errEl); clearMsg(sucEl);

  if (!validEmail(email)) return showErr(errEl, '📧 Please enter a valid email address.');
  if (!pass)              return showErr(errEl, '🔒 Please enter your password.');

  setBtnLoading('loginBtn', 'li-spin', true);

  if (DEMO_MODE) {
    await sleep(800);
    const users = getUsers();
    const user  = users[email];

    if (!user) {
      setBtnLoading('loginBtn', 'li-spin', false);
      return showErr(errEl, '❌ No account found with this email. Please sign up first.');
    }
    if (atob(user.pass) !== pass) {
      setBtnLoading('loginBtn', 'li-spin', false);
      return showErr(errEl, '🔒 Incorrect password. Please try again.');
    }

    localStorage.setItem(HAS_USER_KEY, '1');
    saveSession(user);
    showSuccess(`Welcome back, ${firstName(user.name)}! 💙`, 'Signing you in...');
  } else {
    try {
      await AUTH.signInWithEmailAndPassword(email, pass);
      localStorage.setItem(HAS_USER_KEY, '1');
      showSuccess('Welcome back! 💙', 'Signing you in...');
    } catch (err) {
      setBtnLoading('loginBtn', 'li-spin', false);
      showErr(errEl, firebaseMsg(err.code));
    }
  }
}

// ── GOOGLE ─────────────────────────────────────────────────────
async function signInWithGoogle() {
  if (DEMO_MODE) {
    // Simulate Google auth in demo mode
    await sleep(600);
    const mockName  = 'Demo User';
    const mockEmail = 'demo@gmail.com';
    const users = getUsers();
    if (!users[mockEmail]) {
      users[mockEmail] = { name: mockName, email: mockEmail, pass: '', created: Date.now() };
      saveUsers(users);
    }
    localStorage.setItem(HAS_USER_KEY, '1');
    saveSession({ name: mockName, email: mockEmail });
    showSuccess('Welcome, Demo! 🎉', 'Signed in with Google (demo)...');
    return;
  }

  if (!GOOGLE_PROV) { showSetupModal(); return; }
  setSocialLoading(true);

  try {
    const result = await AUTH.signInWithPopup(GOOGLE_PROV);
    localStorage.setItem(HAS_USER_KEY, '1');
    const name = result.user.displayName || 'Friend';
    showSuccess(`Welcome, ${firstName(name)}! 🎉`, 'Signed in with Google...');
  } catch (err) {
    setSocialLoading(false);
    if (['auth/popup-closed-by-user','auth/cancelled-popup-request'].includes(err.code)) return;
    showToast('❌ ' + firebaseMsg(err.code));
  }
}

// ── GITHUB ─────────────────────────────────────────────────────
async function signInWithGitHub() {
  if (DEMO_MODE) {
    await sleep(600);
    const mockName  = 'Dev User';
    const mockEmail = 'dev@github.com';
    const users = getUsers();
    if (!users[mockEmail]) {
      users[mockEmail] = { name: mockName, email: mockEmail, pass: '', created: Date.now() };
      saveUsers(users);
    }
    localStorage.setItem(HAS_USER_KEY, '1');
    saveSession({ name: mockName, email: mockEmail });
    showSuccess('Welcome, Dev! 🎉', 'Signed in with GitHub (demo)...');
    return;
  }

  if (!GITHUB_PROV) { showSetupModal(); return; }
  setSocialLoading(true);

  try {
    const result = await AUTH.signInWithPopup(GITHUB_PROV);
    localStorage.setItem(HAS_USER_KEY, '1');
    const name = result.user.displayName || result.user.email || 'Developer';
    showSuccess(`Welcome, ${firstName(name)}! 🎉`, 'Signed in with GitHub...');
  } catch (err) {
    setSocialLoading(false);
    if (['auth/popup-closed-by-user','auth/cancelled-popup-request'].includes(err.code)) return;
    if (err.code === 'auth/account-exists-with-different-credential') {
      showToast('⚠️ Email linked to another provider. Try Google sign-in instead.');
      return;
    }
    showToast('❌ ' + firebaseMsg(err.code));
  }
}

// ── FORGOT PASSWORD ────────────────────────────────────────────
async function handleForgotPassword() {
  const email = val('li-email');
  const errEl = document.getElementById('li-error');
  const sucEl = document.getElementById('li-success');
  clearMsg(errEl); clearMsg(sucEl);

  if (!validEmail(email)) {
    return showErr(errEl, '📧 Enter your email above first, then click Forgot Password.');
  }

  if (DEMO_MODE) {
    // Always appear to succeed for security
    sucEl.textContent = '✅ If that email is registered, a reset link has been sent. (Demo: password reset simulated)';
    showMsg(sucEl);
    return;
  }

  try {
    await AUTH.sendPasswordResetEmail(email);
  } catch (e) { /* silence — never reveal existence */ }
  sucEl.textContent = '✅ If that email is registered, a reset link has been sent. Check your inbox.';
  showMsg(sucEl);
}

// ── SUCCESS → REDIRECT ─────────────────────────────────────────
function showSuccess(title, msg) {
  ['signupForm','loginForm'].forEach(id => hide(id));
  show('successPane');
  document.getElementById('successTitle').textContent = title;
  document.getElementById('successMsg').textContent   = msg;
  setTimeout(() => document.getElementById('progressFill').style.width = '100%', 100);
  setTimeout(redirectToApp, 2700);
}

function redirectToApp() {
  window.location.href = APP_PAGE;
}

// ── TAB CONTROL ────────────────────────────────────────────────
function showSignup() {
  show('signupForm'); hide('loginForm'); hide('successPane');
  setTabActive('tabSignup', 'tabSignin');
  moveTabPill('right');
  clearAllMsgs();
}

function showLogin() {
  show('loginForm'); hide('signupForm'); hide('successPane');
  setTabActive('tabSignin', 'tabSignup');
  moveTabPill('left');
  clearAllMsgs();
}

function setTabActive(activeId, inactiveId) {
  document.getElementById(activeId).classList.add('active');
  document.getElementById(inactiveId).classList.remove('active');
}

function initTabSlider() {
  const hasUser = localStorage.getItem(HAS_USER_KEY);
  moveTabPill(hasUser ? 'left' : 'right');
}

function moveTabPill(side) {
  const pill = document.getElementById('tabPill');
  const tabs = document.getElementById('tabs');
  if (!pill || !tabs) return;
  const w = (tabs.offsetWidth / 2) - 4;
  pill.style.width  = w + 'px';
  pill.style.height = (tabs.offsetHeight - 8) + 'px';
  pill.style.top    = '4px';
  pill.style.left   = side === 'left' ? '4px' : (w + 4) + 'px';
}

// ── PASSWORD STRENGTH ──────────────────────────────────────────
function bindPasswordStrength() {
  const input = document.getElementById('su-pass');
  if (!input) return;
  input.addEventListener('input', () => checkStrength(input.value));
}

function checkStrength(pass) {
  const bars   = [1,2,3,4].map(n => document.getElementById('psb' + n));
  const label  = document.getElementById('psLabel');
  if (!bars[0] || !label) return;

  let score = 0;
  if (pass.length >= 6)               score++;
  if (pass.length >= 10)              score++;
  if (/[A-Z]/.test(pass) && /[a-z]/.test(pass)) score++;
  if (/[^A-Za-z0-9]/.test(pass))     score++;

  const colors = ['#ef4444','#f59e0b','#3b82f6','#10b981'];
  const labels = ['Weak','Fair','Good','Strong'];

  bars.forEach((bar, i) => {
    bar.style.background = i < score ? colors[score - 1] : 'rgba(255,255,255,0.07)';
  });

  label.textContent = pass ? labels[score - 1] || '' : '';
  label.style.color = pass ? colors[score - 1] : '';
}

// ── SETUP MODAL ────────────────────────────────────────────────
function showSetupModal() { document.getElementById('setupModal').classList.remove('hidden'); }
function hideSetupModal()  { document.getElementById('setupModal').classList.add('hidden'); }

// ── TOGGLE PASSWORD VISIBILITY ─────────────────────────────────
function toggleVis(inputId, btn) {
  const input = document.getElementById(inputId);
  const isPass = input.type === 'password';
  input.type = isPass ? 'text' : 'password';

  // Swap icon
  const openEye  = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>`;
  const closedEye = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>`;
  const svg = btn.querySelector('svg');
  if (svg) svg.innerHTML = isPass ? closedEye : openEye;
}

// ── ENTER KEY ──────────────────────────────────────────────────
function bindEnterKey() {
  document.addEventListener('keydown', e => {
    if (e.key !== 'Enter' || e.shiftKey) return;
    const tag = document.activeElement?.tagName;
    if (tag === 'TEXTAREA') return;
    if (!document.getElementById('signupForm').classList.contains('hidden')) handleSignup();
    else if (!document.getElementById('loginForm').classList.contains('hidden')) handleLogin();
  });
}

// ── TOAST ──────────────────────────────────────────────────────
function showToast(msg) {
  // Remove existing toasts
  document.querySelectorAll('.emora-toast').forEach(t => t.remove());
  const t = document.createElement('div');
  t.className = 'emora-toast';
  t.style.cssText = `
    position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(20px);
    background:rgba(10,14,30,0.97);border:1px solid rgba(139,92,246,0.3);
    color:#e2e8f0;padding:12px 24px;border-radius:9999px;
    font-size:13px;z-index:9999;backdrop-filter:blur(16px);
    box-shadow:0 8px 30px rgba(0,0,0,0.5);
    font-family:'Inter',sans-serif;white-space:nowrap;max-width:90vw;
    opacity:0;transition:all 0.35s cubic-bezier(0.34,1.56,0.64,1);
  `;
  t.textContent = msg;
  document.body.appendChild(t);
  requestAnimationFrame(() => {
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(-50%) translateY(10px)';
    setTimeout(() => t.remove(), 400);
  }, 4000);
}

// ── HELPERS ────────────────────────────────────────────────────
const val  = id => (document.getElementById(id)?.value || '').trim();
const show = id => document.getElementById(id)?.classList.remove('hidden');
const hide = id => document.getElementById(id)?.classList.add('hidden');

function showErr(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.classList.remove('hidden');
  el.style.animation = 'none';
  requestAnimationFrame(() => el.style.animation = 'shake 0.4s ease');
}
function showMsg(el) {
  if (!el) return;
  el.classList.remove('hidden');
  el.style.animation = 'none';
  requestAnimationFrame(() => el.style.animation = 'paneIn 0.3s ease');
}
function clearMsg(el) { if (el) { el.classList.add('hidden'); el.textContent = ''; } }
function clearAllMsgs() {
  ['su-error','li-error','li-success'].forEach(id => clearMsg(document.getElementById(id)));
}

function setBtnLoading(btnId, spinnerId, on) {
  const btn    = document.getElementById(btnId);
  const spin   = document.getElementById(spinnerId);
  const label  = btn?.querySelector('.btn-label');
  const arrow  = btn?.querySelector('.btn-arrow');
  if (btn)   btn.disabled = on;
  if (spin)  spin.classList.toggle('hidden', !on);
  if (label) label.style.opacity = on ? '0.6' : '1';
  if (arrow) arrow.style.opacity = on ? '0'   : '1';
}

function setSocialLoading(on) {
  ['su-google','su-github','li-google','li-github'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.disabled = on;
  });
}

function validEmail(e) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
}
function firstName(name) {
  return (name || '').split(' ')[0] || name;
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── LOCAL USER STORE (Demo Mode) ───────────────────────────────
function getUsers() {
  try { return JSON.parse(localStorage.getItem(USERS_KEY) || '{}'); }
  catch { return {}; }
}
function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}
function saveSession(user) {
  localStorage.setItem(SESSION_KEY, JSON.stringify({ ...user, loginAt: Date.now() }));
}

// ── FIREBASE ERROR MESSAGES ────────────────────────────────────
function firebaseMsg(code) {
  const map = {
    'auth/email-already-in-use':        '📧 This email is already registered. Please sign in instead.',
    'auth/invalid-email':               '📧 The email address is not valid.',
    'auth/user-not-found':              '❌ No account found with this email. Please sign up.',
    'auth/wrong-password':              '🔒 Incorrect password. Please try again or reset it.',
    'auth/invalid-credential':          '❌ Incorrect email or password. Please try again.',
    'auth/too-many-requests':           '⏳ Too many attempts. Please wait a few minutes.',
    'auth/network-request-failed':      '🌐 Network error. Check your internet connection.',
    'auth/weak-password':               '🔒 Password is too weak. Use at least 6 characters.',
    'auth/popup-blocked':               '🚫 Popup blocked. Allow popups for this site.',
    'auth/operation-not-allowed':       '⚠️ This sign-in method is not enabled in Firebase.',
    'auth/configuration-not-found':     '⚙️ Firebase not configured. Please fill in firebase-config.js.',
    'auth/internal-error':              '⚙️ Firebase not configured. Please fill in firebase-config.js.',
    'auth/app-not-authorized':          '⚙️ App not authorized. Verify your Firebase project settings.',
  };
  return map[code] || `Authentication error (${code}). Please try again.`;
}
