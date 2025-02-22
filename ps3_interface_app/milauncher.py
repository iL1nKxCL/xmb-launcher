from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QFrame, QGridLayout, QVBoxLayout  # Se mantiene la importación de QVBoxLayout

import subprocess
import os

class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi Launcher")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Sin bordes
        self.setGeometry(0, 0, 1920, 1080)  # Tamaño de pantalla completa

        # Fondo con la imagen
        self.set_fondo_imagen()

        # Layout principal
        self.layout = QVBoxLayout(self)  # Usamos QVBoxLayout

        # Contenedor central cuadrado para las aplicaciones
        self.frame_apps = QFrame(self)
        self.frame_apps.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 20px; padding: 20px;")
        self.frame_apps_layout = QGridLayout()  # Crear un layout de cuadrícula
        self.frame_apps.setLayout(self.frame_apps_layout)  # Asignar el layout al QFrame
        self.layout.addWidget(self.frame_apps)

        # Botón de agregar aplicación en la esquina superior izquierda
        self.button_add_app = QPushButton("Agregar", self)
        self.button_add_app.setStyleSheet("background-color: #6c5ce7; color: white; font-size: 16px; border-radius: 10px; padding: 10px 20px;")
        self.button_add_app.clicked.connect(self.agregar_aplicacion)
        self.button_add_app.setGeometry(10, 10, 100, 40)  # Esquina superior izquierda

        # Botón de salir de pantalla completa en la esquina inferior derecha
        self.button_salir_pantalla_completa = QPushButton("Salir", self)
        self.button_salir_pantalla_completa.setStyleSheet("background-color: #e67e22; color: white; font-size: 16px; border-radius: 10px; padding: 10px 20px;")
        self.button_salir_pantalla_completa.clicked.connect(self.salir_pantalla_completa)
        self.button_salir_pantalla_completa.setGeometry(1710, 1040, 100, 40)  # Ajustado para ver el texto completo

        # Botón de cerrar en la esquina inferior derecha
        self.button_cerrar = QPushButton("Cerrar", self)
        self.button_cerrar.setStyleSheet("background-color: #e74c3c; color: white; font-size: 16px; border-radius: 10px; padding: 10px 20px;")
        self.button_cerrar.clicked.connect(self.close)
        self.button_cerrar.setGeometry(1710, 990, 100, 40)  # Esquina inferior derecha ajustada

        self.aplicaciones = []
        self.botones = []  # Lista para almacenar los botones de aplicaciones
        self.botones_enfocados = -1  # Indice del botón enfocado

    def set_fondo_imagen(self):
        # Cargar la imagen de fondo y asegurar que se ajuste al tamaño de la ventana
        imagen_fondo = QImage('fondo_emuladores_steam.jpg')  # Cambia la ruta si es necesario
        imagen_fondo = imagen_fondo.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(imagen_fondo))
        self.setPalette(palette)

    def agregar_aplicacion(self):
        # Abrir el diálogo para seleccionar un archivo
        ruta_aplicacion, _ = QFileDialog.getOpenFileName(self, "Seleccione la aplicación", "", "Archivos ejecutables (*.exe)")
        
        if ruta_aplicacion:
            self.aplicaciones.append(ruta_aplicacion)
            nombre_aplicacion = os.path.basename(ruta_aplicacion).split('.')[0].upper()
            self.agregar_boton_aplicacion(nombre_aplicacion, ruta_aplicacion)

    def agregar_boton_aplicacion(self, nombre_aplicacion, ruta_aplicacion):
        # Crear un botón cuadrado para la aplicación
        button_app = QPushButton(nombre_aplicacion, self)
        button_app.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-size: 14px;
            border-radius: 10px;
            padding: 10px;
            width: 120px;   # Establecer un tamaño cuadrado
            height: 120px;  # Establecer un tamaño cuadrado
            margin: 10px;
        """)
        button_app.clicked.connect(lambda: self.abrir_aplicacion(ruta_aplicacion))

        # Crear botón para quitar la aplicación
        button_remove_app = QPushButton("Quitar", self)
        button_remove_app.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            font-size: 12px;
            border-radius: 10px;
            padding: 10px;
            width: 80px;   # Establecer un tamaño cuadrado
            height: 80px;  # Establecer un tamaño cuadrado
            margin: 10px;
        """)
        button_remove_app.clicked.connect(lambda: self.quitar_aplicacion(ruta_aplicacion))

        # Añadir los botones al layout de cuadrícula
        row = len(self.aplicaciones) // 3  # Tres botones por fila
        column = len(self.aplicaciones) % 3  # Tres botones por fila
        self.frame_apps_layout.addWidget(button_app, row, column)
        self.frame_apps_layout.addWidget(button_remove_app, row, column + 1)  # Poner el botón de quitar al lado

        self.botones.append(button_app)  # Agregar botón de aplicación a la lista
        self.botones.append(button_remove_app)  # Agregar botón de quitar a la lista

    def abrir_aplicacion(self, ruta_aplicacion):
        # Ejecutar la aplicación
        subprocess.Popen(ruta_aplicacion)

    def quitar_aplicacion(self, ruta_aplicacion):
        # Eliminar la aplicación de la lista
        if ruta_aplicacion in self.aplicaciones:
            self.aplicaciones.remove(ruta_aplicacion)

        # Limpiar la lista de botones de la interfaz
        for widget in self.frame_apps.findChildren(QPushButton):
            widget.deleteLater()

        # Volver a agregar los botones restantes
        for app in self.aplicaciones:
            nombre_aplicacion = os.path.basename(app).split('.')[0].upper()
            self.agregar_boton_aplicacion(nombre_aplicacion, app)

    def salir_pantalla_completa(self):
        self.showNormal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            # Mover el enfoque hacia el botón anterior
            self.mover_enfoque(-1)
        elif event.key() == Qt.Key_Down:
            # Mover el enfoque hacia el botón siguiente
            self.mover_enfoque(1)
        elif event.key() == Qt.Key_Enter:
            # Ejecutar la aplicación o quitar
            self.ejecutar_o_quitar_aplicacion()
        elif event.key() == Qt.Key_Delete:
            # Eliminar la aplicación
            self.quitar_aplicacion_de_enfoque()

    def mover_enfoque(self, direccion):
        # Cambiar el enfoque entre los botones
        if self.botones_enfocados != -1:
            self.botones[self.botones_enfocados].setStyleSheet("""
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 10px;
                width: 120px;   
                height: 120px;
                margin: 10px;
            """)
        
        self.botones_enfocados += direccion
        if self.botones_enfocados >= len(self.botones):
            self.botones_enfocados = 0  # Volver al primer botón si llegamos al final
        elif self.botones_enfocados < 0:
            self.botones_enfocados = len(self.botones) - 1  # Volver al último botón si estamos al principio

        self.botones[self.botones_enfocados].setStyleSheet("""
            background-color: #3498db;
            color: white;
            font-size: 14px;
            border-radius: 10px;
            padding: 10px;
            width: 120px;   
            height: 120px;
            margin: 10px;
        """)  # Resaltar el botón enfocado

    def ejecutar_o_quitar_aplicacion(self):
        # Ejecutar o quitar la aplicación dependiendo de si es un botón de aplicación o de quitar
        if self.botones_enfocados % 2 == 0:  # Si el botón es de aplicación (están en posiciones pares)
            self.botones[self.botones_enfocados].click()
        else:
            self.botones[self.botones_enfocados].click()

    def quitar_aplicacion_de_enfoque(self):
        # Eliminar la aplicación que está actualmente enfocada
        if self.botones_enfocados % 2 != 0:  # Si es un botón de quitar
            self.botones[self.botones_enfocados].click()

    def run(self):
        self.showFullScreen()  # Iniciar en pantalla completa
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    launcher = Launcher()
    launcher.run()
    app.exec_()
