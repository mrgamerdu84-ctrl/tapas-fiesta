from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# ---------- Standalone Défi screen -> Pièce Mexico ----------
old_view_re = re.compile(r'''  <!-- DEFI -->\n  <section class="view" id="view-defi">.*?\n  </section>\n\n  <!-- MINUTEUR -->''', re.S)
new_view = '''  <!-- DEFI : PIECE MEXICO -->
  <section class="view" id="view-defi">
    <h2 class="view-title">Pièce Mexico</h2>
    <div class="tf-coin-card">
      <div class="tf-coin-kicker">🪙 DÉFI MEXICO</div>
      <p class="tf-coin-help">Choisis ton côté avant le lancer.</p>
      <div class="tf-coin-choice-row" id="tfCoinChoiceRow">
        <button class="tf-coin-choice active" data-side="tortilla"><span>🌮</span><b>PILE</b><small>Tortilla</small></button>
        <button class="tf-coin-choice" data-side="piment"><span>🌶️</span><b>FACE</b><small>Piment</small></button>
      </div>
      <div class="tf-mexico-coin" id="tfStandaloneCoin" aria-label="Pièce Mexico">
        <div class="tf-mexico-coin-inner">
          <div class="tf-mexico-face tf-mexico-front"><span>🌮</span><strong>PILE</strong><small>TORTILLA</small></div>
          <div class="tf-mexico-face tf-mexico-back"><span>🌶️</span><strong>FACE</strong><small>PIMENT</small></div>
        </div>
      </div>
      <button class="draw-btn" id="tfCoinLaunch">🪙 Lancer la pièce</button>
      <div class="tf-coin-result" id="tfCoinResult">Pile = Tortilla 🌮 • Face = Piment 🌶️</div>
    </div>
  </section>

  <!-- MINUTEUR -->'''
s, n = old_view_re.subn(new_view, s, count=1)
if n != 1:
    raise SystemExit('ERROR: standalone challenge view not found')

# Home + nav wording.
s = s.replace('Le compagnon de jeu de Tapas Fiesta! : fais tourner la roue, tire un Coup de Piment, chronomètre les gages.',
              'Le compagnon de jeu de Tapas Fiesta! : fais tourner la roue, lance la Pièce Mexico et cuisine tes recettes.', 1)
s = s.replace('<span class="qemoji">🌶️</span>\n        <span class="qlabel">Tirer un Coup de Piment</span>',
              '<span class="qemoji">🪙</span>\n        <span class="qlabel">Lancer la Pièce Mexico</span>', 1)
s = s.replace('<button class="tab-btn" data-view="defi"><span class="ticon">🌶️</span>Défi</button>',
              '<button class="tab-btn" data-view="defi"><span class="ticon">🪙</span>Pièce</button>', 1)
s = s.replace('<p><strong>Gages :</strong> en cas de désaccord, on relance la roue plutôt que de trancher.</p>',
              '<p><strong>Pièce Mexico :</strong> Pile = Tortilla 🌮, Face = Piment 🌶️. Le joueur défié choisit avant le lancer.</p>', 1)

