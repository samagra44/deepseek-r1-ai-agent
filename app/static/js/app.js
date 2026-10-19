const $ = (s, p) => (p || document).querySelector(s);

const messages = $('#messages');
const statusEl = $('#status');
const sendBtn = $('#send-button');
const chatForm = $('#chat-form');
const messageInput = $('#message');
const loadingEl = $('#loading-indicator');
const chatSubtitle = $('#chat-subtitle');
const docList = $('#doc-list');

function getSessionId() {
  let sid = localStorage.getItem('session_id');
  if (!sid) {
    sid = crypto.randomUUID ? crypto.randomUUID() : 's-' + Date.now() + '-' + Math.random().toString(36).slice(2, 10);
    localStorage.setItem('session_id', sid);
  }
  return sid;
}
const SESSION_ID = getSessionId();

marked.setOptions({ breaks: true, gfm: true });

function setStatus(text, isError) {
  statusEl.textContent = text;
  statusEl.className = 'status' + (isError ? ' error' : '');
}

function setLoading(on) {
  loadingEl.classList.toggle('hidden', !on);
  sendBtn.disabled = on;
}

function scrollToBottom() {
  messages.scrollTop = messages.scrollHeight;
}

function removeWelcome() {
  const wel = messages.querySelector('.welcome');
  if (wel) wel.remove();
}

function renderMarkdown(text) {
  const raw = marked.parse(text);
  return DOMPurify.sanitize(raw, { ADD_ATTR: ['target'] });
}

function addCopyButtons() {
  messages.querySelectorAll('pre code').forEach((block) => {
    const pre = block.parentElement;
    if (pre.querySelector('.copy-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.onclick = async () => {
      try {
        await navigator.clipboard.writeText(block.textContent);
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      } catch {
        btn.textContent = 'Failed';
      }
    };
    pre.appendChild(btn);
  });
}

function addMessage(text, role, isHtml) {
  removeWelcome();
  const article = document.createElement('article');
  article.className = 'message ' + role;
  article.innerHTML = `
    <div class="message-avatar">${role === 'assistant' ? 'AI' : 'YO'}</div>
    <div class="message-bubble${isHtml ? ' prose' : ''}"></div>
  `;
  const bubble = article.querySelector('.message-bubble');
  if (isHtml) {
    bubble.innerHTML = text;
  } else {
    bubble.textContent = text;
  }
  messages.append(article);
  scrollToBottom();
  if (isHtml) addCopyButtons();
  if (role === 'user') chatSubtitle.textContent = 'Waiting for response...';
  return article;
}

function addThinkingMessage() {
  removeWelcome();
  const article = document.createElement('article');
  article.className = 'message assistant thinking-message';
  article.innerHTML = `
    <div class="message-avatar">AI</div>
    <div class="message-bubble thinking-bubble">
      <span class="thinking-text">Thinking</span>
      <span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>
    </div>
  `;
  messages.append(article);
  scrollToBottom();
  return article;
}

async function api(url, options) {
  const res = await fetch(url, options);
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Request failed.');
  return data;
}

/* ── Document list ── */

async function refreshDocList() {
  try {
    const data = await api('/api/documents?session_id=' + encodeURIComponent(SESSION_ID));
    renderDocList(data.documents || []);
  } catch {
    docList.innerHTML = '<p class="doc-list-empty">Failed to load documents.</p>';
  }
}

function renderDocList(docs) {
  if (!docs.length) {
    docList.innerHTML = '<p class="doc-list-empty">No documents yet.</p>';
    return;
  }
  docList.innerHTML = docs.map((d) => {
    const icon = d.source_type === 'pdf' ? '📄' : '🔗';
    const label = d.source_type === 'pdf' ? 'PDF' : 'URL';
    const ts = d.timestamp ? new Date(d.timestamp).toLocaleDateString() : '';
    return `
      <div class="doc-item" data-id="${d.id}">
        <span class="doc-icon">${icon}</span>
        <div class="doc-info">
          <div class="doc-name" title="${escapeHtml(d.source_name)}">${escapeHtml(d.source_name)}</div>
          <div class="doc-meta">${label} · ${d.chunk_count} chunk${d.chunk_count > 1 ? 's' : ''}${ts ? ' · ' + ts : ''}</div>
        </div>
        <button class="doc-delete" data-id="${d.id}" title="Remove document">&times;</button>
      </div>
    `;
  }).join('');
  docList.querySelectorAll('.doc-delete').forEach((btn) => {
    btn.onclick = async () => {
      if (!confirm('Remove this document from your knowledge base?')) return;
      try {
        await api('/api/documents/' + encodeURIComponent(btn.dataset.id), { method: 'DELETE' });
        setStatus('Document removed.');
        await refreshDocList();
      } catch (err) {
        setStatus(err.message, true);
      }
    };
  });
}

function escapeHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

/* ── Chat ── */

chatForm.onsubmit = async (e) => {
  e.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  messageInput.value = '';
  messageInput.style.height = 'auto';
  setLoading(true);
  setStatus('Generating answer...');
  const thinkingEl = addThinkingMessage();
  try {
    const data = await api('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        session_id: SESSION_ID,
        rag_enabled: $('#rag-toggle').checked,
        web_search_enabled: $('#web-toggle').checked,
      })
    });
    const html = renderMarkdown(data.answer);
    thinkingEl.replaceWith(addMessage(html, 'assistant', true));
    chatSubtitle.textContent = data.sources_used ? `${data.sources_used} document chunks used` : 'Ready';
    setStatus(data.sources_used ? `${data.sources_used} document chunks used` : 'Ready');
  } catch (err) {
    thinkingEl.remove();
    addMessage('Sorry, ' + err.message, 'assistant');
    setStatus(err.message, true);
    chatSubtitle.textContent = 'Error occurred';
  } finally {
    setLoading(false);
    messageInput.focus();
  }
};

