import streamlit as st
import random
import time

st.set_page_config(page_title="🎅 산타 선물 심사위원회", page_icon="🎄")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp{
    background:linear-gradient(#dff6ff,#ffffff);
}

.title{
    text-align:center;
    font-size:45px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:25px;
}

.result{
    background:#fff7e6;
    padding:20px;
    border-radius:18px;
    font-size:22px;
    border:3px dashed #ff4b4b;
}

.small{
    color:gray;
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- 제목 ----------------

st.markdown("<div class='title'>🎄 산타 선물 심사위원회 🎅</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>※ 산타, 루돌프, 엘프가 매우 공정(?)하게 심사합니다.</div>", unsafe_allow_html=True)

wish = st.text_input("🎁 받고 싶은 선물")

letter = st.text_area(
"💌 산타에게 편지를 써보세요",
height=180,
placeholder="산타 할아버지... 올해는 진짜..."
)

level = st.select_slider(
"🥺 얼마나 간절한가요?",
options=[
"🤏 있으면 좋겠다",
"🙂 조금 갖고 싶다",
"🥺 진짜 갖고 싶다",
"😭 제발...",
"💀 없으면 올해 못 산다"
]
)

if st.button("📮 루돌프에게 몰래 전달하기"):

    if wish == "":
        st.warning("🎅 받고 싶은 선물을 적어줘야 심사를 하지!")
        st.stop()

    progress = st.empty()

    steps = [
        "🧝 엘프가 편지를 펼치는 중...",
        "🦌 루돌프가 냄새 맡는 중...",
        "🎅 산타가 돋보기 찾는 중...",
        "📋 심사위원회 회의 중..."
    ]

    for s in steps:
        progress.info(s)
        time.sleep(1)

    progress.empty()

    st.subheader("📊 산타 AI 분석")

    sincerity=random.randint(0,100)
    crying=random.randint(0,100)
    acting=random.randint(60,100)
    trust=random.randint(0,40)

    st.progress(sincerity,text=f"🥺 진심도 {sincerity}%")
    st.progress(crying,text=f"😭 눈물 자국 {crying}%")
    st.progress(acting,text=f"🎭 오버액션 {acting}%")
    st.progress(trust,text=f"🤨 산타 신뢰도 {trust}%")

    st.divider()

    bad_gifts=[
        "🧦 오른쪽 양말",
        "🥔 감자",
        "🧅 양파 한 망",
        "🪨 그냥 돌",
        "📦 빈 택배상자",
        "🧻 휴지심",
        "🍞 식빵 테두리",
        "🥒 오이",
        "🐟 붕어빵 꼬리",
        "🥬 양배추",
        "🧱 벽돌",
        "🪥 칫솔 한 개",
        "🍠 고구마",
        "🥚 달걀 한 알",
        "🧃 빨대만 있는 음료수"
    ]

    good_gifts=[
        "🎁 "+wish,
        "🎮 닌텐도",
        "💻 게이밍 PC",
        "📱 최신 스마트폰",
        "💸 용돈 100만원"
    ]

    bad_comments=[
        "🎅 편지가 너무 짧아서 접는 데 2초 걸렸단다.",
        "🦌 루돌프가 읽다가 하품했어.",
        "🧝 엘프 회의 결과 '성의 부족'이래.",
        "🎅 작년 편지를 복붙한 거 아니니?",
        "🦌 간절하다면서 맞춤법은 왜 틀렸지?",
        "🎅 음... 나도 갖고 싶은데?",
        "🧝 GPT 쓴 거 아니야?",
        "🎅 올해는 경쟁률이 너무 높구나.",
        "🦌 솔직히 감동은 못 받았어."
    ]

    good_comments=[
        "🎅 오... 살짝 감동했단다.",
        "🦌 루돌프 눈에 눈물이 고였어!",
        "🧝 엘프들이 만장일치로 통과시켰어!",
        "🎅 그래! 올해는 특별히 들어주마!"
    ]

    chance=random.random()

    # 간절해도 대부분 꽝
    if level=="💀 없으면 올해 못 산다":
        success=0.15
    elif level=="😭 제발...":
        success=0.08
    elif level=="🥺 진짜 갖고 싶다":
        success=0.04
    else:
        success=0.01

    st.markdown("## 📢 심사 결과")

    if chance<success:
        st.balloons()
        st.snow()

        st.markdown(f"""
<div class="result">

{random.choice(good_comments)}

<h2>{random.choice(good_gifts)}</h2>

🎄 메리 크리스마스!

</div>
""",unsafe_allow_html=True)

    else:

        st.markdown(f"""
<div class="result">

{random.choice(bad_comments)}

<h2>{random.choice(bad_gifts)}</h2>

🎁 산타가 준비한 선물입니다.

불만은 북극 고객센터로 문의해주세요.

</div>
""",unsafe_allow_html=True)

    st.divider()

    if random.random()<0.3:
        st.info("🦌 루돌프 : 다음엔 편지를 좀 더 울면서 써봐.")
    elif random.random()<0.6:
        st.info("🧝 엘프 : 선물보다 양심부터 챙기래.")
    else:
        st.info("🎅 산타 : 내년에도 또 와. 어차피 또 떨어질 수도 있지만.")
