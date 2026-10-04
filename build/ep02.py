#!/usr/bin/env python3
"""第 2 集：先把门锁好——权限、工作空间与备份。用法：ep02.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 2, "先把门锁好：权限、工作空间与备份"
TEXT = {
 "A开场": "先做个实验。我让它，把这个文件夹里所有的 txt 文件都删掉。你看，它没有直接动手，先把要删的文件列出来，提醒我风险，再问我怎么处理。我选，取消，不动任何文件。它回复，一个都没删。今天就讲：它能碰什么，怎么让它别乱来。",
 "B围墙": "第一道门，是工作空间。你给它选哪个文件夹，它就在这个文件夹里干活。选好之后，输入框下面会显示文件夹的名字，没显示，就是没选上。建议每类任务建一个自己的文件夹，里面放副本，不放原件。",
 "C权限": "第二道门，是权限。点输入框下面的，默认权限。这段话的意思是：所有操作都在安全沙箱里进行，超出范围，会来请求你的允许。下面这个开关，允许完全访问，打开之后，这些确认基本都不问了，而且对所有任务都生效。新手的建议很简单：一直别开。",
 "D安全中心": "第三道门，在设置里。左下角头像，设置，安全中心。沙箱安全，默认开着。文件、命令、网络，各有一套规则，超出规则的，就停下来问你。再往下是自动备份，它改你的文件之前，会先备份一份，总上限三千兆。点，打开备份目录，备份就放在这里。",
 "E删除保护": "那删除呢？我另外让它删一个测试文件，它没问我，直接删了。但你看它的回复：不是彻底删除，是移进了废纸篓，可以还原。这就是安全中心里的删除保护。下面还有一条，批量删除审批，一次删到一定数量，必须你批准。再往下是审计中心，它执行过的命令、碰过的文件，都有记录。",
 "F三个坑": "最后说三个坑。第一，点产物的分享图标，它会立刻开始上传，链接默认是，互联网上拿到链接的人都能看，别随手点。第二，新建定时任务的时候，权限默认是红色的，允许完全访问，记得点开，把它关掉，改回默认权限。第三，身份证、密码、银行卡这类敏感内容，别放进它能读的文件夹。",
 "G收尾": "今天三句话：文件夹是围墙，默认权限就够用，完全访问不要开。下一集，教你怎么把需求写清楚，让它一次做对。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F2 = K.F; F1 = f"{V}/footage/ep01"; SH = f"{V}/shots"

def plan():
    at, T = K.at, K.T
    P = {}
    # 注意：A2/A3/B/D/F 的 events 时间与画面已对齐（scene 同步检测）；下面 anchors 把源时间映射到口播时间
    n = "A开场"; t = T(n); a3 = at(n, "你看") - 0.2
    P[n] = [("R", f"{F2}/A2-批量删除.mov", {"anchors": [[2.2, 0], [9.0, a3*0.55], [12.0, a3*0.7], [185.0, a3]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "让它批量删除", "set": {"zoom": 1.5}}, {"contains": "发送", "set": {"zoom": 1.8}}],
                "badges": [{"from": 12.0, "to": 185.0, "text": "加速播放", "t0": 0}]}),
            ("R", f"{F2}/A3-拒绝删除.mov", {"anchors": seg_anchor([[1.5, a3], [4.0, at(n,"提醒我风险")], [9.0, at(n,"再问我")], [13.4, at(n,"我选")+0.3], [26.0, at(n,"它回复")+0.5], [40.0, t]], a3),
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "它停下来问我", "set": {"zoom": 1.5, "focus": True}}, {"contains": "选「取消", "set": {"zoom": 1.6, "focus": True}}],
                "events_extra": [{"t": 26.5, "kind": "move", "target": [476,248,560,30], "label": "没有删除任何文件", "zoom": 1.6, "focus": True, "dur": 3.0}]})]
    n = "B围墙"; t = T(n)
    P[n] = [("R", f"{F2}/B-选工作空间.mov", {"anchors": [[2.4, 0], [8.5, at(n,"它就在")], [14.6, at(n,"选好之后")+0.4], [17.5, at(n,"没显示")], [19.6, t]],
                "drop_masks": ["推广","用户行","对话框"], "masks_extra": [USER, PROMO(), {"name":"对话框侧栏","rect":[282,208,142,444],"t":[[7.0,14.6]]}],
                "patch": [{"contains": "选择工作空间", "set": {"zoom": 1.8}}, {"contains": "打开本地", "set": {"zoom": 1.8}},
                          {"contains": "演示文件夹", "set": {"zoom": 1.5}}, {"contains": "显示文件夹名", "set": {"zoom": 2.0, "focus": True, "dur": 4.0}}]})]
    n = "C权限"; t = T(n)
    P[n] = [("R", f"{F1}/I-权限.mov", {"anchors": [[2.0, 0], [4.1, at(n,"点输入框")+0.6], [5.5, at(n,"下面这个开关")], [6.8, at(n,"新手")-0.3], [12.4, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "events_extra": [{"t": 4.3, "kind": "move", "target": [606,372,192,72], "label": "所有操作都在沙箱里", "zoom": 2.2, "focus": True, "dur": 0.9}],
                "patch": [{"contains": "默认是关着", "set": {"zoom": 2.3, "focus": True, "dur": 3.0, "label": "新手一直别开", "side": "bottom"}},
                          {"contains": "完全访问开关", "set": {"label": None, "zoom": 2.0}},
                          {"contains": "默认权限", "set": {"zoom": 1.8}}]})]
    n = "D安全中心"; t = T(n)
    menu_mask = [{"name":"菜单昵称","rect":[22,240,130,38],"t":[[4.3,7.6]]}, {"name":"菜单积分","rect":[222,350,100,30],"t":[[4.3,7.6]]}]
    P[n] = [("R", f"{F2}/D-安全中心.mov", {"anchors": [[3.4, 0], [4.6, at(n,"左下角")+0.3], [7.3, at(n,"设置",1)+0.3], [9.8, at(n,"安全中心")+0.3],
                    [11.2, at(n,"沙箱")], [14.0, at(n,"文件")], [17.2, at(n,"再往下")], [19.8, at(n,"总上限")], [22.5, at(n,"点")+0.1], [26.6, at(n,"备份就放")-0.6], [31.5, t]],
                "drop_masks": DROP, "masks_extra": [USER] + menu_mask + [{"name":"Finder侧栏","rect":[426,124,172,432],"t":[[26.4,32.9]]}],
                "patch": [{"contains": "沙箱", "set": {"zoom": 1.8}}, {"contains": "越界", "set": {"zoom": 1.5}}, {"contains": "自动备份", "set": {"zoom": 1.8}},
                          {"contains": "3000", "set": {"zoom": 2.2, "focus": True}}, {"contains": "打开备份目录", "set": {"zoom": 2.0}}]})]
    n = "E删除保护"; t = T(n); e1 = at(n, "这就是") - 0.3
    audit_mask = [{"name":"审计用户名列","rect":[950,96,215,644],"t":[[42.6,44.4],[49.3,51.2]]}, {"name":"审计用户名","rect":[950,236,215,26],"t":[[44.4,49.3]]}]
    P[n] = [("R", f"{F2}/A4-单删回复.mov", {"anchors": [[2.0, 0], [2.0+e1, e1]], "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 2.3, "kind": "move", "target": [470,82,760,36], "label": "让它删一个测试文件", "zoom": 1.3, "dur": 2.0},
                                    {"t": 3.0 + max(0, at(n,"但你看")-1.0), "kind": "move", "target": [470,236,760,50], "label": "移进了废纸篓，可以还原", "zoom": 1.6, "focus": True, "dur": 4.0}]}),
            ("R", f"{F2}/D-安全中心.mov", {"anchors": seg_anchor([[37.5, e1], [41.0, at(n,"下面还有")+0.6], [42.6, at(n,"再往下")], [45.0, at(n,"都有记录")-0.5], [49.0, t]], e1),
                "drop_masks": DROP, "masks_extra": [USER] + audit_mask, "events_override": [
                    {"t": 37.8, "kind": "move", "target": [664,262,644,48], "label": "删除保护：先移到废纸篓", "zoom": 1.7, "focus": True, "dur": 1.8},
                    {"t": 40.2, "kind": "move", "target": [664,330,644,70], "label": "批量删除审批", "zoom": 1.7, "focus": True, "dur": 1.6},
                    {"t": 44.6, "kind": "move", "target": [654,96,646,330], "label": "审计中心：每一步都有记录", "zoom": 1.3, "dur": 3.4}]})]
    n = "F三个坑"; t = T(n); f2 = at(n, "第二") - 0.2; f3 = at(n, "第三") - 0.2
    P[n] = [("R", f"{SH}/26-产物分享菜单.png", {"anchors": [[0, 0], [f2, f2]], "masks_extra": [{"name":"加油站卡片","rect":[20,1330,480,160],"style":"fillmed"}], "events_override": [
                {"t": at(n,"第一"), "kind": "move", "target": [2240,128,72,62], "label": "分享图标", "zoom": 1.8, "dur": 1.6},
                {"t": at(n,"立刻开始上传"), "kind": "move", "target": [760,594,880,142], "label": "一点就开始上传", "zoom": 1.6, "focus": True, "dur": 1.8},
                {"t": at(n,"链接默认"), "kind": "move", "target": [760,850,880,68], "label": "互联网上拿到链接就能看", "zoom": 1.6, "focus": True, "dur": f2 - at(n,"链接默认") - 1.2}]}),
            ("R", f"{F2}/F-定时任务权限.mov", {"anchors": seg_anchor([[2.0, f2], [4.0, at(n,"权限默认")], [8.0, at(n,"记得点开")], [12.8, at(n,"把它关掉")+0.3], [18.0, f3]], f2),
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "红色", "set": {"zoom": 2.0, "focus": True}}, {"contains": "提醒", "set": {"zoom": 2.0}},
                          {"contains": "关掉", "set": {"zoom": 2.4}}, {"contains": "改回默认", "set": {"zoom": 2.0, "focus": True}}, {"contains": "取消", "set": {"label": None}}]}),
            ("CARD", "f3", t - f3, [{"from": 0, "to": t - f3, "last": True, "lines": [("容易踩的坑 · 3", "t", 0.15),
                ("身份证、密码、银行卡", "r", at(n,"身份证")-f3), ("别放进它能读的文件夹", "b", at(n,"别放进")-f3)]}])]
    n = "G收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "g", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 文件夹是围墙", "n", at(n,"文件夹")), ("② 默认权限就够用", "n", at(n,"默认权限")), ("③ 完全访问不要开", "n", at(n,"完全访问"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("一句话说清需求", "b", at(n,"教你")), ("让它一次做对", "s", at(n,"让它一次"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep02-v1.mp4")
