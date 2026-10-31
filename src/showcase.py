"""Local presentation only: original SVG, scripted story and isolated progressive enhancement."""

LOGO = """<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 3 56 13v20c0
14-13 23-24 28C21 56 8 47 8 33V13z" fill="currentColor"/><path d="M19 26c0-10 5-15 13-15s13
5 13 15v13H19z" fill="#faf7ef"/><path d="M23 28c0-6 3-10 9-10s9 4 9 10v8c0 8-18 8-18 0z"
fill="#ffb695"/><g stroke="#17182f" stroke-width="2"><circle cx="26" cy="30" r="6"/>
<circle cx="39" cy="30" r="6"/><path d="M32 30h1m-5 12q4 4 8 0"/></g><circle cx="32" cy="21"
r="2" fill="#f15f44"/></svg>"""
NAV = (
    '<nav class="sc-nav" aria-label="Main"><a class="sc-brand" href="#showcase-intro">'
    + LOGO
    + """
<span>DADI<span class="sc-brand-sub">VS DIGITAL ARREST</span></span></a><div class="sc-nav-links">
<a href="#sc-story">The idea</a><a href="#sc-engine">Inside Dadi</a>
<a href="#live-lab" class="sc-nav-cta">Try the simulation <span aria-hidden="true">↗</span></a>
</div></nav>"""
)

