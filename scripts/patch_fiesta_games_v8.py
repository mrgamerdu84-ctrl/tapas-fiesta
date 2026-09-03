from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

segments_re = re.compile(r'''  var segments = \[.*?\n  \];\n  var wheelColors = \[.*?\];\n  var wheelColorsDark = \[.*?\];\n  var wheelLabelColors = \[.*?\];''', re.S)
segments_new = r'''  var segments = [
    { key:"avocat", name:"Avocat / Guacamole", emoji:"🥑", type:"ingredient" },
    { key:"piment", name:"Piment / Salsa", emoji:"🌶️", type:"ingredient" },
    { key:"tortilla", name:"Tortilla / Nachos", emoji:"🌮", type:"ingredient" },
    { key:"fromage", name:"Fromage / Queso", emoji:"🧀", type:"ingredient" },
    { key:"viande", name:"Viande / Haricots", emoji:"🍖", type:"ingredient" },
    { key:"epice", name:"Épice Mystère", emoji:"✨", type:"mystere" },
    { key:"coin", name:"Pièce Mexico", emoji:"🪙", type:"coin" },
    { key:"memory", name:"Mémoire Mexico", emoji:"🃏", type:"memory" },
    { key:"bonus", name:"Panier Surprise", emoji:"🎁", type:"bonus" },
    { key:"exchange", name:"Échange Fiesta", emoji:"🔄", type:"exchange" }
  ];
  var wheelColors = ["#5B7B3F","#C6401F","#E8A33D","#F2D06B","#B85C38","#7A3B8C","#0B7C71","#B33B66","#D49B22","#3C78A8"];
  var wheelColorsDark = ["#4A6432","#9E2E17","#C4831C","#D9AD3A","#96492C","#5F2E70","#07564F","#812847","#A97615","#295477"];
  var wheelLabelColors = ["#fff","#fff","#3a2a12","#3a2a12","#fff","#fff","#fff","#fff","#3a2a12","#fff"];'''
s, n = segments_re.subn(segments_new, s, count=1)
if n != 1: raise SystemExit('ERROR V8: wheel segment block not found')

build_re = re.compile(r'''  function buildWheelSVG\(svgEl\)\{.*?\n  \}\n\n  // spins svgEl''', re.S)
build_new = r'''  function buildWheelSVG(svgEl){
    while(svgEl.firstChild) svgEl.removeChild(svgEl.firstChild);
    var slice = 360 / segments.length;
    segments.forEach(function(seg, i){
      var startA=i*slice,endA=(i+1)*slice,p1=pointAt(startA,R),p2=pointAt(endA,R);
      var path=document.createElementNS(svgNS,"path");
      path.setAttribute("d","M"+CX+","+CY+" L"+p1.x.toFixed(2)+","+p1.y.toFixed(2)+" A"+R+","+R+" 0 0,1 "+p2.x.toFixed(2)+","+p2.y.toFixed(2)+" Z");
      path.setAttribute("fill",wheelColors[i%wheelColors.length]); path.setAttribute("stroke",wheelColorsDark[i%wheelColorsDark.length]); path.setAttribute("stroke-width","0.7"); svgEl.appendChild(path);
      var mid=startA+slice/2,textRot=(mid>90&&mid<270)?mid+180:mid,ep=pointAt(mid,R*.72),et=document.createElementNS(svgNS,"text");
      et.setAttribute("x",ep.x.toFixed(2));et.setAttribute("y",ep.y.toFixed(2));et.style.fontSize="9.8px";et.setAttribute("text-anchor","middle");et.setAttribute("dominant-baseline","middle");et.setAttribute("transform","rotate("+textRot+" "+ep.x.toFixed(2)+" "+ep.y.toFixed(2)+")");et.textContent=seg.emoji;svgEl.appendChild(et);
      var lp=pointAt(mid,R*.43),t=document.createElementNS(svgNS,"text");t.setAttribute("x",lp.x.toFixed(2));t.setAttribute("y",lp.y.toFixed(2));t.setAttribute("fill",wheelLabelColors[i%wheelLabelColors.length]);t.setAttribute("text-anchor","middle");t.setAttribute("dominant-baseline","middle");t.style.fontSize="4.4px";t.style.fontWeight="800";t.setAttribute("transform","rotate("+textRot+" "+lp.x.toFixed(2)+" "+lp.y.toFixed(2)+")");
      t.textContent=seg.name.split(" / ")[0].replace("Panier Surprise","Panier").replace("Mémoire Mexico","Mémoire").replace("Échange Fiesta","Échange").replace("Pièce Mexico","Pièce");svgEl.appendChild(t);
    });
    var rim=document.createElementNS(svgNS,"circle");rim.setAttribute("cx",CX);rim.setAttribute("cy",CY);rim.setAttribute("r",R-.5);rim.setAttribute("fill","none");rim.setAttribute("stroke","rgba(255,244,214,.92)");rim.setAttribute("stroke-width","1.2");svgEl.appendChild(rim);
  }

  // spins svgEl'''
