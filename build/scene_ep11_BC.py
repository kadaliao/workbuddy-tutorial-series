import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep11"; os.makedirs(O, exist_ok=True)
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def B11(h):
    h.pause(0.8)
    h.move_to(100,224,dur=0.8,target=[12,208,245,32],label="专家·技能·连接器"); h.pause(0.4); h.click(); h.pause(1.0)
    b=ocr.find("连接器",exact=True,region=[200,150,300,200]); h.move_to(*C(b),dur=0.6,target=[b[0]-20,b[1]-8,120,b[3]+16],label="连接器"); h.pause(0.4); h.click(); h.pause(2.0)
    h.move_to(850,250,dur=0.8,target=[290,80,1130,330],label="能接的服务"); h.pause(2.4)
    b=ocr.find("腾讯文档",exact=True); h.move_to(b[0]+30,b[1]+8,dur=0.7,target=[1056,206,360,96],label="腾讯文档"); h.pause(1.6)
    b=ocr.find("QQ邮箱"); h.move_to(b[0]+30,b[1]+8,dur=0.6,target=[1056,90,360,96],label="QQ 邮箱"); h.pause(1.2)
    b=ocr.find("腾讯会议"); h.move_to(b[0]+30,b[1]+8,dur=0.6,target=[296,320,360,96],label="腾讯会议"); h.pause(1.2)
    h.move_to(900,500,dur=0.6); h.scroll(400,dur=1.4); h.pause(1.4); h.scroll(-600,dur=1.0); h.pause(0.8)
    b=ocr.find("自定义连接器"); h.move_to(*C(b),dur=0.7,target=tgt(b),label="自定义连接器"); h.pause(2.0)
def C11(h):
    h.pause(0.8)
    h.move_to(482,473,dur=0.7,target=[466,458,28,28],label="点「+」"); h.pause(0.4); h.click(); h.pause(1.0)
    b=ocr.find("连接器",exact=True,region=[440,150,300,330]); h.move_to(b[0]+20,b[1]+8,dur=0.6,target=[b[0]-30,b[1]-8,196,b[3]+16],label="连接器"); h.pause(0.8)
    h.move_to(720,b[1]+8,dur=0.5); h.pause(0.4)
    h.move_to(760,520,dur=0.6,target=[662,410,320,350],label="这次要用的，点连接"); h.pause(3.0)
    h.esc(); h.pause(0.3); h.esc(); h.pause(0.6)
h=Human(); new_task(h)
M={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34],"t":[[0,3]]}]}
scene("B-连接器页",B11,outdir=O,extra=M)
new_task(h)
scene("C-输入框里开",C11,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
