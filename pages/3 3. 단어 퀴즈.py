import streamlit as st
from openai import OpenAI
import random

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["openai_api_key"])

# 단어 목록
words = {
    'alphabet': '알파벳',
    'anything': '무엇이든',
    'dodgeball': '피구',
    'hit': '맞히다, 때리다',
    'invent': '발명하다',
    'know': '알다',
    'real': '진짜의, 실제의',
    'team': '팀',
    'tell': '말하다',
    'throw': '던지다',
    'traditional': '전통적인',
    'each other': '서로'
}

def generate_question():
    word, meaning = random.choice(list(words.items()))
    is_english_to_korean = random.choice([True, False])
    
    if is_english_to_korean:
        question = f"'{word}'의 한국어 뜻은 무엇인가요?"
        correct_answer = meaning
        other_options = [v for v in words.values() if v != meaning]
        options = random.sample(other_options, 3)
    else:
        question = f"'{meaning}'의 영어 단어는 무엇인가요?"
        correct_answer = word
        other_options = [k for k in words.keys() if k != word]
        options = random.sample(other_options, 3)

    options.append(correct_answer)
    random.shuffle(options)
    return question, options, correct_answer

# 단어 퀴즈 상태 초기화
if 'vocabulary_quiz_state' not in st.session_state:
    st.session_state.vocabulary_quiz_state = {
        'question_generated': False,
        'correct_count': 0,
        'total_count': 0,
        'current_question': None,
        'current_options': None,
        'current_answer': None,
        'initialized': False,
        'answered': False  # 새로운 상태 추가
    }

# 앱이 로드될 때마다 초기화
if not st.session_state.vocabulary_quiz_state['initialized']:
    st.session_state.vocabulary_quiz_state = {
        'question_generated': False,
        'correct_count': 0,
        'total_count': 0,
        'current_question': None,
        'current_options': None,
        'current_answer': None,
        'initialized': True,
        'answered': False  # 새로운 상태 추가
    }

# 메인 화면 구성
st.header("✨인공지능 영어단어 퀴즈 선생님 퀴즐링🕵️‍♀️")
st.subheader("어떤것에 대해 알고있는지 묻고 답하기 영어단어 퀴즈💡")
st.divider()

#확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ [새 문제 만들기] 버튼을 눌러 문제 만들기.<br>
    2️⃣ 질문을 읽고 정답을 선택하기.<br> 
    3️⃣ [정답 확인] 버튼 누르기.<br>
    4️⃣ 정답 확인하기.<br>
    <br>
    🙏 퀴즐링은 완벽하지 않을 수 있어요.<br> 
    🙏 그럴 때에는 [새 문제 만들기] 버튼을 눌러주세요.
    """
    ,  unsafe_allow_html=True)

if st.session_state.vocabulary_quiz_state['question_generated']:
    st.markdown("### 질문")
    st.write(st.session_state.vocabulary_quiz_state['current_question'])
      
    with st.form(key='answer_form'):
        selected_option = st.radio("정답을 선택하세요:", st.session_state.vocabulary_quiz_state['current_options'], index=None)
        submit_button = st.form_submit_button(label='정답 확인')

        if submit_button and not st.session_state.vocabulary_quiz_state['answered']:
            if selected_option:
                st.info(f"선택한 답: {selected_option}")
                st.session_state.vocabulary_quiz_state['answered'] = True
                if selected_option.strip() == st.session_state.vocabulary_quiz_state['current_answer'].strip():  
                    st.success("정답입니다!")
                    st.session_state.vocabulary_quiz_state['correct_count'] += 1
                else:
                    st.error(f"틀렸습니다. 정답은 {st.session_state.vocabulary_quiz_state['current_answer']}입니다.")
            else:
                st.warning("답을 선택해주세요.")
        elif st.session_state.vocabulary_quiz_state['answered']:
            st.warning("이미 답변을 제출했습니다. 새 문제를 만들어주세요.")

else:
    st.info("아래의 '새 문제 만들기' 버튼을 눌러 퀴즈를 시작하세요.")

# 새 문제 만들기 버튼
if st.button("새 문제 만들기"):
    question, options, correct_answer = generate_question()
    st.session_state.vocabulary_quiz_state['current_question'] = question
    st.session_state.vocabulary_quiz_state['current_options'] = options
    st.session_state.vocabulary_quiz_state['current_answer'] = correct_answer
    st.session_state.vocabulary_quiz_state['question_generated'] = True
    st.session_state.vocabulary_quiz_state['answered'] = False  # 답변 상태 초기화
    st.session_state.vocabulary_quiz_state['total_count'] += 1  # 총 문제 수 증가
    st.rerun()

# 사이드바에 정답 카운트 표시
st.sidebar.header("단어퀴즈 점수")
st.sidebar.write(f"총 문제 수: {st.session_state.vocabulary_quiz_state['total_count']}")
st.sidebar.write(f"맞춘 문제 수: {st.session_state.vocabulary_quiz_state['correct_count']}")
if st.session_state.vocabulary_quiz_state['total_count'] > 0:
    accuracy = int((st.session_state.vocabulary_quiz_state['correct_count'] / st.session_state.vocabulary_quiz_state['total_count']) * 100)
    st.sidebar.write(f"정확도: {accuracy}%")
