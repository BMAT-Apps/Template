#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:25:40 2021

@author: ColinVDB
Template
"""


import sys
import os
from os.path import join as pjoin
from os.path import exists as pexists
# from dicom2bids import *
import logging
from PyQt5.QtCore import (QSize,
                          Qt,
                          QModelIndex,
                          QMutex,
                          QObject,
                          QThread,
                          pyqtSignal,
                          QRunnable,
                          QThreadPool,
                          QEvent)
from PyQt5.QtWidgets import (QDesktopWidget,
                             QApplication,
                             QWidget,
                             QPushButton,
                             QMainWindow,
                             QLabel,
                             QLineEdit,
                             QVBoxLayout,
                             QHBoxLayout,
                             QFileDialog,
                             QDialog,
                             QTreeView,
                             QFileSystemModel,
                             QGridLayout,
                             QPlainTextEdit,
                             QMessageBox,
                             QListWidget,
                             QTableWidget,
                             QTableWidgetItem,
                             QMenu,
                             QAction,
                             QTabWidget,
                             QCheckBox, 
                             QTextBrowser,
                             QToolBar)
from PyQt5.QtGui import (QFont,
                         QIcon)
import markdown



def launch(parent, add_info=None):
    """
    

    Parameters
    ----------
    parent : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    window = MainWindow(parent, add_info)
    window.show()



# =============================================================================
# MainWindow
# =============================================================================
class MainWindow(QMainWindow):
    """
    """
    

    def __init__(self, parent, add_info):
        """
        

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init__()
        self.parent = parent
        self.bids = self.parent.bids
        self.add_info = add_info

        self.setWindowTitle("Template")
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.center()
        
        # Create a toolbar and add it to the main window
        self.toolbar = QToolBar("Help?")
        self.addToolBar(self.toolbar)

        # Create a Help action and add it to the toolbar
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        self.toolbar.addAction(help_action)
        
        self.tab = TemplateTab(self)
        layout = QVBoxLayout()
        layout.addWidget(self.tab)

        self.window.setLayout(layout)


    def center(self):
        """
        

        Returns
        -------
        None.

        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
    def event(self, event):
        # Override the help button event
        if event.type() == QEvent.NonClientAreaMouseButtonPress:
            if self.windowFlags() & Qt.WindowContextHelpButtonHint:
                self.show_help()
                return True
        return super().event(event)

    def show_help(self):
        # Open the help window with the Markdown file
        markdown_path = pjoin(os.path.dirname(__file__), "..", "README.md")
        if pexists(markdown_path):
            self.help_window = HelpWindow(markdown_path)
            self.help_window.show()
        else:
            print('Readme not found')
        

class HelpWindow(QWidget):
    def __init__(self, markdown_file):
        super().__init__()
        self.setWindowTitle("Help")
        self.resize(600, 400)

        # Load and convert markdown to HTML
        with open(markdown_file, 'r') as file:
            markdown_content = file.read()
        html_content = markdown.markdown(markdown_content)

        # Setup QTextBrowser to display the HTML content
        self.text_browser = QTextBrowser()
        self.text_browser.setHtml(html_content)

        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        self.setLayout(layout)



# =============================================================================
# TemplateTab
# =============================================================================
class TemplateTab(QWidget):
    """
    """
    

    def __init__(self, parent):
        """
        

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init__()
        self.parent = parent
        self.bids = self.parent.bids
        self.setMinimumSize(500, 200)
        
        self.label = QLabel("This is a Template Pipeline")
        self.button = QPushButton("Pipeline Action")
        self.button.clicked.connect(self.action)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.setLayout(layout)


    def action(self):
        """
        

        Returns
        -------
        None.

        """
        self.thread = QThread()
        self.action = ActionWorker()
        self.action.moveToThread(self.thread)
        self.thread.started.connect(self.action.run)
        self.action.finished.connect(self.thread.quit)
        self.action.finished.connect(self.action.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        
        self.parent.hide()



# =============================================================================
# ActionWorker
# =============================================================================
class ActionWorker(QObject):
    """
    """
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    

    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        super().__init__()
        

    def run(self):
        """
        

        Returns
        -------
        None.

        """
        # Action
        print('Beginning of the action')
        print('End of the action')
        self.finished.emit()


