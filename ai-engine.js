/**
 * ai-engine.js
 * Bridges the frontend to the Python backend
 */

window.AIEngine = {
  init: function(messages) {
    console.log("AIEngine initialized with message history size:", messages.length);
  },

  getStatus: function() {
    return { color: '#06b6d4', label: 'Python NLP backend' };
  },

  isUsingGPT: function() {
    return true; 
  },

  process: async function(text, profile, mode, emotion, companion) {
     // Retrieve or create session ID
     const s = JSON.parse(localStorage.getItem('emora_session') || '{}');
     const sessionId = s.sessionId || 'sess_' + Math.random().toString(36).substr(2,9);
     s.sessionId = sessionId;
     localStorage.setItem('emora_session', JSON.stringify(s));
 
     try {
       const response = await fetch('http://127.0.0.1:8000/api/chat', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ message: text, session_id: sessionId })
       });
       
       if (!response.ok) {
           throw new Error("HTTP connection error: " + response.status);
       }
       
       const data = await response.json();
       
       // Format matching app.js expectations
       return {
         text: data.response,
         emotion: {
            dominant: data.emotion,
            isCrisis: data.is_crisis,
            source: 'bert-ensemble' // So app.js uses this accurate result
         },
         bert: {
            sentiment: data.sentiment
         }
       };
     } catch (err) {
       console.error("AI Engine API Error:", err);
       throw err; 
       // Falls back natively in app.js
     }
   }
};
