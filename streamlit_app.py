import random
import math
import streamlit as st

st.title("분수의 약분 마스터")
st.markdown("<style>div[data-testid='stNumberInput'] {width: 10cm !important;}</style>", unsafe_allow_html=True)

def generate_fraction():
    while True:
        numerator = random.randint(2, 50)
        denominator = random.randint(2, 50)
        if numerator < denominator and math.gcd(numerator, denominator) != 1:
            return numerator, denominator

def get_divisors(numerator, denominator):
    divisors = []
    for i in range(2, min(numerator, denominator) + 1):
        if numerator % i == 0 and denominator % i == 0:
            divisors.append(i)
    return divisors

# -------------------------------
# 초기 세션 설정
# -------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'numerator' not in st.session_state or 'denominator' not in st.session_state:
    st.session_state.numerator, st.session_state.denominator = generate_fraction()
if 'current_divisor' not in st.session_state:
    st.session_state.current_divisor = None

numerator = st.session_state.numerator
denominator = st.session_state.denominator

# -------------------------------
# STEP 1: 어떤 수로 나눌 수 있나요?
# -------------------------------
if st.session_state.step == 1:
    st.write(f"**문제:** {numerator}/{denominator} 를 약분해봅시다.")
    st.info("분수를 보고, 어떤 수로 나눌 수 있는지 직접 입력하세요.")
    user_divisor = st.number_input(
        "어떤 수로 나눌 수 있나요? (2~50)", min_value=1, max_value=50, step=1,
        key="user_divisor_input_new",
        label_visibility="visible",
        format="%d",
    )
    if st.button("완료", key="divisor_btn"):
        divisors = get_divisors(numerator, denominator)
        if user_divisor in divisors:
            st.session_state.current_divisor = user_divisor
            st.session_state.step = 2  # 약분 단계로 이동
            st.rerun()
        else:
            st.warning("답이 맞지 않아요. 다시 생각해보세요.")

# -------------------------------
# STEP 2: 약분 수행
# -------------------------------
if st.session_state.step == 2:
    st.success(f"좋아요! 이제 {st.session_state.current_divisor}로 약분해봅시다.")
    st.write(f"문제로 제시한 분수 {numerator}/{denominator} 를 {st.session_state.current_divisor}로 나누세요.")

    user_num = st.number_input("분자(나눈 결과)", min_value=1, max_value=numerator, step=1, key=f"user_num_{numerator}_{denominator}")
    user_den = st.number_input("분모(나눈 결과)", min_value=1, max_value=denominator, step=1, key=f"user_den_{numerator}_{denominator}")

    if st.button("완료", key=f"reduce_btn_{numerator}_{denominator}"):
        correct_num = numerator // st.session_state.current_divisor
        correct_den = denominator // st.session_state.current_divisor

        if user_num == correct_num and user_den == correct_den:
            st.session_state.numerator = correct_num
            st.session_state.denominator = correct_den

            # ✅ 기약분수 검사
            if math.gcd(correct_num, correct_den) == 1:
                st.session_state.step = 3  # 완성
            else:
                # 🔁 아직 기약분수가 아니면 "기약분수가 아니네요" 문구 보여주기
                st.session_state.step = 2.5
            st.rerun()
        else:
            st.warning("답이 틀렸습니다. 다시 약분해보세요.")

# -------------------------------
# STEP 2.5: 기약분수가 아닐 때
# -------------------------------
if st.session_state.step == 2.5:
    st.info("기약분수가 아니네요. 다시 약분해 봅시다.")
    st.write(f"현재 분수: **{st.session_state.numerator}/{st.session_state.denominator}**")

    if st.button("다음", key="next_to_repeat"):
        st.session_state.current_divisor = None
        st.session_state.step = 1  # 다시 어떤 수로 나눌 수 있나요? 단계로 이동
        st.rerun()

# -------------------------------
# STEP 3: 완료
# -------------------------------
if st.session_state.step == 3:
    final_num = st.session_state.numerator
    final_den = st.session_state.denominator
    st.success(f"정답: {final_num}/{final_den}  \n기약분수 입니다. 잘 했어요!")

    if st.button("새로운 문제 풀기", key="new_problem_btn"):
        st.session_state.step = 1
        st.session_state.numerator, st.session_state.denominator = generate_fraction()
        st.session_state.current_divisor = None
        st.rerun()
