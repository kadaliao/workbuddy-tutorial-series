#!/usr/bin/env python3
"""番外：积分到底是怎么花掉的。用法：ep13.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 13, "番外：积分到底是怎么花掉的"
TEXT = {
 "A开场": "第一集那份周报，花了 2.4 个积分。积分到底怎么算，怎么花得值？这集番外讲清楚。",
 "B每个任务的账": "每个任务开始时，它会给一个预计消耗的范围；跑的过程中，显示已经消耗了多少；结束时，底部写着这次一共花了多少。所以账是透明的，做完看一眼就知道。",
 "C套餐页": "总账在设置里的，套餐与积分。这里看你现在是什么套餐，还剩多少积分。基础积分按月刷新，平台奖励的积分有到期时间。具体价格和每档积分经常调整，以官网当天为准。",
 "D什么最费": "什么最费积分？第一，任务越长越费，读的材料多、步骤多，自然花得多。第二，模型档位越高越费。第三，Max 模式，消耗明显更快。还有一个容易忽略的：反复返工。说不清楚，改三遍，就花了三遍的钱。",
 "E省积分": "所以省积分就三招。先用快速档，不满意再升。需求一次说清楚，这是第三集讲的。复杂任务先开计划模式，方向对了再执行，这是第四集讲的。",
 "F收尾": "今天三句话：每个任务都有账，档位和返工最花钱，说清楚就是最好的省钱办法。感谢你看到这里。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F13 = K.F; G5 = f"{V}/footage/ep01/G5-执行.mov"

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("R", G5, {"anchors": [[89.0, 0], [89.0 + t, t]], "drop_masks": DROP, "masks_extra": [USER],
                "events_override": [{"t": 89.3, "kind": "move", "target": [495,612,320,34], "label": "共消耗 2.4", "zoom": 2.4, "focus": True, "dur": t - 1.2}]})]
    n = "B每个任务的账"; t = T(n); b2 = at(n, "跑的过程中"); b3 = at(n, "结束时")
    P[n] = [("R", G5, {"anchors": [[29.0, 0], [31.0, b2], [84.0, b2 + 0.3], [86.0, b3 - 0.5], [89.0, b3], [89.0 + t - b3, t]], "drop_masks": DROP, "masks_extra": [USER, PROMO([[0, 6]])],
                "events_override": [{"t": 29.2, "kind": "move", "target": [470,186,330,38], "label": "开始：预计消耗范围", "zoom": 2.0, "focus": True, "dur": 1.6},
                                    {"t": 31.2, "kind": "move", "target": [470,430,520,34], "label": "过程中：已消耗", "zoom": 2.0, "focus": True, "dur": 1.0},
                                    {"t": 89.2, "kind": "move", "target": [495,612,320,34], "label": "结束：一共花了多少", "zoom": 2.2, "focus": True, "dur": t - b3 - 1.0}]})]
    n = "C套餐页"; t = T(n)
    P[n] = [("R", f"{F13}/C-套餐与积分.mov", {"anchors": [[2.4, 0], [2.8, at(n,"这里看")], [5.7, at(n,"还剩多少")-0.3], [8.8, at(n,"基础积分")], [12.0, at(n,"具体价格")], [13.2, t]],
                "drop_masks": DROP + ["总剩余"], "masks_extra": [USER, {"name":"总剩余2","rect":[672,168,122,46],"style":"fillmed"}],
                "patch": [{"contains": "当前套餐", "set": {"zoom": 2.0}}, {"contains": "总剩余", "set": {"zoom": 1.8}}, {"contains": "按月刷新", "set": {"zoom": 1.5, "focus": True, "label": "基础积分月刷新，奖励积分会到期"}}],
                "events_extra": [{"t": 12.1, "kind": "move", "target": [664,100,650,430], "label": "价格以官网当天为准", "zoom": 1.2, "dur": 1.2}]})]
    n = "D什么最费"; t = T(n)
    P[n] = [("CARD", "d", t, [{"from": 0, "to": t, "last": True, "lines": [("什么最费积分", "t", 0.2),
        ("① 任务越长越费", "n", at(n,"第一")), ("② 档位越高越费", "n", at(n,"第二")), ("③ Max 模式消耗更快", "n", at(n,"第三")), ("④ 反复返工", "r", at(n,"还有一个"))]}])]
    n = "E省积分"; t = T(n)
    P[n] = [("CARD", "e", t, [{"from": 0, "to": t, "last": True, "lines": [("省积分三招", "t", 0.2),
        ("先用快速档，不满意再升", "n", at(n,"先用快速")), ("需求一次说清楚（第 3 集）", "n", at(n,"需求一次")), ("复杂任务先开计划（第 4 集）", "n", at(n,"复杂任务"))]}])]
    n = "F收尾"; t = T(n); nx = at(n, "感谢") - 0.15
    P[n] = [("CARD", "f", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 每个任务都有账", "n", at(n,"每个任务")), ("② 档位和返工最花钱", "n", at(n,"档位和")), ("③ 说清楚就是最好的省钱办法", "n", at(n,"说清楚"))]},
        {"from": nx, "to": t, "last": True, "lines": [("WorkBuddy 零基础实战", "b", nx+0.1), ("感谢收看", "s", nx+0.4)]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep13-番外-v1.mp4")
