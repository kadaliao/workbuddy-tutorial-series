import sys; sys.path.insert(0,'.')
from human import *
import ocr
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep04"
class Abort(Exception): pass
def C(b): return b[0]+b[2]/2, b[1]+b[3]/2
def F(h):
    h.pause(0.8)
    ind=ocr.find("仅问答",region=[450,440,800,60])
    if not ind: raise Abort("no indicator")
    x,y=560,474; h.move_to(x,y,dur=0.8,target=[512,460,80,28],label="输入框里的模式标识"); h.pause(1.6)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/fx.png"])
    h.log("mark",text="hover")
    h.move_to(522,474,dur=0.5,target=[512,462,22,24],label="点 × 退出"); h.pause(0.6); h.click(); h.log("mark",text="exit"); h.pause(1.6)
    if ocr.find("仅问答",region=[450,440,800,60]): raise Abort("still on")
    h.move_to(800,600,dur=0.6); h.pause(1.0)
def setup():
    subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
    h=Human(); h.move_to(76,124); h.click(); time.sleep(1.8)
    if ocr.find("活动"): h.move_to(1210,176); h.click(); time.sleep(0.6)
    h.move_to(482,473,dur=0.5); time.sleep(0.3); h.click(); time.sleep(1.0)
    b=ocr.find("模式",exact=True,region=[440,150,300,330]); x,y=C(b); h.move_to(x+20,y); time.sleep(0.8); h.move_to(720,y); time.sleep(0.6)
    q=ocr.find("仅问答",exact=True,region=[640,150,300,330]); h.move_to(q[0]+152,q[1]+q[3]/2); time.sleep(0.5); h.click(); time.sleep(0.8)
    h.esc(); time.sleep(0.4); h.esc(); time.sleep(0.6)
    assert not ocr.find("工程师")
scene("F-退出模式",F,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
