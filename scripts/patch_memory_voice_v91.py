from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

award_old = '''function tfAwardCompleteRecipe(i,source){var p=game.players[i],r=null;if(p.recipes.length)r=p.recipes.splice(Math.floor(Math.random()*p.recipes.length),1)[0];else if(game.deck.length)r=game.deck.pop();if(!r)return null;p.validated.push(r);if(game.deck.length)p.recipes.push(game.deck.pop());showToast("🏆 "+p.name+" gagne « "+r.name+" » !",3200);tfSpeak(p.name+" gagne une recette complète grâce à "+source);if(p.validated.length>=3){game.status="ended";game.winnerIdx=i}return r}'''
award_new = '''function tfAwardCompleteRecipe(i,source){var p=game.players[i],r=null;if(p.recipes.length)r=p.recipes.splice(Math.floor(Math.random()*p.recipes.length),1)[0];else if(game.deck.length)r=game.deck.pop();if(!r)return null;p.validated.push(r);if(game.deck.length)p.recipes.push(game.deck.pop());showToast("🏆 "+p.name+" gagne « "+r.name+" » !",3200);var phrase=source==="Mémoire Duel"?p.name+" a trouvé trois paires et gagne une recette complète.":source==="Masque Mexicain"?p.name+" obtient le Masque Mexicain et gagne une recette complète.":p.name+" gagne une recette complète grâce à "+source;tfSpeak(phrase);if(p.validated.length>=3){game.status="ended";game.winnerIdx=i;setTimeout(function(){tfSpeak(p.name+" possède trois recettes et remporte la Tapas Fiesta !")},1300)}return r}'''
if award_old not in s:
    raise SystemExit('V9.1 award function not found')
s = s.replace(award_old, award_new, 1)

lose_old = '''function tfLoseCompleteRecipe(i){var p=game.players[i];if(!p.validated.length)return{lost:null,eliminated:false};var r=p.validated.splice(Math.floor(Math.random()*p.validated.length),1)[0];game.deck=shuffle(game.deck.concat([r]));var e=p.validated.length===0;if(e){p.eliminated=true;game.status="ended";game.winnerIdx=1-i}return{lost:r,eliminated:e}}'''
lose_new = '''function tfLoseCompleteRecipe(i){var p=game.players[i];if(!p.validated.length){tfSpeak(p.name+" n'a aucune recette à perdre.");return{lost:null,eliminated:false}}var r=p.validated.splice(Math.floor(Math.random()*p.validated.length),1)[0];game.deck=shuffle(game.deck.concat([r]));var e=p.validated.length===0;if(e){p.eliminated=true;game.status="ended";game.winnerIdx=1-i;tfSpeak(p.name+" perd sa dernière recette et est éliminé.");setTimeout(function(){var w=game.players[1-i];tfSpeak(w.name+" remporte la Tapas Fiesta !")},1300)}else{tfSpeak(p.name+" perd la recette "+r.name+".")}return{lost:r,eliminated:e}}'''
if lose_old not in s:
    raise SystemExit('V9.1 lose function not found')
s = s.replace(lose_old, lose_new, 1)

cook_old = '''    if(player.validated.length >= 3){
      game.status = "ended";
      game.winnerIdx = playerIdx;
    }'''
cook_new = '''    if(player.validated.length >= 3){
      game.status = "ended";
      game.winnerIdx = playerIdx;
      setTimeout(function(){ tfSpeak(player.name + " possède trois recettes et remporte la Tapas Fiesta !"); }, 1200);
    }'''
if cook_old not in s:
    raise SystemExit('V9.1 normal victory block not found')
s = s.replace(cook_old, cook_new, 1)

