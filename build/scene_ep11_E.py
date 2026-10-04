import sys, hashlib; sys.path.insert(0,'.')
from wslib import *
O="/Volumes/Data-External/workspace/cc-test/wbd/video/footage/ep11"
BOX=[454,358,795,143]
T1="用腾讯文档连接器帮我新建一个文档，标题叫“连接器测试”，内容是一段虚构的周会纪要：3 条决议、2 条待办。先把草稿发给我看，我确认后再创建。只操作这一个文档，不要搜索或列出我其他的文档。"
def snap(p="/private/tmp/claude-501/poll.png"):
    subprocess.run(["screencapture","-x","-R80,40,1440,860",p]); return hashlib.md5(open(p,"rb").read()).hexdigest()
def wait(h, maxs, mins):
    t0=mono(); last=None; stable=0
    while mono()-t0 < maxs:
        h.jitter(2.5); hs=snap(); stable = stable+1 if hs==last else 0; last=hs
        if stable>=5 and mono()-t0>mins: break
    return round(mono()-t0,1)
def E1(h):
    h.pause(0.8)
    h.move_to(640,395,dur=0.7,target=BOX); h.pause(0.3); h.click(None,BOX); h.pause(0.4); h.click(); h.pause(0.4)
    h.type_text(T1,label="先出草稿，确认后再创建",target=BOX); h.pause(0.8)
    if not ocr.find("连接器测试"): raise RuntimeError("not typed")
    h.move_to(1220,473,target=[1195,448,50,50]); h.pause(0.4); h.click(None,[1195,448,50,50]); h.log("mark",text="send")
    print("E1 waited", wait(h, 300, 20)); h.log("mark",text="draft")
    subprocess.run(["cp","/private/tmp/claude-501/poll.png","/private/tmp/claude-501/draft.png"])
if __name__=="__main__":
  h=Human(); new_task(h); pick_folder(h, "/Users/Shared/周报素材")
  scene("E1-草稿",E1,outdir=O,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
