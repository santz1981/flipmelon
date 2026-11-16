"""Standalone test of custom window frame (no ADB, scrcpy or RLottie)."""
import sys
from pathlib import Path
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel
from window_chrome import FlipmelonTitleBar, create_resize_grips, arrange_resize_grips
from i18n import set_language, tr, language

class Preview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.resize(1040, 740)
        self.setMinimumSize(940, 710)
        self.setWindowTitle('Flipmelon — Prévia da janela')
        shell=QWidget(self)
        shell.setStyleSheet('background:#0A0A0C; color:#F7F7F8;')
        layout=QVBoxLayout(shell)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.title_bar=FlipmelonTitleBar(self, Path(__file__).resolve().parent/'assets'/'flipmelon-icon.png', shell)
        layout.addWidget(self.title_bar)
        self.body=QLabel('')
        body=self.body
        self.change_language(language())
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setStyleSheet('font-size:18px; color:#F7F7F8;')
        layout.addWidget(body,1)
        self.setCentralWidget(shell)
        self._resize_grips=create_resize_grips(self)

    def change_language(self, code):
        set_language(code)
        self.title_bar.select_language(code)
        self.body.setText({'pt': 'Prévia do Flipmelon\n\nTeste mover, minimizar, maximizar e arrastar as bordas.',
                           'en': 'Flipmelon preview\n\nTry moving, minimizing, maximizing, and resizing.',
                           'ru': 'Предпросмотр Flipmelon\n\nПереместите, сверните, разверните или измените размер.',
                           'es': 'Vista previa de Flipmelon\n\nPrueba mover, minimizar, maximizar y cambiar el tamaño.',
                           'fr': 'Aperçu de Flipmelon\n\nEssayez de déplacer, réduire, agrandir et redimensionner.'}[code])

    def resizeEvent(self,event):
        super().resizeEvent(event)
        if hasattr(self,'_resize_grips'): arrange_resize_grips(self,self._resize_grips)

    def changeEvent(self,event):
        super().changeEvent(event)
        if event.type()==QEvent.Type.WindowStateChange:
            if hasattr(self,'_resize_grips'): arrange_resize_grips(self,self._resize_grips)
            if hasattr(self,'title_bar'): self.title_bar.maximize.update()

    def showEvent(self,event):
        super().showEvent(event)
        arrange_resize_grips(self,self._resize_grips)

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Preview()
    window.show()
    sys.exit(app.exec())
