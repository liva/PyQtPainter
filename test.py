#! usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *

class FocusManager:
    def __init__(self, gview):
        self.current = None
        self.textbox = gview.textbox

    def Focus(self, item, text):
        if self.current != None:
            self.current.update()
        self.current = item
        self.current.update()
        self.textbox.setText(text)

class OperationManager:
    def __init__(self, gview):
        self.move_button = gview.move_button
        self.resize_button = gview.resize_button
        self.rotate_button = gview.rotate_button
        self.move_button.toggled.connect(self.move_button_toggled)
        self.resize_button.toggled.connect(self.resize_button_toggled)
        self.rotate_button.toggled.connect(self.rotate_button_toggled)

    def move_button_toggled(self, checked):
        if checked:
            self.rotate_button.setChecked(False)
            self.resize_button.setChecked(False)

    def resize_button_toggled(self, checked):
        if checked:
            self.move_button.setChecked(False)
            self.rotate_button.setChecked(False)

    def rotate_button_toggled(self, checked):
        if checked:
            self.move_button.setChecked(False)
            self.resize_button.setChecked(False)
            
class Managers:
    def __init__(self, f, o):
        self.f = f
        self.o = o

class Object(QGraphicsItem):
    def __init__(self, m, w, h):
        QGraphicsItem.__init__(self)
        self.m = m
        self.w = w
        self.h = h
    
    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-self.w / 2 - penWidth / 2, -self.h / 2 - penWidth / 2,
                             self.w + penWidth, self.h + penWidth)

    def paint_sub(self, painter):
        pass
    
    def paint(self, painter, option, widget):
        self.paint_sub(painter)
        if self.m.f.current == self:
            pass
            #pen = QPen(Qt.red)
            #pen.setStyle(Qt.DotLine)
            #painter.setPen(pen)
            #painter.drawLine(QLineF(-self.w / 2, 0, self.w / 2, 0))
            #painter.drawLine(QLineF(0, -self.h / 2, 0, self.h / 2))

    def mousePressEvent( self, event ):
        self.cPos    = event.scenePos()

        self.m.f.Focus(self, str(self.scenePos().x()) + "," + str(self.scenePos().y()))
 
    def mouseReleaseEvent( self, event ):
        self.cPos    = None
        super(Object, self).mouseReleaseEvent( event )
        self.update()
        
    def mouseMoveEvent( self, event ):
        if self.m.o.move_button.isChecked():
            if not self.cPos:
                return

            # 描画位置を変更
            cur = event.scenePos()
            value = cur - self.cPos
            self.cPos = cur
            transform = self.transform()
            transform *= QTransform().translate( value.x(), value.y() )
 
            # 変更を適用
            self.setTransform(transform)

            self.m.f.Focus(self, str(self.scenePos().x()) + ", " + str(self.scenePos().y()))
        
class Rect(Object):
    def __init__(self, m, w, h):
        Object.__init__(self, m, w, h)

    def paint_sub(self, painter):
        painter.drawRect(-self.w / 2, -self.h / 2, self.w, self.h)

class Triangle(Object):
    def __init__(self, m, w, h):
        Object.__init__(self, m, w, h)

    def paint_sub(self, painter):
        painter.setBrush(Qt.SolidPattern)
        painter.drawPolygon([QPointF(self.w / 2, self.h / 2), QPointF(0, -self.h / 2), QPointF(-self.w / 2, self.h / 2)])

class Arrow(Object):
    def __init__(self, m, l):
        Object.__init__(self, m, 4, l)
        self.l = l

    def paint_sub(self, painter):
        painter.setBrush(Qt.SolidPattern)
        painter.drawPolygon([QPointF(2, -self.l / 2 + 8), QPointF(0, -self.l / 2), QPointF(-2, -self.l / 2 + 8)])
        painter.drawLine(QLineF(0, -self.l / 2, 0, self.l / 2))

class Text(Object):
    def __init__(self, m, text):
        self.text = text
        fm = QFontMetrics(QPainter().font())
        w = fm.width(self.text)
        h = fm.height()
        Object.__init__(self, m, w, h)

    def paint_sub(self, painter):
        painter.drawText(-self.w / 2, self.h / 2, self.text)

class graphicView(QGraphicsView):
 
    def __init__(self, w, h):
        QGraphicsView.__init__(self)

        self.w = w
        self.h = h
        
        self.scene = QGraphicsScene()

        self.setScene(self.scene)
      
        rect = QRect(0, 0, self.w, self.h + 24)

        self.scene.setSceneRect(rect)

        self.textbox = QLineEdit(self)
        self.textbox.move(150, self.h)
        self.textbox.resize(self.w-150, 24)

        self.move_button = QPushButton('M', self)
        self.move_button.move(0, self.h)
        self.move_button.resize(50, 24)
        self.move_button.setCheckable(True)

        self.resize_button = QPushButton('S', self)
        self.resize_button.move(50, self.h)
        self.resize_button.resize(50, 24)
        self.resize_button.setCheckable(True)

        self.rotate_button = QPushButton('R', self)
        self.rotate_button.move(100, self.h)
        self.rotate_button.resize(50, 24)
        self.rotate_button.setCheckable(True)

    def out(self):
        svg_gen = QSvgGenerator()
        svg_gen.setFileName("hello.svg")
        svg_gen.setSize(QSize(self.w, self.h))
        svg_gen.setViewBox(QRect(0, 0, self.w, self.h))
        svg_gen.setTitle("")
        svg_gen.setDescription("")
        
        painter = QPainter()
        painter.begin(svg_gen)

        self.scene.render(painter)

        painter.end()

app = QApplication(sys.argv)

widget = graphicView(800, 200)

fm = FocusManager(widget)

om = OperationManager(widget)

m = Managers(fm, om)

node = Rect(m, 200, 20)
node.setPos(50, 50)
widget.scene.addItem(node)

node = Rect(m, 100, 60)
node.setPos(700, 140)
widget.scene.addItem(node)

node = Triangle(m, 4, 8)
node.setPos(500, 140)
widget.scene.addItem(node)

node = Arrow(m, 100)
node.setPos(300, 100)
widget.scene.addItem(node)

node = Text(m, "Fuga")
node.setPos(200, 140)
widget.scene.addItem(node)

node = Text(m, "hoge")
node.setPos(700, 140)
widget.scene.addItem(node)

widget.out()
widget.show()



sys.exit(app.exec_())
