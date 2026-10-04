import sys, hashlib; sys.path.insert(0,'.')
from wslib import *
from scene_ep11_E import wait
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep11"
BOX=[454,358,795,143]
T="读取腾讯文档《连接器测试》，用三句话总结：做了哪些决定、谁负责什么、下次什么时候开会。只读这一个文档。"
def F1(h):
    h.pause(0.8)
    h.move_to(640,395,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text(T,label="让它读在线文档",target=BOX); h.pause(0.8)
    if not ocr.find("连接器测试"): raise RuntimeError("not typed")
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50]); h.log("mark",text="send")
    print("F waited", wait(h, 300, 20)); h.log("mark",text="done")
    subprocess.run(["cp","/private/tmp/claude-501/poll.png","/private/tmp/claude-501/read.png"])
h=Human(); new_task(h); pick_folder(h, "/Users/Shared/周报素材")
scene("F-读取总结",F1,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
