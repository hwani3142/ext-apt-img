import pandas as pd
from pandas import Series, DataFrame

data_path = "./datasource/raw_data_code.tsv"
simple_fields = ['시도', '시군구', '읍면', '동리', '법정동주소', '도로명주소', '세대수', '코드']

"""
raw-data
시도	시군구	읍면	동리	단지코드	단지명	단지분류	법정동주소	우편번호	도로명주소	분양형태	사용승인일	가입일	동수	세대수	분양세대수	임대세대수	복도유형	일반관리-관리방식	일반관리-인원	경비관리-관리방식	경비관리-인원	경비관리-계약업체	승강기(승객용)	승강기(화물용)	승강기(승객+화물)	승강기(장애인)	승강기(비상용)	승강기(기타)	총승강기	총주차대수	지상주차대수	지하주차대수	CCTV대수	홈네트워크	부대복리시설	최고층수	최고층수(건축물대장상)	지하층수	연면적	주거전용면적	전용면적	건축물대장연면적
경기도	용인처인구	남사읍	아곡리	A10023854	이편한세상용인파크카운티	연립주택	경기도 용인처인구 남사읍 아곡리 686 이편한세상용인파크카운티	17117	경기도 용인시 처인구 한숲로33번길 36	분양	20190628	20220420	8	75	75	0	계단식	위탁관리	3				12	0	10	2	0	0	24	115	1	114	83	유	관리사무소, 문고, 주민공동시설, 커뮤니티공간, 자전거보관소	4	4	1

raw-data with code
raw-data + [시도코드, 분류코드, 승인시기코드, 동수, 세대수, 복도유형코드, 주차유형코드, 코드]

여기에 학습돌린 컬럼이 추가되었다고 가정
"""

# tsv OR csv 파일 읽기
def read(path: str):
    data = pd.read_csv(path, delimiter='\t', keep_default_na=False)
    print(data.head())
    return data.loc[:]

# 각 row 에 대해 돌면서 작업 수행 (iteration)
def iter(data: DataFrame):
    for index, row in data.iterrows():
        if 4989 < index < 5000:
            print(index)
        # print(index) # row 중 N번째
        # print(row) # N-th row 값
        # print(row['코드']) # N-th row 의 코드 컬럼 값
        # DO SOMETHING MORE

# 각 row 마다 돌면서 컬럼 추가
def append_column(data: DataFrame):
    for index, row in data.iterrows():
        data.at[index, "신규컬럼"] = generate_column_value(row)

def generate_column_value(row: Series):
    return "(신규)" + row['코드']


# 특정 조건으로 row 를 필터링1 (시도 코드가 SE 인 데이터)
def filter_by_sido(data: DataFrame):
    return data.query("시도코드 == 'SE'")

# 특정 조건으로 row 를 필터링2 (1970년대, 아파트)
def filter_by_complex(data: DataFrame):
    return data.query("(승인시기코드 == '1h70' | 승인시기코드 == '2h70') & (분류코드 == 'APT')")


# 특정 조건으로 row 를 필터링3 (계단식 중 지하주차가 가능하고 최고층수가 20 이상 데이터)
def filter_by_complex_hard(data: DataFrame):
    return data.query("(복도유형코드 == 'S') & (주차유형코드 == 'GB' | 주차유형코드 == 'BL') & (최고층수 >= 20)")


# 특정 컬럼만 뽑아오기
# ex) columns = ['ID', '시도', '코드']
def select(data: DataFrame, columns: list):
    return data.filter(items=columns, axis=1)


# tsv 형태로 저장
def save_as_tsv(data: DataFrame, output_path: str, include_header: bool):
    data.to_csv(output_path, index=False, header=include_header, sep="\t")



def extract_by_class(result: dict):
    by_class = result['predictions'][0]['predictions']
    confidences = [0.0, 0.0, 0.0, 0.0] # Unlabeled, Square, Distributed, lattice 순서
    for i in range(0, 4):
        if by_class[i]['class_id'] == 0:
            confidences[0] = by_class[i]['confidence']
        elif by_class[i]['class_id'] == 1:
            confidences[1] = by_class[i]['confidence']
        elif by_class[i]['class_id'] == 2:
            confidences[2] = by_class[i]['confidence']
        elif by_class[i]['class_id'] == 3:
            confidences[3] = by_class[i]['confidence'].astype()
    return confidences

# dataframe.py 직접 실행 시 호출
if __name__ == "__main__":
    data: DataFrame = read(data_path)
    filtered = filter_by_complex_hard(data)
    iter(data)
    simple = select(filtered, ['ID', '시도', '승인시기코드', '분류코드', '복도유형코드', '최고층수', '코드'])
    # print(simple)
    save_as_tsv(simple, 'test.tsv', True)
