from qgis.core import QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
import os

class RoundCoordinates(QObject):

    def __init__(self, iface: QgisInterface):
        super().__init__()
        self.iface = iface
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.action = QAction(QIcon(icon_path), "Round Coordinates", self.iface.mainWindow())
        self.action.triggered.connect(self.round_coordinates)

    def initGui(self):
        self.iface.addPluginToMenu("&Round Coordinates Plugin", self.action)
        self.iface.addToolBarIcon(self.action)

    def round_coordinates(self):
        layer = self.iface.activeLayer()
        if not isinstance(layer, QgsVectorLayer) or layer.geometryType() != QgsWkbTypes.LineGeometry:
            QMessageBox.warning(self.iface.mainWindow(), "Error", "Please select a polyline layer.")
            return

        features = layer.getFeatures()
        layer.startEditing()

        for feature in features:
            geom = feature.geometry()
            if geom.type() == QgsWkbTypes.LineGeometry:
                if geom.isMultipart():
                    coords = geom.asMultiPolyline()
                    rounded_coords = [[QgsPointXY(round(x), round(y)) for x, y in part] for part in coords]
                    rounded_geom = QgsGeometry.fromMultiPolylineXY(rounded_coords)
                else:
                    coords = geom.asPolyline()
                    rounded_coords = [QgsPointXY(round(x), round(y)) for x, y in coords]
                    rounded_geom = QgsGeometry.fromPolylineXY(rounded_coords)
                layer.changeGeometry(feature.id(), rounded_geom)

        layer.commitChanges()
        QMessageBox.information(self.iface.mainWindow(), "Success", "Coordinates have been rounded.")

    def unload(self):
        self.iface.removePluginMenu("&Round Coordinates Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

def classFactory(iface: QgisInterface):
    return RoundCoordinates(iface)
