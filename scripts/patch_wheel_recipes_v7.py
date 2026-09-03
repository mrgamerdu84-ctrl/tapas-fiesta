from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# --- Wheel sound: make WebAudio explicitly resume on Android/WebView interaction. ---
play_tick_pat = re.compile(r'''  var tickCtx = null;\n  function playTick\(\)\{.*?\n  \}\n  function scheduleTicks\(totalMs\)\{''', re.S)
play_tick_repl = r'''  var tickCtx = null;
  function unlockWheelAudio(){
    try{
      tickCtx = tickCtx || new (window.AudioContext || window.webkitAudioContext)();
      if(tickCtx.state === "suspended"){
        var rp = tickCtx.resume();
        if(rp && rp.catch) rp.catch(function(){});
      }
    }catch(e){}
  }
  ["pointerdown","touchstart","mousedown","click"].forEach(function(ev){
    document.addEventListener(ev, unlockWheelAudio, {passive:true});
  });
  function playTick(strength){
    try{
      unlockWheelAudio();
      if(!tickCtx || tickCtx.state !== "running") return;
      var now = tickCtx.currentTime;
      var o = tickCtx.createOscillator();
      var g = tickCtx.createGain();
      o.type = "square";
      o.frequency.setValueAtTime(620 + Math.random()*170, now);
      o.frequency.exponentialRampToValueAtTime(350 + Math.random()*70, now + 0.045);
      var gain = 0.16 * (typeof strength === "number" ? strength : 1);
      g.gain.setValueAtTime(gain, now);
      g.gain.exponentialRampToValueAtTime(0.001, now + 0.055);
      o.connect(g); g.connect(tickCtx.destination);
      o.start(now); o.stop(now + 0.058);
    }catch(e){}
  }
  function scheduleTicks(totalMs){'''
s, n = play_tick_pat.subn(play_tick_repl, s, count=1)
if n != 1:
    raise SystemExit('ERROR: wheel tick audio block not found')

# Slightly richer slowing cadence while preserving the existing scheduler.
s = s.replace('''      playTick();\n      interval = Math.min(interval + 9, 230); // ratchet slows down like the wheel''',
              '''      var progress = Math.min(1, elapsed / Math.max(1,totalMs));\n      playTick(1 - progress * 0.35);\n      interval = Math.min(interval + 7 + Math.floor(progress*8), 245); // ratchet slows down like the wheel''', 1)

# CSS: pointer visibly rattles left/right like a physical ratchet while the wheel spins.
css = r'''
<style id="tf-wheel-gameplay-v7">
.wheel-holder .pointer.tf-ratchet{
  transform-origin:50% 4px;
  animation:tfPointerRatchet .105s ease-in-out infinite alternate;
}
@keyframes tfPointerRatchet{
  from{transform:translateX(-50%) rotate(-8deg)}
  to{transform:translateX(-50%) rotate(8deg)}
}
.wheel-holder.tf-wheel-pulse{animation:tfWheelPulse .6s ease-in-out infinite alternate;}
@keyframes tfWheelPulse{from{filter:drop-shadow(0 10px 12px rgba(70,39,20,.16))}to{filter:drop-shadow(0 14px 19px rgba(216,61,32,.27))}}
@media (prefers-reduced-motion:reduce){.wheel-holder .pointer.tf-ratchet,.wheel-holder.tf-wheel-pulse{animation:none!important}}
</style>
'''
if 'id="tf-wheel-gameplay-v7"' not in s:
    s = s.replace('</head>', css + '\n</head>', 1)

# Wheel engine: anti-repeat weighted selection + varied spin duration/turn count.
spin_pat = re.compile(r'''  function spinWheelEl\(svgEl, state, onDone, lightsEl\)\{.*?\n  \}\n\n  var wheelEl =''', re.S)
spin_repl = r'''  function pickWheelIndex(state){
    state.history = state.history || [];
    var weights = segments.map(function(seg, i){
      var w = seg.type === "mystere" ? 0.90 : 1.0;
      if(state.history[0] === i) w *= 0.08;
      if(state.history[1] === i) w *= 0.42;
      w *= 0.88 + Math.random() * 0.24;
      return w;
    });
    var total = weights.reduce(function(a,b){ return a+b; }, 0);
    var r = Math.random() * total;
    var idx = 0;
    for(var i=0;i<weights.length;i++){
      r -= weights[i];
      if(r <= 0){ idx = i; break; }
    }
    state.history.unshift(idx);
    if(state.history.length > 3) state.history.length = 3;
    return idx;
  }

  function spinWheelEl(svgEl, state, onDone, lightsEl){
    var idx = pickWheelIndex(state);
    var center = idx * 60 + 30;
    var jitter = (Math.random() * 22) - 11;
    var extraSpins = 4 + Math.floor(Math.random() * 5);
    var duration = 3350 + Math.floor(Math.random() * 1450);
    var desiredRotation = ((360 - center + jitter) % 360 + 360) % 360;
    var currentRotation = ((state.rotation % 360) + 360) % 360;
    var deltaRotation = extraSpins * 360 + ((desiredRotation - currentRotation + 360) % 360);
    var holder = svgEl && svgEl.closest ? svgEl.closest(".wheel-holder") : null;
    var pointer = holder ? holder.querySelector(".pointer") : null;

    unlockWheelAudio();
    state.rotation += deltaRotation;
    svgEl.style.transition = "transform " + duration + "ms cubic-bezier(0.12,0.76,0.25,1)";
    svgEl.style.transform = "rotate(" + state.rotation + "deg)";
    if(holder) holder.classList.add("tf-wheel-pulse");
    if(pointer) pointer.classList.add("tf-ratchet");
    if(lightsEl){ lightsEl.classList.remove("idle-glow"); lightsEl.classList.add("spinning"); }
    duckMusicFor(duration);

    setTimeout(function(){
      if(lightsEl){ lightsEl.classList.remove("spinning"); lightsEl.classList.add("idle-glow"); }
      if(holder) holder.classList.remove("tf-wheel-pulse");
      if(pointer) pointer.classList.remove("tf-ratchet");
      onDone(idx);
    }, duration + 80);
  }

  var wheelEl ='''
