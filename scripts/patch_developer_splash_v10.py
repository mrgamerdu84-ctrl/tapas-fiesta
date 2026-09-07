from pathlib import Path
import base64
import hashlib
import re

html_path = Path('www/index.html')
html = html_path.read_text(encoding='utf-8')

# Official user-supplied tikoWikoFamily vertical artwork.
# Only resized/compressed for Android; never redrawn. The game name is HTML.
parts = [Path(f'branding/original-splash-clean/part{i:02d}.b64') for i in range(1, 5)]
missing_parts = [str(p) for p in parts if not p.exists()]
if missing_parts:
    raise SystemExit('ERROR: clean tikoWikoFamily splash chunks missing: ' + ', '.join(missing_parts))

encoded = ''.join(''.join(p.read_text(encoding='utf-8').split()) for p in parts)
try:
    splash_bytes = base64.b64decode(encoded, validate=True)
except Exception as exc:
    raise SystemExit('ERROR: invalid clean tikoWikoFamily splash base64: ' + str(exc))

expected_sha256 = 'f8b8b0143c1219e4717edecbeec48877b48b1714416ed16796c4bf823508c645'
actual_sha256 = hashlib.sha256(splash_bytes).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit('ERROR: tikoWikoFamily splash checksum mismatch: ' + actual_sha256)
if not splash_bytes.startswith(b'RIFF') or b'WEBP' not in splash_bytes[:20]:
    raise SystemExit('ERROR: clean tikoWikoFamily splash is not a valid WebP image')
Path('www/tikowiko-original-vertical-splash.webp').write_bytes(splash_bytes)

# Replace the old launch CSS with ONE startup layer only. No second splash/flicker.
style_re = re.compile(r'<style id="tf-launch-splash-style">.*?</style>', re.S)
new_style = '''<style id="tf-launch-splash-style">
#tfLaunchSplash{position:fixed;inset:0;z-index:2147483647;pointer-events:none;opacity:1;transition:opacity .35s ease;background:#0b6f66 url("tikowiko-original-vertical-splash.webp") center center/contain no-repeat;overflow:hidden;}
#tfLaunchGameName{position:absolute;left:50%;bottom:max(20px,calc(env(safe-area-inset-bottom) + 14px));transform:translateX(-50%);width:min(84vw,540px);box-sizing:border-box;padding:11px 16px;border-radius:20px;background:rgba(71,30,15,.94);border:3px solid #f4bd48;box-shadow:0 8px 24px rgba(45,17,8,.34);color:#fff5d5;text-align:center;font:900 clamp(27px,7.3vw,47px)/1 Georgia,serif;letter-spacing:.02em;text-shadow:0 2px 0 #9c2d1f;}
#tfLaunchSplash.tf-hide{opacity:0;}
</style>'''
html, n = style_re.subn(new_style, html, count=1)
if n != 1:
    raise SystemExit('ERROR: existing launch splash style block not found')

# The workflow inserts this initial splash shell before gameplay patches run.
launch_re = re.compile(r'<div id="tfLaunchSplash" aria-hidden="true"></div>\s*<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>', re.S)
new_launch = '''<!-- TF_TIKOWIKO_FAMILY_ORIGINAL_TAPAS_FIESTA_SPLASH_V101 -->
<div id="tfLaunchSplash" aria-hidden="true"><div id="tfLaunchGameName">TAPAS FIESTA!</div></div>
<script>
(function(){
  var done=false;
  function hideDeveloperSplash(){
    if(done) return; done=true;
    var el=document.getElementById('tfLaunchSplash');
    if(!el) return;
    el.classList.add('tf-hide');
    setTimeout(function(){ if(el && el.parentNode) el.parentNode.removeChild(el); },380);
  }
  window.addEventListener('load',function(){ setTimeout(hideDeveloperSplash,1950); },{once:true});
  setTimeout(hideDeveloperSplash,3200);
})();
</script>'''
html, n = launch_re.subn(new_launch, html, count=1)
if n != 1:
    raise SystemExit('ERROR: existing launch splash script block not found')

required = (
    'TF_TIKOWIKO_FAMILY_ORIGINAL_TAPAS_FIESTA_SPLASH_V101',
    'tikowiko-original-vertical-splash.webp',
    'id="tfLaunchGameName"',
    'TAPAS FIESTA!',
    'id="tfLaunchSplash"',
    'hideDeveloperSplash',
)
missing = [x for x in required if x not in html]
if missing:
    raise SystemExit('ERROR: startup splash validation failed: ' + ', '.join(missing))
if 'id="tfGameSplash"' in html or 'hideGameSplash' in html:
    raise SystemExit('ERROR: old double splash is still present')

html_path.write_text(html, encoding='utf-8')
print('V10.1 startup fixed: clean official tikoWikoFamily splash, one layer, checksum verified')
