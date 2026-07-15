import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🍰 달콤 주차장",
    page_icon="🍮",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        180deg,
        #FFF9F5 0%,
        #FFE5EC 35%,
        #FFD6A5 70%,
        #FFC6D9 100%);
}

/* 제목 */

.title{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#ff5c8d;
    text-shadow:2px 2px 8px white;
}

.subtitle{
    text-align:center;
    color:#666;
    font-size:18px;
}

/* 카드 */

.card{

    background:white;
    border-radius:25px;
    padding:20px;
    box-shadow:0px 10px 25px rgba(0,0,0,0.12);
    margin-bottom:20px;

}

/* 업로드 */

[data-testid="stFileUploader"]{

    background:white;
    border-radius:20px;
    padding:18px;
    border:3px dashed #ff9ec4;

}

/* 입력창 */

.stTextInput input{

    border-radius:15px;
    border:2px solid #ffb3d1;

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

    background:#ff4f91;

}

/* dataframe */

[data-testid="stDataFrame"]{

    border-radius:20px;

}

/* 성공메시지 */

.stSuccess{

    border-radius:15px;

}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------

st.markdown("""
<div class="title">
🍓✨ Sweet Parking ✨🍓
</div>

<div class="subtitle">
반짝반짝 공영주차장을 찾아보세요 🚗🍰
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------
# 업로드
# -----------------------------

uploaded_file = st.file_uploader(
    "🍓 서울시 공영주차장 CSV 업로드",
    type=["csv"]
)

# -----------------------------
# CSV 읽기
# -----------------------------

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")

    except:

        uploaded_file.seek(0)

        df = pd.read_csv(uploaded_file, encoding="utf-8")

    st.success("🍰 CSV 업로드 완료!")

    # -----------------------------
    # 컬럼 이름 공백 제거
    # -----------------------------

    df.columns = df.columns.str.strip()

    # -----------------------------
    # 컬럼 확인
    # -----------------------------

    st.write("### 🍭 데이터 미리보기")

    st.dataframe(df.head())

    st.write("")

    # -----------------------------
    # 검색창
    # -----------------------------

    keyword = st.text_input(
        "🔎 주소 또는 주차장명을 입력하세요"
    )

    # -----------------------------
    # 컬럼 자동 찾기
    # -----------------------------

    parking_col = None
    address_col = None
    lat_col = None
    lon_col = None

    for c in df.columns:

        if "주차장명" in c:
            parking_col = c

        if "주소" in c:
            address_col = c

        if "위도" in c:
            lat_col = c

        if "경도" in c:
            lon_col = c

    if parking_col is None or address_col is None:
        st.error("❌ CSV의 컬럼을 찾을 수 없습니다.")
        
        st.stop()
    # -----------------------------
    # 검색
    # -----------------------------

    if keyword != "":

        result = df[
            df[parking_col].astype(str).str.contains(keyword, case=False, na=False)
            |
            df[address_col].astype(str).str.contains(keyword, case=False, na=False)
        ]

    else:

        result = df

    st.write("")

    # -----------------------------
    # 통계
    # -----------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🍓 검색 결과",
        len(result)
    )

    fee_col = None

    for c in df.columns:

        if "기본" in c and "요금" in c:
            fee_col = c
            break

    if fee_col:

        fee = pd.to_numeric(
            result[fee_col],
            errors="coerce"
        )

        col2.metric(
            "🍰 평균 기본요금",
            f"{int(fee.mean()):,}원"
            if fee.notna().sum() else "-"
        )

        col3.metric(
            "🍭 최저 기본요금",
            f"{int(fee.min()):,}원"
            if fee.notna().sum() else "-"
        )

    st.write("---")

    # -----------------------------
    # 검색 결과 카드
    # -----------------------------

    if len(result)==0:

        st.warning("검색 결과가 없습니다 😥")

    else:

        st.subheader("🍩 검색 결과")

        for i,row in result.head(20).iterrows():

            parking_name = row.get(parking_col,"-")
            address = row.get(address_col,"-")

            base_fee = "-"

            base_time = "-"

            add_fee = "-"

            add_time = "-"

            tel = "-"

            for c in df.columns:

                if "기본" in c and "요금" in c:
                    base_fee=row[c]

                if "기본" in c and "시간" in c:
                    base_time=row[c]

                if "추가" in c and "요금" in c:
                    add_fee=row[c]

                if "추가" in c and "시간" in c:
                    add_time=row[c]

                if "전화" in c:
                    tel=row[c]

            st.markdown(f"""
            <div class="card">

            <h3>🍓 {parking_name}</h3>

            📍 <b>주소</b><br>
            {address}<br><br>

            💰 <b>기본요금</b><br>
            {base_fee} 원<br><br>

            ⏰ <b>기본시간</b><br>
            {base_time} 분<br><br>

            🍬 <b>추가요금</b><br>
            {add_fee} 원<br><br>

            ⌛ <b>추가시간</b><br>
            {add_time} 분<br><br>

            ☎️ {tel}

            </div>
            """,unsafe_allow_html=True)

    st.write("---")

    # -----------------------------
    # 위도·경도 확인
    # -----------------------------

    if lat_col is None or lon_col is None:

        st.error("위도 또는 경도 컬럼이 없습니다.")

    else:

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
            subset=[lat_col,lon_col]
        )

        # Part3에서 이어집니다.
        # -----------------------------
        # 지도 생성
        # -----------------------------

        if len(map_df) > 0:

            center_lat = map_df[lat_col].mean()
            center_lon = map_df[lon_col].mean()

            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=12,
                tiles="CartoDB Positron"
            )

            for _, row in map_df.iterrows():

                parking_name = row.get(parking_col, "-")
                address = row.get(address_col, "-")

                base_fee = "-"
                base_time = "-"
                add_fee = "-"
                add_time = "-"
                tel = "-"

                for c in df.columns:

                    if "기본" in c and "요금" in c:
                        base_fee = row[c]

                    if "기본" in c and "시간" in c:
                        base_time = row[c]

                    if "추가" in c and "요금" in c:
                        add_fee = row[c]

                    if "추가" in c and "시간" in c:
                        add_time = row[c]

                    if "전화" in c:
                        tel = row[c]

                popup = f"""
                <b>🍓 {parking_name}</b><br><br>

                📍 주소<br>
                {address}<br><br>

                💰 기본요금 : {base_fee}원<br>
                ⏰ 기본시간 : {base_time}분<br><br>

                🍬 추가요금 : {add_fee}원<br>
                ⌛ 추가시간 : {add_time}분<br><br>

                ☎️ {tel}
                """

                # 검색한 결과는 빨간색
                color = "pink"

                if keyword != "":

                    if keyword.lower() in str(parking_name).lower() \
                    or keyword.lower() in str(address).lower():

                        color = "red"

                folium.Marker(

                    location=[
                        row[lat_col],
                        row[lon_col]
                    ],

                    tooltip=f"🍰 {parking_name}",

                    popup=popup,

                    icon=folium.Icon(
                        color=color,
                        icon="heart"
                    )

                ).add_to(m)

            st.subheader("🗺️ 달콤 주차장 지도")

            st_folium(
                m,
                width=None,
                height=650
            )

        else:

            st.warning("지도에 표시할 위치 정보가 없습니다.")

    # -----------------------------
    # 푸터
    # -----------------------------

    st.write("")
    st.write("")

    st.markdown("""
    <hr>

    <div style="text-align:center;
                color:#ff5c8d;
                font-size:22px;
                font-weight:bold;">

    ✨🍰 Sweet Parking 🍰✨

    </div>

    <div style="text-align:center;
                color:gray;">

    서울시 공영주차장을 쉽고 귀엽게 찾아보세요 💕

    </div>

    <br>

    """, unsafe_allow_html=True)
