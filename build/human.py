"""Human-like mouse/keyboard driver + screen recorder with event log.

All public coordinates are LOGICAL POINTS relative to REGION origin.
"""
import json, math, random, subprocess, time, os, signal, re
import Quartz
from Quartz import (CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap,
                    kCGEventMouseMoved, kCGEventLeftMouseDown, kCGEventLeftMouseUp,
                    kCGEventLeftMouseDragged, kCGMouseButtonLeft, CGPointMake,
                    CGEventCreateKeyboardEvent, CGEventKeyboardSetUnicodeString,
                    CGEventCreateScrollWheelEvent, kCGScrollEventUnitPixel,
                    CGEventCreate, CGEventGetLocation, CGEventSetIntegerValueField,
                    kCGMouseEventClickState)

REGION = (80, 40, 1440, 860)   # x, y, w, h  logical points
SCALE = 2
FPS = 30


def mono():
    return time.monotonic()


def ease(t):  # ease-in-out cubic
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def cur_pos():
    p = CGEventGetLocation(CGEventCreate(None))
    return p.x, p.y


def post(ev):
    CGEventPost(kCGHIDEventTap, ev)


class Human:
    def __init__(self, region=REGION):
        self.region = region
        self.ox, self.oy = region[0], region[1]
        self.events = []
        self.t0 = mono()

    # ---- logging
    def log(self, kind, x=None, y=None, target=None, label=None, text=None, dur=0.0, t=None):
        if x is None:
            gx, gy = cur_pos()
            x, y = gx - self.ox, gy - self.oy
        e = {"t": round((t if t is not None else mono()) - self.t0, 3), "kind": kind,
             "x": round(x, 1), "y": round(y, 1)}
        if target is not None:
            e["target"] = list(target)
        if label:
            e["label"] = label
        if text is not None:
            e["text"] = text
        e["dur"] = round(dur, 3)
        self.events.append(e)

    # ---- mouse
    def _warp(self, gx, gy, drag=False):
        t = kCGEventLeftMouseDragged if drag else kCGEventMouseMoved
        post(CGEventCreateMouseEvent(None, t, CGPointMake(gx, gy), kCGMouseButtonLeft))

    def move_to(self, x, y, dur=None, label=None, target=None, overshoot=True, drag=False, log=True):
        """x,y relative to region. Bezier w/ slight arc, overshoot-and-correct, ease-in-out."""
        sx, sy = cur_pos()
        ex, ey = x + self.ox, y + self.oy
        dist = math.hypot(ex - sx, ey - sy)
        if dur is None:
            dur = max(0.5, min(1.2, 0.35 + dist / 1400.0)) * random.uniform(0.92, 1.1)
        t_start = mono()
        if log:
            self.log("move", x, y, target, label, dur=dur, t=t_start)
        if dist < 3:
            time.sleep(0.05)
            return
        # control points for arc
        nx, ny = -(ey - sy) / dist, (ex - sx) / dist
        arc = random.uniform(-0.12, 0.12) * dist
        use_over = overshoot and dist > 160
        if use_over:
            od = random.uniform(6, 14)
            ux, uy = (ex - sx) / dist, (ey - sy) / dist
            tx, ty = ex + ux * od, ey + uy * od
        else:
            tx, ty = ex, ey
        c1 = (sx + (tx - sx) * 0.3 + nx * arc, sy + (ty - sy) * 0.3 + ny * arc)
        c2 = (sx + (tx - sx) * 0.75 + nx * arc * 0.5, sy + (ty - sy) * 0.75 + ny * arc * 0.5)
        main_dur = dur * (0.85 if use_over else 1.0)
        n = max(12, int(main_dur * 120))
        for i in range(1, n + 1):
            u = ease(i / n)
            bx = ((1 - u) ** 3) * sx + 3 * ((1 - u) ** 2) * u * c1[0] + 3 * (1 - u) * u * u * c2[0] + u ** 3 * tx
            by = ((1 - u) ** 3) * sy + 3 * ((1 - u) ** 2) * u * c1[1] + 3 * (1 - u) * u * u * c2[1] + u ** 3 * ty
            bx += random.uniform(-0.25, 0.25)
            by += random.uniform(-0.25, 0.25)
            self._warp(bx, by, drag)
            time.sleep(main_dur / n)
        if use_over:
            m = max(8, int(dur * 0.15 * 120))
            for i in range(1, m + 1):
                u = ease(i / m)
                self._warp(tx + (ex - tx) * u, ty + (ey - ty) * u, drag)
                time.sleep(dur * 0.15 / m)
        self._warp(ex, ey, drag)

    def sync(self, x, y):
        """instant cursor jump used as the video/event sync marker"""
        self._warp(x + self.ox, y + self.oy)
        self.log("sync", x, y, label="同步标记(光标跳入)")

    def jitter(self, secs, amp=2.5, label=None):
        """small idle movement"""
        t_end = mono() + secs
        x0, y0 = cur_pos()
        self.log("wait", dur=secs, label=label)
        while mono() < t_end:
            self._warp(x0 + random.uniform(-amp, amp), y0 + random.uniform(-amp, amp))
            time.sleep(random.uniform(0.25, 0.6))

    def pause(self, a, b=None, label=None):
        d = random.uniform(a, b) if b else a
        self.log("wait", dur=d, label=label)
        time.sleep(d)

    def click(self, label=None, target=None, hold=0.07):
        gx, gy = cur_pos()
        t = mono()
        self.log("click", gx - self.ox, gy - self.oy, target, label, dur=hold, t=t)
        p = CGPointMake(gx, gy)
        d = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, p, kCGMouseButtonLeft)
        CGEventSetIntegerValueField(d, kCGMouseEventClickState, 1)
        post(d)
        time.sleep(hold + random.uniform(0, 0.04))
        u = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, p, kCGMouseButtonLeft)
        CGEventSetIntegerValueField(u, kCGMouseEventClickState, 1)
        post(u)

    def go_click(self, x, y, label=None, target=None, pre=None, post_wait=None):
        """move, dwell 0.2-0.5, click, wait 0.6-1.5"""
        self.move_to(x, y, label=label, target=target)
        time.sleep(random.uniform(0.2, 0.5) if pre is None else pre)
        self.click(label, target)
        time.sleep(random.uniform(0.6, 1.5) if post_wait is None else post_wait)

    def mouse_down(self):
        gx, gy = cur_pos()
        post(CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, CGPointMake(gx, gy), kCGMouseButtonLeft))

    def mouse_up(self):
        gx, gy = cur_pos()
        post(CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, CGPointMake(gx, gy), kCGMouseButtonLeft))

    # ---- keyboard
    def _type_char(self, ch):
        for down in (True, False):
            ev = CGEventCreateKeyboardEvent(None, 0, down)
            CGEventKeyboardSetUnicodeString(ev, len(ch), ch)
            post(ev)
            time.sleep(0.004)

    def type_text(self, text, cps=(7, 10), label=None, target=None):
        t = mono()
        self.log("type", target=target, label=label, text=text, dur=len(text) / 8.5, t=t)
        for i, ch in enumerate(text):
            self._type_char(ch)
            base = 1.0 / random.uniform(*cps)
            d = base * random.uniform(0.6, 1.5)
            if ch in "，。,.、：:" and random.random() < 0.7:
                d += random.uniform(0.25, 0.7)
            elif random.random() < 0.04:
                d += random.uniform(0.3, 0.8)
            time.sleep(d)

    def key(self, code, flags=0):
        for down in (True, False):
            ev = CGEventCreateKeyboardEvent(None, code, down)
            Quartz.CGEventSetFlags(ev, flags if down else 0)   # 抬起时清掉修饰键，避免 ⌘ 卡住
            post(ev)
            time.sleep(0.02)
        if flags:   # 同时补发修饰键抬起
            for mc in (55, 56, 58, 59):
                ev = CGEventCreateKeyboardEvent(None, mc, False); Quartz.CGEventSetFlags(ev, 0); post(ev)

    def esc(self):
        self.key(53)

    # ---- scroll
    def scroll(self, total_px, dur=2.0, label=None, target=None):
        """total_px>0 scrolls content up (view moves down). Small steps with inertia."""
        self.log("scroll", target=target, label=label, text=str(total_px), dur=dur)
        n = max(10, int(dur * 40))
        done = 0
        for i in range(1, n + 1):
            u = ease(i / n)
            want = int(total_px * u)
            step = want - done
            done = want
            if step:
                post(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 1, -step))
            time.sleep(dur / n)
        # inertia tail
        tail = abs(total_px) * 0.04
        s = 1 if total_px > 0 else -1
        for k in range(8):
            st = int(tail * (0.6 ** k))
            if st:
                post(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 1, -s * st))
            time.sleep(0.03)


