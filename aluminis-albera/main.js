// mobile menu
const header = document.querySelector('.site-header');
document.querySelector('.burger')?.addEventListener('click', () => header.classList.toggle('open'));

// product / project filters
document.querySelectorAll('[data-filter-group]').forEach(group => {
  const chips = group.querySelectorAll('.chip');
  const items = document.querySelectorAll(group.dataset.filterGroup);
  chips.forEach(chip => chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.toggle('on', c === chip));
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

// lightbox
const lb = document.createElement('div');
lb.className = 'lb';
lb.innerHTML = '<button aria-label="Tancar">&times;</button><img alt="">';
document.body.appendChild(lb);
const closeLb = () => lb.classList.remove('open');
lb.addEventListener('click', closeLb);
document.addEventListener('keydown', e => e.key === 'Escape' && closeLb());
document.querySelectorAll('a[data-lightbox]').forEach(a => a.addEventListener('click', e => {
  e.preventDefault();
  lb.querySelector('img').src = a.getAttribute('href');
  lb.classList.add('open');
}));

// contact form (demo only: no backend yet)
document.querySelector('#contact-form')?.addEventListener('submit', e => {
  e.preventDefault();
  e.target.outerHTML = '<p class="form-ok">Gràcies! Hem rebut la teva sol·licitud i et respondrem aviat.</p>';
});
