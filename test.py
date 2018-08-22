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


class Object(QGraphicsItem):
    def __init__(self, fm, w, h):
        QGraphicsItem.__init__(self)
        self.fm = fm
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
        if fm.current == self:
            pen = QPen(Qt.red)
            pen.setStyle(Qt.DotLine)
            painter.setPen(pen)
            painter.drawLine(QLineF(-self.w / 2, 0, self.w / 2, 0))
            painter.drawLine(QLineF(0, -self.h / 2, 0, self.h / 2))

    def mousePressEvent( self, event ):
        self.cPos    = event.scenePos()
        self.pressedButton = event.button()
  
        if self.pressedButton == Qt.RightButton:
            cursorShape = Qt.SizeAllCursor
        else:
            cursorShape = Qt.ClosedHandCursor
        qApp.setOverrideCursor(QCursor(cursorShape))

        fm.Focus(self, str(self.scenePos().x()) + "," + str(self.scenePos().y()))
 
    def mouseReleaseEvent( self, event ):
        self.cPos    = None
        self.pressedButton = None
        qApp.restoreOverrideCursor()
        super(Object, self).mouseReleaseEvent( event )
        self.update()
        
    def mouseMoveEvent( self, event ):
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

        fm.Focus(self, str(self.scenePos().x()) + ", " + str(self.scenePos().y()))

class Rect(Object):
    def __init__(self, fm, w, h):
        Object.__init__(self, fm, w, h)

    def paint_sub(self, painter):
        painter.drawRect(-self.w / 2, -self.h / 2, self.w, self.h)

class Text(Object):
    def __init__(self, fm, text):
        self.text = text
        fm = QFontMetrics(QPainter().font())
        w = fm.width(self.text)
        h = fm.height()
        Object.__init__(self, fm, w, h)

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
        self.textbox.move(0, self.h)
        self.textbox.resize(self.w, 24)

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

node = Rect(fm, 200, 20)
node.setPos(50, 50)
widget.scene.addItem(node)

node = Rect(fm, 100, 60)
node.setPos(700, 140)
widget.scene.addItem(node)

node = Text(fm, "Fuga")
node.setPos(200, 140)
widget.scene.addItem(node)

node = Text(fm, "hoge")
node.setPos(700, 140)
widget.scene.addItem(node)

widget.out()
widget.show()



sys.exit(app.exec_())
