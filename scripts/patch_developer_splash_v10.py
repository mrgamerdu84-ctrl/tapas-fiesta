from pathlib import Path
import re

html_path = Path('www/index.html')
html = html_path.read_text(encoding='utf-8')

# Build a scalable developer splash directly in the APK.
# tikoWikoFamily stays the developer brand, while TAPAS FIESTA is always visible
# so users immediately know which game they launched.
svg = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 1280" role="img" aria-label="tikoWikoFamily présente Tapas Fiesta">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d7f73"/><stop offset="0.55" stop-color="#26a886"/><stop offset="1" stop-color="#f6c45a"/></linearGradient>
  <linearGradient id="wood" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#7d3b18"/><stop offset="1" stop-color="#4b1f0e"/></linearGradient>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#321609" flood-opacity=".34"/></filter>
</defs>
<rect width="720" height="1280" fill="url(#bg)"/>
<circle cx="360" cy="430" r="285" fill="#fff4c8" opacity=".14"/>
<g opacity=".9">
  <path d="M0 70h720v74H0z" fill="#063f43"/>
  <path d="M15 70l70 74 70-74 70 74 70-74 70 74 70-74 70 74 70-74 70 74 70-74" fill="#ef4b31"/>
  <circle cx="70" cy="170" r="10" fill="#ffd15a"/><circle cx="150" cy="160" r="8" fill="#ff7958"/><circle cx="245" cy="174" r="9" fill="#ffe26d"/><circle cx="470" cy="166" r="9" fill="#ff7958"/><circle cx="590" cy="172" r="10" fill="#ffe26d"/>
</g>
<!-- red panda mascot -->
<g transform="translate(360 420)" filter="url(#shadow)">
  <ellipse cx="0" cy="128" rx="174" ry="160" fill="#c94822"/>
  <path d="M-150-70l-74-115 125 48z" fill="#c94822"/><path d="M150-70l74-115-125 48z" fill="#c94822"/>
  <path d="M-169-112l-33-51 66 25z" fill="#fff0d8"/><path d="M169-112l33-51-66 25z" fill="#fff0d8"/>
  <ellipse cx="0" cy="15" rx="166" ry="145" fill="#ed642d"/>
  <ellipse cx="-68" cy="15" rx="52" ry="70" fill="#fff1df"/><ellipse cx="68" cy="15" rx="52" ry="70" fill="#fff1df"/>
  <ellipse cx="0" cy="62" rx="78" ry="62" fill="#fff6e7"/>
  <ellipse cx="-62" cy="0" rx="21" ry="27" fill="#2b160f"/><ellipse cx="62" cy="0" rx="21" ry="27" fill="#2b160f"/>
  <circle cx="-55" cy="-9" r="6" fill="white"/><circle cx="69" cy="-9" r="6" fill="white"/>
  <ellipse cx="0" cy="44" rx="22" ry="15" fill="#402016"/>
  <path d="M-28 77q28 36 56 0" fill="none" stroke="#4a1b14" stroke-width="9" stroke-linecap="round"/>
  <path d="M-110-105q110-76 220 0l34 30q-144-42-288 0z" fill="#efd08a" stroke="#8f451b" stroke-width="8"/>
  <path d="M-98-103q98-58 196 0" fill="none" stroke="#ef442b" stroke-width="18"/>
  <path d="M-72 130l72 62 72-62-10 108H-62z" fill="#d22f25"/>
  <path d="M-22 170l22-22 22 22-22 23z" fill="#ffd05a"/>
  <path d="M-162 66q-84 42-97 104" fill="none" stroke="#6f321e" stroke-width="46" stroke-linecap="round"/>
  <path d="M162 70q79 38 94 96" fill="none" stroke="#6f321e" stroke-width="46" stroke-linecap="round"/>
