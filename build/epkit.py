#!/usr/bin/env python3
"""各集通用的成片工具（由第 1 集 assemble_ep01_v4.py 抽出）。
一集一个 epNN.py：定义 EP、TITLE、TEXT（分段口播）、ORDER、plan(k)（每段的画面列表），然后调用 epkit.main(...)。
流程：voice（Charon 配音 + whisper 逐字时间 + listen 听验）→ render（画面按口播对齐）→ 字幕条 → 片头 → 配乐 → 成片 video/epNN-vX.mp4
"""
import json, os, re, subprocess, sys, hashlib
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

V = "/Volumes/Data-External/workspace/cc-test/wbd/video"
PY = f"{V}/build/venv/bin/python"; ANN = f"{V}/build/annotate4.py"
TTS = os.path.expanduser("~/.claude/skills/tts/scripts/tts.py"); LISTEN = os.path.expanduser("~/.claude/skills/tts/scripts/listen.py")
VOICE, STYLE = "Charon", "friendly, clear and confident tech tutorial narrator speaking natural Mandarin Chinese, conversational, medium pace, warm"
BGM = f"{V}/audio/bgm/mixkit-568-focus-on-yourself.mp3"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"; ACC = (255, 176, 32); BG = (20, 24, 31)
LEAD, TAIL = 0.3, 0.6
PUN = set("，。、：；！？,.:;!? “”「」")
USER = {"name": "用户行", "rect": [8,795,180,55], "style": "fillmed"}
def PROMO(t=None): return dict({"name": "推广", "rect": [1262,6,172,42], "style": "fillmed"}, **({"t": t} if t else {}))
DROP = ["推广", "用户行"]

def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))

