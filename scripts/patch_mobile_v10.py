from pathlib import Path
import re

p=Path('www/index.html')
s=p.read_text(encoding='utf-8')

# ---- CSS ----
css=r'''
<style id="tf-v10-mobile">
.tf-mode-choice{margin:14px 0 16px;padding:12px;border-radius:20px;background:linear-gradient(145deg,#fff9e9,#f8ecd0);border:1px solid rgba(92,58,30,.14);box-shadow:0 7px 18px rgba(70,40,20,.08)}
.tf-mode-choice h3{font-family:Georgia,serif;text-align:center;color:#7d2e22;margin:0 0 9px;font-size:1.05rem}.tf-mode-choice-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px}.tf-mode-option{border:2px solid transparent;border-radius:16px;background:#fff;padding:12px 8px;font-weight:900;color:#573323;min-height:92px}.tf-mode-option .big{display:block;font-size:1.75rem;margin-bottom:5px}.tf-mode-option small{display:block;font-weight:700;color:#78624b;margin-top:4px;line-height:1.25}.tf-mode-option.active{border-color:#087267;background:#effaf6;box-shadow:0 0 0 3px rgba(8,114,103,.10)}.tf-mode-option.soon{opacity:.83}.tf-mode-status{text-align:center;font-size:.78rem;font-weight:800;color:#6e5942;margin-top:8px}
.tf-dice-game{padding:4px 0 2px}.tf-dice-recipe{background:#fff5dc;border:1px solid rgba(116,70,30,.14);border-radius:17px;padding:10px;text-align:center;margin-bottom:10px}.tf-dice-recipe h3{font-family:Georgia,serif;color:#8f2e21;margin:0 0 5px}.tf-dice-needs{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}.tf-dice-need{padding:5px 8px;border-radius:999px;background:#fff;border:1px solid rgba(90,55,30,.12);font-weight:900}.tf-dice-score{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:start;margin:9px 0}.tf-dice-player{background:#fff;border-radius:15px;padding:9px 6px;text-align:center;border:1px solid rgba(90,55,30,.11);font-weight:900}.tf-dice-progress{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;margin-top:6px}.tf-dice-progress span{font-size:.78rem;padding:3px 5px;border-radius:8px;background:#f4ede2;opacity:.52}.tf-dice-progress span.done{background:#e7f7ed;opacity:1;box-shadow:inset 0 0 0 1px rgba(25,115,72,.16)}.tf-dice-turn{text-align:center;font-weight:950;color:#8f2e21;margin:7px 0}.tf-die-stage{height:110px;display:flex;align-items:center;justify-content:center;perspective:500px;margin:4px 0}.tf-die3d{width:70px;height:70px;position:relative;transform-style:preserve-3d;transition:transform .82s cubic-bezier(.18,.74,.23,1)}.tf-die3d.rolling{animation:tfDieShake .18s linear infinite}.tf-die-face{position:absolute;width:70px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:13px;background:linear-gradient(145deg,#fffef8,#f2e3bc);border:3px solid #8d4e2c;box-shadow:inset 0 0 14px rgba(255,255,255,.8);font-size:2rem}.tf-die-face.f1{transform:translateZ(35px)}.tf-die-face.f2{transform:rotateY(90deg) translateZ(35px)}.tf-die-face.f3{transform:rotateY(180deg) translateZ(35px)}.tf-die-face.f4{transform:rotateY(-90deg) translateZ(35px)}.tf-die-face.f5{transform:rotateX(90deg) translateZ(35px)}.tf-die-face.f6{transform:rotateX(-90deg) translateZ(35px)}@keyframes tfDieShake{0%{transform:rotateX(0) rotateY(0) rotateZ(0)}50%{transform:rotateX(48deg) rotateY(72deg) rotateZ(22deg)}100%{transform:rotateX(96deg) rotateY(144deg) rotateZ(44deg)}}
.tf-dice-roll{width:100%;border:0;border-radius:15px;padding:13px;background:#087267;color:#fff;font-weight:950;font-size:1rem}.tf-dice-roll:disabled{opacity:.55}.tf-dice-result{text-align:center;min-height:48px;margin-top:8px;font-weight:850;color:#573323}.tf-dice-win{animation:tfDiceWin .55s ease-out both}@keyframes tfDiceWin{0%{transform:scale(.75);opacity:.3}70%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
@media(max-width:390px){.tf-mode-choice-grid{grid-template-columns:1fr}.tf-dice-score{grid-template-columns:1fr}.tf-dice-score>b{display:none}.tf-die-stage{height:100px}.tf-die3d,.tf-die-face{width:62px;height:62px}.tf-die-face.f1{transform:translateZ(31px)}.tf-die-face.f2{transform:rotateY(90deg) translateZ(31px)}.tf-die-face.f3{transform:rotateY(180deg) translateZ(31px)}.tf-die-face.f4{transform:rotateY(-90deg) translateZ(31px)}.tf-die-face.f5{transform:rotateX(90deg) translateZ(31px)}.tf-die-face.f6{transform:rotateX(-90deg) translateZ(31px)}}
</style>
'''
if 'id="tf-v10-mobile"' not in s:
    s=s.replace('</head>',css+'\n</head>',1)