s,n=build_re.subn(build_new,s,count=1)
if n!=1: raise SystemExit('ERROR V8: buildWheelSVG not found')

pick_re=re.compile(r'''  function pickWheelIndex\(state\)\{.*?\n  \}\n\n  function spinWheelEl\(svgEl, state, onDone, lightsEl\)\{.*?\n  \}\n\n  var wheelEl =''',re.S)
pick_new=r'''  function pickWheelIndex(state){
    state.history=state.history||[];
    var weights=segments.map(function(seg,i){var w=1;if(seg.type==="mystere")w=.82;if(seg.type==="coin")w=.72;if(seg.type==="memory")w=.66;if(seg.type==="bonus")w=.60;if(seg.type==="exchange")w=.52;if(state.history[0]===i)w*=.06;if(state.history[1]===i)w*=.38;return w*(.86+Math.random()*.28);});
    var total=weights.reduce(function(a,b){return a+b},0),r=Math.random()*total,idx=0;for(var i=0;i<weights.length;i++){r-=weights[i];if(r<=0){idx=i;break}}state.history.unshift(idx);if(state.history.length>4)state.history.length=4;return idx;
  }

  function spinWheelEl(svgEl,state,onDone,lightsEl){
    var idx=pickWheelIndex(state),slice=360/segments.length,center=idx*slice+slice/2,jitter=(Math.random()*slice*.42)-(slice*.21),extraSpins=4+Math.floor(Math.random()*6),duration=3300+Math.floor(Math.random()*1750);
    var desiredRotation=((360-center+jitter)%360+360)%360,currentRotation=((state.rotation%360)+360)%360,deltaRotation=extraSpins*360+((desiredRotation-currentRotation+360)%360),holder=svgEl&&svgEl.closest?svgEl.closest(".wheel-holder"):null,pointer=holder?holder.querySelector(".pointer"):null;
    unlockWheelAudio();state.rotation+=deltaRotation;svgEl.style.transition="transform "+duration+"ms cubic-bezier(0.10,0.74,0.21,1)";svgEl.style.transform="rotate("+state.rotation+"deg)";if(holder)holder.classList.add("tf-wheel-pulse");if(pointer)pointer.classList.add("tf-ratchet");if(lightsEl){lightsEl.classList.remove("idle-glow");lightsEl.classList.add("spinning")}duckMusicFor(duration);
    setTimeout(function(){if(lightsEl){lightsEl.classList.remove("spinning");lightsEl.classList.add("idle-glow")}if(holder)holder.classList.remove("tf-wheel-pulse");if(pointer)pointer.classList.remove("tf-ratchet");onDone(idx)},duration+90);
  }

  var wheelEl ='''
s,n=pick_re.subn(pick_new,s,count=1)
if n!=1: raise SystemExit('ERROR V8: V7 wheel picker/spinner not found')

