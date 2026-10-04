import sys; sys.path.insert(0,'.')
from human import *
USER=[8,795,180,55]; PROMO=[1240,0,200,34]
DOC=[864,169,565,659]; TABLE=[947,477,384,100]; PROB2=[956,628,310,22]; HEADS=[940,180,200,560]
def H(h):
    h.pause(1.0)
    h.move_to(1140,300,target=DOC,label="右侧是成品预览"); h.pause(1.5)
    h.move_to(1138,526,target=TABLE,label="数字：和数据表逐个对"); h.pause(2.6,3.0)
    h.move_to(1000,600,dur=0.8); h.pause(0.4)
    h.move_to(1110,638,target=PROB2,label="材料里没提「比价」"); h.pause(3.2,3.6)
    h.move_to(1150,700,dur=0.8); h.pause(1.0)
def K(h):
    h.pause(1.0)
    h.move_to(1411,79,target=[1385,63,52,32],label="点右上角「…」"); h.pause(0.3,0.5); h.click(None,[1385,63,52,32]); h.pause(0.9,1.2)
    h.move_to(1361,124,target=[1304,106,110,36],label="选「打开文件夹」"); h.pause(0.5,0.8); h.click(None,[1304,106,110,36])
    h.pause(2.4)
    subprocess.run(["screencapture","-x","/private/tmp/claude-501/k_chk.png"])
    h.pause(3.5)
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep01"
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(1.0)
scene("H5-验收",H,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER}]})
time.sleep(0.5)
scene("K5-找文件",K,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":USER}]})
