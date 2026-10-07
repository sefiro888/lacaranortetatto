/* La Cara Norte Custom Tattoo — demo web · JS sin dependencias */
(function () {
  "use strict";
  var WA = "34613075889";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Splash (una vez por sesión, solo portada) ---------- */
  var splash = $(".splash");
  if (splash) {
    var seen = false;
    try { seen = sessionStorage.getItem("lcn-splash") === "1"; } catch (e) {}
    if (seen) { splash.remove(); }
    else {
      document.body.style.overflow = "hidden";
      setTimeout(function () {
        splash.classList.add("hide");
        document.body.style.overflow = "";
        try { sessionStorage.setItem("lcn-splash", "1"); } catch (e) {}
        setTimeout(function () { splash.remove(); }, 1800);
      }, 1900);
    }
  }

  /* ---------- Cabecera ---------- */
  var header = $(".site-header");
  var onScroll = function () { header && header.classList.toggle("scrolled", window.scrollY > 30); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  var toggle = $("#navToggle"), mnav = $("#mobileNav");
  function setMenuTop() { if (header) document.documentElement.style.setProperty("--menu-top", Math.max(0, Math.round(header.getBoundingClientRect().bottom)) + "px"); }
  function setMenu(open) {
    if (!toggle || !mnav) return;
    if (open) setMenuTop();
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    mnav.classList.toggle("open", open);
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (toggle && mnav) {
    toggle.addEventListener("click", function () { setMenu(toggle.getAttribute("aria-expanded") !== "true"); });
    $$("a", mnav).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && mnav.classList.contains("open")) { setMenu(false); toggle.focus(); } });
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) setMenu(false); else if (mnav.classList.contains("open")) setMenuTop(); });
    // acordeones: uno abierto a la vez
    var accs = $$(".mn-acc", mnav);
    accs.forEach(function (d) { d.addEventListener("toggle", function () { if (d.open) accs.forEach(function (o) { if (o !== d) o.open = false; }); }); });
  }

  /* ---------- Estado abierto / cerrado (hora de Madrid) ---------- */
  function madridNow() {
    var parts = new Intl.DateTimeFormat("es-ES", { timeZone: "Europe/Madrid", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false, month: "numeric" }).formatToParts(new Date());
    var o = {}; parts.forEach(function (p) { o[p.type] = p.value; });
    var map = { "lun": 1, "mar": 2, "mié": 3, "jue": 4, "vie": 5, "sáb": 6, "dom": 0 };
    var wd = (o.weekday || "").toLowerCase().replace(".", "");
    return { d: map[wd], h: parseInt(o.hour, 10) % 24, m: parseInt(o.minute, 10), month: parseInt(o.month, 10) };
  }
  function renderStatus() {
    var n = madridNow(), mins = n.h * 60 + n.m;
    var open = n.d >= 1 && n.d <= 5 && mins >= 600 && mins < 1080;
    var summer = n.month === 7 || n.month === 8;
    var text;
    if (open) text = summer ? "Abierto ahora · solo con cita (jul–ago)" : "Abierto ahora · hasta las 18:00";
    else if (n.d >= 1 && n.d <= 5 && mins < 600) text = "Cerrado · abrimos a las 10:00";
    else {
      var next = n.d === 5 && mins >= 1080 ? "el lunes" : n.d === 6 ? "el lunes" : n.d === 0 ? "mañana" : "mañana";
      text = "Cerrado ahora · abrimos " + next + " a las 10:00";
    }
    if (window.innerWidth < 640) text = text.replace("Cerrado ahora · abrimos mañana a las 10:00", "Cerrado · abre mañana 10:00").replace("Cerrado ahora · abrimos el lunes a las 10:00", "Cerrado · abre el lunes 10:00").replace("Cerrado · abrimos a las 10:00", "Cerrado · abre a las 10:00").replace("Abierto ahora · solo con cita (jul–ago)", "Abierto · solo con cita").replace("Abierto ahora · hasta las 18:00", "Abierto · hasta las 18:00");
    $$("[data-open-status]").forEach(function (el) {
      el.classList.toggle("is-open", open);
      var t = $(".status-text", el); if (t) t.textContent = text;
    });
    $$("[data-hours-row]").forEach(function (tr) { tr.classList.toggle("today", parseInt(tr.getAttribute("data-hours-row"), 10) === n.d); });
  }
  renderStatus(); setInterval(renderStatus, 60000);

  /* ---------- Reveal ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: .01, rootMargin: "0px 0px -30px 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- Pausar animaciones del hero fuera de pantalla ---------- */
  var hero = $(".hero");
  if (hero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { hero.classList.toggle("paused", !es[0].isIntersecting); }).observe(hero);
  }

  /* ---------- Contadores ---------- */
  $$("[data-count]").forEach(function (el) {
    var end = parseFloat(el.getAttribute("data-count")), dec = (el.getAttribute("data-count").split(".")[1] || "").length, done = false;
    var run = function () {
      if (done) return; done = true; var t0 = performance.now(), dur = 1400;
      (function tick(t) { var p = Math.min(1, (t - t0) / dur), v = end * (1 - Math.pow(1 - p, 3));
        el.textContent = v.toFixed(dec).replace(".", ","); if (p < 1) requestAnimationFrame(tick); })(t0);
    };
    if ("IntersectionObserver" in window) { new IntersectionObserver(function (es, ob) { if (es[0].isIntersecting) { run(); ob.disconnect(); } }).observe(el); } else run();
  });

  /* ---------- Filtros de galería ---------- */
  var filters = $$(".filter");
  filters.forEach(function (f) {
    f.addEventListener("click", function () {
      filters.forEach(function (x) { x.classList.remove("active"); x.setAttribute("aria-pressed", "false"); });
      f.classList.add("active"); f.setAttribute("aria-pressed", "true");
      var k = f.getAttribute("data-filter");
      $$(".masonry .shot").forEach(function (s) { s.hidden = !(k === "all" || (s.getAttribute("data-cat") || "").split(" ").indexOf(k) > -1); });
    });
  });

  /* ---------- Lightbox ---------- */
  var shots = [], idx = 0, lb;
  function buildLb() {
    lb = document.createElement("div"); lb.className = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true"); lb.setAttribute("aria-label", "Visor de imágenes");
    lb.innerHTML = '<button class="x" aria-label="Cerrar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 5l14 14M19 5L5 19"/></svg></button><button class="prev" aria-label="Anterior"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5l-7 7 7 7"/></svg></button><button class="next" aria-label="Siguiente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg></button><figure><img alt=""><figcaption></figcaption></figure>';
    document.body.appendChild(lb);
    $(".x", lb).onclick = closeLb; $(".prev", lb).onclick = function () { go(-1); }; $(".next", lb).onclick = function () { go(1); };
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
    var sx = 0; lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1); });
  }
  function show() {
    var s = shots[idx], img = $("img", s), full = s.getAttribute("data-full") || img.getAttribute("src");
    $("img", lb).src = full; $("img", lb).alt = img.alt;
    $("figcaption", lb).innerHTML = "<b>" + (s.getAttribute("data-artist") || "") + "</b>" + (img.alt || "");
  }
  function visibleShots(group) { return $$(group + " .shot").filter(function (s) { return !s.hidden; }); }
  function openLb(group, el) { if (!lb) buildLb(); shots = visibleShots(group); idx = shots.indexOf(el); show(); lb.classList.add("open"); document.body.style.overflow = "hidden"; $(".x", lb).focus(); }
  function closeLb() { lb.classList.remove("open"); document.body.style.overflow = ""; }
  function go(d) { idx = (idx + d + shots.length) % shots.length; show(); }
  $$("[data-lightbox]").forEach(function (g) {
    var sel = "[data-lightbox='" + g.getAttribute("data-lightbox") + "']";
    $$(".shot", g).forEach(function (s) { s.addEventListener("click", function (e) { e.preventDefault(); openLb(sel, s); }); });
  });
  document.addEventListener("keydown", function (e) {
    if (!lb || !lb.classList.contains("open")) return;
    if (e.key === "Escape") closeLb(); if (e.key === "ArrowRight") go(1); if (e.key === "ArrowLeft") go(-1);
  });

  /* ---------- ¿Qué artista encaja con tu idea? ---------- */
  var finder = $("[data-finder]");
  if (finder) {
    var res = $(".finder-result", finder);
    $$(".opt", finder).forEach(function (o) {
      o.addEventListener("click", function () {
        $$(".opt", finder).forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        o.setAttribute("aria-pressed", "true");
        $(".fr-img", res).src = o.getAttribute("data-img"); $(".fr-img", res).alt = o.getAttribute("data-name");
        $(".fr-name", res).textContent = o.getAttribute("data-name");
        $(".fr-why", res).textContent = o.getAttribute("data-why");
        $(".fr-link", res).href = o.getAttribute("data-href");
        $(".fr-wa", res).href = "https://wa.me/" + WA + "?text=" + encodeURIComponent("Hola, me interesa " + o.getAttribute("data-topic") + " y me gustaría pedir cita con " + o.getAttribute("data-name") + ".");
        res.classList.add("show");
      });
    });
  }

  /* ---------- Formulario de cita → WhatsApp ---------- */
  var form = $("[data-wa-form]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = new FormData(form), g = function (k) { return (f.get(k) || "").toString().trim(); };
      var lines = ["Hola, soy " + (g("nombre") || "(sin nombre)") + " y quiero pedir cita en La Cara Norte."];
      lines.push("• Servicio: " + g("servicio"));
      if (g("artista")) lines.push("• Artista preferido: " + g("artista"));
      if (g("zona")) lines.push("• Zona del cuerpo: " + g("zona"));
      if (g("tamano")) lines.push("• Tamaño aproximado: " + g("tamano"));
      if (g("fecha")) lines.push("• Cuándo me viene bien: " + g("fecha"));
      if (g("idea")) lines.push("• Mi idea: " + g("idea"));
      lines.push("Adjunto fotos de referencia en este chat. ¡Gracias!");
      window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    });
  }


  /* ---------- Progreso de lectura + volver arriba ---------- */
  var bar = document.createElement("div"); bar.className = "progress"; bar.setAttribute("aria-hidden", "true"); document.body.appendChild(bar);
  var up = document.createElement("button"); up.className = "to-top"; up.setAttribute("aria-label", "Volver arriba");
  up.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
  up.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); }); document.body.appendChild(up);
  var tick = false;
  window.addEventListener("scroll", function () {
    if (tick) return; tick = true;
    requestAnimationFrame(function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + "%";
      up.classList.toggle("show", scrollY > 900); tick = false;
    });
  }, { passive: true });

  /* ---------- Titulares palabra a palabra ---------- */
  $$(".split-words").forEach(function (el) {
    var i = 0;
    (function walk(n) {
      Array.prototype.slice.call(n.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var frag = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (t) {
            if (!t) return;
            if (/^\s+$/.test(t)) { frag.appendChild(document.createTextNode(" ")); return; }
            var w = document.createElement("span"); w.className = "w"; var s = document.createElement("span");
            s.textContent = t; s.style.transitionDelay = (i++ * 70) + "ms"; w.appendChild(s); frag.appendChild(w);
          });
          n.replaceChild(frag, c);
        } else if (c.nodeType === 1 && !c.classList.contains("w")) walk(c);
      });
    })(el);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es, ob) { if (es[0].isIntersecting) { el.classList.add("in"); ob.disconnect(); } }, { threshold: .3 }).observe(el);
    } else el.classList.add("in");
  });

  /* ---------- Carrusel arrastrable ---------- */
  $$(".hscroll").forEach(function (el) {
    var down = false, sx = 0, sl = 0, moved = false;
    el.addEventListener("mousedown", function (e) { down = true; moved = false; sx = e.pageX; sl = el.scrollLeft; });
    window.addEventListener("mouseup", function () { down = false; el.classList.remove("drag"); });
    el.addEventListener("mousemove", function (e) { if (!down) return; var dx = e.pageX - sx; if (Math.abs(dx) > 5) { moved = true; el.classList.add("drag"); } el.scrollLeft = sl - dx; });
    el.addEventListener("click", function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);
  });

  /* ---------- Slider de reseñas ---------- */
  var testi = $("[data-testi]");
  if (testi) {
    var slides = $$(".testi-slide", testi), dots = $$(".testi-dots button", testi), cur = 0, timer;
    var set = function (n) { cur = (n + slides.length) % slides.length; slides.forEach(function (s, i) { s.classList.toggle("on", i === cur); }); dots.forEach(function (d, i) { d.classList.toggle("on", i === cur); }); };
    var auto = function () { clearInterval(timer); timer = setInterval(function () { set(cur + 1); }, 7000); };
    dots.forEach(function (d, i) { d.addEventListener("click", function () { set(i); auto(); }); });
    testi.addEventListener("mouseenter", function () { clearInterval(timer); }); testi.addEventListener("mouseleave", auto);
    set(0); auto();
  }

  /* ---------- Inclinación suave en tarjetas (solo ratón) ---------- */
  if (window.matchMedia("(hover:hover) and (pointer:fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    $$(".artist-card").forEach(function (c) {
      c.addEventListener("mousemove", function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.style.transform = "translateY(-8px) perspective(900px) rotateY(" + (x * 6) + "deg) rotateX(" + (-y * 6) + "deg)";
      });
      c.addEventListener("mouseleave", function () { c.style.transform = ""; });
    });
  }



  /* ---------- Reels: vídeo propio si existe; si no, modo cine con el reproductor de Instagram (solo al pulsar play) ---------- */
  var cine;
  function closeCine() { if (!cine) return; cine.classList.remove("open"); var f = $("iframe", cine); if (f) f.remove(); document.body.style.overflow = ""; if (cine._from) cine._from.focus(); }
  function openCine(id, from) {
    if (!cine) {
      cine = document.createElement("div"); cine.className = "cine"; cine.setAttribute("role", "dialog"); cine.setAttribute("aria-modal", "true"); cine.setAttribute("aria-label", "Reel de Instagram");
      cine.innerHTML = '<button class="cine-x" aria-label="Cerrar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 5l14 14M19 5L5 19"/></svg></button><div class="cine-box"></div><p class="cine-note">Reproductor de Instagram · pulsa Esc o fuera del vídeo para cerrar</p>';
      document.body.appendChild(cine);
      $(".cine-x", cine).addEventListener("click", closeCine);
      cine.addEventListener("click", function (e) { if (e.target === cine || e.target.className === "cine-note") closeCine(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeCine(); });
    }
    cine._from = from;
    var f = document.createElement("iframe");
    f.src = "https://www.instagram.com/reel/" + id + "/embed/";
    f.title = "Reel de Instagram"; f.setAttribute("allowfullscreen", ""); f.setAttribute("allow", "autoplay; encrypted-media; fullscreen");
    $(".cine-box", cine).appendChild(f);
    cine.classList.add("open"); document.body.style.overflow = "hidden"; $(".cine-x", cine).focus();
  }
  $$("[data-reel]").forEach(function (fig) {
    var btn = $(".reel-play", fig);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var vid = fig.getAttribute("data-video");
      if (vid) {
        var v = document.createElement("video");
        v.src = vid; v.controls = true; v.autoplay = true; v.playsInline = true; v.setAttribute("poster", $("img", btn).getAttribute("src")); v.className = "reel-video";
        btn.replaceWith(v);
      } else openCine(fig.getAttribute("data-reel"), btn);
    });
  });

  /* ---------- Año del pie ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
