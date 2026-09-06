from pathlib import Path
import base64
import re

html_path = Path('www/index.html')
html = html_path.read_text(encoding='utf-8')

# IMPORTANT: use the real tikoWikoFamily vertical design supplied by the user.
# The source artwork is never redrawn or edited. TAPAS FIESTA! is added only as
# an HTML overlay so future games can reuse the same developer artwork safely.
asset = Path('branding/tikowiko-original-vertical-splash.b64')
if not asset.exists():
    raise SystemExit('ERROR: original tikoWikoFamily vertical splash asset is missing')
encoded = ''.join(asset.read_text(encoding='utf-8').split())
try:
    splash_bytes = base64.b64decode(encoded, validate=True)
except Exception as exc:
    raise SystemExit('ERROR: invalid original tikoWikoFamily splash base64: ' + str(exc))

if not splash_bytes.startswith(b'RIFF') or b'WEBP' not in splash_bytes[:20]:
    raise SystemExit('ERROR: original tikoWikoFamily splash is not a valid WebP image')
Path('www/tikowiko-original-vertical-splash.webp').write_bytes(splash_bytes)

if not Path('www/tapas-fiesta-splash.png').exists():
    raise SystemExit('ERROR: Tapas Fiesta game splash missing')

style_re = re.compile(r'<style id="tf-launch-splash-style">.*?</style>', re.S)
new_style = '''<style id="tf-launch-splash-style">
#tfGameSplash,#tfLaunchSplash{position:fixed;inset:0;pointer-events:none;opacity:1;transition:opacity .42s ease;background-repeat:no-repeat;background-position:center center;}
#tfGameSplash{z-index:2147483646;background-color:#F6EEDD;background-image:url("tapas-fiesta-splash.png");background-size:contain;}
#tfLaunchSplash{z-index:2147483647;background-color:#0b6f66;background-image:url("tikowiko-original-vertical-splash.webp");background-size:contain;overflow:hidden;}
#tfLaunchGameName{position:absolute;left:50%;bottom:max(22px,calc(env(safe-area-inset-bottom) + 16px));transform:translateX(-50%);width:min(82vw,540px);box-sizing:border-box;padding:12px 18px;border-radius:22px;background:rgba(71,30,15,.94);border:3px solid #f4bd48;box-shadow:0 8px 24px rgba(45,17,8,.35);color:#fff5d5;text-align:center;font:900 clamp(28px,7.7vw,48px)/1 Georgia,serif;letter-spacing:.02em;text-shadow:0 2px 0 #9c2d1f;}
#tfGameSplash.tf-hide,#tfLaunchSplash.tf-hide{opacity:0;}
</style>'''
html, n = style_re.subn(new_style, html, count=1)
if n != 1:
    raise SystemExit('ERROR: existing launch splash style block not found')

launch_re = re.compile(r'<div id="tfLaunchSplash" aria-hidden="true"></div>\s*<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', re.S)
new_launch = '''<!-- TF_TIKOWIKO_FAMILY_ORIGINAL_TAPAS_FIESTA_SPLASH -->
<div id="tfGameSplash" aria-hidden="true"></div>
<div id="tfLaunchSplash" aria-hidden="true"><div id="tfLaunchGameName">TAPAS FIESTA!</div></div>
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
    setTimeout(hideDeveloperSplash,1900);
    setTimeout(hideGameSplash,3250);
  },{once:true});
  setTimeout(hideDeveloperSplash,3100);
  setTimeout(hideGameSplash,4550);
})();
</script>'''
html, n = launch_re.subn(new_launch, html, count=1)
if n != 1:
    raise SystemExit('ERROR: existing launch splash script block not found')

required = (
    'TF_TIKOWIKO_FAMILY_ORIGINAL_TAPAS_FIESTA_SPLASH',
    'tikowiko-original-vertical-splash.webp',
    'id="tfLaunchGameName"',
    'TAPAS FIESTA!',
    'id="tfGameSplash"',
    'id="tfLaunchSplash"',
    'hideDeveloperSplash',
    'hideGameSplash',
)
missing = [x for x in required if x not in html]
if missing:
    raise SystemExit('ERROR: original developer splash validation failed: ' + ', '.join(missing))

html_path.write_text(html, encoding='utf-8')
print('Original tikoWikoFamily design preserved; TAPAS FIESTA added only as overlay')
