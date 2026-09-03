from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# Idempotent: remove an earlier V6 layer if the workflow is rerun on an already-built page.
s = re.sub(r'\n?<style id="tf-gameplay-v6">.*?</style>\n?', '\n', s, flags=re.S)

css = r'''
<style id="tf-gameplay-v6">
/* V6 only enhances play feedback; approved Mexican reference screens keep their layout. */
#view-jouer #boardScreen{position:relative;}
#view-jouer .score-row{position:relative;overflow:hidden;padding:12px 13px!important;}
#view-jouer .score-side{padding:7px 9px;border-radius:14px;transition:background .2s ease,transform .2s ease,box-shadow .2s ease;}
#view-jouer .score-row[data-turn="0"] .score-side:first-child,
#view-jouer .score-row[data-turn="1"] .score-side.right{
  background:linear-gradient(145deg,rgba(0,110,101,.13),rgba(255,248,226,.85));
  box-shadow:inset 0 0 0 1px rgba(0,110,101,.22),0 4px 10px rgba(62,43,25,.08);
  transform:translateY(-1px);
}
#view-jouer .score-side .pscore{display:inline-block!important;margin-top:3px;padding:2px 7px;border-radius:999px;background:#F4E3BB;color:#76533D!important;font-weight:800!important;}
#view-jouer .turn-banner{position:relative;padding:12px 14px 13px!important;margin-bottom:14px!important;overflow:hidden;}
#view-jouer .turn-banner::after{content:attr(data-hint);display:block;margin-top:5px;color:#6D5848;font:700 .76rem/1.35 "Trebuchet MS",system-ui,sans-serif;letter-spacing:0;text-transform:none;}
#view-jouer .turn-banner[data-phase="spin"]{border-left:5px solid #08786D!important;background:linear-gradient(90deg,#EAF5EC,#FFF1C9)!important;color:#075F57!important;}
#view-jouer .turn-banner[data-phase="cook"]{border-left:5px solid #D84A26!important;background:linear-gradient(90deg,#FFF0D4,#FFF8E9)!important;color:#8A3326!important;}
#view-jouer .turn-banner[data-phase="finish"]{border-left:5px solid #6F8E31!important;background:linear-gradient(90deg,#EEF4DB,#FFF8E9)!important;color:#536B27!important;}

#view-jouer .hand-chip{animation:tfChipIn .24s ease both;}
#view-jouer .hand-chip:nth-child(2){animation-delay:.025s}#view-jouer .hand-chip:nth-child(3){animation-delay:.05s}#view-jouer .hand-chip:nth-child(4){animation-delay:.075s}#view-jouer .hand-chip:nth-child(5){animation-delay:.10s}#view-jouer .hand-chip:nth-child(6){animation-delay:.125s}
@keyframes tfChipIn{from{opacity:.2;transform:translateY(5px) scale(.96)}to{opacity:1;transform:none}}

#view-jouer .recipe-card{position:relative;overflow:hidden;transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;}
#view-jouer .recipe-card.ready{border:2px solid #6F8E31!important;box-shadow:0 9px 20px rgba(74,102,38,.14),inset 0 0 0 1px rgba(255,255,255,.75)!important;}
#view-jouer .recipe-card.ready::before{content:"PRÊTE À CUISINER";display:block;width:max-content;margin:-12px -14px 10px;padding:5px 12px 5px 14px;border-radius:0 0 12px 0;background:linear-gradient(90deg,#5F842B,#7E9C38);color:#fff;font-size:.64rem;font-weight:950;letter-spacing:.07em;}
#view-jouer .recipe-card.ready .cook-btn:not(:disabled){animation:tfCookReady 1.6s ease-in-out infinite;}
@keyframes tfCookReady{0%,100%{box-shadow:0 5px 0 #7F2D27,0 9px 18px rgba(113,47,34,.20)}50%{box-shadow:0 5px 0 #7F2D27,0 9px 24px rgba(216,74,38,.38)}}

#view-jouer #endTurnBtn:not(:disabled){animation:tfEndReady 1.8s ease-in-out infinite;}
@keyframes tfEndReady{0%,100%{filter:none}50%{filter:drop-shadow(0 0 7px rgba(111,142,49,.38))}}
#view-jouer #gameSpinBtn.tf-busy,#spinBtn.tf-busy{opacity:.82;cursor:wait;}
.wheel-holder.tf-spinning{animation:tfWheelStage .7s ease-in-out infinite alternate;}
@keyframes tfWheelStage{from{filter:drop-shadow(0 14px 18px rgba(64,35,22,.19))}to{filter:drop-shadow(0 17px 25px rgba(216,74,38,.28))}}
.result-box.tf-result-in{animation:tfResultPop .35s cubic-bezier(.2,1.2,.4,1) both;}
@keyframes tfResultPop{from{opacity:.2;transform:translateY(8px) scale(.96)}to{opacity:1;transform:none}}

/* Dynamic challenge animation without changing the approved static design. */
#view-defi .piment-draw{transform-style:preserve-3d;transform-origin:center;will-change:transform,opacity;}
#view-defi .piment-draw.tf-dealing{animation:tfDealOut .22s ease both;}
#view-defi .piment-draw.tf-revealed{animation:tfDealIn .38s cubic-bezier(.2,1.15,.4,1) both;}
@keyframes tfDealOut{to{opacity:.12;transform:translateY(8px) rotateY(72deg) scale(.94)}}
@keyframes tfDealIn{from{opacity:.15;transform:translateY(-7px) rotateY(-72deg) scale(.94)}to{opacity:1;transform:none}}
#view-defi .draw-btn.tf-busy{opacity:.75;pointer-events:none;}

/* Timer feedback. */
#view-minuteur .timer-num{transition:transform .16s ease,color .16s ease;}
#view-minuteur .timer-ring.tf-tick .timer-num{animation:tfTimerTick .3s ease;}
#view-minuteur .timer-ring.tf-low{box-shadow:0 0 0 11px #D9512C,0 0 0 14px #E6B64D,0 0 30px rgba(216,61,32,.25),0 13px 28px rgba(92,45,24,.19)!important;}
#view-minuteur .timer-ring.tf-done{animation:tfTimerDone .55s cubic-bezier(.2,1.25,.4,1);}
#view-minuteur .timer-ring.tf-done .timer-num{color:#08756B!important;}
@keyframes tfTimerTick{50%{transform:scale(1.12)}}
@keyframes tfTimerDone{0%{transform:scale(.96)}55%{transform:scale(1.06)}100%{transform:none}}

/* Lightweight celebration layer used for recipes and victory. */
.tf-v6-celebration{position:fixed;inset:0;z-index:2147482500;display:flex;align-items:center;justify-content:center;pointer-events:none;background:rgba(36,23,16,.12);animation:tfCelebFade 1.25s ease both;}
.tf-v6-celebration-card{position:relative;min-width:min(84vw,330px);max-width:88vw;padding:22px 20px;text-align:center;border-radius:26px;background:linear-gradient(155deg,#FFFDF7,#FFF0CC);border:2px solid #E3A72D;box-shadow:0 20px 50px rgba(55,31,19,.28);animation:tfCelebPop .5s cubic-bezier(.2,1.3,.4,1) both;}
.tf-v6-celebration-card .big{display:block;font-size:3rem;line-height:1;margin-bottom:7px;filter:drop-shadow(0 5px 5px rgba(80,43,23,.15));}
.tf-v6-celebration-card strong{display:block;color:#8F3023;font-family:Georgia,"Times New Roman",serif;font-size:1.16rem;}
.tf-v6-particle{position:fixed;left:50%;top:48%;font-size:1.1rem;animation:tfParticle .85s ease-out both;}
@keyframes tfCelebPop{from{opacity:.2;transform:scale(.78) translateY(10px)}to{opacity:1;transform:none}}
@keyframes tfCelebFade{0%,72%{opacity:1}100%{opacity:0}}
@keyframes tfParticle{from{opacity:1;transform:translate(-50%,-50%) rotate(0deg) translateY(0) scale(.7)}to{opacity:0;transform:translate(calc(-50% + var(--dx)),calc(-50% + var(--dy))) rotate(var(--rot)) scale(1.15)}}

@media (prefers-reduced-motion:reduce){
  #view-jouer .hand-chip,#view-jouer .recipe-card.ready .cook-btn:not(:disabled),#view-jouer #endTurnBtn:not(:disabled),.wheel-holder.tf-spinning,#view-defi .piment-draw.tf-dealing,#view-defi .piment-draw.tf-revealed,#view-minuteur .timer-ring.tf-tick .timer-num,#view-minuteur .timer-ring.tf-done,.tf-v6-celebration,.tf-v6-celebration-card,.tf-v6-particle{animation:none!important;}
}
</style>
'''
s = s.replace('</head>', css + '\n</head>', 1)

