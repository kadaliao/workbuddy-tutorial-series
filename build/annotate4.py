#!/usr/bin/env python3
"""第1集 v4 标注渲染：录屏/静帧 → 舞台画面（下方留字幕条），带推近、高亮框、聚光灯、标注、提示面板、加速角标、隐私遮挡。
用法: annotate4.py clip.(mov|png) out.mp4 --cfg cfg.json
mov 需同目录 clip.meta.json / clip.events.json（坐标为相对录制区域的逻辑点）；png 的坐标为像素（scale=1）。
cfg 主要字段:
  anchors: [[src_t, out_t], ...] 分段线性时间映射（src 可相等表示定格）；不给则用 trim + speed（同 annotate.py）
  events_override / events_shift / events_extra / drop_labels / patch / auto_zoom / zoom_default
  cam_fixed: [x,y,w,h] 固定镜头框住该区域
  masks_extra: [{rect, t:[[a,b]], style: blur|fillmed}]   mask_times: {名字关键词: [[a,b]]}
  badges: [{from, to, text, t0}]  text 可含 {real}（= src - t0，m:ss）
  notes: [{out:[a,b], x, y, title, lines:[[text, out_t], ...]}]  按输出时间显示的提示面板（舞台坐标）
"""
import sys, os, json, math, subprocess, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
ACC = (255, 176, 32); INK = (20, 24, 31); BG = (20, 24, 31)
STAGE = (156, 10, 1608, 960)  # 内容区；下方 970~1080 为字幕条

def ease(x):
    x = max(0.0, min(1.0, x)); return x*x*x*(x*(x*6-15)+10)

def font(sz): return ImageFont.truetype(FONT, sz)

def probe(path):
    o = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height,r_frame_rate,duration","-of","json",path])
    s = json.loads(o)["streams"][0]; n, d = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(n)/float(d), float(s.get("duration") or 0)

class Cam:
    def __init__(self, W, H, segs, fixed=None, keys=None, scale=1):
        self.W, self.H, self.segs, self.fixed, self.scale = W, H, segs, fixed, scale
        self.keys = [(k[0], self.rect(k[1:])) for k in keys] if keys else None
    def rect(self, r):
        x, y, w, h = r; s = self.scale
        return (min(self.W/(w*s), self.H/(h*s)), (x+w/2)*s, (y+h/2)*s)
    def clamp(self, z, cx, cy):
        w, h = self.W/z, self.H/z
        return z, min(max(cx, w/2), self.W-w/2), min(max(cy, h/2), self.H-h/2)
    def at(self, t):
        if self.fixed: return self.clamp(*self.fixed)
        if self.keys:
            K = self.keys
            if t <= K[0][0]: return self.clamp(*K[0][1])
            for (t0, a), (t1, b) in zip(K, K[1:]):
                if t0 <= t <= t1:
                    k = ease((t-t0)/(t1-t0)) if t1 > t0 else 1.0
                    z = a[0] * (b[0]/a[0])**k
                    return self.clamp(z, a[1] + (b[1]-a[1])*k, a[2] + (b[2]-a[2])*k)
            return self.clamp(*K[-1][1])
        z, cx, cy = 1.0, self.W/2, self.H/2
        for s in self.segs:
            a, b, ti, to = s["t_in"], s["t_out"], s["ease_in"], s["ease_out"]
            if t < a - ti or t > b + to: continue
            k = ease((t-(a-ti))/ti) if t < a else (1.0 if t <= b else 1 - ease((t-b)/to))
            zz = 1 + (s["zoom"]-1)*k
            z = zz if z == 1.0 else max(z, zz)
            cx = cx + (s["cx"]-cx)*k; cy = cy + (s["cy"]-cy)*k
        return self.clamp(z, cx, cy)

def build_zoom_segs(events, W, H, scale, zdef, auto_on=True):
    segs = []
    for e in events:
        tg = e.get("target"); zm = e.get("zoom")
        if not tg or zm is False: continue
        auto = auto_on and e["kind"] in ("click","type") and (tg[2]*tg[3] < 0.18*(W/scale)*(H/scale))
        if zm is None and not auto: continue
        z = zdef if zm in (None, True) else float(zm)
        cx = (tg[0]+tg[2]/2)*scale; cy = (tg[1]+tg[3]/2)*scale
        z = min(z, 0.7*W/max(tg[2]*scale, 1), 0.7*H/max(tg[3]*scale, 1)); z = max(z, 1.25)
        t0 = e["t"]; d = e.get("dur", 1.2)
        segs.append(dict(t_in=t0-0.1, t_out=t0+max(d, 1.0)+0.4, ease_in=0.7, ease_out=0.8, zoom=z, cx=cx, cy=cy))
    segs.sort(key=lambda s: s["t_in"]); out = []
    for s in segs:
        if out and s["t_in"] - out[-1]["t_out"] < 0.9:
            out[-1]["t_out"] = max(out[-1]["t_out"], s["t_out"]); out[-1].update(cx=s["cx"], cy=s["cy"], zoom=s["zoom"])
        else: out.append(s)
    return out

