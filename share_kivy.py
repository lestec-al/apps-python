from kivy.config import Config
Config.set('graphics', 'maxfps', '60')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.dialog import MDDialog
import kivy
if kivy.platform == "android":
    from kivymd.utils.set_bars_colors import set_bars_colors
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
import os, stat, re, sys, time
import socket, http.server, socketserver, threading, pyqrcode, requests
from ftplib import FTP
from requests.utils import requote_uri
from urllib import request
from pathlib import Path


kivy_str = """
#:import images_path kivymd.images_path
#:import path os.path


<ListFTPLabel>:

    IconLeftWidgetWithoutTouch:
        icon: root.icon
        ripple_scale: 0
        md_bg_color: app.theme_cls.bg_normal

<FTPScreen>:

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: "keyboard-backspace"
                pos_hint: {"center_x":.5, "center_y":.5}
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal
                on_release: root.change_screen()

            MDIconButton:
                icon: "arrow-up"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release: root.move_up(self)
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal

            MDLabel:
                adaptive_height: True
                id: path_text
                halign: "center"
                size: self.texture_size
                text: r"C:\\Users\\alex-win\\Downloads\\test"

            MDTextField:
                adaptive_height: True
                id: url_text
                halign: "center"
                text: "192.168.100.144:8000"

        RecycleView:
            id: rv
            key_viewclass: "viewclass"
            key_size: "height"
            size_hint: 1.0,1.0
            bar_width: dp(10)
            scroll_type: ["bars", "content"]
            effect_cls: "ScrollEffect"
            on_scroll_move: root.scroll_timer(True)

            RecycleBoxLayout:
                default_size: None, dp(60)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"


<ListLabel>:

    IconLeftWidgetWithoutTouch:
        icon: root.icon
        ripple_scale: 0
        md_bg_color: app.theme_cls.bg_normal

<FilesScreen>:

    MDBoxLayout:
        orientation: 'vertical'

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: "keyboard-backspace"
                pos_hint: {"center_x":.5, "center_y":.5}
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal
                on_release: root.change_screen()

            MDIconButton:
                icon: "arrow-up"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release: root.move_up(self)
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal

            MDIconButton:
                icon: "check"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release: root.change_screen(path_text.text)
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal

            MDTextField:
                id: path_text
                text: root.last_path
                on_text_validate: root.update_files(self.text)

        RecycleView:
            id: rv
            key_viewclass: "viewclass"
            key_size: "height"
            size_hint: 1.0,1.0
            bar_width: dp(10)
            scroll_type: ["bars", "content"]
            effect_cls: "ScrollEffect"
            on_scroll_move: root.scroll_timer(True)

            RecycleBoxLayout:
                default_size: None, dp(60)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"


<ShareScreen>:

    MDBoxLayout:
        id: box_layout
        orientation: 'vertical'

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                id: start_stop_button
                icon: "play-outline"
                pos_hint: {"center_x":.5, "center_y":.5}
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal
                on_release: root.start_stop()

            MDIconButton:
                id: folder_edit_button
                icon: "folder-edit"
                pos_hint: {"center_x":.5, "center_y":.5}
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal
                on_release: root.change_screen()

            MDLabel:
                id: connections_label
                text: "0 connected"

            MDIconButton:
                id: download_button
                icon: "cloud-download-outline"
                pos_hint: {"center_x":.5, "center_y":.5}
                ripple_scale: 0
                md_bg_color: app.theme_cls.bg_normal
                on_release: root.download()

        MDLabel:
            adaptive_height: True
            id: path_text
            halign: "center"
            size: self.texture_size

        MDTextField:
            adaptive_height: True
            id: url_text
            halign: "center"
            text: "192.168.100.144:8000"

        TextInput:
            id: output_widget
"""