INTRO = """<div class="sc-root" data-showcase-root>
<section class="sc-hero" aria-labelledby="sc-title">
<div class="sc-hero-copy"><div class="sc-kicker"><span class="sc-dot"></span> A LITTLE PATIENCE.
A DIFFERENT KIND OF DEFENCE.</div><h1 id="sc-title">Waste<br><span class="sc-italic">their</span>
time.<br>
<span class="sc-outline">Keep yours.</span></h1><p>Meet Dadi. A grandmother persona designed to turn
scam-call pressure into a slower conversation.</p><div class="sc-hero-actions">
<a class="sc-primary" href="#live-lab">Try Dadi in the call lab <span
aria-hidden="true">↗</span></a>
<a class="sc-text-link" href="#sc-story">See her in action <span
aria-hidden="true">↓</span></a></div>
<div class="sc-small-note">A scam-awareness prototype. Teammates role-play every call.</div></div>
<div class="sc-art" data-sc-tilt aria-label="Illustration of Dadi with her old phone">
<div class="sc-orbit sc-orbit-one"></div><div class="sc-orbit sc-orbit-two"></div>
<span class="sc-art-caption">UNRUSHED. UNBOTHERED. UNEXPECTED.</span>
<svg class="sc-dadi" viewBox="0 0 520 590" fill="none" role="img"
aria-label="Dadi, glasses on, phone in hand">
<defs><linearGradient id="sc-sari" x1="130" y1="290" x2="440" y2="570"
gradientUnits="userSpaceOnUse">
<stop stop-color="#d8f47f"/><stop offset="1" stop-color="#a8c84b"/></linearGradient>
<pattern id="sc-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="4" cy="4"
r="2" fill="#203820" opacity=".15"/></pattern></defs>
<path d="M73 582c0-134 45-219 184-219s191 87 191 219" fill="url(#sc-sari)"/>
<path d="M73 582c0-134 45-219 184-219s191 87 191 219" fill="url(#sc-dots)"/>
<path d="m284 386-118 196h91l98-176" fill="#eff9c5"/><path d="M156 221c-26-91 12-155 92-155
95 0 141 86 111 177l-16 120H175z" fill="#f7f0de"/>
<path d="M210 344v54c0 27 68 32 68 0v-54" fill="#dd936d"/>
<ellipse cx="246" cy="256" rx="91" ry="112" fill="#ffba90"/>
<path d="M153 236c6-103 59-122 95-120 43-5 96 43 91 117-46-15-73-46-87-79-15 44-47
70-99 82" fill="#fffaf1"/><path d="M174 211c22-12 44-21 69-54m23-10c15 26 29 45 50 58"
stroke="#ded6c8" stroke-width="4" stroke-linecap="round"/>
<path d="M180 260c0-26 16-39 34-39 25 0 37 18 37 39s-12 37-37 37c-20 0-34-13-34-37z
m78 0c0-26 16-39 34-39 25 0 37 18 37 39s-12 37-37 37c-20 0-34-13-34-37z"
stroke="#292735" stroke-width="7"/><path d="M251 252h7m-78-5-22-6m171 6 12-5"
stroke="#292735" stroke-width="6"/><circle cx="217" cy="258" r="4" fill="#292735"/>
<circle cx="289" cy="258" r="4" fill="#292735"/><path d="M249 269v27h-10m-14 26q27 25 53-2"
stroke="#955b49" stroke-width="4" stroke-linecap="round"/>
<circle cx="251" cy="211" r="6" fill="#f15f44"/><circle cx="160" cy="289" r="8"
stroke="#d0a14a" stroke-width="5"/><path d="M343 364q49 18 50 91l-54 14-36-73"
fill="#f4f1ce"/><path d="M368 451c-6-35-5-46 2-57 6-8 18-10 26 1l15 44" fill="#ffba90"/>
<g transform="rotate(-16 393 384)"><rect x="359" y="300" width="73" height="141" rx="17"
fill="#222435"/><rect x="370" y="319" width="51" height="48" rx="5" fill="#b5c997"/>
<path d="M384 311h24" stroke="#737784" stroke-width="3"/><g fill="#a4a6ae">
<rect x="372" y="380" width="11" height="7" rx="2"/><rect x="389" y="380" width="11"
height="7" rx="2"/><rect x="406" y="380" width="11" height="7" rx="2"/>
<rect x="372" y="394" width="11" height="7" rx="2"/><rect x="389" y="394" width="11"
height="7" rx="2"/><rect x="406" y="394" width="11" height="7" rx="2"/>
<rect x="372" y="408" width="11" height="7" rx="2"/><rect x="389" y="408" width="11"
height="7" rx="2"/><rect x="406" y="408" width="11" height="7" rx="2"/></g></g>
<path d="M358 416q14-34 23-25c10 9-2 38-5 45" fill="#ffba90"/>
<path d="m102 139 8-23 8 23 23 8-23 8-8 23-8-23-23-8zM377 183l5-16 5 16 16 5-16
5-5 16-5-16-16-5z" fill="#f7f0de"/></svg>
<div class="sc-sticker"><span>HER SUPERPOWER?</span><strong>“One minute,<br>beta.”</strong>
<svg viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M20 4v32M4 20h32M9 9l22 22M9
31 31 9" stroke="currentColor" stroke-width="3"/></svg></div>
<div class="sc-caption-card"><span class="sc-dot"></span><div><b>They bring urgency.</b>
<span>She brings a missing pair of glasses.</span></div><span
class="sc-caption-arrow">↗</span></div>
</div></section>
<div class="sc-ribbon" aria-label="Project principles"><span>MORE PATIENCE</span><i>✳</i>
<span>LESS PANIC</span><i>✳</i><span>ALWAYS YOUR CHOICE</span><i>✳</i><span>ONE MORE
MINUTE</span></div>
<section class="sc-story" id="sc-story" aria-labelledby="sc-story-title" data-reveal>
<div class="sc-section-top"><span class="sc-label">01 / THE IDEA</span><span>PRESSURE, MEET
PATIENCE.</span></div>
<div class="sc-story-grid"><div><h2 id="sc-story-title">Their script.<br>Her <em>plot
twist.</em></h2>
<p>A rushed caller wants a rushed decision. Dadi slows the story down: a question, a lost
notebook, another explanation. Explore the idea one beat at a time.</p>
<div class="sc-scene-buttons" role="group" aria-label="Scripted conversation scenes">
<button type="button" data-sc-scene="0" aria-pressed="true"><span>01</span> The pressure
<b>↗</b></button>
<button type="button" data-sc-scene="1" aria-pressed="false"><span>02</span> The detour
<b>↗</b></button>
<button type="button" data-sc-scene="2" aria-pressed="false"><span>03</span> The extra minute
<b>↗</b></button>
</div></div><div class="sc-scene" aria-live="polite" aria-atomic="true">
<div class="sc-scene-top"><span><span class="sc-dot"></span> SCRIPTED PREVIEW</span>
<span data-sc-count>01 / 03</span></div><div class="sc-caller"><span>THE CALLER</span>
<p data-sc-caller>“Your bank account will be blocked. You must act now.”</p></div>
<div class="sc-wave"
aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
<div class="sc-grandma"><span>DADI</span><p data-sc-reply>“Which branch, beta? Let me find my
glasses first.”</p></div>
<div class="sc-scene-bottom"><span data-sc-tactic>TACTIC / ASK THEM TO REPEAT</span>
<small>Illustrative dialogue. No model, audio or service calls.</small></div></div></div></section>
<section class="sc-engine" id="sc-engine" data-reveal aria-labelledby="sc-engine-title">
<div class="sc-section-top"><span class="sc-label">02 / UNDER THE HOOD</span>
<span>ONE VOICE. THREE PARTS.</span></div><div class="sc-engine-heading"><h2 id="sc-engine-title">
She listens.<br>She thinks. <em>She stalls.</em></h2><p>A sequential speech loop with a human in
control.
Tap each part to see its job. These are architecture roles, not connection indicators.</p></div>
<div class="sc-engine-grid"><details open><summary><span class="sc-engine-no">01 ↗</span>
<span class="sc-engine-name">Listen</span><b>PRISMA · SPEECH TO TEXT</b><span
class="sc-expand">+</span></summary>
<p>A short recording becomes caller text. Your language choice selects the transcription route.
The call lab accepts WAV clips up to thirty seconds.</p></details>
<details><summary><span class="sc-engine-no">02 ✳</span><span class="sc-engine-name">Think</span>
<b>SARVAM · THE BRAIN</b><span class="sc-expand">+</span></summary><p>The configured brain uses
context,
family facts and a fresh assigned tactic. Output guards check the reply before it reaches speech.
Real language quality still needs review.</p></details>
<details><summary><span class="sc-engine-no">03 ≋</span><span class="sc-engine-name">Speak</span>
<b>TIMBRE · TEXT TO SPEECH</b><span class="sc-expand">+</span></summary><p>The reply becomes audio,
then the caller gets another turn. Real speech services require explicit configuration.
The key-free test fixture does not synthesize audio.</p></details></div></section>
<div id="live-lab" class="sc-lab-heading" data-reveal><span class="sc-label">03 / THE CALL
LAB</span>
<h2>Now, put Dadi<br><em>on the line.</em> <span aria-hidden="true">↘</span></h2>
<p>Be the role-play caller. Share two caller messages, make the human choice,
and see what happens next.
Your configured mode and any errors are shown in the workspace below.</p></div>
</div>"""

