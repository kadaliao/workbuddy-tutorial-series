import sys; sys.path.insert(0,'.')
from human import *
def run(h):
    h.pause(1.0,label="成品预览页")
    h.move_to(1411,79,target=[1385,63,52,32],label="点右上角“…”更多"); h.pause(0.3,0.5); h.click("点“更多”",[1385,63,52,32]); h.pause(0.9,1.2)
    h.move_to(1361,124,target=[1304,106,110,36],label="选“打开文件夹”"); h.pause(0.5,0.8); h.click("点“打开文件夹”",[1304,106,110,36])
    h.pause(2.2,2.6,label="Finder 打开了工作空间文件夹")
    h.move_to(517,281,target=[440,236,150,110],label="这就是刚生成的 本周周报.docx"); h.pause(3.0,label="悬停在 本周周报.docx 上")
    h.jitter(1.0)
    # close Finder window with Cmd+W so WorkBuddy is visible again
    h.key(13, Quartz.kCGEventFlagMaskCommand); h.pause(1.0)
scene("K-找文件",run,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"左侧回复首行含绝对路径(含用户名)，仅在 WorkBuddy 画面中可见","rect":[390,100,380,24]},{"name":"Finder 窗口已隐藏边栏/路径栏，标题只显示 WorkBuddy-demo","rect":[0,0,0,0]}]})
