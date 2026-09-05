from pathlib import Path
import re

p=Path('www/index.html')
s=p.read_text(encoding='utf-8')

css=r'''
<style id="tf-v82-visibility">
/* V8.2: the wheel itself contains only symbols. Names live clearly below it. */
.tf-wheel-legend{
  display:flex;flex-wrap:wrap;justify-content:center;gap:6px 8px;
  width:min(100%,430px);margin:20px auto 12px;padding:11px 10px;
  border-radius:17px;background:rgba(255,250,238,.95);
  border:1px solid rgba(123,75,38,.16);box-shadow:0 5px 12px rgba(70,42,24,.07);
}
.tf-wheel-legend span{display:inline-flex;align-items:center;gap:4px;padding:5px 8px;border-radius:999px;background:#fff8e8;border:1px solid rgba(100,65,35,.12);font-size:.70rem;font-weight:850;color:#533827;white-space:nowrap}
.tf-wheel-legend b{font-size:.92rem;line-height:1}
#wheelHolderBox + .tf-wheel-legend{margin-top:24px!important;margin-bottom:10px!important}
#view-roue .wheel-holder + .tf-wheel-legend{margin-top:25px!important;margin-bottom:18px!important}
#wheelStickyBox.tf-ai-showcase{outline:4px solid rgba(227,167,45,.40)!important;outline-offset:2px!important;animation:tfAiShowcase .72s ease-in-out infinite alternate}
@keyframes tfAiShowcase{from{transform:scale(.992)}to{transform:scale(1)}}
#gameWheelResultText .tf-ai-result{font-size:1rem;font-weight:950;color:#8f2e21;padding:7px 5px}
.tf-ai-mini-status{font-family:Georgia,serif;font-size:1.02rem;font-weight:850;color:#573323;text-align:center;margin:2px 0 12px}
@media(max-width:480px){.tf-wheel-legend{gap:5px;margin-top:18px;padding:9px 7px}.tf-wheel-legend span{font-size:.64rem;padding:4px 7px}}
</style>
'''
if 'id="tf-v82-visibility"' not in s:
    s=s.replace('</head>',css+'\n</head>',1)

label_re=re.compile(r'''\n      var lp=pointAt\(mid,R\*\.56\),t=document\.createElementNS\(svgNS,"text"\);.*?svgEl\.appendChild\(t\);''',re.S)
s,n=label_re.subn('\n      // V8.2: text labels are rendered in the legend below the wheel.',s,count=1)
if n!=1:
    raise SystemExit('ERROR V8.2: current wheel SVG label block not found')

legend='''<div class="tf-wheel-legend" aria-label="Légende de la roue"><span><b>🥑</b>Avocat</span><span><b>🌶️</b>Piment</span><span><b>🌮</b>Tortilla</span><span><b>🧀</b>Fromage</span><span><b>🍖</b>Viande</span><span><b>✨</b>Mystère</span><span><b>🪙</b>Pièce</span><span><b>🃏</b>Mémoire</span><span><b>🎁</b>Panier</span><span><b>🔄</b>Échange</span></div>'''
if 'aria-label="Légende de la roue"' not in s:
    game_anchor='''            <div class="hub"></div>\n          </div>\n          <div class="result-box" id="gameWheelResult">'''
    game_new='''            <div class="hub"></div>\n          </div>\n          '''+legend+'''\n          <div class="result-box" id="gameWheelResult">'''
    if game_anchor not in s: raise SystemExit('ERROR V8.2: game wheel legend anchor not found')
    s=s.replace(game_anchor,game_new,1)
    stand_anchor='''        <div class="hub"></div>\n      </div>\n      <button class="spin-btn" id="spinBtn">Tourner</button>'''
    stand_new='''        <div class="hub"></div>\n      </div>\n      '''+legend+'''\n      <button class="spin-btn" id="spinBtn">Tourner</button>'''
    if stand_anchor not in s: raise SystemExit('ERROR V8.2: standalone wheel legend anchor not found')
    s=s.replace(stand_anchor,stand_new,1)

