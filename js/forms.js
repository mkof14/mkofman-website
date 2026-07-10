function getFormStrings(lang) {
  return {
    sending: t('ui.sending', lang) || 'Sending…',
    sent: t('ui.messageSent', lang) || 'Message Sent',
    error: t('ui.formError', lang) || 'Could not send. Please email directly.',
    send: t('ui.sendMessage', lang) || 'Send Message',
  };
}

function buildMailtoLink(form) {
  const email = SITE_CONFIG.email;
  const data = new FormData(form);
  const subject = data.get('subject')
    || data.get('topic')
    || data.get('_subject')
    || `Website inquiry from ${data.get('firstName') || ''} ${data.get('lastName') || ''}`.trim()
    || 'Website inquiry';
  const lines = [];
  if (data.get('firstName') || data.get('lastName')) {
    lines.push(`Name: ${[data.get('firstName'), data.get('lastName')].filter(Boolean).join(' ')}`);
  }
  if (data.get('email')) lines.push(`Email: ${data.get('email')}`);
  if (data.get('company')) lines.push(`Company: ${data.get('company')}`);
  if (data.get('topic')) lines.push(`Topic: ${data.get('topic')}`);
  lines.push('');
  lines.push(String(data.get('message') || '').trim());
  const body = lines.join('\n');
  return `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

function ensureFormspreeFields(form) {
  const endpoint = SITE_CONFIG.formspreeEndpoint;
  if (!endpoint) return false;

  form.action = endpoint;
  form.method = 'POST';

  if (!form.querySelector('input[name="_replyto"]')) {
    const reply = document.createElement('input');
    reply.type = 'hidden';
    reply.name = '_replyto';
    form.appendChild(reply);
  }

  if (!form.querySelector('input[name="_subject"]')) {
    const subj = document.createElement('input');
    subj.type = 'hidden';
    subj.name = '_subject';
    subj.value = 'Michael Kofman website inquiry';
    form.appendChild(subj);
  }

  if (!form.querySelector('input[name="_gotcha"]')) {
    const honeypot = document.createElement('input');
    honeypot.type = 'text';
    honeypot.name = '_gotcha';
    honeypot.tabIndex = -1;
    honeypot.autocomplete = 'off';
    honeypot.setAttribute('aria-hidden', 'true');
    honeypot.style.cssText = 'position:absolute;left:-9999px;height:0;width:0;opacity:0;';
    form.appendChild(honeypot);
  }

  const emailField = form.querySelector('[name="email"]');
  const replyField = form.querySelector('[name="_replyto"]');
  if (emailField && replyField) {
    const syncReply = () => { replyField.value = emailField.value || ''; };
    emailField.addEventListener('input', syncReply);
    syncReply();
  }

  return true;
}

async function submitSiteForm(form, button) {
  const lang = localStorage.getItem('lang') || 'en';
  const strings = getFormStrings(lang);
  const endpoint = SITE_CONFIG.formspreeEndpoint;
  const usesFormspree = Boolean(endpoint);

  if (button) {
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = strings.sending;
  }

  try {
    if (usesFormspree) {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) throw new Error('formspree failed');
      return true;
    }

    window.location.href = buildMailtoLink(form);
    return true;
  } catch {
    if (usesFormspree) {
      window.location.href = buildMailtoLink(form);
      return true;
    }
    if (button) {
      button.textContent = strings.error;
      setTimeout(() => {
        button.disabled = false;
        button.textContent = button.dataset.originalText || strings.send;
      }, 3500);
    }
    return false;
  } finally {
    if (button && usesFormspree) {
      button.disabled = false;
      button.textContent = button.dataset.originalText || strings.send;
    }
  }
}

function showFormSuccess(wrapper) {
  if (!wrapper) return;
  wrapper.classList.add('success');
  setTimeout(() => wrapper.classList.remove('success'), 5000);
}

function initSiteForms() {
  document.querySelectorAll('.contact-form form, .footer-form form, .insights-connect-form form').forEach(form => {
    if (form.dataset.bound === 'true') return;
    form.dataset.bound = 'true';

    const usesFormspree = ensureFormspreeFields(form);

    form.addEventListener('submit', async e => {
      e.preventDefault();
      const button = form.querySelector('button[type="submit"]');
      const wrapper = form.closest('.footer-form, .insights-connect-form, .contact-form');
      const ok = await submitSiteForm(form, button);

      if (ok && usesFormspree) {
        if (wrapper) showFormSuccess(wrapper);
        else submitFormFeedback(button, 'ui.sendMessage');
        form.reset();
        const replyField = form.querySelector('[name="_replyto"]');
        if (replyField) replyField.value = '';
      }
    });
  });
}
