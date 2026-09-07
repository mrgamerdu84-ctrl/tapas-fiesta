from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

if 'TF_MUSIC_CONTROL_V101' in s:
    print('V10.1 music control already applied')
    raise SystemExit(0)

old = '''  var bgMusic = document.getElementById("bgMusic");
  var volumeBtn = document.getElementById("volumeBtn");
  var volumeLevels = [0.6, 0.25, 0];
  var volumeIcons = ["🔊", "🔉", "🔇"];
  var volumeIndex = 0;
  var duckTimer = null;

  function currentVolume(){ return volumeLevels[volumeIndex]; }

  function applyVolume(){
    bgMusic.volume = currentVolume();
    volumeBtn.textContent = volumeIcons[volumeIndex];
  }
  applyVolume();

  volumeBtn.addEventListener("click", function(){
    volumeIndex = (volumeIndex + 1) % volumeLevels.length;
    applyVolume();
    if(currentVolume() > 0 && bgMusic.paused) tryPlayMusic();
  });

  function tryPlayMusic(){
    if(currentVolume() <= 0) return;
    var p = bgMusic.play();
    if(p && p.catch) p.catch(function(){ /* still blocked; will retry on the next interaction */ });
  }
  // Try immediately (works if the browser allows it), then retry on the first
  // interaction of pretty much any kind — different mobile browsers/WebViews
  // fire different event types first, so we listen broadly and unlock once.
  tryPlayMusic();
  var unlockEvents = ["pointerdown", "touchstart", "mousedown", "click", "keydown"];
  function unlockAudioOnce(){
    tryPlayMusic();
    if(!bgMusic.paused){
      unlockEvents.forEach(function(ev){ document.removeEventListener(ev, unlockAudioOnce); });
    }
  }
  unlockEvents.forEach(function(ev){ document.addEventListener(ev, unlockAudioOnce, { passive: true }); });
  document.addEventListener("visibilitychange", function(){
    if(document.visibilityState === "visible") tryPlayMusic();
  });'''

new = '''  /* TF_MUSIC_CONTROL_V101 */
  var bgMusic = document.getElementById("bgMusic");
  var volumeBtn = document.getElementById("volumeBtn");
  var volumeLevels = [0.6, 0.30, 0];
  var volumeIcons = ["🔊", "🔉", "🔇"];
  var volumeLabels = ["100%", "50%", "Muet"];
  var volumeIndex = 0;
  var duckTimer = null;
  var MUSIC_KEY = "tfMusicLevelV101";

  try{
    var savedMusicIndex = parseInt(localStorage.getItem(MUSIC_KEY), 10);
    if(savedMusicIndex >= 0 && savedMusicIndex < volumeLevels.length) volumeIndex = savedMusicIndex;
  }catch(e){}

  var musicPanel = document.createElement("div");
  musicPanel.id = "tfMusicPanel";
  musicPanel.setAttribute("role", "dialog");
  musicPanel.setAttribute("aria-label", "Réglage de la musique");
  musicPanel.innerHTML =
    '<div class="tf-music-title">🎵 Musique</div>'+
    '<button type="button" data-music-index="0">🔊 100%</button>'+
    '<button type="button" data-music-index="1">🔉 50%</button>'+
    '<button type="button" data-music-index="2">🔇 Muet</button>';
  document.body.appendChild(musicPanel);

  function currentVolume(){ return volumeLevels[volumeIndex]; }

  function updateMusicButton(){
    if(!volumeBtn) return;
    volumeBtn.classList.add("tf-music-button");
    volumeBtn.setAttribute("aria-label", "Régler la musique");
    volumeBtn.setAttribute("title", "Régler ou couper la musique");
    volumeBtn.innerHTML = '<span aria-hidden="true">🎵</span><span class="tf-music-state">'+volumeLabels[volumeIndex]+'</span>';
    var options = musicPanel.querySelectorAll("button[data-music-index]");
    for(var i=0;i<options.length;i++){
      var idx = parseInt(options[i].getAttribute("data-music-index"),10);
      options[i].classList.toggle("selected", idx === volumeIndex);
    }
  }

  function rememberVolume(){
    try{ localStorage.setItem(MUSIC_KEY, String(volumeIndex)); }catch(e){}
  }

  function tryPlayMusic(){
    if(currentVolume() <= 0) return;
    bgMusic.volume = currentVolume();
    var pr = bgMusic.play();
    if(pr && pr.catch) pr.catch(function(){});
  }

  function applyVolume(fromUser){
    bgMusic.volume = currentVolume();
    if(currentVolume() <= 0){
      bgMusic.pause();
    }else if(fromUser){
      tryPlayMusic();
    }
    rememberVolume();
    updateMusicButton();
  }

  updateMusicButton();
  applyVolume(false);

  if(volumeBtn){
    volumeBtn.addEventListener("click", function(ev){
      ev.preventDefault();
      ev.stopPropagation();
      musicPanel.classList.toggle("open");
    });
  }

  musicPanel.addEventListener("click", function(ev){
    var target = ev.target.closest ? ev.target.closest("button[data-music-index]") : null;
    if(!target) return;
    var idx = parseInt(target.getAttribute("data-music-index"),10);
    if(idx >= 0 && idx < volumeLevels.length){
      volumeIndex = idx;
      applyVolume(true);
      musicPanel.classList.remove("open");
      if(typeof showToast === "function") showToast(idx === 2 ? "🔇 Musique coupée" : "🎵 Musique : "+volumeLabels[idx]);
    }
  });

  document.addEventListener("click", function(ev){
    if(!musicPanel.classList.contains("open")) return;
    if(ev.target === volumeBtn || (volumeBtn && volumeBtn.contains(ev.target)) || musicPanel.contains(ev.target)) return;
    musicPanel.classList.remove("open");
  });

  // Android/WebView: autoplay may be blocked until a real user gesture.
  tryPlayMusic();
  var unlockEvents = ["pointerdown", "touchstart", "mousedown", "click", "keydown"];
  function unlockAudioOnce(){
    if(currentVolume() <= 0) return;
    tryPlayMusic();
    if(!bgMusic.paused){
      unlockEvents.forEach(function(ev){ document.removeEventListener(ev, unlockAudioOnce); });
    }
  }
  unlockEvents.forEach(function(ev){ document.addEventListener(ev, unlockAudioOnce, { passive: true }); });
  document.addEventListener("visibilitychange", function(){
    if(document.visibilityState === "visible" && currentVolume() > 0) tryPlayMusic();
  });'''