helper_marker='  /* ---------- Coup de Piment resolution ---------- */'
helpers=r'''  /* ---------- V8 Fiesta Games + voice ---------- */
  var tfVoiceLast="";
  function tfSpeak(text){try{if(!text||!window.speechSynthesis||currentVolume()<=0)return;if(tfVoiceLast===text)return;tfVoiceLast=text;window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang="fr-FR";u.rate=.96+Math.random()*.06;u.pitch=.98+Math.random()*.08;u.volume=.9;var voices=window.speechSynthesis.getVoices?window.speechSynthesis.getVoices():[],fr=voices.filter(function(v){return /^fr/i.test(v.lang||"")});if(fr.length)u.voice=fr[Math.floor(Math.random()*fr.length)];window.speechSynthesis.speak(u);setTimeout(function(){tfVoiceLast=""},700)}catch(e){}}
  function tfSayWheel(seg,player){var who=player?player.name+", ":"",opts=seg.type==="ingredient"?["la roue choisit ","tu remportes ","Fiesta ! voici "]:["la roue déclenche ","attention, ","nouveau défi : "];tfSpeak(who+opts[Math.floor(Math.random()*opts.length)]+seg.name.split(" / ")[0])}
  function tfNormalIngredientKeys(){return ["avocat","piment","tortilla","fromage","viande"]}
  function tfIngredientEmoji(k){var x=segments.filter(function(s){return s.key===k})[0];return x?x.emoji:"🍽️"}
  function tfGiveRandomIngredient(player){var keys=tfNormalIngredientKeys(),key=keys[Math.floor(Math.random()*keys.length)];player.hand[key]=(player.hand[key]||0)+1;return {key:key,label:ING[key].label,emoji:tfIngredientEmoji(key)}}
  function tfOwnedIngredientKeys(player){return tfNormalIngredientKeys().filter(function(k){return(player.hand[k]||0)>0})}
  function tfExchangeFiesta(player,opponent){var a=tfOwnedIngredientKeys(player),b=tfOwnedIngredientKeys(opponent);if(!a.length||!b.length){var g=tfGiveRandomIngredient(player);return "Échange impossible : bonus "+g.emoji+" "+g.label+" !"}var ka=a[Math.floor(Math.random()*a.length)],kb=b[Math.floor(Math.random()*b.length)];player.hand[ka]--;opponent.hand[kb]--;player.hand[kb]=(player.hand[kb]||0)+1;opponent.hand[ka]=(opponent.hand[ka]||0)+1;return player.name+" échange "+ING[ka].label+" contre "+ING[kb].label+"."}

  function tfBuildWheelCoinHTML(playerName){return '<div class="tf-duel-title">'+playerName+', choisis PILE ou FACE :</div><div class="tf-coin-choice-row tf-modal-choices"><button class="tf-coin-choice" data-wheel-coin="tortilla"><span>🌮</span><b>PILE</b><small>Tortilla</small></button><button class="tf-coin-choice" data-wheel-coin="piment"><span>🌶️</span><b>FACE</b><small>Piment</small></button></div><div class="tf-mexico-coin tf-modal-coin" id="tfWheelCoin"><div class="tf-mexico-coin-inner"><div class="tf-mexico-face tf-mexico-front"><span>🌮</span><strong>PILE</strong><small>TORTILLA</small></div><div class="tf-mexico-face tf-mexico-back"><span>🌶️</span><strong>FACE</strong><small>PIMENT</small></div></div></div><div class="modal-result" id="tfWheelCoinResult">Si tu gagnes, tu remportes un ingrédient bonus.</div>'}
  function tfRunWheelCoin(playerIdx,done){var player=game.players[playerIdx];if(player.isAI){var choice=Math.random()<.5?"tortilla":"piment",result=Math.random()<.5?"tortilla":"piment";setTimeout(function(){if(choice===result){var g=tfGiveRandomIngredient(player);showToast("🪙 "+player.name+" gagne : +1 "+g.emoji+" "+g.label,2800);tfSpeak(player.name+" gagne la Pièce Mexico")}else showToast("🪙 "+player.name+" perd la Pièce Mexico.",2400);renderGame();setTimeout(done,700)},900);return}openModal("🪙 Pièce Mexico",tfBuildWheelCoinHTML(player.name),function(){var buttons=document.querySelectorAll("#modalBody [data-wheel-coin]"),settled=false;buttons.forEach(function(btn){btn.addEventListener("click",function(){if(settled)return;settled=true;buttons.forEach(function(b){b.disabled=true;b.classList.toggle("active",b===btn)});var choice=btn.dataset.wheelCoin,result=Math.random()<.5?"tortilla":"piment",res=document.getElementById("tfWheelCoinResult");res.textContent="🪙 La pièce tourne…";tfAnimateCoin(document.getElementById("tfWheelCoin"),result,function(){if(choice===result){var g=tfGiveRandomIngredient(player);res.innerHTML="🎉 <strong>Gagné !</strong> +1 "+g.emoji+" "+g.label;tfSpeak("Gagné, ingrédient bonus")}else{res.innerHTML="🌶️ <strong>Perdu !</strong> Aucun bonus cette fois.";tfSpeak("Perdu, aucun bonus")}setTimeout(function(){closeModal();renderGame();done()},1200)})})})})}

  function tfMemoryDeck(){var keys=tfNormalIngredientKeys().slice(),chosen=[];while(chosen.length<4)chosen.push(keys.splice(Math.floor(Math.random()*keys.length),1)[0]);return shuffle(chosen.concat(chosen).map(function(k,i){return{key:k,id:k+"-"+i}}))}
  function tfBuildMemoryHTML(){var deck=tfMemoryDeck();window.tfMemoryRound={deck:deck,open:[],pairs:0,attempts:0,busy:false};var html='<div class="tf-memory-head"><strong>🃏 Trouve 3 paires</strong><span id="tfMemoryScore">0/3 paires • 0/7 essais</span></div><div class="tf-memory-grid">';deck.forEach(function(c,i){html+='<button class="tf-memory-card" data-memory-index="'+i+'"><span class="tf-card-back">🌵</span><span class="tf-card-front">'+tfIngredientEmoji(c.key)+'</span></button>'});return html+'</div><div class="modal-result" id="tfMemoryResult">Retourne deux cartes. Maximum 7 essais.</div>'}
  function tfRunMemory(playerIdx,done){var player=game.players[playerIdx];if(player.isAI){showToast("🃏 "+player.name+" joue à Mémoire Mexico…");setTimeout(function(){var success=Math.random()<.68;if(success){var g=tfGiveRandomIngredient(player);showToast("🤖 3 paires ! +1 "+g.emoji+" "+g.label,2700);tfSpeak(player.name+" trouve trois paires")}else showToast("🤖 "+player.name+" rate le Mémoire Mexico.",2300);renderGame();setTimeout(done,700)},1500);return}openModal("🃏 Mémoire Mexico",tfBuildMemoryHTML(),function(){var st=window.tfMemoryRound,cards=document.querySelectorAll("#modalBody .tf-memory-card");function finish(success){st.busy=true;cards.forEach(function(c){c.disabled=true});var res=document.getElementById("tfMemoryResult");if(success){var g=tfGiveRandomIngredient(player);res.innerHTML="🎉 <strong>3 paires trouvées !</strong><br>+1 "+g.emoji+" "+g.label;tfSpeak("Trois paires trouvées, ingrédient bonus")}else{res.innerHTML="🌶️ <strong>Défi raté.</strong> Il fallait 3 paires en 7 essais.";tfSpeak("Défi mémoire raté")}setTimeout(function(){closeModal();renderGame();done()},1400)}cards.forEach(function(card){card.addEventListener("click",function(){if(st.busy||card.classList.contains("matched")||card.classList.contains("open"))return;var idx=Number(card.dataset.memoryIndex);card.classList.add("open");st.open.push(idx);if(st.open.length<2)return;st.busy=true;st.attempts++;var a=st.open[0],b=st.open[1],same=st.deck[a].key===st.deck[b].key;setTimeout(function(){if(same){cards[a].classList.add("matched");cards[b].classList.add("matched");st.pairs++}else{cards[a].classList.remove("open");cards[b].classList.remove("open")}st.open=[];st.busy=false;var score=document.getElementById("tfMemoryScore");if(score)score.textContent=st.pairs+"/3 paires • "+st.attempts+"/7 essais";if(st.pairs>=3)finish(true);else if(st.attempts>=7)finish(false)},650)})})})}

'''
if 'function tfRunMemory(' not in s:
    if helper_marker not in s: raise SystemExit('ERROR V8: Coup de Piment marker not found')
    s=s.replace(helper_marker,helpers+helper_marker,1)

