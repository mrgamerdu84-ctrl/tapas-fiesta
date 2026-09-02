from pathlib import Path

p = Path('www/index.html')
s = p.read_text(encoding='utf-8')

# Fix repeated-spin math: selected logical result and visual slice stay aligned on every spin.
old_spin = '''var targetRotation = extraSpins * 360 + (360 - center) + jitter;\n    state.rotation += targetRotation;'''
new_spin = '''var desiredRotation = ((360 - center + jitter) % 360 + 360) % 360;\n    var currentRotation = ((state.rotation % 360) + 360) % 360;\n    var deltaRotation = extraSpins * 360 + ((desiredRotation - currentRotation + 360) % 360);\n    state.rotation += deltaRotation;'''
if old_spin in s:
    s = s.replace(old_spin, new_spin, 1)
elif 'var desiredRotation = ((360 - center + jitter)' not in s:
    raise SystemExit('ERROR: wheel spin code not found')

# Remove the translucent wash that made the compact wheel look faded/ghosted.
old_shine = 'shine.setAttribute("fill", "url(#wheelShine-" + svgEl.id + ")");'
new_shine = 'shine.setAttribute("fill", "none"); shine.setAttribute("stroke", "#FFE7A7"); shine.setAttribute("stroke-width", "1.2");'
if old_shine in s:
    s = s.replace(old_shine, new_shine, 1)

