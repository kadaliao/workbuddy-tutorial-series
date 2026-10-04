import re,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
B="/Volumes/Data-External/workspace/cc-test/wbd/video/build/ep01"
V="/Volumes/Data-External/workspace/cc-test/wbd/video"
font=ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc",48)
cues=[]
for blk in open(f"{B}/sub.srt").read().strip().split("\n\n"):
    l=blk.split("\n"); a,b=l[1].split(" --> ")
    f=lambda x:(lambda h,m,s:int(h)*3600+int(m)*60+float(s.replace(",",".")))(*x.split(":"))
    cues.append((f(a),f(b),"\n".join(l[2:])))
inputs=[];flt=[];last="0:v"
for i,(s,e,t) in enumerate(cues):
    im=Image.new("RGBA",(1920,1080),(0,0,0,0)); d=ImageDraw.Draw(im)
    w=d.textlength(t,font=font); x=(1920-w)/2; y=950
    d.rounded_rectangle((x-24,y-12,x+w+24,y+68),radius=14,fill=(0,0,0,150))
    d.text((x,y),t,font=font,fill=(255,255,255,255))
    p=f"{B}/s{i}.png"; im.save(p); inputs+=["-i",p]
    out=f"v{i}"; flt.append(f"[{last}][{i+1}:v]overlay=enable='between(t,{s:.3f},{e:.3f})'[{out}]"); last=out
cmd=["ffmpeg","-y","-v","error","-i",f"{B}/video_noaudio.mp4"]+inputs+["-i",f"{B}/voice.wav","-filter_complex",";".join(flt),"-map",f"[{last}]","-map",f"{len(cues)+1}:a","-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",f"{V}/ep01-v1-静帧版.mp4"]
subprocess.run(cmd,check=True); print("ok",len(cues))