handle_re=re.compile(r'''  function handleSpinResult\(idx\)\{.*?\n  \}\n\n  var gameWheelEl =''',re.S)
handle_new=r'''  function handleSpinResult(idx){
    var seg=segments[idx],player=game.players[game.turn],opponent=game.players[1-game.turn];game.hasSpun=true;tfSayWheel(seg,player);
    if(seg.type==="ingredient"||seg.type==="mystere"){player.hand[seg.key]=(player.hand[seg.key]||0)+1;if(player.isAI)showToast("🤖 "+player.name+" pioche "+seg.emoji+" "+ING[seg.key].label);setTimeout(function(){if(seg.key==="epice")resolveCoupDePiment(game.turn,1-game.turn,function(){afterSpinUpdate()});else afterSpinUpdate()},1050);return}
    if(seg.type==="coin"){setTimeout(function(){tfRunWheelCoin(game.turn,function(){afterSpinUpdate()})},500);return}
    if(seg.type==="memory"){setTimeout(function(){tfRunMemory(game.turn,function(){afterSpinUpdate()})},500);return}
    if(seg.type==="bonus"){var g=tfGiveRandomIngredient(player);showToast("🎁 Panier Surprise : +1 "+g.emoji+" "+g.label,2600);tfSpeak("Panier surprise, "+g.label);setTimeout(afterSpinUpdate,1000);return}
    if(seg.type==="exchange"){var msg=tfExchangeFiesta(player,opponent);showToast("🔄 "+msg,3000);tfSpeak("Échange Fiesta");setTimeout(afterSpinUpdate,1100);return}
    setTimeout(afterSpinUpdate,600);
  }

  var gameWheelEl ='''