# ---------- Standalone JS: replace old Coup de Piment card drawer ----------
standalone_re = re.compile(r'''  /\* ---------- Coup de Piment draw ---------- \*/.*?\n  /\* ---------- Timer ---------- \*/''', re.S)
standalone_js = r'''  /* ---------- Pièce Mexico standalone ---------- */
  var tfStandaloneChoice = "tortilla";
  var tfCoinBusy = false;
  var tfCoinChoiceBtns = document.querySelectorAll("#tfCoinChoiceRow .tf-coin-choice");
  var tfStandaloneCoin = document.getElementById("tfStandaloneCoin");
  var tfCoinLaunch = document.getElementById("tfCoinLaunch");
  var tfCoinResult = document.getElementById("tfCoinResult");

  function tfSideLabel(side){ return side === "tortilla" ? "PILE — Tortilla 🌮" : "FACE — Piment 🌶️"; }

  function tfAnimateCoin(coinEl, resultSide, done){
    if(!coinEl){ if(done) done(); return; }
    var inner = coinEl.querySelector(".tf-mexico-coin-inner");
    if(!inner){ if(done) done(); return; }
    var turns = 5 + Math.floor(Math.random()*3);
    var finalHalf = resultSide === "piment" ? 180 : 0;
    inner.style.transition = "none";
    inner.style.transform = "rotateY(0deg) rotateZ(0deg)";
    void inner.offsetWidth;
    inner.style.transition = "transform 1.55s cubic-bezier(.18,.72,.25,1)";
    inner.style.transform = "rotateY(" + (turns*360 + finalHalf) + "deg) rotateZ(" + ((Math.random()*16)-8) + "deg)";
    coinEl.classList.add("tf-coin-air");
    setTimeout(function(){
      coinEl.classList.remove("tf-coin-air");
      if(done) done();
    }, 1580);
  }

  tfCoinChoiceBtns.forEach(function(btn){
    btn.addEventListener("click", function(){
      if(tfCoinBusy) return;
      tfStandaloneChoice = btn.dataset.side;
      tfCoinChoiceBtns.forEach(function(b){ b.classList.toggle("active", b === btn); });
      tfCoinResult.textContent = "Tu choisis " + tfSideLabel(tfStandaloneChoice) + ". Lance la pièce !";
    });
  });

  tfCoinLaunch.addEventListener("click", function(){
    if(tfCoinBusy) return;
    tfCoinBusy = true;
    tfCoinLaunch.disabled = true;
    tfCoinLaunch.textContent = "🪙 La pièce tourne…";
    tfCoinResult.textContent = "Suspense…";
    var resultSide = Math.random() < 0.5 ? "tortilla" : "piment";
    tfAnimateCoin(tfStandaloneCoin, resultSide, function(){
      var win = resultSide === tfStandaloneChoice;
      tfCoinResult.innerHTML = '<strong>' + tfSideLabel(resultSide) + '</strong><br>' +
        (win ? '🎉 Gagné ! Ton choix était le bon.' : '🌶️ Perdu ! La Pièce Mexico a choisi l’autre côté.');
      tfCoinLaunch.disabled = false;
      tfCoinLaunch.textContent = "🪙 Relancer la pièce";
      tfCoinBusy = false;
    });
  });

  /* ---------- Timer ---------- */'''
s, n = standalone_re.subn(standalone_js, s, count=1)
if n != 1:
    raise SystemExit('ERROR: standalone Coup de Piment JS block not found')

# ---------- Replace physical gages with Pièce Mexico tokens (same 6/20 odds) ----------
gages_re = re.compile(r'''  var GAGES = \[.*?\n  \];\n  var COUP_BAS =''', re.S)
gages_new = '''  var GAGES = [
    "Pièce Mexico", "Pièce Mexico", "Pièce Mexico",
    "Pièce Mexico", "Pièce Mexico", "Pièce Mexico"
  ];
  var COUP_BAS ='''
s, n = gages_re.subn(gages_new, s, count=1)
if n != 1:
    raise SystemExit('ERROR: GAGES array not found')

# ---------- In-game gage branch -> Pièce Mexico duel ----------
gage_branch_re = re.compile(r'''    if\(card\.type === "gage"\)\{.*?\n      return;\n    \}\n\n    done\(\);''', re.S)
gage_branch_new = r'''    if(card.type === "gage"){
      if(defender.isAI){
        var aiChoice = Math.random() < 0.5 ? "tortilla" : "piment";
        showToast("🪙 " + defender.name + " choisit " + tfSideLabel(aiChoice) + "…");
        setTimeout(function(){
          var resultSide = Math.random() < 0.5 ? "tortilla" : "piment";
          var success = aiChoice === resultSide;
          if(!success){
            var n = penaltyFor(attackerIdx), m = "";
            for(var i=0;i<n;i++){ m = stealRandom(attacker, defender); }
            showToast("🪙 " + tfSideLabel(resultSide) + " ! 🤖 " + defender.name + " perd le duel. " + m, 3300);
          } else {
            showToast("🪙 " + tfSideLabel(resultSide) + " ! 🤖 " + defender.name + " gagne le duel.", 2800);
          }
          renderGame();
          setTimeout(done, 900);
        }, 900);
        return;
      }
      openModal("🪙 Pièce Mexico", buildMexicoCoinHTML(defender.name), function(){
        wireMexicoCoinDuel(attackerIdx, defenderIdx, done);
      });
      return;
    }

    done();'''
