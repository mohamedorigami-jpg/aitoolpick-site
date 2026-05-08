// Brevo newsletter subscription — aitoolpick.co.uk
// Posts email to Brevo Contacts API v3. CORS-restricted to this domain.
(function() {
  const API_KEY = 'xkeysib-4b623597374259c515d63d6cead21e75b4d7cc05027f7d8dde8f7c4f184c9f19-zBQq';
  const LIST_ID = 5; // "AIToolpick Newsletter"
  const API_URL = 'https://api.brevo.com/v3/contacts';

  window.brevoSubscribe = function(email, formEl) {
    const btn = formEl ? formEl.querySelector('button[type="submit"]') : null;
    if (btn) { btn.disabled = true; btn.textContent = 'Signing up...'; }

    fetch(API_URL, {
      method: 'POST',
      headers: {
        'api-key': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        listIds: [LIST_ID],
        updateEnabled: true,
        attributes: { SUBSCRIBED_AT: new Date().toISOString() }
      })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (formEl) {
        formEl.style.display = 'none';
        var note = formEl.parentElement.querySelector('.newsletter-note');
        if (note) {
          note.textContent = "You're signed up! We'll email new posts and useful picks straight to your inbox.";
          note.style.color = 'var(--accent, #d4500a)';
          note.style.fontSize = '16px';
          note.style.fontWeight = '600';
        }
      }
    })
    .catch(function(err) {
      console.error('Brevo subscribe error:', err);
      if (btn) { btn.disabled = false; btn.textContent = 'Subscribe'; }
      if (formEl) {
        var note = formEl.parentElement.querySelector('.newsletter-note');
        if (note) {
          note.textContent = 'Something went wrong. Try again or email us directly.';
          note.style.color = '#e53e3e';
        }
      }
    });
  };
})();