# ---- Home mobile / plateau choice ----
chooser='''\n    <div class="tf-mode-choice" id="tfModeChoice">\n      <h3>Choisis ta façon de jouer</h3>\n      <div class="tf-mode-choice-grid">\n        <button class="tf-mode-option active" id="tfModeMobile" type="button"><span class="big">📱</span>Mode Mobile<small>Jeu complet dans l’application, avec IA ou ami.</small></button>\n        <button class="tf-mode-option soon" id="tfModeBoard" type="button"><span class="big">🎲</span>Mode Plateau<small>Compagnon du plateau imprimé — prochaine étape.</small></button>\n      </div>\n      <div class="tf-mode-status" id="tfModeStatus">📱 Mode Mobile sélectionné</div>\n    </div>\n'''
if 'id="tfModeChoice"' not in s:
    anchor='''    <div class="quick-grid">'''
    if anchor not in s: raise SystemExit('V10 home quick-grid anchor missing')
    s=s.replace(anchor,chooser+anchor,1)

# ---- Add Dice Tapas to wheel segment and color arrays ----
old='''{key:"mask",name:"Masque Mexicain",emoji:"🎭",type:"mask"}\n  ];'''
new='''{key:"mask",name:"Masque Mexicain",emoji:"🎭",type:"mask"},{key:"dicegame",name:"Dé Tapas",emoji:"🎲",type:"dicegame"}\n  ];'''
if 'type:"dicegame"' not in s:
    if old not in s: raise SystemExit('V10 mask segment anchor missing')
    s=s.replace(old,new,1)
    s=s.replace('''var wheelColors=["#5B7B3F","#C6401F","#E8A33D","#F2D06B","#B85C38","#7A3B8C","#0B7C71","#B33B66","#D49B22","#3C78A8","#6B2523","#E7B52C","#116C65"];''','''var wheelColors=["#5B7B3F","#C6401F","#E8A33D","#F2D06B","#B85C38","#7A3B8C","#0B7C71","#B33B66","#D49B22","#3C78A8","#6B2523","#E7B52C","#116C65","#5B4DA8"];''',1)
    s=s.replace('''var wheelColorsDark=["#4A6432","#9E2E17","#C4831C","#D9AD3A","#96492C","#5F2E70","#07564F","#812847","#A97615","#295477","#3B1110","#A8780C","#084A45"];''','''var wheelColorsDark=["#4A6432","#9E2E17","#C4831C","#D9AD3A","#96492C","#5F2E70","#07564F","#812847","#A97615","#295477","#3B1110","#A8780C","#084A45","#3D337B"];''',1)
    s=s.replace('''var wheelLabelColors=["#fff","#fff","#3a2a12","#3a2a12","#fff","#fff","#fff","#fff","#3a2a12","#fff","#fff","#35240a","#fff"];''','''var wheelLabelColors=["#fff","#fff","#3a2a12","#3a2a12","#fff","#fff","#fff","#fff","#3a2a12","#fff","#fff","#35240a","#fff","#fff"];''',1)

