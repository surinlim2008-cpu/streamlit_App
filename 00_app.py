import streamlit as st
import random

st.set_page_config(
    page_title="🎅 산타 선물 심사소",
    page_icon="🎄",
    layout="centered"
)

st.markdown("""
<style>
.stApp{
    background: linear-gradient(#dff6ff,#ffffff);
}
.big{
font-size:45px;
font-weight:bold;
text-align:center;
}
.small{
text-align:center;
font-size:20px;
}
.result{
padding:20px;
border-radius:20px;
background:#fff5f5;
font-size:24px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big'>🎅 산타 선물 심사소 🎄</div>", unsafe_allow_html=True)
st.markdown("<div class='small'>산타가 여러분의 편지를 읽고 간절함을 심사합니다.</div>", unsafe_allow_html=True)

st.divider()

wish = st.text_input("🎁 받고 싶은 선물")

letter = st.text_area(
"💌 산타할아버지께 편지를 써보세요",
height=180
)

score = st.slider(
"❤️ 얼마나 간절한가요?",
0,100,50
)

if st.button("🎄 산타에게 보내기"):

    if wish=="":
        st.warning("선물은 적어줘야지... 산타도 독심술은 없어.")
        st.stop()

    length=len(letter)

    bonus=0

    if length>300:
        bonus+=15
    elif length>150:
        bonus+=8

    emotional_words=[
        "제발","정말","간절","평생","착하게","사랑","울","소원",
        "꼭","부탁","감사","행복"
    ]

    for word in emotional_words:
        if word in letter:
            bonus+=3

    final=min(score+bonus,100)

    st.snow()

    st.markdown(f"## 🎅 산타의 간절함 분석 결과")
    st.progress(final)

    st.write(f"최종 간절함 : **{final}점**")

    terrible=[
        "벽돌 한 장 🧱",
        "돌멩이 컬렉션 🪨",
        "편의점 영수증 🧾",
        "반쯤 먹은 붕어빵 🐟",
        "양말 한 짝 🧦",
        "빈 택배상자 📦",
        "산타 싸인 종이 ✍️"
    ]

    okay=[
        "초코우유 🥛",
        "문화상품권 5천원 💳",
        "치킨 한 조각 🍗",
        "귤 한 박스 🍊",
        "붕어빵 3개 🐟",
        "핫팩 10개 🔥"
    ]

    good=[
        wish+" 🎁",
        "아이패드 ✨",
        "PS6(?) 🎮",
        "최신 게이밍 PC 💻",
        "용돈 100만원 💸",
        "닌텐도 스위치 🎮"
    ]

    legendary=[
        "🎁 "+wish,
        "🎅 산타 주식회사 VIP 회원권",
        "🦌 루돌프 택시 1년 이용권",
        "❄️ 크리스마스를 하루 더 늘릴 권리",
        "💎 다이아몬드 쿠폰",
        "🎄 산타의 비밀 선물 창고 입장권"
    ]

    if final<25:
        gift=random.choice(terrible)
        msg="🎅 음... 편지를 읽다가 산타가 졸아버렸단다."

    elif final<50:
        gift=random.choice(okay)
        msg="🎅 조금 더 진심을 담으면 좋겠구나."

    elif final<80:
        gift=random.choice(good)
        msg="🎅 오호! 꽤 간절하구나!"

    else:
        gift=random.choice(legendary)
        msg="🎅 감동받았다!! 루돌프도 울고 갔단다!!"

    st.markdown(f"""
<div class="result">

{msg}

<br><br>

🎁 <b>산타가 준비한 선물</b>

<h2>{gift}</h2>

</div>
""",unsafe_allow_html=True)

    st.balloons()
