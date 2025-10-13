import random
import math
import streamlit as st  # ✅ FIX: 누락된 임포트 추가

st.title("분수의 약분 마스터")

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

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'numerator' not in st.session_state or 'denominator' not in st.session_state:
    st.session_state.numerator, st.session_state.denominator = generate_fraction()
if 'current_divisor' not in st.session_state:
    st.session_state.current_divisor = None

numerator = st.session_state.numerator
denominator = st.session_state.denominator

if st.session_state.step == 1:
    st.write(f"**문제:** {numerator}/{denominator} 를 약분해봅시다.")
    st.info("분수를 보고, 어떤 수로 나눌 수 있는지 직접 입력하세요.")
    user_divisor = st.number_input("어떤 수로 나눌 수 있나요? (2~50)", min_value=2, max_value=50, step=1, key="user_divisor_input_new")
    if st.button("완료", key="divisor_btn"):
        divisors = get_divisors(numerator, denominator)
        if user_divisor in divisors:
            st.session_state.current_divisor = user_divisor
            st.session_state.show_next = True
            st.session_state.step = 1.5
        else:
            st.warning("답이 맞지 않아요. 다시 생각해보세요")

if st.session_state.step == 1.5:
    st.success("정답입니다. 이제 약분을 해보세요!")
    if st.button("다음", key="go_to_reduction"):
        st.session_state.step = 2
        st.session_state.show_next = False
        st.rerun()  # ✅ FIX: 즉시 재실행하여 1.5단계 메시지 잔존 방지

if st.session_state.step == 4:
    st.write(f"{numerator}/{denominator} 를 {st.session_state.current_divisor}로 나누면 어떻게 되나요?")
    user_num = st.number_input("분자(나눈 결과)", min_value=1, max_value=numerator, step=1, key="user_num_input2")
    user_den = st.number_input("분모(나눈 결과)", min_value=1, max_value=denominator, step=1, key="user_den_input2")
    if st.button("완료", key="reduce_btn2"):
        correct_num = numerator // st.session_state.current_divisor
        correct_den = denominator // st.session_state.current_divisor
        if user_num == correct_num and user_den == correct_den:
            # 기약분수인지 확인
            if math.gcd(correct_num, correct_den) == 1:
                # ✅ FIX: 최종 값으로 갱신 후 step=3
                st.session_state.numerator = correct_num
                st.session_state.denominator = correct_den
                st.session_state.step = 3
            else:
                st.info("기약분수가 아니네요. 더 약분해 볼까요?")
                st.session_state.numerator = correct_num
                st.session_state.denominator = correct_den
                st.session_state.current_divisor = None
                st.session_state.step = 2.5

if st.session_state.step == 2.5:
    st.info("기약분수가 아니네요. 더 약분해 볼까요?")
    if st.button("다음", key="next_to_repeat"):
        st.session_state.step = 2.55

if st.session_state.step == 2.55:
    st.write(f"분수 {st.session_state.numerator}/{st.session_state.denominator} 를 더 약분해봅시다.")
    st.info("약분할 숫자를 선택하세요.")
    user_divisor = st.number_input("어떤 수로 나눌 수 있나요? (2~50)", min_value=2, max_value=50, step=1, key="user_divisor_input_repeat")
    if st.button("완료", key="divisor_btn_repeat"):
        divisors = get_divisors(st.session_state.numerator, st.session_state.denominator)
        if user_divisor in divisors:
            st.session_state.current_divisor = user_divisor
            st.session_state.step = 2.6
        else:
            st.warning("답이 맞지 않아요. 다시 생각해보세요")

if st.session_state.step == 2.6:
    st.session_state.step = 2.7
    st.rerun()  # ✅ 권장: experimental_rerun 대신 rerun

if st.session_state.step == 2.7:
    st.write(f"문제로 제시한 분수 {st.session_state.numerator}/{st.session_state.denominator} 를 {st.session_state.current_divisor}로 약분하세요.")
    user_num = st.number_input("분자(나눈 결과)", min_value=1, max_value=st.session_state.numerator, step=1, key="user_num_input_repeat")
    user_den = st.number_input("분모(나눈 결과)", min_value=1, max_value=st.session_state.denominator, step=1, key="user_den_input_repeat")
    if st.button("완료", key="reduce_btn_repeat"):
        correct_num = st.session_state.numerator // st.session_state.current_divisor
        correct_den = st.session_state.denominator // st.session_state.current_divisor
        if user_num == correct_num and user_den == correct_den:
            if math.gcd(correct_num, correct_den) == 1:
                # ✅ FIX: 최종 값으로 갱신 후 step=3
                st.session_state.numerator = correct_num
                st.session_state.denominator = correct_den
                st.session_state.step = 3
            else:
                st.info("기약분수가 아니네요. 더 약분해 볼까요?")
                st.session_state.numerator = correct_num
                st.session_state.denominator = correct_den
                st.session_state.current_divisor = None
                st.session_state.step = 2.5
        else:
            st.warning("답이 틀렸습니다. 다시 약분해보세요")

if st.session_state.step == 2:
    st.write(f"문제로 제시한 분수 {numerator}/{denominator} 를 {st.session_state.current_divisor}로 약분하세요.")
    user_num = st.number_input("분자(나눈 결과)", min_value=1, max_value=numerator, step=1, key="user_num_input")
    user_den = st.number_input("분모(나눈 결과)", min_value=1, max_value=denominator, step=1, key="user_den_input")
    if st.button("완료", key="reduce_btn"):
        correct_num = numerator // st.session_state.current_divisor
        correct_den = denominator // st.session_state.current_divisor
        if user_num == correct_num and user_den == correct_den:
            # 기약분수인지 확인
            if math.gcd(correct_num, correct_den) == 1:
                # ✅ FIX: 최종 값으로 갱신 후 step=3
                st.session_state.numerator = correct_num
                st.session_state.denominator = correct_den
                st.session_state.step = 3
            else:
                st.info("기약분수가 아니네요. 더 약분해 볼까요?")
                st.session_state.numerator = correct_num
                st.session_state.denominator = correct_den
                st.session_state.current_divisor = None
                st.session_state.step = 1
        else:
            st.warning("답이 틀렸습니다. 다시 약분해보세요")

if st.session_state.step == 3:
    if 'show_success' not in st.session_state or st.session_state.show_success:
        final_num = st.session_state.numerator
        final_den = st.session_state.denominator
        st.success(f"정답: {final_num}/{final_den}  \n기약분수 입니다. 잘 했어요!")
        st.session_state.show_success = False
    if st.button("새로운 문제 풀기", key="new_problem_btn"):
        st.session_state.step = 1
        st.session_state.numerator, st.session_state.denominator = generate_fraction()
        st.session_state.current_divisor = None
        st.session_state.show_success = True
        st.rerun()
