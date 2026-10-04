import sys; sys.path.insert(0,'.')
from human import *
APP=[419,277,65,65]; APPS=[733,277,76,76]
def run(h):
    h.pause(1.2,label="打开 dmg 后看到安装窗口")
    h.move_to(451,312,target=APP,label="WorkBuddy 图标"); h.pause(0.8,1.0)
    h.move_to(771,312,dur=0.9,target=APPS,label="Applications 文件夹快捷方式",overshoot=False); h.pause(0.9,1.2,label="目标在这里")
    h.move_to(451,312,dur=0.8,target=APP,label="从这个图标开始拖",overshoot=False); h.pause(0.5,0.7)
    h.log("click",label="按住图标开始拖",target=APP); h.mouse_down(); time.sleep(0.25)
    h.move_to(690,312,dur=1.5,target=APPS,label="拖向 Applications（演示：不松手到目标上）",overshoot=False,drag=True); h.pause(0.9,1.1,label="拖拽中")
    h.esc(); time.sleep(0.3); h.mouse_up(); h.log("wait",label="按 Esc 取消拖拽（真实安装时在这里松手）",dur=0)
    h.pause(1.6)
    h.move_to(900,700,dur=0.8); h.pause(0.8)
scene("C-安装",run,extra={"mask_regions":[{"name":"侧栏用户行(WorkBuddy 窗口在 dmg 窗口后面)","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}],"note":"拖拽中途 Esc 取消，未复制/覆盖已安装应用"})
