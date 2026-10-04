"""通用：新建任务页 + 用“打开本地文件夹”选定某个目录作为工作空间（OCR 校验）。"""
import sys, os, time, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from human import *
import ocr
def C(b): return b[0]+b[2]/2, b[1]+b[3]/2
def new_task(h):
    subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
    h.move_to(76,124); h.click(); time.sleep(1.8)
    if ocr.find("活动"): h.move_to(1210,176); h.click(); time.sleep(0.6)
def pick_folder(h, path):
    name = os.path.basename(path.rstrip("/"))
    h.move_to(531,521); h.click(); time.sleep(1.2)
    w = ocr.find(name, exact=True, region=[440,100,300,420])
    if w:
        h.move_to(*C(w)); h.click(); time.sleep(1.0)
    else:
        o = ocr.find("打开本地文件夹", exact=True, region=[440,100,300,420]); h.move_to(*C(o)); h.click(); time.sleep(2.2)
        old = subprocess.run(["pbpaste"], capture_output=True).stdout
        subprocess.run(["pbcopy"], input=(path.rstrip("/")+"/").encode())
        Cm=Quartz.kCGEventFlagMaskCommand; SH=Quartz.kCGEventFlagMaskShift
        h.key(5, Cm|SH); time.sleep(1.0); h.key(9, Cm); time.sleep(1.0)
        subprocess.run(["osascript","-e",'tell application "System Events" to key code 36']); time.sleep(1.8)
        subprocess.run(["pbcopy"], input=old)
        h.move_to(1103,621); h.click(); time.sleep(1.6)
    ok = ocr.find(name, region=[440,500,400,40])
    assert ok, f"workspace {name} not selected"
    return ok