# ---- Weight the new mini-game as a special, not too common ----
if 'seg.type==="dicegame"' not in s[s.find('function pickWheelIndex'):s.find('function spinWheelEl')]:
    s=s.replace('''if(seg.type==="mask")x=.30;''','''if(seg.type==="mask")x=.30;if(seg.type==="dicegame")x=.48;''',1)

# ---- Wheel legends: both game and standalone ----
s=s.replace('<span><b>🎭</b>Masque</span></div>','<span><b>🎭</b>Masque</span><span><b>🎲</b>Dé Tapas</span></div>')

# ---- standalone wheel tip ----
s=s.replace('''mask:"Gagne une recette complète."};var tip=tips[seg.type]||"Événement Fiesta !";''','''mask:"Gagne une recette complète.",dicegame:"Dé Tapas : complète la recette avant ton adversaire."};var tip=tips[seg.type]||"Événement Fiesta !";''',1)

# ---- Dice Tapas duel helpers, before Coup de Piment ----
marker='''  /* ---------- Coup de Piment resolution ---------- */'''
helpers=r'''
  function tfDiceKeys(){return ["avocat","piment","tortilla","fromage","viande","epice"]}
  function tfDiceFaceTransform(n){var map={1:"rotateX(0deg) rotateY(0deg)",2:"rotateX(0deg) rotateY(-90deg)",3:"rotateX(0deg) rotateY(180deg)",4:"rotateX(0deg) rotateY(90deg)",5:"rotateX(-90deg) rotateY(0deg)",6:"rotateX(90deg) rotateY(0deg)"};return map[n]||map[1]}
  function tfDiceNeedEntries(recipe){var arr=[];Object.keys(recipe.need).forEach(function(k){for(var n=0;n<recipe.need[k];n++)arr.push(k)});return arr}
  function tfDiceProgressHTML(st,idx){var need=tfDiceNeedEntries(st.recipe),got=st.progress[idx]||{},used={};return need.map(function(k){used[k]=(used[k]||0)+1;var ok=(got[k]||0)>=used[k];return '<span class="'+(ok?'done':'')+'">'+tfIngredientEmoji(k)+'</span>'}).join('')}
  function tfDiceDone(st,idx){var got=st.progress[idx]||{},keys=Object.keys(st.recipe.need);for(var i=0;i<keys.length;i++){var k=keys[i];if((got[k]||0)<st.recipe.need[k])return false}return true}
  function tfBuildDiceTapasHTML(st){var faces=tfDiceKeys().map(function(k,i){return '<div class="tf-die-face f'+(i+1)+'">'+tfIngredientEmoji(k)+'</div>'}).join('');var needs=tfDiceNeedEntries(st.recipe).map(function(k){return '<span class="tf-dice-need">'+tfIngredientEmoji(k)+' '+ING[k].label+'</span>'}).join('');return '<div class="tf-dice-game"><div class="tf-dice-recipe"><h3>🌮 '+st.recipe.name+'</h3><div class="tf-dice-needs">'+needs+'</div></div><div class="tf-dice-score"><div class="tf-dice-player">'+game.players[0].avatar+' '+game.players[0].name+'<div class="tf-dice-progress" id="tfDiceProg0"></div></div><b>VS</b><div class="tf-dice-player">'+game.players[1].avatar+' '+game.players[1].name+'<div class="tf-dice-progress" id="tfDiceProg1"></div></div></div><div class="tf-dice-turn" id="tfDiceTurn"></div><div class="tf-die-stage"><div class="tf-die3d" id="tfDie3d">'+faces+'</div></div><button class="tf-dice-roll" id="tfDiceRoll">🎲 Lancer le dé</button><div class="tf-dice-result" id="tfDiceResult">Le premier qui complète la tapas gagne une recette complète.</div></div>'}
  function tfRunDiceTapas(starter,done){
    var recipe=RECIPES_ALL[Math.floor(Math.random()*RECIPES_ALL.length)];
    var st={recipe:recipe,progress:[{},{}],turn:starter,busy:false,ended:false,rolls:0};
    openModal("🎲 Dé Tapas — Duel",tfBuildDiceTapasHTML(st),function(){
      var die=document.getElementById("tfDie3d"),btn=document.getElementById("tfDiceRoll"),res=document.getElementById("tfDiceResult"),turn=document.getElementById("tfDiceTurn");
      function update(){for(var i=0;i<2;i++){var el=document.getElementById("tfDiceProg"+i);if(el)el.innerHTML=tfDiceProgressHTML(st,i)}var p=game.players[st.turn];if(turn)turn.textContent=(p.isAI?"🤖 ":"👉 ")+"Au tour de "+p.name;if(btn){btn.disabled=st.busy||st.ended||p.isAI;btn.textContent=p.isAI?"🤖 L’IA lance le dé…":"🎲 Lancer le dé"}}
      function finish(i){if(st.ended)return;st.ended=true;st.busy=true;var p=game.players[i],r=tfAwardCompleteRecipe(i,"Dé Tapas");if(res){res.classList.add("tf-dice-win");res.innerHTML='🏆 <strong>'+p.name+' complète '+st.recipe.name+' !</strong><br>'+(r?'Recette gagnée : '+r.name:'Victoire du duel !')}tfSpeak(p.name+" termine la tapas en premier et gagne le duel du dé");setTimeout(function(){closeModal();renderGame();done()},2100)}
      function roll(){if(st.busy||st.ended)return;st.busy=true;var p=game.players[st.turn],n=1+Math.floor(Math.random()*6),key=tfDiceKeys()[n-1];if(btn)btn.disabled=true;if(res)res.textContent=p.name+" lance le dé…";if(die){die.classList.add("rolling");die.style.transform="rotateX("+(360+Math.random()*360)+"deg) rotateY("+(360+Math.random()*360)+"deg)"}duckMusicFor(950);setTimeout(function(){if(die){die.classList.remove("rolling");die.style.transform=tfDiceFaceTransform(n)}var need=st.recipe.need[key]||0,have=st.progress[st.turn][key]||0,useful=have<need;if(useful)st.progress[st.turn][key]=have+1;st.rolls++;if(res)res.innerHTML='🎲 '+p.name+' obtient '+tfIngredientEmoji(key)+' <strong>'+ING[key].label+'</strong><br>'+(useful?'✅ Ingrédient ajouté à la tapas.':'↪️ Cet ingrédient n’est plus nécessaire.');tfSpeak(p.name+" obtient "+ING[key].label);update();if(tfDiceDone(st,st.turn)){setTimeout(function(){finish(st.turn)},650);return}st.turn=1-st.turn;st.busy=false;update();if(game.players[st.turn].isAI)setTimeout(roll,850)},900)}
      btn.addEventListener("click",roll);update();if(game.players[st.turn].isAI)setTimeout(roll,900)
    })
  }

'''
if 'function tfRunDiceTapas(' not in s:
    if marker not in s: raise SystemExit('V10 Coup de Piment marker missing')
    s=s.replace(marker,helpers+marker,1)

