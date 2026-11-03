/* Shared interactions. Swedish is the default; static /fi/ pages are Finnish. */
document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('.site-menu-toggle');
  const menu = document.querySelector('.site-menu');
  const closeMenu = () => {
    button?.setAttribute('aria-expanded', 'false');
    menu?.classList.remove('is-open');
  };
  button?.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    menu.classList.toggle('is-open', open);
  });
  menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const wasOpen = button?.getAttribute('aria-expanded') === 'true';
    closeMenu();
    document.querySelectorAll('.site-dropdown[open]').forEach(details => {
      details.open = false;
      if (!wasOpen) details.querySelector('summary').focus();
    });
    if (wasOpen) button.focus();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1280) closeMenu();
  });
  const form = document.getElementById('contactForm');
  if (!form) return;
  const finnish = document.documentElement.lang === 'fi';
  const labels = finnish
    ? { subject: 'Yhteydenotto', name: 'Nimi', email: 'Sähköposti', phone: 'Puhelin', service: 'Palvelu', car: 'Auto', status: 'Sähköpostiohjelma avataan. Lähetä viesti sieltä. Jos ohjelma ei avaudu, kirjoita osoitteeseen info@powerafix.com.' }
    : { subject: 'Förfrågan', name: 'Namn', email: 'E-post', phone: 'Telefon', service: 'Tjänst', car: 'Bil', status: 'Ditt e-postprogram öppnas. Skicka meddelandet därifrån. Om programmet inte öppnas kan du skriva till info@powerafix.com.' };
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    const subject = `${labels.subject} — ${data.carModel || 'PoweraFix'}`;
    const body = `${data.message}\n\n${labels.name}: ${data.firstName} ${data.lastName}\n${labels.email}: ${data.email}\n${labels.phone}: ${data.phone}\n${labels.service}: ${data.service}\n${labels.car}: ${data.carModel}`;
    document.getElementById('formStatus').textContent = labels.status;
    window.location.href = `mailto:info@powerafix.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
});