class FTPScreen(Screen):
    home_path = None
    last_path = home_path
    button_pressed_time = None
    scroll_end_time = None

    def show_ftp_files(self, dirname):
        def add_item(text, path, icon):
            self.ids.rv.data.append({"viewclass": "ListLabel", "icon": icon, "text": text, "path": path})

        try:

            # Scan
            if kivy.platform == "android":
                request_permissions([Permission.INTERNET])

            files = os.listdir(dirname)

            files_list, dirs_list = [], []
            for f in files:
                f_path = os.path.join(dirname, f)
                f_stat = os.stat(f_path)
                size = self.convert_size(f_stat.st_size)
                if os.path.isdir(f_path):
                    if sys.platform == "win32":
                        if not f.is_symlink() and not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                            dirs_list.append([f, "dir", f_path, "folder"])
                    else:
                        if not f.name.startswith("."):
                            dirs_list.append([f, "dir", f_path, "folder"])
                if os.path.isfile(f_path):
                    if sys.platform == "win32":
                        if not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                            files_list.append([f, size[0], f_path, "file", size[1]])
                    else:
                        if not f.name.startswith("."):
                            files_list.append([f, size[0], f_path, "file", size[1]])
            # Sorting
            if self.sort == "size":
                if self.reverse == False:
                    dirs_list.sort(key=lambda s: s[0])
                    files_list.sort(key=lambda s: s[4])
                if self.reverse == True:
                    dirs_list.sort(key=lambda s: s[0], reverse=True)
                    files_list.sort(key=lambda s: s[4], reverse=True)
            else:
                if self.reverse == False:
                    dirs_list.sort(key=lambda f: f[0])
                    files_list.sort(key=lambda f: f[0])
                elif self.reverse == True:
                    dirs_list.sort(key=lambda f: f[0], reverse=True)
                    files_list.sort(key=lambda f: f[0], reverse=True)
            # Clear old & Add new
            self.ids.rv.data = []
            for i in dirs_list:
                add_item(text=i[0], secondary_text=f"{i[1]}", path=i[2], icon=i[3])
            for i in files_list:
                add_item(text=i[0], secondary_text=f"{i[1]}", path=i[2], icon=i[3])
            self.last_path = dirname
            self.ids.text_input.text = dirname
            self.ids.rv.scroll_y = 1# return scroll to up

        except Exception as e:
            MDDialog(text=f"{e}").open()

    def connect_ftp(self):
        try:
            os.chdir(self.ids.path_text.text)

            x = self.ids.url_text.text.rsplit(":")

            self.ftp = FTP("")
            self.ftp.connect(x[0],int(x[1]))
            self.ftp.login()
            file_names = self.ftp.nlst()

            for filename in file_names:
                filename

        except Exception as e:
            self.ids.output_widget.text += "FTP\n"
            self.ids.output_widget.text += f"{e}\n"

    def disconnect_ftp(self):
        self.ftp.close()

    def change_screen(self, text=None):
        if text != None:
            app.screen.ids.path_text.text = text
        app.screen_manager.current = "share_screen"

    def move_up(self, button):
        if self.timer():
            up_path = self.last_path.rsplit(self.slash, 1)
            self.update_files(up_path[0])

    def scroll_timer(self, var=None):
        if var == True:
            self.scroll_end_time = time.time()
        elif var == None:
            if self.scroll_end_time == None or time.time() - self.scroll_end_time > 1.0:
                return True
            else:
                return False

    def timer(self):
        if self.button_pressed_time == None or time.time() - self.button_pressed_time > 0.5:
            self.button_pressed_time = time.time()
            return True
        else:
            return False

    def convert_size(self, var):
        if type(var) == type(1):
            s = var
        else:
            s = os.stat(var).st_size
        if s < 1000:
            size = str(s) + " B"
        if s >= 1000:
            size = str(round(s/1000, 2)) + " KB"
        if s >= 1000000:
            size = str(round(s/1000000, 2)) + " MB"
        if s >= 1000000000:
            size = str(round(s/1000000000, 2)) + " GB"
        if s >= 1000000000000:
            size = str(round(s/1000000000000, 2)) + " TB"
        return [size, s]


