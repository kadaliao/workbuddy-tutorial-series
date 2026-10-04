import sys, json; sys.path.insert(0,'.')
from human import *
APP=[419,277,65,65]; APPS=[733,277,76,76]
FIND_BTN='''
tell application "System Events"
  repeat with pn in {"Finder","CoreServicesUIAgent","UserNotificationCenter"}
    try
      tell process pn
        repeat with w in windows
          try
            set bs to every button of w
          on error
            set bs to {}
          end try
          try
            repeat with sh in sheets of w
              set bs to bs & (every button of sh)
            end repeat
          end try
          repeat with b in bs
            set nm to name of b
            if nm is "停止" or nm is "Stop" then
              set p to position of b
              set s to size of b
              return pn & "|" & nm & "|" & (item 1 of p) & "," & (item 2 of p) & "," & (item 1 of s) & "," & (item 2 of s)
            end if
          end repeat
        end repeat
      end tell
    end try
  end repeat
  return ""
end tell'''
def find_stop():
    out=subprocess.run(["/private/tmp/claude-501/wl"],capture_output=True,text=True).stdout
    for ln in out.splitlines():
        if "拷贝" in ln:
            p=ln.split()
            x,y,w,hh=[int(v) for v in p[-5:-1]]
            # 停止 button: ~63% across, ~78% down the dialog
            bx=x+int(w*0.631); by=y+int(hh*0.784)
            return f"Finder|停止|{bx-30},{by-12},60,24"
    return ""
state={}
def run(h):
    h.pause(1.2)
    h.move_to(451,312,target=APP,label="WorkBuddy 图标"); h.pause(0.7,0.9)
    h.log("click",label="拖进「应用程序」",target=APP); h.mouse_down(); time.sleep(0.3)
    h.move_to(771,312,dur=1.5,target=APPS,label=None,overshoot=False,drag=True); time.sleep(0.12)
    h.log("click",label="松手，开始安装",target=APPS); h.mouse_up()
    t=mono(); res=""
    while mono()-t<8:
        res=find_stop()
        if res: break
        time.sleep(0.4)
    state["dialog"]=res
    h.pause(1.5,1.7)            # let the dialog sit in frame
    if res:
        pn,nm,pos=res.split("|"); x,y,w,hh=[int(v) for v in pos.split(",")]
        bx,by=x+w/2-80, y+hh/2-40
        h.move_to(bx,by,dur=0.9,target=[x-80,y-40,w,hh],label="选「停止」，不替换"); h.pause(0.5,0.7)
        h.click("点「停止」",[x-80,y-40,w,hh]); h.pause(1.2,1.5)
    else:
        h.esc(); h.pause(1.0)
    h.move_to(900,700,dur=0.8); h.pause(1.0)
h=scene("C-安装",run,park=(900,720),pre_wait=1.0,extra={"mask_regions":[{"name":"侧栏左下用户行(WorkBuddy 窗口在 dmg 窗口后面)","rect":[8,795,180,55]},{"name":"右上推广按钮","rect":[1240,0,200,34]}]})
print("dialog:",state.get("dialog"))
