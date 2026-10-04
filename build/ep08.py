#!/usr/bin/env python3
"""第 8 集：文件、资料库与云文档。用法：ep08.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 8, "文件、资料库与云文档"
TEXT = {
 "A开场": "用 AI 干活，绕不开两个问题：材料怎么给它，做好的东西放在哪。今天一次讲清楚。",
 "B进材料": "材料进来，有三条路。第一条，工作空间，你选的文件夹里的东西，它都能读。第二条，点输入框左边的加号，添加文件，这里能选本地文件，也能选资料库、腾讯文档、ima、乐享知识库。第三条，在输入框里打一个 @，文件夹里的文件直接列出来，点一下就引用了。",
 "C拖拽": "还有最省事的：直接把文件拖进输入框，它会变成一个文件胶囊。",
 "D成品": "成品默认就在你的工作空间里，就在本地。预览右上角有四个按钮：保存、上传到云端、分享、更多。更多里有打开文件夹和另存为，想换个地方存，用另存为。上传到云端，可以选资料库、腾讯文档、ima、乐享，这是存，不是公开。",
 "E分享坑": "重点说一下分享。点分享图标，它会立刻开始上传，而且链接默认是，互联网上拿到链接的人都能看。哪怕你只是想看看菜单，上传也已经发生了。所以工作文件、带客户信息的文件，别随手点分享。",
 "F资料库": "上传和分享的东西，都在左边的资料库。分我的资料和团队空间；最近里面，能看到我分享的，和与我共享的。容量在底部显示。",
 "G取消分享": "分享错了怎么办？打开设置，数据管理，分享的文件里能找到它，在这里复制链接，或者取消分享。",
 "H收尾": "今天三句话：材料三条路，成品在本地，分享前想清楚。下一集，让它每天自己上班：定时任务。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F8 = K.F; SH = f"{V}/shots"

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("CARD", "a", t, [{"from": 0, "to": t, "last": True, "lines": [("材料怎么给它？", "n", at(n,"材料怎么")), ("做好的东西放在哪？", "n", at(n,"做好的"))]}])]
    n = "B进材料"; t = T(n)
    P[n] = [("R", f"{F8}/B-进材料.mov", {"anchors": [[2.4, 0], [2.8, at(n,"第一条")], [5.9, at(n,"第二条")], [7.2, at(n,"添加文件")-0.2], [12.1, at(n,"也能选")], [17.0, at(n,"第三条")], [18.0, at(n,"打一个")], [19.9, at(n,"文件夹里的文件")+0.3], [23.0, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "①", "set": {"zoom": 2.0, "focus": True}}, {"contains": "②", "set": {"zoom": 1.8}}, {"contains": "添加文件", "set": {"zoom": 1.6}},
                          {"contains": "本地、资料库", "set": {"zoom": 1.6, "focus": True}}, {"contains": "③", "set": {"zoom": 1.4}}],
                "events_extra": [{"t": 19.9, "kind": "move", "target": [452,96,790,150], "label": "点一下就引用", "zoom": 1.5, "focus": True, "dur": 2.6}]})]
    n = "C拖拽"; t = T(n)
    P[n] = [("R", f"{F8}/C-拖拽.mov", {"anchors": [[5.0, 0], [5.9, at(n,"直接把文件")], [10.4, at(n,"它会变成")], [11.8, at(n,"文件胶囊")-0.3], [14.5, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "拖进来", "set": {"zoom": False}}, {"contains": "胶囊", "set": {"zoom": 2.0, "focus": True}}]})]
    n = "D成品"; t = T(n)
    P[n] = [("R", f"{F8}/D-成品在哪.mov", {"anchors": [[2.4, 0], [2.8, at(n,"成品默认")], [6.0, at(n,"四个按钮")+0.4], [8.3, at(n,"上传到云端")], [9.9, at(n,"分享")], [12.2, at(n,"更多")], [13.8, at(n,"更多里有")], [16.5, at(n,"想换个地方")], [19.5, at(n,"上传到云端",1)], [21.0, at(n,"可以选")], [25.6, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "成品默认", "set": {"zoom": 1.6, "focus": True}}, {"contains": "保存", "set": {"zoom": 2.4}}, {"contains": "上传到云端", "set": {"zoom": 2.4}},
                          {"contains": "分享", "set": {"zoom": 2.4}}, {"contains": "更多", "set": {"zoom": 2.4}}],
                "events_extra": [{"t": 14.0, "kind": "move", "target": [1299,101,128,80], "label": "打开文件夹 · 另存为", "zoom": 2.2, "focus": True, "dur": 4.0},
                                 {"t": 19.8, "kind": "move", "target": [1197,105,110,145], "label": "资料库、腾讯文档、ima、乐享", "zoom": 2.0, "focus": True, "side": "left", "dur": 4.6}]})]
    n = "E分享坑"; t = T(n)
    P[n] = [("R", f"{SH}/26-产物分享菜单.png", {"anchors": [[0, 0], [t, t]], "masks_extra": [{"name":"加油站卡片","rect":[20,1330,480,160],"style":"fillmed"}], "events_override": [
                {"t": at(n,"点分享图标"), "kind": "move", "target": [2240,128,72,62], "label": "分享图标", "zoom": 1.8, "dur": 1.6},
                {"t": at(n,"立刻开始上传"), "kind": "move", "target": [760,594,880,142], "label": "一点就开始上传", "zoom": 1.6, "focus": True, "dur": 2.0},
                {"t": at(n,"链接默认"), "kind": "move", "target": [760,850,880,68], "label": "互联网上拿到链接就能看", "zoom": 1.6, "focus": True, "dur": at(n,"所以工作文件") - at(n,"链接默认") - 1.0},
                {"t": at(n,"所以工作文件"), "kind": "move", "target": [720,470,920,680], "label": "工作文件，别随手点", "zoom": 1.2, "dur": t - at(n,"所以工作文件") - 1.2}]})]
    n = "F资料库"; t = T(n)
    P[n] = [("R", f"{F8}/G-资料库.mov", {"anchors": [[2.4, 0], [4.2, at(n,"左边的资料库")+0.4], [6.3, at(n,"分我的资料")], [9.5, at(n,"团队空间")], [13.2, at(n,"最近里面")], [14.5, at(n,"我分享的")+0.2], [20.2, at(n,"容量")], [24.2, t]],
                "drop_masks": DROP, "masks_extra": [USER, {"name":"所有者列","rect":[900,195,110,240],"style":"fillmed"}],
                "patch": [{"contains": "资料库", "set": {"zoom": 1.6}}, {"contains": "我的资料", "set": {"zoom": 1.8}}, {"contains": "团队空间", "set": {"zoom": 1.8}},
                          {"contains": "我分享的", "set": {"zoom": 1.8}}, {"contains": "容量", "set": {"zoom": 2.0}}]})]
    n = "G取消分享"; t = T(n)
    P[n] = [("R", f"{F8}/H-数据管理.mov", {"anchors": [[2.0, 0], [3.6, at(n,"打开设置")], [6.9, at(n,"数据管理")+0.4], [9.4, at(n,"分享的文件")], [12.2, at(n,"能找到它")], [16.0, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "数据管理", "set": {"zoom": 1.8, "label": "设置 → 数据管理"}}, {"contains": "分享的文件", "set": {"zoom": 1.8}},
                          {"contains": "取消分享", "set": {"zoom": 1.6, "focus": True, "target": [674,150,636,52], "label": "分享过的文件都在这里"}}],
                "events_extra": [{"t": 14.0, "kind": "move", "target": [1250,160,80,32], "label": "复制链接 / 取消分享", "zoom": 2.0, "focus": True, "dur": 2.0}]})]
    n = "H收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "h", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 材料三条路", "n", at(n,"材料三条")), ("② 成品在本地", "n", at(n,"成品在本地")), ("③ 分享前想清楚", "n", at(n,"分享前"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("定时任务：让它每天自己上班", "b", at(n,"让它每天"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep08-v1.mp4")
