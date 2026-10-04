#!/usr/bin/env python3
"""给操作录屏加：镜头推近(局部放大)、高亮框、聚光灯、文字标注、点击涟漪、加速标记。
用法: annotate.py clip.mov out.mp4 [--cfg cfg.json] [--size 1920x1080]
clip 同目录需要 clip.meta.json 与 clip.events.json（光标/目标坐标为相对录制区域的逻辑点）。
cfg.json(可选): {"trim":[a,b], "speed":[{"from":a,"to":b,"factor":8,"badge":"等待中 8x"}],
                 "zoom_default":1.7, "events_override":[...]}
事件字段: t, kind(move|click|type|scroll|wait), x,y, target[x,y,w,h], label, zoom(可选:true/false/数值), focus(可选:聚光灯), dur
"""
import sys, os, json, math, subprocess, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
ACC = (255, 176, 32)       # 高亮色
INK = (20, 24, 31)

def ease(x):  # smootherstep
    x = max(0.0, min(1.0, x)); return x*x*x*(x*(x*6-15)+10)

def probe(path):
    o = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height,r_frame_rate,nb_frames,duration","-of","json",path])
    s = json.loads(o)["streams"][0]
    n, d = s["r_frame_rate"].split("/"); fps = float(n)/float(d)
    return int(s["width"]), int(s["height"]), fps, float(s.get("duration") or 0)

class Cam:
    """虚拟摄像机：在源画面(像素)里取一个窗口，随时间平滑推近/移动。"""
    def __init__(self, W, H, segs):
        self.W, self.H, self.segs = W, H, segs
    def at(self, t):
        z, cx, cy = 1.0, self.W/2, self.H/2
        for s in self.segs:
            a, b, ti, to = s["t_in"], s["t_out"], s["ease_in"], s["ease_out"]
            if t < a - ti or t > b + to: continue
            if t < a:   k = ease((t-(a-ti))/ti)
            elif t <= b: k = 1.0
            else:       k = 1 - ease((t-b)/to)
            zz = 1 + (s["zoom"]-1)*k
            # 在 z 和 cx 之间做插值(以 k 为权)
            z_new = z + (zz - z) if z == 1.0 else max(z, zz)
            cx = cx + (s["cx"]-cx)*k; cy = cy + (s["cy"]-cy)*k; z = z_new
        # 限制窗口不越界
        w, h = self.W/z, self.H/z
        cx = min(max(cx, w/2), self.W-w/2); cy = min(max(cy, h/2), self.H-h/2)
        return z, cx, cy

def build_zoom_segs(events, W, H, scale, zdef, auto_on=True):
    segs = []
    for e in events:
        tg = e.get("target"); zm = e.get("zoom")
        if not tg or zm is False: continue
        auto = auto_on and e["kind"] in ("click","type") and (tg[2]*tg[3] < 0.18*(W/scale)*(H/scale))
        if zm is None and not auto: continue
        z = zdef if zm in (None, True) else float(zm)
        cx = (tg[0]+tg[2]/2)*scale; cy = (tg[1]+tg[3]/2)*scale
        # 放大后目标应占画面 ≤ 70%
        z = min(z, 0.7*W/max(tg[2]*scale, 1), 0.7*H/max(tg[3]*scale, 1))
        z = max(z, 1.25)
        t0 = e["t"]; d = e.get("dur", 1.2)
        segs.append(dict(t_in=t0-0.1, t_out=t0+max(d, 1.0)+0.4, ease_in=0.7, ease_out=0.8, zoom=z, cx=cx, cy=cy))
    # 合并相邻重叠的片段：后一个接管（避免来回抖动）
    segs.sort(key=lambda s: s["t_in"]); out = []
    for s in segs:
        if out and s["t_in"] - out[-1]["t_out"] < 0.9:
            out[-1]["t_out"] = max(out[-1]["t_out"], s["t_out"]); out[-1]["cx"], out[-1]["cy"], out[-1]["zoom"] = s["cx"], s["cy"], max(out[-1]["zoom"]*0.0+s["zoom"], 1.25)
        else: out.append(s)
    return out

def font(sz): return ImageFont.truetype(FONT, sz)

