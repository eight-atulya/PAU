// Toggle active section
function toggleSection(section) {
  document.querySelectorAll('.content-area > div').forEach(div => {
    div.classList.remove('visible');
  });
  document.getElementById(section).classList.add('visible');

  document.querySelectorAll('.toggle-buttons button').forEach(btn => {
    btn.classList.remove('active');
  });
  document.querySelector(`[data-section="${section}"]`).classList.add('active');
}

window.addEventListener('DOMContentLoaded', () => {
  // ---- Chat Logic ----
  const chatInput = document.querySelector('.input-area input');
  const chatSendBtn = document.querySelector('.input-area button');
  const chatArea = document.getElementById('chat-area');
  const greetingDiv = document.getElementById('chat-greeting');
  const inputAreaDiv = document.getElementById('input-area');
  const recallBtn = document.getElementById('recallConversationBtn');
  const startFreshBtn = document.getElementById('startFreshBtn');

  // -- Step A: On load, show greeting, hide chat area --
  chatArea.style.display = 'none';
  inputAreaDiv.style.display = 'none';

  // -- Step B: If user clicks "Recall Conversation" --
  recallBtn.addEventListener('click', async () => {
    greetingDiv.style.display = 'none';
    chatArea.style.display = 'flex';
    inputAreaDiv.style.display = 'flex';

    try {
      const resp = await fetch('/api/chat/history'); // <--- You need an endpoint that returns chat history
      if (!resp.ok) throw new Error('Failed to fetch history');
      const history = await resp.json();

      // Append each message in the retrieved history
      history.forEach(msg => {
        addMessageToChat(msg.role, msg.content);
      });
    } catch (err) {
      console.error('Error fetching chat history:', err);
    }
  });

  // -- Step C: If user clicks "Start Fresh" --
  startFreshBtn.addEventListener('click', () => {
    greetingDiv.style.display = 'none';
    chatArea.style.display = 'flex';
    inputAreaDiv.style.display = 'flex';
    // No old messages, so we leave chatArea empty
  });

  // -- Step D: Sending new messages to the server (unchanged, just refactor) --
  chatSendBtn.addEventListener('click', sendMessage);
  chatInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });

  async function sendMessage() {
    const userMessage = chatInput.value.trim();
    if(!userMessage) return;

    // Display user message
    addMessageToChat('user', userMessage);
    chatInput.value = '';

    // Send to /api/chat
    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userMessage })
      });
      const data = await resp.json();

      if(data.botReply) {
        addMessageToChat('assistant', data.botReply);
      } else if(data.error) {
        alert('Error: ' + data.error);
      }
    } catch(e) {
      console.error('Chat error:', e);
    }
  }

  // -- Helper to add messages to chat area --
  function addMessageToChat(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${role === 'user' ? 'user-message' : 'bot-message'}`;
  // NEW: parse markdown into HTML with marked
  const renderedMarkdown = marked.parse(content);
  msgDiv.innerHTML = renderedMarkdown;

  chatArea.appendChild(msgDiv);

  // Auto-scroll to bottom
  chatArea.scrollTop = chatArea.scrollHeight;
}

  // ---- Search Logic ----
  const searchSection = document.getElementById('search-section');
  const searchInput = searchSection.querySelector('input');
  const searchResultsDiv = searchSection.querySelector('.search-results');

  // Press Enter to search
  searchInput.addEventListener('keydown', async (e) => {
    if(e.key === 'Enter') {
      await performSearch();
    }
  });

  async function performSearch() {
    const query = searchInput.value.trim();
    if(!query) return;
    searchResultsDiv.innerHTML = 'Searching...';

    try {
      const resp = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const data = await resp.json();
      if(data.results) {
        // Render results
        searchResultsDiv.innerHTML = '';
        data.results.forEach(item => {
          const div = document.createElement('div');
          div.className = 'search-result-item';

          const a = document.createElement('a');
          a.href = item.url;
          a.target = '_blank';
          a.textContent = item.title || 'No Title';

          const p = document.createElement('p');
          p.textContent = item.content || 'No Description';

          div.appendChild(a);
          div.appendChild(p);
          searchResultsDiv.appendChild(div);
        });
      } else if(data.error) {
        searchResultsDiv.textContent = 'Error: ' + data.error;
      }
    } catch(err) {
      console.error('Search error:', err);
      searchResultsDiv.textContent = 'Search failed.';
    }
  }

  // ---- Notes Logic ----
  const noteSection = document.getElementById('note-section');
  const noteEditor = noteSection.querySelector('.note-editor');
  const noteNameInput = document.createElement('input');
  noteNameInput.type = 'text';
  noteNameInput.placeholder = 'Enter note filename (e.g., myNote.md)';
  noteNameInput.style.width = '100%';
  noteNameInput.style.padding = '10px';
  noteNameInput.style.marginBottom = '10px';
  noteNameInput.value = 'myNote.md';
  noteSection.insertBefore(noteNameInput, noteEditor);

  const [saveBtn, newBtn, loadListBtn] = noteSection.querySelectorAll('button');

  // Make sure the 3rd button is "Show All Notes"
  if(!loadListBtn) {
    const loadBtn = document.createElement('button');
    loadBtn.textContent = 'Show All Notes';
    noteSection.appendChild(loadBtn);
  }

  const noteButtons = noteSection.querySelectorAll('button');
  const saveNoteBtn = noteButtons[0];
  const startNewNoteBtn = noteButtons[1];
  let showAllNotesBtn = noteButtons[2];

  // Create a container for listing notes
  const notesListDiv = document.createElement('div');
  notesListDiv.style.marginTop = '10px';
  noteSection.appendChild(notesListDiv);

  showAllNotesBtn.innerText = 'Show All Notes';

  saveNoteBtn.addEventListener('click', async () => {
    const noteName = noteNameInput.value.trim();
    const noteContent = noteEditor.value;
    if(!noteName || !noteContent) {
      alert('Please provide both note name and content.');
      return;
    }
    try {
      const resp = await fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ noteName, noteContent })
      });
      const data = await resp.json();
      if(data.message) {
        alert(data.message);
      } else if(data.error) {
        alert('Error: ' + data.error);
      }
    } catch(err) {
      console.error('Note save error:', err);
      alert('Failed to save note.');
    }
  });

  startNewNoteBtn.addEventListener('click', () => {
    noteNameInput.value = 'myNote.md';
    noteEditor.value = '# Markdown Note\n\nWrite your notes here.';
  });

  showAllNotesBtn.addEventListener('click', async () => {
    // Fetch list of notes
    try {
      const resp = await fetch('/api/notes');
      const data = await resp.json();
      if(data.notes) {
        notesListDiv.innerHTML = '<h4>Available Notes:</h4>';
        data.notes.forEach(noteFile => {
          const item = document.createElement('div');
          item.style.cursor = 'pointer';
          item.style.textDecoration = 'underline';
          item.textContent = noteFile;
          item.onclick = () => loadNote(noteFile);
          notesListDiv.appendChild(item);
        });
      } else if(data.error) {
        notesListDiv.textContent = 'Error: ' + data.error;
      }
    } catch(err) {
      console.error('List notes error:', err);
    }
  });

  async function loadNote(noteFile) {
    // Fetch note content
    try {
      const resp = await fetch(`/api/notes/${encodeURIComponent(noteFile)}`);
      const data = await resp.json();
      if(data.content) {
        noteNameInput.value = noteFile;
        noteEditor.value = data.content;
      } else if(data.error) {
        alert('Error: ' + data.error);
      }
    } catch(err) {
      console.error('Load note error:', err);
    }
  }

  // ---- Progress Logic ----
  const progressSection = document.getElementById('progress-section');
  const progressGraphDiv = progressSection.querySelector('.progress-graph');
  progressGraphDiv.innerHTML = `
    <button id="refreshProgressBtn" style="margin-bottom:10px;">Refresh Progress</button>
    <div id="progressData"></div>
  `;

  const refreshProgressBtn = progressGraphDiv.querySelector('#refreshProgressBtn');
  const progressDataDiv = progressGraphDiv.querySelector('#progressData');

  refreshProgressBtn.addEventListener('click', async () => {
    try {
      const resp = await fetch('/api/progress');
      const data = await resp.json();
      if(!data.error) {
        // data = { chat: x, search: y, notes: z }
        progressDataDiv.innerHTML = `
          <p>Chats used: ${data.chat || 0}</p>
          <p>Searches performed: ${data.search || 0}</p>
          <p>Notes saved: ${data.notes || 0}</p>
        `;
      } else {
        progressDataDiv.textContent = 'Error: ' + data.error;
      }
    } catch(err) {
      console.error('Progress error:', err);
      progressDataDiv.textContent = 'Unable to load progress.';
    }
  });
});

    // When the DOM is fully loaded, fetch the stored user name
    document.addEventListener("DOMContentLoaded", () => {
      fetchUserName();
    });

    async function fetchUserName() {
      try {
        const response = await fetch("/api/get_user");
        const data = await response.json();
        
        // If name is found, display it in #username-display
        if (data.name && data.name.trim() !== "") {
          document.getElementById("username-display").textContent = data.name;
        }
      } catch (error) {
        console.error("Error fetching user name:", error);
      }
    }



// -- Preserving your existing user-name fetch logic --
document.addEventListener("DOMContentLoaded", () => {
  fetchUserName();
});

async function fetchUserName() {
  try {
    const response = await fetch("/api/get_user");
    const data = await response.json();

    if (data.name && data.name.trim() !== "") {
      document.getElementById("username-display").textContent = data.name;
    }
  } catch (error) {
    console.error("Error fetching user name:", error);
  }
}