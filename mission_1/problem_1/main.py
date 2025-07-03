try:
    with open('mission_computer_main.log', 'r') as file:
        content=file.read()
        print(content)
except FileNotFoundError:
    print('파일 찾을 수 없습니다.')