s, n = gage_branch_re.subn(gage_branch_new, s, count=1)
if n != 1:
    raise SystemExit('ERROR: in-game gage branch not found')

# Insert new in-game coin helpers before old buildGageHTML. Keep old helpers harmless/unreferenced.
helper_marker = '  function buildGageHTML(text){'
coin_helpers = r'''  function buildMexicoCoinHTML(defenderName){
    return '' +
      '<div class="tf-duel-title">' + defenderName + ', choisis ton côté :</div>' +
      '<div class="tf-coin-choice-row tf-modal-choices">' +
        '<button class="tf-coin-choice" data-mexico-side="tortilla"><span>🌮</span><b>PILE</b><small>Tortilla</small></button>' +
        '<button class="tf-coin-choice" data-mexico-side="piment"><span>🌶️</span><b>FACE</b><small>Piment</small></button>' +
      '</div>' +
      '<div class="tf-mexico-coin tf-modal-coin" id="tfModalCoin">' +
        '<div class="tf-mexico-coin-inner">' +
          '<div class="tf-mexico-face tf-mexico-front"><span>🌮</span><strong>PILE</strong><small>TORTILLA</small></div>' +
          '<div class="tf-mexico-face tf-mexico-back"><span>🌶️</span><strong>FACE</strong><small>PIMENT</small></div>' +
        '</div>' +
      '</div>' +
      '<div class="modal-result" id="tfMexicoDuelResult">Pile = Tortilla 🌮 • Face = Piment 🌶️</div>';
  }

  function wireMexicoCoinDuel(attackerIdx, defenderIdx, done){
    var buttons = document.querySelectorAll("#modalBody [data-mexico-side]");
    var settled = false;
    buttons.forEach(function(btn){
      btn.addEventListener("click", function(){
        if(settled) return;
        settled = true;
        buttons.forEach(function(b){ b.disabled = true; b.classList.toggle("active", b === btn); });
        var choice = btn.dataset.mexicoSide;
        var resultSide = Math.random() < 0.5 ? "tortilla" : "piment";
        var resultEl = document.getElementById("tfMexicoDuelResult");
        resultEl.textContent = "🪙 Lancer de la Pièce Mexico…";
        tfAnimateCoin(document.getElementById("tfModalCoin"), resultSide, function(){
          var success = choice === resultSide;
          if(success){
            resultEl.innerHTML = '<strong>' + tfSideLabel(resultSide) + '</strong><br>✅ Gagné ! Aucun ingrédient perdu.';
          } else {
            var attacker = game.players[attackerIdx], defender = game.players[defenderIdx];
            var n = penaltyFor(attackerIdx), m = "";
            for(var i=0;i<n;i++){ m = stealRandom(attacker, defender); }
            resultEl.innerHTML = '<strong>' + tfSideLabel(resultSide) + '</strong><br>❌ Perdu ! ' + m;
          }
          setTimeout(function(){
            closeModal();
            renderGame();
            done();
          }, 1450);
        });
      });
    });
  }

'''
if 'function buildMexicoCoinHTML(' not in s:
    if helper_marker not in s:
        raise SystemExit('ERROR: buildGageHTML marker not found')
    s = s.replace(helper_marker, coin_helpers + helper_marker, 1)

