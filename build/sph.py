import sys, os, time, subprocess, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from human import *
import ocr
ocr.REGION=(0,0,1920,1080)
V="/Volumes/Data-External/workspace/cc-test/wbd/video"
def C(b): return b[0]+b[2]/2, b[1]+b[3]/2
H=Human(region=(0,0,1920,1080))
def shot(name):
    subprocess.run(["screencapture","-x",f"/private/tmp/claude-501/{name}.png"])
def paste(text):
    old=subprocess.run(["pbpaste"],capture_output=True).stdout
    subprocess.run(["pbcopy"],input=text.encode()); time.sleep(0.2)
    H.key(9, Quartz.kCGEventFlagMaskCommand); time.sleep(0.4)
    subprocess.run(["pbcopy"],input=old)
def find(t, region=None, exact=False, tries=1, wait=0.8):
    for _ in range(tries):
        b=ocr.find(t, exact=exact, region=region)
        if b: return b
        time.sleep(wait)
    return None
def choose_file(path):
    time.sleep(1.5)
    H.key(5, Quartz.kCGEventFlagMaskCommand|Quartz.kCGEventFlagMaskShift); time.sleep(1.0)
    paste(path); time.sleep(0.8)
    subprocess.run(["osascript","-e",'tell application "System Events" to key code 36']); time.sleep(1.2)
    subprocess.run(["osascript","-e",'tell application "System Events" to key code 36']); time.sleep(2.5)
def cover(edit_xy, path):
    H.move_to(*edit_xy,dur=0.4); H.click(); time.sleep(2.0)
    d=find("直接编辑")
    if d: H.move_to(*C(d),dur=0.4); H.click(); time.sleep(2.0)
    b=find("上传封面",tries=3)
    if not b: raise RuntimeError("cover editor not open")
    H.move_to(b[0]+b[2]/2, b[1]-40, dur=0.4); H.click(); choose_file(path)
    b=find("确认",exact=True,region=[1600,800,250,100],tries=3)
    H.move_to(*C(b),dur=0.4); H.click(); time.sleep(1.5)
def scroll_down(n=10):
    H.move_to(1700,750,dur=0.3); time.sleep(0.2)
    for i in range(n):
        post(CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitPixel, 1, -100)); time.sleep(0.06)
    time.sleep(0.8)
