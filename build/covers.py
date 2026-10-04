#!/usr/bin/env python3
"""视频号封面：3:4（个人主页卡片）与 4:3（分享卡片），统一系列风格。"""
import json, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V="/Volumes/Data-External/workspace/cc-test/wbd/video"; O=f"{V}/publish/covers"
FONT="/System/Library/Fonts/Hiragino Sans GB.ttc"
ACC=(255,176,32); BG=(20,24,31)
EPS=[("第 1 集","装好并跑通","第一个任务","ep01-v7.mp4"),("第 2 集","先把门锁好","权限·工作空间·备份","ep02-v1.mp4"),
 ("第 3 集","一句话","说清需求","ep03-v1.mp4"),("第 4 集","三种模式","什么时候用哪种","ep04-v1.mp4"),
 ("第 5 集","验收三步","它做对了吗","ep05-v1.mp4"),("第 6 集","存成技能","和斜杠指令","ep06-v1.mp4"),
 ("第 7 集","专家","与专家团","ep07-v1.mp4"),("第 8 集","材料从哪来","成品放哪去","ep08-v1.mp4"),
 ("第 9 集","定时任务","让它自己上班","ep09-v1.mp4"),("第 10 集","手机","遥控电脑","ep10-v1.mp4"),
 ("第 11 集","连接器","文档邮箱一键连","ep11-v1.mp4"),("第 12 集","越用越懂你","个性化·记忆·模型","ep12-v1.mp4"),
 ("番外","积分","怎么花掉的","ep13-番外-v1.mp4")]
AT={1:15.0}
FT="/Volumes/Data-External/workspace/cc-test/wbd/video/footage"
RAW={2:(f"{FT}/ep02/A3-拒绝删除.mov",8.0,(250,0,1190,860)),3:(f"{FT}/ep03/A-模糊指令.mov",96.0,(250,0,1190,860)),
     5:(f"{FT}/ep05/B-验收.mov",14.5,(250,0,1190,860)),6:(f"{FT}/ep06/D-调用技能.mov",11.0,(380,0,1060,560)),
     8:(f"{FT}/ep08/D-成品在哪.mov",15.0,(700,0,740,560)),9:(f"{FT}/ep09/E-频率与保存.mov",8.0,(250,100,1000,560))}
def raw_frame(i):
    f,t,(x,y,w,h)=RAW[i]; p="/private/tmp/claude-501/cv.png"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t}","-i",f,"-frames:v","1",p])
    return Image.open(p).convert("RGB").crop((x*2,y*2,(x+w)*2,(y+h)*2))
def F(s): return ImageFont.truetype(FONT, s)
def trim(im):
    a=np.asarray(im).astype(int); diff=np.abs(a-np.array(BG)).sum(2)>40
    ys=np.where(diff.mean(1)>0.3)[0]; xs=np.where(diff.mean(0)>0.3)[0]
    return im.crop((xs[0],ys[0],xs[-1]+1,ys[-1]+1)) if len(xs) and len(ys) else im
def best_frame(vid, at=None):
    if at is not None:
        p="/private/tmp/claude-501/cv.png"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{at}","-i",vid,"-frames:v","1",p])
        return trim(Image.open(p).convert("RGB").crop((156,10,1764,970)))
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",vid]))
    best=None
    for k in range(8):
        t=16+(d-40)*k/7
        p="/private/tmp/claude-501/cv.png"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t:.2f}","-i",vid,"-frames:v","1",p])
        im=Image.open(p).convert("RGB").crop((156,10,1764,970))
        a=np.asarray(im).astype(float); score=a.mean()+a.std()*0.5
        if best is None or score>best[0]: best=(score,im.copy())
    return trim(best[1])
def bg(w,h):
    im=Image.new("RGB",(w,h),BG); d=ImageDraw.Draw(im)
    for y in range(h): c=int(14*y/h); d.line((0,y,w,y),fill=(BG[0]+c,BG[1]+c,BG[2]+c+4))
    return im
def card(im, shot, box):
    x,y,w,h=box
    sw,sh_=shot.size; k=max(w/sw,h/sh_); s=shot.resize((int(sw*k)+1,int(sh_*k)+1),Image.LANCZOS)
    ox=(s.size[0]-w)//2; s=s.crop((ox,0,ox+w,h))
    sh=Image.new("L",im.size,0); ImageDraw.Draw(sh).rounded_rectangle((x+6,y+14,x+w+6,y+h+14),22,fill=170)
    sh=sh.filter(ImageFilter.GaussianBlur(18)); black=Image.new("RGB",im.size,(0,0,0)); im.paste(black,(0,0),sh)
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),18,fill=255)
    im.paste(s,(x,y),m); ImageDraw.Draw(im).rounded_rectangle((x,y,x+w-1,y+h-1),18,outline=(70,78,92),width=2)
    return y+h
def tag(d,x,y,text,size=40):
    f=F(size); w=d.textlength(text,font=f)
    d.rounded_rectangle((x,y,x+w+44,y+size+26),radius=(size+26)//2,fill=ACC)
    d.text((x+22,y+10),text,font=f,fill=BG)
def portrait(ep,l1,l2,shot):
    W,H=1080,1440; im=bg(W,H); d=ImageDraw.Draw(im)
    d.rectangle((0,0,14,H),fill=ACC)
    d.text((80,90),"WorkBuddy 零基础实战",font=F(44),fill=(170,178,190))
    tag(d,80,170,ep,44)
    d.text((80,280),l1,font=F(132),fill=(245,247,250))
    d.text((80,440),l2,font=F(88 if len(l2)>6 else 104),fill=ACC)
    card(im,shot,(80,640,920,560))
    d.text((80,1330),"每集一个，看完就能照做的小任务",font=F(40),fill=(170,178,190))
    return im
def landscape(ep,l1,l2,shot):
    W,H=1440,1080; im=bg(W,H); d=ImageDraw.Draw(im)
    d.rectangle((0,0,14,H),fill=ACC)
    d.text((80,80),"WorkBuddy 零基础实战",font=F(42),fill=(170,178,190))
    tag(d,80,160,ep,42)
    d.text((80,280),l1,font=F(112),fill=(245,247,250))
    d.text((80,420),l2,font=F(72 if len(l2)>6 else 88),fill=ACC)
    card(im,shot,(80,580,1280,420))
    return im
if __name__=="__main__":
    import sys
    only=[int(a) for a in sys.argv[1:]] or list(range(1,14))
    for i in only:
        ep,l1,l2,f=EPS[i-1]
        shot=raw_frame(i) if i in RAW else best_frame(f"{V}/{f}", AT.get(i))
        portrait(ep,l1,l2,shot).save(f"{O}/ep{i:02d}-3x4.png")
        landscape(ep,l1,l2,shot).save(f"{O}/ep{i:02d}-4x3.png")
        print("cover",i)
