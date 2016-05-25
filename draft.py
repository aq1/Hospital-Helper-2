
'''
Python Syntax Highlighting Example

Copyright (C) 2009 Carson J. Q. Farmer

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public Licence as published by the Free Software
Foundation; either version 2 of the Licence, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more
details.

You should have received a copy of the GNU General Public Licence along with
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA  02110-1301, USA
'''

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyHighlighter(QSyntaxHighlighter):

    def __init__(self, parent, theme):
        QSyntaxHighlighter.__init__(self, parent)

        self.rules = []

        # keyword
        brush = QBrush(Qt.darkBlue, Qt.SolidPattern)
        self.keyword = QTextCharFormat()
        self.keyword.setForeground(brush)
        self.keyword.setFontWeight(QFont.Bold)
        keywords = QStringList(["break", "else", "for", "if", "in",
                                      "next", "repeat", "return", "switch",
                                      "try", "while"])

        for w in keywords:
            pattern = QRegExp(r"\{%s\}" % w)
            rule = HighlightingRule(pattern, self.keyword)
            self.rules.append(rule)

    def change_rules(self):
        self.rules = []
        for w in ('fuck', 'you'):
            pattern = QRegExp(r"\{%s\}" % w)
            rule = HighlightingRule(pattern, self.keyword)
            self.rules.append(rule)

    def highlightBlock(self, text):
        for rule in self.rules:
          expression = QRegExp(rule.pattern)
          index = expression.indexIn(text)
          while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, rule.format)
            index = text.indexOf(expression, index + length)
        self.setCurrentBlockState(0)


class HighlightingRule():
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format


class W(QWidget):

    def __init__(self):
        super(W, self).__init__()

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)
        editor = QTextEdit()
        editor.setFont(font)
        highlighter = MyHighlighter(editor, "Classic")
        vbox.addWidget(editor)
        b = QPushButton('change')
        b.clicked.connect(highlighter.change_rules)
        vbox.addWidget(b)



class TestApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setCentralWidget(W())
        self.setWindowTitle("Syntax Highlighter")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
