import os
import sys
from PyQt5.QtWidgets import QApplication
from adblockparser import AdblockRules
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineCore, QtWebEngineWidgets
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QToolBar, QAction, QLineEdit, QProgressBar, QLabel, QMainWindow, QTabWidget, QStatusBar

# # Ad Blocker (Slow)
# with open("easylist.txt", encoding="utf8") as f:
#     raw_rules = f.readlines()
#     rules = AdblockRules(raw_rules)

# class setUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
#     def interceptRequest(self, info):
#         url = info.requestUrl().toString()
#         if rules.should_block(url):
#             # print("block::::::::::::::::::::::", url)
#             info.block(True)

class BrowserEngineView(QWebEngineView):
    tabs = []

    def __init__(self, Main, parent=None):
        super(BrowserEngineView, self).__init__(parent)
        self.mainWindow = Main

    def createWindow(self, QWebPage_WebWindowType):
        webview = BrowserEngineView(self.mainWindow)
        tab = BrowserTab(self.mainWindow)
        tab.browser = webview
        tab.setCentralWidget(tab.browser)
        self.tabs.append(tab)
        self.mainWindow.add_new_tab(tab)
        return webview


class BrowserTab(QMainWindow):
    def __init__(self, Main, parent=None):
        super(BrowserTab, self).__init__(parent)
        self.mainWindow = Main
        self.browser = BrowserEngineView(self.mainWindow)
        self.browser.load(QUrl.fromLocalFile(os.path.abspath('assets/html/index.html')))
        self.setCentralWidget(self.browser)
        self.navigation_bar = QToolBar('Navigation')
        self.navigation_bar.setIconSize(QSize(24, 24))
        self.navigation_bar.setMovable(False)
        self.addToolBar(self.navigation_bar)


        self.back_button = QAction(QIcon('assets/img/back.png'), 'Back', self)
        self.next_button = QAction(QIcon('assets/img/forward.png'), 'Next', self)
        self.stop_button = QAction(QIcon('assets/img/stop.png'), 'Stop', self)
        self.refresh_button = QAction(QIcon('assets/img/refresh.png'), 'Refresh', self)
        self.home_button = QAction(QIcon('assets/img/home.png'), 'Home', self)
        self.enter_button = QAction(QIcon('assets/img/search.png'), 'Search', self)
        self.add_button = QAction(QIcon('assets/img/new.png'), 'New Tab', self)
        self.ssl_label1 = QLabel(self)
        self.ssl_label2 = QLabel(self)
        self.url_text_bar = QLineEdit(self)
        self.url_text_bar.setMinimumWidth(300)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        # self.set_button = QAction(QIcon('assets/img/setting.png'), 'Settings', self)
        self.navigation_bar.addAction(self.back_button)
        self.navigation_bar.addAction(self.next_button)
        # Stop Button
        # self.navigation_bar.addAction(self.stop_button)
        self.navigation_bar.addAction(self.refresh_button)
        self.navigation_bar.addAction(self.home_button)
        self.navigation_bar.addAction(self.add_button)
        self.navigation_bar.addSeparator()
        self.navigation_bar.addWidget(self.ssl_label1)
        self.navigation_bar.addWidget(self.ssl_label2)
        self.navigation_bar.addWidget(self.url_text_bar)
        self.navigation_bar.addAction(self.enter_button)
        # self.navigation_bar.addSeparator()
        self.navigation_bar.addWidget(self.progress_bar)
        # self.navigation_bar.addSeparator()
        # Settings Button
        # self.navigation_bar.addAction(self.set_button)


    def navigate_to_url(self):
        s = QUrl(self.url_text_bar.text())
        if s.scheme() == '':
            s.setScheme('http')
        self.browser.load(s)

    def navigate_to_home(self):
        s = QUrl.fromLocalFile(os.path.abspath('assets/html/index.html'))
        self.browser.load(s)

    def renew_urlbar(self, s):
        prec = s.scheme()
        if prec == 'http':
            self.ssl_label1.setPixmap(QPixmap("assets/img/unsafe.png").scaledToHeight(24))
            self.ssl_label2.setText(" Unseccured SSL ")
            self.ssl_label2.setStyleSheet("color:#4d4d4d;")
        elif prec == 'https':
            self.ssl_label1.setPixmap(QPixmap("assets/img/safe.png").scaledToHeight(24))
            self.ssl_label2.setText(" Secured SSL ")
            self.ssl_label2.setStyleSheet("color:#228be6;")
        self.url_text_bar.setText(s.toString())
        self.url_text_bar.setCursorPosition(0)

    def renew_progress_bar(self, p):
        self.progress_bar.setValue(p)


class BrowserWindow(QMainWindow):
    name = "Pixify Web Browser"
    version = "1.1"
    date = "08.16.2022"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(self.name + " " + self.version)
        self.setWindowIcon(QIcon('assets/img/logo.png'))
        self.resize(1920, 1080)
        self.tabs = QTabWidget()
        # making document mode true
        self.tabs.setDocumentMode(True)
        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setTabShape(0)
        self.setCentralWidget(self.tabs)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(lambda i: self.setWindowTitle(self.tabs.tabText(i)))
        # self.tabs.currentChanged.connect(lambda i: self.setWindowTitle(self.tabs.tabText(i) + " - " + self.name))
        self.init_tab = BrowserTab(self)
        self.init_tab.browser.load(QUrl.fromLocalFile(os.path.abspath('assets/html/index.html')))
        self.add_new_tab(self.init_tab)

    def add_blank_tab(self):
        blank_tab = BrowserTab(self)
        self.add_new_tab(blank_tab)

    def add_new_tab(self, tab):
        i = self.tabs.addTab(tab, "")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabIcon(i,QIcon('assets/img/logo.png'))
        tab.back_button.triggered.connect(tab.browser.back)
        tab.next_button.triggered.connect(tab.browser.forward)
        tab.stop_button.triggered.connect(tab.browser.stop)
        tab.refresh_button.triggered.connect(tab.browser.reload)
        tab.home_button.triggered.connect(tab.navigate_to_home)
        tab.enter_button.triggered.connect(tab.navigate_to_url)
        tab.add_button.triggered.connect(self.add_blank_tab)
        tab.url_text_bar.returnPressed.connect(tab.navigate_to_url)
        tab.browser.urlChanged.connect(tab.renew_urlbar)
        tab.browser.loadProgress.connect(tab.renew_progress_bar)
        tab.browser.titleChanged.connect(lambda title: (self.tabs.setTabText(i, title),
        self.tabs.setTabToolTip(i, title),
        self.setWindowTitle(self.tabs.tabText(i))))
        # self.setWindowTitle(self.tabs.tabText(i) + " - " + self.name)))
        # tab.browser.iconChanged.connect(self.tabs.setTabIcon(i, tab.browser.icon()))

    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
 
        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_blank_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        page = self.tabs.widget(i)
        self.tabs.removeTab(i)
        page.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    # Ad Blocker Code
    # interceptor = setUrlRequestInterceptor()
    # QtWebEngineWidgets.QWebEngineProfile.defaultProfile().setUrlRequestInterceptor(interceptor)
    MainWindow = BrowserWindow()
    MainWindow.setStyleSheet("background-color:#ffffff")
    MainWindow.show()

    with open("assets\css\style.css", "r") as style:
        app.setStyleSheet(style.read())

    sys.exit(app.exec_())