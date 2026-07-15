import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="공영주차장 안내",
    page_icon="🅿️",
    layout="wide"
)

st.title("🅿️ 공영주차장 정보 안내")
st.write("CSV를 업로드하면 주소별 주차요금을 확인할 수 있습니다.")

uploaded_file = st.file_uploader(
    "공영주차장 CSV 업로드",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success("CSV 업로드 완료!")

    search = st.text_input("주소 검색")

    if search:

        result = df[df["주소"].str.contains(search, case=False, na=False)]

        if len(result)==0:
            st.warning("검색 결과가 없습니다.")

        else:

            st.subheader("검색 결과")

            st.dataframe(
                result[
                    ["주차장명","주소","기본요금","추가요금"]
                ],
                use_container_width=True
            )

    # 지도 중심

    center_lat = df["위도"].mean()
    center_lon = df["경도"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12
    )

    # 전체 마커

    for _, row in df.iterrows():

        popup = f"""
        <b>{row['주차장명']}</b><br>
        주소 : {row['주소']}<br>
        기본요금 : {row['기본요금']}<br>
        추가요금 : {row['추가요금']}
        """

        tooltip = f"{row['주소']}"

        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # 검색한 결과 빨간색 표시

    if uploaded_file and search:

        result = df[df["주소"].str.contains(search, case=False, na=False)]

        for _, row in result.iterrows():

            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=f"<b>{row['주차장명']}</b>",
                tooltip="검색 결과",
                icon=folium.Icon(color="red")
            ).add_to(m)

    st.subheader("📍 공영주차장 지도")

    st_folium(
        m,
        width=1200,
        height=600
    )
# ==========================
# 🌇 Sunset Theme CSS
# ==========================
st.markdown("""
<style>

/* 전체 배경 */
.stApp{
    background: linear-gradient(180deg,
    #FFF3E0 0%,
    #FFD8B1 25%,
    #FFB07C 55%,
    #FF8C69 80%,
    #B07CC6 100%);
    background-attachment: fixed;
}

/* 제목 */
h1{
    text-align:center;
    color:white;
    font-size:48px;
    text-shadow:2px 2px 10px rgba(0,0,0,0.25);
}

/* 소제목 */
h2,h3{
    color:white;
}

/* 설명글 */
p,label{
    color:#ffffff;
    font-size:16px;
}

/* 업로드 박스 */
[data-testid="stFileUploader"]{
    background:rgba(255,255,255,0.22);
    border:2px dashed rgba(255,255,255,0.7);
    border-radius:20px;
    padding:18px;
    backdrop-filter: blur(10px);
    box-shadow:0 8px 20px rgba(0,0,0,0.15);
}

/* 입력창 */
.stTextInput input{
    background:rgba(255,255,255,0.9);
    border-radius:12px;
    border:none;
    padding:10px;
}

/* 데이터프레임 */
[data-testid="stDataFrame"]{
    border-radius:18px;
    overflow:hidden;
    box-shadow:0 10px 25px rgba(0,0,0,0.18);
}

/* 버튼 */
.stButton>button{
    background:linear-gradient(90deg,#FF9966,#FF5E62);
    color:white;
    border:none;
    border-radius:14px;
    padding:0.6em 1.2em;
    font-weight:bold;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.05);
    box-shadow:0 8px 18px rgba(0,0,0,0.2);
}

/* 성공 메시지 */
.stSuccess{
    border-radius:15px;
}

/* 경고 */
.stWarning{
    border-radius:15px;
}

/* 메트릭 카드 */
[data-testid="metric-container"]{
    background:rgba(255,255,255,0.25);
    border-radius:20px;
    padding:18px;
    backdrop-filter:blur(10px);
    box-shadow:0 8px 18px rgba(0,0,0,0.15);
}

/* 사이드바 */
section[data-testid="stSidebar"]{
    background:rgba(255,255,255,0.18);
    backdrop-filter:blur(12px);
}

/* 지도 */
iframe{
    border-radius:20px;
    overflow:hidden;
    box-shadow:0 12px 30px rgba(0,0,0,0.2);
}

/* 스크롤바 */
::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#ff8c69;
    border-radius:20px;
}

::-webkit-scrollbar-track{
    background:#ffe6d5;
}

</style>
""", unsafe_allow_html=True)