marker = 'id="tf-mexican-ui-v2"'
if marker not in s:
    css = r'''
<style id="tf-mexican-ui-v2">
:root{
  --masa:#FFF3D6;
  --masa-deep:#F7DFA9;
  --ink:#342016;
  --chile:#D9432E;
  --chile-deep:#A82720;
  --marigold:#F3AF32;
  --avocado:#47864A;
  --avocado-deep:#285C34;
  --clay:#B95D3E;
  --turquesa:#168C8C;
  --rosa:#B83E74;
  --cacao:#6B3B27;
  --line:rgba(83,48,28,.18);
}
html,body{background:#FFF3D6;}
body{
  background:
    radial-gradient(circle at 12% 12%, rgba(243,175,50,.18) 0 4%, transparent 4.5%),
    radial-gradient(circle at 88% 22%, rgba(22,140,140,.10) 0 5%, transparent 5.5%),
    linear-gradient(180deg,#FFF8E9 0%,#FFF1CE 55%,#FBE4B8 100%);
}
.appbar{
  background:linear-gradient(135deg,#B82324 0%,#D9432E 42%,#E96A2D 100%);
  border-bottom:4px solid #F3AF32;
  box-shadow:0 5px 18px rgba(74,28,17,.28);
  overflow:visible;
}
.appbar::after{
  content:"";position:absolute;left:0;right:0;bottom:-11px;height:11px;
  background:repeating-linear-gradient(135deg,#168C8C 0 18px,#F3AF32 18px 36px,#B83E74 36px 54px,#47864A 54px 72px);
  clip-path:polygon(0 0,100% 0,100% 35%,97% 100%,94% 35%,91% 100%,88% 35%,85% 100%,82% 35%,79% 100%,76% 35%,73% 100%,70% 35%,67% 100%,64% 35%,61% 100%,58% 35%,55% 100%,52% 35%,49% 100%,46% 35%,43% 100%,40% 35%,37% 100%,34% 35%,31% 100%,28% 35%,25% 100%,22% 35%,19% 100%,16% 35%,13% 100%,10% 35%,7% 100%,4% 35%,1% 100%);
}
.appbar h1{font-size:1.55rem;text-shadow:0 2px 0 rgba(91,25,16,.45);letter-spacing:.02em;}
.appbar .tagline{font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#FFF2C8;opacity:1;}
.volume-btn{background:rgba(255,246,214,.2);border:2px solid rgba(255,232,166,.7);}
main{padding-top:28px;}
h2.view-title{font-size:1.45rem;text-align:center;color:#8F241F;margin-bottom:18px;text-shadow:0 1px 0 #fff;position:relative;}
h2.view-title::after{content:"";display:block;width:86px;height:5px;margin:8px auto 0;border-radius:20px;background:linear-gradient(90deg,#168C8C,#F3AF32,#D9432E,#47864A);}
.home-hero{
  background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(255,244,211,.96));
  border:2px solid #EAC87C;border-radius:24px;padding:22px 18px;margin:4px 0 18px;
  box-shadow:0 10px 24px rgba(92,49,22,.12),inset 0 0 0 4px rgba(255,255,255,.55);
  position:relative;overflow:hidden;
}
.home-hero::before,.home-hero::after{position:absolute;font-size:1.7rem;opacity:.18;transform:rotate(-15deg);}
.home-hero::before{content:"🌵";left:9px;bottom:8px}.home-hero::after{content:"🌶️";right:8px;top:8px;transform:rotate(18deg)}
.home-hero .emoji{font-size:3rem;filter:drop-shadow(0 4px 4px rgba(80,45,20,.18));}
.home-hero p{color:#5A3825;font-weight:600;line-height:1.45;}
.quick-grid{gap:13px;}
.quick-card,.mode-card,.player-setup-block,.score-row,.recipe-card,.acc-item,.piment-draw,.handoff-box,.end-box{border:2px solid rgba(206,153,71,.35)!important;box-shadow:0 8px 18px rgba(82,45,22,.10)!important;}
.quick-card{border-radius:20px;padding:18px 10px;background:linear-gradient(155deg,#fff 0%,#FFF7E4 100%);position:relative;overflow:hidden;}
.quick-card::after{content:"";position:absolute;left:0;right:0;bottom:0;height:5px;background:var(--marigold);}
.quick-card:nth-child(2)::after{background:var(--turquesa)}
.quick-card:nth-child(3)::after{background:var(--chile)}
.quick-card:nth-child(4)::after{background:var(--avocado)}
.quick-card:nth-child(5)::after{background:var(--rosa)}
.quick-card .qemoji{font-size:2rem;filter:drop-shadow(0 3px 2px rgba(80,40,10,.14));}
.goal-box{border:2px dashed #D99B32;border-left:6px solid #D9432E;background:linear-gradient(90deg,#FFE9A9,#FFF3D6);border-radius:16px;padding:14px 15px;box-shadow:0 5px 12px rgba(80,40,15,.08);}
.spin-btn,.draw-btn,#startTimer,.cook-btn,.end-turn-btn{background:linear-gradient(180deg,#EF5A37,#C92F26)!important;border:2px solid #A82720!important;box-shadow:0 7px 0 #8F241F,0 12px 20px rgba(130,45,28,.25)!important;color:#fff!important;text-shadow:0 1px 0 rgba(90,20,10,.35);font-weight:800!important;}
.spin-btn:active,.draw-btn:active,.end-turn-btn:active{transform:translateY(4px) scale(.99)!important;box-shadow:0 3px 0 #8F241F,0 6px 12px rgba(130,45,28,.2)!important;}
.preset-btn.active,.avatar-opt.selected{background:#168C8C!important;border-color:#0C6C6C!important;color:#fff!important;}
.piment-draw{background:linear-gradient(145deg,#fff,#FFF0D4);border-left:7px solid #D9432E!important;}
.timer-ring{filter:drop-shadow(0 8px 8px rgba(75,37,17,.12));}.ring-fg{stroke:#D9432E}.ring-bg{stroke:#F1C96E}
.acc-item{border-radius:17px;background:rgba(255,255,255,.86);}.acc-head{color:#8F241F;}
.turn-banner{background:linear-gradient(90deg,#FFF0BD,#FFE0A0);border:1px solid #E5B34B;border-radius:14px;padding:9px;color:#A82720!important;box-shadow:0 4px 10px rgba(85,44,18,.08);}
.hand-chip{border-width:2px;background:linear-gradient(160deg,#fff,#F2F8EA);border-radius:14px;}
.recipe-card{border-radius:16px;background:linear-gradient(160deg,#fff,#FFF7E6);}
nav.tabbar{background:rgba(255,251,240,.98);border-top:3px solid #F3AF32;box-shadow:0 -8px 22px rgba(80,40,18,.14);padding-top:7px;}
.tab-btn{border-radius:12px;color:#765A44;transition:transform .16s ease,background .16s ease;}.tab-btn.active{color:#A82720;background:#FFE7A7;transform:translateY(-2px);}.tab-btn.active .ticon{filter:drop-shadow(0 2px 2px rgba(90,40,10,.18));}

/* Rebuilt wheel presentation: larger, opaque and layered correctly. */
.wheel-wrap{padding-top:10px;}
.wheel-sticky{position:relative!important;top:auto!important;z-index:8;background:linear-gradient(155deg,#FFF8E8,#FFE7AD)!important;border:2px solid #E3AE46!important;border-radius:24px;padding:18px 10px 16px!important;margin:8px 0 16px!important;box-shadow:0 10px 24px rgba(80,40,18,.14);overflow:visible!important;}
#wheelHolderBox{width:min(72vw,280px)!important;height:min(72vw,280px)!important;margin:12px auto 18px!important;overflow:visible!important;}
#view-roue .wheel-holder{width:min(84vw,340px)!important;height:min(84vw,340px)!important;}
.wheel-holder{isolation:isolate;border-radius:50%;}
.wheel-lights{inset:-13px!important;z-index:1!important;border-radius:50%;background:transparent!important;}
#wheel,#gameWheel{position:relative;z-index:2!important;background:#FFF9E9!important;border:8px solid #F3C95B!important;outline:4px solid #7E3427;outline-offset:-1px;box-shadow:0 12px 26px rgba(72,35,18,.30),inset 0 0 0 3px rgba(255,255,255,.75)!important;}
#gameWheel text{font-size:7px!important;font-weight:900!important;paint-order:stroke;stroke:rgba(50,25,12,.18);stroke-width:.25px;}#wheel text{font-weight:900!important;paint-order:stroke;stroke:rgba(50,25,12,.15);stroke-width:.2px;}
.pointer{top:-11px!important;z-index:6!important;border-left-width:18px!important;border-right-width:18px!important;border-top:29px solid #B82324!important;filter:drop-shadow(0 4px 2px rgba(65,28,16,.35))!important;}
.hub{z-index:5!important;width:19%!important;height:19%!important;background:radial-gradient(circle,#FFF9E9 0 35%,#F3C95B 36% 62%,#B82324 63% 100%)!important;border:3px solid #7E3427;box-shadow:0 4px 10px rgba(55,25,12,.32)!important;}
.hub::after{content:"🌶️";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:clamp(14px,4vw,24px);filter:drop-shadow(0 1px 1px #fff);}
.bulb{width:10px!important;height:10px!important;margin:-5px 0 0 -5px!important;box-shadow:0 0 0 2px rgba(105,52,27,.18),0 0 7px 2px currentColor!important;}
.wheel-sticky .spin-btn{font-size:1rem!important;padding:12px 36px!important;}.wheel-sticky .result-box{background:rgba(255,255,255,.58);border-radius:14px;padding:4px 8px;}.reveal-wheel-btn{color:#8F241F!important;font-size:.84rem!important;}
@media (max-width:360px){#wheelHolderBox{width:min(76vw,255px)!important;height:min(76vw,255px)!important}.quick-card{padding:15px 8px}}
</style>
'''
    s = s.replace('</head>', css + '\n</head>', 1)

p.write_text(s, encoding='utf-8')
print('Tapas Fiesta Mexican UI v2 applied; wheel alignment fixed')
