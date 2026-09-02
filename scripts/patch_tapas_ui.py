from pathlib import Path
import re

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# Keep the wheel result and the slice under the pointer aligned after every spin.
old_spin = '''var targetRotation = extraSpins * 360 + (360 - center) + jitter;\n    state.rotation += targetRotation;'''
new_spin = '''var desiredRotation = ((360 - center + jitter) % 360 + 360) % 360;\n    var currentRotation = ((state.rotation % 360) + 360) % 360;\n    var deltaRotation = extraSpins * 360 + ((desiredRotation - currentRotation + 360) % 360);\n    state.rotation += deltaRotation;'''
if old_spin in s:
    s = s.replace(old_spin, new_spin, 1)
elif 'var desiredRotation = ((360 - center + jitter)' not in s:
    raise SystemExit('ERROR: wheel spin code not found')

# Remove the translucent glass layer that washed out the wheel.
old_shine = 'shine.setAttribute("fill", "url(#wheelShine-" + svgEl.id + ")");'
new_shine = 'shine.setAttribute("fill", "none"); shine.setAttribute("stroke", "rgba(255,244,214,.82)"); shine.setAttribute("stroke-width", "1");'
if old_shine in s:
    s = s.replace(old_shine, new_shine, 1)

# Remove an older injected skin when rebuilding an already-patched page.
s = re.sub(r'\n?<style id="tf-mexican-ui-v2">.*?</style>\n?', '\n', s, flags=re.S)
s = re.sub(r'\n?<style id="tf-mexican-ui-v4">.*?</style>\n?', '\n', s, flags=re.S)