mem_re = re.compile(r'''  function tfRunMemory\(starter,done\)\{.*?\n  function tfEnsureTurboPanel''', re.S)
mem_new = r'''  function tfRunMemory(starter,done){openModal("🃏 Mémoire Duel",tfBuildMemoryDuelHTML(starter),function(){var st=window.tfMemoryDuel,cards=document.querySelectorAll("#modalBody .tf-memory-card"),res=document.getElementById("tfMemoryResult"),turn=document.getElementById("tfMemoryTurn");st.round=1;st.roundStarter=starter;function avail(){var x=[];cards.forEach(function(c,i){if(!c.classList.contains("matched"))x.push(i)});return x}function upd(){for(var i=0;i<2;i++){var e=document.getElementById("tfMemScore"+i);if(e)e.textContent=st.scores[i]+(st.scores[i]>1?" paires":" paire")}var p=game.players[st.turn];turn.textContent="Manche "+st.round+" • "+(p.isAI?"🤖 ":"👉 ")+"Au tour de "+p.name;turn.classList.toggle("ai",p.isAI)}function reveal(i){if(st.busy||st.finished||cards[i].classList.contains("matched")||cards[i].classList.contains("open"))return false;cards[i].classList.add("open");st.seen[i]=st.deck[i].key;st.sel.push(i);return true}function finish(i){if(st.finished)return;st.finished=true;st.busy=true;cards.forEach(function(c){c.disabled=true});var r=tfAwardCompleteRecipe(i,"Mémoire Duel");res.innerHTML='🏆 <strong>'+game.players[i].name+' trouve 3 paires et gagne !</strong><br>'+(r?'Recette : '+r.name:'');setTimeout(function(){closeModal();renderGame();done()},2500)}function restartTie(){st.busy=true;st.round++;st.roundStarter=1-st.roundStarter;st.turn=st.roundStarter;st.deck=tfMemoryDeck();st.seen={};st.sel=[];st.scores=[0,0];cards.forEach(function(c,i){c.disabled=false;c.classList.remove("matched","open");var f=c.querySelector(".tf-card-front");if(f)f.textContent=tfIngredientEmoji(st.deck[i].key)});res.innerHTML='🤝 <strong>Égalité 2–2 !</strong><br>Nouvelle manche automatique…';tfSpeak("Égalité deux partout. Nouvelle manche de Mémoire Duel.");upd();setTimeout(function(){st.busy=false;res.textContent="Manche "+st.round+" : premier à 3 paires gagne la recette.";sched()},1400)}function resolve(a,b){st.busy=true;setTimeout(function(){var ok=st.deck[a].key===st.deck[b].key;if(ok){cards[a].classList.add("matched");cards[b].classList.add("matched");st.scores[st.turn]++;res.textContent="✅ Paire pour "+game.players[st.turn].name}else{cards[a].classList.remove("open");cards[b].classList.remove("open");st.turn=1-st.turn;res.textContent="❌ Raté : joueur suivant"}st.sel=[];st.busy=false;upd();if(st.scores[0]>=3)finish(0);else if(st.scores[1]>=3)finish(1);else if(avail().length===0&&st.scores[0]===2&&st.scores[1]===2)restartTie();else sched()},620)}function known(){var a=avail();for(var x=0;x<a.length;x++)for(var y=x+1;y<a.length;y++)if(st.seen[a[x]]&&st.seen[a[x]]===st.seen[a[y]])return[a[x],a[y]];return null}function rnd(ex){var a=avail().filter(function(i){return ex.indexOf(i)<0});return a.length?a[Math.floor(Math.random()*a.length)]:-1}function ai(){if(st.finished||st.busy||!game.players[st.turn].isAI)return;var p=known();if(p){reveal(p[0]);setTimeout(function(){reveal(p[1]);resolve(p[0],p[1])},430);return}var a=rnd([]);if(a<0)return;reveal(a);setTimeout(function(){var m=avail().filter(function(i){return i!==a&&st.seen[i]===st.deck[a].key}),b=m.length?m[0]:rnd([a]);if(b>=0){reveal(b);resolve(a,b)}},520)}function sched(){upd();if(game.players[st.turn].isAI)setTimeout(ai,700)}cards.forEach(function(c){c.addEventListener("click",function(){if(st.busy||st.finished||game.players[st.turn].isAI)return;var i=Number(c.dataset.memoryIndex);if(reveal(i)&&st.sel.length===2)resolve(st.sel[0],st.sel[1])})});sched()})}
  function tfEnsureTurboPanel'''
s, n = mem_re.subn(mem_new, s, count=1)
if n != 1:
    raise SystemExit('V9.1 Memory Duel function not found')

marker = '<!-- TF_V91_MEMORY_VOICE -->'
if marker not in s:
    s = s.replace('</body>', marker + '\n</body>', 1)

need = ['Égalité 2–2', 'Nouvelle manche automatique', 'st.roundStarter', 'possède trois recettes et remporte la Tapas Fiesta', 'perd sa dernière recette et est éliminé', marker]
miss = [x for x in need if x not in s]
if miss:
    raise SystemExit('V9.1 validation failed: ' + ', '.join(miss))

p.write_text(s, encoding='utf-8')
print('V9.1 Memory tie replay + voice announcements OK')
