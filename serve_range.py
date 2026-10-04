import os,re,sys
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
class H(SimpleHTTPRequestHandler):
    def send_head(self):
        r=self.headers.get("Range"); path=self.translate_path(self.path)
        if not r or not os.path.isfile(path): return super().send_head()
        m=re.match(r"bytes=(\d*)-(\d*)",r)
        size=os.path.getsize(path); a,b=m.groups()
        if a=="": start=max(0,size-int(b)); end=size-1
        else: start=int(a); end=int(b) if b else size-1
        end=min(end,size-1)
        if start>=size: self.send_error(416); return None
        f=open(path,"rb"); f.seek(start); self.range=(start,end)
        self.send_response(206); self.send_header("Content-Type",self.guess_type(path))
        self.send_header("Content-Range",f"bytes {start}-{end}/{size}"); self.send_header("Content-Length",str(end-start+1))
        self.send_header("Accept-Ranges","bytes"); self.end_headers(); return f
    def copyfile(self,src,dst):
        rg=getattr(self,"range",None); self.range=None
        if not rg: return super().copyfile(src,dst)
        left=rg[1]-rg[0]+1
        while left>0:
            d=src.read(min(65536,left))
            if not d: break
            try: dst.write(d)
            except (BrokenPipeError,ConnectionResetError): break
            left-=len(d)
    def end_headers(self):
        self.send_header("Accept-Ranges","bytes"); super().end_headers()
ThreadingHTTPServer(("127.0.0.1",8888),H).serve_forever()
