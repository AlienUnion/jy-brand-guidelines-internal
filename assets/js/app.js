(function () {
  'use strict';

  const body = document.body;
  const modal = document.getElementById('searchModal');
  const searchInput = document.getElementById('globalSearch');
  const results = document.getElementById('searchResults');
  const toast = document.getElementById('toast');

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(window.__toastTimer);
    window.__toastTimer = setTimeout(() => toast.classList.remove('show'), 1600);
  }

  function openSearch() {
    if (!modal) return;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => searchInput && searchInput.focus(), 30);
  }

  function closeSearch() {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
  }

  document.querySelectorAll('[data-open-search]').forEach(el => el.addEventListener('click', openSearch));
  document.querySelectorAll('[data-close-search]').forEach(el => el.addEventListener('click', closeSearch));
  if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeSearch(); });

  document.addEventListener('keydown', e => {
    if ((e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName)) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) {
      e.preventDefault(); openSearch();
    }
    if (e.key === 'Escape') { closeSearch(); body.classList.remove('nav-open'); }
  });

  if (searchInput) searchInput.addEventListener('input', () => {
    const q = searchInput.value.trim().toLowerCase();
    if (!q) { results.innerHTML = '<div class="empty-state">輸入章節、規則、色值或關鍵字</div>'; return; }
    const items = (window.JY_SEARCH_INDEX || []).filter(item => item.text.toLowerCase().includes(q) || item.title.toLowerCase().includes(q)).slice(0, 16);
    const fromSubpage = /\/pages\//.test(location.pathname);
    results.innerHTML = items.length ? items.map(item => {
      const href = fromSubpage && item.url.startsWith('pages/') ? `../${item.url}` : item.url;
      return `<a class="search-result" href="${href}"><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.snippet)}</span></a>`;
    }).join('') : '<div class="empty-state">找不到符合結果</div>';
  });

  function escapeHtml(value) {
    return value.replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}[c]));
  }

  document.querySelectorAll('[data-menu-toggle]').forEach(el => el.addEventListener('click', () => body.classList.toggle('nav-open')));
  document.querySelectorAll('[data-menu-close]').forEach(el => el.addEventListener('click', () => body.classList.remove('nav-open')));

  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const value = button.getAttribute('data-copy');
      try { await navigator.clipboard.writeText(value); showToast(`已複製 ${value}`); }
      catch (_) { showToast('複製失敗，請手動選取'); }
    });
  });

  const typeText = document.getElementById('typeText');
  const typeWeight = document.getElementById('typeWeight');
  const typeSize = document.getElementById('typeSize');
  const typePreview = document.getElementById('typePreview');
  function updateTypePreview() {
    if (!typePreview) return;
    typePreview.textContent = typeText ? typeText.value : '';
    typePreview.style.fontWeight = typeWeight ? typeWeight.value : '400';
    typePreview.style.fontSize = `${typeSize ? typeSize.value : 42}px`;
  }
  [typeText, typeWeight, typeSize].forEach(el => el && el.addEventListener('input', updateTypePreview));
  updateTypePreview();

  const logoAsset = document.getElementById('logoAsset');
  const logoBackground = document.getElementById('logoBackground');
  const logoSize = document.getElementById('logoSize');
  const logoImage = document.getElementById('logoImage');
  const logoPreview = document.getElementById('logoPreview');
  const logoDownload = document.getElementById('logoDownload');
  function updateLogoPreview() {
    if (!logoImage) return;
    const file = logoAsset.value;
    logoImage.src = `../assets/logo/${file}`;
    logoImage.style.width = `${logoSize.value}px`;
    logoPreview.className = `preview-box logo-preview ${logoBackground.value}`;
    logoDownload.href = `../assets/logo/${file}`;
    logoDownload.setAttribute('download', file);
  }
  [logoAsset, logoBackground, logoSize].forEach(el => el && el.addEventListener('input', updateLogoPreview));
  if (logoImage) updateLogoPreview();

  const gridCount = document.getElementById('gridCount');
  const gridColumns = document.getElementById('gridColumns');
  function updateGrid() {
    if (!gridColumns || !gridCount) return;
    const count = Number(gridCount.value);
    gridColumns.style.gridTemplateColumns = `repeat(${count}, 1fr)`;
    gridColumns.innerHTML = '<span></span>'.repeat(count);
  }
  if (gridCount) gridCount.addEventListener('input', updateGrid);
  updateGrid();

  document.querySelectorAll('.checklist').forEach(list => {
    const key = `jy-checklist:${list.dataset.checklist || location.pathname}`;
    let state = {};
    try { state = JSON.parse(localStorage.getItem(key) || '{}'); } catch (_) {}
    list.querySelectorAll('input[type="checkbox"]').forEach(input => {
      input.checked = Boolean(state[input.value]);
      input.closest('.check-item')?.classList.toggle('is-done', input.checked);
      input.addEventListener('change', () => {
        state[input.value] = input.checked;
        localStorage.setItem(key, JSON.stringify(state));
        input.closest('.check-item')?.classList.toggle('is-done', input.checked);
      });
    });
    const reset = document.querySelector(`[data-reset-checklist="${list.dataset.checklist}"]`);
    if (reset) reset.addEventListener('click', () => {
      localStorage.removeItem(key); state = {};
      list.querySelectorAll('input').forEach(input => { input.checked = false; input.closest('.check-item')?.classList.remove('is-done'); });
      showToast('檢核已重設');
    });
  });

  const tocLinks = Array.from(document.querySelectorAll('.toc a'));
  const headings = tocLinks.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window && headings.length) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (!visible) return;
      tocLinks.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === `#${visible.target.id}`));
    }, { rootMargin: '-80px 0px -70% 0px' });
    headings.forEach(h => observer.observe(h));
  }

  document.querySelectorAll('[data-print]').forEach(el => el.addEventListener('click', () => window.print()));

  // 搜尋結果鍵盤導覽（Linear / Stripe ⌘K 式）
  let activeIndex = -1;
  function resultEls() { return Array.from(results ? results.querySelectorAll('.search-result') : []); }
  function setActive(idx) {
    const els = resultEls();
    if (!els.length) return;
    activeIndex = (idx + els.length) % els.length;
    els.forEach((el, i) => el.classList.toggle('is-active', i === activeIndex));
    els[activeIndex].scrollIntoView({ block: 'nearest' });
  }
  if (searchInput) {
    searchInput.addEventListener('input', () => { activeIndex = -1; });
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(activeIndex + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(activeIndex - 1); }
      else if (e.key === 'Enter') { const els = resultEls(); if (activeIndex >= 0 && els[activeIndex]) els[activeIndex].click(); }
    });
  }

  // 標題錨點：點擊複製深層連結（Stripe / GitHub docs 式）
  document.querySelectorAll('[data-anchor]').forEach(a => {
    a.addEventListener('click', async () => {
      const id = a.getAttribute('href');
      const url = `${location.origin}${location.pathname}${id}`;
      try { await navigator.clipboard.writeText(url); showToast('已複製此節連結'); } catch (_) {}
    });
  });
})();