needle = '''  function playerIndex(player){ return game.players.indexOf(player); }'''
helper = r'''  function tfCelebrate(icon, text, kind){
    var old = document.querySelector('.tf-v6-celebration');
    if(old) old.remove();
    var layer = document.createElement('div');
    layer.className = 'tf-v6-celebration';
    layer.innerHTML = '<div class="tf-v6-celebration-card"><span class="big">' + icon + '</span><strong>' + text + '</strong></div>';
    document.body.appendChild(layer);
    var bits = ['✦','●','◆','✿','🌶️','✨'];
    for(var i=0;i<14;i++){
      var b=document.createElement('span'); b.className='tf-v6-particle'; b.textContent=bits[i%bits.length];
      var a=(Math.PI*2*i/14)+(Math.random()*.25); var d=65+Math.random()*95;
      b.style.setProperty('--dx',(Math.cos(a)*d).toFixed(0)+'px');
      b.style.setProperty('--dy',(Math.sin(a)*d-25).toFixed(0)+'px');
      b.style.setProperty('--rot',((Math.random()*240)-120).toFixed(0)+'deg');
      layer.appendChild(b);
    }
    setTimeout(function(){ if(layer && layer.parentNode) layer.parentNode.removeChild(layer); },1300);
  }

  function tfPopResult(el){
    if(!el) return; el.classList.remove('tf-result-in'); void el.offsetWidth; el.classList.add('tf-result-in');
  }

  function playerIndex(player){ return game.players.indexOf(player); }'''
