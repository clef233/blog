/**
 * 目录（TOC）功能
 * - 滚动高亮当前章节
 * - 点击目录项平滑滚动
 * - 移动端折叠/展开
 */

document.addEventListener('DOMContentLoaded', function() {
  const tocLinks = document.querySelectorAll('.toc-link');
  const headings = document.querySelectorAll('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]');

  if (!tocLinks.length || !headings.length) return;

  // ========== 移动端折叠 ==========
  window.toggleToc = function() {
    const sidebar = document.getElementById('toc-sidebar');
    if (sidebar) {
      sidebar.classList.toggle('open');
    }
  };

  // 点击遮罩关闭
  document.getElementById('toc-sidebar')?.addEventListener('click', function(e) {
    if (e.target === this) {
      this.classList.remove('open');
    }
  });

  // ========== IntersectionObserver 高亮 ==========
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          const link = document.querySelector(`.toc-link[href="#${id}"]`);
          if (link) {
            tocLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
          }
        }
      });
    },
    {
      rootMargin: '-80px 0px -70% 0px',
      threshold: 0
    }
  );

  headings.forEach((heading) => observer.observe(heading));

  // ========== 点击滚动 ==========
  tocLinks.forEach((link) => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const id = this.getAttribute('href').substring(1);
      const target = document.getElementById(id);
      if (target) {
        // 更新高亮
        tocLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');

        // 滚动
        const offset = target.getBoundingClientRect().top + window.pageYOffset - 80;
        window.scrollTo({ top: offset, behavior: 'smooth' });

        // 移动端关闭目录
        const sidebar = document.getElementById('toc-sidebar');
        if (sidebar && window.innerWidth <= 768) {
          sidebar.classList.remove('open');
        }
      }
    });
  });
});