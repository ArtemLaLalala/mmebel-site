/* М МЕБЕЛЬ — интерактив */
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const WA = '79288204184';
  const waLink = (text) => `https://wa.me/${WA}?text=${encodeURIComponent(text)}`;

  /* header */
  const header = $('.header');
  const onScroll = () => header && header.classList.toggle('scrolled', window.scrollY > 30);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* mobile menu */
  const burger = $('.burger');
  if (burger) {
    burger.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open);
    });
    $$('.mobile-menu a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('menu-open')));
  }

  /* reveal on scroll */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    $$('.rv').forEach(el => io.observe(el));
  } else { $$('.rv').forEach(el => el.classList.add('in')); }

  /* hero slider */
  const slides = $$('.hero-slide');
  if (slides.length) {
    const dots = $('.hero-dots');
    const name = $('.hero-caption b');
    const coll = $('.hero-caption span');
    let i = 0, timer;
    slides.forEach((s, k) => {
      const b = document.createElement('button');
      b.setAttribute('aria-label', 'Слайд ' + (k + 1));
      b.addEventListener('click', () => { go(k); restart(); });
      dots.appendChild(b);
    });
    function go(k) {
      slides[i].classList.remove('active'); dots.children[i].classList.remove('active');
      i = (k + slides.length) % slides.length;
      slides[i].classList.add('active'); dots.children[i].classList.add('active');
      name.textContent = slides[i].dataset.name; if (coll) coll.textContent = slides[i].dataset.coll;
    }
    function restart() { clearInterval(timer); timer = setInterval(() => go(i + 1), 4800); }
    go(0); restart();
  }

  /* collection switcher */
  $$('[data-switch]').forEach(sw => {
    const stage = $(sw.dataset.switch);
    const pill = $('.pill', sw);
    const btns = $$('button', sw);
    function set(btn) {
      const key = btn.dataset.key;
      btns.forEach(b => b.classList.toggle('active', b === btn));
      pill.style.width = btn.offsetWidth + 'px';
      pill.style.transform = `translateX(${btn.offsetLeft - 6}px)`;
      sw.dataset.active = key;
      if (stage) {
        stage.dataset.active = key;
        $$('.coll-panel', stage).forEach(p => p.classList.toggle('active', p.dataset.key === key));
      }
    }
    btns.forEach(b => b.addEventListener('click', () => set(b)));
    const init = () => set(btns.find(b => b.classList.contains('active')) || btns[0]);
    init(); window.addEventListener('resize', init);
    if (document.fonts) document.fonts.ready.then(init);
  });

  /* ---------- catalog ---------- */
  const grid = $('#catalog-grid');
  const cards = $$('.card[data-id]');
  const state = { coll: 'all', type: 'all', mech: 'all', q: '' };

  function applyFilters() {
    if (!grid) return;
    let n = 0;
    cards.forEach(c => {
      const ok = (state.coll === 'all' || c.dataset.coll === state.coll) &&
        (state.type === 'all' || c.dataset.type === state.type) &&
        (state.mech === 'all' || c.dataset.mech === state.mech) &&
        (!state.q || c.dataset.search.includes(state.q));
      c.classList.toggle('hide', !ok);
      if (ok) { n++; c.classList.remove('reveal'); void c.offsetWidth; c.classList.add('reveal'); c.style.animationDelay = Math.min(n, 12) * 30 + 'ms'; }
    });
    $$('.coll-divider', grid).forEach(d => {
      const any = cards.some(c => c.dataset.coll === d.dataset.coll && !c.classList.contains('hide'));
      d.classList.toggle('hide', !any);
    });
    const cnt = $('#count'); if (cnt) cnt.textContent = n + ' ' + plural(n, ['модель', 'модели', 'моделей']);
    $('#empty').style.display = n ? 'none' : 'block';
    const p = new URLSearchParams();
    if (state.coll !== 'all') p.set('c', state.coll);
    if (state.type !== 'all') p.set('t', state.type);
    history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : '') + location.hash);
  }
  function plural(n, f) { const a = n % 100, b = n % 10; return f[(a > 10 && a < 20) ? 2 : b === 1 ? 0 : (b > 1 && b < 5) ? 1 : 2]; }

  if (grid) {
    const params = new URLSearchParams(location.search);
    if (params.get('c')) state.coll = params.get('c');
    if (params.get('t')) state.type = params.get('t');
    $$('.seg[data-filter]').forEach(seg => {
      const key = seg.dataset.filter;
      $$('button', seg).forEach(b => {
        b.classList.toggle('active', b.dataset.v === state[key]);
        b.addEventListener('click', () => {
          $$('button', seg).forEach(x => x.classList.toggle('active', x === b));
          state[key] = b.dataset.v; applyFilters();
        });
      });
    });
    const mech = $('#f-mech'); if (mech) mech.addEventListener('change', () => { state.mech = mech.value; applyFilters(); });
    const q = $('#f-q'); if (q) q.addEventListener('input', () => { state.q = q.value.trim().toLowerCase(); applyFilters(); });
    applyFilters();
  }

  /* ---------- product modal ---------- */
  const modal = $('#modal');
  const data = window.PRODUCTS || [];
  let current = -1, view = 'photo';
  function visibleList() {
    const vis = cards.filter(c => !c.classList.contains('hide')).map(c => c.dataset.id);
    return vis.length ? vis : data.map(p => p.id);
  }
  function openModal(id, push = true) {
    const p = data.find(x => x.id === id); if (!p || !modal) return;
    current = id;
    $('#m-coll').textContent = p.collName; $('#m-coll').className = 'badge ' + p.coll;
    $('#m-type').textContent = p.typeName;
    $('#m-name').textContent = p.name;
    $('#m-sizes').innerHTML = p.sizes.map(s => `<li>${s}</li>`).join('');
    $('#m-mech').textContent = p.mech;
    $('#m-mat').innerHTML = p.mat.map(s => `<li>${s}</li>`).join('');
    const msg = `Здравствуйте! Меня интересует модель «${p.name}» (${p.collName}, стр. ${p.page} каталога). Подскажите, пожалуйста, цену и варианты обивки.`;
    $('#m-wa').href = waLink(msg);
    setView('photo', p);
    modal.classList.add('open'); document.body.style.overflow = 'hidden';
    if (push) history.replaceState(null, '', location.pathname + location.search + '#' + id);
  }
  function setView(v, p) {
    p = p || data.find(x => x.id === current); view = v;
    const img = $('#m-img');
    img.src = v === 'photo' ? `img/products/${p.img}.webp` : `img/pages/${p.img}.webp`;
    img.alt = p.name;
    $$('#m-views button').forEach(b => b.classList.toggle('active', b.dataset.v === v));
  }
  function closeModal() {
    if (!modal) return;
    modal.classList.remove('open'); document.body.style.overflow = '';
    history.replaceState(null, '', location.pathname + location.search);
  }
  function step(d) {
    const list = visibleList(); const k = list.indexOf(current);
    openModal(list[(k + d + list.length) % list.length]);
  }
  if (modal) {
    cards.forEach(c => c.addEventListener('click', (e) => { if (e.target.closest('a')) return; openModal(c.dataset.id); }));
    $$('[data-close]', modal).forEach(b => b.addEventListener('click', closeModal));
    $$('#m-views button').forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
    $('#m-prev').addEventListener('click', () => step(-1));
    $('#m-next').addEventListener('click', () => step(1));
    document.addEventListener('keydown', e => {
      if (!modal.classList.contains('open')) return;
      if (e.key === 'Escape') closeModal();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    });
    let sx = null;
    $('.modal-media', modal).addEventListener('touchstart', e => sx = e.touches[0].clientX, { passive: true });
    $('.modal-media', modal).addEventListener('touchend', e => {
      if (sx === null) return; const dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); sx = null;
    });
    if (location.hash.length > 1) openModal(decodeURIComponent(location.hash.slice(1)), false);
  }

  /* lazy map */
  $$('[data-map]').forEach(box => {
    const load = () => { if (box.dataset.loaded) return; box.dataset.loaded = 1; box.innerHTML = `<iframe loading="lazy" src="${box.dataset.map}" title="Карта"></iframe>`; };
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { load(); io.disconnect(); } }));
      io.observe(box);
    } else load();
  });

  /* map switch on contacts */
  $$('[data-map-btn]').forEach(b => b.addEventListener('click', () => {
    const box = $('#map'); box.dataset.loaded = ''; box.dataset.map = b.dataset.mapBtn;
    box.innerHTML = `<iframe loading="lazy" src="${b.dataset.mapBtn}" title="Карта"></iframe>`;
    box.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }));
})();