css = r'''
<style id="tf-mexican-ui-v4">
:root{
  --tf-cream:#F6EEDC;
  --tf-paper:#FFFDF7;
  --tf-paper-2:#FFF8E9;
  --tf-ink:#2D241E;
  --tf-muted:#756255;
  --tf-terracotta:#C65235;
  --tf-terracotta-dark:#8E3428;
  --tf-jade:#177A70;
  --tf-jade-dark:#0D544F;
  --tf-gold:#E6A62E;
  --tf-gold-soft:#F5D98D;
  --tf-wine:#7C2C35;
  --tf-line:rgba(86,57,37,.16);
  --tf-shadow:0 12px 30px rgba(70,42,25,.12);
  --tf-shadow-soft:0 6px 16px rgba(70,42,25,.09);
}

*{box-sizing:border-box}
html{background:var(--tf-cream)}
body{
  color:var(--tf-ink)!important;
  background-color:var(--tf-cream)!important;
  background-image:
    linear-gradient(30deg,rgba(23,122,112,.035) 12%,transparent 12.5%,transparent 87%,rgba(23,122,112,.035) 87.5%),
    linear-gradient(150deg,rgba(198,82,53,.035) 12%,transparent 12.5%,transparent 87%,rgba(198,82,53,.035) 87.5%),
    linear-gradient(30deg,rgba(230,166,46,.028) 12%,transparent 12.5%,transparent 87%,rgba(230,166,46,.028) 87.5%),
    linear-gradient(150deg,rgba(124,44,53,.025) 12%,transparent 12.5%,transparent 87%,rgba(124,44,53,.025) 87.5%),
    linear-gradient(180deg,#FBF6EB 0%,#F6EEDC 58%,#F2E3C9 100%)!important;
  background-size:56px 96px,56px 96px,56px 96px,56px 96px,100% 100%!important;
  font-family:ui-rounded,"Avenir Next","Trebuchet MS",system-ui,-apple-system,sans-serif!important;
}

/* Header: calm, premium, strongly branded. */
.appbar{
  position:relative!important;
  overflow:hidden!important;
  background:
    radial-gradient(circle at 14% 10%,rgba(255,255,255,.14),transparent 28%),
    linear-gradient(118deg,#0E5A53 0%,#14786D 52%,#0D5E58 100%)!important;
  border-bottom:0!important;
  box-shadow:0 8px 24px rgba(22,63,54,.24)!important;
  padding-bottom:14px!important;
}
.appbar::before{
  content:"";position:absolute;left:0;right:0;bottom:0;height:7px;
  background:linear-gradient(90deg,var(--tf-gold) 0 22%,var(--tf-terracotta) 22% 44%,#F2D071 44% 62%,var(--tf-wine) 62% 78%,var(--tf-gold) 78% 100%);
}
.appbar::after{
  content:"";position:absolute;right:-38px;top:-54px;width:150px;height:150px;border:18px solid rgba(255,244,213,.08);border-radius:50%;box-shadow:0 0 0 16px rgba(255,244,213,.04);
}
.appbar h1{
  color:#FFF8E8!important;font-size:1.58rem!important;font-weight:900!important;letter-spacing:.01em!important;
  text-shadow:0 2px 0 rgba(0,0,0,.16)!important;
}
.appbar .tagline{color:#EDE5C9!important;opacity:.95!important;font-size:.72rem!important;font-weight:800!important;letter-spacing:.12em!important;text-transform:uppercase!important;}
.volume-btn{background:rgba(255,255,255,.11)!important;border:1px solid rgba(255,246,219,.38)!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.12)!important;}

main{padding-top:22px!important;padding-bottom:100px!important;}
.view{animation:tfViewIn .22s ease both}
@keyframes tfViewIn{from{opacity:.2;transform:translateY(5px)}to{opacity:1;transform:none}}

h2.view-title{
  color:#3B3027!important;font-size:1.42rem!important;font-weight:900!important;text-align:left!important;margin:4px 4px 18px!important;letter-spacing:-.02em!important;text-shadow:none!important;
}
h2.view-title::after{content:"";display:block;width:54px;height:4px;border-radius:99px;margin-top:7px;background:linear-gradient(90deg,var(--tf-terracotta),var(--tf-gold))!important;}

/* Home hero: less toy-like, more like a real casual game landing card. */
.home-hero{
  position:relative!important;overflow:hidden!important;
  background:
    radial-gradient(circle at 88% 15%,rgba(230,166,46,.20),transparent 28%),
    radial-gradient(circle at 6% 92%,rgba(23,122,112,.12),transparent 27%),
    linear-gradient(145deg,#FFFDF8 0%,#FFF7E7 100%)!important;
  border:1px solid rgba(139,91,47,.18)!important;border-radius:26px!important;padding:24px 20px 22px!important;margin:4px 0 18px!important;
  box-shadow:var(--tf-shadow)!important;
}
.home-hero::before{
  content:"";position:absolute;inset:8px;border:1px solid rgba(198,82,53,.14);border-radius:20px;pointer-events:none;
}
.home-hero::after{
  content:"";position:absolute;right:-36px;bottom:-42px;width:130px;height:130px;border:16px double rgba(198,82,53,.09);border-radius:50%;pointer-events:none;
}
.home-hero .emoji{font-size:2.8rem!important;filter:drop-shadow(0 5px 7px rgba(76,42,23,.13));}
.home-hero p{color:#5E4B3F!important;font-weight:650!important;line-height:1.5!important;}

.quick-grid{gap:12px!important;}
.quick-card,.mode-card,.player-setup-block,.score-row,.recipe-card,.acc-item,.piment-draw,.handoff-box,.end-box{
  background:linear-gradient(165deg,#FFFDF8 0%,#FFF9ED 100%)!important;
  border:1px solid var(--tf-line)!important;border-radius:20px!important;
  box-shadow:var(--tf-shadow-soft)!important;
}
.quick-card{position:relative!important;overflow:hidden!important;padding:18px 12px!important;transition:transform .15s ease,box-shadow .15s ease!important;}
.quick-card:active{transform:scale(.98)!important;box-shadow:0 3px 9px rgba(67,41,25,.08)!important;}
.quick-card::before{content:"";position:absolute;left:12px;right:12px;top:0;height:3px;border-radius:0 0 8px 8px;background:var(--tf-gold)}
.quick-card:nth-child(2)::before{background:var(--tf-jade)}
.quick-card:nth-child(3)::before{background:var(--tf-terracotta)}
.quick-card:nth-child(4)::before{background:var(--tf-wine)}
.quick-card:nth-child(5)::before{background:#B07A35}
.quick-card .qemoji{font-size:1.9rem!important;filter:drop-shadow(0 3px 4px rgba(66,37,20,.11));}

.goal-box{
  background:linear-gradient(100deg,#FFF6DC,#FCE9BD)!important;border:1px solid rgba(205,145,42,.32)!important;border-left:5px solid var(--tf-terracotta)!important;
  border-radius:17px!important;padding:15px 16px!important;box-shadow:0 4px 12px rgba(95,60,30,.07)!important;color:#5B4434!important;
}

/* Buttons: tactile without looking plastic. */
button,.btn{font-family:inherit!important;}
.spin-btn,.draw-btn,#startTimer,.cook-btn,.end-turn-btn{
  background:linear-gradient(180deg,#D96647 0%,#B94131 100%)!important;
  border:1px solid #963126!important;border-radius:16px!important;color:#FFF9EF!important;font-weight:900!important;letter-spacing:.01em!important;
  box-shadow:0 5px 0 #7F2D27,0 9px 18px rgba(113,47,34,.20)!important;text-shadow:0 1px 0 rgba(70,20,12,.24)!important;
}
.spin-btn:active,.draw-btn:active,#startTimer:active,.cook-btn:active,.end-turn-btn:active{transform:translateY(3px)!important;box-shadow:0 2px 0 #7F2D27,0 5px 10px rgba(113,47,34,.16)!important;}
.preset-btn.active,.avatar-opt.selected{background:var(--tf-jade)!important;border-color:var(--tf-jade-dark)!important;color:white!important;box-shadow:0 3px 8px rgba(23,122,112,.18)!important;}

.piment-draw{border-left:5px solid var(--tf-terracotta)!important;background:linear-gradient(150deg,#FFFDF9,#FFF2DC)!important;}
.timer-ring{filter:drop-shadow(0 8px 10px rgba(72,45,27,.11))!important}.ring-fg{stroke:var(--tf-terracotta)!important}.ring-bg{stroke:#ECD8A6!important}
.acc-item{overflow:hidden!important}.acc-head{color:#5A4133!important;font-weight:850!important;background:rgba(255,249,236,.65)!important;}
.turn-banner{background:#FFF0CB!important;border:1px solid #E3C177!important;border-radius:15px!important;padding:10px!important;color:#87352E!important;box-shadow:0 4px 11px rgba(86,54,28,.07)!important;font-weight:800!important;}
.hand-chip{background:linear-gradient(160deg,#FFFDF8,#F5F7EB)!important;border:1px solid rgba(56,112,67,.20)!important;border-radius:15px!important;}
.recipe-card{background:linear-gradient(155deg,#FFFDF9,#FFF5E5)!important;border-radius:18px!important;}

/* Wheel stage: main visual centerpiece, with no ghost image behind it. */
.wheel-wrap{padding-top:5px!important;}
.wheel-sticky{
  position:relative!important;top:auto!important;z-index:8!important;overflow:visible!important;
  background:
    radial-gradient(circle at 50% 38%,rgba(255,255,255,.92) 0 18%,transparent 55%),
    linear-gradient(150deg,#FFF9ED 0%,#F7E7C8 100%)!important;
  border:1px solid rgba(120,75,40,.20)!important;border-radius:28px!important;padding:22px 12px 18px!important;margin:7px 0 18px!important;
  box-shadow:0 16px 34px rgba(72,43,25,.14),inset 0 1px 0 rgba(255,255,255,.8)!important;
}
.wheel-sticky::before,.wheel-sticky::after{content:"";position:absolute;width:34px;height:34px;opacity:.42;pointer-events:none;background:linear-gradient(45deg,transparent 44%,var(--tf-terracotta) 45% 54%,transparent 55%),linear-gradient(-45deg,transparent 44%,var(--tf-jade) 45% 54%,transparent 55%);}
.wheel-sticky::before{left:11px;top:11px}.wheel-sticky::after{right:11px;bottom:11px;transform:rotate(180deg)}
#wheelHolderBox{width:min(78vw,320px)!important;height:min(78vw,320px)!important;margin:14px auto 20px!important;overflow:visible!important;}
#view-roue .wheel-holder{width:min(88vw,380px)!important;height:min(88vw,380px)!important;margin-left:auto!important;margin-right:auto!important;}
.wheel-holder{isolation:isolate!important;border-radius:50%!important;filter:drop-shadow(0 14px 18px rgba(62,34,22,.18));}
.wheel-lights{inset:-16px!important;z-index:1!important;border-radius:50%!important;background:transparent!important;}
#wheel,#gameWheel{
  position:relative!important;z-index:2!important;background:#FFFAEE!important;
  border:9px solid #E7B84A!important;outline:5px solid #7C362D!important;outline-offset:-1px!important;
  box-shadow:inset 0 0 0 3px rgba(255,255,255,.90),inset 0 0 26px rgba(112,64,30,.10),0 10px 24px rgba(63,34,22,.22)!important;
}
#gameWheel text,#wheel text{font-weight:900!important;paint-order:stroke!important;stroke:rgba(42,29,20,.24)!important;stroke-width:.23px!important;letter-spacing:.01em!important;}
#gameWheel text{font-size:7.2px!important;}
.pointer{top:-14px!important;z-index:7!important;border-left-width:19px!important;border-right-width:19px!important;border-top:31px solid #98372E!important;filter:drop-shadow(0 4px 3px rgba(61,27,18,.30))!important;}
.hub{z-index:6!important;width:20%!important;height:20%!important;background:radial-gradient(circle,#FFF9E9 0 33%,#E8B849 34% 61%,#177A70 62% 100%)!important;border:3px solid #6F322B!important;box-shadow:0 5px 12px rgba(54,28,18,.26)!important;}
.hub::after{content:"TF"!important;position:absolute!important;inset:0!important;display:flex!important;align-items:center!important;justify-content:center!important;color:#6F322B!important;font-size:clamp(12px,3.4vw,20px)!important;font-weight:950!important;letter-spacing:-.08em!important;text-shadow:0 1px 0 #FFF6D9!important;}
.bulb{width:9px!important;height:9px!important;margin:-4.5px 0 0 -4.5px!important;border:1px solid rgba(91,52,30,.22)!important;box-shadow:0 0 5px rgba(230,166,46,.72)!important;}
.wheel-sticky .spin-btn{min-width:176px!important;font-size:1.02rem!important;padding:13px 34px!important;}
.wheel-sticky .result-box{background:rgba(255,253,246,.78)!important;border:1px solid rgba(118,75,41,.13)!important;border-radius:15px!important;padding:7px 10px!important;backdrop-filter:blur(4px)!important;}
.reveal-wheel-btn{color:#6E4938!important;font-size:.82rem!important;font-weight:800!important;}

/* Navigation: clean floating game dock. */
nav.tabbar{
  left:10px!important;right:10px!important;bottom:10px!important;width:auto!important;
  background:rgba(255,253,247,.96)!important;border:1px solid rgba(91,61,41,.15)!important;border-radius:20px!important;
  box-shadow:0 9px 28px rgba(55,37,24,.18)!important;padding:6px 5px calc(6px + env(safe-area-inset-bottom))!important;
  backdrop-filter:blur(10px)!important;
}
.tab-btn{color:#7A695C!important;border-radius:14px!important;transition:transform .15s ease,background .15s ease,color .15s ease!important;}
.tab-btn.active{color:#0F635C!important;background:#E7F1EB!important;transform:translateY(-2px)!important;font-weight:850!important;}
.tab-btn.active .ticon{filter:drop-shadow(0 2px 2px rgba(23,122,112,.18))!important;}

@media (max-width:380px){
  .appbar h1{font-size:1.42rem!important}
  main{padding-top:18px!important}
  .home-hero{padding:20px 16px!important;border-radius:22px!important}
  #wheelHolderBox{width:min(80vw,286px)!important;height:min(80vw,286px)!important}
  #view-roue .wheel-holder{width:min(90vw,335px)!important;height:min(90vw,335px)!important}
  .quick-card{padding:16px 9px!important}
}
</style>
'''

s = s.replace('</head>', css + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('Tapas Fiesta premium Mexican UI v4 applied; wheel alignment preserved')
