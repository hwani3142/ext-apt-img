import pandas as pd
from pandas import DataFrame

data_path = "./datasource/raw_data.tsv"
fields = ['시도', '시군구', '읍면', '동리', '법정동주소', '도로명주소']

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

def append_jibun_addr(data: DataFrame):
    multi_addr_count = 0
    data["법정동"] = "" # 동 OR 면 리 OR 면 OR 읍 리 OR 읍
    data["번지-1"] = "" # 123-456 에서 123
    data["번지-2"] = "" # 123-456 에서 456
    for index, row in data.iterrows():
        jibun_count: int = 0
        address: str = row['법정동주소']
        if "," in address:
            address = address.split(',')[0]
            # print(address)
            multi_addr_count += 1

        if len(row['시도']) > 0:
            jibun_count += 1

        if len(row['시군구']) > 0:
            jibun_count += 1

        if len(row['읍면']) > 0:
            jibun_count += 1

        if len(row['동리']) > 0:
            jibun_count += 1

        # 세종특별자치시 예외처리
        if jibun_count == 2:
            # print(f"two={row}")
            jibun_count += 1

        # 번지 추가
        bunji = address.split(" ")[jibun_count]
        if "-" in bunji:
            data.at[index, "번지-1"] = bunji.split("-")[0]
            data.at[index, "번지-2"] = bunji.split("-")[1]
            # row["번지-1"] = bunji.split("-")[0]
            # row["번지-2"] = bunji.split("-")[1]
        else:
            data.at[index, "번지-1"] = bunji

        # 시군구 예외처리
        # 1) 세종특별시 처리
        if row['시도'] == "세종특별자치시":
            data.at[index, "시군구"] = "세종특별자치시"
        # 2) 시 누락
        for sido in ["고양", "성남", "수원", "안산", "안양", "용인", "청주", "천안", "전주", "포항", "창원"] :
            if sido in row['시군구']:
                data.at[index, "시군구"] = sido + "시" + row['시군구'][2:]
                # print(f"시군구 - {data.at[index, '시군구']}")

        # 법정동 결합
        bjdong = []
        if len(row["읍면"]) > 0:
            bjdong.append(row["읍면"])

        if len(row["동리"]) > 0:
            bjdong.append(row["동리"])

        data.at[index, "법정동"] = " ".join(bjdong)
        # print(f"{data.at[index, '법정동']}")


    # print(data.loc[:, ['번지-1', '번지-2']])
    # print(f"total={multi_addr_count}")
    return data




if __name__ == "__main__":
    print("tf")
    data: DataFrame = read()
    append_jibun_addr(data)