coin_re=re.compile(r'''  function tfRunWheelCoin\(playerIdx,done\)\{.*?\n\n  function tfMemoryDeck\(\)''',re.S)
coin_new=r'''  function tfRunWheelCoin(playerIdx,done){
    var player=game.players[playerIdx];
    if(player.isAI){
      var choice=Math.random()<.5?"tortilla":"piment", result=Math.random()<.5?"tortilla":"piment";
      var choiceText=choice==="tortilla"?"PILE — Tortilla 🌮":"FACE — Piment 🌶️";
      var body='<div class="tf-ai-mini-status">🤖 '+player.name+' choisit <strong>'+choiceText+'</strong></div>'+
        '<div class="tf-mexico-coin tf-modal-coin" id="tfAiWheelCoin"><div class="tf-mexico-coin-inner"><div class="tf-mexico-face tf-mexico-front"><span>🌮</span><strong>PILE</strong><small>TORTILLA</small></div><div class="tf-mexico-face tf-mexico-back"><span>🌶️</span><strong>FACE</strong><small>PIMENT</small></div></div></div>'+
        '<div class="modal-result" id="tfAiWheelCoinResult">🪙 La pièce va être lancée…</div>';
      openModal("🤖 Pièce Mexico — tour de l’IA",body,function(){
        setTimeout(function(){
          var res=document.getElementById("tfAiWheelCoinResult");
          if(res)res.textContent="🪙 La pièce tourne…";
          tfAnimateCoin(document.getElementById("tfAiWheelCoin"),result,function(){
            var won=choice===result;
            var resultLabel=result==="tortilla"?"PILE — Tortilla 🌮":"FACE — Piment 🌶️";
            if(won){var g=tfGiveRandomIngredient(player);if(res)res.innerHTML='<strong>'+resultLabel+'</strong><br>🎉 '+player.name+' gagne +1 '+g.emoji+' '+g.label;tfSpeak(player.name+" gagne la Pièce Mexico");}
            else{if(res)res.innerHTML='<strong>'+resultLabel+'</strong><br>🌶️ '+player.name+' perd la Pièce Mexico.';tfSpeak(player.name+" perd la Pièce Mexico");}
            renderGame();setTimeout(function(){closeModal();done()},1500);
          });
        },700);
      });
      return;
    }
    openModal("🪙 Pièce Mexico",tfBuildWheelCoinHTML(player.name),function(){var buttons=document.querySelectorAll("#modalBody [data-wheel-coin]"),settled=false;buttons.forEach(function(btn){btn.addEventListener("click",function(){if(settled)return;settled=true;buttons.forEach(function(b){b.disabled=true;b.classList.toggle("active",b===btn)});var choice=btn.dataset.wheelCoin,result=Math.random()<.5?"tortilla":"piment",res=document.getElementById("tfWheelCoinResult");res.textContent="🪙 La pièce tourne…";tfAnimateCoin(document.getElementById("tfWheelCoin"),result,function(){if(choice===result){var g=tfGiveRandomIngredient(player);res.innerHTML="🎉 <strong>Gagné !</strong> +1 "+g.emoji+" "+g.label;tfSpeak("Gagné, ingrédient bonus")}else{res.innerHTML="🌶️ <strong>Perdu !</strong> Aucun bonus cette fois.";tfSpeak("Perdu, aucun bonus")}setTimeout(function(){closeModal();renderGame();done()},1200)})})})})
  }

  function tfMemoryDeck()'''
s,n=coin_re.subn(coin_new,s,count=1)
if n!=1: raise SystemExit('ERROR V8.2: tfRunWheelCoin block not found')

mem_re=re.compile(r'''  function tfRunMemory\(playerIdx,done\)\{.*?\n\n  /\* ---------- Coup de Piment resolution ---------- \*/''',re.S)
mem_new=r'''  function tfRunMemory(playerIdx,done){
    var player=game.players[playerIdx];
    if(player.isAI){
      var success=Math.random()<.68;
      openModal("🤖 Mémoire Mexico — tour de l’IA",tfBuildMemoryHTML(),function(){
        var st=window.tfMemoryRound,cards=document.querySelectorAll("#modalBody .tf-memory-card"),groups={};
        st.deck.forEach(function(c,i){(groups[c.key]=groups[c.key]||[]).push(i)});
        var pairs=Object.keys(groups).map(function(k){return groups[k]}),target=success?3:2,shown=0;
        var res=document.getElementById("tfMemoryResult");
        if(res)res.textContent="🤖 "+player.name+" mémorise les cartes…";
        function showNext(){
          if(shown>=target){
            if(success){var g=tfGiveRandomIngredient(player);if(res)res.innerHTML="🎉 <strong>3 paires !</strong><br>🤖 "+player.name+" gagne +1 "+g.emoji+" "+g.label;tfSpeak(player.name+" trouve trois paires");}
            else{if(res)res.innerHTML="🌶️ <strong>2 paires seulement.</strong><br>🤖 "+player.name+" rate Mémoire Mexico.";tfSpeak(player.name+" rate le défi mémoire");}
            renderGame();setTimeout(function(){closeModal();done()},1600);return;
          }
          var pair=pairs[shown],a=pair[0],b=pair[1];
          cards[a].classList.add("open");
          setTimeout(function(){cards[b].classList.add("open");setTimeout(function(){cards[a].classList.add("matched");cards[b].classList.add("matched");shown++;if(res)res.textContent=shown+"/3 paires trouvées par "+player.name;setTimeout(showNext,450)},420)},320);
        }
        setTimeout(showNext,650);
      });
      return;
    }
    openModal("🃏 Mémoire Mexico",tfBuildMemoryHTML(),function(){var st=window.tfMemoryRound,cards=document.querySelectorAll("#modalBody .tf-memory-card");function finish(success){st.busy=true;cards.forEach(function(c){c.disabled=true});var res=document.getElementById("tfMemoryResult");if(success){var g=tfGiveRandomIngredient(player);res.innerHTML="🎉 <strong>3 paires trouvées !</strong><br>+1 "+g.emoji+" "+g.label;tfSpeak("Trois paires trouvées, ingrédient bonus")}else{res.innerHTML="🌶️ <strong>Défi raté.</strong> Il fallait 3 paires en 7 essais.";tfSpeak("Défi mémoire raté")}setTimeout(function(){closeModal();renderGame();done()},1400)}cards.forEach(function(card){card.addEventListener("click",function(){if(st.busy||card.classList.contains("matched")||card.classList.contains("open"))return;var idx=Number(card.dataset.memoryIndex);card.classList.add("open");st.open.push(idx);if(st.open.length<2)return;st.busy=true;st.attempts++;var a=st.open[0],b=st.open[1],same=st.deck[a].key===st.deck[b].key;setTimeout(function(){if(same){cards[a].classList.add("matched");cards[b].classList.add("matched");st.pairs++}else{cards[a].classList.remove("open");cards[b].classList.remove("open")}st.open=[];st.busy=false;var score=document.getElementById("tfMemoryScore");if(score)score.textContent=st.pairs+"/3 paires • "+st.attempts+"/7 essais";if(st.pairs>=3)finish(true);else if(st.attempts>=7)finish(false)},650)})})})
  }

  /* ---------- Coup de Piment resolution ---------- */'''
