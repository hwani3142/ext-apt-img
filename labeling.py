from pandas import Series, DataFrame
import datasource.transform as tf

output_fields = ['ID', '시도코드', '분류코드', '승인시기코드', '동수', '세대수', '복도유형코드', '주차유형코드', '최고층수']

def sido(row: Series):
    return {
        "서울특별시": "SE",
        "부산광역시": "BS",
        "대구광역시": "DG",
        "인천광역시": "IC",
        "광주광역시": "GJ",
        "대전광역시": "DJ",
        "울산광역시": "US",
        "세종특별자치시": "SJ",
        "경기도": "GG",
        "강원특별자치도": "GW",
        "충청북도": "CB",
        "충청남도": "CN",
        "전라북도": "JB",
        "전라남도": "JN",
        "경상북도": "GB",
        "경상남도": "GN",
        "제주특별자치도": "JJ"
    }.get(row['시도'], "nosido")

def classify(row: Series):
    return {
        "아파트": "APT",
        "연립주택": "tRH",
        "주상복합": "RCC",
        "도시형 생활주택(아파트)": "utA",
        "도시형 생활주택(연립주택)": "utB",
        "도시형 생활주택(주상복합)": "utC"
    }.get(row['단지분류'], "noclassify")

def period(row: Series):
    value = row['사용승인일'].__str__()
    code = "noperiod"
    if '19600101' <= value <= '19641231':
        code = '1h60'
    elif '19650101' <= value <= '19691231':
        code = '2h60'
    elif '19700101' <= value <= '19741231':
        code = '1h70'
    elif '19750101' <= value <= '19791231':
        code = '2h70'
    elif '19800101' <= value <= '19841231':
        code = '1h80'
    elif '19850101' <= value <= '19891231':
        code = '2h80'
    elif '19900101' <= value <= '19941231':
        code = '1h90'
    elif '19950101' <= value <= '19991231':
        code = '2h90'
    elif '20000101' <= value <= '20041231':
        code = '1h00'
    elif '20050101' <= value <= '20091231':
        code = '2h00'
    elif '20100101' <= value <= '20141231':
        code = '1h10'
    elif '20150101' <= value <= '20191231':
        code = '2h10'
    elif '20200101' <= value <= '20241231':
        code = '1h20'
    elif '20250101' <= value <= '20291231':
        code = '2h20'
    return code

def dong_count(row: Series):
    # if row['동수'] >= 100:
    #     print(f"detect {row['도로명주소']}")
    return "%03d" % row["동수"]

def house_count(row: Series):
    value = row['세대수']

    code = "nohouse"
    if 0 <= value <= 149:
        code = "1"
    elif 150 <= value <= 299:
        code = "2"
    elif 300 <= value <= 499:
        code = "3"
    elif 500 <= value <= 999:
        code = "4"
    elif 1000 <= value <= 1999:
        code = "5"
    elif 2000 <= value:
        code = "6"

    return code

def corridor(row: Series):
    value = row['복도유형']
    return {
        "계단식": "S",
        "복도식": "H",
        "타워형": "T",
        "혼합식": "M"
    }.get(value, "nocorridor")

def parking(row: Series):
    # print(f"-- {row['도로명주소']} {row['지상주차대수']}")
    gl_num = row['지상주차대수']
    bl_num = row['지하주차대수']
    if gl_num == "":
        gl_num = 0
    if bl_num == "":
        bl_num = 0

    if type(gl_num) == str:
        gl_num = gl_num.replace(".", "")
    if type(bl_num) == str:
        bl_num = bl_num.replace(".", "")

    gl = int(gl_num)
    bl = int(bl_num)

    code = "LL"
    if gl > 0 and bl > 0:
        code = "GB"
    elif gl > 0:
        code = "GL"
    elif bl > 0:
        code = "BL"
    return code

def summary(index, row: Series):
    return f"{index}_{row['시도코드']}_{row['분류코드']}_{row['승인시기코드']}_{row['동수']}_{row['세대수']}_{row['복도유형코드']}_{row['주차유형코드']}_{row['최고층수']}"

def append_label(data: DataFrame):
    try:
        # data["시도코드"] = ""
        # data["분류코드"] = ""
        # data["승인시기코드"] = ""
        # data["동수"] = ""
        # data["세대수"] = ""
        # data["복도유형코드"] = ""
        # data["주차유형코드"] = ""
        # data["코드"] = ""

        for index, row in data.iterrows():
            data.at[index, "시도코드"] = sido(row)
            data.at[index, "분류코드"] = classify(row)
            data.at[index, "승인시기코드"] = period(row)
            data.at[index, "동수"] = dong_count(row)
            data.at[index, "세대수"] = house_count(row)
            data.at[index, "복도유형코드"] = corridor(row)
            data.at[index, "주차유형코드"] = parking(row)

        for index, row in data.iterrows():
            data.at[index, "코드"] = summary(index, row)

        print(data['코드'])
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    print("labeling")
    data: DataFrame = tf.read()
    append_label(data)
    # data.to_csv('datasource/raw_data_code.tsv', index=False, header=True, sep="\t")