OUTRO = """<div class="sc-root sc-outro" data-showcase-root><section class="sc-impact" data-reveal>
<span class="sc-label">THE POINT OF EVERY EXTRA MINUTE</span><h2>Less pressure on people.<br>
<em>More patience on the line.</em></h2><p>Designed to explore how a grandmother decoy could occupy
an unwanted caller and make scam tactics easier to recognise. Our prototype uses teammate
role-play. It has not measured real scam prevention or money saved.</p><a href="#live-lab"
class="sc-primary">Try another role-play <span aria-hidden="true">↑</span></a>
<div class="sc-impact-seal" aria-hidden="true">HUMAN<br>CHOICE<br><span>ALWAYS
↗</span></div></section>
<section class="sc-faq" data-reveal><div><span class="sc-label">A FEW GOOD QUESTIONS</span>
<h2>Before you<br>pick up.</h2></div><div class="sc-faq-list">
<details><summary>Does this connect to real scammers?<span>+</span></summary><p>No. This is a
clearly
labelled scam-awareness simulation with teammates. There is no actual phone
connection.</p></details>
<details><summary>Can I try it without API keys?<span>+</span></summary><p>Yes, in the configured
Sarvam test-fixture mode. Its canned replies are labelled. Mock speech has no synthesized audio;
real Prisma and Timbre calls require explicit opt-in and process keys.</p></details>
<details><summary>What about Hindi, Kannada and English?<span>+</span></summary><p>The speech UI
routes
Hindi/Hinglish, Kannada/Kanglish and English explicitly. Native-script replies are checked.
Real accuracy, pronunciation and naturalness still require testing and native-speaker
review.</p></details>
<details><summary>What does the case file actually measure?<span>+</span></summary><p>In the Sarvam
speech path it shows tracked turns, recorded caller duration, assigned tactics and guard
rejections. Recorded duration is a simulation proxy, not proven scammer time wasted.</p></details>
</div></section><footer class="sc-footer"><a href="#showcase-intro"
class="sc-footer-brand">DADI<span>↗</span></a>
<div><b>A familiar voice. An unexpected defence.</b><p>Inspired by O2’s Daisy. Built as a
scam-awareness
simulation.<br>No real callers. No real secrets. Always a human choice.</p></div>
<a href="#showcase-intro" class="sc-back">BACK TO TOP ↑</a></footer></div>"""