s,n=mem_re.subn(mem_new,s,count=1)
if n!=1: raise SystemExit('ERROR V8.2: tfRunMemory block not found')

ai_re=re.compile(r'''  function runAiTurn\(\)\{.*?\n  \}\n\n  function handleSpinResult\(idx\)\{''',re.S)
ai_new=r'''  function runAiTurn(){
    var gw=document.getElementById("gameWheel"),wheelBox=document.getElementById("wheelStickyBox"),thinking=document.getElementById("aiThinking"),aiPlayer=game&&game.players?game.players[game.turn]:null,mainEl=document.querySelector("main");
    if(wheelBox){wheelBox.classList.remove("collapsed");wheelBox.classList.add("tf-ai-spinning","tf-ai-showcase");}
    if(thinking){thinking.classList.add("tf-ai-visible");thinking.textContent="🤖 "+(aiPlayer?aiPlayer.name:"L’IA")+" va tourner la roue…";}
    var flip=document.getElementById("drawFlipCard");if(flip)flip.classList.remove("flipped");
    var rt=document.getElementById("gameWheelResultText");if(rt)rt.innerHTML='<div class="tf-ai-result">🤖 Tour de '+(aiPlayer?aiPlayer.name:"l’IA")+' : regarde la roue !</div>';
    if(mainEl&&wheelBox){var mr=mainEl.getBoundingClientRect(),wr=wheelBox.getBoundingClientRect(),target=mainEl.scrollTop+(wr.top-mr.top)-8;try{mainEl.scrollTo({top:Math.max(0,target),behavior:"smooth"})}catch(e){mainEl.scrollTop=Math.max(0,target)}}
    showToast("🤖 "+(aiPlayer?aiPlayer.name:"L’IA")+" tourne la roue…",2500);tfSpeak((aiPlayer?aiPlayer.name:"L'intelligence artificielle")+" tourne la roue");
    setTimeout(function(){
      spinWheelEl(gw,gameWheelState,function(idx){
        var seg=segments[idx],emoji=document.getElementById("flipEmoji"),label=document.getElementById("flipLabel"),card=document.getElementById("drawFlipCard"),resultText=document.getElementById("gameWheelResultText");
        if(emoji)emoji.textContent=seg.emoji;if(label)label.textContent=seg.name.split(" / ")[0];if(card)card.classList.add("flipped");
        if(resultText)resultText.innerHTML='<div class="tf-ai-result">🤖 '+(aiPlayer?aiPlayer.name:"L’IA")+' obtient '+seg.emoji+' <strong>'+seg.name.split(" / ")[0]+'</strong></div>';
        if(thinking){thinking.textContent="🤖 Résultat : "+seg.name.split(" / ")[0];}
        if(wheelBox)wheelBox.classList.remove("tf-ai-spinning");
        setTimeout(function(){if(wheelBox)wheelBox.classList.remove("tf-ai-showcase");if(thinking){thinking.classList.remove("tf-ai-visible");thinking.textContent="";}handleSpinResult(idx)},1350);
      },document.getElementById("gameWheelLights"));
    },900);
  }

  function handleSpinResult(idx){'''
s,n=ai_re.subn(ai_new,s,count=1)
if n!=1: raise SystemExit('ERROR V8.2: runAiTurn block not found')

required=['tf-v82-visibility','aria-label="Légende de la roue"','tour de l’IA','tfAiWheelCoin','Mémoire Mexico — tour de l’IA','function handleSpinResult(idx)','function tfRunMemory(','function tfRunWheelCoin(']
missing=[x for x in required if x not in s]
if missing: raise SystemExit('ERROR V8.2 validation: '+', '.join(missing))

p.write_text(s,encoding='utf-8')
print('V8.2 visibility patch OK')
