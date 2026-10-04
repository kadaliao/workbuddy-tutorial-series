#!/usr/bin/env python3
"""第 4 集：默认、计划、仅问答。用法：ep04.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 4, "默认、计划、仅问答：什么时候用哪种"
TEXT = {
 "A开场": "同一个输入框，三种用法。默认模式，说做就做。计划模式，先给你看方案，你点头才动手。仅问答模式，只聊，不动你的文件。今天讲，什么时候用哪一种。",
 "B开关": "先找开关。点输入框左边的加号，找到模式。上面一行写着，当前为默认模式。下面两个开关：计划，和仅问答。两个都不开，就是默认模式。注意，它们是开关，不是三选一的列表。",
 "C仅问答": "先试仅问答。打开之后，输入框里会多一个标识。我问它：如果我让你整理这个文件夹，你会怎么做？会删除文件吗？它只给思路，还主动说明，现在是只读模式，确认方案后再切回去执行。我看了一下文件夹，一个文件都没变。拿不准一个操作安不安全，先用仅问答问一句，没有任何风险。",
 "D计划": "再试计划。打开计划，给它一个步骤多一点的任务：读日报，统计每天完成几件事，算四项指标的环比，最后出一份 Excel。它没有马上动手，先把数据读了一遍，然后问我几个问题：表格怎么排，要不要图表。我都选了推荐项。接着它把计划写出来，问我：确认按此计划执行吗？方向不对，现在改，成本最低。我点开始执行。一分多钟后，Excel 出来了，表格、环比、图表都有。",
 "E组合": "这三种可以接力用。想法还乱，先仅问答，把思路理清。任务复杂，用计划，把方案定下来。需求很清楚了，用默认，一口气做完。",
 "F退出": "想退出，把鼠标移到输入框里的模式标识上，点叉就行。",
 "G收尾": "今天三句话：简单任务用默认，复杂任务先计划，拿不准就仅问答。下一集，讲验收：它做对了吗？",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F4 = K.F

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("CARD", "a", t, [{"from": 0, "to": t, "last": True, "lines": [("同一个输入框，三种用法", "t", 0.2),
        ("默认：说做就做", "n", at(n,"默认模式")), ("计划：先给方案，你点头才动手", "n", at(n,"计划模式")), ("仅问答：只聊，不动文件", "n", at(n,"仅问答模式"))]}])]
    n = "B开关"; t = T(n)
    P[n] = [("R", f"{F4}/BC-仅问答.mov", {"anchors": [[2.4, 0], [4.2, at(n,"点输入框")+0.6], [5.3, at(n,"找到模式")], [7.6, at(n,"上面一行")], [11.1, at(n,"下面两个")], [13.4, at(n,"和仅问答")], [15.0, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "点「+」", "set": {"zoom": 1.8}}, {"contains": "模式", "set": {"zoom": 1.6}},
                          {"contains": "不开开关", "set": {"zoom": 2.0, "focus": True, "label": "当前为默认模式"}},
                          {"contains": "计划 Plan", "set": {"zoom": 2.0, "label": "计划"}}, {"contains": "仅问答 Ask", "set": {"zoom": 2.0, "label": "仅问答"}}]})]
    n = "C仅问答"; t = T(n); c3 = at(n, "我看了一下") - 0.2
    P[n] = [("R", f"{F4}/BC-仅问答.mov", {"anchors": [[15.0, 0], [15.8, at(n,"打开之后")+0.6], [18.2, at(n,"我问它")], [26.0, at(n,"它只给思路")-0.6], [28.0, at(n,"它只给思路")], [62.7, at(n,"还主动说明")], [64.9, c3]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "问一句", "set": {"label": None}}, {"contains": "发送", "set": {"label": None}}],
                "badges": [{"from": 28.0, "to": 62.0, "text": "加速播放", "t0": 0}],
                "events_extra": [{"t": 16.0, "kind": "move", "target": [500,458,90,30], "label": "多了「仅问答」标识", "zoom": 2.2, "focus": True, "dur": 1.6},
                                 {"t": 63.0, "kind": "move", "target": [470,586,760,52], "label": "只读模式，确认后再执行", "zoom": 1.6, "focus": True, "dur": 2.5}]}),
            ("CARD", "c", t - c3, [{"from": 0, "to": t - c3, "last": True, "lines": [("文件夹：4 个文件，一个没变", "b", 0.2), ("拿不准安不安全，先用仅问答问一句", "s", at(n,"拿不准")-c3)]}])]
    n = "D计划"; t = T(n)
    d2 = at(n, "我都选了") - 0.6; d3 = at(n, "接着它把") - 0.3
    P[n] = [("R", f"{F4}/D1-计划.mov", {"anchors": [[9.2, 0], [11.7, at(n,"打开计划")+0.5], [17.2, at(n,"给它一个")], [28.6, at(n,"它没有马上")], [52.5, at(n,"然后问我")], [56.0, d2]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 30.0, "to": 51.0, "text": "加速播放", "t0": 0}],
                "patch": [{"contains": "打开「计划」", "set": {"zoom": 2.0}}, {"contains": "一个多步任务", "set": {"zoom": 1.5}}, {"contains": "发送", "set": {"label": None}}],
                "events_extra": [{"t": 52.6, "kind": "move", "target": [470,598,766,180], "label": "动手前先问我", "zoom": 1.5, "focus": True, "dur": 2.8}]}),
            ("R", f"{F4}/D2-回答问题.mov", {"anchors": [[4.0, 0], [19.7, (d3-d2)*0.6], [50.6, d3-d2]], "drop_masks": DROP, "masks_extra": [USER],
                "badges": [{"from": 21.0, "to": 49.0, "text": "加速播放", "t0": 0}],
                "patch": [{"contains": "选推荐项", "set": {"zoom": 1.6}}]}),
            ("R", f"{F4}/D3-确认执行.mov", {"anchors": [[2.6, 0], [3.1, at(n,"接着它把")-d3+0.3], [7.9, at(n,"方向不对")-d3], [9.9, at(n,"我点开始")-d3+0.4], [12.0, at(n,"一分多钟")-d3], [84.0, at(n,"Excel 出来了")-d3], [92.0, t-d3]],
                "drop_masks": DROP, "masks_extra": [USER],
                "badges": [{"from": 12.0, "to": 82.0, "text": "加速播放 · 实际 {real}", "t0": 9.9}],
                "patch": [{"contains": "写好的计划", "set": {"zoom": 1.5, "focus": True, "label": "它写的计划"}},
                          {"contains": "开始执行", "set": {"zoom": 1.8, "focus": True, "label": "确认按此计划执行？"}}],
                "events_extra": [{"t": 85.0, "kind": "move", "target": [855,170,585,690], "label": "表格、环比、图表", "zoom": 1.3, "dur": 4.0}]})]
    n = "E组合"; t = T(n)
    P[n] = [("CARD", "e", t, [{"from": 0, "to": t, "last": True, "lines": [("三种模式接力用", "t", 0.2),
        ("想法还乱 → 仅问答", "n", at(n,"想法还乱")), ("任务复杂 → 计划", "n", at(n,"任务复杂")), ("需求清楚 → 默认", "n", at(n,"需求很清楚"))]}])]
    n = "F退出"; t = T(n)
    P[n] = [("R", f"{F4}/F-退出模式.mov", {"anchors": [[2.8, 0], [3.6, at(n,"把鼠标")+0.4], [6.3, at(n,"点叉")], [9.0, t]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "patch": [{"contains": "模式标识", "set": {"zoom": 2.4}}, {"contains": "点 ×", "set": {"zoom": 2.4, "focus": True}}]})]
    n = "G收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "g", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 简单任务用默认", "n", at(n,"简单任务")), ("② 复杂任务先计划", "n", at(n,"复杂任务")), ("③ 拿不准就仅问答", "n", at(n,"拿不准"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("验收：它做对了吗？", "b", at(n,"讲验收"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep04-v1.mp4")
