"""屏幕文字定位：find(text) → 录制区域内逻辑坐标 (x,y,w,h)；all_text() 列出识别结果。"""
import subprocess, Vision, Quartz
from Foundation import NSURL
REGION = (80, 40, 1440, 860)
def _shot(p="/private/tmp/claude-501/ocr.png"):
    x, y, w, h = REGION
    subprocess.run(["screencapture", "-x", f"-R{x},{y},{w},{h}", p], check=True); return p
def all_text(p=None):
    p = p or _shot()
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLanguages_(["zh-Hans", "en-US"]); req.setRecognitionLevel_(0); req.setUsesLanguageCorrection_(False)
    h = Vision.VNImageRequestHandler.alloc().initWithURL_options_(NSURL.fileURLWithPath_(p), None)
    h.performRequests_error_([req], None)
    out = []
    W, H = REGION[2], REGION[3]
    for r in req.results() or []:
        c = r.topCandidates_(1)[0]; bb = r.boundingBox()
        x = bb.origin.x * W; y = (1 - bb.origin.y - bb.size.height) * H
        out.append((str(c.string()), (round(x), round(y), round(bb.size.width * W), round(bb.size.height * H))))
    return out
import re
def _norm(s):  # 去掉图标被识别成的前缀（如“口 ”“13 ”“+ ”）和尾部的 ～ 〈 >
    s = s.strip()
    m = re.match(r"^(\S+)\s+(\S.*)$", s)
    if m and (len(m.group(1)) == 1 or (len(m.group(1)) <= 3 and not re.search(r"[\u4e00-\u9fff]", m.group(1)))):
        s = m.group(2)
    return s.strip(" ～~〈>＞")
def find(text, exact=False, p=None, region=None):
    for s, box in all_text(p):
        n = _norm(s)
        if (n == text or n.split(" ")[0] == text) if exact else (text in s):
            if region:
                x, y, w, h = region
                if not (x <= box[0] <= x + w and y <= box[1] <= y + h): continue
            return box
    return None
if __name__ == "__main__":
    for s, b in all_text(): print(b, s)
