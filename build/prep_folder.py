import sys; sys.path.insert(0,'.')
from human import *
subprocess.run(["osascript","-e",'tell application "WorkBuddy" to activate']); time.sleep(1.0)
h=Human()
h.move_to(531,521); h.click(); time.sleep(1.2)
h.move_to(547,478); h.click(); time.sleep(2.0)
# Cmd+Shift+G -> type path -> Enter
h.key(5, Quartz.kCGEventFlagMaskCommand|Quartz.kCGEventFlagMaskShift); time.sleep(1.0)
for ch in "/Users/Shared/周报素材": h._type_char(ch); time.sleep(0.03)
time.sleep(0.8); h.key(36); time.sleep(1.5)
subprocess.run(["screencapture","-x","/private/tmp/claude-501/-Volumes-Data-External-workspace-cc-test-wbd/21c7afcb-8140-452c-8ad3-07d43f627114/scratchpad/prep.png"])
