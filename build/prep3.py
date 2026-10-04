import sys; sys.path.insert(0,'.')
from human import *
h=Human()
C=Quartz.kCGEventFlagMaskCommand
h.key(0, C); time.sleep(0.2); h.key(9, C); time.sleep(1.2); h.key(36); time.sleep(1.5)
subprocess.run(["screencapture","-x","/private/tmp/claude-501/-Volumes-Data-External-workspace-cc-test-wbd/21c7afcb-8140-452c-8ad3-07d43f627114/scratchpad/prep.png"])
