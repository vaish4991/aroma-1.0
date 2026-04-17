/**
 * EMORA AI — Firebase Configuration
 * Project: eroma-ai
 * ─────────────────────────────────────────────────────────────────
 * Authentication enabled:
 *   ✅ Email / Password
 *   ✅ Google  (enable in Firebase Console → Auth → Sign-in method)
 *   ✅ GitHub  (enable in Firebase Console → Auth → Sign-in method)
 *
 * Authorized domains (Firebase Console → Auth → Settings):
 *   Add: localhost  and  127.0.0.1  for local testing
 * ─────────────────────────────────────────────────────────────────
 */

const firebaseConfig = {
  apiKey:            "AIzaSyD7P0tKADFzRofOQwPQmAFlT2OZlP1IiAQ",
  authDomain:        "eroma-ai.firebaseapp.com",
  projectId:         "eroma-ai",
  storageBucket:     "eroma-ai.firebasestorage.app",
  messagingSenderId: "884796853441",
  appId:             "1:884796853441:web:e60a763c48e32e0de01840"
};

// ─────────────────────────────────────────────────────────────────
// AUTO-DETECT: checks if config looks valid before initializing.
// If placeholder values remain, app falls back to Demo Mode.
// ─────────────────────────────────────────────────────────────────
const _isConfigured = (
  firebaseConfig.apiKey &&
  !firebaseConfig.apiKey.includes('PASTE_YOUR')
);

if (_isConfigured) {
  try {
    firebase.initializeApp(firebaseConfig);
    window._firebaseAuth = firebase.auth();

    // Persist auth session across page reloads
    window._firebaseAuth.setPersistence(firebase.auth.Auth.Persistence.LOCAL)
      .catch(() => {});

    // Google Provider
    window._googleProvider = new firebase.auth.GoogleAuthProvider();
    window._googleProvider.addScope('profile');
    window._googleProvider.addScope('email');
    window._googleProvider.setCustomParameters({ prompt: 'select_account' });

    // GitHub Provider
    window._githubProvider = new firebase.auth.GithubAuthProvider();
    window._githubProvider.addScope('user:email');

    console.log('✅ Emora AI: Firebase initialized — project:', firebaseConfig.projectId);
  } catch (err) {
    console.warn('⚠️ Emora AI: Firebase init failed — running in Demo Mode.', err.message);
    window._firebaseAuth   = null;
    window._googleProvider = null;
    window._githubProvider = null;
  }
} else {
  console.info('ℹ️ Emora AI: Firebase not configured — running in Demo Mode (localStorage auth).');
  window._firebaseAuth   = null;
  window._googleProvider = null;
  window._githubProvider = null;
}
