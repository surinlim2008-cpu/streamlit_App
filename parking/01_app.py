import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="공영주차장 안내",
    page_icon="🅿️",
    layout="wide"
)

# ==========================
# CSS
# ==========================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(180deg,#FFF4E6,#FFD6A5,#FFB4A2,#B583D6);
}

h1{
    color:white;
    text-align:center;
}

h3{
    color:white;
}

[data-testid="stFileUploader"]{
    background:rgba(255,255,255,0.3);
    border-radius:15px;
    padding:15px;
}

.stTextInput input{
    border-radius:12px;
}

iframe{
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

st.title("🌇 공영주차장 안내 서비스")

uploaded_file = st.file_uploader(
    "CSV 파일 업로드",
    type="csv"
)

if uploaded_file is not None:

    # CP949 / UTF8 모두 지원
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    st.success("CSV 업로드 완료!")

    keyword = st.text_input("주소 검색")

    if keyword != "":
        result = df[df["주소"].str.contains(keyword, na=False)]

        if len(result) == 0:
            st.warning("검색 결과가 없습니다.")

        else:

            st.subheader("검색 결과")

            st.dataframe(
                result[
                    ["주차장명","주소","기본요금","추가요금"]
                ],
                use_container_width=True
            )

    # 지도 생성

    m = folium.Map(
        location=[
            df["위도"].mean(),
            df["경도"].mean()
        ],
        zoom_start=12
    )

    for _, row in df.iterrows():

        popup = f"""
        <b>{row['주차장명']}</b><br>
        주소 : {row['주소']}<br>
        기본요금 : {row['기본요금']}<br>
        추가요금 : {row['추가요금']}
        """

        color = "blue"

        if keyword != "" and keyword.lower() in str(row["주소"]).lower():
            color = "red"

        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=popup,
            tooltip=row["주소"],
            icon=folium.Icon(color=color)
        ).add_to(m)

    st.subheader("🗺️ 공영주차장 지도")

    st_folium(
        m,
        width=1200,
        height=600
    )
