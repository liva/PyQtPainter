#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *

class graphicView(QGraphicsView):
 
    def __init__(self):
        QGraphicsView.__init__(self)
        
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-200, -200, 400, 400)

        self.setScene(self.scene)
      
    def sub(self):
        line = QLineF(0,0,100,100)
        node = QGraphicsLineItem(line)
 
        self.scene.addItem(node)

        rect = QRect(0, 0, 200, 80)

        self.scene.setSceneRect(rect)

        #self.scene.addRect(rect, QPen(Qt.transparent), QBrush(Qt.yellow))
        

    def set_text(self):
        text_item = self.scene.addText("Hello SVG", QFont("Arial", 30))
        #text_item.setPos(100, 200)
        text_item.setDefaultTextColor(Qt.blue)

    def set_rect(self):
        rect = QRect(10, 10, 100, 100)
        self.scene.addRect(rect, QPen(Qt.black), QBrush(Qt.transparent))

    def out(self):
        svg_gen = QSvgGenerator()
        svg_gen.setFileName("hello.svg")
        svg_gen.setSize(QSize(200, 80))
        svg_gen.setViewBox(QRect(0, 0, 200, 80))
        svg_gen.setTitle("hello svg")
        svg_gen.setDescription("this is sample svg.")
        
        painter = QPainter()
        painter.begin(svg_gen)

        self.scene.render(painter)

        painter.end()

app = QApplication(sys.argv)

widget = graphicView()
widget.set_text()
widget.sub()
widget.set_rect()
widget.out()
widget.show()

sys.exit(app.exec_())