class Kit:
    def __init__(self, ep, text, order, extra=None):
        self.ep, self.TEXT, self.ORDER = ep, text, order
        self.A = f"{V}/audio/ep{ep:02d}"; self.B = f"{V}/build/ep{ep:02d}"; self.F = f"{V}/footage/ep{ep:02d}"
        for d in (self.A, self.B, f"{self.B}/wj", self.F): os.makedirs(d, exist_ok=True)
        self.extra = extra or {}
        self._ct = {}

    # ---------- 配音 ----------
    def voice(self, only=None, force=False):
        def stale(n):
            w, t = f"{self.A}/{n}.wav", f"{self.A}/{n}.txt"
            return force or not os.path.exists(w) or not os.path.exists(t) or open(t).read() != self.TEXT[n]
        jobs = [n for n in self.ORDER if (not only or n in only) and stale(n)]
        def one(n):
            subprocess.run([TTS, self.TEXT[n], "--voice", VOICE, "--style", STYLE, "-o", f"{self.A}/{n}.wav"], check=True, capture_output=True)
            open(f"{self.A}/{n}.txt", "w").write(self.TEXT[n])
            w16 = f"{self.B}/wj/{n}_16k.wav"
            subprocess.run(["ffmpeg","-y","-v","error","-i",f"{self.A}/{n}.wav","-ar","16000","-ac","1",w16], check=True)
            subprocess.run(["whisper", w16, "--model","base","--language","zh","--word_timestamps","True","--output_format","json","--output_dir",f"{self.B}/wj"], check=True, capture_output=True)
            os.replace(f"{self.B}/wj/{n}_16k.json", f"{self.B}/wj/{n}.json")
            q = "逐字转写这段中文语音（只输出转写），然后另起一行写：问题：有没有读错字、多念或漏念、怪异停顿、杂音（没有就写“无”）。"
            r = subprocess.run([LISTEN, f"{self.A}/{n}.wav", "--ask", q], capture_output=True, text=True).stdout.strip()
            open(f"{self.A}/{n}.listen.txt", "w").write(r); return n, r
        with ThreadPoolExecutor(4) as ex:
            for n, r in ex.map(one, jobs): print(f"===== {n}\n{r}")

    # ---------- 时间 ----------
    def AD(self, n): return dur(f"{self.A}/{n}.wav")
    def T(self, n): return round(self.AD(n) + LEAD + TAIL + self.extra.get(n, 0), 3)
    def char_times(self, n):
        if n not in self._ct:
            d = json.load(open(f"{self.B}/wj/{n}.json")); ts = []
            for s in d["segments"]:
                for w in s["words"]:
                    cs = [c for c in w["word"] if c not in PUN and not c.isspace()]
                    for i, _ in enumerate(cs): ts.append(w["start"] + (w["end"]-w["start"])*i/max(len(cs),1))
            self._ct[n] = ts
        return self._ct[n]
    def sc(self, n): return "".join(c for c in self.TEXT[n] if c not in PUN and not c.isspace())
    def at(self, n, phrase, k=0):
        txt = self.sc(n); pos = -1; phrase = "".join(c for c in phrase if c not in PUN and not c.isspace())
        for _ in range(k+1): pos = txt.index(phrase, pos+1)
        ts = self.char_times(n); j = min(len(ts)-1, round(pos*len(ts)/len(txt)))
        return round(ts[j] + LEAD, 3)

    # ---------- 画面 ----------
    def card(self, name, secs, groups):
        return card(self.B, name, secs, groups)
    def render(self, src, cfg):
        key = hashlib.md5((src + json.dumps(cfg, sort_keys=True, ensure_ascii=False) + hashlib.md5(open(ANN,"rb").read()).hexdigest()).encode()).hexdigest()[:8]
        out = f"{self.B}/r_{os.path.basename(src).rsplit('.',1)[0]}_{key}.mp4"
        if os.path.exists(out): return out
        cp = out[:-4] + ".cfg.json"; json.dump(cfg, open(cp,"w"), ensure_ascii=False)
        subprocess.run([PY, ANN, src, out, "--cfg", cp], check=True); return out

    def subs_cues(self):
        cues = []; off = 0.0
        for n in self.ORDER:
            parts = [p for p in re.split(r"(?<=[。！？，：；])", self.TEXT[n]) if p.strip()]; cl = []; cur = ""
            for p in parts:
                if len(cur) + len(p) <= 18 or not cur: cur += p
                else: cl.append(cur); cur = p
            if cur: cl.append(cur)
            sc = self.sc(n); ts = self.char_times(n); k = 0; starts = []
            for c in cl:
                starts.append(ts[min(len(ts)-1, round(k*len(ts)/len(sc)))] + LEAD)
                k += len([ch for ch in c if ch not in PUN and not ch.isspace()])
            ad = self.AD(n)
            for i, c in enumerate(cl):
                e = starts[i+1] - 0.05 if i+1 < len(cl) else ad + LEAD + 0.25
                cues.append((off + starts[i], off + e, c.rstrip("，。；：！？").strip()))
            off += self.T(n)
        return cues

    def build_body(self, P, out):
        items = [(n, it) for n in self.ORDER for it in P[n]]
        def build(it):
            if it[0] == "R": return self.render(it[1], it[2])
            if it[0] == "CARD": return self.card(it[1], it[2], it[3])
            if it[0] == "SPLIT":   # 左手机、右电脑并排
                L = self.render(it[1], dict(it[2], stage=[60, 10, 470, 950]))
                R = self.render(it[3], dict(it[4], stage=[560, 40, 1330, 890]))
                out = L[:-4] + "_split.mp4"
                if not os.path.exists(out):
                    subprocess.run(["ffmpeg","-y","-v","error","-i",R,"-i",L,"-filter_complex","[1:v]crop=545:1080:0:0[l];[0:v][l]overlay=0:0:shortest=1",
                        "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",out], check=True)
                return out
            raise ValueError(it)
        with ThreadPoolExecutor(4) as ex: res = list(ex.map(lambda x: build(x[1]), items))
        segs = []; i = 0
        for n in self.ORDER:
            ps = res[i:i+len(P[n])]; i += len(P[n])
            lst = f"{self.B}/lst_{n}.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in ps))
            vcat = f"{self.B}/seg_{n}_v.mp4"; subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lst,"-c","copy",vcat], check=True)
            vd = dur(vcat); total = self.T(n); o = f"{self.B}/seg_{n}.mov"
            subprocess.run(["ffmpeg","-y","-v","error","-i",vcat,"-i",f"{self.A}/{n}.wav","-filter_complex",
                f"[0:v]tpad=stop_mode=clone:stop_duration={max(0,total-vd)+0.1:.3f},fps=30,trim=duration={total:.3f}[v];"
                f"[1:a]aresample=48000,adelay={int(LEAD*1000)}:all=1,apad=whole_dur={total:.3f}[a]",
                "-map","[v]","-map","[a]","-t",f"{total:.3f}","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p","-c:a","pcm_s16le",o], check=True)
            segs.append(o); print(f"{n}: video {vd:.2f}s / seg {total:.2f}s")
        open(f"{self.B}/final.txt","w").write("".join(f"file '{p}'\n" for p in segs))
        nosub = f"{self.B}/final_nosub.mov"
        subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{self.B}/final.txt","-c","copy",nosub], check=True)
        font = ImageFont.truetype(FONT, 44); ins = []; fl = []; last = "0:v"
        for k, (a_, b_, t_) in enumerate(self.subs_cues()):
            im = Image.new("RGBA", (1920,110), (0,0,0,0)); d = ImageDraw.Draw(im)
            w = d.textlength(t_, font=font); d.text(((1920-w)/2, 26), t_, font=font, fill=(250,250,250,255))
            pth = f"{self.B}/sub{k}.png"; im.save(pth); ins += ["-i", pth]
            fl.append(f"[{last}][{k+1}:v]overlay=0:970:enable='between(t,{a_:.3f},{b_:.3f})'[v{k}]"); last = f"v{k}"
        subprocess.run(["ffmpeg","-y","-v","error","-i",nosub]+ins+["-filter_complex",";".join(fl)+";[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]",
            "-map",f"[{last}]","-map","[a]","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",out], check=True)
        return out

    def finish(self, body, title, final):
        """片头（Charon 版，替换标题）+ 正片 → 配乐 → final"""
        env = dict(os.environ, INTRO_AU=f"{V}/audio/intro_v2", INTRO_BUILD=f"{V}/build/intro_v2", INTRO_OUT=f"{V}/intro/v2",
                   JOIN_EP=body, JOIN_OUT=f"{self.B}/joined.mp4")
        subprocess.run([PY, f"{V}/build/intro.py", str(self.ep), title, "--join"], check=True, env=env)
        il = dur(f"{V}/intro/v2/intro-ep{self.ep:02d}.mp4")
        subprocess.run([PY, f"{V}/build/bgm_mix.py", f"{self.B}/joined.mp4", BGM, final, "--intro", f"{il}", "--start", "52",
                        "--head", "-17", "--body", "-23", "--duck-th", "0.1", "--duck-ratio", "2"], check=True)
        print("FINAL", final, dur(final))

