import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep10"
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def B10(h):
    h.pause(0.8)
    h.move_to(62,158,dur=0.8,target=[12,142,245,32],label="助理：本地助理"); h.pause(0.4); h.click(); h.pause(1.6)
    b=ocr.find("已连接"); h.move_to(*C(b),dur=0.7,target=tgt(b),label="已连接微信小程序"); h.pause(2.2)
    h.move_to(232,826,dur=0.9,target=[220,812,26,26],label="多端协同"); h.pause(0.4); h.click(); h.pause(1.4)
    b=ocr.find("允许移动端"); h.move_to(*C(b),dur=0.7,target=[b[0]-30,b[1]-8,b[2]+50,b[3]+16],label="允许移动端连接：开着"); h.pause(2.6)
    b=ocr.find("保持唤醒"); h.move_to(*C(b),dur=0.6,target=[b[0]-30,b[1]-8,b[2]+50,b[3]+16],label="保持唤醒：要远程就打开"); h.pause(2.8)
    h.esc(); h.pause(0.6); h.move_to(800,300,dur=0.5); h.click(); h.pause(0.6)
    h.key(43, Quartz.kCGEventFlagMaskCommand); h.pause(1.8)
    b=ocr.find("通用",exact=True,region=[430,100,200,60]) or ocr.find("通用")
    h.move_to(*C(b),dur=0.6); h.pause(0.3); h.click(); h.pause(1.4)
    b=ocr.find("允许锁屏运行"); h.move_to(b[0]+200,b[1]+12,dur=0.7,target=[664,b[1]-10,650,54],label="锁屏后也能接着跑"); h.pause(3.0)
    close_settings(h)
def C10(h):
    h.pause(0.8)
    b=ocr.find("摘要周报文档",region=[0,350,260,120]) or ocr.find("摘要周报",region=[0,350,260,120])
    h.move_to(b[0]+60,b[1]+8,dur=0.8,target=[12,b[1]-8,245,32],label="手机派来的任务"); h.pause(0.4); h.click(); h.pause(2.0)
    h.move_to(800,300,dur=0.7,target=[470,60,760,300],label="电脑上同步显示"); h.pause(2.4)
    h.move_to(800,500,dur=0.5); h.scroll(1500,dur=3.0); h.pause(1.5)
    h.move_to(800,450,dur=0.7,target=[470,300,760,300],label="移进了废纸篓"); h.pause(3.0)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.5)
h=Human(); new_task(h)
def close_settings(h):
    n=subprocess.run(["osascript","-e",'tell application "System Events" to tell process "WorkBuddy" to count windows'],capture_output=True,text=True).stdout.strip()
    if n=="2": h.move_to(450,76,dur=0.7); h.click(); h.pause(1.0)
M={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34],"t":[[0,3]]}]}
scene("B-电脑端设置",B10,outdir=O,extra=M)
scene("C-电脑上看任务",C10,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
