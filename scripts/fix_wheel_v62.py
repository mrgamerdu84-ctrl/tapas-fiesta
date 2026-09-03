from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# V6.2: replace the wheel engine itself with a fail-safe implementation.
# The completion timer is armed BEFORE audio/visual effects, so an audio or
# WebView error can never leave the game stuck on "Ca tourne...".
pattern = re.compile(
    r'  function spinWheelEl\(svgEl, state, onDone, lightsEl\)\{.*?\n  \}\n\n  var wheelEl =',
    re.S,
)

new_engine = r'''  function spinWheelEl(svgEl, state, onDone, lightsEl){
    var idx = Math.floor(Math.random() * segments.length);
    var center = idx * 60 + 30;
    var jitter = (Math.random() * 30) - 15;
    var extraSpins = 5 + Math.floor(Math.random() * 3);
    var desiredRotation = ((360 - center + jitter) % 360 + 360) % 360;
    var currentRotation = ((state.rotation % 360) + 360) % 360;
    var deltaRotation = extraSpins * 360 + ((desiredRotation - currentRotation + 360) % 360);
    var tfWheelHolder = svgEl && svgEl.closest ? svgEl.closest(".wheel-holder") : null;
    var finished = false;

    function finishWheel(){
      if(finished) return;
      finished = true;
      try{
        if(lightsEl){ lightsEl.classList.remove("spinning"); lightsEl.classList.add("idle-glow"); }
        if(tfWheelHolder) tfWheelHolder.classList.remove("tf-spinning");
      }catch(e){}
      try{
        onDone(idx);
      }catch(e){
        console.error("Tapas Fiesta wheel callback error", e);
        var gb = document.getElementById("gameSpinBtn");
        if(gb){ gb.classList.remove("tf-busy"); gb.disabled = false; gb.textContent = "🎡 Tourner la roue"; }
        var sb = document.getElementById("spinBtn");
        if(sb){ sb.classList.remove("tf-busy"); sb.disabled = false; sb.textContent = "🎡 Tourner la roue"; }
      }
    }

    // Critical watchdog: armed first, before any optional sound/effect code.
    var finishTimer = setTimeout(finishWheel, 4200);

    try{
      state.rotation += deltaRotation;
      if(svgEl){
        svgEl.style.transition = "transform 4s cubic-bezier(0.18, 0.79, 0.32, 1)";
        svgEl.style.transform = "rotate(" + state.rotation + "deg)";
      }
      if(tfWheelHolder) tfWheelHolder.classList.add("tf-spinning");
      if(lightsEl){ lightsEl.classList.remove("idle-glow"); lightsEl.classList.add("spinning"); }
    }catch(e){
      console.error("Tapas Fiesta wheel visual error", e);
    }

    // Audio is optional: it must never be able to block wheel completion.
    try{ duckMusicFor(4100); }catch(e){ console.warn("Wheel audio disabled for this spin", e); }

    // Extra WebView fallback in case a timer was delayed or interrupted.
    setTimeout(finishWheel, 5600);
  }

  var wheelEl ='''

s, count = pattern.subn(new_engine, s, count=1)
if count != 1:
    raise SystemExit('ERROR: spinWheelEl engine not found for V6.2 replacement')

# Add a separate button watchdog for the in-game wheel. This is independent
# from spinWheelEl and protects the UI if a WebView pauses/resumes strangely.
click_marker = '''    gameSpinButton.textContent = "🎡 Ça tourne…";'''
click_repl = '''    gameSpinButton.textContent = "🎡 Ça tourne…";
    clearTimeout(window.tfGameWheelUiWatchdog);
    window.tfGameWheelUiWatchdog = setTimeout(function(){
      var b = document.getElementById("gameSpinBtn");
      var holder = document.getElementById("wheelHolderBox");
      var lights = document.getElementById("gameWheelLights");
      if(holder) holder.classList.remove("tf-spinning");
      if(lights){ lights.classList.remove("spinning"); lights.classList.add("idle-glow"); }
      if(b && b.textContent.indexOf("Ça tourne") !== -1){
        b.classList.remove("tf-busy");
        b.disabled = false;
        b.textContent = "🎡 Tourner la roue";
        showToast("⚠️ La roue a été réinitialisée. Tu peux réessayer.");
      }
    }, 6500);'''
if 'window.tfGameWheelUiWatchdog' not in s:
    if click_marker not in s:
        raise SystemExit('ERROR: V6 game spin button state not found')
    s = s.replace(click_marker, click_repl, 1)

# Clear the independent UI watchdog as soon as a valid result arrives.
result_marker = '''      tfPopResult(document.getElementById("gameWheelResult"));
      gameSpinButton.classList.remove("tf-busy");'''
result_repl = '''      tfPopResult(document.getElementById("gameWheelResult"));
      clearTimeout(window.tfGameWheelUiWatchdog);
      gameSpinButton.classList.remove("tf-busy");'''
if 'clearTimeout(window.tfGameWheelUiWatchdog);\n      gameSpinButton.classList.remove' not in s:
    if result_marker not in s:
        raise SystemExit('ERROR: V6 wheel result callback not found')
    s = s.replace(result_marker, result_repl, 1)

p.write_text(s, encoding='utf-8')
print('Tapas Fiesta V6.2 wheel engine installed: hard completion watchdog + UI recovery')
