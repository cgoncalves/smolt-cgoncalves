#!/usr/bin/python
# -*- coding: utf-8 -*-

# File ratingpainter.cpp originally taken from the Nepomuk KDE project.
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

class RatingPainter:

  def __init__(self):
    self.maxRating = 10
    self.isEnabled = True
    self.bHalfSteps = True
    self.alignment = Qt.AlignCenter
    self.direction = Qt.LeftToRight
    self.spacing = 0
    self.customPixmap = QPixmap()
    self.icon = QIcon()
    
  def getPixmap(self, size):
    if (self.customPixmap.isNull() != True):
      return self.customPixmap.scaled(QSize(size, size))
    else:
      _icon = QIcon(self.icon)
      if (_icon.isNull()):
        _icon = QIcon("rating.png")
      return _icon.pixmap(size)

  def maxinumRating(self):
    return self.maxRating

  def halfStepsEnabled(self):
    return self.bHalfSteps

  def aligment(self):
    return self.aligment

  def layoutDirection(self):
    return self.direction

  def icon(self):
    return self.icon

  def isEnabled(self):
    return self.isEnabled

  def customPixmap(self):
    return self.customPixmap

#  def spacing(self):
#    return self.spacing

  def setMaxRating(self, max):
    self.maxRating = max

  def setHalfStepsEnabled(self, enabled):
    self.bHalfSteps = enabled

  def setAligment(self, align):
    self.aligment = align

  def setLayoutDirection(self, direction):
    self.direction = direction

  def setIcon(self, icon):
    self.icon = icon

  def setEnabled(self, enabled):
    self.isEnabled = enabled

  def setCustomPixmap(self, pixmap):
    self.customPixmap = pixmap

  def setSpacing(self, s):
    self.spacing = max(0, s)

  def paint(self, painter, rect, rating, hoverRating):
    if (rating > self.maxRating):
      rating = self.maxRating

    if (rating > self.maxRating):
      hoverRating = self.maxRating
    else:
      hoverRating = rating
    rating = min(rating, self.maxRating)
    hoverRating = min(hoverRating, self.maxRating)

    if (self.bHalfSteps):
      numUsedStars = self.maxRating / 2
    else:
      numUsedStars = self.maxRating

    if (hoverRating > 0 and hoverRating < rating):
      hoverRating, rating = rating, hoverRating

    usedSpacing = self.spacing

    ''' get the rating pixmaps '''
    maxHSizeOnePix = (rect.width() - (numUsedStars-1) * usedSpacing) / numUsedStars

    if (rect.height() > maxHSizeOnePix):
      tmp = maxHSizeOnePix
    else:
      tmp = rect.height()
    ratingPix = self.getPixmap( tmp )
    ratingPix = self.getPixmap( min(rect.height(), maxHSizeOnePix) )

    # FIXME does this really work as we want?
    disabledRatingPix = ratingPix.alphaChannel()

    # if we are disabled we become gray and more transparent
    if (self.isEnabled == False):
      ratingPix = disabledRatingPix
      disabledRatingPix.fill(Qt.transparent)

    half = self.bHalfSteps and rating%2
    
    if (self.bHalfSteps):
      numRatingStars = rating / 2
    else:
      numRatingStars = rating

    numHoverStars = 0
    halfHover = False

    if (hoverRating > 0 and rating != hoverRating and self.isEnabled):
      if (self.bHalfSteps):
        numHoverStars = hoverRating / 2
      else:
        numHoverStars = hoverRating
      halfHover = self.bHalfSteps and hoverRating%2
      # FIXME we don't want 1.0 gray, but 0.5
      hoverPix.alphaChannel()
    
    if (self.aligment == Qt.AlignJustify):
      w = rect.width()
      w -= numUsedStars * ratingPix.width()
      usedSpacing = w / (numUsedStars-1)

    ratingAreaWidth = ratingPix.width()*numUsedStars + usedSpacing*(numUsedStars-1)

    i = 0
    x = rect.x()

    if (self.aligment == Qt.AlignRight):
      x += ( rect.width() - ratingAreaWidth )
    elif (self.aligment == Qt.AlignHCenter):
      x += (rect.width() - ratingAreaWidth) / 2

    xInc = ratingPix.width() + usedSpacing
    if (self.direction == Qt.RightToLeft):
        x = rect.width() - ratingPix.width() - x
        xInc = -xInc

    y = rect.y()
    if (self.alignment == Qt.AlignVCenter ):
        y += (rect.height() / 2 - ratingPix.height() / 2)
    elif ( self.alignment == Qt.AlignBottom ):
        y += (rect.height() - ratingPix.height())
    
    for i in range(int(numRatingStars)):
      painter.drawPixmap( x, y, ratingPix )
      x += xInc

    if (half):

      if (self.direction == Qt.LeftToRight):
        tmp = ratingPix
      else:
        if (numHoverStars > 0):
          tmp = hoverPix
        else:
          tmp = disabledRatingPix
      
      painter.drawPixmap(x, y, ratingPix.width()/2, ratingPix.height(), \
          tmp, 0, 0, ratingPix.width()/2, ratingPix.height())

      if (self.direction == Qt.LeftToRight):
        if (numHoverStars > 0):
          tmp = hoverPix
        else:
          tmp = disabledRatingPix
      else:
        tmp = ratingPix

      painter.drawPixmap( x + ratingPix.width()/2, y, ratingPix.width()/2, ratingPix.height(), \
          tmp, ratingPix.width()/2, 0, ratingPix.width()/2, ratingPix.height() )

      x += xInc
      i += 1

    for i in range(numHoverStars):
      painter.drawPixmap(x, y, hoverPix)
      x += xInc

    if (halfHover):
      if (self.direction == Qt.LeftToRight):
        tmp = hoverPix
      else:
        tmp = disabledRatingPix

      painter.drawPixmap( x, y, ratingPix.width()/2, ratingPix.height(), \
          tmp, 0, 0, ratingPix.width()/2, ratingPix.height() )
 
      if (self.direction == Qt.LeftToRight):
        tmp = disabledRatingPix
      else:
        tmp = hoverPix

      painter.drawPixmap( x + ratingPix.width()/2, y, ratingPix.width()/2, ratingPix.height(), \
          tmp, ratingPix.width()/2, 0, ratingPix.width()/2, ratingPix.height() )
      
      x += xInc
      i += 1

    for i in range(numUsedStars):
      painter.drawPixmap(x, y, disabledRatingPix)
      x += xInc

  def ratingFromPosition(self, rect, pos):
    usedSpacing = self.spacing
    
    if(self.bHalfSteps):
      numUsedStars = self.maxRating/2
    else:
      numUsedStars = self.maxRating
  
    maxHSizeOnePix = ( rect.width() - (numUsedStars-1)*usedSpacing ) / numUsedStars

    if (rect.height() > maxHSizeOnePix):
      tmp = maxHSizeOnePix
    else:
      tmp = rect.height()
    ratingPix = self.getPixmap( tmp )
    ratingAreaWidth = ratingPix.width()*numUsedStars + usedSpacing*(numUsedStars-1)
  
    usedRect = QRect(rect)
  
    if (self.aligment == Qt.AlignRight):
      usedRect.setLeft(rect.right() - ratingAreaWidth)
    elif (self.aligment == Qt.AlignHCenter):
      x = (rect.width() - ratingAreaWidth) / 2
      usedRect.sefLeft(rect.left() + x)
      usedRect.setRight(rec.right() - x)
    else:
      usedRect.setRight(rect.left() + ratingAreaWidth - 1)
  
    if (self.aligment == Qt.AlignBottom):
      usedrect.setTop(rect.bottom() - ratingPix.height() + 1)
    elif (self.aligment == Qt.AlignVCenter):
      x = (rect.height() - ratingPix.height()) / 2
      usedRect.setTop(rect.top() + x)
      usedRect.setBottom(rect.bottom() - x)
    else:
      usedRect.setBottom( rect.top() + ratingPix.height() - 1 )
  
    if (usedRect.contains(pos)):
      x = 0
      if (self.direction == Qt.RightToLeft):
        x = usedRect.right() - pos.x()
      else:
        x = pos.x() - usedRect.left()
  
      one = float(float(usedRect.width()) / float(self.maxRating))
  
      return x / one + 0.5
    else:
     return -1
  
  def paintRating(self, painter, rect, align, rating, hoverRating):
    rp = RatingPainter()
    rp.setAlignment( align )
    rp.setLayoutDirection( painter,layoutDirection() )
    rp.paint( painter, rect, rating, hoverRating )
  
  def getRatingFromPosition(self, rect, align, direction, pos):
    rp = RatingPainter()
    rp.setAlignment( align )
    rp.setLayoutDirection( direction )
    return rp.ratingFromPosition( rect, pos )
  
