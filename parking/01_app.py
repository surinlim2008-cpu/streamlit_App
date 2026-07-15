import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --------------------------
# 페이지 설정
# --------------------------

st.set_page_config(
    page_title="🍰 주차를 열심히^^",
    page_icon="🍓",
    layout="wide"
)

# --------------------------
# CSS
# --------------------------

st.markdown("""
<style>

.stApp{

background:linear-gradient(
180deg,
#FFF8F8 0%,
#FFE8EF 40%,
#FFE2C7 80%,
#FFF7D6 100%);

}

/* 제목 */

.title{

text-align:center;
font-size:54px;
font-weight:800;
color:#ff5d8f;

text-shadow:
2px 2px white,
0px 0px 12px #ffc4d6;

}

.subtitle{

text-align:center;
font-size:20px;
color:#666;

}

/* 카드 */

.card{

background:white;
padding:25px;

border-radius:25px;

box-shadow:
0 10px 25px rgba(0,0,0,.12);

margin-bottom:18px;

transition:.3s;

}

.card:hover{

transform:translateY(-5px);

}

/* 업로드 */

[data-testid="stFileUploader"]{

background:white;

border:3px dashed #ffb6cf;

border-radius:20px;

padding:20px;

}

/* 검색창 */

.stTextInput input{

border-radius:15px;

border:2px solid #ffc2d8;

}

/* 버튼 */

.stButton button{

background:#ff7bac;

color:white;

border:none;

border-radius:15px;

font-size:18px;

padding:10px 20px;

}

.stButton button:hover{

background:#ff5d8f;

}

/* metric */

[data-testid="metric-container"]{

background:white;

border-radius:20px;

padding:15px;

box-shadow:0 5px 15px rgba(0,0,0,.08);

}

iframe{

border-radius:25px;

}

</style>

""",unsafe_allow_html=True)

# --------------------------
# 제목
# --------------------------

st.markdown("""

<div class="title">

🍰 주차 한입 💗

</div>

<div class="subtitle">

달콤하게 찾는 서울 공영주차장 🍓✨

</div>

""",unsafe_allow_html=True)

st.write("")

# --------------------------
# 업로드
# --------------------------

uploaded_file = st.file_uploader(

"🍓 서울시 공영주차장 CSV 업로드",

type=["csv"]

)

# --------------------------
# CSV
# --------------------------