JS = r"""() => {
  const scenes = [
    ['Your bank account will be blocked. You must act now.',
     'Which branch, beta? Let me find my glasses first.', 'ASK THEM TO REPEAT'],
    ['Open the app. Tap the button on your screen.',
     'The blue one or the green one? My old phone only has buttons.', 'MAKE THEM EXPLAIN'],
    ['Please hurry. We cannot wait any longer.',
     'One minute, beta. My tea is boiling. Tell me your name again?', 'A BELIEVABLE DETOUR']
  ];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const fine = window.matchMedia('(pointer: fine)');
  let revealObserver;
  const init = () => {
    const roots = document.querySelectorAll('[data-showcase-root]');
    roots.forEach(root => {
      if (root.dataset.scBound) return;
      root.dataset.scBound = 'true';
      root.addEventListener('click', event => {
        const button = event.target.closest('[data-sc-scene]');
        if (!button || !root.contains(button)) return;
        const index = Number(button.dataset.scScene);
        const scene = root.querySelector('.sc-scene');
        if (!scene || !scenes[index]) return;
        root.querySelectorAll('[data-sc-scene]').forEach(b =>
          b.setAttribute('aria-pressed', String(b === button)));
        scene.querySelector('[data-sc-caller]').textContent = '“' + scenes[index][0] + '”';
        scene.querySelector('[data-sc-reply]').textContent = '“' + scenes[index][1] + '”';
        scene.querySelector('[data-sc-tactic]').textContent = 'TACTIC / ' + scenes[index][2];
        scene.querySelector('[data-sc-count]').textContent = '0' + (index + 1) + ' / 03';
        if (!reduced.matches && scene.animate) scene.animate(
          [{opacity: .4, transform: 'translateY(8px)'}, {opacity: 1, transform: 'translateY(0)'}],
          {duration: 280, easing: 'ease-out'});
      });
      if (!reduced.matches && 'IntersectionObserver' in window) {
        root.classList.add('sc-ready');
        if (!revealObserver) revealObserver = new IntersectionObserver(entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('sc-seen');
              revealObserver.unobserve(entry.target);
            }
          });
        }, {threshold: .08});
        root.querySelectorAll('[data-reveal]').forEach(el => revealObserver.observe(el));
      }
      const art = root.querySelector('[data-sc-tilt]');
      if (art && fine.matches && !reduced.matches) {
        art.addEventListener('pointermove', event => {
          const box = art.getBoundingClientRect();
          art.style.setProperty('--sc-x',
            ((event.clientX - box.left) / box.width - .5) * 7 + 'deg');
          art.style.setProperty('--sc-y',
            -((event.clientY - box.top) / box.height - .5) * 7 + 'deg');
        }, {passive:true});
        art.addEventListener('pointerleave', () => {
          art.style.setProperty('--sc-x', '0deg'); art.style.setProperty('--sc-y', '0deg');
        });
      }
    });
    return roots.length >= 2;
  };
  if (!init()) {
    const observer = new MutationObserver(() => { if (init()) observer.disconnect(); });
    observer.observe(document.body, {childList: true, subtree: true});
  }
  reduced.addEventListener('change', () => {
    if (reduced.matches) document.querySelectorAll('[data-showcase-root]').forEach(root =>
      root.classList.remove('sc-ready'));
  });
}"""