class Recorder:
    """ffmpeg avfoundation screen capture (3840x2160 source) cropped to REGION."""

    def __init__(self, out_mov, region=REGION, hw=True):
        self.out = out_mov
        self.region = region
        x, y, w, h = region
        cx, cy, cw, ch = x * SCALE, y * SCALE, w * SCALE, h * SCALE
        vcodec = ["-c:v", "h264_videotoolbox", "-b:v", "16M", "-realtime", "1"] if hw else \
                 ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18"]
        self.cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "avfoundation",
                    "-capture_cursor", "1", "-capture_mouse_clicks", "1", "-framerate", str(FPS),
                    "-pixel_format", "uyvy422", "-i", "1:none".replace("1", "0"),
                    "-vf", f"crop={cw}:{ch}:{cx}:{cy},fps={FPS}"] + vcodec + \
                   ["-pix_fmt", "yuv420p", "-tag:v", "avc1", "-movflags", "+faststart", out_mov]
        self.p = None
        self.t_launch = None

    def start(self):
        self.t_launch = mono()
        self.p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE)
        return self.t_launch

    def stop(self):
        try:
            self.p.stdin.write(b"q")
            self.p.stdin.flush()
        except Exception:
            pass
        try:
            self.p.wait(timeout=30)
        except Exception:
            self.p.send_signal(signal.SIGINT)
            self.p.wait(timeout=30)


