// 全局变量
let articles = [];
let currentArticle = null;
let editor = null;

// ========== 初始化 ==========
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initEditor();
    loadStats();
    loadArticles();
});

function initNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            showPage(page);
        });
    });
}

function showPage(pageId) {
    // 更新导航
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.dataset.page === pageId);
    });

    // 显示页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.toggle('active', page.id === pageId);
    });

    // 特殊处理
    if (pageId === 'editor' && !currentArticle) {
        resetEditor();
    }
}

// ========== 编辑器 ==========
function initEditor() {
    editor = new EasyMDE({
        element: document.getElementById('article-content'),
        spellChecker: false,
        autosave: { enabled: false },
        placeholder: '在此输入 Markdown 正文...',
        toolbar: [
            'bold', 'italic', 'heading', '|',
            'quote', 'unordered-list', 'ordered-list', '|',
            'link', 'image', 'code', '|',
            'preview', 'side-by-side', 'fullscreen'
        ]
    });
}

function resetEditor() {
    document.getElementById('editor-title').textContent = '新建文章';
    document.getElementById('article-path').value = '';
    document.getElementById('article-title').value = '';
    document.getElementById('article-tags').value = '';
    document.getElementById('article-categories').value = '';
    document.getElementById('article-description').value = '';
    editor.value('');
    currentArticle = null;
}

function loadArticle(path) {
    fetch(`/api/article/${encodeURIComponent(path)}`)
        .then(res => res.json())
        .then(data => {
            currentArticle = data;
            document.getElementById('editor-title').textContent = '编辑文章';
            document.getElementById('article-path').value = data.path;
            document.getElementById('article-title').value = data.title;
            document.getElementById('article-tags').value = data.tags.join(', ');
            document.getElementById('article-categories').value = data.categories.join(', ');
            document.getElementById('article-description').value = data.description;
            editor.value(data.content);
            showPage('editor');
        });
}

function saveDraft() {
    saveArticle(true);
}

function publishArticle() {
    saveArticle(false);
}

function saveArticle(draft = true) {
    const path = document.getElementById('article-path').value;
    const data = {
        title: document.getElementById('article-title').value || '未命名',
        tags: document.getElementById('article-tags').value.split(',').map(t => t.trim()).filter(t => t),
        categories: document.getElementById('article-categories').value.split(',').map(t => t.trim()).filter(t => t) || ['未分类'],
        description: document.getElementById('article-description').value,
        content: editor.value(),
        draft: draft
    };

    const url = path ? `/api/article/${encodeURIComponent(path)}` : '/api/article';
    const method = path ? 'PUT' : 'POST';

    fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            alert(draft ? '草稿已保存' : '文章已发布');
            loadArticles();
            if (!path && result.path) {
                document.getElementById('article-path').value = result.path;
            }
        } else {
            alert('保存失败: ' + (result.error || result.message));
        }
    });
}

// ========== 文章列表 ==========
function loadArticles() {
    fetch('/api/articles')
        .then(res => res.json())
        .then(data => {
            articles = data;
            renderArticles(data);
        });
}

function renderArticles(data) {
    const container = document.getElementById('articles-list');
    container.innerHTML = data.map(article => `
        <div class="article-item">
            <div class="article-info">
                <h4>${article.title}</h4>
                <div class="article-meta">
                    <span>${article.date || '无日期'}</span>
                    <span>${article.word_count} 字</span>
                    ${article.draft ? '<span class="draft-badge">草稿</span>' : ''}
                    ${article.tags.slice(0, 3).map(t => `<span class="tag">${t}</span>`).join('')}
                </div>
            </div>
            <div class="btn-group">
                <button class="btn" onclick="loadArticle('${article.path}')">编辑</button>
                <button class="btn btn-danger" onclick="deleteArticle('${article.path}')">删除</button>
            </div>
        </div>
    `).join('');
}

function filterArticles() {
    const query = document.getElementById('search-input').value.toLowerCase();
    const filtered = articles.filter(a =>
        a.title.toLowerCase().includes(query) ||
        a.tags.some(t => t.toLowerCase().includes(query))
    );
    renderArticles(filtered);
}

function deleteArticle(path) {
    showConfirm('确认删除', '确定要删除这篇文章吗？', () => {
        fetch(`/api/article/${encodeURIComponent(path)}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(result => {
                if (result.success) {
                    loadArticles();
                } else {
                    alert('删除失败');
                }
            });
    });
}

// ========== 统计 ==========
function loadStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('stats-grid').innerHTML = `
                <div class="stat-card">
                    <h3>总文章数</h3>
                    <div class="value">${data.total}</div>
                </div>
                <div class="stat-card">
                    <h3>已发布</h3>
                    <div class="value">${data.published}</div>
                </div>
                <div class="stat-card">
                    <h3>草稿</h3>
                    <div class="value">${data.drafts}</div>
                </div>
                <div class="stat-card">
                    <h3>总字数</h3>
                    <div class="value">${data.total_words.toLocaleString()}</div>
                </div>
            `;
        });
}

// ========== 构建部署 ==========
function startPreview() {
    log('启动本地预览... 请在终端运行: hugo server -D');
}

function buildSite() {
    log('构建中...');
    fetch('/api/build', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            log(data.message || (data.success ? '构建成功!' : '构建失败'));
        });
}

function deploySite() {
    log('部署中...');
    fetch('/api/deploy', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            log(data.message || (data.success ? '部署成功!' : '部署失败'));
        });
}

function log(message) {
    const logEl = document.getElementById('build-log');
    const time = new Date().toLocaleTimeString();
    logEl.textContent += `[${time}] ${message}\n`;
}

// ========== 模态框 ==========
function showConfirm(title, message, onConfirm) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-message').textContent = message;
    document.getElementById('confirm-modal').classList.add('show');

    const confirmBtn = document.getElementById('modal-confirm');
    confirmBtn.onclick = () => {
        closeModal();
        onConfirm();
    };
}

function closeModal() {
    document.getElementById('confirm-modal').classList.remove('show');
}