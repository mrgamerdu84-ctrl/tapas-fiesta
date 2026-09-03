from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# V6.1: make the in-game wheel collapse deterministic after a spin.
# The V6 visual layer made the wheel feedback richer, but the board should never
# remain visually stuck on the spinning/re-spin state after the result is known.

css = r'''
<style id="tf-wheel-v61-fix">
/* Force the gameplay wheel to really disappear when the game marks it collapsed. */
#wheelStickyBox.collapsed #wheelHolderBox{
  max-height:0!important;
  height:0!important;
  min-height:0!important;
  opacity:0!important;
  margin:0 auto!important;
  padding:0!important;
  overflow:hidden!important;
  pointer-events:none!important;
  filter:none!important;
}
#wheelStickyBox.collapsed{overflow:hidden!important;}
</style>
'''
if 'id="tf-wheel-v61-fix"' not in s:
    s = s.replace('</head>', css + '\n</head>', 1)

old_game = '''      tfPopResult(document.getElementById("gameWheelResult"));
      gameSpinButton.classList.remove("tf-busy");
      handleSpinResult(idx);'''
new_game = '''      tfPopResult(document.getElementById("gameWheelResult"));
      gameSpinButton.classList.remove("tf-busy");
      gameSpinButton.textContent = "✅ Résultat obtenu";
      handleSpinResult(idx);

      // Independent UI failsafe: collapse the wheel even before the board refresh.
      // renderGame() will keep the same state once game.hasSpun is true.
      setTimeout(function(){
        var tfBox = document.getElementById("wheelStickyBox");
        var tfReveal = document.getElementById("revealWheelBtn");
        var tfButton = document.getElementById("gameSpinBtn");
        if(tfBox) tfBox.classList.add("collapsed");
        if(tfButton){
          tfButton.style.display = "none";
          tfButton.disabled = true;
          tfButton.classList.remove("tf-busy");
          tfButton.textContent = "🎡 Tourner la roue";
        }
        if(tfReveal){
          tfReveal.style.display = "block";
          tfReveal.textContent = "🎡 Revoir la roue";
        }
      }, 950);'''
if 'Independent UI failsafe: collapse the wheel' not in s:
    if old_game not in s:
        raise SystemExit('ERROR: V6 gameplay wheel callback not found')
    s = s.replace(old_game, new_game, 1)

# The standalone wheel remains reusable, but do not leave the confusing
# "Tourner encore" label: return to the normal action label after every result.
old_standalone = '      spinBtn.textContent = "Tourner encore";'
new_standalone = '      spinBtn.textContent = "🎡 Tourner la roue";'
if old_standalone in s:
    s = s.replace(old_standalone, new_standalone, 1)

p.write_text(s, encoding='utf-8')
print('Tapas Fiesta V6.1 wheel fix applied: deterministic collapse and reset')
