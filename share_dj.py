import tkinter as tk, os, sys, platform, socket, http.server, socketserver, pyqrcode, threading, logging, subprocess
from tkinter import filedialog
from requests.utils import requote_uri
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer


# TCP
class TCPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        addOutputMsg(f"{self.log_date_time_string()} - {self.address_string()} - {format%args}\n")

    def list_directory(self, path):
        from http import HTTPStatus
        import html, io
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = requote_uri(self.path)
        except UnicodeDecodeError:
            displaypath = requote_uri(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Files %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                r.append('<li><a href="%s">%s</a></li>'
                        % (requote_uri(linkname), html.escape(displayname, quote=False)))
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
                r.append('<li><a href="%s">%s</a></li>'
                        % (requote_uri(linkname), html.escape(displayname, quote=False)))
            else:
                r.append('<li><a href="%s" download>%s</a></li>'
                        % (requote_uri(linkname), html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


class TCPServer(socketserver.ThreadingTCPServer):
    def verify_request(self, request, client_address):
        updateConnections(client_address[0])
        return True


class TCPThread(threading.Thread):
    def run(self):
        self.server = TCPServer(("", int(entryPort.get())), TCPRequestHandler)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


# FTP
class FTPLogHandler():
    def write(self, str=None):
        addOutputMsg(f"{str}")
    def flush(self, str=None):
        pass


class FTPServer(ThreadedFTPServer):
    def handle_accepted(self, request, client_address):
        updateConnections(client_address[0])
        return super().handle_accepted(request, client_address)


class FTPThread(threading.Thread):
    def run(self):
        authorizer = DummyAuthorizer()
        # authorizer.add_user("user", "12345", textPath.cget("text"), perm="elradfmwMT")
        authorizer.add_anonymous(textPath.cget("text"))
        handler = FTPHandler
        handler.authorizer = authorizer
        logging.basicConfig(stream=FTPLogHandler(), level=logging.INFO)
        self.server = FTPServer((IP, int(entryPort.get())), handler)
        self.server.serve_forever()

    def stop(self):
        self.server.close_all()


# DJANGO WEB
class WebLogHandler(threading.Thread):
    def run(self):
        with SERVER.stdout as s:
            try:
                for line in iter(s.readline, b''):
                    addOutputMsg(line.decode("utf-8").strip())

            except Exception as e:
                addOutputMsg(str(e))

    def stop(self):
        pass


#
def startStop(goal):
    textOutput.configure(state="normal")
    global SERVER
    global QR_IMG
    # Start
    if SERVER == None:
        try:
            path = textPath.cget("text")
            os.chdir(path)

            if goal == "web":
                pyPath = "python"
                webFound = False
                for f in os.scandir(path):
                    if f.name == "manage.py":
                        webFound = True
                    if f.is_dir():
                        for f1 in os.scandir(f.path.replace("\\", "/")):
                            if f1.is_dir():
                                for f2 in os.scandir(f1.path.replace("\\", "/")):
                                    if f2.name == "python.exe":
                                        pyPath = path + "/" + f.name + "/" + f1.name + "/" + "python.exe"
                                        break
                if webFound == False:
                    textOutput.insert("end", "Django web project not found in catalog\n")
                    return None

            CONNECTIONS.clear()
            textOutput.delete("1.0", "end")
            buttonCatalog.config(state="disabled")

            port = int(entryPort.get())
            address = f"{IP}:{int(entryPort.get())}"
            link = f"ftp://{address}" if goal == "ftp" else f"http://{address}"
            textURL.config(text=link)
            textURL.pack(side="top", pady=10)
            textOutput.insert("end", f"Start at {link}\n")

            QR_IMG = tk.BitmapImage(data=pyqrcode.create(link).xbm(scale=8))
            labelImage.config(image=QR_IMG)
            labelImage.pack(side="bottom")

            if goal == "tcp":
                buttonFTP.config(state="disabled")
                buttonWeb.config(state="disabled")
                SERVER = TCPThread()
                SERVER.start()

            elif goal == "ftp":
                buttonTCP.config(state="disabled")
                buttonWeb.config(state="disabled")
                SERVER = FTPThread()
                SERVER.start()
            
            elif goal == "web":
                buttonFTP.config(state="disabled")
                buttonTCP.config(state="disabled")
                SERVER = subprocess.Popen(
                    ["powershell", "-Command", f"{pyPath} {path}/manage.py runserver {IP}:{port}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                os.startfile(link)
                log = WebLogHandler()
                log.start()

        except Exception as e:
            textOutput.insert("end", f"{e}\n")
    # Stop
    else:
        if goal == "tcp":
            SERVER.stop()
            buttonFTP.config(state="normal")
            buttonWeb.config(state="normal")
        
        elif goal == "ftp":
            SERVER.stop()
            buttonTCP.config(state="normal")
            buttonWeb.config(state="normal")
        
        elif goal == "web":
            if os.name == 'nt':
                subprocess.Popen(f"TASKKILL /F /PID {SERVER.pid} /T")
            else:
                SERVER.terminate()
            buttonFTP.config(state="normal")
            buttonTCP.config(state="normal")

        SERVER = None
        labelImage.pack_forget()
        textURL.pack_forget()
        buttonCatalog.config(state="normal")
        labelConnections.config(text=" ")
        textOutput.insert("end", "\nStop\n")
    
    textOutput.configure(state="disabled")


def updateConnections(address):
    if address not in CONNECTIONS:
        CONNECTIONS.append(address)
    labelConnections.config(text=f"{len(CONNECTIONS)}")


def addOutputMsg(msg: str):
    textOutput.configure(state="normal")
    textOutput.insert("end", f"{msg}\n")
    textOutput.see("end")
    textOutput.configure(state="disabled")


def askPath():
    path = filedialog.askdirectory()
    if path != textPath.cget("text") and path != "":
        textPath.config(text=path)


SERVER = None
QR_IMG = None
CONNECTIONS = []
IP = socket.gethostbyname(socket.gethostname())

# Fix graphics on Win 10
if sys.platform == "win32" and platform.release() == "10":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# GUI
root = tk.Tk()
root.title("Share")
root.resizable(True, True)
root.iconphoto(False, tk.PhotoImage(file="data/copy.png"))
root.configure(bg="white")
window = tk.Frame(root, border=20, bg="white")
window.pack(side="top")

f = tk.Frame(window, border=1, bg="white")
f.pack(side="top", fill="x", expand=1, pady=1, padx=1)

buttonCatalog = tk.Button(f, text="Select catalog", font=("Arial", 12), bg="white", relief="groove", command=askPath)
buttonCatalog.pack(side="left", padx=5)

buttonTCP = tk.Button(
    f, text="TCP", font=("Arial", 12), bg="white", relief="groove", border=2, padx=5, command=lambda:startStop("tcp")
)
buttonTCP.pack(side="left", padx=5)

buttonFTP = tk.Button(
    f, text="FTP", font=("Arial", 12), bg="white", relief="groove", border=2, padx=5, command=lambda:startStop("ftp")
)
buttonFTP.pack(side="left", padx=5)

buttonWeb = tk.Button(f, text="Django web", font=("Arial", 12), bg="white", relief="groove", command=lambda:startStop("web"))
buttonWeb.pack(side="left", padx=5)

entryPort = tk.Entry(f, font=("Arial", 18), bg="white", width=10, justify="center", relief="groove")
entryPort.pack(side="left", padx=5)
entryPort.insert("end", "8000")

labelConnections = tk.Label(f, text=" ", font=("Arial", 12), bg="white")
labelConnections.pack(side="left", padx=5)

textPath = tk.Label(window, text="", font=("Arial", 12), border=2, bg="white")
textPath.pack(side="top", pady=10)

textURL = tk.Label(window, text="", font=("Arial", 12), border=2, bg="white")
labelImage = tk.Label(window, text="", font=("Arial", 12), border=2, bg="white")

textOutput = tk.Text(root, height=15, width=15)
textOutput.pack(side="bottom", fill="both", expand=1)
textOutput.configure(state="disabled")

root.mainloop()