def draw_overlay(canvas, t, events, cam_state, W, H, scale, ox, oy, k_out, speed_badge):
    """在已缩放到输出尺寸的画面上叠加标注。cam_state=(z,cx,cy)；坐标变换：源像素→输出像素。"""
    z, cx, cy = cam_state
    def tx(px, py):  # 源像素 → 输出
        return ox + ((px - (cx - W/z/2)) * z * k_out), oy + ((py - (cy - H/z/2)) * z * k_out)
    ov = Image.new("RGBA", canvas.size, (0,0,0,0)); d = ImageDraw.Draw(ov)
    for e in events:
        tg = e.get("target"); t0 = e["t"]; dur = e.get("dur", 1.2)
        show_a, show_b = t0 - 0.25, t0 + dur + 0.8
        if tg and e.get("label") is not None and show_a <= t <= show_b:
            p = ease((t-show_a)/0.3); q = 1 - ease((t-(show_b-0.3))/0.3) if t > show_b-0.3 else 1
            al = int(255*p*q)
            x1,y1 = tx(tg[0]*scale, tg[1]*scale); x2,y2 = tx((tg[0]+tg[2])*scale, (tg[1]+tg[3])*scale)
            pad = 8 + 6*(1-p)
            box = (x1-pad, y1-pad, x2+pad, y2+pad)
            if e.get("focus"):  # 聚光灯：框外压暗
                shade = Image.new("RGBA", canvas.size, (0,0,0,int(120*p*q)))
                mask = Image.new("L", canvas.size, 0); ImageDraw.Draw(mask).rounded_rectangle(box, radius=14, fill=255)
                shade.putalpha(Image.eval(mask, lambda v: 255-v).point(lambda v: int(v*(120*p*q)/255)))
                ov.alpha_composite(shade)
            pulse = 0.5 + 0.5*math.sin((t-show_a)*6)
            wlen = 5 if pulse > 0.5 else 4
            d.rounded_rectangle(box, radius=12, outline=ACC+(al,), width=wlen)
            lab = e.get("label") or ""
            if lab:
                f = font(40); w = d.textlength(lab, font=f); bw, bh = w+44, 66
                cwid, chei = canvas.size
                cy_ = min(max((box[1]+box[3])/2 - bh/2, 24), chei-bh-24)
                if box[2]+24+bw <= cwid-24:   bx, by = box[2]+24, cy_          # 右侧
                elif box[0]-24-bw >= 24:      bx, by = box[0]-24-bw, cy_       # 左侧
                else:
                    bx = min(max((box[0]+box[2])/2 - bw/2, 24), cwid-bw-24)
                    by = box[1]-bh-16 if box[1] > bh+60 else box[3]+16
                d.rounded_rectangle((bx,by,bx+bw,by+bh), radius=18, fill=INK+(int(235*p*q),))
                d.rounded_rectangle((bx,by,bx+10,by+bh), radius=5, fill=ACC+(al,))
                d.text((bx+26, by+9), lab, font=f, fill=(255,255,255,al))
        if e["kind"] == "click" and t0 <= t <= t0 + 0.6 and "x" in e:
            r = ease((t-t0)/0.6); px,py = tx(e["x"]*scale, e["y"]*scale)
            rad = 14 + 60*r; a = int(220*(1-r))
            d.ellipse((px-rad,py-rad,px+rad,py+rad), outline=(255,255,255,a), width=6)
            d.ellipse((px-rad*0.6,py-rad*0.6,px+rad*0.6,py+rad*0.6), outline=ACC+(a,), width=4)
    if speed_badge:
        f = font(36); w = d.textlength(speed_badge, font=f)
        d.rounded_rectangle((canvas.size[0]-w-90, 36, canvas.size[0]-36, 104), radius=20, fill=INK+(220,))
        d.text((canvas.size[0]-w-64, 46), speed_badge, font=f, fill=(255,255,255,255))
    canvas.alpha_composite(ov)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("out")
    ap.add_argument("--cfg"); ap.add_argument("--size", default="1920x1080"); ap.add_argument("--max-frames", type=int, default=0)
    a = ap.parse_args()
    OW, OH = map(int, a.size.split("x"))
    base = os.path.splitext(a.clip)[0]
    meta = json.load(open(base + ".meta.json")); ev = json.load(open(base + ".events.json"))
    cfg = json.load(open(a.cfg)) if a.cfg else {}
    ev = cfg.get("events_override", ev)
    W, H, fps, dur = probe(a.clip); scale = meta.get("scale") or (W / meta["region"][2])
    trim = cfg.get("trim", [0, dur]); speeds = cfg.get("speed", [])
    zdef = cfg.get("zoom_default", 1.7)
    for pt in cfg.get("patch", []):
        for e in ev:
            if pt["contains"] in (e.get("label") or ""): e.update(pt["set"])
    cam = Cam(W, H, build_zoom_segs(ev, W, H, scale, zdef, cfg.get("auto_zoom", True)))
    # 内容在输出里的适配（保持比例，居中，背景为模糊放大的自身画面）
    k_out = min(OW / W, OH / H); cw, ch = int(W*k_out), int(H*k_out); ox, oy = (OW-cw)//2, (OH-ch)//2
    # 输出帧 → 源时间 映射
    segs = sorted(speeds, key=lambda s: s["from"]); tmap = []; t = trim[0]; ot = 0.0; dt = 1.0/fps
    while t < trim[1]:
        f = 1.0; b = None
        for s in segs:
            if s["from"] <= t < s["to"]: f = s["factor"]; b = s["badge"] if "badge" in s else f"加速 {int(f)}x"
        tmap.append((t, b)); t += dt*f
    for _ in range(int(cfg.get("hold_end", 0)*fps)): tmap.append((trim[1]-dt, None))
    if a.max_frames: tmap = tmap[:a.max_frames]
    masks = meta.get("mask_regions", []) + cfg.get("masks_extra", [])
    for m in masks:
        for key, rng in cfg.get("mask_times", {}).items():
            if key in m.get("name", ""): m["t"] = rng
    rd = subprocess.Popen(["ffmpeg","-v","error","-i",a.clip,"-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{OW}x{OH}","-r",str(fps),"-i","-",
        "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",a.out], stdin=subprocess.PIPE)
    fsz = W*H*3; cur_i = -1; cur = None
    for (st, badge) in tmap:
        idx = int(round(st*fps))
        while cur_i < idx:
            buf = rd.stdout.read(fsz)
            if len(buf) < fsz: break
            cur = np.frombuffer(buf, np.uint8).reshape(H, W, 3); cur_i += 1
        if cur is None: break
        frame = cur.copy()
        for m in masks:
            if m.get("t"):
                rr = m["t"] if isinstance(m["t"][0], list) else [m["t"]]
                if not any(a_ <= st <= b_ for a_, b_ in rr): continue
            rx, ry, rw, rh = [int(v*scale) for v in m["rect"]]
            rx, ry = max(rx, 0), max(ry, 0); rx2, ry2 = min(rx+rw, W), min(ry+rh, H)
            if rx2 <= rx or ry2 <= ry: continue
            fill = m.get("style") == "fill" or "推广" in m.get("name","") or "活动" in m.get("name","") or any(k in m.get("name","") for k, v in cfg.get("mask_style", {}).items() if v == "fill")
            if fill:
                xs = rx-8 if rx >= 8 else min(rx2+8, W-1)
                col = np.median(frame[ry:ry2, xs:xs+1].reshape(-1,3), axis=0).astype(np.uint8)
                frame[ry:ry2, rx:rx2] = col
            else:
                reg = Image.fromarray(frame[ry:ry2, rx:rx2]).filter(ImageFilter.GaussianBlur(radius=16))
                frame[ry:ry2, rx:rx2] = np.array(reg)
        z, cx, cy = cam.at(st); w, h = W/z, H/z; x0, y0 = cx-w/2, cy-h/2
        im = Image.fromarray(frame)
        crop = im.crop((x0, y0, x0+w, y0+h)).resize((cw, ch), Image.LANCZOS)
        bg = im.resize((OW, OH), Image.BILINEAR).filter(ImageFilter.GaussianBlur(40)); bg = Image.eval(bg, lambda v: int(v*0.55))
        canvas = bg.convert("RGBA"); canvas.paste(crop, (ox, oy))
        draw_overlay(canvas, st, ev, (z, cx, cy), W, H, scale, ox, oy, k_out, badge)
        wr.stdin.write(canvas.convert("RGB").tobytes())
    wr.stdin.close(); wr.wait(); rd.kill()
    print("ok", len(tmap), "frames")

if __name__ == "__main__": main()