if 'function tfCelebrate(' not in s:
    if needle not in s:
        raise SystemExit('ERROR: playerIndex insertion point not found')
    s = s.replace(needle, helper, 1)

score_needle = '''    document.getElementById("scoreRow").innerHTML =
      '<span class="score-side"><span class="pav">' + (p0.avatar || "🧑") + '</span><span><span class="pname">' + p0.name + '</span><span class="pscore">' + p0.validated.length + '/3 recettes</span></span></span>' +
      '<span class="vs">VS</span>' +
      '<span class="score-side right"><span class="pav">' + (p1.avatar || "🤖") + '</span><span><span class="pname">' + p1.name + '</span><span class="pscore">' + p1.validated.length + '/3 recettes</span></span></span>';'''
score_repl = score_needle + '''
    document.getElementById("scoreRow").dataset.turn = String(game.turn);'''
if 'scoreRow").dataset.turn' not in s:
    if score_needle not in s:
        raise SystemExit('ERROR: score row block not found')
    s = s.replace(score_needle, score_repl, 1)

turn_old = '''    document.getElementById("turnBanner").textContent =
      (current.avatar ? current.avatar + " " : "") + "Au tour de " + current.name + (current.isAI ? " 🤖" : "");'''
turn_new = '''    var turnBannerEl = document.getElementById("turnBanner");
    turnBannerEl.textContent = (current.avatar ? current.avatar + " " : "") + "Au tour de " + current.name + (current.isAI ? " 🤖" : "");
    if(current.skipCook){
      turnBannerEl.dataset.phase = "finish";
      turnBannerEl.dataset.hint = "Coup de Piment : termine ton tour.";
    } else if(game.hasSpun){
      turnBannerEl.dataset.phase = "cook";
      turnBannerEl.dataset.hint = "Cuisine une recette si elle est prête, puis termine ton tour.";
    } else {
      turnBannerEl.dataset.phase = "spin";
      turnBannerEl.dataset.hint = "Tourne la roue pour gagner un ingrédient.";
    }'''
if 'turnBannerEl.dataset.phase' not in s:
    if turn_old not in s:
        raise SystemExit('ERROR: turn banner block not found')
    s = s.replace(turn_old, turn_new, 1)

cook_old = '''    showToast((playerIdx === game.turn ? "🎉 Recette validée : " : "🎉 ") + recipe.name + " !");
    if(player.validated.length >= 3){
      game.status = "ended";
      game.winnerIdx = playerIdx;
    }'''
cook_new = '''    showToast((playerIdx === game.turn ? "🎉 Recette validée : " : "🎉 ") + recipe.name + " !");
    if(player.validated.length >= 3){
      game.status = "ended";
      game.winnerIdx = playerIdx;
      tfCelebrate("🏆", player.name + " remporte la Tapas Fiesta !", "victory");
    } else {
      tfCelebrate("🌮", "Recette validée : " + recipe.name, "recipe");
    }'''
if 'tfCelebrate("🌮"' not in s:
    if cook_old not in s:
        raise SystemExit('ERROR: cook celebration block not found')
    s = s.replace(cook_old, cook_new, 1)

