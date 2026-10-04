import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep11"
def D11(h):
    h.pause(0.8)
    h.move_to(1383,227,dur=0.8,target=[1370,214,26,26],label="点「+」授权"); h.pause(1.0); h.click(); h.pause(2.0)
    subprocess.run(["screencapture","-x","-R80,40,1440,860","/private/tmp/claude-501/auth1.png"])
    h.log("mark",text="after_click"); h.pause(0.5)
h=Human(); new_task(h)
h.move_to(100,224); h.click(); time.sleep(1.0)
b=ocr.find("连接器",exact=True,region=[200,150,300,200]); h.move_to(*C(b)); h.click(); time.sleep(2.0)
scene("D-点授权",D11,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]}]})
