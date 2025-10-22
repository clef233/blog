// ========================================
   🎯 增强版目录高亮功能
   ========================================
document.addEventListener('DOMContentLoaded', function() {
    const tocLinks = document.querySelectorAll('.toc-link');
    const headings = document.querySelectorAll('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]');

    if (!tocLinks.length || !headings.length) return;

    // 配置选项
    const config = {
        offset: 100,              // 滚动偏移量
        threshold: 0.3,           // 元素可见度阈值
        smoothScroll: true,        // 是否启用平滑滚动
        scrollOffset: 80,         // 滚动到元素时的偏移
        debounceDelay: 100        // 防抖延迟
    };

    // 移除所有active类
    function removeActiveClass() {
        tocLinks.forEach(link => link.classList.remove('active'));
    }

    // 添加active类到当前链接
    function addActiveClass(link) {
        link.classList.add('active');
    }

    // 检查元素是否在视口中（增强版）
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;
        const windowWidth = window.innerWidth || document.documentElement.clientWidth;

        // 元素在视口中的可见比例
        const visibleHeight = Math.min(rect.bottom, windowHeight) - Math.max(rect.top, 0);
        const visibleWidth = Math.min(rect.right, windowWidth) - Math.max(rect.left, 0);
        const elementHeight = rect.height;
        const elementWidth = rect.width;

        const visibleHeightRatio = visibleHeight / elementHeight;
        const visibleWidthRatio = elementWidth > 0 ? visibleWidth / elementWidth : 0;

        // 元素至少有一定比例在视口中
        return visibleHeightRatio >= config.threshold && rect.top < windowHeight;
    }

    // 获取元素在视口中的位置（0-1之间）
    function getElementPosition(element) {
        const rect = element.getBoundingClientRect();
        const windowHeight = window.innerHeight || document.documentElement.clientHeight;

        if (rect.top >= windowHeight) {
            return -1; // 元素在视口下方
        }
        if (rect.bottom <= 0) {
            return 1; // 元素在视口上方
        }

        // 计算元素在视口中的相对位置
        const elementCenter = rect.top + rect.height / 2;
        return elementCenter / windowHeight;
    }

    // 获取当前最合适的标题
    function getCurrentHeading() {
        let bestHeading = null;
        let bestPosition = Infinity;
        let bestInViewport = false;

        headings.forEach(heading => {
            const position = getElementPosition(heading);
            const inViewport = isInViewport(heading);

            // 优先选择在视口中的元素
            if (inViewport && (!bestInViewport || Math.abs(position) < Math.abs(bestPosition))) {
                bestHeading = heading;
                bestPosition = position;
                bestInViewport = true;
            } else if (!bestInViewport && position > 0 && position < bestPosition) {
                // 如果没有元素在视口中，选择即将进入视口的元素
                bestHeading = heading;
                bestPosition = position;
            }
        });

        return bestHeading;
    }

    // 更新活动链接
    function updateActiveLink() {
        const currentHeading = getCurrentHeading();

        if (currentHeading) {
            const currentId = currentHeading.getAttribute('id');
            const currentLink = document.querySelector(`.toc-link[href="#${currentId}"]`);

            if (currentLink) {
                // 检查是否已经是活动链接
                if (!currentLink.classList.contains('active')) {
                    removeActiveClass();
                    addActiveClass(currentLink);

                    // 可选：滚动到视口中确保活动链接可见
                    ensureLinkVisible(currentLink);
                }
            } else {
                // 如果没有找到对应的链接，清除所有活动状态
                removeActiveClass();
            }
        } else {
            // 如果没有当前标题，清除所有活动状态
            removeActiveClass();
        }
    }

    // 确保活动链接在视口中可见
    function ensureLinkVisible(link) {
        const tocContainer = link.closest('.sidebar');
        if (!tocContainer) return;

        const containerRect = tocContainer.getBoundingClientRect();
        const linkRect = link.getBoundingClientRect();

        // 检查链接是否在容器视口中
        if (linkRect.top < containerRect.top || linkRect.bottom > containerRect.bottom) {
            // 平滑滚动到链接位置
            const scrollTarget = tocContainer.scrollTop + (linkRect.top - containerRect.top - 50);
            tocContainer.scrollTo({
                top: scrollTarget,
                behavior: 'smooth'
            });
        }
    }

    // 防抖函数
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                timeout = null;
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // 滚动事件处理（防抖）
    const handleScroll = debounce(function() {
        updateActiveLink();
    }, config.debounceDelay);

    // 平滑滚动到目标元素
    function smoothScrollToElement(targetElement) {
        if (!targetElement) return;

        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - config.scrollOffset;

        if (config.smoothScroll) {
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        } else {
            window.scrollTo(0, offsetPosition);
        }
    }

    // 为目录链接添加点击事件
    tocLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                // 立即更新活动状态
                removeActiveClass();
                addActiveClass(this);

                // 平滑滚动到目标
                smoothScrollToElement(targetElement);

                // 延迟再次更新，确保滚动后的状态正确
                setTimeout(() => {
                    updateActiveLink();
                }, 500);
            }
        });
    });

    // 监听滚动事件
    window.addEventListener('scroll', handleScroll, { passive: true });

    // 监听窗口大小变化
    window.addEventListener('resize', handleScroll, { passive: true });

    // 监听主题变化（如果支持）
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                // 主题变化时重新计算位置
                setTimeout(updateActiveLink, 100);
            }
        });
    });

    // 观察html元素的主题变化
    const htmlElement = document.documentElement;
    if (htmlElement) {
        observer.observe(htmlElement, {
            attributes: true,
            attributeFilter: ['data-theme', 'class']
        });
    }

    // 初始检查
    setTimeout(() => {
        updateActiveLink();
    }, 100);

    // 添加键盘导航支持
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
            const activeLink = document.querySelector('.toc-link.active');
            const allLinks = Array.from(tocLinks);
            const currentIndex = activeLink ? allLinks.indexOf(activeLink) : -1;

            let nextIndex;
            if (e.key === 'ArrowUp') {
                nextIndex = currentIndex > 0 ? currentIndex - 1 : allLinks.length - 1;
            } else {
                nextIndex = currentIndex < allLinks.length - 1 ? currentIndex + 1 : 0;
            }

            if (nextIndex >= 0 && nextIndex < allLinks.length) {
                e.preventDefault();
                allLinks[nextIndex].click();
            }
        }
    });

    console.log('目录高亮功能已启用');
});