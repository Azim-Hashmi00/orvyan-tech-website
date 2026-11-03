/* Orvyan Tech v3 — behaviour */

(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- year ---- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---- sticky header state ---- */
  var head = document.querySelector('.site-head');
  if (head) {
    var onScroll = function () {
      head.classList.toggle('stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- mobile menu ---- */
  var menuBtn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        nav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- reveal on scroll ---- */
  var targets = document.querySelectorAll('.reveal');
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('in'); });
  }

  /* ---- subtle pointer glow on cards ---- */
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.card').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
        card.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
      });
    });
  }

  /* ---- page transition out ---- */
  if (!reduce) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || a.target === '_blank' || a.hasAttribute('download')) return;
      if (a.host && a.host !== window.location.host) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      document.body.classList.add('leaving');
      setTimeout(function () { window.location.href = href; }, 190);
    });
    window.addEventListener('pageshow', function () {
      document.body.classList.remove('leaving');
    });
  }
})();

/* docked WhatsApp window: starts open, collapses to a round button */
(function(){
  var dock = document.getElementById('waDock');
  if (!dock) return;
  var minBtn = dock.querySelector('.wa-min');
  function collapse(){ dock.classList.add('min'); }
  function expand(){ dock.classList.remove('min'); }
  minBtn && minBtn.addEventListener('click', function(e){ e.stopPropagation(); collapse(); });
  dock.addEventListener('click', function(){ if (dock.classList.contains('min')) expand(); });
  dock.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' ') expand(); });
  if (window.matchMedia('(max-width:760px)').matches) setTimeout(collapse, 4200);
})();
