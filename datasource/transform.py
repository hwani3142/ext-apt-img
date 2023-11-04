import pandas as pd

data_path = "./datasource/raw_data.tsv"
fields = ['법정동주소', '도로명주소']

"""
raw-data format
시도	시군구	읍면	동리	단지코드	단지명	단지분류	법정동주소	우편번호	도로명주소	분양형태	사용승인일	가입일	동수	세대수	분양세대수	임대세대수	복도유형	일반관리-관리방식	일반관리-인원	경비관리-관리방식	경비관리-인원	경비관리-계약업체	승강기(승객용)	승강기(화물용)	승강기(승객+화물)	승강기(장애인)	승강기(비상용)	승강기(기타)	총승강기	총주차대수	지상주차대수	지하주차대수	CCTV대수	홈네트워크	부대복리시설	최고층수	최고층수(건축물대장상)	지하층수	연면적	주거전용면적	전용면적	건축물대장연면적
경기도	용인처인구	남사읍	아곡리	A10023854	이편한세상용인파크카운티	연립주택	경기도 용인처인구 남사읍 아곡리 686 이편한세상용인파크카운티	17117	경기도 용인시 처인구 한숲로33번길 36	분양	20190628	20220420	8	75	75	0	계단식	위탁관리	3				12	0	10	2	0	0	24	115	1	114	83	유	관리사무소, 문고, 주민공동시설, 커뮤니티공간, 자전거보관소	4	4	1				
"""
def read():
    data = pd.read_csv(data_path, delimiter='\t', keep_default_na=False)
    print(data.head())
    # for index, row in data.iterrows():
    #     print(index, row['법정동주소'], "|", row['도로명주소'])
    # slice = data.loc[:, ['시도', '시군구']]  # 컬럼 슬라이싱
    # print(slice)
    return data.loc[:, fields]


if __name__ == "__main__":
    print("tf")
    read()
