#!/usr/bin/env python3
"""第1集 v2 编排：录屏(带标注/放大) + 静态页 + 文字卡片，对齐旁白，输出成片。"""
import json, os, subprocess, sys, hashlib, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
V = "/Volumes/Data-External/workspace/cc-test/wbd/video"; B = f"{V}/build/ep01v2"; F = f"{V}/footage/ep01"; A = f"{V}/audio/ep01"
PY = f"{V}/build/venv/bin/python"; os.makedirs(B, exist_ok=True)
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"; ACC = (255, 176, 32)
segs = json.load(open(f"{A}/segs.json"))

def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))

# ---------- 文字卡片 ----------
def card(name, lines, secs, sub=None):
    out = f"{B}/card_{name}.mp4"
    if os.path.exists(out): return out
    wr = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r","30","-i","-","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE)
    n = int(secs*30)
    for i in range(n):
        t = i/30; im = Image.new("RGB", (1920,1080), (20,24,31)); d = ImageDraw.Draw(im)
        for y in range(1080):  # 轻微渐变
            c = int(8*y/1080); d.line((0,y,1920,y), fill=(20+c,24+c,31+c))
        d.rectangle((0,0,16,1080), fill=ACC)
        total_h = len(lines)*130; y0 = (1080-total_h)//2
        for k, ln in enumerate(lines):
            st = 0.25 + k*0.7; p = min(1, max(0, (t-st)/0.45)); p = p*p*(3-2*p)
            if p <= 0: continue
            big = isinstance(ln, tuple) and ln[1] == "big"; txt = ln[0] if isinstance(ln, tuple) else ln
            f = ImageFont.truetype(FONT, 96 if big else 78); w = d.textlength(txt, font=f)
            lay = Image.new("RGBA", (1920,200), (0,0,0,0)); ld = ImageDraw.Draw(lay)
            col = ACC if big else (240,243,247)
            ld.text(((1920-w)/2, 40 + (1-p)*28), txt, font=f, fill=col+(int(255*p),))
            im.paste(lay, (0, y0 + k*130 - 20), lay)
        wr.stdin.write(im.tobytes())
    wr.stdin.close(); wr.wait(); return out

# ---------- 静态页 → 带标注的“录屏” ----------
def still(name, img, secs, events, scale=1.0, size=None, cfg=None):
    mov = f"{B}/still_{name}.mov"
    im = Image.open(img); w, h = im.size; w -= w % 2; h -= h % 2
    subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-i",img,"-t",str(secs),"-r","30","-vf",f"crop={w}:{h}:0:0","-c:v","libx264","-crf","14","-pix_fmt","yuv420p",mov], check=True)
    base = mov[:-4]
    json.dump({"region":[0,0,w,h],"scale":scale,"fps":30}, open(base+".meta.json","w"))
    json.dump(events, open(base+".events.json","w"), ensure_ascii=False)
    return render(mov, cfg or {"trim":[0, secs-0.05]})

# ---------- 标注渲染（缓存）----------
def render(clip, cfg, tag=None):
    key = hashlib.md5((clip + json.dumps(cfg, sort_keys=True) + hashlib.md5(open(f"{V}/build/annotate.py","rb").read()).hexdigest()).encode()).hexdigest()[:8]
    out = f"{B}/r_{os.path.basename(clip)[:-4]}_{key}.mp4"
    if os.path.exists(out): return out
    cp = out[:-4] + ".cfg.json"; json.dump(cfg, open(cp,"w"), ensure_ascii=False)
    subprocess.run([PY, f"{V}/build/annotate.py", clip, out, "--cfg", cp], check=True)
    return out

def R(name, cfg): return ("R", f"{F}/{name}.mov", cfg)