def label_box(d, box, lab, stage, al, p, q, side=None, dx=0):
    f = font(38); w = d.textlength(lab, font=f); bw, bh = w+44, 62
    L, T_, R, Bt = stage[0]+16, stage[1]+12, stage[0]+stage[2]-16, stage[1]+stage[3]-12
    cy_ = min(max((box[1]+box[3])/2 - bh/2, T_), Bt-bh)
    cx_ = min(max((box[0]+box[2])/2 - bw/2, L), R-bw)
    if side == "bottom":                 bx, by = cx_, min(box[3]+14, Bt-bh)
    elif side == "top":                  bx, by = cx_, max(box[1]-bh-14, T_)
    elif box[2]+22+dx+bw <= R and side != "left":  bx, by = box[2]+22+dx, cy_
    elif box[0]-22-bw >= L:              bx, by = box[0]-22-bw, cy_
    else:                                bx, by = cx_, (box[1]-bh-14 if box[1]-bh-14 >= T_ else min(box[3]+14, Bt-bh))
    d.rounded_rectangle((bx,by,bx+bw,by+bh), radius=16, fill=INK+(int(235*p*q),))
    d.rounded_rectangle((bx,by,bx+9,by+bh), radius=4, fill=ACC+(al,))
    d.text((bx+26, by+9), lab, font=f, fill=(255,255,255,al))

def draw_overlay(canvas, t, ot, events, cam_state, W, H, scale, ox, oy, k_out, badge, notes, stage):
    z, cx, cy = cam_state
    def tx(px, py): return ox + (px - (cx - W/z/2))*z*k_out, oy + (py - (cy - H/z/2))*z*k_out
    ov = Image.new("RGBA", canvas.size, (0,0,0,0)); d = ImageDraw.Draw(ov)
    ch_lim = stage[1] + stage[3]
    for e in events:
        tg = e.get("target"); t0 = e["t"]; dur = e.get("dur", 1.2)
        a, b = t0 - 0.25, t0 + dur + 0.8
        if tg and e.get("label") is not None and a <= t <= b:
            p = ease((t-a)/0.3); q = 1 - ease((t-(b-0.3))/0.3) if t > b-0.3 else 1; al = int(255*p*q)
            x1, y1 = tx(tg[0]*scale, tg[1]*scale); x2, y2 = tx((tg[0]+tg[2])*scale, (tg[1]+tg[3])*scale)
            pad = 8 + 6*(1-p); box = (x1-pad, y1-pad, x2+pad, y2+pad)
            if e.get("focus"):
                m = Image.new("L", canvas.size, int(120*p*q)); ImageDraw.Draw(m).rounded_rectangle(box, radius=14, fill=0)
                shade = Image.new("RGBA", canvas.size, (0,0,0,0)); shade.putalpha(m); ov.alpha_composite(shade)
            d.rounded_rectangle(box, radius=12, outline=ACC+(al,), width=5 if math.sin((t-a)*6) > 0 else 4)
            if e.get("label"): label_box(d, box, e["label"], stage, al, p, q, e.get("side"), e.get("dx", 0))
        if e["kind"] == "click" and t0 <= t <= t0 + 0.6 and "x" in e:
            r = ease((t-t0)/0.6); px, py = tx(e["x"]*scale, e["y"]*scale); rad = 14 + 60*r; a_ = int(220*(1-r))
            d.ellipse((px-rad,py-rad,px+rad,py+rad), outline=(255,255,255,a_), width=6)
            d.ellipse((px-rad*0.6,py-rad*0.6,px+rad*0.6,py+rad*0.6), outline=ACC+(a_,), width=4)
    for n in notes:
        a, b = n["out"]
        if not (a <= ot <= b): continue
        p = ease((ot-a)/0.35); q = 1 - ease((ot-(b-0.35))/0.35) if ot > b-0.35 else 1; al = int(255*p*q)
        ft, fl = font(40), font(36); x, y = n["x"], n["y"]
        rows = [l for l in n["lines"] if ot >= l[1]]
        wmax = max([d.textlength(n["title"], font=ft)] + [d.textlength(l[0] + (l[2] if len(l) > 2 else ""), font=fl) + 40 for l in n["lines"]]) + 60
        hh = 76 + 58*len(n["lines"])
        d.rounded_rectangle((x, y, x+wmax, y+hh), radius=20, fill=INK+(int(238*p*q),))
        d.rounded_rectangle((x, y, x+10, y+hh), radius=5, fill=ACC+(al,))
        d.text((x+30, y+18), n["title"], font=ft, fill=ACC+(al,))
        for i, l in enumerate(rows):
            k = ease((ot-l[1])/0.3)
            d.text((x+30 + (1-k)*16, y+76+58*i), l[0], font=fl, fill=(255,255,255,int(al*k)))
            if len(l) > 3 and ot >= l[3]:
                k2 = ease((ot-l[3])/0.3); xr = x+30+d.textlength(l[0], font=fl)+28
                d.text((xr + (1-k2)*16, y+76+58*i), l[2], font=fl, fill=tuple(l[4])+(int(al*k2),))
    if badge:
        f = font(34); w = d.textlength(badge, font=f); rx = stage[0]+stage[2]-24; ry = stage[1]+24
        d.rounded_rectangle((rx-w-52, ry, rx, ry+62), radius=18, fill=INK+(225,))
        d.ellipse((rx-w-36, ry+24, rx-w-22, ry+38), fill=ACC+(255,))
        d.text((rx-w-12, ry+10), badge, font=f, fill=(255,255,255,255))
    canvas.alpha_composite(ov)