# ---- Handle wheel result special ----
if 'if(seg.type==="dicegame")' not in s[s.find('function handleSpinResult(idx)'):s.find('var gameWheelEl')]:
    s=s.replace('''if(seg.type==="lightning"){setTimeout(function(){tfRunLightning(game.turn)},400);return}setTimeout(afterSpinUpdate,500)}''','''if(seg.type==="lightning"){setTimeout(function(){tfRunLightning(game.turn)},400);return}if(seg.type==="dicegame"){setTimeout(function(){tfRunDiceTapas(game.turn,afterSpinUpdate)},450);return}setTimeout(afterSpinUpdate,500)}''',1)

# Better game result label mapping (also fixes old fallback for bomb/lightning/mask)
pat=re.compile(r'''var tfResultLabel=\(seg\.type==="mystere"\).*?;\n      document\.getElementById\("gameWheelResultText"\)''',re.S)
repl='''var tfResultLabels={mystere:"✨ Coup de Piment !",coin:"🪙 Pièce Mexico !",memory:"🃏 Mémoire Duel !",bonus:"🎁 Panier Surprise !",exchange:"🔄 Échange Fiesta !",bomb:"💣 Explosif !",lightning:"⚡ Éclair Turbo !",mask:"🎭 Masque Mexicain !",dicegame:"🎲 Dé Tapas !"};var tfResultLabel=seg.type==="ingredient"?"+1 "+ING[seg.key].label:(tfResultLabels[seg.type]||"🎉 Événement Fiesta !");\n      document.getElementById("gameWheelResultText")'''
s,n=pat.subn(repl,s,count=1)
if n!=1: raise SystemExit('V10 wheel result label block missing')

