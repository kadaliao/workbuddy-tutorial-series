#!/usr/bin/env python3
"""系列统一片头：真实操作快剪（会说话→说清需求→读材料做成品→你来把关）+ 系列标题卡 + 本集标题。
用法: intro.py [集数 "本集标题"]  默认第 1 集。输出 video/intro/intro-epNN.mp4；加 --join 时再拼上 video/ep01-v4.mp4 → video/ep01-v5.mp4
"""
import json, os, subprocess, sys, hashlib
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
V = "/Volumes/Data-External/workspace/cc-test/wbd/video"; F = f"{V}/footage/ep01"; AU = os.environ.get("INTRO_AU", f"{V}/audio/intro")
B = os.environ.get("INTRO_BUILD", f"{V}/build/intro"); OUT = os.environ.get("INTRO_OUT", f"{V}/intro"); os.makedirs(B, exist_ok=True); os.makedirs(OUT, exist_ok=True)
PY = f"{V}/build/venv/bin/python"; ANN = f"{V}/build/annotate4.py"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"; ACC = (255, 176, 32); BG = (20, 24, 31); FPS = 30
LEAD = 0.15
EP = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
TITLE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "装好并跑通第一个任务"
JOIN = "--join" in sys.argv

def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
CH = []   # 逐字时间
for s_ in json.load(open(f"{AU}/intro.json"))["segments"]:
    for w in s_["words"]:
        cs = [c for c in w["word"] if c.strip() and c not in "，。、,.;；"]
        CH += [(c, w["start"] + (w["end"]-w["start"])*i/max(len(cs),1)) for i, c in enumerate(cs)]
SCRIPT = "".join(c for c in "会说话，就能让 AI 替你干活。你说清需求，它读材料、做成品；你只负责把关。WorkBuddy 零基础实战，每集一个，看完就能照做的小任务。" if c.strip() and c not in "，。、；")
def at(phrase):  # 台本字位置 → 按字数比例映射到识别出的逐字时间（识别字可能有错，位置比例仍可靠）
    return CH[min(len(CH)-1, round(SCRIPT.index(phrase)*len(CH)/len(SCRIPT)))][1] + LEAD

USER = {"name": "用户行", "rect": [8,795,180,55], "style": "fillmed"}
PROMO = {"name": "推广", "rect": [1262,6,172,42], "style": "fillmed"}
DROP = ["推广", "用户行"]
t1, t2, t3, t4, t5 = 0.0, at("你说") - 0.15, at("它") - 0.1, at("你只") - 0.15, at("Work") - 0.2
END = round(dur(f"{AU}/intro.wav") + LEAD + 1.9, 2)   # 口播后留出本集标题

SHOTS = [  # (源, 片段长度, cfg)
 (f"{F}/F5-写需求.mov", t2-t1, {"anchors": [[5.6, 0], [13.6, t2-t1]], "cam_fixed": [440,250,830,500], "events_override": [],
     "drop_masks": DROP, "masks_extra": [USER, PROMO]}),
 (f"{F}/G5-执行.mov", t3-t2, {"anchors": [[3.1, 0], [4.58, t3-t2]], "cam_fixed": [760,340,620,240], "drop_masks": DROP, "masks_extra": [USER, PROMO],
     "events_override": [{"t": 4.42, "kind": "click", "x": 1220, "y": 473, "target": [1195,448,50,50], "label": None, "dur": 0.6}]}),
 (f"{F}/G5-执行.mov", t4-t3, {"anchors": [[8.0, 0], [76.0, (t4-t3)*0.42], [86.0, t4-t3]], "events_override": [],
     "cam_keys": [[8.0, 270,0,880,526], [76.0, 270,0,880,526], [80.5, 0,0,1440,860]], "drop_masks": DROP, "masks_extra": [USER],
     "badges": [{"from": 8.0, "to": 76.0, "text": "它自己在干活 · 实际 {real}", "t0": 5.0}]}),
 (f"{F}/H5-验收.mov", t5-t4, {"anchors": [[9.7, 0], [12.6, t5-t4]], "drop_masks": DROP, "masks_extra": [USER],
     "events_override": [{"t": 9.9, "kind": "move", "target": [956,628,310,22], "label": "多写了一句，你来把关", "zoom": 2.2, "focus": True, "dur": 2.6}]}),
]

def render(src, cfg):
    key = hashlib.md5((src + json.dumps(cfg, sort_keys=True, ensure_ascii=False) + hashlib.md5(open(ANN,"rb").read()).hexdigest()).encode()).hexdigest()[:8]
    out = f"{B}/r_{os.path.basename(src)[:2]}_{key}.mp4"
    if not os.path.exists(out):
        cp = out[:-4] + ".json"; json.dump(cfg, open(cp, "w"), ensure_ascii=False)
        subprocess.run([PY, ANN, src, out, "--cfg", cp], check=True)
    return out

def ease(x): x = max(0.0, min(1.0, x)); return x*x*x*(x*(x*6-15)+10)

