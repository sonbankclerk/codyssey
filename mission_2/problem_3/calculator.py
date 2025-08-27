import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 그리드 레이아웃 생성
        grid = QGridLayout()
        self.setLayout(grid)

        # 위젯 간의 간격을 0으로 설정하여 버튼들이 붙어있게 함
        grid.setSpacing(5)

        # 계산기 디스플레이 (결과가 표시되는 부분)
        self.display = QLineEdit('0')
        self.display.setReadOnly(True) # 읽기 전용으로 설정
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight) # 텍스트를 오른쪽 정렬
        self.display.setMaxLength(15) # 최대 15자리까지 표시
        
        # 디스플레이 스타일 설정
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
        
        # 디스플레이를 그리드의 첫 번째 행에 추가하고, 4개의 열을 차지하도록 설정
        grid.addWidget(self.display, 0, 0, 1, 4)

        # 버튼 이름과 위치를 리스트로 정의
        # (텍스트, 행, 열, 행병합, 열병합)
        buttons = [
            ('AC', 1, 0), ('+/-', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 1, 2), ('.', 5, 2), ('=', 5, 3),
        ]

        # 반복문을 사용하여 버튼 생성 및 그리드에 추가
        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(self.button_clicked) # 버튼 클릭 시 이벤트 처리 함수 연결
            button.setSizePolicy(
                button.sizePolicy().horizontalPolicy(),
                button.sizePolicy().verticalPolicy()
            )
            
            # 버튼 스타일 설정
            button.setStyleSheet(self.get_button_style(btn_text))
            
            font = button.font()
            font.setPointSize(20)
            button.setFont(font)

            if span:
                grid.addWidget(button, row, col, span[0], span[1])
            else:
                grid.addWidget(button, row, col)

        # 창 설정
        self.setWindowTitle('Calculator')
        self.setGeometry(300, 300, 400, 600)
        self.setStyleSheet("background-color: #333;")
        self.show()

    def get_button_style(self, text):
        """버튼 텍스트에 따라 다른 스타일을 반환하는 함수"""
        if text in ('/', '*', '-', '+', '='):
            return """
                QPushButton {
                    background-color: #f1a33c; color: white; border-radius: 40px;
                }
                QPushButton:hover { background-color: #c88731; }
            """
        elif text in ('AC', '+/-', '%'):
            return """
                QPushButton {
                    background-color: #a5a5a5; color: black; border-radius: 40px;
                }
                QPushButton:hover { background-color: #8c8c8c; }
            """
        else:
            return """
                QPushButton {
                    background-color: #333333; color: white; border-radius: 40px;
                    border: 1px solid #555;
                }
                QPushButton:hover { background-color: #555555; }
            """

    def button_clicked(self):
        """버튼이 클릭되었을 때 호출되는 이벤트 처리 함수"""
        button = self.sender()
        key = button.text()

        # 현재 디스플레이 텍스트 가져오기
        current_text = self.display.text()

        if key == 'AC':
            self.display.setText('0')
        elif key in '0123456789':
            if current_text == '0':
                self.display.setText(key)
            else:
                self.display.setText(current_text + key)
        # (추가 기능은 여기에 구현)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    sys.exit(app.exec())
