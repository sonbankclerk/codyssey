import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

class CalculatorLogic:
    """계산의 실제 로직을 담당하는 클래스"""
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Error"
        return a / b

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = CalculatorLogic()
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False
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
        self.display.setMaxLength(15)
        
        font = self.display.font()
        font.setPointSize(40)
        self.display.setFont(font)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                border: none;
                color: white;
                padding: 5px;
            }
        """)
        grid.addWidget(self.display, 0, 0, 1, 4)

        # 버튼 정의
        buttons = [
            ('AC', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3),
        ]

        # 버튼 생성 및 연결
        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(self.button_clicked)
            button.setStyleSheet(self.get_button_style(btn_text))
            font = button.font()
            font.setPointSize(20)
            button.setFont(font)
            if span:
                grid.addWidget(button, row, col, span[0], span[1])
            else:
                grid.addWidget(button, row, col)

        self.setWindowTitle('Calculator')
        self.setGeometry(300, 300, 400, 600)
        self.setStyleSheet("background-color: #333;")
        self.show()

    def get_button_style(self, text):
        """버튼 텍스트에 따라 다른 스타일을 반환하는 함수"""
        if text in ('/', '*', '-', '+', '='):
            return "QPushButton { background-color: #f1a33c; color: white; border-radius: 40px; } QPushButton:hover { background-color: #c88731; }"
        elif text in ('AC', '+/-', '%'):
            return "QPushButton { background-color: #a5a5a5; color: black; border-radius: 40px; } QPushButton:hover { background-color: #8c8c8c; }"
        else:
            return "QPushButton { background-color: #333333; color: white; border-radius: 40px; border: 1px solid #555; } QPushButton:hover { background-color: #555555; }"

    def button_clicked(self):
        """버튼 클릭 이벤트를 처리하는 메인 함수"""
        button = self.sender()
        key = button.text()
        current_text = self.display.text()

        if key in '0123456789':
            if self.waiting_for_operand or current_text == '0':
                self.display.setText(key)
                self.waiting_for_operand = False
            else:
                self.display.setText(current_text + key)
        elif key == '.':
            if '.' not in current_text:
                self.display.setText(current_text + '.')
        elif key == 'AC':
            self.reset()
        elif key == '+/-':
            self.negative_positive()
        elif key == '%':
            self.percent()
        elif key == '=':
            self.equal()
        elif key in ('/', '*', '-', '+'):
            self.handle_operator(key)

    def reset(self):
        self.display.setText('0')
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False

    def negative_positive(self):
        value = float(self.display.text())
        self.display.setText(str(-value))

    def percent(self):
        value = float(self.display.text())
        self.display.setText(str(value * 0.01))

    def handle_operator(self, op):
        if self.operator and not self.waiting_for_operand:
            self.equal()
        
        self.first_operand = float(self.display.text())
        self.operator = op
        self.waiting_for_operand = True

    def equal(self):
        if self.operator is None or self.first_operand is None:
            return

        second_operand = float(self.display.text())
        
        if self.operator == '+':
            result = self.logic.add(self.first_operand, second_operand)
        elif self.operator == '-':
            result = self.logic.subtract(self.first_operand, second_operand)
        elif self.operator == '*':
            result = self.logic.multiply(self.first_operand, second_operand)
        elif self.operator == '/':
            result = self.logic.divide(self.first_operand, second_operand)
        
        # 정수이면 .0을 제거하여 표시
        if isinstance(result, float) and result.is_integer():
            self.display.setText(str(int(result)))
        else:
            self.display.setText(str(result))
        
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec())
