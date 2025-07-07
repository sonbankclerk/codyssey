import json

#dict to json 및 파일저장
def dict_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        print('파일 저장 완료')
        return True
    except Exception as e:
        print('파일 저장 실패')
        return False

try:
    with open('mission_computer_main.log', 'r') as file:
        #콤마를 기준으로 날짜 및 시간과 로그 내용을 분류
        content = file.read()
        part = content.splitlines()
        parsed = [line.split(',') for line in part]

        header = parsed[0]
        data = parsed[1:]
        
        # 리스트 객체를 시간의 역순으로 정렬(sort)
        data.sort(key=lambda x: x[0], reverse=True)

        # 리스트 객체를 사전(Dict) 객체로 전환
        dict_list = [dict(zip(header,row)) for row in data]

        for row in dict_list:
            print(row)

        dict_to_json(dict_list, 'mission_computer_main.json')

except FileNotFoundError:
    print('파일을 찾을 수 없다.')