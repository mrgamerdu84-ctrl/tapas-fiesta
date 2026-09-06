from pathlib import Path
import base64
import re

html_path = Path('www/index.html')
html = html_path.read_text(encoding='utf-8')

# Official tikoWikoFamily developer splash for THIS game.
# Important: the game name TAPAS FIESTA is baked into this image so every app
# can keep the same developer mascot while remaining immediately identifiable.
asset = Path('branding/tikowiko-tapas-fiesta-splash.b64')
if not asset.exists():
    raise SystemExit('ERROR: Tapas Fiesta branded tikoWikoFamily splash asset is missing')
encoded = ''.join(asset.read_text(encoding='utf-8').split())
try:
    splash_bytes = base64.b64decode(encoded, validate=True)
except Exception as exc:
    raise SystemExit('ERROR: invalid Tapas Fiesta developer splash base64: ' + str(exc))

if not splash_bytes.startswith(b'RIFF') or b'WEBP' not in splash_bytes[:20]:
    raise SystemExit('ERROR: Tapas Fiesta developer splash is not a valid WebP image')
Path('www/tikowiko-tapas-fiesta-splash.webp').write_bytes(splash_bytes)

# The workflow already copied the approved Tapas Fiesta game splash into www/tapas-fiesta-splash.png.
if not Path('www/tapas-fiesta-splash.png').exists():
    raise SystemExit('ERROR: Tapas Fiesta game splash missing')

style_re = re.compile(r'<style id="tf-launch-splash-style">.*?</style>', re.S)
new_style = '''<style id="tf-launch-splash-style">
#tfGameSplash,#tfLaunchSplash{position:fixed;inset:0;pointer-events:none;opacity:1;transition:opacity .42s ease;background-repeat:no-repeat;background-position:center center;}
#tfGameSplash{z-index:2147483646;background-color:#F6EEDD;background-image:url("tapas-fiesta-splash.png");background-size:contain;}
#tfLaunchSplash{z-index:2147483647;background-color:#2f160f;background-image:url("tikowiko-tapas-fiesta-splash.webp");background-size:cover;}
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
    'tikowiko-tapas-fiesta-splash.webp',
    'id="tfGameSplash"',
    'id="tfLaunchSplash"',
    'hideDeveloperSplash',
    'hideGameSplash',
)
missing = [x for x in required if x not in html]
if missing:
    raise SystemExit('ERROR: developer splash validation failed: ' + ', '.join(missing))

html_path.write_text(html, encoding='utf-8')
print('tikoWikoFamily + TAPAS FIESTA developer splash added before game splash')