class ListLabel(OneLineIconListItem):
    icon = StringProperty()
    divider = None
    ripple_scale = 0

    def on_release(self):
        if app.screen_files.timer() and app.screen_files.scroll_timer():
            app.screen_files.update_files(self.path)
        return super().on_release()


class FilesScreen(Screen):
    if kivy.platform == "android":
        home_path = primary_external_storage_path()
    else:
        home_path = str(Path.home())
    last_path = home_path
    slash = "\\" if sys.platform == "win32" else "/"
    button_pressed_time = None
    scroll_end_time = None

    def update_files(self, dirname):
        def add_item(text, path, icon):
            self.ids.rv.data.append({"viewclass": "ListLabel", "icon": icon, "text": text, "path": path})

        try:
            # Check path
            if re.match(r".+\\$", dirname) or re.match(r".+/$", dirname):
                dirname = dirname[0:-1]
            if re.match(r"\w:$", dirname) or dirname == "":
                dirname = dirname + self.slash
            # Scan
            if kivy.platform == "android":
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            files = os.scandir(dirname)
            files_list, dirs_list = [], []
            for f in files:
                f_stat = f.stat()
                if f.is_dir():
                    if sys.platform == "win32":
                        if not f.is_symlink() and not bool(f_stat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN):
                            dirs_list.append([f.name, f.path, "folder"])
                    else:
                        if not f.name.startswith("."):
                            dirs_list.append([f.name, f.path, "folder"])
            dirs_list.sort(key=lambda f: f[0])
            # Clear old & Add new
            self.ids.rv.data = []
            for i in dirs_list:
                add_item(text=i[0], path=i[1], icon=i[2])
            for i in files_list:
                add_item(text=i[0], path=i[1], icon=i[2])
            self.last_path = dirname
            self.ids.path_text.text = dirname
            self.ids.rv.scroll_y = 1# return scroll to up

        except Exception as e:
            MDDialog(text=f"{e}").open()

    def change_screen(self, text=None):
        if text != None:
            app.screen.ids.path_text.text = text
        app.screen_manager.current = "share_screen"

    def move_up(self, button):
        if self.timer():
            up_path = self.last_path.rsplit(self.slash, 1)
            self.update_files(up_path[0])

    def scroll_timer(self, var=None):
        if var == True:
            self.scroll_end_time = time.time()
        elif var == None:
            if self.scroll_end_time == None or time.time() - self.scroll_end_time > 1.0:
                return True
            else:
                return False

    def timer(self):
        if self.button_pressed_time == None or time.time() - self.button_pressed_time > 0.5:
            self.button_pressed_time = time.time()
            return True
        else:
            return False

    def convert_size(self, var):
        if type(var) == type(1):
            s = var
        else:
            s = os.stat(var).st_size
        if s < 1000:
            size = str(s) + " B"
        if s >= 1000:
            size = str(round(s/1000, 2)) + " KB"
        if s >= 1000000:
            size = str(round(s/1000000, 2)) + " MB"
        if s >= 1000000000:
            size = str(round(s/1000000000, 2)) + " GB"
        if s >= 1000000000000:
            size = str(round(s/1000000000000, 2)) + " TB"
        return [size, s]


class MySimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        Clock.schedule_once(
            lambda d: app.screen.update_output(f"{self.log_date_time_string()} - {self.address_string()} - {format%args}\n"), 0.5)

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
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
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


class MyThreadingTCPServer(socketserver.ThreadingTCPServer):
    def verify_request(self, request, client_address):
        if client_address[0] not in app.screen.connections:
            app.screen.connections.append(client_address[0])
        app.screen.ids.connections_label.text = f"{len(app.screen.connections)} connected"
        return True


class MyServer(threading.Thread):
    def run(self):
        self.server = MyThreadingTCPServer(("", app.screen.port), MySimpleHTTPRequestHandler)
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


