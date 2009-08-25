#!/usr/bin/python
# -*- coding: utf-8 -*-

# File kratingwidget.cpp originally taken from the Nepomuk KDE project.
#
# Copyright (C) 2006-2007 Sebastian Trueg <trueg@kde.org> 
# Copyright (C) 2009 Carlos Gonçalves <mail@cgoncalves.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ratingPainter import RatingPainter

class RatingWidget(QFrame):

  def __init__(self, parent):
    QFrame.__init__(self, parent)
    self.rating = 0
    self.hoverRating = -1
    self.pixSize = 16
    self.ratingPainter = RatingPainter()

  def setPixmap(self, pix):
    self.setCustomPixmap(pix)
  
  def setCustomPixmap(self, pix):
    self.ratingPainter.setCustomPixmap(pix)
    self.update()
  
  def setIcon(self, icon):
    self.ratingPainter.setIcon(icon)
    self.update()
  
  def setPixmapSize(self, size):
    self.pixSize = size
    self.updateGeometry()
  
  def spacing(self):
    return self.ratingPainter.spacing
  
  def icon(self):
    return self.ratingPainter.icon()
  
  def setSpacing(self, s):
    self.ratingPainter.setSpacing(s)
    self.update()
  
  def alignment(self):
    return self.ratingPainter.alignment()
  
  def setAlignment(self, align):
    self.ratingPainter.setAlignment(align)
    self.update()
  
  def layoutDirection(self):
    return self.ratingPainter.layoutDirection()
  
  def setLayoutDirection(self, direction):
    self.ratingPainter.setLayoutDirection( direction )
    self.update()
  
  def rating(self):
    return self.rating
  
  def maxRating(self):
    return self.ratingPainter.maxinumRating()
    
  def halfStepsEnabled(self):
    return self.ratingPainter.halfStepsEnabled()
  
  def setRating(self, rating):
    self.rating = rating
    self.hoverRating = rating
    self.update()
  
  def setMaxRating(self, max):
		self.ratingPainter.setMaxRating(max)
		self.update()
  
  def setHalfStepsEnabled(self, enabled):
    self.ratingPainter.setHalfStepsEnabled( enabled )
    self.update()
  
  def setOnlyPaintFullSteps(self, fs):
    self.setHalfStepsEnabled(not fs)
  
  def mousePressEvent(self, e):
     if ( e.button() == Qt.LeftButton ):
        self.hoverRating = self.rating = self.ratingPainter.ratingFromPosition(self.contentsRect(), e.pos())
        self.update()
        self.emit(SIGNAL('ratingChanged(PyQt_PyObject)'), self.rating)
  
  def mouseMoveEvent(self, e):
    # when moving the mouse we show the user what the result of clicking will be
    self.hoverRating = self.ratingPainter.ratingFromPosition(self.contentsRect(), e.pos())
    if ( self.hoverRating >= 0 and e.buttons() & Qt.LeftButton):
      self.rating = self.hoverRating
      self.emit(SIGNAL('ratingChanged(PyQt_PyObject)'), self.rating)
    
    self.update();
  
  def leaveEvent(self, e):
      self.hoverRating = -1
      self.update()
  
  def paintEvent(self, e):
    QFrame.paintEvent(self, e)
    p = QPainter(self)
    self.ratingPainter.setEnabled(self.isEnabled())
    self.ratingPainter.paint(p, self.contentsRect(), self.rating, self.hoverRating)
  
  def sizeHint(self):
    numPix = self.ratingPainter.maxRating
    if (self.ratingPainter.halfStepsEnabled()):
        numPix /= 2
  
    pixSize = QSize(self.pixSize, self.pixSize )
    if (not self.ratingPainter.customPixmap.isNull()):
        pixSize = self.ratingPainter.customPixmap().size()
  
    return QSize( pixSize.width()*numPix + self.spacing()*(numPix-1) + self.frameWidth()*2, pixSize.height() + self.frameWidth()*2 )
  
  def resizeEvent(self, e ):
      QFrame.resizeEvent(self, e )

