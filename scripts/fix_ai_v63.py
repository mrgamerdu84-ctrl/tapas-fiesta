from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# Add guarded AI scheduler before afterSpinUpdate.
needle = '''  function afterSpinUpdate(){
    renderGame();
    if(game.status === "ended") return;
    var player = game.players[game.turn];
    if(player.isAI){
      setTimeout(aiTryCookThenEnd, 700);
    }
  }'''
repl = '''  var tfAiSpinTimer = null;
  var tfAiSpinWatchdog = null;
  var tfAiSpinning = false;

  function queueAiSpin(delay){
    if(!game || game.status !== "playing") return;
    var expectedTurn = game.turn;
    var player = game.players[expectedTurn];
    if(!player || !player.isAI || game.hasSpun) return;
    clearTimeout(tfAiSpinTimer);
    tfAiSpinTimer = setTimeout(function(){
      if(!game || game.status !== "playing" || game.turn !== expectedTurn) return;
      var current = game.players[game.turn];
      if(!current || !current.isAI || game.hasSpun || tfAiSpinning) return;
      runAiTurn();
    }, typeof delay === "number" ? delay : 800);
  }

  function afterSpinUpdate(){
    renderGame();
    if(game.status === "ended") return;
    var player = game.players[game.turn];
    if(player && player.isAI){
      setTimeout(aiTryCookThenEnd, 700);
    }
  }'''
if 'function queueAiSpin(' not in s:
    if needle not in s:
        raise SystemExit('ERROR: afterSpinUpdate block not found')
    s = s.replace(needle, repl, 1)

old_ai_cook = '''  function aiTryCookThenEnd(){
    if(game.status === "ended"){ renderGame(); return; }
    var player = game.players[game.turn];
    if(player.skipCook){ setTimeout(endTurn, 500); return; }'''
new_ai_cook = '''  function aiTryCookThenEnd(){
    if(!game || game.status === "ended"){ if(game) renderGame(); return; }
    var player = game.players[game.turn];
    // Ignore stale AI timers after the turn has already returned to a human.
    if(!player || !player.isAI) return;
    if(player.skipCook){ setTimeout(endTurn, 500); return; }'''
if 'Ignore stale AI timers' not in s:
    if old_ai_cook not in s:
        raise SystemExit('ERROR: aiTryCookThenEnd block not found')
    s = s.replace(old_ai_cook, new_ai_cook, 1)

old_end = '''    renderGame();
    if(game.status === "playing" && game.players[game.turn].isAI){
      showToast("🤖 Tour de " + game.players[game.turn].name + "…");
      setTimeout(runAiTurn, 800);
    }'''
new_end = '''    tfAiSpinning = false;
    clearTimeout(tfAiSpinWatchdog);
    renderGame();
    if(game.status === "playing" && game.players[game.turn].isAI){
      showToast("🤖 Tour de " + game.players[game.turn].name + "…");
      queueAiSpin(800);
    }'''
if 'queueAiSpin(800);' not in s:
    if old_end not in s:
        raise SystemExit('ERROR: endTurn AI scheduling block not found')
    s = s.replace(old_end, new_end, 1)

old_run = '''  function runAiTurn(){
    var gw = document.getElementById("gameWheel");
    spinWheelEl(gw, gameWheelState, function(idx){
      handleSpinResult(idx);
    }, document.getElementById("gameWheelLights"));
  }'''
new_run = '''  function runAiTurn(){
    if(!game || game.status !== "playing") return;
    var expectedTurn = game.turn;
    var player = game.players[expectedTurn];
    if(!player || !player.isAI || game.hasSpun || tfAiSpinning) return;

    tfAiSpinning = true;
    var thinking = document.getElementById("aiThinking");
    if(thinking){ thinking.style.display = "block"; thinking.textContent = "🤖 " + player.name + " tourne la roue…"; }

    var gw = document.getElementById("gameWheel");
    clearTimeout(tfAiSpinWatchdog);
    tfAiSpinWatchdog = setTimeout(function(){
      if(!game || game.status !== "playing" || game.turn !== expectedTurn || game.hasSpun) return;
      tfAiSpinning = false;
      showToast("🤖 " + game.players[expectedTurn].name + " reprend son tour…");
      // Last-resort AI recovery: resolve one valid segment instead of freezing the match.
      handleSpinResult(Math.floor(Math.random() * segments.length));
    }, 7000);

    spinWheelEl(gw, gameWheelState, function(idx){
      if(!game || game.status !== "playing" || game.turn !== expectedTurn) return;
      clearTimeout(tfAiSpinWatchdog);
      tfAiSpinning = false;
      handleSpinResult(idx);
    }, document.getElementById("gameWheelLights"));
  }'''
if 'Last-resort AI recovery' not in s:
    if old_run not in s:
        raise SystemExit('ERROR: runAiTurn block not found')
    s = s.replace(old_run, new_run, 1)

# Add a backup at the end of renderGame: when an AI turn is visible and no spin
# has happened yet, make sure an AI spin is queued. queueAiSpin de-duplicates timers.
render_tail = '''      document.getElementById("gameSpinBtn").disabled = game.hasSpun;
      document.getElementById("endTurnBtn").disabled = !game.hasSpun;
    }
  }

  var tfAiSpinTimer'''
render_tail_new = '''      document.getElementById("gameSpinBtn").disabled = game.hasSpun;
      document.getElementById("endTurnBtn").disabled = !game.hasSpun;
    }

    // Safety net: simply displaying an AI turn is enough to start it.
    if(current.isAI && !game.hasSpun && !tfAiSpinning){
      queueAiSpin(900);
    }
  }

  var tfAiSpinTimer'''
if 'Safety net: simply displaying an AI turn' not in s:
    if render_tail not in s:
        raise SystemExit('ERROR: renderGame tail not found')
    s = s.replace(render_tail, render_tail_new, 1)

p.write_text(s, encoding='utf-8')
print('AI V6.3 patch applied')
