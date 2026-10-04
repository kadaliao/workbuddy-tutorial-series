import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep05"
R=[855,150,585,680]
def hover(h, text, label, w=None, pad=6, hold=2.6):
    b=ocr.find(text, region=R)
    if not b: print("MISS", text); return
    x,y=C(b); ww = w or b[2]
    h.move_to(b[0]+min(ww,b[2])/2, y, dur=0.8, target=[b[0]-pad, b[1]-pad, ww+2*pad, b[3]+2*pad], label=label); h.pause(hold)
    h.log("mark", text="hover:"+text)
def B(h):
    h.pause(0.8)
    h.move_to(1140,500,dur=0.6); h.scroll(-4000,dur=1.0); h.pause(0.6); h.scroll(180,dur=1.2); h.pause(1.2)
    b=ocr.find("客户投诉数", region=[900,500,500,300])
    if b: h.move_to(1100,b[1]+8,dur=0.8,target=[b[0]-8,b[1]-8,400,b[3]+16],label="① 数字：没补数，标了“未填报”"); h.pause(2.8); h.log("mark",text="hover:未填报")
    else: print("MISS table")
    hover(h, "均在当周", "② 来源：日报里没这句", w=420)
    hover(h, "恢复线上", "② 日报里也没这句", w=420)
    h.move_to(1140,500,dur=0.5); h.scroll(520,dur=1.6); h.pause(1.4)
    hover(h, "多家比价", "② 材料只说“需要再比价”", w=140)
    hover(h, "补齐并规范", "③ 计划：材料里没有", w=400)
    h.move_to(1140,600,dur=0.5); h.scroll(200,dur=0.8); h.pause(1.0)
    hover(h, "跟进供应商", "③ 材料里也没有", w=400)
    h.pause(1.0)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.6)
scene("B-验收",B,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