def detect_first_change(mov, cx, cy, size=70):
    """Return video time (s) at which the cursor first leaves its parked spot.
    cx, cy in region logical points; analyses a small crop around it."""
    px, py = int(cx * SCALE), int(cy * SCALE)
    half = size
    x0, y0 = max(0, px - half), max(0, py - half)
    cmd = ["ffmpeg", "-hide_banner", "-i", mov, "-vf",
           f"crop={half*2}:{half*2}:{x0}:{y0},select='gt(scene,0.004)',showinfo",
           "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ts = [float(m.group(1)) for m in re.finditer(r"pts_time:([0-9.]+)", r.stderr)]
    return ts


def probe(mov):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", mov],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def finalize(name, rec, human, sync_pos, region=REGION, extra_meta=None, outdir="../footage/ep01"):
    """Stop recorder is done by caller. Computes start-delay via cursor sync and writes json."""
    mov = rec.out
    pr = probe(mov)
    st = pr["streams"][0]
    dur = float(pr["format"]["duration"])
    ts = detect_first_change(mov, sync_pos[0], sync_pos[1])
    # first move event in human log
    first_move = next(e for e in human.events if e["kind"] == "sync")
    t_move_log = first_move["t"]            # relative to human.t0 (== rec.t_launch if aligned)
    t_move_vid = ts[0] if ts else None
    delay = None
    if t_move_vid is not None:
        delay = (t_move_log + (human.t0 - rec.t_launch)) - t_move_vid   # = start delay of video wrt launch
    # shift: video_time = log_time + (human.t0 - rec.t_launch) - delay
    shift = (human.t0 - rec.t_launch) - (delay or 0.0)
    evs = []
    for e in human.events:
        e2 = dict(e)
        e2["t"] = round(max(0.0, e["t"] + shift), 3)
        if e["kind"] == "sync":
            continue
        evs.append(e2)
    meta = {"region": list(region), "video_size": [st["width"], st["height"]], "scale": SCALE,
            "fps": FPS, "duration": round(dur, 2),
            "t0": "events.t = seconds from first video frame; aligned via cursor-leave sync "
                  f"(measured start delay {None if delay is None else round(delay,3)}s)",
            "sync_detect_ts": ts[:3]}
    if extra_meta:
        meta.update(extra_meta)
    base = mov[:-4]
    json.dump(evs, open(base + ".events.json", "w"), ensure_ascii=False, indent=1)
    json.dump(meta, open(base + ".meta.json", "w"), ensure_ascii=False, indent=1)
    return meta


import sys
def _inputsrc(*a):
    return subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputsrc.py"), *a], capture_output=True, text=True).stdout.strip()


def scene(name, fn, park=(900, 760), pre_wait=1.5, outdir="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep01", extra=None):
    """Record `fn(h)` as footage/ep01/<name>.mov with events/meta. Cursor first parked off-spot then sync-jumped."""
    mov = os.path.join(outdir, name + ".mov")
    prev_src = _inputsrc("current")          # 录制期间切到 ABC（中文输入法会吞掉合成的字符），结束后切回
    if prev_src and prev_src != "com.apple.keylayout.ABC": _inputsrc("select", "com.apple.keylayout.ABC")
    h = Human(); rec = Recorder(mov)
    h.move_to(park[0] - 200, park[1] - 120, dur=0.3, log=False)   # start elsewhere
    time.sleep(0.3)
    rec.start(); h.t0 = rec.t_launch
    time.sleep(pre_wait)
    h.sync(*park)
    time.sleep(1.0)
    err = None
    try:
        fn(h)
    except Exception as e:
        err = e
    time.sleep(1.0)
    rec.stop()
    if prev_src and prev_src != "com.apple.keylayout.ABC": _inputsrc("select", prev_src)
    meta = finalize(name, rec, h, park, extra_meta=extra)
    print(name, meta)
    if err:
        raise err
    return h
