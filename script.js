(function() {
  const todoList = document.getElementById('todo-list');
  const taskInput = document.getElementById('task-input');
  const addTaskBtn = document.getElementById('add-task');

  const chatLog = document.getElementById('chat-log');
  const chatInput = document.getElementById('chat-message');
  const chatBtn = document.getElementById('send-chat');
  const themeToggle = document.getElementById('toggle-theme');

  // respect saved theme
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
  }

  // basic add task functionality
  addTaskBtn.addEventListener('click', () => {
    const text = taskInput.value.trim();
    if (!text) return;
    const li = document.createElement('li');
    li.textContent = text;
    todoList.appendChild(li);
    taskInput.value = '';
  });

  // toggle dark mode
  themeToggle.addEventListener('click', () => {
    const dark = document.body.classList.toggle('dark');
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  });

  // stubbed chat interaction
  chatBtn.addEventListener('click', () => {
    const msg = chatInput.value.trim();
    if (!msg) return;
    appendMessage('user', msg);
    chatInput.value = '';
    // For preview purposes we'll echo the message.
    setTimeout(() => appendMessage('ai', `You said: ${msg}`), 500);
  });

  function appendMessage(author, text) {
    const div = document.createElement('div');
    div.className = 'chat-message';
    div.textContent = text;
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
  }
})();
