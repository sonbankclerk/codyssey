# engineering_calculator.py
# PyQt6를 사용하여 아이폰 공학용 계산기와 유사한 UI와 기능을 구현하는 스크립트

import sys
import math
import random
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

class EngineeringCalculatorLogic:
    """공학용 계산의 실제 로직을 담당하는 클래스"""
    
    # 기본 사칙연산
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b):
        if b == 0: return "Error"
        return a / b

    # 단항 연산 함수들
    def square(self, a): return a ** 2
    def cube(self, a): return a ** 3
    def reciprocal(self, a): 
        if a == 0: return "Error"
        return 1 / a
    def factorial(self, a):
        if a < 0 or a != int(a): return "Error"
        return float(math.factorial(int(a)))

    # 삼각함수 (라디안/도 변환은 UI 클래스에서 처리)
    def sine(self, a): return math.sin(a)
    def cosine(self, a): return math.cos(a)
    def tangent(self, a): return math.tan(a)
    def sinh(self, a): return math.sinh(a)
    def cosh(self, a): return math.cosh(a)
    def tanh(self, a): return math.tanh(a)


class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = EngineeringCalculatorLogic()
        self.reset_state()
        self.initUI()

    def reset_state(self):
        """계산기 상태를 초기화하는 함수"""
        self.first_operand = None
        self.operator = None
        self.waiting_for_operand = False
        self.is_deg_mode = False # False: Rad, True: Deg

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(5)

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setMaxLength(20)
        
        font = self.display.font()
        font.setPointSize(40)
        self.display.setFont(font)
        self.display.setStyleSheet("QLineEdit { background-color: #1c1c1c; border: none; color: white; padding: 5px; }")
        grid.addWidget(self.display, 0, 0, 1, 10)

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

        self.buttons = {}
        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(self.button_clicked)
            button.setStyleSheet(self.get_button_style(btn_text))
            font = button.font()
            font.setPointSize(16)
            button.setFont(font)
            self.buttons[btn_text] = button
            if span:
                grid.addWidget(button, row, col, span[0], span[1])
            else:
                grid.addWidget(button, row, col)

        self.setWindowTitle('Engineering Calculator')
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("background-color: #1c1c1c;")
        self.show()

    def get_button_style(self, text):
        if text in ('÷', '×', '−', '+', '='): return "QPushButton { background-color: #f1a33c; color: white; border-radius: 25px; } QPushButton:hover { background-color: #c88731; }"
        elif text in '0123456789.': return "QPushButton { background-color: #505050; color: white; border-radius: 25px; } QPushButton:hover { background-color: #7c7c7c; }"
        elif text in ('C', '+/-', '%'): return "QPushButton { background-color: #d4d4d2; color: black; border-radius: 25px; } QPushButton:hover { background-color: #b5b5b3; }"
        else: return "QPushButton { background-color: #333333; color: white; border-radius: 25px; } QPushButton:hover { background-color: #555555; }"

    def button_clicked(self):
        button = self.sender()
        key = button.text()
        current_text = self.display.text()

        # 숫자 및 소수점 처리
        if key in '0123456789':
            if self.waiting_for_operand or current_text == '0':
                self.display.setText(key)
                self.waiting_for_operand = False
            else:
                self.display.setText(current_text + key)
        elif key == '.':
            if '.' not in current_text:
                self.display.setText(current_text + '.')
        
        # 상수 처리
        elif key == 'π': self.display.setText(str(math.pi))
        elif key == 'e': self.display.setText(str(math.e))
        elif key == 'Rand': self.display.setText(str(random.random()))

        # 초기화 및 기본 기능
        elif key == 'C': self.reset()
        elif key == '+/-': self.display.setText(str(float(current_text) * -1))
        elif key == '%': self.display.setText(str(float(current_text) * 0.01))

        # 단항 연산자 (결과를 바로 화면에 표시)
        elif key in ('x²', 'x³', '1/x', 'x!', 'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh'):
            self.handle_unary_operator(key)

        # 이항 연산자
        elif key in ('÷', '×', '−', '+', 'xʸ'):
            self.handle_binary_operator(key)
        
        elif key == '=': self.equal()
        
        # Rad/Deg 토글
        elif key in ('Rad', 'Deg'):
            self.toggle_rad_deg()

    def handle_unary_operator(self, op):
        try:
            value = float(self.display.text())
            
            # 삼각함수는 Rad/Deg 모드에 따라 변환
            if op in ('sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh') and self.is_deg_mode:
                value = math.radians(value)

            op_map = {
                'x²': self.logic.square, 'x³': self.logic.cube,
                '1/x': self.logic.reciprocal, 'x!': self.logic.factorial,
                'sin': self.logic.sine, 'cos': self.logic.cosine, 'tan': self.logic.tangent,
                'sinh': self.logic.sinh, 'cosh': self.logic.cosh, 'tanh': self.logic.tanh,
            }
            result = op_map[op](value)
            self.display_result(result)
        except (ValueError, OverflowError):
            self.display_result("Error")

    def handle_binary_operator(self, op):
        if self.operator and not self.waiting_for_operand:
            self.equal()
        
        self.first_operand = float(self.display.text())
        self.operator = op
        self.waiting_for_operand = True

    def equal(self):
        if self.operator is None or self.first_operand is None:
            return

        second_operand = float(self.display.text())
        op_map = {
            '+': self.logic.add, '−': self.logic.subtract,
            '×': self.logic.multiply, '÷': self.logic.divide,
            'xʸ': pow
        }
        result = op_map[self.operator](self.first_operand, second_operand)
        self.display_result(result)
        self.first_operand = result # 연속 계산을 위해 결과 저장
        self.operator = None
        self.waiting_for_operand = True

    def reset(self):
        self.display.setText('0')
        self.reset_state()

    def display_result(self, result):
        if isinstance(result, float) and result.is_integer():
            self.display.setText(str(int(result)))
        else:
            self.display.setText(str(result))

    def toggle_rad_deg(self):
        rad_button = self.buttons.get('Rad') or self.buttons.get('Deg')
        if not rad_button: return
        
        if self.is_deg_mode:
            self.is_deg_mode = False
            rad_button.setText('Rad')
        else:
            self.is_deg_mode = True
            rad_button.setText('Deg')
        
        # 버튼 딕셔너리 키 업데이트
        if 'Rad' in self.buttons and self.is_deg_mode:
            self.buttons['Deg'] = self.buttons.pop('Rad')
        elif 'Deg' in self.buttons and not self.is_deg_mode:
            self.buttons['Rad'] = self.buttons.pop('Deg')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculator()
    sys.exit(app.exec())