</g>
<!-- developer + game title -->
<g filter="url(#shadow)">
  <rect x="70" y="720" width="580" height="158" rx="34" fill="url(#wood)" stroke="#f0a331" stroke-width="9"/>
  <text x="360" y="786" text-anchor="middle" font-family="Arial, sans-serif" font-weight="900" font-size="54" fill="#fff6dc">tikoWikoFamily</text>
  <text x="360" y="842" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="28" fill="#ffd05a">PRÉSENTE</text>
  <rect x="55" y="905" width="610" height="210" rx="42" fill="#fff3ce" stroke="#a92820" stroke-width="10"/>
  <text x="360" y="1000" text-anchor="middle" font-family="Arial, sans-serif" font-weight="1000" font-size="82" fill="#d83b27" stroke="#6d281a" stroke-width="2">TAPAS</text>
  <text x="360" y="1082" text-anchor="middle" font-family="Arial, sans-serif" font-weight="1000" font-size="82" fill="#108873" stroke="#6d281a" stroke-width="2">FIESTA!</text>
</g>
<text x="360" y="1188" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="26" fill="#4b2b18">Des jeux qui rassemblent • Créé en France 🇫🇷</text>
<circle cx="92" cy="1180" r="18" fill="#e63b2b"/><circle cx="625" cy="1192" r="18" fill="#ffd34f"/><circle cx="664" cy="1160" r="13" fill="#e63b2b"/>
</svg>'''
Path('www/tikowiko-tapas-fiesta-splash.svg').write_text(svg, encoding='utf-8')

if not Path('www/tapas-fiesta-splash.png').exists():
    raise SystemExit('ERROR: Tapas Fiesta game splash missing')

style_re = re.compile(r'<style id="tf-launch-splash-style">.*?</style>', re.S)
new_style = '''<style id="tf-launch-splash-style">
#tfGameSplash,#tfLaunchSplash{position:fixed;inset:0;pointer-events:none;opacity:1;transition:opacity .42s ease;background-repeat:no-repeat;background-position:center center;}
#tfGameSplash{z-index:2147483646;background-color:#F6EEDD;background-image:url("tapas-fiesta-splash.png");background-size:contain;}
#tfLaunchSplash{z-index:2147483647;background-color:#0d7f73;background-image:url("tikowiko-tapas-fiesta-splash.svg");background-size:cover;}
#tfGameSplash.tf-hide,#tfLaunchSplash.tf-hide{opacity:0;}
</style>'''
html, n = style_re.subn(new_style, html, count=1)
if n != 1:
    raise SystemExit('ERROR: existing launch splash style block not found')

launch_re = re.compile(r'<div id="tfLaunchSplash" aria-hidden="true"></div>\s*<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', re.S)
new_launch = '''<!-- TF_TIKOWIKO_FAMILY_TAPAS_FIESTA_SPLASH -->
<div id="tfGameSplash" aria-hidden="true"></div>
<div id="tfLaunchSplash" aria-hidden="true"></div>
<script>
(function(){
  var devDone=false, gameDone=false;
  function hideDeveloperSplash(){
    if(devDone) return; devDone=true;
    var el=document.getElementById('tfLaunchSplash');
    if(!el) return;
    el.classList.add('tf-hide');
    setTimeout(function(){ if(el && el.parentNode) el.parentNode.removeChild(el); },460);
  }
  function hideGameSplash(){
    if(gameDone) return; gameDone=true;
    var el=document.getElementById('tfGameSplash');
    if(!el) return;
    el.classList.add('tf-hide');
    setTimeout(function(){ if(el && el.parentNode) el.parentNode.removeChild(el); },460);
  }
  window.addEventListener('load',function(){
    setTimeout(hideDeveloperSplash,1750);
    setTimeout(hideGameSplash,3100);
  },{once:true});
  setTimeout(hideDeveloperSplash,2900);
  setTimeout(hideGameSplash,4400);
})();
</script>'''
html, n = launch_re.subn(new_launch, html, count=1)
if n != 1:
    raise SystemExit('ERROR: existing launch splash script block not found')

required = (
    'TF_TIKOWIKO_FAMILY_TAPAS_FIESTA_SPLASH',
    'tikowiko-tapas-fiesta-splash.svg',
    'id="tfGameSplash"',
    'id="tfLaunchSplash"',
    'hideDeveloperSplash',
    'hideGameSplash',
)
missing = [x for x in required if x not in html]
if missing:
    raise SystemExit('ERROR: developer splash validation failed: ' + ', '.join(missing))

html_path.write_text(html, encoding='utf-8')
print('tikoWikoFamily red panda + TAPAS FIESTA developer splash added before game splash')