def build_tmap(cfg, fps, dur):
    if "anchors" in cfg:
        A = cfg["anchors"]; n = int(round(A[-1][1]*fps)); out = []
        assert A[0][1] == 0, f"anchors must start at output 0, got {A[0]}"
        assert all(b[0] >= a[0] for a, b in zip(A, A[1:])), "source times must not go backwards"
        for i in range(n):
            ot = i/fps
            for (s0,o0),(s1,o1) in zip(A, A[1:]):
                if o0 <= ot <= o1:
                    st = s0 if o1 == o0 else s0 + (s1-s0)*(ot-o0)/(o1-o0); break
            else: st = A[-1][0]
            out.append(st)
        return out
    trim = cfg.get("trim", [0, dur]); segs = sorted(cfg.get("speed", []), key=lambda s: s["from"])
    out = []; t = trim[0]; dt = 1.0/fps
    while t < trim[1]:
        f = next((s["factor"] for s in segs if s["from"] <= t < s["to"]), 1.0); out.append(t); t += dt*f
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("out"); ap.add_argument("--cfg")
    a = ap.parse_args(); cfg = json.load(open(a.cfg)) if a.cfg else {}
    OW, OH = 1920, 1080; stage = cfg.get("stage", STAGE)
    is_png = a.clip.lower().endswith(".png")
    if is_png:
        img = np.array(Image.open(a.clip).convert("RGB")); H, W = img.shape[:2]; fps = 30.0; dur = 1e9
        meta = {"scale": 1}; ev = []
    else:
        base = os.path.splitext(a.clip)[0]
        meta = json.load(open(base + ".meta.json")); ev = json.load(open(base + ".events.json"))
        W, H, fps, dur = probe(a.clip)
    scale = meta.get("scale") or 1
    ev = cfg.get("events_override", ev)
    sh = cfg.get("events_shift", 0)
    ev = [dict(e, t=e["t"]+sh) for e in ev] + cfg.get("events_extra", [])
    ev = [e for e in ev if not any(a_ <= e["t"] <= b_ for a_, b_ in cfg.get("drop_events_t", []))]
    for e in ev:
        if any(k in (e.get("label") or "") for k in cfg.get("drop_labels", [])): e.pop("label", None)
    for pt in cfg.get("patch", []):
        for e in ev:
            if pt["contains"] in (e.get("label") or ""): e.update(pt["set"])
    fixed = None
    if cfg.get("cam_fixed"):
        x, y, w, h = cfg["cam_fixed"]; z = min(W/(w*scale), H/(h*scale)); fixed = (z, (x+w/2)*scale, (y+h/2)*scale)
    cam = Cam(W, H, build_zoom_segs(ev, W, H, scale, cfg.get("zoom_default", 1.7), cfg.get("auto_zoom", False)), fixed, cfg.get("cam_keys"), scale)
    sx, sy, sw, shh = stage; k_out = min(sw/W, shh/H); cw, ch = int(W*k_out), int(H*k_out)
    ox, oy = sx + (sw-cw)//2, sy + (shh-ch)//2
    tmap = build_tmap(cfg, fps, dur)
    masks = [] if is_png else [dict(m) for m in meta.get("mask_regions", []) if m["rect"][2] > 0]
    masks = [m for m in masks if not any(k in m.get("name", "") for k in cfg.get("drop_masks", []))]
    masks += cfg.get("masks_extra", [])
    for m in masks:
        for key, rng in cfg.get("mask_times", {}).items():
            if key in m.get("name", ""): m["t"] = rng
        for key, sty in cfg.get("mask_style", {}).items():
            if key in m.get("name", ""): m["style"] = sty
    # 舞台底板：纯色 + 内容区阴影 + 圆角遮罩
    base_bg = Image.new("RGBA", (OW, OH), BG+(255,))
    sh_ = Image.new("L", (OW, OH), 0); ImageDraw.Draw(sh_).rounded_rectangle((ox, oy+6, ox+cw, oy+ch+6), radius=16, fill=150)
    shadow = Image.new("RGBA", (OW, OH), (0,0,0,0)); shadow.putalpha(sh_.filter(ImageFilter.GaussianBlur(14))); base_bg.alpha_composite(shadow)
    rmask = Image.new("L", (cw, ch), 0); ImageDraw.Draw(rmask).rounded_rectangle((0,0,cw-1,ch-1), radius=16, fill=255)
    notes = cfg.get("notes", []); badges = cfg.get("badges", [])
    rd = None if is_png else subprocess.Popen(["ffmpeg","-v","error","-i",a.clip,"-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{OW}x{OH}","-r","30","-i","-",
        "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",a.out], stdin=subprocess.PIPE)
    fsz = W*H*3; cur_i = -1; cur = img if is_png else None
    for oi, st in enumerate(tmap):
        ot = oi/30.0
        if not is_png:
            idx = int(round(st*fps))
            while cur_i < idx:
                buf = rd.stdout.read(fsz)
                if len(buf) < fsz: break
                cur = np.frombuffer(buf, np.uint8).reshape(H, W, 3); cur_i += 1
        frame = cur.copy()
        for m in masks:
            if m.get("t"):
                rr = m["t"] if isinstance(m["t"][0], list) else [m["t"]]
                if not any(a_ <= st <= b_ for a_, b_ in rr): continue
            rx, ry, rw, rh = [int(v*scale) for v in m["rect"]]
            rx, ry = max(rx, 0), max(ry, 0); rx2, ry2 = min(rx+rw, W), min(ry+rh, H)
            if rx2 <= rx or ry2 <= ry: continue
            sty = m.get("style", "fillmed")
            if sty == "fill":
                frame[ry:ry2, rx:rx2] = np.array(m.get("color", [255,255,255]), np.uint8)
            elif sty == "fillmed":
                frame[ry:ry2, rx:rx2] = np.median(frame[ry:ry2, rx:rx2].reshape(-1,3), axis=0).astype(np.uint8)
            else:
                frame[ry:ry2, rx:rx2] = np.array(Image.fromarray(frame[ry:ry2, rx:rx2]).filter(ImageFilter.GaussianBlur(16)))
        z, cx, cy = cam.at(st); w, h = W/z, H/z; x0, y0 = cx-w/2, cy-h/2
        crop = Image.fromarray(frame).crop((x0, y0, x0+w, y0+h)).resize((cw, ch), Image.LANCZOS)
        canvas = base_bg.copy(); canvas.paste(crop, (ox, oy), rmask)
        badge = None
        for b in badges:
            if b["from"] <= st < b["to"]:
                r = max(0, st - b.get("t0", 0)); badge = b["text"].replace("{real}", f"{int(r//60)}:{int(r%60):02d}")
        draw_overlay(canvas, st, ot, ev, (z, cx, cy), W, H, scale, ox, oy, k_out, badge, notes, stage)
        wr.stdin.write(canvas.convert("RGB").tobytes())
    wr.stdin.close(); wr.wait()
    if rd: rd.kill()
    print("ok", len(tmap), "frames", a.out)

if __name__ == "__main__": main()