class ShareScreen(Screen):
    server = None
    port = 8000
    connections = []

    def update_output(self, new_str):
        self.ids.output_widget.text += new_str

    def change_screen(self):
        app.screen_files.update_files(app.screen_files.home_path)
        app.screen_manager.current = 'files_screen'

    def start_stop(self):
        if self.server == None:
            try:
                self.connections.clear()
                self.ids.output_widget.text = ""

                os.chdir(self.ids.path_text.text)

                self.ids.folder_edit_button.disabled = True
                self.ids.download_button.disabled = True
                self.ids.start_stop_button.icon = "stop"

                link = f"http://{socket.gethostbyname(socket.gethostname())}:{self.port}"
                self.ids.output_widget.text += f"Sharing start at {link}\n"
                # QRcode
                qr = pyqrcode.create(link)
                qr.png("testq2w3e4r5t6y7u8i9o0pgtttgbnjff.png", scale=6, background=[0xfa, 0xfa, 0xfa])
                self.img = Image(source="testq2w3e4r5t6y7u8i9o0pgtttgbnjff.png")
                self.ids.box_layout.add_widget(self.img, -1)
                os.remove("testq2w3e4r5t6y7u8i9o0pgtttgbnjff.png")

                self.server = MyServer()
                self.server.start()

            except Exception as e:
                self.ids.output_widget.text += f"{e}\n"

        elif self.server != None:
            self.server.stop()
            self.server = None

            self.ids.box_layout.remove_widget(self.img)
            self.ids.start_stop_button.icon = "play-outline"
            self.ids.folder_edit_button.disabled = False
            self.ids.download_button.disabled = False
            self.ids.connections_label.text = "0 connected"
            self.ids.output_widget.text += "Sharing stop\n"

    def download(self):
        self.ids.start_stop_button.disabled = True
        self.ids.folder_edit_button.disabled = True
        self.ids.download_button.disabled = True

        try:
            os.chdir(self.ids.path_text.text)

            # TCP connection attempt
            try:
                raw_request = requests.get(f"http://{self.ids.url_text.text}/")
                decode_request = raw_request.content.decode("utf-8")
                files_indexes = re.finditer("download>", decode_request)
                self.ids.output_widget.text += f"{len(files_indexes)} files\n"

                for i in files_indexes:
                    start_index = i.span()[1]
                    len_index = decode_request[start_index:].find("</")
                    file = decode_request[start_index:start_index+len_index]
                    url_file = requote_uri(file)
                    request.urlretrieve(f"http://{self.ids.url_text.text}/{url_file}", file)
                    self.ids.output_widget.text += f"{file} - OK\n"

            except Exception as e:
                self.ids.output_widget.text += "Web\n"
                self.ids.output_widget.text += f"{e}\n"

                # FTP connection attempt
                try:
                    x = self.ids.url_text.text.rsplit(":")
                    with FTP("") as ftp:
                        ftp.connect(x[0],int(x[1]))
                        ftp.login()
                        file_names = ftp.nlst()
                        self.ids.output_widget.text += f"{len(file_names)} files\n"

                        for filename in file_names:
                            with open( filename, "wb" ) as file:
                                ftp.retrbinary("RETR %s" % filename, file.write)
                                file.close()
                                self.ids.output_widget.text += f"{filename} - OK\n"

                except Exception as e:
                    self.ids.output_widget.text += "FTP\n"
                    self.ids.output_widget.text += f"{e}\n"

        except Exception as e:
            self.ids.output_widget.text += f"{e}\n"

        self.ids.start_stop_button.disabled = False
        self.ids.folder_edit_button.disabled = False
        self.ids.download_button.disabled = False


class ShareApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(kivy_str)
        self.screen_files = FilesScreen(name="files_screen")
        self.screen = ShareScreen(name="share_screen")
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(self.screen)
        self.screen_manager.add_widget(self.screen_files)

    def build(self):
        if kivy.platform == "android":
            self.set_bars_colors_s()
            request_permissions([Permission.INTERNET])
        else:
            self.icon = "data/copy.png"
        return self.screen_manager

    def set_bars_colors_s(self):
            set_bars_colors(app.theme_cls.bg_normal, app.theme_cls.bg_normal, "Dark")

app = ShareApp()
app.run()