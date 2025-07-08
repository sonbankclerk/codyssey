import csv

# 예외 처리
try:
    # CSV 파일 읽고, 출력(CSV|Comma Separated Values: 데이터를 쉼표로 구분하여 저장하는 텍스트 파일)
    # encoding='utf-8': 파일 출력시 깨짐 방지
    with open('Mars_Base_Inventory_list.csv', 'r', encoding='utf-8') as infile:
        #print([file.read()])
        reader = csv.reader(infile)
        header = next(reader)
        data = list(reader)

        # 인화성이 높은 순으로 정렬
        data.sort(key=lambda x:x[4], reverse=True)
        
        # 출력
        print(header)
        for row in data:
            print(row)

        # 인화성 0.7 이상 목록 출력
        fileter = [row for row in data if float(row[4])>=0.7]
        print(header)
        for row in fileter:
            print(row)

    # 인화성 0.7 이상 목록 CSV 포멧으로 저장
    # newline=''| Windows에서 빈 줄이 추가로 생기는 것을 방지
    # row, rows| row: 하나의 행 저장, rows: 여러 행 저장
    with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(fileter)
    print('csv 파일이 저장되었습니다.')
except FileNotFoundError:
    print('파일을 찾을 수 없다.')