# ---------- Mexican coin CSS ----------
css = r'''
<style id="tf-mexico-coin-style">
.tf-coin-card{max-width:390px;margin:4px auto 22px;padding:24px 18px 26px;border-radius:28px;background:linear-gradient(160deg,#fffdf8,#fff0cf);border:1px solid rgba(135,82,40,.24);box-shadow:0 15px 30px rgba(77,44,25,.14);text-align:center;overflow:hidden;position:relative}
.tf-coin-card:before{content:"✦  MEXICO  ✦";position:absolute;left:0;right:0;top:0;height:7px;color:transparent;background:linear-gradient(90deg,#0b776c 0 33%,#fff0b4 33% 66%,#c53b24 66%);}
.tf-coin-kicker{font-weight:900;color:#9d3022;letter-spacing:.12em;font-size:.78rem;margin-top:5px}.tf-coin-help{font-family:Georgia,serif;font-weight:700;color:#5a3c2b;margin:8px 0 14px}
.tf-coin-choice-row{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin:10px 0 18px}.tf-coin-choice{border:2px solid rgba(101,73,48,.18);border-radius:18px;background:#fffaf0;padding:11px 8px;color:#3d281c;display:flex;flex-direction:column;align-items:center;gap:2px;box-shadow:0 5px 12px rgba(79,44,23,.07)}
.tf-coin-choice span{font-size:1.75rem}.tf-coin-choice b{font-size:.93rem}.tf-coin-choice small{font-weight:700;opacity:.7}.tf-coin-choice.active{border-color:#087267;background:#edf8ef;box-shadow:0 0 0 3px rgba(8,114,103,.10)}.tf-coin-choice:disabled{opacity:.68}
.tf-mexico-coin{width:150px;height:150px;margin:10px auto 20px;perspective:900px;filter:drop-shadow(0 13px 10px rgba(76,45,24,.22));transition:transform .25s ease}.tf-mexico-coin.tf-coin-air{animation:tfCoinHop .48s ease-in-out infinite alternate}@keyframes tfCoinHop{from{transform:translateY(5px) scale(.97)}to{transform:translateY(-16px) scale(1.035)}}
.tf-mexico-coin-inner{width:100%;height:100%;position:relative;transform-style:preserve-3d;border-radius:50%}.tf-mexico-face{position:absolute;inset:0;backface-visibility:hidden;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;border:8px double #e7b84e;box-shadow:inset 0 0 0 5px rgba(255,255,255,.42),inset 0 0 22px rgba(92,47,20,.17);font-family:Georgia,serif}
.tf-mexico-face span{font-size:2.8rem;line-height:1}.tf-mexico-face strong{font-size:1rem;margin-top:4px;letter-spacing:.08em}.tf-mexico-face small{font-size:.65rem;font-weight:900;letter-spacing:.08em}.tf-mexico-front{background:radial-gradient(circle,#fff6b8 0,#eac765 58%,#c89a36 100%);color:#3c5b26}.tf-mexico-back{transform:rotateY(180deg);background:radial-gradient(circle,#ffd7a4 0,#e77c39 57%,#b53b25 100%);color:#7b1715}
.tf-coin-result{min-height:52px;padding:11px 9px;border-radius:15px;background:#fff7e7;border:1px solid rgba(126,82,43,.17);font-weight:700;line-height:1.35;color:#53392a}.tf-duel-title{text-align:center;font-family:Georgia,serif;font-size:1.08rem;font-weight:800;margin:4px 0 12px;color:#4d3023}.tf-modal-choices{margin-top:4px}.tf-modal-coin{width:124px;height:124px;margin:8px auto 14px}.tf-modal-coin .tf-mexico-face span{font-size:2.2rem}
</style>
'''
if 'id="tf-mexico-coin-style"' not in s:
    s = s.replace('</head>', css + '\n</head>', 1)

# Version marker for CI validation.
if 'TF_MEXICO_COIN_V71' not in s:
    s = s.replace('</body>', '<!-- TF_MEXICO_COIN_V71 -->\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Tapas Fiesta V7.1 Pièce Mexico applied')