# ---------- 文字卡片 ----------
_CARD_BG = None
STY = {"t": (54, (165,173,186)), "n": (70, (240,243,247)), "b": (86, ACC), "s": (46, (200,206,214)), "r": (70, (255,120,110))}
def card_bg():
    global _CARD_BG
    if _CARD_BG is None:
        im = Image.new("RGB", (1920,1080), BG); d = ImageDraw.Draw(im)
        for y in range(970): c = int(10*y/970); d.line((0,y,1920,y), fill=(BG[0]+c, BG[1]+c, BG[2]+c))
        d.rectangle((0,0,14,970), fill=ACC); _CARD_BG = im
    return _CARD_BG
def card(B, name, secs, groups):
    key = hashlib.md5(json.dumps([secs, groups], ensure_ascii=False).encode()).hexdigest()[:8]; out = f"{B}/card_{name}_{key}.mp4"
    if os.path.exists(out): return out
    wr = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r","30","-i","-",
                           "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE)
    fonts = {k: ImageFont.truetype(FONT, v[0]) for k, v in STY.items()}
    for i in range(int(round(secs*30))):
        t = i/30; im = card_bg().copy()
        for g in groups:
            if not (g["from"] <= t < g["to"]): continue
            q = 1.0 if g["to"] - t > 0.3 or g.get("last") else max(0, (g["to"]-t)/0.3)
            hs = [STY[s][0]*1.55 for _, s, _ in g["lines"]]; y = (970 - sum(hs))/2
            lay = Image.new("RGBA", (1920,1080), (0,0,0,0)); d = ImageDraw.Draw(lay)
            for (txt, s, ta), h in zip(g["lines"], hs):
                p = min(1, max(0, (t-ta)/0.45)); p = p*p*(3-2*p)
                if p > 0:
                    f = fonts[s]; w = d.textlength(txt, font=f)
                    d.text(((1920-w)/2, y + (h-STY[s][0])/2 + (1-p)*26), txt, font=f, fill=STY[s][1]+(int(255*p*q),))
                y += h
            im.paste(lay, (0,0), lay)
        wr.stdin.write(im.tobytes())
    wr.stdin.close(); wr.wait(); return out

def seg_anchor(pairs, seg_from):
    return [[s, round(o - seg_from, 3)] for s, o in pairs]