draw_old = '''  drawBtn.addEventListener("click", function(){
    var group = piment[Math.floor(Math.random()*piment.length)];
    var text = group.texts[Math.floor(Math.random()*group.texts.length)];
    pimentCard.style.opacity = 0;
    setTimeout(function(){
      catTag.textContent = group.cat;
      catTag.style.background = group.color;
      catText.textContent = text;
      pimentCard.style.transition = "opacity 0.25s ease";
      pimentCard.style.opacity = 1;
    }, 150);
  });'''
draw_new = '''  drawBtn.addEventListener("click", function(){
    if(drawBtn.classList.contains("tf-busy")) return;
    drawBtn.classList.add("tf-busy");
    drawBtn.disabled = true;
    drawBtn.textContent = "🌶️ Mélange des cartes…";
    var group = piment[Math.floor(Math.random()*piment.length)];
    var text = group.texts[Math.floor(Math.random()*group.texts.length)];
    pimentCard.classList.remove("tf-revealed");
    pimentCard.classList.add("tf-dealing");
    setTimeout(function(){
      catTag.textContent = group.cat;
      catTag.style.background = group.color;
      catText.textContent = text;
      pimentCard.classList.remove("tf-dealing");
      pimentCard.classList.add("tf-revealed");
      drawBtn.textContent = "🌶️ Piocher une autre carte";
      drawBtn.disabled = false;
      drawBtn.classList.remove("tf-busy");
    }, 260);
  });'''
if 'Mélange des cartes' not in s:
    if draw_old not in s:
        raise SystemExit('ERROR: piment draw listener not found')
    s = s.replace(draw_old, draw_new, 1)

timer_old = '''  function renderTimer(){
    timerNum.textContent = remaining;
    var offset = circumference * (1 - remaining / duration);
    ringFg.style.strokeDashoffset = offset;
  }'''
timer_new = '''  function renderTimer(){
    timerNum.textContent = remaining;
    var offset = circumference * (1 - remaining / duration);
    ringFg.style.strokeDashoffset = offset;
    var timerRingEl = document.querySelector("#view-minuteur .timer-ring");
    if(timerRingEl){
      timerRingEl.classList.toggle("tf-low", remaining > 0 && remaining <= 3);
      timerRingEl.classList.toggle("tf-done", remaining === 0);
      timerRingEl.classList.remove("tf-tick"); void timerRingEl.offsetWidth;
      if(remaining > 0 && remaining < duration) timerRingEl.classList.add("tf-tick");
    }
  }'''
if 'timerRingEl.classList.toggle("tf-low"' not in s:
    if timer_old not in s:
        raise SystemExit('ERROR: timer render function not found')
    s = s.replace(timer_old, timer_new, 1)

start_old = '''    startBtn.disabled = true;
    remaining = duration;'''
start_new = '''    startBtn.disabled = true;
    startBtn.textContent = "⏳ En cours…";
    remaining = duration;'''
if 'startBtn.textContent = "⏳ En cours…"' not in s:
    s = s.replace(start_old, start_new, 1)

finish_old = '''        startBtn.disabled = false;
        beep();
        return;'''
finish_new = '''        startBtn.disabled = false;
        startBtn.textContent = "▶ Relancer";
        beep();
        return;'''
if 'startBtn.textContent = "▶ Relancer"' not in s:
    if finish_old not in s: raise SystemExit('ERROR: timer finish block not found')
    s = s.replace(finish_old, finish_new, 1)

reset_old = '''    startBtn.disabled = false;
    remaining = duration;
    renderTimer();
  });'''
reset_new = '''    startBtn.disabled = false;
    startBtn.textContent = "▶ Lancer";
    remaining = duration;
    renderTimer();
  });'''
if 'startBtn.textContent = "▶ Lancer";\n    remaining = duration;' not in s:
    pos = s.find('resetBtn.addEventListener("click"')
    if pos == -1: raise SystemExit('ERROR: reset timer listener not found')
    tail = s[pos:]
    if reset_old not in tail: raise SystemExit('ERROR: reset timer body not found')
    tail = tail.replace(reset_old, reset_new, 1)
    s = s[:pos] + tail

transform_old = '''    svgEl.style.transform = "rotate(" + state.rotation + "deg)";
    if(lightsEl){ lightsEl.classList.remove("idle-glow"); lightsEl.classList.add("spinning"); }'''
transform_new = '''    svgEl.style.transform = "rotate(" + state.rotation + "deg)";
    var tfWheelHolder = svgEl.closest ? svgEl.closest(".wheel-holder") : null;
    if(tfWheelHolder) tfWheelHolder.classList.add("tf-spinning");
    if(lightsEl){ lightsEl.classList.remove("idle-glow"); lightsEl.classList.add("spinning"); }'''
