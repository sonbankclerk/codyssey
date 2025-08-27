# engineering_calculator.py
# PyQt6를 사용하여 아이폰 공학용 계산기와 유사한 UI를 만드는 스크립트

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 그리드 레이아웃 생성
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(5)

        # 계산기 디스플레이
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setMaxLength(20)
        
        font = self.display.font()
        font.setPointSize(40)
        self.display.setFont(font)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                border: none;
                color: white;
                padding: 5px;
            }
        """)
        # 디스플레이는 10개의 열을 모두 차지하도록 설정
        grid.addWidget(self.display, 0, 0, 1, 10)

        # 공학용 계산기 버튼 레이아웃 정의
        buttons = [
            ('(', 1, 0), (')', 1, 1), ('mc', 1, 2), ('m+', 1, 3), ('m-', 1, 4),
            ('mr', 1, 5), ('C', 1, 6), ('+/-', 1, 7), ('%', 1, 8), ('÷', 1, 9),
            
            ('2nd', 2, 0), ('x²', 2, 1), ('x³', 2, 2), ('xʸ', 2, 3), ('eˣ', 2, 4),
            ('10ˣ', 2, 5), ('7', 2, 6), ('8', 2, 7), ('9', 2, 8), ('×', 2, 9),

            ('1/x', 3, 0), ('√x', 3, 1), ('∛x', 3, 2), ('ʸ√x', 3, 3), ('ln', 3, 4),
            ('log₁₀', 3, 5), ('4', 3, 6), ('5', 3, 7), ('6', 3, 8), ('−', 3, 9),

            ('x!', 4, 0), ('sin', 4, 1), ('cos', 4, 2), ('tan', 4, 3), ('e', 4, 4),
            ('EE', 4, 5), ('1', 4, 6), ('2', 4, 7), ('3', 4, 8), ('+', 4, 9),

            ('Rad', 5, 0), ('sinh', 5, 1), ('cosh', 5, 2), ('tanh', 5, 3), ('π', 5, 4),
            ('Rand', 5, 5), ('0', 5, 6, 1, 2), ('.', 5, 8), ('=', 5, 9),
        ]

        # 반복문을 사용하여 버튼 생성 및 그리드에 추가
        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(self.button_clicked)
            button.setStyleSheet(self.get_button_style(btn_text))
            
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)
            
            if span:
                grid.addWidget(button, row, col, span[0], span[1])
            else:
                grid.addWidget(button, row, col)

        # 창 설정
        self.setWindowTitle('Engineering Calculator')
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("background-color: #1c1c1c;")
        self.show()

    def get_button_style(self, text):
        """버튼 텍스트에 따라 다른 스타일을 반환하는 함수"""
        if text in ('÷', '×', '−', '+', '='):
            return "QPushButton { background-color: #f1a33c; color: white; border-radius: 25px; } QPushButton:hover { background-color: #c88731; }"
        elif text in '0123456789.':
            return "QPushButton { background-color: #505050; color: white; border-radius: 25px; } QPushButton:hover { background-color: #7c7c7c; }"
        elif text in ('C', '+/-', '%'):
            return "QPushButton { background-color: #d4d4d2; color: black; border-radius: 25px; } QPushButton:hover { background-color: #b5b5b3; }"
        else: # 공학용 함수 버튼
            return "QPushButton { background-color: #333333; color: white; border-radius: 25px; } QPushButton:hover { background-color: #555555; }"

    def button_clicked(self):
        """버튼이 클릭되었을 때 호출되는 이벤트 처리 함수 (UI 기능만 구현)"""
        button = self.sender()
        key = button.text()
        current_text = self.display.text()

        if key == 'C':
            self.display.setText('0')
        elif key in '0123456789':
            if current_text == '0':
                self.display.setText(key)
            else:
                self.display.setText(current_text + key)
        # (이번 과제에서는 다른 버튼의 기능은 구현하지 않음)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculator()
    sys.exit(app.exec())