# ---- Home mode chooser behavior ----
js=r'''
  /* ---------- V10 mode selector ---------- */
  window.tfAppMode="mobile";
  (function(){
    var mobile=document.getElementById("tfModeMobile"),board=document.getElementById("tfModeBoard"),status=document.getElementById("tfModeStatus");
    function setMobile(){window.tfAppMode="mobile";if(mobile)mobile.classList.add("active");if(board)board.classList.remove("active");if(status)status.textContent="📱 Mode Mobile sélectionné";tfSpeak("Mode mobile sélectionné")}
    if(mobile)mobile.addEventListener("click",setMobile);
    if(board)board.addEventListener("click",function(){window.tfAppMode="plateau";board.classList.add("active");mobile.classList.remove("active");if(status)status.textContent="🎲 Mode Plateau : prochaine étape";openModal("🎲 Mode Plateau",'<div class="tf-v9-special"><div class="big">🎲</div><h3>Mode Plateau</h3><p>Le compagnon Plateau utilisera la roue, Mémoire Duel et le dé automatique, uniquement entre joueurs humains.</p><p><strong>Pour cette V10, le Mode Mobile reste la version jouable complète.</strong></p>',function(){})});
    var launch=document.querySelector('#view-accueil [data-goto="jouer"]');if(launch)launch.addEventListener("click",function(){window.tfAppMode="mobile";if(status)status.textContent="📱 Mode Mobile sélectionné"});
  })();
'''
if 'V10 mode selector' not in s:
    pos=s.rfind('</script>')
    if pos<0: raise SystemExit('V10 closing script missing')
    s=s[:pos]+js+'\n'+s[pos:]

s=s.replace('roue Fiesta, Mémoire Duel, Éclair Turbo, Explosif, Masque Mexicain et recettes à cuisiner.','roue Fiesta, Dé Tapas, Mémoire Duel, Éclair Turbo, Explosif, Masque Mexicain et recettes à cuisiner.')

required=['type:"dicegame"','function tfRunDiceTapas(','tf-die3d','Dé Tapas — Duel','tfModeMobile','tfModeBoard','dicegame:"🎲 Dé Tapas !"','if(seg.type==="dicegame")','Égalité 2–2','function tfRunMemory(','function runAiTurn()','function tfAwardCompleteRecipe(']
miss=[x for x in required if x not in s]
if miss: raise SystemExit('V10 validation: '+', '.join(miss))

p.write_text(s,encoding='utf-8')
print('V10 mobile patch OK')
