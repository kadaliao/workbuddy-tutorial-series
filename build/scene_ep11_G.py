import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep11"
def tgt(b,p=8): return [b[0]-p,b[1]-p,b[2]+2*p,b[3]+2*p]
def G11(h):
    h.pause(0.8)
    h.move_to(1250,226,dur=0.8,target=[1056,206,360,96],label="绿点：已连接"); h.pause(2.0)
    h.move_to(1150,225,dur=0.5); h.pause(0.3); h.click(); h.pause(1.6)
    b=ocr.find("解绑"); h.move_to(*C(b),dur=0.8,target=tgt(b),label="不用了：解绑"); h.pause(3.0); h.log("mark",text="unbind")
    h.move_to(1004,186,dur=0.7); h.pause(0.3); h.click(); h.pause(1.0)
h=Human(); new_task(h)
h.move_to(100,224); h.click(); time.sleep(1.0)
b=ocr.find("连接器",exact=True,region=[200,150,300,200]); h.move_to(*C(b)); h.click(); time.sleep(2.0)
scene("G-解绑位置",G11,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
