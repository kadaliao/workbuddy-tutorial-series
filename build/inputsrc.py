"""列出/切换输入法：inputsrc.py list | current | select <id>"""
import sys, ctypes, ctypes.util
from Foundation import NSString
import objc
carbon = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Carbon"))
cf = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreFoundation"))
carbon.TISCopyCurrentKeyboardInputSource.restype = ctypes.c_void_p
carbon.TISCreateInputSourceList.restype = ctypes.c_void_p
carbon.TISCreateInputSourceList.argtypes = [ctypes.c_void_p, ctypes.c_bool]
carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p
carbon.TISGetInputSourceProperty.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
carbon.TISSelectInputSource.argtypes = [ctypes.c_void_p]
cf.CFArrayGetCount.restype = ctypes.c_long; cf.CFArrayGetCount.argtypes = [ctypes.c_void_p]
cf.CFArrayGetValueAtIndex.restype = ctypes.c_void_p; cf.CFArrayGetValueAtIndex.argtypes = [ctypes.c_void_p, ctypes.c_long]
kID = ctypes.c_void_p.in_dll(carbon, "kTISPropertyInputSourceID")
kSel = ctypes.c_void_p.in_dll(carbon, "kTISPropertyInputSourceIsSelectCapable")
def sid(src): return str(objc.objc_object(c_void_p=carbon.TISGetInputSourceProperty(src, kID)))
def srcs():
    arr = carbon.TISCreateInputSourceList(None, False)
    return [cf.CFArrayGetValueAtIndex(arr, i) for i in range(cf.CFArrayGetCount(arr))]
cmd = sys.argv[1]
if cmd == "current": print(sid(carbon.TISCopyCurrentKeyboardInputSource()))
elif cmd == "list": [print(sid(s)) for s in srcs()]
elif cmd == "select":
    for s in srcs():
        if sid(s) == sys.argv[2]: print("select", sid(s), carbon.TISSelectInputSource(s)); break
    else: print("not found")
