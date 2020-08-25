from PySide import QtGui, QtCore
from PySide.QtGui import QPixmap, QMovie, QLabel
from PySide.QtCore import *
from FreeCAD import Base
import Part, Draft
import math, string
import time

def calcolo_arco_x(C, R, A, B):
    mid_point = C + 0.5 * math.sqrt((R + A - C) * (R + B - C)) + 0.5 * math.sqrt((R - A + C) * (R - B + C))
    print("Punto centrale: ", round(mid_point, 4))
    return round(mid_point, 4)

def calcolo_arco_y(C, R, A, B):
    mid_point = C + 0.5 * math.sqrt((R + A - C) * (R + B - C)) - 0.5 * math.sqrt((R - A + C) * (R - B + C))
    print("Punto centrale: ", round(mid_point, 4))
    return round(mid_point, 4)

class ExampleModalGuiClass(QtGui.QDialog):
    def __init__(self):
        super(ExampleModalGuiClass, self).__init__()
        self.initUI()
    def initUI(self):
        self.label1 = QtGui.QLabel(self)
        self.label1.setFixedWidth(250)
        self.label1.setText("DG-DM-SM-L-SC-LC-LM-T-ST-DF-SF")
        self.label1.move(70, 120)
        #
        self.label2 = QtGui.QLabel(self)
        self.label2.setText("")
        self.label2.setFixedWidth(240)
        self.label2.setStyleSheet("font-size: 15px; color: rgb(127,255,0);")
        self.label2.move(70, 90)
        #
        self.label = QtGui.QLabel(self)
        movie = QtGui.QMovie("C:/Users/Matheus/Desktop/tres.gif")
        self.label.setMovie(movie)
        movie.start()
        self.label.show()
        #self.label.move(230,180)
        self.label.move(120,150)
        #
        self.textInput = QtGui.QLineEdit(self)
        self.textInput.setText("")
        self.textInput.setFixedWidth(240)
        self.textInput.move(70, 150)
        #
        self.option1Button = QtGui.QPushButton("Generare", self)
        self.option1Button.setCheckable(True)
        #self.option1Button.isChecked.connect(self.onOption1)
        self.option1Button.move(150, 200)
        self.option2Button = QtGui.QPushButton("Annulare", self)
        self.option2Button.clicked.connect(self.onOption2)
        self.option2Button.move(150, 240)
        #
        self.label1.setStyleSheet("font-size: 15px; color: white;")
        self.textInput.setStyleSheet("font-size: 15px; background-color: white;")
        self.setStyleSheet("background-color: rgb(36,36,36);")
        self.option1Button.setStyleSheet("background-color: rgb(211,211,211);")
        self.option1Button.setIcon(QtGui.QIcon("C:/Users/Matheus/Desktop/ruotaAn.gif"))
        self.option1Button.setGeometry(QRect(150, 200, 80, 35))
        self.option2Button.setStyleSheet("background-color: rgb(211,211,211);")
        self.option2Button.setGeometry(QRect(150, 250, 80, 35))
        #
        self.setGeometry(250, 250, 400, 350)
        self.setWindowTitle("Impostazioni del disegno")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #
        self.show()
        self.seguire_input()
        self.onOption1()
        #
        self.label1.hide()
        self.label2.hide()
        self.textInput.hide()
        self.option1Button.hide()
        self.option2Button.hide()
        #
        self.bt_esportare = QtGui.QPushButton("Salvare PDF", self)
        self.bt_esportare.setGeometry(QRect(150,200, 90, 35))
        self.bt_esportare.setStyleSheet("background-color: rgb(211,211,211);")
        self.bt_esportare.clicked.connect(self.esportarepdf)

    def esportarepdf(self):
        doc_name = App.ActiveDocument.Name
        FreeCAD.addExportType(doc_name+"(*.pdf)", "Export_PDF")


    def seguire_input(self):
        while self.option1Button.isChecked() == False:
            txt = self.textInput.text()
            ct = txt.count('-')
            if ct == 0:
                self.label2.setText("Diametro Gomma")
            if ct == 1:
                self.label2.setText("Diametro Metallo")
            if ct == 2:
                self.label2.setText("Spessore Metallo")
            if ct == 3:
                self.label2.setText("Larghezza")
            if ct == 4:
                self.label2.setText("Sede cuscinetto")
            if ct == 5:
                self.label2.setText("Larghezza cuscinetto")
            if ct == 6:
                self.label2.setText("Larghezza mozzo")
            if ct == 7:
                self.label2.setText("Diametro tubo")
            if ct == 8:
                self.label2.setText("Spessore tubo")
            if ct == 9:
                self.label2.setText("Distanza flangia a filo")
            if ct == 10:
                self.label2.setText("Spessore flangia")
            QtGui.QApplication.processEvents()
            time.sleep(.001)
        return

    def onOption1(self):
        #
        # controlla se ce il numero giusto di numeri
        #
        txt_input = self.textInput.text()
        if txt_input.count('-') > 10:
            print("c'e un tratto in piu")
            return
        if txt_input.count('-') < 9:
            print("manca un tratto")
            return
        x = txt_input.split('-')
        i = 0
        for item in x:
            x[i] = float(x[i])
            i += 1
        doc_name = App.ActiveDocument.Name
        print("Diametro gomma = ", x[0])
        print("Diametro metallo = ", x[1])
        print("Spessore metallo = ", x[2])
        print("Larghezza = ", x[3])
        print("Sede cuscinetto = ", x[4])
        print("Larghezza cuscinetto = ", x[5])
        print("Larghezza mozzo = ", x[6])
        print("Diametro Tubo = ", x[7])
        print("Spessore Tubo = ", x[8])
        print("Distanza flangia a filo = ", x[9])
        print("Spessore flangia = ", x[10])
        x_minor_arc = calcolo_arco_x(2, 2.5, 2, 4.5)
        y_minor_arc = calcolo_arco_y(x[1] / 2 + 6.5, 2.5, x[1] / 2 + 4, x[1] / 2 + 6.5)
        #
        # costruisce il disegno
        #
        v1 = Base.Vector(0, 0, 0)
        v2 = Base.Vector(x[3], 0, 0)
        v3 = Base.Vector(0, x[1] / 2, 0)
        v4 = Base.Vector(x[3], x[1] / 2, 0)
        l1 = Part.LineSegment(v1, v2)
        l2 = Part.LineSegment(v1, v3)
        l3 = Part.LineSegment(v3, v4)
        l4 = Part.LineSegment(v4, v2)
        S1 = Part.Shape([l1, l2, l3, l4])
        Part.show(S1)
        v5 = Base.Vector(0, x[1] / 2 - x[2])
        v6 = Base.Vector(x[3], x[1] / 2 - x[2])
        l5 = Part.LineSegment(v5, v6)
        S2 = Part.Shape([l5])
        Part.show(S2)
        v7 = Base.Vector(0, x[7] / 2, 0)
        v8 = Base.Vector(x[3], x[7] / 2)
        v33 = Base.Vector(x[5], x[7] / 2 - x[8], 0)
        v34 = Base.Vector(x[6]-x[5], x[7] / 2 - x[8], 0)
        l16 = Part.LineSegment(v33,v34)
        l6 = Part.LineSegment(v7, v8)
        S3 = Part.Shape([l6, l16])
        Part.show(S3)
        v9 = Base.Vector(0, x[4] / 2, 0)
        v10 = Base.Vector(x[5], x[4] / 2, 0)
        v11 = Base.Vector(x[3] - x[5], x[4] / 2, 0)
        v12 = Base.Vector(x[3], x[4] / 2, 0)
        l7 = Part.LineSegment(v9, v10)
        l8 = Part.LineSegment(v11, v12)
        v13 = Base.Vector(x[5], 0, 0)
        v14 = Base.Vector(x[3] - x[5], 0, 0)
        l9 = Part.LineSegment(v10, v13)
        l10 = Part.LineSegment(v11, v14)
        S4 = Part.Shape([S3, l7, l8, l9, l10])
        Part.show(S4)
        v15 = Base.Vector(x[5], (x[7] - x[8]) / 2, 0)
        v16 = Base.Vector(x[3] - x[5], (x[7] - x[8]) / 2, 0)
        l11 = Part.LineSegment(v15, v16)
        S4 = Part.Shape([S4, l11])
        v25 = Base.Vector(0, x[1] / 2 + 4, 0)
        l14 = Part.LineSegment(v3, v25)
        v26 = Base.Vector(2, x[1] / 2 + 4, 0)
        l12 = Part.LineSegment(v25, v26)
        S4 = Part.Shape([S4, l12, l14])
        Part.show(S4)
        v27 = Base.Vector(x_minor_arc, y_minor_arc)
        v28 = Base.Vector(4.5, x[1] / 2 + 6.5)
        a1 = Part.Arc(v26, v27, v28)
        S5 = Part.Shape([S4, a1])
        Part.show(S5)
        v29 = Base.Vector(15, x[0] / 2, 0)
        v32 = Base.Vector(x[3]/2, x[0]/2, 0)
        l15 = Part.LineSegment(v29,v32)
        major_arc_x = calcolo_arco_y(15, 8, 7, 15)
        major_arc_y = calcolo_arco_x(x[0]/2 - 8, 8, x[0]/2 - 8, x[0]/2)
        v30 = Base.Vector(major_arc_x, major_arc_y, 0)
        v31 = Base.Vector(7, x[0]/2 - 8, 0)
        a2 = Part.Arc(v31,v30,v29)
        l13 = Part.LineSegment(v31,v28)
        S6 = Part.Shape([S5,a2,l13,l15])
        Part.show(S6)
        S7 = App.ActiveDocument.Shape004.Shape.mirror(Base.Vector(x[3]/2, 0, x[0] / 2), Base.Vector(1, 0, 0))
        S8 = App.ActiveDocument.Shape005.Shape.mirror(Base.Vector(x[3]/2, 0, x[0] / 2), Base.Vector(1, 0, 0))
        S9 = App.ActiveDocument.Shape006.Shape.mirror(Base.Vector(x[3]/2, 0, x[0] / 2), Base.Vector(1, 0, 0))
        S10 = Part.makeCompound([S7,S8,S9])
        Part.show(S10)
        v35 = Base.Vector(x[9], x[1]/2-x[2], 0)
        v36 = Base.Vector(x[9], x[7]/2, 0)
        v37 = Base.Vector(x[9]+x[10], x[1]/2-x[2], 0)
        v38 = Base.Vector(x[9]+x[10], x[7]/2, 0)
        l17 = Part.LineSegment(v35,v36)
        l18 = Part.LineSegment(v37,v38)
        S11 = Part.Shape([S10,l17,l18])
        Part.show(S11)
        S12 = App.ActiveDocument.Shape008.Shape.mirror(Base.Vector(x[3] / 2, 0, x[1]/2 - x[2]), Base.Vector(1, 0, 0))
        Part.Shape([S12])
        Part.show(S12)
        Gui.SendMsgToActiveView("ViewFit")
        #
        #construisce la pagina del disegno tecnico
        #
        page = FreeCAD.ActiveDocument.addObject('TechDraw::DrawPage', 'Page')
        FreeCAD.ActiveDocument.addObject('TechDraw::DrawSVGTemplate', 'Template')
        FreeCAD.ActiveDocument.Template.Template = "C:/Program Files/FreeCAD 0.18/data/Mod/TechDraw/Templates/A4_Landscape_ISO7200_Pep.svg"
        FreeCAD.ActiveDocument.Page.Template = FreeCAD.ActiveDocument.Template
        #
        # calcola la scala del disegno
        #
        scale = 0
        lista_scala = [0.1,0.2,0.25,0.3,0.4,0.5,0.6,0.75,0.8,1,2,2.5,3.0,3.5,4,4.5]
        for item in lista_scala:
            if ( 110 <= (x[0]/2)*item <= 120 ):
                scale = item
                print("Scale is:", scale)
                break
        FreeCAD.ActiveDocument.Page.Scale = scale
        #
        #aggiunge la vista alla pagina con le parti
        #
        page.ViewObject.show()
        view = FreeCAD.ActiveDocument.addObject('TechDraw::DrawViewPart', 'View')
        rc = page.addView(view)
        view.X = 150
        view.Y = (x[0]/2)*scale
        FreeCAD.ActiveDocument.View.Source = [
            App.getDocument(doc_name).getObject('Shape'), App.getDocument(doc_name).getObject('Shape001'),
            App.getDocument(doc_name).getObject('Shape002'), App.getDocument(doc_name).getObject('Shape003'),
            App.getDocument(doc_name).getObject('Shape004'), App.getDocument(doc_name).getObject('Shape005'),
            App.getDocument(doc_name).getObject('Shape006'), App.getDocument(doc_name).getObject('Shape007'),
            App.getDocument(doc_name).getObject('Shape008'),
            App.getDocument(doc_name).getObject('Shape009')]
        FreeCAD.ActiveDocument.View.Direction = (0.0, 0.0, 1.0)
        App.activeDocument().recompute()
        Gui.ActiveDocument.resetEdit()
        page.ViewObject.show()
        #
        #aggiunge le quote al disegno
        #
        dim1 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawViewDimension', 'Dimension')
        dim1.Y = ((x[0]/2)*scale)/2 + 10
        dim1.Type = "DistanceX"
        dim1.References2D = [(view, 'Edge2')]
        rc = page.addView(dim1)
        dim2 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawViewDimension', 'Dimension1')
        dim2.X = (((x[3]) * scale) / 2 - x[5]/2 +2) * -1
        dim2.Y = (((x[0]/2)*scale)/2 + 10)  * -1
        dim2.Type = "DistanceX"
        dim2.References2D = [(view, 'Edge7')]
        #dim2.Arbitrary = True
        #dim2.FormatSpec = str.join("Ø" + str(x[5]))
        rc = page.addView(dim2)
        dim3 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawViewDimension', 'Dimension1')
        dim3.Y = (x[4] / 2) * scale
        dim3.Type = "DistanceY"
        dim3.Arbitrary = True
        dim3.FormatSpec = "Ø" + str(x[4])
        dim3.References2D = [(view, 'Edge7')]

        super(ExampleModalGuiClass, self).close()
        #
        # permette di selezionare la faccia e fare il tratteggio
        #
        while True:
            try:
                face_selected = Gui.Selection.getSelectionEx(App.ActiveDocument.Name)[0].SubElementNames
                if "Face" in str(face_selected):
                    break
            except:
                pass
            QtGui.QApplication.processEvents()
            time.sleep(.001)
        hatch = FreeCAD.ActiveDocument.addObject('TechDraw::DrawGeomHatch', 'GeomHatch')
        hatch.Source = (view, str(face_selected).translate(str.maketrans('', '', string.punctuation)))
        hatch.FilePattern = "C:/Program Files/FreeCAD 0.18/data/Mod/TechDraw/PAT/FCPAT.pat"
        hatch.NamePattern = "Gomma"
        rc = page.addView(hatch)
        FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("GeomHatch").ColorPattern = (0.00, 0.00, 0.00)
        Gui.Selection.clearSelection()
        App.activeDocument().recompute()
        #seleziona la faccia
        while True:
            try:
                face_selected = Gui.Selection.getSelectionEx(App.ActiveDocument.Name)[0].SubElementNames
                if "Face" in str(face_selected):
                    break
            except:
                pass
            QtGui.QApplication.processEvents()
            time.sleep(.001)
        hatch2 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawGeomHatch', 'GeomHatch2')
        hatch2.Source = (view, str(face_selected).translate(str.maketrans('', '', string.punctuation)))
        hatch2.FilePattern = "C:/Program Files/FreeCAD 0.18/data/Mod/TechDraw/PAT/FCPAT.pat"
        hatch2.NamePattern = "Diagonal4"
        rc = page.addView(hatch2)
        FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("GeomHatch2").ColorPattern = (0.00, 0.00, 0.00)
        App.activeDocument().recompute()
        Gui.Selection.clearSelection()
        #seleziona la faccia
        while True:
            try:
                face_selected = Gui.Selection.getSelectionEx(App.ActiveDocument.Name)[0].SubElementNames
                if "Face" in str(face_selected):
                    break
            except:
                pass
            QtGui.QApplication.processEvents()
            time.sleep(.001)
        hatch3 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawGeomHatch', 'GeomHatch3')
        hatch3.Source = (view, str(face_selected).translate(str.maketrans('', '', string.punctuation)))
        hatch3.FilePattern = "C:/Program Files/FreeCAD 0.18/data/Mod/TechDraw/PAT/FCPAT.pat"
        hatch3.NamePattern = "Diagonal5"
        rc = page.addView(hatch3)
        FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("GeomHatch3").ColorPattern = (0.00, 0.00, 0.00)
        App.activeDocument().recompute()
        Gui.Selection.clearSelection()
        #seleziona la faccia
        while True:
            try:
                face_selected = Gui.Selection.getSelectionEx(App.ActiveDocument.Name)[0].SubElementNames
                if "Face" in str(face_selected):
                    break
            except:
                pass
            QtGui.QApplication.processEvents()
            time.sleep(.001)
        hatch4 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawGeomHatch', 'GeomHatch4')
        hatch4.Source = (view, str(face_selected).translate(str.maketrans('', '', string.punctuation)))
        hatch4.FilePattern = "C:/Program Files/FreeCAD 0.18/data/Mod/TechDraw/PAT/FCPAT.pat"
        hatch4.NamePattern = "Diagonal5"
        rc = page.addView(hatch4)
        FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("GeomHatch4").ColorPattern = (0.00, 0.00, 0.00)
        App.activeDocument().recompute()
        Gui.Selection.clearSelection()
        #seleziona la faccia
        while True:
            try:
                face_selected  = Gui.Selection.getSelectionEx(App.ActiveDocument.Name)[0].SubElementNames
                if "Face" in str(face_selected):
                    break
            except:
                pass
            QtGui.QApplication.processEvents()
            time.sleep(.001)
        hatch5 = FreeCAD.ActiveDocument.addObject('TechDraw::DrawGeomHatch', 'GeomHatch5')
        hatch5.Source = (view, str(face_selected).translate(str.maketrans('', '', string.punctuation)))
        hatch5.FilePattern = "C:/Program Files/FreeCAD 0.18/data/Mod/TechDraw/PAT/FCPAT.pat"
        hatch5.NamePattern = "Diagonal4"
        rc = page.addView(hatch5)
        FreeCADGui.getDocument(App.ActiveDocument.Name).getObject("GeomHatch5").ColorPattern = (0.00, 0.00, 0.00)
        App.activeDocument().recompute()
        page.ViewObject.show()

    def onOption2(self):
        self.close()

form = ExampleModalGuiClass()
form.exec_()