s,n=handle_re.subn(handle_new,s,count=1)
if n!=1: raise SystemExit('ERROR V8: handleSpinResult not found')

wrapper_old='''      document.getElementById("gameWheelResultText").innerHTML =\n        '<div class="result-sub">' + (seg.type === "mystere" ? "✨ Coup de Piment !" : "+1 " + ING[seg.key].label) + '</div>';'''
wrapper_new='''      var tfResultLabel=(seg.type==="mystere")?"✨ Coup de Piment !":(seg.type==="ingredient"?"+1 "+ING[seg.key].label:(seg.type==="coin"?"🪙 Pièce Mexico !":(seg.type==="memory"?"🃏 Mémoire Mexico !":(seg.type==="bonus"?"🎁 Panier Surprise !":"🔄 Échange Fiesta !"))));\n      document.getElementById("gameWheelResultText").innerHTML='<div class="result-sub">'+tfResultLabel+'</div>';'''
if wrapper_old not in s: raise SystemExit('ERROR V8: game wheel result block not found')
s=s.replace(wrapper_old,wrapper_new,1)

stand_old='''      wheelResult.innerHTML =\n        '<div class="result-pill">' + seg.name + '</div>' +\n        '<div class="result-sub">' + (seg.type === "mystere" ? "Pioche une carte Coup de Piment !" : "Pioche la carte Ingrédient correspondante.") + '</div>';\n      spinBtn.disabled = false;'''
stand_new='''      var tip=seg.type==="ingredient"?"Pioche la carte Ingrédient correspondante.":(seg.type==="mystere"?"Coup de Piment !":(seg.type==="coin"?"Lance la Pièce Mexico : Pile Tortilla ou Face Piment.":(seg.type==="memory"?"Joue à Mémoire Mexico et trouve 3 paires.":(seg.type==="bonus"?"Panier Surprise : gagne un ingrédient au hasard.":"Échange un ingrédient avec un adversaire."))));\n      wheelResult.innerHTML='<div class="result-pill">'+seg.emoji+' '+seg.name+'</div><div class="result-sub">'+tip+'</div>';tfSayWheel(seg,null);spinBtn.disabled=false;'''
if stand_old not in s: raise SystemExit('ERROR V8: standalone wheel result block not found')
s=s.replace(stand_old,stand_new,1)

