import sys; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep13"; os.makedirs(O, exist_ok=True)
def C13(h):
    h.pause(0.8)
    h.move_to(700,125,dur=0.8,target=[664,105,150,36],label="当前套餐"); h.pause(2.0)
    h.move_to(760,195,dur=0.7,target=[664,168,420,60],label="总剩余积分"); h.pause(2.2)
    h.move_to(800,420,dur=0.7,target=[664,350,650,180],label="基础积分按月刷新"); h.pause(2.6)
    h.move_to(450,76,dur=0.8); h.click(); h.pause(1.0)
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(0.4)
scene("C-套餐与积分",C13,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},
   {"name":"总剩余","rect":[674,172,90,36],"style":"fillmed"},{"name":"奖励积分","rect":[888,250,110,34],"style":"fillmed"},
   {"name":"奖励用量","rect":[1100,464,210,32],"style":"fillmed"},{"name":"到期","rect":[674,464,240,30],"style":"fillmed"}]})
