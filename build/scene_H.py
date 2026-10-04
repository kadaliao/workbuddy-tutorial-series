import sys; sys.path.insert(0,'.')
from human import *
DOC=[864,169,565,659]; TABLE=[947,477,382,98]
def run(h):
    h.pause(1.0,label="成品预览")
    h.move_to(1140,300,target=DOC,label="右侧是成品预览"); h.pause(1.2)
    h.move_to(1138,526,target=TABLE,label="数据表现：表格里的数字来自 CSV"); h.pause(2.0,2.4,label="悬停在表格上")
    h.move_to(1138,380,dur=0.7,target=DOC)
    h.scroll(260,dur=3.0,label="慢慢往下看整份周报",target=DOC); h.pause(1.2)
    h.scroll(260,dur=2.5,target=DOC); h.pause(1.2)
    h.scroll(-600,dur=3.0,label="回到页首",target=DOC); h.pause(1.5)
    h.move_to(1138,300,dur=0.7); h.pause(1.0)
scene("H-验收",run,extra={"mask_regions":[{"name":"侧栏用户行","rect":[8,795,180,55]},{"name":"左侧回复首行含本机绝对路径(含用户名)","rect":[390,100,380,24]},{"name":"左侧过程/工具调用行可能含 /Applications 与用户目录路径","rect":[390,140,380,260]}]})