if 'tfWheelHolder.classList.add("tf-spinning")' not in s:
    if transform_old not in s: raise SystemExit('ERROR: wheel transform block not found')
    s = s.replace(transform_old, transform_new, 1)

wheel_done_old = '''      if(lightsEl){ lightsEl.classList.remove("spinning"); lightsEl.classList.add("idle-glow"); }
      onDone(idx);'''
wheel_done_new = '''      if(lightsEl){ lightsEl.classList.remove("spinning"); lightsEl.classList.add("idle-glow"); }
      if(tfWheelHolder) tfWheelHolder.classList.remove("tf-spinning");
      onDone(idx);'''
if 'tfWheelHolder.classList.remove("tf-spinning")' not in s:
    if wheel_done_old not in s: raise SystemExit('ERROR: wheel done block not found')
    s = s.replace(wheel_done_old, wheel_done_new, 1)

standalone_old = '''    spinBtn.disabled = true;
    wheelResult.innerHTML = "";'''
standalone_new = '''    spinBtn.disabled = true;
    spinBtn.classList.add("tf-busy");
    spinBtn.textContent = "🎡 Ça tourne…";
    wheelResult.innerHTML = "";'''
if 'spinBtn.textContent = "🎡 Ça tourne…"' not in s:
    if standalone_old not in s: raise SystemExit('ERROR: standalone spin start not found')
    s = s.replace(standalone_old, standalone_new, 1)

standalone_done_old = '''      spinBtn.disabled = false;
    }, document.getElementById("standaloneWheelLights"));'''
standalone_done_new = '''      tfPopResult(wheelResult);
      spinBtn.disabled = false;
      spinBtn.classList.remove("tf-busy");
      spinBtn.textContent = "Tourner encore";
    }, document.getElementById("standaloneWheelLights"));'''
if 'spinBtn.textContent = "Tourner encore"' not in s:
    if standalone_done_old not in s: raise SystemExit('ERROR: standalone spin done not found')
    s = s.replace(standalone_done_old, standalone_done_new, 1)

game_spin_old = '''  document.getElementById("gameSpinBtn").addEventListener("click", function(){
    document.getElementById("gameSpinBtn").disabled = true;'''
game_spin_new = '''  document.getElementById("gameSpinBtn").addEventListener("click", function(){
    var gameSpinButton = document.getElementById("gameSpinBtn");
    gameSpinButton.disabled = true;
    gameSpinButton.classList.add("tf-busy");
    gameSpinButton.textContent = "🎡 Ça tourne…";'''
if 'gameSpinButton.textContent = "🎡 Ça tourne…"' not in s:
    if game_spin_old not in s: raise SystemExit('ERROR: game spin listener not found')
    s = s.replace(game_spin_old, game_spin_new, 1)

flip_result_old = '''      document.getElementById("gameWheelResultText").innerHTML =
        '<div class="result-sub">' + (seg.type === "mystere" ? "✨ Coup de Piment !" : "+1 " + ING[seg.key].label) + '</div>';
      handleSpinResult(idx);'''
flip_result_new = '''      document.getElementById("gameWheelResultText").innerHTML =
        '<div class="result-sub">' + (seg.type === "mystere" ? "✨ Coup de Piment !" : "+1 " + ING[seg.key].label) + '</div>';
      tfPopResult(document.getElementById("gameWheelResult"));
      gameSpinButton.classList.remove("tf-busy");
      handleSpinResult(idx);'''
if 'tfPopResult(document.getElementById("gameWheelResult"))' not in s:
    if flip_result_old not in s: raise SystemExit('ERROR: game wheel result block not found')
    s = s.replace(flip_result_old, flip_result_new, 1)

render_spin_old = '''      document.getElementById("gameSpinBtn").style.display = "block";
      revealBtn.style.display = "none";'''
render_spin_new = '''      document.getElementById("gameSpinBtn").style.display = "block";
      document.getElementById("gameSpinBtn").textContent = "🎡 Tourner la roue";
      document.getElementById("gameSpinBtn").classList.remove("tf-busy");
      revealBtn.style.display = "none";'''
if 'textContent = "🎡 Tourner la roue"' not in s:
    if render_spin_old not in s: raise SystemExit('ERROR: render spin button block not found')
    s = s.replace(render_spin_old, render_spin_new, 1)

p.write_text(s, encoding='utf-8')
print('Tapas Fiesta gameplay V6 applied: clearer turns, richer feedback, safer interactions')
