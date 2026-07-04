#!/usr/bin/env python3
"""Build the ZILAL AL SAFA 1-minute concept animation frame-by-frame."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT="/home/ubuntu/aipark-submission"
OUT=os.path.join(ROOT,"video","frames")
os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT,f))

W,H=1920,1080
FPS=25
NAVY=(18,41,79); NAVY2=(28,58,99); ORANGE=(232,121,43); INK=(34,48,63)
WHITE=(245,248,252); MUTE=(150,170,200)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def fnt(sz,bold=True): return ImageFont.truetype(FONTB if bold else FONT,sz)

def smooth(t): return t*t*(3-2*t)
def lerp(a,b,t): return a+(b-a)*t
def clamp(v,lo,hi): return max(lo,min(hi,v))

def load(path,target_w=2600):
    im=Image.open(path).convert("RGB")
    if im.width>target_w:
        im=im.resize((target_w,int(im.height*target_w/im.width)),Image.LANCZOS)
    return im

# --- caption overlay (bottom-left scrim + title/sub) ---
_scrim=None
def scrim():
    global _scrim
    if _scrim is None:
        s=Image.new("RGBA",(W,H),(0,0,0,0))
        d=ImageDraw.Draw(s)
        for y in range(H-380,H):
            a=int(clamp((y-(H-380))/380,0,1)**1.4*220)
            d.line([(0,y),(W,y)],fill=(8,18,38,a))
        _scrim=s
    return _scrim

def draw_caption(fr,title,sub,alpha):
    if alpha<=0.01: return fr
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ov=Image.alpha_composite(ov,scrim())
    d=ImageDraw.Draw(ov)
    x=110; y=H-235
    d.rectangle([x,y+8,x+70,y+58],fill=ORANGE+(255,))
    d.text((x+92,y),title,font=fnt(60),fill=WHITE+(255,))
    if sub:
        d.text((x+92,y+82),sub,font=fnt(33,False),fill=(206,220,244,255))
    a=int(clamp(alpha,0,1)*255)
    ov.putalpha(ov.getchannel("A").point(lambda p:int(p*a/255)))
    base=fr.convert("RGBA")
    return Image.alpha_composite(base,ov).convert("RGB")

def kenburns(im,t,z0,z1,c0,c1):
    z=lerp(z0,z1,smooth(t))
    cw=im.width/z; ch=cw*9/16
    if ch>im.height:
        ch=im.height; cw=ch*16/9
    cx=lerp(c0[0],c1[0],smooth(t))*im.width
    cy=lerp(c0[1],c1[1],smooth(t))*im.height
    left=clamp(cx-cw/2,0,im.width-cw); top=clamp(cy-ch/2,0,im.height-ch)
    crop=im.crop((round(left),round(top),round(left+cw),round(top+ch)))
    return crop.resize((W,H),Image.LANCZOS)

def vignette(fr):
    v=Image.new("L",(W,H),0); d=ImageDraw.Draw(v)
    d.ellipse([-260,-260,W+260,H+260],fill=255)
    v=v.filter(ImageFilter.GaussianBlur(180))
    dark=Image.new("RGB",(W,H),(6,12,26))
    return Image.composite(fr,dark,v)

# --- title / closing cards ---
def bg_card():
    g=Image.new("RGB",(W,H),NAVY)
    d=ImageDraw.Draw(g)
    for y in range(H):
        f=y/H
        c=(int(lerp(NAVY[0],10,f)),int(lerp(NAVY[1],22,f)),int(lerp(NAVY[2],44,f)))
        d.line([(0,y),(W,y)],fill=c)
    return g

def title_card(t):
    fr=bg_card(); d=ImageDraw.Draw(fr)
    # subtle rising: content shifts up slightly
    dy=int(lerp(24,0,smooth(min(t*1.6,1))))
    d.text((W/2,H/2-70+dy),"ZILAL AL SAFA",font=fnt(120),fill=WHITE,anchor="mm")
    d.line([(W/2-260,H/2+14+dy),(W/2+260,H/2+14+dy)],fill=ORANGE,width=5)
    d.text((W/2,H/2+80+dy),"An AI-designed, self-cooling neighbourhood oasis for Al Safa Park 2",
           font=fnt(40,False),fill=(206,220,244),anchor="mm")
    d.text((W/2,H-90),"DUBAI MUNICIPALITY  ·  WORLD'S FIRST AI-POWERED PARK DESIGN CHALLENGE",
           font=fnt(24),fill=MUTE,anchor="mm")
    return fr

def problem_card(t):
    fr=bg_card(); d=ImageDraw.Draw(fr)
    d.text((W/2,H/2-120),"THE PROBLEM",font=fnt(30),fill=ORANGE,anchor="mm")
    d.text((W/2,H/2-40),"The desert heat closes the park",font=fnt(58,False),fill=WHITE,anchor="mm")
    d.text((W/2,H/2+30),"for roughly six hours a day.",font=fnt(58,False),fill=WHITE,anchor="mm")
    d.text((W/2,H/2+150),"We use AI to reclaim those lost hours.",font=fnt(46),fill=(232,180,120),anchor="mm")
    return fr

def closing_card(t):
    fr=bg_card(); d=ImageDraw.Draw(fr)
    d.text((W/2,150),"BUILT TO WIN — AND BUILT WITHIN BUDGET",font=fnt(30),fill=ORANGE,anchor="mm")
    stats=[("18\u219272%","Reliable shade over paths"),("+5.5 h","Comfortable hrs/day, summer"),
           ("\u221241%","Irrigation water demand"),("Net+","On-site solar energy")]
    n=len(stats); gap=60; bw=(W-220-(n-1)*gap)/n; y0=330; bh=250
    for i,(v,s) in enumerate(stats):
        x0=110+i*(bw+gap)
        ap=smooth(clamp((t*1.4)-i*0.12,0,1))
        yy=y0+int(lerp(40,0,ap))
        card=Image.new("RGBA",(int(bw),bh),(0,0,0,0)); cd=ImageDraw.Draw(card)
        cd.rounded_rectangle([0,0,int(bw)-1,bh-1],22,fill=(255,255,255,int(16*ap)+8),outline=(120,150,200,int(120*ap)),width=2)
        fr.paste(Image.alpha_composite(Image.new("RGBA",card.size,(0,0,0,0)),card),(int(x0),yy),card)
        dd=ImageDraw.Draw(fr)
        col=tuple(int(c) for c in (lerp(18,255,ap),lerp(41,255,ap),lerp(79,255,ap)))
        dd.text((x0+bw/2,yy+bh/2-28),v,font=fnt(64),fill=(WHITE if ap>0.5 else (120,140,175)),anchor="mm")
        dd.text((x0+bw/2,yy+bh/2+56),s,font=fnt(26,False),fill=(190,206,232) if ap>0.5 else (90,110,150),anchor="mm")
    d=ImageDraw.Draw(fr)
    d.text((W/2,H-260),"ZILAL AL SAFA",font=fnt(88),fill=WHITE,anchor="mm")
    d.line([(W/2-300,H-196),(W/2+300,H-196)],fill=ORANGE,width=4)
    d.text((W/2,H-150),"A year-round, AI-designed, self-cooling oasis  ·  delivered within AED 35 million",
           font=fnt(34,False),fill=(206,220,244),anchor="mm")
    return fr

# ---- scene definitions ----
IMG={
 "aerial":load(f"{ROOT}/assets/render_aerial.png"),
 "plan":load(f"{ROOT}/drawings/masterplan.png"),
 "majlis":load(f"{ROOT}/assets/render_majlis.png"),
 "coolloop":load(f"{ROOT}/assets/render_coolloop.png"),
 "play":load(f"{ROOT}/assets/render_play.png"),
 "night":load(f"{ROOT}/assets/render_night.png"),
}

def photo_scene(key,title,sub,z0,z1,c0,c1,plan=False):
    def render(t):
        if plan:
            im=IMG[key]
            fr=kenburns(im,t,z0,z1,c0,c1)
        else:
            fr=vignette(kenburns(IMG[key],t,z0,z1,c0,c1))
        cap=clamp((t)/0.12,0,1)*clamp((1-t)/0.10,0,1)
        cap=clamp(cap,0,1)
        return draw_caption(fr,title,sub,0.35+0.65*cap if cap>0 else 0)
    return render

SCENES=[
 (6.0, title_card),
 (5.5, problem_card),
 (7.0, photo_scene("aerial","A self-cooling oasis","AI places every path, canopy and tree where the data does the most good",1.14,1.0,(0.5,0.46),(0.5,0.5))),
 (6.5, photo_scene("plan","One idea, five moves","The Cool Loop wraps a cool, green social core",1.02,1.16,(0.5,0.5),(0.46,0.5),plan=True)),
 (7.0, photo_scene("majlis","The Majlis Grove","The shaded social heart — tuned to the 6 pm peak",1.16,1.0,(0.45,0.5),(0.55,0.52))),
 (7.0, photo_scene("coolloop","The Cool Loop","A continuous, fully-shaded ~1 km circuit",1.0,1.16,(0.5,0.5),(0.56,0.48))),
 (6.0, photo_scene("play","Adaptive, all-abilities play","Designed with the neighbouring school & health centre",1.14,1.0,(0.5,0.52),(0.48,0.5))),
 (7.0, photo_scene("night","From day to night","Solar-powered lighting keeps the park safe & alive after dark",1.16,1.0,(0.52,0.5),(0.46,0.52))),
 (7.5, closing_card),
]
OVERLAP=0.5

# build timeline with crossfades
starts=[]; tcur=0.0
for i,(dur,_) in enumerate(SCENES):
    starts.append(tcur)
    tcur+=dur-(OVERLAP if i<len(SCENES)-1 else 0)
total=tcur
print(f"total duration ~ {total:.1f}s, frames ~ {int(total*FPS)}")

def scene_frame(i,tg):
    dur,fn=SCENES[i]
    tl=clamp((tg-starts[i])/dur,0,1)
    return fn(tl)

nframes=int(total*FPS)
for f in range(nframes):
    tg=f/FPS
    # find active scene(s)
    active=[i for i in range(len(SCENES)) if starts[i]-1e-6 <= tg < starts[i]+SCENES[i][0]+1e-6]
    if not active: active=[len(SCENES)-1]
    if len(active)==1:
        img=scene_frame(active[0],tg)
    else:
        a,b=active[0],active[1]
        ov_start=starts[b]
        w=clamp((tg-ov_start)/OVERLAP,0,1)
        img=Image.blend(scene_frame(a,tg),scene_frame(b,tg),smooth(w))
    # global fade in/out
    if tg<0.6:
        img=Image.blend(Image.new("RGB",(W,H),(6,12,26)),img,smooth(tg/0.6))
    if tg>total-0.9:
        img=Image.blend(img,Image.new("RGB",(W,H),(6,12,26)),smooth((tg-(total-0.9))/0.9))
    img.save(f"{OUT}/f{f:05d}.jpg",quality=90)
    if f%100==0: print("frame",f)
print("frames done:",nframes)