messageInput.addEventListener('input', () => {
  messageInput.style.height = 'auto';
  messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
});

messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    chatForm.dispatchEvent(new Event('submit'));
  }
});

/* ── Document ingestion ── */

$('#pdf-file').onchange = async (e) => {
  const f = e.target.files[0];
  if (!f) return;
  const form = new FormData();
  form.append('file', f);
  form.append('session_id', SESSION_ID);
  setLoading(true);
  setStatus('Uploading PDF...');
  try {
    const d = await api('/api/documents/pdf', { method: 'POST', body: form });
    setStatus(d.chunks_added + ' chunks added from ' + f.name);
    await refreshDocList();
  } catch (err) {
    setStatus(err.message, true);
  } finally {
    setLoading(false);
  }
  e.target.value = '';
};

$('#url-form').onsubmit = async (e) => {
  e.preventDefault();
  const i = $('#source-url');
  const url = i.value.trim();
  if (!url) return;
  setLoading(true);
  setStatus('Importing URL...');
  try {
    const d = await api('/api/documents/url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, session_id: SESSION_ID })
    });
    setStatus(d.chunks_added + ' chunks added');
    i.value = '';
    await refreshDocList();
  } catch (err) {
    setStatus(err.message, true);
  } finally {
    setLoading(false);
  }
};

$('#clear-chat').onclick = () => {
  messages.querySelectorAll('.message').forEach((el) => el.remove());
  messages.innerHTML = `
    <div class="welcome">
      <div class="welcome-icon">🧠</div>
      <h3>Welcome to DeepSeek RAG</h3>
      <p>Upload a PDF or add a URL to build your knowledge base, then ask anything.</p>
    </div>
  `;
  chatSubtitle.textContent = 'Start a conversation';
  setStatus('Ready');
};

$('#clear-docs').onclick = async () => {
  if (!confirm('Remove ALL your uploaded documents? This cannot be undone.')) return;
  setLoading(true);
  setStatus('Removing all documents...');
  try {
    const d = await api('/api/documents?session_id=' + encodeURIComponent(SESSION_ID), { method: 'DELETE' });
    setStatus(d.deleted + ' document group(s) removed.');
    await refreshDocList();
  } catch (err) {
    setStatus(err.message, true);
  } finally {
    setLoading(false);
  }
};

/* ── Sidebar ── */

const sidebar = $('#sidebar');
const toggleBtn = $('#sidebar-toggle');

let overlay = $('.sidebar-overlay');
if (!overlay) {
  overlay = document.createElement('div');
  overlay.className = 'sidebar-overlay';
  document.body.appendChild(overlay);
}

function toggleSidebar(open) {
  const isOpen = open !== undefined ? open : !sidebar.classList.contains('open');
  sidebar.classList.toggle('open', isOpen);
  overlay.classList.toggle('open', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

toggleBtn.addEventListener('click', () => toggleSidebar());
$('#sidebar-close').addEventListener('click', () => toggleSidebar(false));
overlay.addEventListener('click', () => toggleSidebar(false));

window.addEventListener('resize', () => {
  if (window.innerWidth > 820) toggleSidebar(false);
});

/* ── Init ── */
refreshDocList();
