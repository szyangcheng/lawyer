(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  if (menu && nav) {
    menu.hidden = false;
    const close = () => { nav.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false'); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', (event) => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { close(); menu.focus(); }
    });
  }
  const copyButton = document.querySelector('[data-copy]');
  if (copyButton) {
    copyButton.hidden = false;
    copyButton.addEventListener('click', async () => {
      const status = document.querySelector('#copy-status');
      try {
        if (!navigator.clipboard) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(copyButton.dataset.copy);
        status.textContent = '微信号已复制：13434447220。可前往微信搜索添加。';
      } catch (_) {
        status.textContent = '未能自动复制，请长按或手动复制微信号：13434447220。';
      }
    });
  }
  const search = document.querySelector('#article-search');
  if (search) {
    document.querySelector('.library-controls').hidden = false;
    const rows = [...document.querySelectorAll('.article-row')];
    const buttons = [...document.querySelectorAll('[data-filter]')];
    const status = document.querySelector('.result-status');
    status.hidden = false;
    let filter = 'all';
    const update = () => {
      const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let count = 0;
      rows.forEach((row) => {
        const haystack = row.textContent.toLocaleLowerCase();
        const matches = (filter === 'all' || row.dataset.kind === filter) && words.every((word) => haystack.includes(word));
        row.hidden = !matches;
        if (matches) count++;
      });
      status.textContent = `共 ${count} 篇文章`;
      document.querySelector('.empty-state').hidden = count > 0;
    };
    search.addEventListener('input', update);
    buttons.forEach((button) => button.addEventListener('click', () => {
      filter = button.dataset.filter;
      buttons.forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      update();
    }));
    update();
  }
  const toc = document.querySelector('.article-toc');
  if (toc) {
    const headings = [...document.querySelectorAll('.article-body h2, .article-body h3')];
    if (headings.length > 1) {
      headings.forEach((heading, index) => {
        if (!heading.id) heading.id = `section-${index + 1}`;
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${encodeURIComponent(heading.id)}`;
        link.textContent = heading.textContent;
        item.append(link);
        toc.querySelector('ol').append(item);
      });
      toc.hidden = false;
    }
  }
})();
