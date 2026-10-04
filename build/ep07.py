#!/usr/bin/env python3
"""第 7 集：专家与专家团。用法：ep07.py voice | build"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from epkit import *

EP, TITLE = 7, "专家与专家团"
TEXT = {
 "A开场": "同样一句话，交给普通对话，和交给一个专家，结果不一样。专家自带方法，自带口吻。今天，认识专家和专家团。",
 "B找到": "左边，专家、技能、连接器，点一下，先弹出三个选项，选专家。这里就是专家中心。",
 "C逛": "最上面是精选场景，按你要做的事来推荐。下面分两个页签：专家，是单个角色；专家团，是一组角色分工协作。还可以按行业筛选，或者直接搜。",
 "D召唤": "找到合适的，点开看看它擅长什么，再点召唤专家。输入框里多了它的标识，还预填了一个示例需求。删掉，换成我的：把这个文件夹里的周报，改写成一段给领导看的简短汇报，一百字以内，只用周报里的内容。一分钟后，它给了一段九十多字的汇报，数字都对得上，还说明了每句话取自周报的哪一段。",
 "E专家团": "专家团是升级版。点开一个看看：一位主理人，加上好几个成员，各管一段。交一个大任务，主理人先拆分，再分给成员一起做，最后汇总。适合步骤多的大活。代价是时间更长、积分更多，小任务没必要用。",
 "F我的专家": "右上角，我的专家，可以创建你自己的专家。建议先用现成的，用熟了，再建自己的。",
 "G收尾": "今天三句话：专家是带方法的角色，专家团适合大活，先用现成的再自己建。下一集，讲材料从哪来，成品放哪去。",
}
ORDER = list(TEXT)
K = Kit(EP, TEXT, ORDER)
F7 = K.F

def plan():
    at, T = K.at, K.T
    P = {}
    n = "A开场"; t = T(n)
    P[n] = [("R", f"{F7}/D-专家干活.mov", {"anchors": [[118.0, 0], [118.0 + t, t]], "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "events_override": [{"t": 118.3, "kind": "move", "target": [470,160,760,40], "label": "交给专家", "zoom": 1.6, "dur": 2.6},
                                    {"t": 121.5, "kind": "move", "target": [476,270,760,58], "label": "按汇报的方式重写", "zoom": 1.6, "focus": True, "dur": t - 4.0}]})]
    n = "B找到"; t = T(n)
    P[n] = [("R", f"{F7}/BC-逛专家并召唤.mov", {"anchors": [[2.4, 0], [4.1, at(n,"点一下")+0.3], [7.4, at(n,"选专家")+0.4], [9.4, t]],
                "drop_masks": DROP, "masks_extra": [USER, PROMO([[0, 3]])],
                "patch": [{"contains": "专家·技能", "set": {"zoom": 1.6}}, {"contains": "专家", "set": {"zoom": 1.8}}]})]
    n = "C逛"; t = T(n)
    P[n] = [("R", f"{F7}/BC-逛专家并召唤.mov", {"anchors": [[9.4, 0], [9.5, at(n,"最上面")], [13.8, at(n,"下面分两个")], [15.0, at(n,"专家团")+0.3], [21.3, at(n,"还可以")-0.4], [23.9, at(n,"按行业")], [27.5, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "精选场景", "set": {"zoom": 1.3}}, {"contains": "专家团", "set": {"zoom": 2.0}}, {"contains": "分工协作", "set": {"zoom": 1.2}},
                          {"contains": "按行业", "set": {"zoom": 1.6}}]})]
    n = "D召唤"; t = T(n); d2 = at(n, "输入框里多了") - 0.2
    P[n] = [("R", f"{F7}/BC-逛专家并召唤.mov", {"anchors": [[27.5, 0], [29.6, at(n,"点开看看")+0.3], [31.4, at(n,"它擅长")], [35.7, at(n,"再点召唤")], [37.4, at(n,"召唤专家")+0.4], [39.5, d2]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "选一个专家", "set": {"zoom": 1.8}}, {"contains": "擅长", "set": {"zoom": 1.5, "focus": True}}, {"contains": "召唤专家", "set": {"zoom": 2.0, "focus": True}}]}),
            ("R", f"{F7}/D-专家干活.mov", {"anchors": seg_anchor([[2.4, d2], [2.8, at(n,"输入框里多了")+0.2], [5.6, at(n,"还预填")], [8.2, at(n,"删掉")+0.2], [9.5, at(n,"换成我的")+0.4],
                                                                    [22.6, at(n,"一分钟后")-0.4], [25.0, at(n,"一分钟后")], [118.0, at(n,"它给了一段")], [122.8, t]], d2),
                "drop_masks": DROP, "masks_extra": [USER, PROMO()],
                "badges": [{"from": 25.0, "to": 116.0, "text": "加速播放 · 实际 {real}", "t0": 22.6}],
                "patch": [{"contains": "专家已就位", "set": {"zoom": 2.0, "focus": True, "label": "多了专家标识"}}, {"contains": "示例需求", "set": {"zoom": 1.6}},
                          {"contains": "换成我的", "set": {"zoom": 1.5}}],
                "events_extra": [{"t": 118.4, "kind": "move", "target": [476,270,760,58], "label": "九十多字，数字都对", "zoom": 1.6, "focus": True, "dur": 2.6},
                                 {"t": 121.2, "kind": "move", "target": [476,340,760,52], "label": "每句取自哪一段", "zoom": 1.6, "focus": True, "dur": 1.4}]})]
    n = "E专家团"; t = T(n)
    P[n] = [("R", f"{F7}/EF-专家团与我的专家.mov", {"anchors": [[2.6, 0], [5.1, at(n,"点开一个")+0.6], [7.4, at(n,"一位主理人")-0.4], [14.4, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "打开一个专家团", "set": {"zoom": 1.8}}],
                "events_extra": [{"t": 7.8, "kind": "move", "target": [420,585,612,150], "label": "主理人 + 成员", "zoom": 1.7, "focus": True, "dur": 4.0},
                                 {"t": 12.0, "kind": "move", "target": [420,145,600,60], "label": "召唤专家团", "zoom": 1.8, "dur": 1.8}]})]
    n = "F我的专家"; t = T(n)
    P[n] = [("R", f"{F7}/EF-专家团与我的专家.mov", {"anchors": [[15.6, 0], [18.1, at(n,"我的专家")+0.5], [20.3, at(n,"可以创建")], [25.7, t]],
                "drop_masks": DROP, "masks_extra": [USER],
                "patch": [{"contains": "我的专家", "set": {"zoom": 1.8}}],
                "events_extra": [{"t": 20.5, "kind": "move", "target": [800,278,110,30], "label": "创建专家", "zoom": 2.0, "focus": True, "dur": 3.4}]})]
    n = "G收尾"; t = T(n); nx = at(n, "下一集") - 0.15
    P[n] = [("CARD", "g", t, [
        {"from": 0, "to": nx, "lines": [("今天三句话", "t", 0.2), ("① 专家是带方法的角色", "n", at(n,"专家是")), ("② 专家团适合大活", "n", at(n,"专家团适合")), ("③ 先用现成的，再自己建", "n", at(n,"先用现成"))]},
        {"from": nx, "to": t, "last": True, "lines": [("下一集", "t", nx+0.1), ("材料从哪来，成品放哪去", "b", at(n,"讲材料"))]}])]
    return P

if __name__ == "__main__":
    if sys.argv[1] == "voice": K.voice()
    elif sys.argv[1] == "build":
        body = K.build_body(plan(), f"{K.B}/body.mp4")
        K.finish(body, TITLE, f"{V}/ep07-v1.mp4")
