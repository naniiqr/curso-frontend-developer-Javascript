// mobile menu
const header = document.querySelector('.site-header');
const burger = document.querySelector('.burger');
burger?.addEventListener('click', () => {
  const open = header.classList.toggle('open');
  burger.setAttribute('aria-expanded', open);
  burger.setAttribute('aria-label', open ? 'Tancar el menú' : 'Obrir el menú');
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && header.classList.contains('open')) { burger.click(); burger.focus(); }
});

// product / project filters
document.querySelectorAll('[data-filter-group]').forEach(group => {
  const chips = group.querySelectorAll('.chip');
  const items = document.querySelectorAll(group.dataset.filterGroup);
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => { c.classList.toggle('on', c === chip); c.setAttribute('aria-pressed', c === chip); });
    items.forEach(it => { it.hidden = chip.dataset.f !== 'all' && it.dataset.cat !== chip.dataset.f; });
  }));
});

// project slider
document.querySelectorAll('.slider').forEach(s => {
  const track = s.querySelector('.track');
  const step = () => track.clientWidth * 0.5;
  s.querySelector('.prev')?.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  s.querySelector('.next')?.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
});

// lightbox (focus moves in, Escape closes, focus returns to the thumbnail)
const lb = document.createElement('div');
lb.className = 'lb';
lb.setAttribute('role', 'dialog');
lb.setAttribute('aria-modal', 'true');
lb.setAttribute('aria-label', 'Imatge ampliada');
lb.innerHTML = '<button aria-label="Tancar">&times;</button><img alt="">';
document.body.appendChild(lb);
let lastFocus = null;
const closeLb = () => { lb.classList.remove('open'); lastFocus?.focus(); };
lb.addEventListener('click', closeLb);
document.addEventListener('keydown', e => e.key === 'Escape' && lb.classList.contains('open') && closeLb());
document.querySelectorAll('a[data-lightbox]').forEach(a => a.addEventListener('click', e => {
  e.preventDefault();
  lastFocus = a;
  const img = lb.querySelector('img');
  img.src = a.getAttribute('href');
  img.alt = a.querySelector('img')?.alt || '';
  lb.classList.add('open');
  lb.querySelector('button').focus();
}));

// contact form (demo only: no backend yet). Validates on blur, clears on edit.
const form = document.querySelector('#contact-form');
if (form) {
  const fields = [...form.querySelectorAll('[required]')];
  const err = f => document.getElementById(f.getAttribute('aria-describedby'));
  const check = f => {
    const bad = f.type === 'checkbox' ? !f.checked : (!f.value.trim() || !f.checkValidity());
    f.setAttribute('aria-invalid', bad);
    const e = err(f); if (e) e.hidden = !bad;
    return !bad;
  };
  fields.forEach(f => {
    f.addEventListener('blur', () => check(f));
    f.addEventListener('input', () => { if (f.getAttribute('aria-invalid') === 'true') check(f); });
    f.addEventListener('change', () => { if (f.type === 'checkbox') check(f); });
  });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const bad = fields.filter(f => !check(f));
    if (bad.length) { bad[0].focus(); return; }
    form.outerHTML = '<p class="form-ok" role="status">Gràcies! Hem rebut la teva sol·licitud i et respondrem aviat.</p>';
  });
}
