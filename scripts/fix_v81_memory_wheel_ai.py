from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# 1) Memory cards: avoid WebView 3D/backface glitches. Toggle faces explicitly.
css = r'''
<style id="tf-v81-fixes">
.tf-memory-card{
  transform:none!important;
  transform-style:flat!important;
  -webkit-transform-style:flat!important;
  perspective:none!important;
}
.tf-memory-card .tf-card-back,
.tf-memory-card .tf-card-front{
  position:absolute!important;
  inset:0!important;
  transform:none!important;
  -webkit-transform:none!important;
  backface-visibility:visible!important;
  -webkit-backface-visibility:visible!important;
  align-items:center!important;
  justify-content:center!important;
}
.tf-memory-card .tf-card-back{display:flex!important;z-index:2!important;color:#ffeab0!important;}
.tf-memory-card .tf-card-front{
  display:none!important;z-index:3!important;background:#fff7e6!important;
  font-size:2.25rem!important;line-height:1!important;
}
.tf-memory-card.open .tf-card-back,
.tf-memory-card.matched .tf-card-back{display:none!important;}
.tf-memory-card.open .tf-card-front,
.tf-memory-card.matched .tf-card-front{display:flex!important;animation:tfV81Reveal .18s ease-out both;}
.tf-memory-card.matched .tf-card-front{background:#eff8e8!important;}
@keyframes tfV81Reveal{from{opacity:.15;transform:scale(.72)}to{opacity:1;transform:scale(1)}}

/* Wheel labels: keep names away from the crowded center. */
.wheel-holder svg text{pointer-events:none;paint-order:stroke fill;stroke:rgba(55,35,20,.16);stroke-width:.22px;}

/* AI turn: make the wheel visually obvious while it spins. */
#aiThinking.tf-ai-visible{display:block!important;font-weight:900!important;color:#9e2c1f!important;}
#wheelStickyBox.tf-ai-spinning{box-shadow:0 0 0 4px rgba(227,167,45,.25),0 14px 28px rgba(80,45,25,.16)!important;}
@media(max-width:480px){
  .tf-memory-card .tf-card-front{font-size:2rem!important;}
}
</style>
'''
if 'id="tf-v81-fixes"' not in s:
    s = s.replace('</head>', css + '\n</head>', 1)

# 2) Move wheel labels outward and shorten the two longest labels.
old_label = '''      var lp=pointAt(mid,R*.43),t=document.createElementNS(svgNS,"text");t.setAttribute("x",lp.x.toFixed(2));t.setAttribute("y",lp.y.toFixed(2));t.setAttribute("fill",wheelLabelColors[i%wheelLabelColors.length]);t.setAttribute("text-anchor","middle");t.setAttribute("dominant-baseline","middle");t.style.fontSize="4.4px";t.style.fontWeight="800";t.setAttribute("transform","rotate("+textRot+" "+lp.x.toFixed(2)+" "+lp.y.toFixed(2)+")");
      t.textContent=seg.name.split(" / ")[0].replace("Panier Surprise","Panier").replace("Mémoire Mexico","Mémoire").replace("Échange Fiesta","Échange").replace("Pièce Mexico","Pièce");svgEl.appendChild(t);'''
new_label = '''      var lp=pointAt(mid,R*.56),t=document.createElementNS(svgNS,"text");t.setAttribute("x",lp.x.toFixed(2));t.setAttribute("y",lp.y.toFixed(2));t.setAttribute("fill",wheelLabelColors[i%wheelLabelColors.length]);t.setAttribute("text-anchor","middle");t.setAttribute("dominant-baseline","middle");t.style.fontSize="3.35px";t.style.fontWeight="900";t.setAttribute("transform","rotate("+textRot+" "+lp.x.toFixed(2)+" "+lp.y.toFixed(2)+")");
      var tfShortLabels={avocat:"Avocat",piment:"Piment",tortilla:"Tortilla",fromage:"Fromage",viande:"Viande",epice:"Mystère",coin:"Pièce",memory:"Mémoire",bonus:"Panier",exchange:"Échange"};
      t.textContent=tfShortLabels[seg.key]||seg.name.split(" / ")[0];svgEl.appendChild(t);'''
if 'var tfShortLabels=' not in s:
    if old_label not in s:
        raise SystemExit('ERROR V8.1: wheel label block not found')
    s = s.replace(old_label, new_label, 1)

# 3) AI wheel turn: expand the wheel, scroll it into view, show a clear status, then spin.
old_ai = '''  function runAiTurn(){
    var gw = document.getElementById("gameWheel");
    spinWheelEl(gw, gameWheelState, function(idx){
      handleSpinResult(idx);
    }, document.getElementById("gameWheelLights"));
  }'''
new_ai = '''  function runAiTurn(){
    var gw = document.getElementById("gameWheel");
    var wheelBox = document.getElementById("wheelStickyBox");
    var thinking = document.getElementById("aiThinking");
    var aiPlayer = game && game.players ? game.players[game.turn] : null;
    if(wheelBox){ wheelBox.classList.remove("collapsed"); wheelBox.classList.add("tf-ai-spinning"); }
    if(thinking){ thinking.classList.add("tf-ai-visible"); thinking.textContent = "🤖 " + (aiPlayer ? aiPlayer.name : "L’IA") + " tourne la roue…"; }
    if(gw && gw.scrollIntoView){ try{ gw.scrollIntoView({behavior:"smooth",block:"center"}); }catch(e){ gw.scrollIntoView(); } }
    showToast("🤖 " + (aiPlayer ? aiPlayer.name : "L’IA") + " tourne la roue…", 2200);
    tfSpeak((aiPlayer ? aiPlayer.name : "L'intelligence artificielle") + " tourne la roue");
    setTimeout(function(){
      spinWheelEl(gw, gameWheelState, function(idx){
        if(wheelBox) wheelBox.classList.remove("tf-ai-spinning");
        if(thinking){ thinking.classList.remove("tf-ai-visible"); thinking.textContent = ""; }
        handleSpinResult(idx);
      }, document.getElementById("gameWheelLights"));
    }, 650);
  }'''
if 'wheelBox.classList.add("tf-ai-spinning")' not in s:
    if old_ai not in s:
        raise SystemExit('ERROR V8.1: runAiTurn block not found')
    s = s.replace(old_ai, new_ai, 1)

# Guards: keep the working V8/stable gameplay pieces untouched.
required = (
    'function tfRunMemory(',
    'Maximum 7 essais',
    'function tfRunWheelCoin(',
    'if(seg.type==="ingredient"||seg.type==="mystere")',
    'function runAiTurn()',
    'var tfShortLabels=',
    'tf-memory-card.open .tf-card-front',
)
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit('ERROR V8.1 validation failed: ' + ', '.join(missing))

p.write_text(s, encoding='utf-8')
print('V8.1 fixed: memory card faces + wheel labels + visible AI spin')
