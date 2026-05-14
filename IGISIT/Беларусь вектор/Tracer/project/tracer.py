# -*- coding: utf-8 -*- 

import mapnik
import shapefile as sf
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import shapefile as sf
import transformer

class MapnikWidget(QWidget):

	def __init__(self, parent = None):
		self.replacements = {
			"ID": "Идентификатор",
			"CODE": "Классификационный код",
			"F9": "Собственное название",
			"AREA": "Область",
			"DISTRICT": "Район",
		}
	
	
		QWidget.__init__(self, parent)

		self.theMap = mapnik.Map(256, 256)
		self.loadedLayers = []
		self.layerIndex = 0
		self.tracedLayer = None
		self.traceLength = 0
		self.tracedObjectIndex = -1
		self.traceText = ""
		
		self.qim = QImage()
		self.startDragPos = QPoint()
		self.endDragPos   = QPoint()
		self.drag		 = False
		self.scale		= False
		self.timer		= QTimer()
		

		self.timer.timeout.connect(self.updateMap)
		
		self.zoomed = False
		self.unzoom = None

		self.total_scale = 1.0
		self.displayInfo = ""
		self.selectedFeature = None
		self.tracePolygon = True


	def open(self, xml):
		self.layerNames = ["areas", "districts", "towns", "hydro_l", "hydro_s"]
		self.xml = xml
		
		self.showLayerSettings()
		self.theMap = mapnik.Map(256, 256)
		mapnik.load_map(self.theMap, xml)
		
		self.traceMap = mapnik.Map(256, 256)
		mapnik.load_map(self.traceMap, xml)
		
		self.initMap()
		self.theMap.resize(self.width(), self.height())
		self.traceMap.resize(self.width(), self.height())
		self.zoom_all()
		

	def zoomTrace(self):
		if not self.zoomed:
			self.zoomed = True
			self.unzoom = self.theMap.envelope()
			self.traceMap.zoom_all()
			self.theMap.zoom_to_box(self.traceMap.envelope())
		else:
			self.zoomed = False
			self.theMap.zoom_to_box(self.unzoom)
			
		self.updateMap()
		
	def showLayerSettings(self):
		pass


	def close_map(self):
		self.theMap = mapnik.Map(256, 256)
		self.traceMap = mapnik.Map(256, 256)
		self.updateMap()

	def updateMap(self):
		self.timer.stop()
		self.total_scale = 1.0
		self.scale	   = False

		image = mapnik.Image(self.theMap.width, self.theMap.height)
		mapnik.render(self.theMap, image)
		
		self.traceMap.zoom_to_box(self.theMap.envelope())
		mapnik.render(self.traceMap, image)
		
		self.qim.loadFromData(QByteArray(image.tostring('png')))
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)

		if self.drag:
			painter.drawImage(self.endDragPos - self.startDragPos, self.qim)
		elif self.scale:
			qw = self.qim.width()
			qh = self.qim.height()
			newWidth = int(qw * self.total_scale)
			newHeight = int(qh * self.total_scale)
			newX = (qw - newWidth) / 2
			newY = (qh - newHeight) / 2
			painter.save()
			painter.translate(newX, newY)
			painter.scale(self.total_scale, self.total_scale)
			exposed = painter.matrix().inverted()[0].mapRect(self.rect()).adjusted(-1, -1, 1, 1)
			painter.drawImage(exposed, self.qim, exposed)
			painter.restore()
		else:
			painter.drawImage(0, 0, self.qim)

		if self.selectedFeature and not self.drag:
			env = self.selectedFeature.envelope()
			topLeft = mapnik.Coord(env.minx, env.maxy)
			bottomRight = mapnik.Coord(env.maxx, env.miny)
			topLeft = self.theMap.view_transform().forward(topLeft)
			bottomRight = self.theMap.view_transform().forward(bottomRight)
			painter.setPen(QColor(1, 0, 0, 100))
			painter.setBrush(QColor(0.2, 0.2, 0, 10))
			painter.drawRect(topLeft.x, topLeft.y, bottomRight.x - topLeft.x, bottomRight.y - topLeft.y)


		painter.setPen(QColor(0, 0, 0, 100))
		painter.setBrush(QColor(0, 0, 0, 100))
		painter.drawRect(0, 0, 256, 52)
		painter.setPen(QColor(0, 255 , 0))
		painter.drawText(10, 19, 'Scale Denominator: ' + str(self.theMap.scale_denominator()))
		painter.drawText(10, 38, 'Mouse at: ' + (self.displayInfo))

		if self.selectedFeature:
			attrs = self.selectedFeature.attributes

			startY = 80
			hei = 20
			painter.setPen(QColor(0, 0, 0, 100))
			painter.drawRect(0, startY, 256, hei * (len(attrs) + 1))
			painter.setPen(QColor(0, 255 , 0))
			cnt = 0
			for key in attrs:
				cnt += 1
				if not type(key) is unicode:
					key = str(key)
				val = attrs[key]
				if not type(val) is unicode:
					val = str(val)
				label = str(key) + ": " + val
				painter.drawText(10, startY + cnt * hei, label)

	def addLayer(self, layerName):
		if layerName == "trace" or layerName == "notrace":
			self.traceMap = mapnik.Map(256, 256)
			mapnik.load_map(self.traceMap, self.xml)
			self.traceMap.resize(self.width(), self.height())
			
		if layerName == "notrace":
			return
	
		# Here we instantiate our data layer, first by giving it a name and srs (proj4 projections string), and then by giving it a datasource.
		lyr = mapnik.Layer(layerName,"+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
		# Then provide the full filesystem path to a shapefile in WGS84 or EPSG 4326 projection without the .shp extension
		# A sample shapefile can be downloaded from http://mapnik-utils.googlecode.com/svn/data/world_borders.zip
		ds = mapnik.Shapefile(file = 'data/' + layerName)
		lyr.datasource = ds

		if layerName == "hydro_s":
			lyr.styles.append('region rivers style')
		elif layerName == "trace":
			if self.tracePolygon:
				lyr.styles.append('trace polygon style')	
			else:
				lyr.styles.append('trace line style')
		else:
			lyr.styles.append('basic style')

		if layerName != "trace":
			#theMap.layers.insert(lyr, len(theMap.layers) - 1)
			self.theMap.layers.append(lyr)
			self.loadedLayers.append(layerName)
		else:
			self.traceMap.layers.append(lyr)

		return lyr


	def addLayerHighLevel(self, layerName):
		result = None
		if not (layerName in self.loadedLayers):
			result = self.addLayer(layerName)

			if len(self.loadedLayers) == 1:
				self.zoom_all()

			print "loaded"
		self.updateMap()
		return result

	def traceLayer(self, tracedLayer):
		self.tracedLayer = tracedLayer
		print "Trace layer " + self.tracedLayer

		if tracedLayer == None:
			self.traceLength = 0
			self.tracedObjectIndex = -1
			self.addLayer("notrace")
			return
		
		shf = sf.Reader('data/' + tracedLayer)
		self.shapes = shf.shapes()
		self.records = shf.records()
		self.fields = shf.fields
		self.traceLength = len(self.shapes)
		self.tracedObjectIndex = 0
		self.traceCurrentObject()
		
	
	def generateCompleteInfo(self):
		shape = self.shapes[self.tracedObjectIndex]
		record = list(self.records[self.tracedObjectIndex])

		text = ""
		recordNum = -1
		for i in xrange(len(self.fields)):
			field = self.fields[i][0]
		
			recordNum += 1
			if field == "DeletionFlag":
				recordNum -= 1
				continue
		
			if recordNum >= len(record):
				break
			
			if field in self.replacements:
				field = self.replacements[field]
			
			recordText = record[recordNum]
			if field != "DeletionFlag" and recordText != "":
				line = field.decode("utf-8") + ": " + str(recordText).decode("utf-8")
				text += line+"\n"
		
		text += "\nКоличество точек".decode("utf-8") + ": " + str(len(shape.points)) + "\n"
		
		sk = "[[\n"
		wgs = "[[\n"
		
		for point in shape.points:
			sk += "[" + str(point[0]) + ", " + str(point[1]) + "]\n"
			point = transformer.transform(point)
			wgs += "[" + str(point[0]) + ", " + str(point[1]) + "]\n"
		
		sk += "]]\n"
		wgs += "]]\n"
		
		text += "\nКоординаты СК-42".decode("utf-8") + ": \n" + sk
		text += "\nКоординаты WGS84".decode("utf-8") + ": \n" + wgs
		
		return text
		
		

	def traceCurrentObject(self):
		if self.tracedObjectIndex < 0:
			self.tracedObjectIndex = 0
		elif self.tracedObjectIndex >= len(self.shapes):
			 self.tracedObjectIndex = len(self.shapes) - 1
		
		

		shape = self.shapes[self.tracedObjectIndex]
		record = list(self.records[self.tracedObjectIndex])

		text = ""
		recordNum = -1
		for i in xrange(len(self.fields)):
			field = self.fields[i][0]
		
			recordNum += 1
			if field == "DeletionFlag":
				recordNum -= 1
				continue
			
			
			if field in self.replacements:
				field = self.replacements[field]
			
			recordText = record[recordNum]
			if field != "DeletionFlag" and recordText != "":
				line = field.decode("utf-8") + ": " + str(recordText).decode("utf-8")
				text += line+"\n"
				
		text += "\nКоличество точек".decode("utf-8") + ": " + str(len(shape.points))
		
		
		self.tracePolygon = True
		
		self.traceText = text
		
		
		wr = sf.Writer(sf.POLYGON)
		wr.fields = list(self.fields)
		wr.fields.append(["selected", "C", 5, 0])
		record.append("1")

		wr.record(*record)
		
		wr.poly([shape.points])
		wr.save('data/trace')
		
		self.addLayer("trace")

		self.updateMap()



	def initMap(self):
		#self.addLayer("trace", theMap)

		mapNames = ["areas", "districts", "towns", "hydro_l", "hydro_s"]#, "intersections"]
		mapNames = []
		for mapName in mapNames:
			self.addLayer(mapName)


		#		self.selectionLayer = mapnik.Layer("selection","+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
		#		self.selectionLayer.datasource = mapnik.Shapefile(file = 'data/selection')
		#		self.selectionLayer.styles.append('basic style')
		#		theMap.layers.append(self.selectionLayer)

	def zoom_all(self):
		self.theMap.zoom_all()
		self.updateMap()

	def resizeEvent(self, event):
		self.theMap.resize(event.size().width(), event.size().height())
		self.traceMap.resize(event.size().width(), event.size().height())
		self.updateMap()

	def wheelEvent(self, event):
		self.scale = True
		scale_factor = 1.0 - event.delta() / (360.0 * 8.0) * 4
		self.theMap.zoom(scale_factor)
		self.traceMap.zoom(scale_factor)
		self.total_scale *= 1 / scale_factor
		self.update()
		self.timer.start(400)

	def traceObjectAt(self, index):
		self.tracedObjectIndex = index
		self.traceCurrentObject()
		return self.tracedObjectIndex
		
	def tracePrevious(self):
		self.tracedObjectIndex -= 1
		self.traceCurrentObject()
		return self.tracedObjectIndex
		
	def traceNext(self):
		self.tracedObjectIndex += 1
		self.traceCurrentObject()
		return self.tracedObjectIndex

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
			layerName = self.layerNames[self.layerIndex]
			self.layerIndex = (self.layerIndex + 1) % len(self.layerNames)
			print "Layer",layerName,self.loadedLayers
			print not (layerName in self.loadedLayers)
			self.addLayerHighLevel(layerName)
			print "layer"
		elif event.key() == Qt.Key_T:
			if len(self.loadedLayers) > 0:
				self.traceLayer(self.loadedLayers[-1])
		elif event.key() == Qt.Key_A:
			print "Prev object"
			if self.tracedLayer is None:
				if len(self.loadedLayers) > 0:
					self.traceLayer(self.loadedLayers[-1])
			else:
				self.tracePrevious()
		elif event.key() == Qt.Key_D:
			print "Next object"
			if self.tracedLayer is None:
				if len(self.loadedLayers) > 0:
					self.traceLayer(self.loadedLayers[-1])
			else:
				self.traceNext()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.startDragPos = event.pos()
			self.drag		 = True

	def mouseMoveEvent(self, event):
		if self.drag:
			self.endDragPos = event.pos()
			self.update()


	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.drag = False
			self.endDragPos = event.pos()

			cx = int(0.5 * self.theMap.width)
			cy = int(0.5 * self.theMap.height)
			dpos = self.endDragPos - self.startDragPos

			if dpos.x() != 0 and dpos.y() != 0:
				self.theMap.pan(cx - dpos.x() ,cy - dpos.y())
				self.zoomed = False
				self.updateMap()
			else:
				coord = self.theMap.view_transform().backward(mapnik.Coord(event.x(), event.y()))

				print "Quering map at (",coord.x,",",coord.y,")"
				totalLayers = len(self.theMap.layers)
				feature = None
				for backIndex in xrange(totalLayers):
					layerIndex = totalLayers - 1 - backIndex
					featureSet = self.theMap.query_point(layerIndex, coord.x, coord.y)
					if featureSet:
						for feature in featureSet.features:
							print 'layer',self.theMap.layers[layerIndex].name,":",feature.attributes["CODE"]
							break
						if feature:
							break
					else:
						print 'layer',layerIndex,":","Fail"

				self.selectedFeature = feature

				if feature:
					feature.attributes["selected"] = 1
					if "F9" in feature.attributes:
						self.displayInfo = feature.attributes["F9"]
					else:
						self.displayInfo = "N/A"
					self.updateMap()


import sys


class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		super(MainWindow, self).__init__(parent)



		mapnikWidget=MapnikWidget()
		mapnikWidget.open('styles.xml')
		mapnikWidget.show()

		#self.setCentralWidget(mapnikWidget)

		
class TraceWidget(QWidget):
	def __init__(self, parent = None, layers = [], mapnikWidget = None):
		QWidget.__init__(self, parent)
		
		self.mapnikWidget = mapnikWidget
		self.infoText = None

		layerBox = self.layerBox = QComboBox()
		layerBox.setEditable(False)
		layerBox.addItem("None")
		for layer in layers:
			layerBox.addItem(layer)
		
		self.backButton = backButton = QPushButton("<")		
		self.fwdButton = fwdButton = QPushButton(">")
		self.zoomButton = zoomButton = QPushButton("Zoom")
		
			
		self.numberLabel = numberLabel = QComboBox()
		numberLabel.setEditable(False)
		numberLabel.setMinimumWidth(80)
		#numberLabel.setAlignment(Qt.AlignCenter)
		
		self.connect(layerBox, SIGNAL('currentIndexChanged(QString)'), self.traceLayer)
		self.connect(numberLabel, SIGNAL('currentIndexChanged(int)'), self.traceObject)
		self.connect(fwdButton, SIGNAL('clicked()'), self.traceNext)
		self.connect(backButton, SIGNAL('clicked()'), self.tracePrevious)
		self.connect(zoomButton, SIGNAL('clicked()'), self.zoom)

		layout = QHBoxLayout()
		layout.addStretch(1)
		layout.addWidget(QLabel("Traced layer"))
		layout.addWidget(layerBox)
		layout.addWidget(backButton)
		layout.addWidget(numberLabel)
		layout.addWidget(fwdButton)
		layout.addWidget(zoomButton)
		self.setLayout(layout)
		self.updateButtons()
		
	def zoom(self):
		self.mapnikWidget.zoomTrace()
	
	def traceObject(self, index):
		self.mapnikWidget.traceObjectAt(index)
		self.updateButtons()
	
	def traceLayer(self, newTxt):
		self.numberLabel.clear()
		self.mapnikWidget.traceLayer(str(newTxt))
		for i in xrange(self.mapnikWidget.traceLength):
			self.numberLabel.addItem(str(i))
		self.updateButtons()
		
	def tracePrevious(self):
		self.mapnikWidget.tracePrevious()
		self.updateButtons()
		
	def traceNext(self):
		self.mapnikWidget.traceNext()
		
		self.updateButtons()
		
	def updateButtons(self):
		index = self.mapnikWidget.tracedObjectIndex
		lng = self.mapnikWidget.traceLength
		
		if lng <= 0:
			self.numberLabel.setCurrentIndex(-1)
		else:
			self.numberLabel.setCurrentIndex(index)
		
		self.backButton.setEnabled(index > 0)
		self.fwdButton.setEnabled(index < lng - 1)
		self.zoomButton.setEnabled(lng > 0)
		
		if self.infoText != None:
			self.infoText.setText(self.mapnikWidget.traceText)
			
	def showFullInfo(self):
		text = self.mapnikWidget.generateCompleteInfo()
		
		with open("info.txt", "w") as fw:
			fw.write(text.encode("cp1251"))
			fw.close()
		
		import os
		os.system("info.txt")
		
		
class LayersWidget(QWidget):
	def __init__(self, parent = None, layers = []):
		QWidget.__init__(self, parent)

		groupBox = QGroupBox("Map Layers")

		vbox = QVBoxLayout()
		for name in layers:
			checkBox=QCheckBox(name)
			self.connect(checkBox, SIGNAL('clicked()'), self.checkboxChanged)
			vbox.addWidget(checkBox)

		vbox.addStretch(1)

		groupBox.setLayout(vbox)

		layout = QVBoxLayout()
		layout.addWidget(groupBox)
		self.setLayout(layout)

		self.layerLink = {}
		self.mapnikWidget = None

	#		 setWindowTitle(tr("Group Boxes"));
#		 resize(480, 320);

	def checkboxChanged(self):
		sender = self.sender()
		layerName = str(sender.text())

		if not layerName in self.layerLink.keys():
			layer = self.mapnikWidget.addLayerHighLevel(layerName)
			if layer:
				self.layerLink[layerName] = layer
				sender.setEnabled(False)
		else:
			self.layerLink[layerName].visible = sender.isChecked()
			self.mapnikWidget.updateMap()



def getAvailableLayers():
	import dircache
	names = dircache.listdir("data")
	result = set()
	for i in xrange(len(names)):
		name = names[i][0:-4]
		if len(name) > 0 and name != "selection" and name != "trace":
			result.add(name)

	result = list(result)
	result.sort()
			
	return result


def main(args):
	app=QApplication(args)

	#win = MainWindow()
	#win.show()
	
	baseWidget=QWidget()
	
	mapnikWidget=MapnikWidget(baseWidget)
	mapnikWidget.open('styles.xml')

	layersWidget=LayersWidget(parent=None,layers=getAvailableLayers())
	layersWidget.mapnikWidget = mapnikWidget 
	
	traceWidget=TraceWidget(parent=None,layers=getAvailableLayers(),mapnikWidget=mapnikWidget)
	
	infoText=QTextEdit()
	
	traceWidget.infoText = infoText
	showButton = backButton = QPushButton("Full info")
	traceWidget.connect(showButton, SIGNAL('clicked()'), traceWidget.showFullInfo)
	
	vbox = QVBoxLayout()
	vbox.addWidget(infoText)
	vbox.addWidget(showButton)
		
	infoBox = QWidget()
	infoBox.setLayout(vbox)
	infoBox.setMaximumWidth(300)
	
	grid = QGridLayout()
	grid.addWidget(traceWidget,0,0,1,49)
	grid.addWidget(layersWidget,1,0,1,1)
	grid.addWidget(mapnikWidget,1,1,1,49)
	
	grid.addWidget(infoBox,0,50,2,1)
	
	
	baseWidget.setLayout(grid)
	baseWidget.showMaximized()

	sys.exit(app.exec_())

if __name__=="__main__":
	main(sys.argv)