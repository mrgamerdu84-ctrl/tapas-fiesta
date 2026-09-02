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

# Remove the translucent wheel overlay that made the wheel look ghosted.
old_shine = 'shine.setAttribute("fill", "url(#wheelShine-" + svgEl.id + ")");'
new_shine = 'shine.setAttribute("fill", "none"); shine.setAttribute("stroke", "rgba(255,244,214,.85)"); shine.setAttribute("stroke-width", "1");'
if old_shine in s:
    s = s.replace(old_shine, new_shine, 1)

# Rebuild from a clean skin when the workflow is run again.
for style_id in ('tf-mexican-ui-v2', 'tf-mexican-ui-v4', 'tf-mexican-ui-v5'):
    s = re.sub(r'\n?<style id="' + re.escape(style_id) + r'">.*?</style>\n?', '\n', s, flags=re.S)

css = r'''
<style id="tf-mexican-ui-v5">
:root{
  --tf-bg:#F8E8C9;
  --tf-paper:#FFF7E8;
  --tf-paper-hi:#FFFDF6;
  --tf-ink:#382318;
  --tf-muted:#786253;
  --tf-teal:#006E65;
  --tf-teal-2:#0C8176;
  --tf-teal-dark:#064F49;
  --tf-red:#D83D20;
  --tf-red-dark:#9E2C1F;
  --tf-orange:#EE751E;
  --tf-gold:#E3A72D;
  --tf-green:#6F8E31;
  --tf-purple:#7A3C8F;
  --tf-line:rgba(100,64,35,.20);
  --tf-shadow:0 13px 28px rgba(85,49,24,.14);
  --tf-shadow-sm:0 7px 16px rgba(85,49,24,.11);
}

*{box-sizing:border-box}
html{background:var(--tf-bg)}
body{
  color:var(--tf-ink)!important;
  font-family:"Trebuchet MS",system-ui,-apple-system,sans-serif!important;
  background-color:var(--tf-bg)!important;
  background-image:
    radial-gradient(circle at 8% 14%,rgba(216,61,32,.06) 0 2px,transparent 3px),
    radial-gradient(circle at 88% 22%,rgba(0,110,101,.055) 0 2px,transparent 3px),
    radial-gradient(circle at 12% 82%,rgba(111,142,49,.05) 0 3px,transparent 4px),
    linear-gradient(135deg,rgba(228,167,45,.045) 25%,transparent 25% 75%,rgba(228,167,45,.045) 75%),
    linear-gradient(45deg,rgba(0,110,101,.035) 25%,transparent 25% 75%,rgba(0,110,101,.035) 75%),
    linear-gradient(180deg,#FFF3DA 0%,#F9EBCF 56%,#F3DFC0 100%)!important;
  background-size:70px 70px,86px 86px,96px 96px,84px 84px,84px 84px,100% 100%!important;
}

/* Header: papel picado + Talavera-inspired trim */
.appbar{
  position:relative!important;
  min-height:136px!important;
  padding:29px 64px 24px 74px!important;
  overflow:hidden!important;
  background:
    radial-gradient(circle at 92% 5%,rgba(255,255,255,.07),transparent 28%),
    linear-gradient(120deg,#045B55 0%,#00776C 54%,#075F58 100%)!important;
  border:0!important;
  box-shadow:0 8px 22px rgba(19,66,59,.22)!important;
}
.appbar::before{
  content:"";position:absolute;z-index:0;left:-5px;top:-2px;width:205px;height:47px;opacity:.94;
  background:
    linear-gradient(135deg,transparent 0 43%,#E89A20 44% 100%) 0 0/43px 42px no-repeat,
    linear-gradient(135deg,transparent 0 43%,#1B9A8E 44% 100%) 43px 4px/43px 42px no-repeat,
    linear-gradient(135deg,transparent 0 43%,#8E4C9F 44% 100%) 86px 0/43px 42px no-repeat,
    linear-gradient(135deg,transparent 0 43%,#D84B25 44% 100%) 129px 5px/43px 42px no-repeat;
  transform:rotate(-4deg);transform-origin:left top;filter:drop-shadow(0 3px 2px rgba(0,0,0,.14));
}
.appbar::after{
  content:"";position:absolute;z-index:1;left:0;right:0;bottom:0;height:12px;
  background:
    radial-gradient(circle at 8px 6px,#C83924 0 2px,transparent 2.5px) 0 0/24px 12px,
    radial-gradient(circle at 16px 6px,#007D71 0 2px,transparent 2.5px) 0 0/24px 12px,
    linear-gradient(90deg,#F4D47B,#FFF2B5 18%,#E47C2C 18% 21%,#FFF2B5 21% 39%,#008075 39% 42%,#FFF2B5 42% 60%,#C63F25 60% 63%,#FFF2B5 63% 81%,#7D3D86 81% 84%,#F4D47B 84%);
  box-shadow:0 2px 0 rgba(118,64,31,.25);
}
.appbar h1{
  position:relative;z-index:2;margin:0!important;
  color:#FFF4D7!important;font-family:Georgia,"Times New Roman",serif!important;
  font-size:clamp(2rem,7.2vw,2.65rem)!important;font-weight:900!important;line-height:1!important;letter-spacing:-.035em!important;
  text-shadow:0 3px 0 #7D3825,0 5px 10px rgba(0,0,0,.23)!important;
}
.appbar .tagline{
  position:relative;z-index:2;color:#F2CE65!important;font-weight:900!important;font-size:.78rem!important;
  letter-spacing:.16em!important;text-transform:uppercase!important;margin-top:7px!important;
}
.volume-btn{
  position:absolute!important;z-index:3!important;right:14px!important;top:23px!important;width:48px!important;height:48px!important;border-radius:50%!important;
  color:#FFF7DE!important;background:linear-gradient(145deg,#0A756B,#07584F)!important;border:2px solid #E5C161!important;
  box-shadow:0 5px 12px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.2)!important;font-size:1.25rem!important;
}

main{padding-top:28px!important;padding-bottom:112px!important;}
.view{animation:tfViewIn .22s ease both}
@keyframes tfViewIn{from{opacity:.25;transform:translateY(6px)}to{opacity:1;transform:none}}

/* Typography + page ornaments */
h2.view-title{
  position:relative!important;color:var(--tf-ink)!important;font-family:Georgia,"Times New Roman",serif!important;
  font-size:clamp(1.85rem,8vw,2.55rem)!important;font-weight:900!important;line-height:1.08!important;letter-spacing:-.035em!important;
  margin:7px 6px 30px!important;text-shadow:0 1px 0 #FFF9EA!important;
}
h2.view-title::after{
  content:"✦";display:block;width:118px;height:22px;margin-top:7px;color:var(--tf-red)!important;font-size:1rem!important;letter-spacing:34px!important;
  border-bottom:2px solid var(--tf-green);line-height:18px;
}
#view-defi h2.view-title,#view-minuteur h2.view-title{text-align:center!important;margin-bottom:35px!important;}
#view-defi h2.view-title::after,#view-minuteur h2.view-title::after{margin-left:auto!important;margin-right:auto!important;letter-spacing:28px!important;}

/* Home */
.home-hero{
  position:relative!important;overflow:hidden!important;text-align:center!important;
  background:
    radial-gradient(circle at 89% 14%,rgba(218,61,32,.06),transparent 20%),
    radial-gradient(circle at 10% 84%,rgba(0,110,101,.055),transparent 22%),
    linear-gradient(145deg,#FFFDF8 0%,#FFF3DB 100%)!important;
  border:1px solid rgba(167,106,47,.25)!important;border-radius:28px!important;padding:30px 24px 26px!important;margin:4px 0 22px!important;
  box-shadow:var(--tf-shadow)!important;
}
.home-hero::before{content:"❧";position:absolute;left:15px;top:13px;color:var(--tf-teal);font-size:2.1rem;transform:rotate(-28deg);opacity:.82;}
.home-hero::after{content:"✿";position:absolute;right:20px;bottom:14px;color:var(--tf-red);font-size:1.45rem;text-shadow:-13px -8px 0 #E7A72C,10px -13px 0 #0B7C71;opacity:.85;}
.home-hero .emoji{font-size:3.2rem!important;letter-spacing:.42rem!important;margin-bottom:12px!important;filter:drop-shadow(0 6px 5px rgba(91,51,28,.16));}
.home-hero p{max-width:330px!important;margin:8px auto 0!important;color:#5A4132!important;font-family:Georgia,"Times New Roman",serif!important;font-size:1.02rem!important;font-weight:700!important;line-height:1.5!important;}

.quick-grid{gap:14px!important;margin-top:4px!important;}
.quick-card{
  position:relative!important;overflow:hidden!important;min-height:132px!important;padding:21px 13px 17px!important;
  background:linear-gradient(160deg,#FFFDF8,#FFF4DF)!important;border:1px solid rgba(127,83,44,.22)!important;border-radius:23px!important;
  box-shadow:var(--tf-shadow-sm)!important;color:var(--tf-ink)!important;transition:transform .15s ease,box-shadow .15s ease!important;
}
.quick-card::before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:var(--tf-teal);}
.quick-card::after{content:"✿";position:absolute;left:12px;bottom:7px;color:rgba(0,110,101,.42);font-size:.9rem;letter-spacing:5px;}
.quick-card:nth-child(2)::before{background:var(--tf-purple)}
.quick-card:nth-child(3)::before{background:var(--tf-red)}
.quick-card:nth-child(4)::before{background:var(--tf-orange)}
.quick-card:nth-child(5)::before{background:var(--tf-green)}
.quick-card:nth-child(2)::after{color:rgba(122,60,143,.42)}
.quick-card:nth-child(3)::after{color:rgba(216,61,32,.42)}
.quick-card:nth-child(4)::after{color:rgba(238,117,30,.42)}
.quick-card:nth-child(5)::after{color:rgba(111,142,49,.45)}
.quick-card:active{transform:translateY(2px) scale(.985)!important;box-shadow:0 4px 10px rgba(80,45,23,.10)!important;}
.quick-card .qemoji{font-size:2.5rem!important;margin-bottom:10px!important;filter:drop-shadow(0 5px 4px rgba(75,42,23,.14));}
.quick-card .qlabel{font-family:Georgia,"Times New Roman",serif!important;font-size:1.02rem!important;font-weight:800!important;line-height:1.2!important;}
.quick-card:nth-child(5){grid-column:1/-1!important;width:72%!important;justify-self:center!important;min-height:102px!important;padding:18px 20px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:15px!important;}
.quick-card:nth-child(5) .qemoji{margin:0!important;font-size:2.2rem!important;}
.goal-box{margin-top:20px!important;background:linear-gradient(100deg,#FFF5D7,#F9E6B8)!important;border:1px solid rgba(190,128,39,.30)!important;border-left:6px solid var(--tf-red)!important;border-radius:17px!important;padding:14px 15px!important;color:#664935!important;box-shadow:0 5px 12px rgba(83,47,25,.07)!important;}

/* Generic game/setup panels */
.mode-card,.player-setup-block,.score-row,.recipe-card,.handoff-box,.end-box,.modal-box{
  background:linear-gradient(160deg,#FFFDF8,#FFF5E5)!important;border:1px solid var(--tf-line)!important;border-radius:20px!important;box-shadow:var(--tf-shadow-sm)!important;
}
.player-setup-block h4,.mode-card h3{font-family:Georgia,"Times New Roman",serif!important;color:var(--tf-red-dark)!important;}
.name-input{background:#FFF8E8!important;border:1px solid rgba(108,71,40,.22)!important;border-radius:13px!important;}
.avatar-opt{background:#FFF4D9!important;border-radius:14px!important}.avatar-opt.selected{background:#E4F1E8!important;border-color:var(--tf-teal)!important;}
.turn-banner{background:#FFF0C5!important;border:1px solid #E0BB64!important;border-radius:15px!important;color:#843326!important;font-weight:800!important;box-shadow:0 4px 11px rgba(86,54,28,.07)!important;}
.hand-chip{background:linear-gradient(160deg,#FFFDF8,#F3F7E8)!important;border:1px solid rgba(76,125,62,.22)!important;border-radius:15px!important;}

/* Challenge / Coup de Piment */
.card-stage{max-width:370px!important;margin-top:4px!important;}
.piment-draw{
  position:relative!important;overflow:hidden!important;min-height:245px!important;padding:58px 28px 34px!important;
  background:
    radial-gradient(circle at 92% 7%,rgba(216,61,32,.055),transparent 25%),
    linear-gradient(155deg,#FFFDF8 0%,#FFF3DC 100%)!important;
  border:1px solid rgba(153,95,42,.24)!important;border-radius:27px!important;border-left:1px solid rgba(153,95,42,.24)!important;
  box-shadow:0 15px 28px rgba(84,47,24,.15)!important;
}
.piment-draw::before{content:"❧";position:absolute;left:18px;top:14px;color:var(--tf-teal);font-size:2.2rem;transform:rotate(-28deg);}
.piment-draw::after{content:"✿";position:absolute;right:20px;bottom:17px;color:var(--tf-orange);font-size:1.55rem;text-shadow:-13px -7px 0 var(--tf-green),10px -13px 0 var(--tf-red);}
.piment-draw .cat-tag{
  align-self:center!important;background:linear-gradient(180deg,#E44A25,#B92F1F)!important;border:2px solid #E8B949!important;
  box-shadow:0 4px 0 #8E281E,0 8px 14px rgba(102,42,25,.19)!important;color:#FFF6E0!important;border-radius:14px!important;
  padding:8px 18px!important;font-size:.82rem!important;font-weight:900!important;letter-spacing:.08em!important;margin-bottom:25px!important;
}
.piment-draw .cat-text{font-family:Georgia,"Times New Roman",serif!important;color:#4A3022!important;font-size:1.12rem!important;font-weight:700!important;line-height:1.55!important;text-align:center!important;}
.draw-btn{
  margin-top:22px!important;padding:18px 16px!important;border-radius:20px!important;
  background:linear-gradient(180deg,#E5512C,#C83720)!important;border:2px solid #B42E20!important;color:#FFF6E6!important;
  font-family:Georgia,"Times New Roman",serif!important;font-size:1.18rem!important;font-weight:900!important;
  box-shadow:0 6px 0 #8D2A20,0 11px 20px rgba(104,40,24,.22)!important;text-shadow:0 2px 0 rgba(93,30,20,.25)!important;
}
.draw-btn:active{transform:translateY(4px)!important;box-shadow:0 2px 0 #8D2A20,0 5px 10px rgba(104,40,24,.18)!important;}

/* Timer */
.timer-wrap{padding-top:0!important;}
.timer-presets{gap:13px!important;margin-bottom:42px!important;}
.preset-btn{
  min-width:86px!important;background:linear-gradient(180deg,#FFFDF8,#FFF4E0)!important;border:1px solid rgba(128,83,45,.22)!important;border-radius:18px!important;
  padding:10px 18px!important;color:var(--tf-ink)!important;font-family:Georgia,"Times New Roman",serif!important;font-size:1rem!important;font-weight:800!important;box-shadow:0 4px 10px rgba(84,49,27,.09)!important;
}
.preset-btn.active{background:linear-gradient(180deg,#08786D,#046158)!important;border:2px solid #D8A93B!important;color:#FFF8E4!important;box-shadow:0 4px 0 #064D47,0 7px 13px rgba(0,91,83,.18)!important;}
.timer-ring{
  width:min(62vw,250px)!important;height:min(62vw,250px)!important;margin:16px auto 42px!important;position:relative!important;border-radius:50%!important;
  background:radial-gradient(circle,#FFF8E9 0 60%,#F8E8C9 61% 100%)!important;
  box-shadow:0 0 0 11px #D9512C,0 0 0 14px #E6B64D,0 13px 28px rgba(92,45,24,.19),inset 0 0 30px rgba(199,123,50,.10)!important;
}
.timer-ring::before{content:"✿";position:absolute;z-index:4;left:50%;top:-24px;transform:translateX(-50%);color:#FFF2C9;background:#D9512C;border:2px solid #E6B64D;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;}
.timer-ring svg{position:relative!important;z-index:2!important;}
.timer-ring circle{stroke-width:7!important;}.ring-bg{stroke:#F2DDAE!important}.ring-fg{stroke:#C73F25!important;}
.timer-num{z-index:3!important;color:#3C2518!important;font-size:4.1rem!important;font-family:Georgia,"Times New Roman",serif!important;text-shadow:0 2px 0 #FFF7E3!important;}
.timer-controls{gap:16px!important;}
.timer-controls button{min-width:120px!important;border-radius:18px!important;padding:14px 21px!important;font-family:Georgia,"Times New Roman",serif!important;font-size:1.03rem!important;font-weight:900!important;border:2px solid #D8A83C!important;box-shadow:0 5px 0 rgba(94,53,29,.24),0 9px 15px rgba(80,42,23,.15)!important;}
#startTimer{background:linear-gradient(180deg,#E84E25,#C93620)!important;color:#FFF8E7!important;}
#resetTimer{background:linear-gradient(180deg,#08786D,#075C55)!important;color:#FFF8E7!important;}
.timer-controls button:active{transform:translateY(3px)!important;box-shadow:0 2px 0 rgba(94,53,29,.24),0 4px 8px rgba(80,42,23,.12)!important;}

/* Rules accordion */
#view-regles{padding-bottom:15px!important;}
#view-regles h2.view-title{margin-bottom:30px!important;}
#view-regles .acc-item{
  position:relative!important;overflow:hidden!important;background:linear-gradient(165deg,#FFFDF8,#FFF5E3)!important;
  border:1px solid rgba(137,88,43,.22)!important;border-radius:19px!important;margin-bottom:12px!important;box-shadow:0 7px 15px rgba(76,44,24,.10)!important;
}
#view-regles .acc-item::before{content:"";position:absolute;left:0;top:0;bottom:0;width:58px;background:var(--tf-teal);box-shadow:inset -1px 0 0 rgba(255,255,255,.45);}
#view-regles .acc-item:nth-of-type(2)::before{background:var(--tf-purple)}
#view-regles .acc-item:nth-of-type(3)::before{background:var(--tf-orange)}
#view-regles .acc-item:nth-of-type(4)::before{background:var(--tf-red)}
#view-regles .acc-item:nth-of-type(5)::before{background:var(--tf-green)}
#view-regles .acc-item:nth-of-type(6)::before{background:#D89516}
#view-regles .acc-item:nth-of-type(7)::before{background:#167A76}
#view-regles .acc-head{
  position:relative!important;z-index:1!important;min-height:74px!important;padding:18px 17px 18px 77px!important;background:transparent!important;
  color:#3E291D!important;font-family:Georgia,"Times New Roman",serif!important;font-size:1.08rem!important;font-weight:900!important;line-height:1.2!important;
}
#view-regles .acc-head::before{content:"✿";position:absolute;left:18px;top:50%;transform:translateY(-50%);color:#F7D66C;font-size:1.35rem;text-shadow:0 1px 0 rgba(0,0,0,.15);}
#view-regles .acc-head .chev{
  flex:0 0 38px!important;width:38px!important;height:38px!important;border-radius:50%!important;display:flex!important;align-items:center!important;justify-content:center!important;
  color:var(--tf-teal)!important;background:#FFF6DD!important;border:2px solid currentColor!important;font-family:Arial,sans-serif!important;font-size:1.55rem!important;font-weight:600!important;line-height:1!important;
  box-shadow:0 3px 8px rgba(80,45,23,.10)!important;
}
#view-regles .acc-item:nth-of-type(2) .chev{color:var(--tf-purple)!important}
#view-regles .acc-item:nth-of-type(3) .chev{color:var(--tf-orange)!important}
#view-regles .acc-item:nth-of-type(4) .chev{color:var(--tf-red)!important}
#view-regles .acc-item:nth-of-type(5) .chev{color:var(--tf-green)!important}
#view-regles .acc-item:nth-of-type(6) .chev{color:#C7830D!important}
#view-regles .acc-item:nth-of-type(7) .chev{color:#167A76!important}
#view-regles .acc-body{position:relative!important;z-index:1!important;margin-left:58px!important;color:#5A4233!important;background:rgba(255,250,238,.74)!important;font-size:.92rem!important;line-height:1.5!important;}
#view-regles .acc-item.open .acc-body{padding:0 18px 18px!important;border-top:1px dashed rgba(127,85,44,.20)!important;}
#view-regles .acc-body th{background:#F4DEAE!important;color:#5A3825!important;}
#view-regles .acc-body td{border-color:rgba(119,78,41,.14)!important;}

/* Wheel: large, opaque and ornate */
.wheel-wrap{padding-top:5px!important;}
.wheel-sticky{
  position:relative!important;top:auto!important;z-index:8!important;overflow:visible!important;
  background:
    radial-gradient(circle at 50% 40%,rgba(255,255,255,.92) 0 18%,transparent 58%),
    linear-gradient(150deg,#FFF9EB 0%,#F8E6C5 100%)!important;
  border:1px solid rgba(135,84,40,.22)!important;border-radius:30px!important;padding:23px 12px 19px!important;margin:7px 0 18px!important;
  box-shadow:0 16px 32px rgba(74,42,23,.15),inset 0 1px 0 rgba(255,255,255,.85)!important;
}
.wheel-sticky::before{content:"✿";position:absolute;left:17px;top:12px;color:var(--tf-orange);font-size:1.2rem;text-shadow:18px 4px 0 var(--tf-teal);opacity:.75;}
.wheel-sticky::after{content:"❧";position:absolute;right:16px;bottom:10px;color:var(--tf-green);font-size:1.9rem;transform:rotate(155deg);opacity:.7;}
#wheelHolderBox{width:min(80vw,330px)!important;height:min(80vw,330px)!important;margin:15px auto 22px!important;overflow:visible!important;}
#view-roue .wheel-holder{width:min(90vw,390px)!important;height:min(90vw,390px)!important;margin-left:auto!important;margin-right:auto!important;}
.wheel-holder{isolation:isolate!important;border-radius:50%!important;filter:drop-shadow(0 14px 18px rgba(64,35,22,.19));}
.wheel-lights{inset:-16px!important;z-index:1!important;background:transparent!important;}
#wheel,#gameWheel{position:relative!important;z-index:2!important;background:#FFF9E9!important;border:10px solid #E5B64A!important;outline:5px solid #7B352B!important;outline-offset:-1px!important;box-shadow:inset 0 0 0 3px #FFF8E6,inset 0 0 28px rgba(110,62,28,.11),0 10px 24px rgba(64,34,21,.22)!important;}
#gameWheel text,#wheel text{font-weight:900!important;paint-order:stroke!important;stroke:rgba(49,26,16,.23)!important;stroke-width:.24px!important;}
#gameWheel text{font-size:7.4px!important;}
.pointer{top:-14px!important;z-index:7!important;border-left-width:20px!important;border-right-width:20px!important;border-top:32px solid #A83326!important;filter:drop-shadow(0 4px 3px rgba(62,28,18,.32))!important;}
.hub{z-index:6!important;width:20%!important;height:20%!important;background:radial-gradient(circle,#FFF8E8 0 32%,#E5B64A 33% 61%,#08756B 62% 100%)!important;border:3px solid #6B3028!important;box-shadow:0 5px 12px rgba(54,28,18,.27)!important;}
.hub::after{content:"🌶️"!important;position:absolute!important;inset:0!important;display:flex!important;align-items:center!important;justify-content:center!important;font-size:clamp(15px,4vw,23px)!important;}
.bulb{width:9px!important;height:9px!important;margin:-4.5px 0 0 -4.5px!important;border:1px solid rgba(91,52,30,.22)!important;box-shadow:0 0 6px rgba(229,182,74,.86)!important;}
.wheel-sticky .spin-btn{min-width:185px!important;padding:14px 36px!important;border-radius:19px!important;background:linear-gradient(180deg,#E44A28,#C43621)!important;border:2px solid #B32C20!important;color:#FFF7E5!important;font-family:Georgia,"Times New Roman",serif!important;font-size:1.06rem!important;font-weight:900!important;box-shadow:0 6px 0 #8C291F,0 10px 18px rgba(101,39,22,.20)!important;}
.wheel-sticky .result-box{background:rgba(255,252,242,.86)!important;border:1px solid rgba(119,74,39,.15)!important;border-radius:16px!important;padding:8px 10px!important;}
.reveal-wheel-btn{color:#704735!important;font-weight:800!important;}

/* Bottom navigation */
nav.tabbar{
  left:10px!important;right:10px!important;bottom:8px!important;width:auto!important;overflow:visible!important;
  background:linear-gradient(180deg,#FFFDF8,#FFF2DA)!important;border:2px solid #B5573D!important;border-radius:24px!important;
  box-shadow:0 10px 28px rgba(65,38,22,.19),inset 0 1px 0 #FFF!important;padding:7px 5px calc(7px + env(safe-area-inset-bottom))!important;
}
nav.tabbar::before{content:"";position:absolute;left:15px;right:15px;bottom:-7px;height:8px;border-radius:0 0 10px 10px;background:repeating-linear-gradient(90deg,#08786D 0 10px,#F4CF68 10px 20px,#D84624 20px 30px,#7A3C8F 30px 40px);opacity:.85;}
.tab-btn{color:#6E5A4C!important;border-radius:16px!important;padding:7px 1px!important;font-weight:750!important;transition:transform .15s ease,background .15s ease,color .15s ease!important;}
.tab-btn .ticon{font-size:1.45rem!important;filter:drop-shadow(0 2px 2px rgba(78,43,24,.12));}
.tab-btn.active{color:#075F57!important;background:#E5F1E9!important;transform:translateY(-2px)!important;font-weight:900!important;box-shadow:inset 0 0 0 1px rgba(0,110,101,.09)!important;}

@media (max-width:380px){
  .appbar{min-height:126px!important;padding-left:62px!important;padding-right:58px!important}
  .appbar h1{font-size:1.85rem!important}
  .appbar .tagline{font-size:.66rem!important;letter-spacing:.13em!important}
  main{padding-top:23px!important}
  h2.view-title{font-size:1.85rem!important}
  .home-hero{padding:27px 18px 23px!important}
  .quick-card{min-height:118px!important;padding:18px 10px!important}
  .quick-card .qlabel{font-size:.94rem!important}
  .timer-ring{width:min(61vw,225px)!important;height:min(61vw,225px)!important}
  .timer-controls button{min-width:108px!important;padding:13px 16px!important}
  #view-regles .acc-head{font-size:1rem!important;padding-left:72px!important}
  #wheelHolderBox{width:min(82vw,290px)!important;height:min(82vw,290px)!important}
  #view-roue .wheel-holder{width:min(91vw,340px)!important;height:min(91vw,340px)!important}
}
</style>
'''

s = s.replace('</head>', css + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
print('Tapas Fiesta Mexican Fiesta UI v5 applied; functionality and wheel fix preserved')
