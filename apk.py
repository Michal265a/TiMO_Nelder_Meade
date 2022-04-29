from window import *
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
	app = QApplication([])
	okno = GlowneOkno()
	app.exec()

