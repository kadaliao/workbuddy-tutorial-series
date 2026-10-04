import sys; sys.path.insert(0,'.')
from human import *
ROWS=[("新建任务",125),("助理",158),("项目",191),("专家·技能·连接器",225),("定时任务",258),("资料库",290),("更多",323)]
def T(y): return [12,y-16,240,32]
def run(h):
    h.pause(2.0,label="主界面静止")
    first=True
    for name,y in ROWS:
        h.move_to(110,y,target=T(y),label=f"这是「{name}」")
        h.pause(2.6,3.2,label=f"悬停：{name}")
        if name not in ("新建任务","更多"):
            h.click(f"点进「{name}」",T(y)); h.pause(1.5,1.8,label=f"{name}页面")
            h.move_to(110,125,target=T(125),label="点回「新建任务」"); h.pause(0.3,0.5)
            h.click("回到新建任务",T(125)); h.pause(0.8,1.1)
    h.move_to(700,600,label="移开光标"); h.pause(1.5)
scene("D-侧栏巡览",run,extra={"mask_regions":[{"name":"侧栏用户行(头像/昵称)","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]},{"name":"资料库页含他人用户名(团队空间列)","note":"仅在点进资料库的1.5秒内出现，右侧列表所有者列，后期打码","rect":[560,240,420,300]}]})
