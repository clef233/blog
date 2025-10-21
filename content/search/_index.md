---
title: "搜索"
layout: "search"
summary: "在博客中搜索文章"
---

# 搜索文章

在下方输入关键词搜索博客文章：

<script src="https://cdn.jsdelivr.net/npm/fuse.js/dist/fuse.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/cferdinandi/smooth-scroll/dist/smooth-scroll.polyfills.min.js"></script>

<div class="search-container">
  <input type="search" id="search-input" placeholder="搜索文章..." aria-label="搜索文章">
  <div id="search-results"></div>
</div>

<style>
.search-container {
  max-width: 800px;
  margin: 2rem auto;
}

.search-container input {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  margin-bottom: 2rem;
}

#search-results {
  min-height: 200px;
}

.search-result {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--background-secondary);
}

.search-result h3 {
  margin: 0 0 0.5rem 0;
}

.search-result .search-meta {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.search-result .search-excerpt {
  color: var(--text-primary);
  line-height: 1.6;
}

.highlight {
  background-color: var(--accent-color);
  color: white;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}

.no-results {
  text-align: center;
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-top: 3rem;
}
</style>

<script>
// 搜索功能实现
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
let fuse;
let searchData = [];

// 加载搜索数据
fetch('/index.json')
  .then(response => response.json())
  .then(data => {
    searchData = data;
    fuse = new Fuse(data, {
      keys: ['title', 'content', 'tags', 'categories'],
      threshold: 0.3,
      includeScore: true,
      includeMatches: true,
      minMatchCharLength: 1
    });
  })
  .catch(error => {
    console.error('搜索数据加载失败:', error);
    searchResults.innerHTML = '<div class="no-results">搜索数据加载失败</div>';
  });

// 搜索处理函数
function handleSearch() {
  const query = searchInput.value.trim();

  if (query.length < 1) {
    searchResults.innerHTML = '';
    return;
  }

  if (!fuse) {
    searchResults.innerHTML = '<div class="no-results">搜索索引加载中...</div>';
    return;
  }

  const results = fuse.search(query);
  displayResults(results, query);
}

// 显示搜索结果
function displayResults(results, query) {
  if (results.length === 0) {
    searchResults.innerHTML = '<div class="no-results">未找到相关文章</div>';
    return;
  }

  const html = results.map(result => {
    const item = result.item;
    const highlightedTitle = highlightText(item.title, query);
    const highlightedContent = highlightText(item.content.substring(0, 300) + '...', query);

    return `
      <div class="search-result">
        <h3><a href="${item.permalink}">${highlightedTitle}</a></h3>
        <div class="search-meta">
          📅 ${new Date(item.date).toLocaleDateString('zh-CN')}
          ${item.tags ? `🏷️ ${item.tags.join(', ')}` : ''}
        </div>
        <div class="search-excerpt">${highlightedContent}</div>
      </div>
    `;
  }).join('');

  searchResults.innerHTML = html;
}

// 高亮搜索关键词
function highlightText(text, query) {
  const regex = new RegExp(`(${query})`, 'gi');
  return text.replace(regex, '<span class="highlight">$1</span>');
}

// 事件监听
searchInput.addEventListener('input', handleSearch);

// 页面加载时聚焦搜索框
window.addEventListener('load', () => {
  searchInput.focus();
});
</script>