# ---------- 每个旁白段对应的画面 ----------
PLAN = [
 ("A开场", [R("H-验收", {"trim":[3,15.5], "auto_zoom":False, "patch":[{"contains":"数据表现","set":{"zoom":1.7,"focus":False}}]})]),
 ("B为什么", [("CARD","b1",["每周五下午",("翻聊天记录 · 对数据 · 调格式","big")],5.5),
              ("CARD","b2",["一份周报，动辄一两个小时",("真正要动脑的，只有一件事","big")],4.5),
              ("CARD","b3",["这周哪件事最重要？",("其余的整理活，交给它","big")],4.0)]),
 ("C装好", [("STILL","site",f"{F}/B-官网首页.png",11.0,
               [{"t":1.2,"kind":"move","x":1920,"y":749,"target":[1700,690,440,120],"label":"点「立即下载」","dur":3.2,"zoom":1.5,"focus":True}],1.0),
            R("C-安装", {"trim":[1.5,15.1], "speed":[{"from":1.5,"to":15.1,"factor":1.0,"badge":""}], "auto_zoom":False, "mask_style":{"右上推广":"fill"},
                         "patch":[{"contains":"选「停止」","set":{"label":"弹出提示：点「停止」","zoom":1.8,"focus":True,"dur":2.2}}]}),
            ("STILL","login",f"{V}/shots/01-启动登录页.png",4.8,
               [{"t":0.8,"kind":"click","x":1200,"y":1022,"target":[1020,984,360,76],"label":"登录：扫码，没有游客模式","dur":3.5,"zoom":1.6}],1.0)]),
 ("D界面", [R("D-侧栏巡览", {"trim":[0.8,34.3], "speed":[{"from":0.8,"to":34.3,"factor":1.05,"badge":""}], "auto_zoom":False,
                  "mask_style":{"右上推广":"fill"}, "masks_extra":[{"name":"活动气泡","rect":[1010,160,230,140],"t":[[27.5,34.3]],"style":"fill"}]})]),
 ("E选文件夹", [R("E-选工作空间", {"trim":[1.5,18], "speed":[{"from":1.5,"to":18,"factor":0.8,"badge":""}]})]),
 ("F写需求", [R("F-写需求", {"trim":[1.5,25], "speed":[{"from":1.5,"to":25,"factor":1.12,"badge":""}]})]),
 ("G执行", [R("G-执行", {"trim":[0,141], "auto_zoom":True,
              "speed":[{"from":5.5,"to":125,"factor":24,"badge":"等待中 · 24 倍速"},{"from":125,"to":141,"factor":2.5,"badge":""}]})]),
 ("H验收", [R("H-验收", {"trim":[2.5,26], "speed":[{"from":2.5,"to":26,"factor":1.8,"badge":""}], "auto_zoom":False,
              "patch":[{"contains":"数据表现","set":{"zoom":1.9,"focus":True,"dur":2.2}}]})]),
 ("K找文件", [R("K-找文件", {"trim":[2,17], "speed":[{"from":2,"to":17,"factor":1.8,"badge":""}],
              "patch":[{"contains":"这就是刚生成","set":{"zoom":1.9,"focus":True}}]})]),
 ("I坑", [R("I-权限", {"trim":[1.5,15], "speed":[{"from":1.5,"to":15,"factor":0.75,"badge":""}],
              "patch":[{"contains":"开关是关着","set":{"zoom":2.4,"focus":True,"dur":3.2}},{"contains":"这里是“允许完全访问”","set":{"zoom":False}}]})]),
 ("J收尾", [("CARD","j1",["今天三句话",("1  先装好、登录，认清左边七个入口","")],3.0),
            ("CARD","j2",[("2  让它在一个文件夹里干活","")],3.5),
            ("CARD","j3",[("3  需求说清：做什么、有什么材料、要什么结果","")],5.0),
            ("CARD","j4",["下一集",("把门锁好：权限、工作空间与备份","big")],6.0)]),
]

def build_item(it):
    if it[0] == "R": return render(it[1], it[2])
    if it[0] == "CARD": return card(it[1], it[2], it[3])
    if it[0] == "STILL": return still(it[1], it[2], it[3], it[4], cfg=None)
    raise ValueError(it)

def main():
    only = set(sys.argv[1:])
    items = [(n, it) for n, its in PLAN for it in its]
    # 并行渲染（每个 annotate 进程本身较吃 CPU，限制并发）
    with ThreadPoolExecutor(3) as ex: res = list(ex.map(lambda x: build_item(x[1]), items))
    paths = {}; i = 0
    for n, its in PLAN:
        paths[n] = res[i:i+len(its)]; i += len(its)
    segfiles = []
    for n, its in PLAN:
        ps = paths[n]; lst = f"{B}/lst_{n}.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in ps))
        vcat = f"{B}/seg_{n}_v.mp4"
        subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lst,"-c","copy",vcat], check=True)
        a = f"{A}/{n}.wav"; ad = dur(a); vd = dur(vcat); total = max(vd, ad + 0.6)
        out = f"{B}/seg_{n}.mp4"
        subprocess.run(["ffmpeg","-y","-v","error","-i",vcat,"-i",a,"-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={max(0,total-vd):.3f},fps=30[v];[1:a]adelay=300|300,apad=whole_dur={total:.3f}[a]",
            "-map","[v]","-map","[a]","-t",f"{total:.3f}","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-ar","44100","-b:a","160k",out], check=True)
        segfiles.append(out); print(n, f"video {vd:.1f}s audio {ad:.1f}s -> {total:.1f}s")
    open(f"{B}/final.txt","w").write("".join(f"file '{p}'\n" for p in segfiles))
    nosub = f"{B}/final_nosub.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{B}/final.txt","-c","copy",nosub], check=True)
    # 字幕：按段内旁白起点(+0.3s)与时长按字数分配
    cues = []; off = 0.0
    for n, _ in PLAN:
        ad = dur(f"{A}/{n}.wav"); total = dur(f"{B}/seg_{n}.mp4")
        parts = [p for p in re.split(r"(?<=[。！？，：；])", segs[n]) if p.strip()]; cl = []; cur = ""
        for p_ in parts:
            if len(cur)+len(p_) <= 24: cur += p_
            else:
                if cur: cl.append(cur)
                cur = p_
        if cur: cl.append(cur)
        L = sum(len(c) for c in cl); t = off + 0.3
        for c in cl:
            e = t + ad*len(c)/L; cues.append((t, e, c.rstrip("，；：").strip())); t = e
        off += total
    font = ImageFont.truetype(FONT, 44); ins = []; fl = []; last = "0:v"
    for i, (a_, b_, t_) in enumerate(cues):
        im = Image.new("RGBA", (1920,1080), (0,0,0,0)); d = ImageDraw.Draw(im)
        w = d.textlength(t_, font=font); d.text(((1920-w)/2, 976), t_, font=font, fill=(255,255,255,255), stroke_width=4, stroke_fill=(0,0,0,255))
        pth = f"{B}/sub{i}.png"; im.save(pth); ins += ["-i", pth]
        fl.append(f"[{last}][{i+1}:v]overlay=enable='between(t,{a_:.3f},{b_:.3f})'[v{i}]"); last = f"v{i}"
    final = f"{V}/ep01-v3.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-i",nosub]+ins+["-filter_complex",";".join(fl),"-map",f"[{last}]","-map","0:a","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",final], check=True)
    print("final", dur(final))

if __name__ == "__main__": main()
