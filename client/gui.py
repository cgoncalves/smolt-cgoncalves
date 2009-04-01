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
 
'''This file contains various GUI bits that need to be shared between
the firstboot GUI and the normal GUI.'''
 
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
 
from i18n import _
import smolt
 
class HostTable:
 
	def __init__(self, profile):
		self.profile = profile
		self.host_table = None
 
	def get(self):
		if self.host_table is None:
			self.host_table = QTreeView()
			self.host_table.setRootIsDecorated(False)
			self.host_table.setAlternatingRowColors(True)
			self.host_table.setSortingEnabled(True)
 
			model = QStandardItemModel(0, 2, self.host_table)
			model.setHeaderData(0, Qt.Horizontal, QVariant(_('Label')))
			model.setHeaderData(1, Qt.Horizontal, QVariant(_('Data')))
 
			for label, data in self.profile.hostIter():
				model.insertRow(0)
				label = QStandardItem(str(label))
				label.setEditable(False)
				data = QStandardItem(str(data))
				data.setEditable(False)
				model.setItem(0, 0, label)
				model.setItem(0, 1, data)
 
			self.host_table.setModel(model)
 
		return self.host_table
 
class DeviceTable:
 
	def __init__(self, profile):
		self.profile = profile
		self.device_table = None
 
	def get(self):
		if self.device_table is None:
			self.device_table = QTreeView()
			self.device_table.setRootIsDecorated(False)
			self.device_table.setAlternatingRowColors(True)
			self.device_table.setSortingEnabled(True)
 
			model = QStandardItemModel(0, 4, self.device_table)
			model.setHeaderData(0, Qt.Horizontal, QVariant(_('Bus')))
			model.setHeaderData(1, Qt.Horizontal, QVariant(_('Driver')))
			model.setHeaderData(2, Qt.Horizontal, QVariant(_('Type')))
			model.setHeaderData(3, Qt.Horizontal, QVariant(_('Description')))
 
			for VendorID, DeviceID, SubsysVendorID, SubsysDeviceID, Bus, Driver, Type, Description in self.profile.deviceIter():
				model.insertRow(0)
 
				bus = QStandardItem(str(Bus))
				bus.setEditable(False)
				driver = QStandardItem(str(Driver))
				driver.setEditable(False)
				type = QStandardItem(str(Type))
				type.setEditable(False)
				description = QStandardItem(str(Description))
				description.setEditable(False)
 
				model.setItem(0, 0, bus)
				model.setItem(0, 1, driver)
				model.setItem(0, 2, type)
				model.setItem(0, 3, description)
 
			self.device_table.setModel(model)
 
		return self.device_table