if uploaded_file is not None:

    try:

        df = pd.read_csv(
            uploaded_file,
            encoding="cp949"
        )

    except:

        uploaded_file.seek(0)

        df = pd.read_csv(
            uploaded_file,
            encoding="utf-8"
        )

    st.success("🍰 업로드 완료!")

    df.columns=df.columns.str.strip()

    st.subheader("🍓 데이터 미리보기")

    st.dataframe(df.head())

    keyword=st.text_input(
        "🔎 주소 또는 주차장명을 검색하세요"
    )

    parking_col=None
    address_col=None
    lat_col=None
    lon_col=None

    for c in df.columns:

        if "주차장명" in c:
            parking_col=c

        if "주소" in c:
            address_col=c

        if "위도" in c:
            lat_col=c

        if "경도" in c:
            lon_col=c

    if parking_col is None:

        st.error("주차장명 컬럼을 찾지 못했습니다.")

        st.stop()

    if address_col is None:

        st.error("주소 컬럼을 찾지 못했습니다.")

        st.stop()

    # Part2에서 계속
    # --------------------------
    # 검색
    # --------------------------

    if keyword != "":

        result = df[
            df[parking_col].astype(str).str.contains(keyword, case=False, na=False)
            |
            df[address_col].astype(str).str.contains(keyword, case=False, na=False)
        ]

    else:

        result = df

    # --------------------------
    # 필요한 컬럼 자동 찾기
    # --------------------------

    phone_col = None
    capacity_col = None
    time_col = None
    type_col = None
    agency_col = None
    disabled_col = None

    for c in df.columns:

        if "전화" in c:
            phone_col = c

        if "주차가능" in c or "주차 가능" in c:
            capacity_col = c

        if "운영시간" in c:
            time_col = c

        if "노외" in c or "노상" in c or "주차장 구분" in c:
            type_col = c

        if "관리기관" in c or "운영기관" in c:
            agency_col = c

        if "장애인" in c:
            disabled_col = c

    # --------------------------
    # 통계
    # --------------------------

    st.write("")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🍓 검색 결과",
        len(result)
    )

    if capacity_col:

        cap = pd.to_numeric(
            result[capacity_col],
            errors="coerce"
        )

        c2.metric(
            "🚗 총 주차 가능 대수",
            f"{int(cap.sum()):,}대"
            if cap.notna().sum() else "-"
        )

        c3.metric(
            "🅿️ 평균 규모",
            f"{int(cap.mean()):,}대"
            if cap.notna().sum() else "-"
        )

    st.write("---")

    st.subheader("🍰 주차장 정보")

    if len(result) == 0:

        st.warning("검색 결과가 없습니다 😥")

    else:

        for _, row in result.iterrows():

            phone = row.get(phone_col, "-") if phone_col else "-"
            capacity = row.get(capacity_col, "-") if capacity_col else "-"
            opentime = row.get(time_col, "-") if time_col else "-"
            ptype = row.get(type_col, "-") if type_col else "-"
            agency = row.get(agency_col, "-") if agency_col else "-"
            disabled = row.get(disabled_col, "-") if disabled_col else "-"

            st.markdown(f"""
<div class="card">

<h2>🍓 {row[parking_col]}</h2>

📍 <b>주소</b><br>
{row[address_col]}<br><br>

📞 <b>전화번호</b><br>
{phone}<br><br>

🚗 <b>주차 가능 대수</b><br>
{capacity}<br><br>

🕒 <b>운영시간</b><br>
{opentime}<br><br>

🚙 <b>주차장 종류</b><br>
{ptype}<br><br>

🏢 <b>운영기관</b><br>
{agency}<br><br>

♿ <b>장애인 주차</b><br>
{disabled}

</div>
""", unsafe_allow_html=True)

    # --------------------------
    # 지도 데이터 준비
    # --------------------------

    if lat_col is None or lon_col is None:

        st.error("위도 또는 경도 컬럼이 없습니다.")
        st.stop()

    map_df = result.copy()

    map_df[lat_col] = pd.to_numeric(
        map_df[lat_col],
        errors="coerce"
    )

    map_df[lon_col] = pd.to_numeric(
        map_df[lon_col],
        errors="coerce"
    )

    map_df = map_df.dropna(
        subset=[lat_col, lon_col]
    )

    # Part3에서 계속
    # --------------------------
    # 지도
    # --------------------------

    if len(map_df) > 0:

        center = [
            map_df[lat_col].mean(),
            map_df[lon_col].mean()
        ]

        m = folium.Map(
            location=center,
            zoom_start=12,
            tiles="CartoDB Voyager"
        )

        for _, row in map_df.iterrows():

            phone = row.get(phone_col, "-") if phone_col else "-"
            capacity = row.get(capacity_col, "-") if capacity_col else "-"
            opentime = row.get(time_col, "-") if time_col else "-"
            ptype = row.get(type_col, "-") if type_col else "-"
            agency = row.get(agency_col, "-") if agency_col else "-"
            disabled = row.get(disabled_col, "-") if disabled_col else "-"

            popup = folium.Popup(f"""
            <div style="width:250px">

            <h3 style="color:#ff5d8f;">
            🍰 {row[parking_col]}
            </h3>

            <b>📍 주소</b><br>
            {row[address_col]}<br><br>

            <b>📞 전화번호</b><br>
            {phone}<br><br>

            <b>🚗 주차 가능 대수</b><br>
            {capacity}<br><br>

            <b>🕒 운영시간</b><br>
            {opentime}<br><br>

            <b>🚙 종류</b><br>
            {ptype}<br><br>

            <b>🏢 운영기관</b><br>
            {agency}<br><br>

            <b>♿ 장애인 주차</b><br>
            {disabled}

            </div>

            """, max_width=300)

            # 검색 결과는 빨간 마커
            color = "pink"

            if keyword != "":

                if keyword.lower() in str(row[parking_col]).lower() \
                or keyword.lower() in str(row[address_col]).lower():

                    color = "red"

            folium.Marker(

                location=[
                    row[lat_col],
                    row[lon_col]
                ],

                popup=popup,

                tooltip=f"🍓 {row[parking_col]}",

                icon=folium.Icon(
                    color=color,
                    icon="heart"
                )

            ).add_to(m)

        st.subheader("🗺️ 서울 공영주차장 지도")

        st_folium(
            m,
            width=None,
            height=650
        )

    else:

        st.warning("지도에 표시할 위치 정보가 없습니다.")

# --------------------------
# 푸터
# --------------------------

st.write("")
st.write("")

st.markdown("""
<hr>

<div style="
text-align:center;
font-size:28px;
font-weight:bold;
color:#ff5d8f;
">

🍰 주차 한입 💗

</div>

<div style="
text-align:center;
color:#777;
font-size:17px;
">

서울시 공영주차장을<br>
달콤하고 편하게 찾아보세요 🍓✨

</div>

<br>

""", unsafe_allow_html=True)
