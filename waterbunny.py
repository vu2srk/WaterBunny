import sys
import urllib
from PyQt4 import QtCore, QtGui, QtWebKit

class waterbunny_tab(QtGui.QWidget):
    def __init__(self, index, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        
        self.parent = parent
        self.index = index
        
        self.contentWindow = QtWebKit.QWebView(self)
    
        self.connect(self.contentWindow, QtCore.SIGNAL("loadFinished (bool)"), self.pageLoaded)
        
        self.connect(self.contentWindow, QtCore.SIGNAL("loadStarted ()"), self.pageLoading)
        
        self.init_url = QtCore.QUrl("http://gmail.com")
        self.contentWindow.setUrl(self.init_url)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.contentWindow)

    def loadURL(self, url):
        self.init_url = QtCore.QUrl(url)
        self.contentWindow.setUrl(self.init_url)

    def pageLoading(self):
        self.parent.tabWidget.setTabText(self.index, "Loading...")
        self.parent.statusBar().showMessage("Page Loading...")
    
    def pageLoaded(self, flag):
        if flag:
            self.parent.tabWidget.setTabText(self.index, self.contentWindow.title())
        self.parent.statusBar().showMessage("Page Load Complete", 5000)

class waterbunny(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #call __init__ of the next in MRO (in this case QtGui.QMainWindow)
        super(QtGui.QMainWindow, self).__init__(parent)
        self.resize(600, 400)

        #central widget - the base class of all user interface objects. This one is a window of type QMainWindow (self)
        baseUIObject = QtGui.QWidget(self)

        #all other widgets are children of base widget
        self.toolbar = QtGui.QToolBar(baseUIObject)
        self.addressBar = QtGui.QLineEdit(baseUIObject)
        self.go = QtGui.QPushButton(baseUIObject)
        self.go.setText("Go")
        self.tabWidget = QtGui.QTabWidget(baseUIObject)

        self.tab = self.tabWidget.tabBar()
        self.tab.hide()
        self.openNewTab()

        #grid that lays out the widgets
        gridLayout = QtGui.QGridLayout(baseUIObject)
        gridLayout.addWidget(self.toolbar, 0, 0)
        gridLayout.addWidget(self.addressBar, 1, 0)
        gridLayout.addWidget(self.go, 1, 1)
        gridLayout.addWidget(self.tabWidget, 2, 0, 1, 2)

        self.setCentralWidget(baseUIObject)
        
        self.back = QtGui.QPushButton('Back')
        self.forward = QtGui.QPushButton('Forward')
        self.home = QtGui.QPushButton('Home')
        self.addTab = QtGui.QPushButton('Open New Tab')
        
        self.toolbar.addWidget(self.back)
        self.toolbar.addWidget(self.forward)
        self.toolbar.addWidget(self.home)
        self.toolbar.addWidget(self.addTab)

        statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(statusBar)

        self.connect(self.addTab, QtCore.SIGNAL('clicked()'), self.openNewTab) 
        self.connect(self.go, QtCore.SIGNAL('clicked()'), self.fetchURL)

    def openNewTab(self):
        i = self.tabWidget.count()
        newTab = waterbunny_tab(i, self)
        self.tabWidget.addTab(newTab, "New Tab")
        self.tabWidget.setCurrentWidget(newTab)
        if self.tabWidget.count() > 1:
            self.tab.show()

    def fetchURL(self):
        self.tabWidget.currentWidget().loadURL(self.addressBar.text())

if __name__ == "__main__":
    #initialize application object; here sys.argv = waterbunny.py
    app = QtGui.QApplication(sys.argv)
    
    #initialize browser
    browser = waterbunny()
    browser.show()

    sys.exit(app.exec_()) 

