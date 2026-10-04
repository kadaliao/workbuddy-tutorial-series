import json,subprocess,os,re
V="/Volumes/Data-External/workspace/cc-test/wbd/video"; B=f"{V}/build/ep01"; A=f"{V}/audio/ep01"
segs=json.load(open(f"{A}/segs.json"))
plan=[("A开场",[("24-任务完成.png",1)]),
("B为什么",[("03-主界面.png",1)]),
("C装好",[("B-官网首页.png",.4),("01-启动登录页.png",.3),("02-关于页.png",.3)]),
("D界面",[("03-主界面.png",1),("49-助理页.png",1),("50-项目页.png",1),("34-专家技能连接器页.png",1),("40-定时任务页.png",1),("39-资料库页.png",1),("51-更多菜单.png",1)]),
("E选文件夹",[("04-工作空间下拉.png",.4),("08-选择本地文件夹后.png",.6)]),
("F写需求",[("19-输入指令.png",1)]),
("G执行",[("22-任务执行中.png",.5),("23-任务执行中2.png",.5)]),
("H验收",[("24-任务完成.png",1)]),
("I坑",[("09-权限菜单.png",1)]),
("J收尾",[("03-主界面.png",1)])]
def dur(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def src(n):
    return f"{V}/footage/ep01/{n}" if n.startswith("B-") else f"{V}/shots/{n}"
# 1) 预处理静帧：遮盖广告/积分卡片，放入 1920x1080
cache={}
def frame(n):
    if n in cache: return cache[n]
    out=f"{B}/f_{len(cache)}.png"
    if n.startswith("B-"):
        vf="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#f3f3f3"
    else:
        m=("drawbox=x=1780:y=255:w=450:h=290:color=white:t=fill,"      # 活动气泡
           "drawbox=x=2040:y=15:w=360:h=80:color=white:t=fill,"          # 做任务赢积分
           "drawbox=x=15:y=1325:w=490:h=150:color=0xf3f3f3:t=fill,")    # Buddy加油站
        vf=m+"scale=-2:1080,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#f3f3f3"
    subprocess.run(["ffmpeg","-y","-v","error","-i",src(n),"-vf",vf,out],check=True)
    cache[n]=out; return out
clips=[];srt=[];t0=0.0;auds=[]
def ts(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".",",")
k=0
for name,imgs in plan:
    a=f"{A}/{name}.wav"; d=dur(a)+0.5
    auds.append(a)
    tot=sum(w for _,w in imgs)
    for n,w in imgs:
        dd=d*w/tot; fr=frame(n); out=f"{B}/c{k}.mp4"; k+=1
        frames=int(dd*30)+1
        zp=f"zoompan=z='min(1+0.0008*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30"
        subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-i",fr,"-vf",f"scale=3840:2160,{zp},format=yuv420p","-frames:v",str(frames),"-r","30","-c:v","libx264","-preset","fast","-crf","20",out],check=True)
        clips.append(out)
    # 字幕
    txt=segs[name]; parts=[p for p in re.split(r"(?<=[。！？，：；])",txt) if p.strip()]
    # 合并过短片段
    cues=[];cur=""
    for p in parts:
        if len(cur)+len(p)<=26: cur+=p
        else:
            if cur: cues.append(cur)
            cur=p
    if cur: cues.append(cur)
    L=sum(len(c) for c in cues); s=t0
    for c in cues:
        e=s+(d-0.5)*len(c)/L
        srt.append((s,e,c.rstrip("，；：、").strip())); s=e
    t0+=d
open(f"{B}/list.txt","w").write("".join(f"file '{c}'\n" for c in clips))
with open(f"{B}/sub.srt","w") as f:
    for i,(s,e,c) in enumerate(srt,1): f.write(f"{i}\n{ts(s)} --> {ts(e)}\n{c}\n\n")
# 音频：每段后补 0.5s 静音
al=[]
for i,a in enumerate(auds):
    o=f"{B}/a{i}.wav"; subprocess.run(["ffmpeg","-y","-v","error","-i",a,"-af","apad=pad_dur=0.5","-ar","24000","-ac","1",o],check=True); al.append(o)
open(f"{B}/alist.txt","w").write("".join(f"file '{c}'\n" for c in al))
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{B}/alist.txt","-c","copy",f"{B}/voice.wav"],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{B}/list.txt","-c","copy",f"{B}/video_noaudio.mp4"],check=True)
style="FontName=PingFang SC,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=36,Alignment=2"
subprocess.run(["ffmpeg","-y","-v","error","-i",f"{B}/video_noaudio.mp4","-i",f"{B}/voice.wav","-vf",f"subtitles={B}/sub.srt:force_style='{style}'","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",f"{V}/ep01-v1-静帧版.mp4"],check=True)
print("done",t0)