turn_old='''      showToast("🤖 Tour de " + game.players[game.turn].name + "…");\n      setTimeout(runAiTurn, 800);'''
turn_new='''      showToast("🤖 Tour de " + game.players[game.turn].name + "…");\n      tfSpeak("Au tour de " + game.players[game.turn].name);\n      setTimeout(runAiTurn, 800);'''
if turn_old in s:s=s.replace(turn_old,turn_new,1)
recipe_old='''    showToast((playerIdx === game.turn ? "🎉 Recette validée : " : "🎉 ") + recipe.name + " !");'''
recipe_new='''    showToast((playerIdx === game.turn ? "🎉 Recette validée : " : "🎉 ") + recipe.name + " !");\n    tfSpeak("Recette terminée : " + recipe.name);'''
if recipe_old in s:s=s.replace(recipe_old,recipe_new,1)

css=r'''
<style id="tf-fiesta-games-v8">
.tf-memory-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:0 0 13px;font-family:Georgia,serif;color:#573323}.tf-memory-head span{font:800 .72rem system-ui;color:#087267;background:#edf8ef;padding:6px 8px;border-radius:999px;white-space:nowrap}.tf-memory-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin:10px auto 15px;max-width:390px}.tf-memory-card{position:relative;aspect-ratio:.78;border:2px solid #d8aa4a;border-radius:15px;background:linear-gradient(145deg,#087267,#07564f);box-shadow:0 6px 12px rgba(65,38,22,.13);font-size:1.9rem;overflow:hidden;transform-style:preserve-3d;transition:transform .22s ease}.tf-memory-card .tf-card-back,.tf-memory-card .tf-card-front{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;backface-visibility:hidden}.tf-memory-card .tf-card-back{color:#ffeab0}.tf-memory-card .tf-card-front{transform:rotateY(180deg);background:#fff7e6}.tf-memory-card.open,.tf-memory-card.matched{transform:rotateY(180deg)}.tf-memory-card.matched{border-color:#5f8d3b;box-shadow:0 0 0 3px rgba(95,141,59,.16)}#modalOverlay .modal-box{max-height:min(86vh,720px);overflow:auto;overscroll-behavior:contain}.wheel-holder{margin-left:auto!important;margin-right:auto!important}.wheel-holder svg{display:block;max-width:100%!important;height:auto!important}.game-wheel-section,.wheel-card{overflow:hidden!important}@media(max-width:480px){main{padding-left:12px!important;padding-right:12px!important}.wheel-holder{width:min(78vw,318px)!important;max-width:318px!important}.tf-memory-grid{gap:7px}.tf-memory-card{border-radius:12px;font-size:1.65rem}.modal-box{width:calc(100vw - 22px)!important;margin:11px!important;padding-left:14px!important;padding-right:14px!important}.bottom-nav{padding-bottom:max(8px,env(safe-area-inset-bottom))!important}}@media(max-width:360px){.wheel-holder{width:min(75vw,275px)!important}.tf-memory-grid{gap:5px}.tf-memory-card{font-size:1.45rem}.tf-memory-head{align-items:flex-start;flex-direction:column}}
</style>
'''
if 'id="tf-fiesta-games-v8"' not in s:s=s.replace('</head>',css+'\n</head>',1)
s=s.replace('Le compagnon de jeu de Tapas Fiesta! : fais tourner la roue, lance la Pièce Mexico et cuisine tes recettes.','Le compagnon de jeu de Tapas Fiesta! : roue Fiesta, Pièce Mexico, Mémoire Mexico et recettes à cuisiner.',1)

required=['if(seg.type==="ingredient"||seg.type==="mystere")','resolveCoupDePiment(game.turn,1-game.turn','setTimeout(runAiTurn, 800)','function tfRunWheelCoin(','function tfRunMemory(','Maximum 7 essais','type:"bonus"','type:"exchange"','function tfSpeak(']
for marker in required:
    if marker not in s:raise SystemExit('ERROR V8 validation missing: '+marker)

p.write_text(s,encoding='utf-8')
print('Tapas Fiesta V8 Fiesta Games applied')
