import sys
import os
from PyQt5.QtCore import QUrl, Qt, QStandardPaths
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout,
                             QWidget, QLineEdit, QToolBar, QPushButton, QLabel,
                             QFileDialog, QProgressBar, QStyleFactory)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.QtGui import QIcon, QPalette, QColor


class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://securemaps.pythonanywhere.com/"))

        self.browser.page().profile().downloadRequested.connect(parent.handle_download)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 8px 15px;
                background: #2d2d2d;
                color: #ffffff;
                selection-background-color: #4CAF50;
                font-size: 14px;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url_bar)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(self.url_bar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return

        if '.' in url and ' ' not in url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            self.browser.setUrl(QUrl(url))
        else:
            search_url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
            self.browser.setUrl(QUrl(search_url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecureMaps Browser")
        self.setWindowIcon(self.load_icon())
        self.resize(1200, 800)

        self.set_dark_theme()

        self.downloads = []
        self.current_download = None
        self.download_progress = QProgressBar()
        self.download_progress.setFixedWidth(200)
        self.download_progress.hide()

        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.style_tabs()

        self.toolbar = QToolBar("Navigation")
        self.toolbar.setMovable(False)
        self.setup_toolbar()

        self.statusBar().addPermanentWidget(self.download_progress)

        self.add_new_tab()
        self.setCentralWidget(self.tabs)

    def set_dark_theme(self):
        # Force dark style (works better for window frame on Windows)
        app.setStyle(QStyleFactory.create("Fusion"))

        # Dark palette for all widgets
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)

        # Additional styling for window frame
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QMainWindow::title {
                color: white;
                background-color: #2d2d2d;
            }
            QToolButton {
                color: white;
            }
        """)

    def load_icon(self):
        icon_path = "icon.png"
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon.fromTheme("web-browser")

    def style_tabs(self):
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background: #2d2d2d;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #444;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #4CAF50;
                border-color: #4CAF50;
            }
            QTabBar::tab:hover {
                background: #3d3d3d;
            }
        """)

    def setup_toolbar(self):
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: #2d2d2d;
                border: none;
                padding: 5px;
                spacing: 5px;
            }
        """)

        nav_actions = [
            ("Back", "←", self.navigate_back),
            ("Forward", "→", self.navigate_forward),
            ("Refresh", "⟳", self.refresh_page),
            ("Home", "⌂", self.go_home),
        ]

        for text, icon, callback in nav_actions:
            btn = QPushButton(icon)
            btn.setToolTip(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    padding: 5px;
                    font-size: 16px;
                    color: white;
                }
                QPushButton:hover {
                    background: #3d3d3d;
                    border-radius: 3px;
                }
            """)
            btn.clicked.connect(callback)
            self.toolbar.addWidget(btn)

        new_tab_btn = QPushButton("+ New Tab")
        new_tab_btn.setToolTip("New Tab")
        new_tab_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        new_tab_btn.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(new_tab_btn)

        self.addToolBar(self.toolbar)

    def handle_download(self, download: QWebEngineDownloadItem):
        download_dir = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)

        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", os.path.join(download_dir, download.suggestedFileName()))

        if path:
            download.setPath(path)
            download.accept()

            self.current_download = download
            self.download_progress.show()
            self.download_progress.setValue(0)

            download.downloadProgress.connect(self.update_download_progress)
            download.finished.connect(self.download_finished)

            self.downloads.append(download)

    def update_download_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            progress = int(100 * bytes_received / bytes_total)
            self.download_progress.setValue(progress)

    def download_finished(self):
        self.download_progress.hide()
        self.statusBar().showMessage("Download completed", 3000)
        self.current_download = None

    def add_new_tab(self, url=None):
        tab = BrowserTab(self)  # Pass self as parent for download handling
        if url:
            tab.navigate_to_url(url)

        index = self.tabs.addTab(tab, "New Tab")
        tab.browser.titleChanged.connect(
            lambda title, tab=tab: self.update_tab_title(tab, title))
        self.tabs.setCurrentIndex(index)
        tab.url_bar.setFocus()

    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title[:20] + (title[20:] and '...'))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_back(self):
        current_tab = self.current_browser()
        if current_tab:
            current_tab.browser.back()

    def navigate_forward(self):
        current_tab = self.current_browser()
        if current_tab:
            current_tab.browser.forward()

    def refresh_page(self):
        current_tab = self.current_browser()
        if current_tab:
            current_tab.browser.reload()

    def go_home(self):
        current_tab = self.current_browser()
        if current_tab:
            current_tab.browser.setUrl(QUrl("https://securemaps.pythonanywhere.com/"))

    def current_browser(self):
        current_widget = self.tabs.currentWidget()
        return current_widget if isinstance(current_widget, BrowserTab) else None


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Fusion"))

    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