s, n = spin_pat.subn(spin_repl, s, count=1)
if n != 1:
    raise SystemExit('ERROR: spinWheelEl function not found')

# --- Add new recipes without changing ingredient keys or crafting rules. ---
recipes_pat = re.compile(r'''  var RECIPES_ALL = \[.*?\n  \];''', re.S)
recipes_repl = r'''  var RECIPES_ALL = [
    { name:"Tacos Al Pastor",       need:{viande:1, tortilla:1, piment:1},            level:"Facile" },
    { name:"Quesadilla Supremo",    need:{fromage:1, tortilla:1, viande:1},           level:"Facile" },
    { name:"Salsa Verde Deluxe",    need:{piment:1, avocat:1, tortilla:1},            level:"Facile" },
    { name:"Tostada Fiesta",        need:{tortilla:1, viande:1, avocat:1},            level:"Facile" },
    { name:"Tacos Guacamole",       need:{tortilla:1, avocat:1, fromage:1},           level:"Facile" },
    { name:"Fajitas Fiesta",        need:{viande:1, piment:1, avocat:1},              level:"Facile" },
    { name:"Guacamole Royal",       need:{avocat:1, piment:1, epice:1},               level:"Moyen"  },
    { name:"Molletes Picantes",     need:{viande:1, fromage:1, piment:1},             level:"Moyen"  },
    { name:"Queso Fundido",         need:{fromage:1, piment:1, epice:1},              level:"Moyen"  },
    { name:"Quesadilla Mystère",    need:{tortilla:1, fromage:1, epice:1},            level:"Moyen"  },
    { name:"Taco del Chef",         need:{tortilla:1, viande:1, epice:1},             level:"Moyen"  },
    { name:"Burrito Gigante",       need:{viande:2, fromage:1, tortilla:1},           level:"Corsé"  },
    { name:"Nachos Locos",          need:{tortilla:1, fromage:1, piment:1, epice:1},  level:"Corsé"  },
    { name:"Chimichanga Loca",      need:{viande:1, fromage:1, piment:1, tortilla:1}, level:"Corsé"  },
    { name:"Nachos Supremo",        need:{tortilla:2, fromage:1, piment:1},           level:"Corsé"  },
    { name:"Fiesta del Fuego",      need:{viande:1, avocat:1, piment:1, epice:1},     level:"Corsé"  }
  ];'''
s, n = recipes_pat.subn(recipes_repl, s, count=1)
if n != 1:
    raise SystemExit('ERROR: RECIPES_ALL block not found')

# Rules page: update count and append the six new digital recipes to the existing table.
s = s.replace('10 cartes Recettes Tapas', '16 cartes Recettes Tapas')
s = s.replace('Les 10 Recettes Tapas', 'Les 16 Recettes Tapas')
anchor = '<tr><td>Chimichanga Loca</td><td>Viande, Fromage, Piment, Tortilla</td><td>Corsé</td></tr>'
extra_rows = anchor + '''\n          <tr><td>Tacos Guacamole</td><td>Tortilla, Avocat, Fromage</td><td>Facile</td></tr>\n          <tr><td>Fajitas Fiesta</td><td>Viande, Piment, Avocat</td><td>Facile</td></tr>\n          <tr><td>Quesadilla Mystère</td><td>Tortilla, Fromage, Épice Mystère</td><td>Moyen</td></tr>\n          <tr><td>Taco del Chef</td><td>Tortilla, Viande, Épice Mystère</td><td>Moyen</td></tr>\n          <tr><td>Nachos Supremo</td><td>2 Tortillas, Fromage, Piment</td><td>Corsé</td></tr>\n          <tr><td>Fiesta del Fuego</td><td>Viande, Avocat, Piment, Épice Mystère</td><td>Corsé</td></tr>'''
if 'Tacos Guacamole</td>' not in s:
    if anchor not in s:
        raise SystemExit('ERROR: rules recipe table anchor not found')
    s = s.replace(anchor, extra_rows, 1)

# Do not touch core gain/mystery/AI flow. Guard it here too.
for required in (
    'player.hand[seg.key]++;',
    'if(seg.key === "epice")',
    'setTimeout(runAiTurn, 800)',
    'function handleSpinResult(idx)',
):
    if required not in s:
        raise SystemExit('ERROR: stable gameplay core missing after V7 patch: ' + required)

p.write_text(s, encoding='utf-8')
print('Tapas Fiesta V7 wheel + recipes applied without changing stable ingredient/AI core')
