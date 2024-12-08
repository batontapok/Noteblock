import sys
import webbrowser
import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtWidgets import QMessageBox, QFontDialog, QColorDialog
from PyQt6.QtGui import QFont


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project1.ui', self)
        self.font = QFont('Consolas', 14)
        self.font_color = "black"
        self.bg_color = "white"
        self.mainfield.setCurrentFont(self.font)
        self.setWindowTitle('Noteblock')


        self.actionSave.triggered.connect(self.save_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionNewFile.triggered.connect(self.new_file)
        self.actionFont.triggered.connect(self.change_font)
        self.actionFontColor.triggered.connect(self.change_font_color)
        self.actionBackColor.triggered.connect(self.change_back_color)
        self.actionGitHub.triggered.connect(self.go_to_github)

        con = sqlite3.connect("noteblock_db.sqlite")
        self.con = con
        self.cur = con.cursor()


    def go_to_github(self):
        webbrowser.open('https://github.com/batontapok/Noteblock', new=2)

    def dialog_critical(self, s, t):                                                    #метод окна ошибки
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setWindowTitle(t)
        dlg.show()

    def open_file(self):                                                     #открывает существующий файл
        opng = QFileDialog.getOpenFileName(self, 'Выберите файл', '', 'Текстовые файлы (*.txt)')[0]
        self.setWindowTitle(f'{opng}')
        try:
            info = self.cur.execute(f"""SELECT * FROM files WHERE path='{opng}'""").fetchone()   #проверка на наличие
            if not info:                                                                         #записи о файле в БД
                self.cur.execute(f"""                                                                                           
                        INSERT INTO files (path) VALUES ('{opng}')""").fetchall()
                self.con.commit()
                self.con.close()
            with open(opng, 'r', encoding='utf-8') as f:
                 self.mainfield.setText(f.read())
        except:
            self.dialog_critical('Открытие отменено', 'Ошибка')
            self.setWindowTitle('Noteblock')

    def save_file(self):                                                        #сохраняет файл в указанное место
        file_name = 'Новый'
        inners = self.mainfield.toPlainText()
        file, _ = QFileDialog.getSaveFileName(self, 'Сохранить в...', file_name, 'Текстовые файлы (*.txt)')
        try:
             with open(file, 'w', encoding='utf-8') as f:
                f.write(str(inners))
        except Exception as e:
             self.dialog_critical('Сохранение отменено', 'Ошибка')

    def new_file(self):                                                       #очищает полотно для создания нового файла
        self.mainfield.clear()
        self.setWindowTitle('Новый')
        self.mainfield.setStyleSheet(f"color:black;")
        self.mainfield.setStyleSheet(f"background-color:white;")

    def change_font(self):                                                    #изменяет шрифт
        font, ok = QFontDialog.getFont()
        if ok:
            self.mainfield.setFont(font)

    def change_font_color(self):                                              #изменяет цвет шрифта
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color.name()
            self.mainfield.setStyleSheet(f"color:{self.font_color}; "
                                         f"background-color:{self.bg_color}")

    def change_back_color(self):                                              #изменяет цвет фона
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color.name()
            self.mainfield.setStyleSheet(f"color:{self.font_color}; "
                                         f"background-color:{self.bg_color};")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Notepad()
    ex.show()
    sys.exit(app.exec())