def title_card(secs, t0):
    """系列标题卡：t0 起播（相对片头起点）。"""
    out = f"{B}/card_ep{EP:02d}_{hashlib.md5(f'{secs}{t0}{TITLE}'.encode()).hexdigest()[:6]}.mp4"
    if os.path.exists(out): return out
    wr = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-",
                           "-c:v","libx264","-preset","fast","-crf","16","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE)
    f_tag, f_big, f_sub, f_ep = (ImageFont.truetype(FONT, s) for s in (40, 128, 54, 50))
    base = Image.new("RGB", (1920,1080), BG); d0 = ImageDraw.Draw(base)
    for y in range(1080): c = int(12*y/1080); d0.line((0,y,1920,y), fill=(BG[0]+c, BG[1]+c, BG[2]+c))
    tl_sub = at("每集") - t0; tl_ep = END - 1.9 - t0 + 0.15
    for i in range(int(round(secs*FPS))):
        t = i/FPS; im = base.copy(); lay = Image.new("RGBA", (1920,1080), (0,0,0,0)); d = ImageDraw.Draw(lay)
        p = ease(t/0.5)                                     # 主标题
        bar = ease((t-0.15)/0.6)                            # 下划线
        big = "WorkBuddy 零基础实战"; w = d.textlength(big, font=f_big); x = (1920-w)/2; y = 330
        tag = "系列课程 · 实机演示"; wt = d.textlength(tag, font=f_tag)
        d.text(((1920-wt)/2, y-90 + (1-p)*10), tag, font=f_tag, fill=(165,173,186,int(255*p)))
        d.text((x, y + (1-p)*30), big, font=f_big, fill=(245,247,250,int(255*p)))
        bw = w*bar; d.rounded_rectangle(((1920-bw)/2, y+165, (1920+bw)/2, y+175), radius=5, fill=ACC+(int(255*min(1,bar*2)),))
        q = ease((t-tl_sub)/0.45)
        sub = "每集一个，看完就能照做的小任务"; ws = d.textlength(sub, font=f_sub)
        d.text(((1920-ws)/2, y+215 + (1-q)*20), sub, font=f_sub, fill=ACC+(int(255*q),))
        r = ease((t-tl_ep)/0.4)
        if r > 0:
            ep = TITLE.replace("：", "  ·  ", 1) if TITLE.startswith("番外") else f"第 {EP} 集  ·  {TITLE}"; we = d.textlength(ep, font=f_ep); px, py = (1920-we)/2 - 34, y+345 + (1-r)*18
            d.rounded_rectangle((px, py, px+we+68, py+84), radius=42, fill=(255,255,255,int(26*r)), outline=(255,255,255,int(70*r)), width=2)
            d.text((px+34, py+13), ep, font=f_ep, fill=(240,243,247,int(255*r)))
        im.paste(lay, (0,0), lay); wr.stdin.write(im.tobytes())
    wr.stdin.close(); wr.wait(); return out

def sub_png(i, parts):
    """字幕条：parts=[(文字, 是否强调)]，大号，强调词用强调色。"""
    f = ImageFont.truetype(FONT, 54); im = Image.new("RGBA", (1920,110), (0,0,0,0)); d = ImageDraw.Draw(im)
    w = sum(d.textlength(t, font=f) for t, _ in parts); x = (1920-w)/2
    for t, hi in parts:
        d.text((x, 20), t, font=f, fill=(ACC if hi else (250,250,250))+(255,)); x += d.textlength(t, font=f)
    p = f"{B}/sub{i}.png"; im.save(p); return p

def main():
    clips = [render(s, c) for s, _, c in SHOTS] + [title_card(END - t5, t5)]
    lst = f"{B}/lst.txt"; open(lst, "w").write("".join(f"file '{c}'\n" for c in clips))
    vcat = f"{B}/v.mp4"; subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lst,"-c","copy",vcat], check=True)
    # 提示音：标题出现时一声轻“叮”
    chime = f"{B}/chime.wav"
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
        "aevalsrc='0.32*sin(2*PI*880*t)*exp(-5*t)+0.20*sin(2*PI*1318.5*t)*exp(-6*t)+0.10*sin(2*PI*1760*t)*exp(-8*t)':s=48000:d=1.6",
        "-af","afade=t=in:d=0.005",chime], check=True)
    cues = [(LEAD, t2+0.05, [("会说话", True), ("，就能让 AI 替你干活", False)]),
            (t2+0.05, t4, [("你说清需求，它读材料、", False), ("做成品", True)]),
            (t4, t5, [("你只负责", False), ("把关", True)])]
    ins = []; fl = []; last = "0:v"
    for i, (a, b, parts) in enumerate(cues):
        ins += ["-i", sub_png(i, parts)]
        fl.append(f"[{last}][{i+3}:v]overlay=0:970:enable='between(t,{a:.3f},{b:.3f})'[v{i}]"); last = f"v{i}"
    out = f"{OUT}/intro-ep{EP:02d}.mp4"
    fc = ";".join(fl) + (f";[1:a]aresample=48000,adelay={int(LEAD*1000)}:all=1[vo];[2:a]adelay={int((t5+0.05)*1000)}:all=1,volume=0.9[ch];"
                         f"[vo][ch]amix=inputs=2:duration=longest:normalize=0,apad=whole_dur={END},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]")
    subprocess.run(["ffmpeg","-y","-v","error","-i",vcat,"-i",f"{AU}/intro.wav","-i",chime]+ins+["-filter_complex",fc,
        "-map",f"[{last}]","-map","[a]","-t",f"{END}","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-ac","1","-movflags","+faststart",out], check=True)
    print("intro", out, dur(out))
    if JOIN:
        ep = os.environ.get("JOIN_EP", f"{V}/ep01-v4.mp4"); fin = os.environ.get("JOIN_OUT", f"{V}/ep01-v5.mp4")
        subprocess.run(["ffmpeg","-y","-v","error","-i",out,"-i",ep,"-filter_complex",
            "[0:v]fade=t=out:st=%.2f:d=0.25[a];[1:v]fade=t=in:st=0:d=0.25[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au]" % (END-0.25),
            "-map","[v]","-map","[au]","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ac","1",
            "-movflags","+faststart",fin], check=True)
        print("joined", fin, dur(fin))

if __name__ == "__main__": main()