CSS = """
/* Scoped presentation: never hide or rewrite the call lab's controls. */
html {scroll-behavior:smooth;scroll-padding-top:28px}
.gradio-container {max-width:1440px!important;padding-top:0!important}
#app-nav {padding:0!important;border:0!important}
.sc-nav,.sc-root {font-family:Arial,Helvetica,sans-serif;color:#17182f}
.sc-nav {display:flex;align-items:center;justify-content:space-between;gap:24px;padding:27px 0;
 border-bottom:1px solid #17182f22}
.sc-nav a,.sc-root a {text-decoration:none!important;color:inherit}
.sc-brand
{display:flex;align-items:center;gap:10px;font-size:32px;font-weight:900;letter-spacing:-2px;
 line-height:1}.sc-brand svg {width:49px;height:49px}.sc-brand-sub {display:block;font-size:8px;
 font-weight:700;letter-spacing:1.6px;margin-top:6px}
.sc-nav-links {display:flex;align-items:center;gap:35px;font-size:13px;font-weight:700}
.sc-nav-links a {padding:10px 0}.sc-nav-links .sc-nav-cta {padding:13px 19px;border:1px solid
#17182f;
 border-radius:100px}.sc-nav-cta span {margin-left:15px}
#simulation-banner {margin:0!important;padding:12px 0!important;background:transparent!important;
 border:0!important;border-radius:0!important;box-shadow:none!important;min-height:0!important}
#simulation-banner h1
{font-family:Arial,sans-serif!important;font-size:11px!important;line-height:1.4!important;
 letter-spacing:1.4px;text-transform:uppercase;margin:0 0 3px!important;color:#535466!important}
#simulation-banner p
{font-size:11px!important;margin:0!important;line-height:1.5!important;color:#535466!important}
#showcase-intro,#workspace-footer
{border:0!important;padding:0!important;background:transparent!important}
.sc-root * {box-sizing:border-box}.sc-root p {font-size:16px;line-height:1.75;margin:0}
.sc-root h1,.sc-root h2,.sc-root h3
{color:inherit;font-family:Arial,Helvetica,sans-serif;letter-spacing:-.06em;
 font-weight:750;line-height:1.04;margin:0}
.sc-root h2 {font-size:clamp(36px,5.1vw,72px)}
.sc-root em,.sc-italic {font-family:Georgia,serif;font-weight:400;font-style:italic}
.sc-hero {display:grid;grid-template-columns:1.05fr 1fr;gap:18px;align-items:center;padding:38px 0
64px;
 min-height:710px}.sc-hero-copy {position:relative;z-index:2}
.sc-kicker,.sc-label {font:700 10px/1.6 Arial,sans-serif;letter-spacing:1.65px;display:block}
.sc-kicker {display:flex;align-items:center;gap:10px;margin-bottom:26px;max-width:470px}
.sc-dot {display:inline-block;width:7px;height:7px;border-radius:50%;background:#ff7654;flex:none}
.sc-root h1 {font-size:clamp(64px,7.9vw,112px);line-height:.94;letter-spacing:-.07em}
.sc-outline {-webkit-text-stroke:1.5px #17182f;color:transparent}
.sc-hero-copy>p {max-width:385px;margin-top:28px;color:#56576a;font-size:16px;line-height:1.65}
.sc-hero-actions {display:flex;align-items:center;flex-wrap:wrap;gap:19px;margin-top:29px}
.sc-primary
{display:inline-flex;align-items:center;justify-content:space-between;gap:20px;background:#17182f;
 color:#fff!important;border:1px solid #17182f;border-radius:100px;padding:17px 21px;font-size:12px;
 font-weight:700;transition:transform .2s,background .2s}.sc-primary:hover
{background:#34364e;transform:translateY(-3px)}
.sc-primary span {font-size:20px;line-height:12px}.sc-text-link {font-size:12px;font-weight:700;
 padding:12px 0}.sc-small-note {margin-top:16px;font-size:10px;color:#727280;max-width:390px}
.sc-art {position:relative;isolation:isolate;aspect-ratio:.9;background:#ff7654;border-radius:49%
49% 14px 14px;
 margin:8px 2px 30px 20px;transform:perspective(1000px) rotateX(var(--sc-y,0deg))
rotateY(var(--sc-x,0deg));
 transition:transform .3s ease-out;min-width:0}
.sc-art:after {content:'';position:absolute;inset:0;border-radius:inherit;z-index:-1;opacity:.15;
 background-image:radial-gradient(#713a31 1px,transparent 1px);background-size:7px 7px}
.sc-dadi {position:absolute;width:100%;height:100%;bottom:0;left:0;filter:drop-shadow(0 14px 5px
#8f3e2212)}
.sc-orbit {position:absolute;border:1px solid
#17182f20;border-radius:50%;inset:13%;transform:rotate(-20deg) scale(1.4,.78);
 pointer-events:none}.sc-orbit-two {transform:rotate(30deg) scale(1.3,.84);inset:20%}
.sc-art-caption
{position:absolute;top:38px;left:0;width:100%;text-align:center;font-size:9px;letter-spacing:2px;
 font-weight:700;transform:rotate(-8deg)}
.sc-sticker {position:absolute;top:21%;right:12px;background:#e2f3b1;padding:18px 22px
20px;transform:rotate(9deg);
 box-shadow:3px 6px 0 #17182f10;border-radius:3px;animation:sc-float 7s ease-in-out infinite}
.sc-sticker>span {font-size:8px;letter-spacing:1px;font-weight:700}.sc-sticker strong
{display:block;
 font:italic 27px/1.1 Georgia,serif;letter-spacing:-1px;margin-top:9px}
.sc-sticker svg {position:absolute;width:28px;right:-12px;top:-15px}
.sc-caption-card
{position:absolute;bottom:-23px;left:-30px;right:27px;display:flex;align-items:center;gap:13px;
 padding:20px 21px;border-radius:14px;background:#fffdf7;box-shadow:0 12px 35px
#17182f12;border:1px solid #17182f0b}
.sc-caption-card b {display:block;font-size:13px;letter-spacing:-.2px}.sc-caption-card div>span
{font-size:11px;color:#6c6c7c}
.sc-caption-arrow {margin-left:auto;font-size:26px}
.sc-ribbon {display:flex;align-items:center;justify-content:space-between;gap:20px;padding:25px 4px;
 border-top:1px solid #17182f25;border-bottom:1px solid #17182f25;font-size:11px;font-weight:700;
 letter-spacing:1px}.sc-ribbon i {font-size:27px;font-style:normal;color:#f15f44}
.sc-story {margin-top:77px;background:#17182f;color:#faf7ef;border-radius:26px;padding:36px 44px
49px;
 overflow:hidden}.sc-section-top
{display:flex;justify-content:space-between;align-items:center;gap:20px;
 font-size:9px;letter-spacing:1.2px;font-weight:700;padding-bottom:34px}.sc-story .sc-label
{color:#d7ed9b}
.sc-story-grid {display:grid;grid-template-columns:1fr 1fr;gap:65px;align-items:start}
.sc-story h2 {font-size:clamp(40px,5vw,68px)}.sc-story h2 em {color:#d7ed9b}
.sc-story-grid>div>p {color:#b9bac8;font-size:13px;max-width:350px;margin-top:24px}
.sc-scene-buttons {display:flex;flex-direction:column;gap:2px;margin-top:28px}
.sc-scene-buttons button {font-family:Arial,sans-serif;background:transparent;color:#b9bac8;
 border:0;border-top:1px solid #ffffff22;padding:17px
0;text-align:left;display:flex;align-items:center;
 gap:16px;font-size:12px;cursor:pointer;min-height:49px;transition:padding .2s,color .2s}
.sc-scene-buttons button>span {font-size:9px;color:#9394ab}.sc-scene-buttons button>b
{margin-left:auto;font-size:20px}
.sc-scene-buttons button[aria-pressed=true] {color:#d7ed9b;padding-left:10px}
.sc-scene-buttons button:hover {color:#fff}.sc-scene {background:#24253e;border:1px solid #45465a;
 border-radius:20px;padding:24px;box-shadow:0 15px 60px #0002;align-self:center;min-width:0}
.sc-scene-top {display:flex;justify-content:space-between;gap:15px;color:#c8c9d6;font-size:9px;
 letter-spacing:.9px;padding-bottom:26px}.sc-scene-top>span:first-child
{display:flex;align-items:center;gap:8px}
.sc-caller>span,.sc-grandma>span
{font-size:8px;font-weight:700;letter-spacing:1.3px;display:block;margin-bottom:9px}
.sc-caller {padding:18px 19px;border-radius:12px 12px 12px 3px;background:#33354d;margin-right:30px}
.sc-root .sc-caller p {font-size:16px;line-height:1.5}.sc-grandma
{background:#d7ed9b;color:#17182f;padding:22px;
 border-radius:12px 12px 3px 12px;margin-left:20px}.sc-root .sc-grandma p {font:400 26px/1.25
Georgia,serif;
 letter-spacing:-.6px}.sc-wave
{height:40px;display:flex;justify-content:center;align-items:center;gap:3px}
.sc-wave i {display:block;width:2px;height:7px;background:#999bb6;border-radius:3px}
.sc-wave i:nth-child(3n) {height:17px}.sc-wave i:nth-child(2n) {height:24px}
.sc-scene-bottom {margin-top:26px;font-size:9px;letter-spacing:.5px;color:#d7ed9b}
.sc-scene-bottom small
{display:block;font-size:9px;color:#b5b7ca;letter-spacing:0;margin-top:9px;line-height:1.6}
.sc-engine {padding:95px 0 78px}.sc-engine .sc-section-top {border-bottom:1px solid
#17182f22;padding-bottom:20px;
 margin-bottom:40px}.sc-engine-heading
{display:flex;justify-content:space-between;align-items:end;gap:40px}
.sc-engine-heading p {max-width:310px;color:#656576;font-size:13px}
.sc-engine-grid
{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:37px;align-items:start}
.sc-engine-grid details {background:#eeeae1;border-radius:14px;padding:24px;min-height:220px}
.sc-engine-grid details:nth-child(2) {background:#e4eccd}.sc-engine-grid details:nth-child(3)
{background:#ffe1d5}
.sc-root summary {list-style:none;cursor:pointer}.sc-root summary::-webkit-details-marker
{display:none}
.sc-engine-grid summary {position:relative;min-height:150px}.sc-engine-no
{display:block;font-size:13px;
 margin-bottom:36px}.sc-engine-name
{display:block;font-size:35px;font-weight:600;letter-spacing:-1.5px}
.sc-engine-grid b {display:block;margin-top:11px;font-size:9px;letter-spacing:.8px}
.sc-expand {position:absolute;right:0;top:0;font-size:25px;font-weight:300}
.sc-engine-grid details[open] .sc-expand {transform:rotate(45deg)}
.sc-engine-grid p {border-top:1px solid
#17182f20;padding-top:16px;font-size:12px;margin-top:16px;color:#555363}
.sc-lab-heading {padding:42px 0 35px;border-top:1px solid #17182f22;scroll-margin-top:25px}
.sc-lab-heading h2 {margin:25px 0 18px;font-size:clamp(45px,5vw,72px);max-width:800px}
.sc-lab-heading h2>span {display:inline-block;float:right;color:#f15f44;font-size:88px}
.sc-lab-heading p {font-size:13px;color:#656576;max-width:520px}
#workspace-note {font-size:12px!important;background:#eeeae1!important;border-radius:12px;
 padding:15px 18px!important;margin:0 0 20px!important}
#call-hero {margin-top:0!important;box-shadow:none!important;border-radius:22px!important}
#phone-panel {box-shadow:none!important}#call-language {margin-top:10px}
#case-panel {margin-top:28px!important;margin-bottom:15px!important}
.sc-outro {padding-top:55px}.sc-impact {padding:52px 45px;background:#d7ed9b;border-radius:24px;
 position:relative;overflow:hidden}.sc-impact h2 {font-size:clamp(36px,4.4vw,63px);margin-top:25px;
 max-width:820px}.sc-impact p {max-width:580px;font-size:13px;margin:25px 0;color:#505b43}
.sc-impact-seal {position:absolute;right:45px;bottom:44px;border:1px solid
#17182f44;border-radius:50%;
width:116px;height:116px;display:flex;align-items:center;justify-content:center;flex-direction:column;
text-align:center;transform:rotate(13deg);font-size:18px;font-weight:800;line-height:1.1;letter-spacing:-.6px}
.sc-impact-seal span {font-size:8px;letter-spacing:1px;margin-top:8px}
.sc-faq {display:grid;grid-template-columns:.8fr 1.2fr;gap:60px;padding:82px 0}
.sc-faq h2 {margin-top:24px;font-size:48px}.sc-faq-list details {border-bottom:1px solid #17182f22}
.sc-faq-list summary {padding:22px
0;font-size:14px;font-weight:600;display:flex;justify-content:space-between;
 gap:20px;line-height:1.6}.sc-faq-list summary span {font-size:23px;font-weight:400;line-height:1}
.sc-faq-list details[open] summary span {transform:rotate(45deg)}
.sc-faq-list p {padding:0 28px 23px 0;font-size:12px;color:#656576}
.sc-footer {display:flex;align-items:center;justify-content:space-between;gap:30px;padding:35px 0
30px;
 border-top:1px solid #17182f22}.sc-footer-brand
{font-size:72px;font-weight:900;letter-spacing:-6px;
 line-height:1}.sc-footer-brand span {color:#f15f44;margin-left:12px;font-weight:400}
.sc-footer div {font-size:11px}.sc-footer div p {font-size:10px;color:#727280;margin-top:10px}
.sc-back {font-size:9px;font-weight:700;letter-spacing:1px;white-space:nowrap}
.sc-root a:focus-visible,.sc-root button:focus-visible,.sc-root summary:focus-visible,
.sc-nav a:focus-visible {outline:3px solid #f15f44;outline-offset:6px;border-radius:4px}
.sc-ready [data-reveal] {opacity:0;transform:translateY(25px);transition:opacity .65s
ease,transform .65s ease}
.sc-ready [data-reveal].sc-seen {opacity:1;transform:translateY(0)}
@keyframes sc-float {0%,100%{transform:rotate(9deg) translateY(0)}50%{transform:rotate(6deg)
translateY(-8px)}}
@media(max-width:1050px) {
 .sc-hero {min-height:590px}.sc-root h1 {font-size:clamp(62px,8.5vw,95px)}
 .sc-kicker {font-size:8px}.sc-hero-actions {gap:9px}.sc-primary {font-size:11px;padding:15px 17px}
 .sc-sticker {right:12px;padding:15px}.sc-sticker strong {font-size:22px}
 .sc-story {padding:30px}.sc-story-grid {gap:30px}.sc-impact-seal {display:none}
 .sc-nav-links {gap:22px}.sc-art {margin-left:10px}.sc-caption-card
{left:-10px;right:10px;padding:16px}
}
@media(max-width:680px) {
 .sc-nav {padding:18px 0}.sc-brand {font-size:25px}.sc-brand svg {width:40px;height:40px}
 .sc-brand-sub {font-size:6px;letter-spacing:1px}.sc-nav-links>a:not(.sc-nav-cta){display:none}
 .sc-nav-links .sc-nav-cta {font-size:10px;padding:11px 12px}.sc-nav-cta span {margin-left:5px}
 #simulation-banner {padding:10px 0!important}#simulation-banner h1 {font-size:8px!important}
 #simulation-banner p {font-size:9px!important}.sc-hero {grid-template-columns:1fr;padding:25px 0
48px;
 gap:45px;min-height:0}.sc-root h1 {font-size:clamp(62px,15vw,92px)}
 .sc-kicker {margin-bottom:19px;max-width:310px;line-height:1.7}.sc-hero-copy>p {font-size:14px;
 max-width:340px;margin-top:22px}.sc-hero-actions {gap:18px}.sc-small-note {font-size:9px}
 .sc-art {width:min(90%,440px);margin:0 auto 30px;aspect-ratio:1}.sc-dadi {height:109%;bottom:0}
 .sc-sticker {top:3%;right:-4px;padding:10px 13px}.sc-sticker strong {font-size:20px}
 .sc-art-caption {top:20px;font-size:7px}.sc-caption-card {left:-12px;right:-10px;padding:17px;
 bottom:-27px}.sc-caption-card b {font-size:12px}.sc-caption-card div>span {font-size:10px}
 .sc-ribbon {flex-wrap:wrap;justify-content:center;gap:10px 18px;font-size:8px;padding:17px 0}
 .sc-ribbon i {font-size:18px}.sc-ribbon i:nth-of-type(2) {display:none}
 .sc-story {padding:25px 21px 24px;margin-top:45px;border-radius:20px}
 .sc-section-top {font-size:7px;letter-spacing:.7px;gap:10px;padding-bottom:27px}
 .sc-label {font-size:8px;letter-spacing:1px}.sc-story-grid {grid-template-columns:1fr;gap:28px}
 .sc-story h2 {font-size:48px}.sc-story-grid>div>p {font-size:12px;margin-top:20px}
 .sc-scene-buttons {margin-top:20px}.sc-scene {padding:19px}.sc-grandma
{margin-left:12px;padding:19px}
 .sc-root .sc-grandma p {font-size:25px}.sc-root .sc-caller p {font-size:14px}.sc-caller
{margin-right:12px}
 .sc-engine {padding:55px 0 44px}.sc-engine-heading {display:block}.sc-root h2 {font-size:42px}
 .sc-engine-heading p {margin-top:23px;font-size:12px}.sc-engine-grid
{grid-template-columns:1fr;gap:10px;
 margin-top:25px}.sc-engine-grid details {min-height:0;padding:21px}
 .sc-engine-grid summary {min-height:0;display:grid;grid-template-columns:45px
1fr;align-items:center}
 .sc-engine-no {grid-row:span 2;margin:0;font-size:12px}.sc-engine-name {font-size:28px}
 .sc-engine-grid b {font-size:8px;margin-top:7px}.sc-expand {font-size:23px}
 .sc-engine-grid p {font-size:12px;padding-top:15px;margin-top:18px}
 .sc-lab-heading {padding:30px 0 24px}.sc-lab-heading h2 {font-size:44px;margin-top:19px}
 .sc-lab-heading h2>span {font-size:65px}.sc-lab-heading p {font-size:12px}
 .sc-outro {padding-top:32px}.sc-impact {padding:30px 23px;border-radius:20px}
 .sc-impact h2 {font-size:36px}.sc-impact p {font-size:12px}
 .sc-faq {grid-template-columns:1fr;gap:20px;padding:52px 0}.sc-faq h2
{font-size:43px;margin-top:18px}
 .sc-faq-list summary {font-size:12px;padding:20px 0}.sc-faq-list p {font-size:12px}
 .sc-footer {flex-wrap:wrap;gap:26px}.sc-footer-brand {font-size:62px}.sc-footer div {width:100%}
 .sc-back {margin-top:-8px}.sc-root p {overflow-wrap:break-word}
}
@media(prefers-reduced-motion:reduce) {
 html {scroll-behavior:auto}.sc-root *, .sc-root *:before,.sc-root *:after
{animation:none!important;
 transition:none!important;transform:none!important}.sc-ready [data-reveal] {opacity:1!important}
}

/* Gradio's prose styles assign ink to descendants; set contrast explicitly on dark surfaces. */
.sc-story .sc-story-grid,.sc-story .sc-story-grid>div,.sc-story h2,
.sc-story .sc-caller,.sc-story .sc-caller p,.sc-story .sc-caller>span {color:#faf7ef!important}
.sc-story .sc-section-top>span,.sc-story .sc-scene-top span {color:#c8c9d6!important}
.sc-story .sc-label,.sc-story h2 em,.sc-story .sc-scene-bottom>span {color:#d7ed9b!important}
.sc-story .sc-grandma,.sc-story .sc-grandma p,.sc-story .sc-grandma>span {color:#17182f!important}
.sc-story .sc-scene-buttons button b {color:inherit!important}
.sc-root .sc-primary>span {color:#fff!important}

.sc-story .sc-scene-buttons button[aria-pressed=true] {color:#d7ed9b!important;
 background:#ffffff08;border-left:2px solid #d7ed9b;padding-left:10px}
"""
