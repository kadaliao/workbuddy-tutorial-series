import sys; sys.path.insert(0,'.')
from human import *
h=Human(); r=Recorder('/private/tmp/claude-501/t1.mov'); r.start(); time.sleep(2.0)
h.move_to(700,600,dur=0.1,log=False); time.sleep(1.0)
h.move_to(300,300,dur=1.0); h.pause(.3); h.click('x'); time.sleep(0.5)
r.stop(); print(finalize('t1',r,h,(700,600)))