if old not in s:
    raise SystemExit('ERROR V10.1: original music control block not found')
s = s.replace(old, new, 1)

css = '''
<style id="tf-music-control-v101-style">
#volumeBtn.tf-music-button{width:auto!important;min-width:76px!important;height:48px!important;border-radius:24px!important;padding:5px 10px!important;display:flex!important;gap:5px!important;align-items:center!important;justify-content:center!important;font-size:18px!important;white-space:nowrap!important;}
#volumeBtn.tf-music-button .tf-music-state{font-size:12px!important;font-weight:900!important;line-height:1!important;}
#tfMusicPanel{position:fixed;z-index:2147483000;top:calc(env(safe-area-inset-top) + 74px);right:12px;width:min(210px,calc(100vw - 24px));box-sizing:border-box;padding:10px;border-radius:18px;background:#fff8df;border:3px solid #d99a2b;box-shadow:0 14px 32px rgba(57,29,16,.28);display:none;}
#tfMusicPanel.open{display:block;animation:tfMusicPop .16s ease-out both;}
#tfMusicPanel .tf-music-title{font-weight:900;color:#6f2c20;text-align:center;margin:2px 0 8px;font-size:17px;}
#tfMusicPanel button{display:block;width:100%;margin:6px 0;padding:11px 12px;border:2px solid #d8a74c;border-radius:13px;background:#fffdf5;color:#553324;font-weight:900;font-size:15px;text-align:left;}
#tfMusicPanel button.selected{background:#e8f5df;border-color:#2f8f72;box-shadow:inset 0 0 0 1px #2f8f72;}
@keyframes tfMusicPop{from{opacity:0;transform:translateY(-6px) scale(.97)}to{opacity:1;transform:none}}
</style>
'''
s = s.replace('</head>', css + '\n</head>', 1)

required = (
    'TF_MUSIC_CONTROL_V101',
    'tfMusicLevelV101',
    'id = "tfMusicPanel"',
    'data-music-index="2"',
    '🔇 Muet',
    'tf-music-control-v101-style',
)
missing = [x for x in required if x not in s]
if missing:
    raise SystemExit('ERROR V10.1 music validation failed: ' + ', '.join(missing))

p.write_text(s, encoding='utf-8')
print('V10.1 music control added: visible 100% / 50% / mute + persistent setting')
