#!/usr/bin/python
# -*- coding: utf-8 -*-

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


import sys
from ratingWidget import *

class Test(QMainWindow):
 
  def __init__(self):
 
    ''' Main Window '''
    QMainWindow.__init__(self)
    
    self.central = QWidget(self)
    self.mainLayout = QGridLayout()
    
    self.rp = RatingWidget(self.central)
    self.rp.setRating(5)
    self.rp.setMaxRating(5)
    self.rp.setEnabled(True)
    self.rp.setHalfStepsEnabled(False)

    self.central.setLayout(self.mainLayout)
    self.setCentralWidget(self.central)

    self.connect (self.rp, SIGNAL('ratingChanged(PyQt_PyObject)'), self.ratingChange)
    
  def ratingChange(self, rating):
    print "Rating changed to: %s" % rating

if __name__ == '__main__':
  app = QApplication(sys.argv)
  test = Test()
  test.show()
  sys.exit(app.exec_())
