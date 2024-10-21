import streamlit as st
import random
import re

sentences = [
    ("Do you know anything about pansori?", "판소리에 대해 알고있나요?", "🎭"),
    ("Do you know anything about yakgwa?", "약과에 대해 알고있나요?", "🍪"),
    ("Do you know anything about Hangeul?", "한글에 대해 알고있나요?", "ㄱㄴㄷ"),
    ("Yes, I know about it.", "네, 그것에 대해 알고 있어요.", "👍"),
    ("No, I have no idea.", "아니요, 전혀 모르겠어요.", "🤷")
]

# 세션 상태 초기화
if 'writing_quiz_question_order' not in st.session_state:
    st.session_state.writing_quiz_question_order = list(range(len(sentences)))
    random.shuffle(st.session_state.writing_quiz_question_order)
if 'writing_quiz_current_question_index' not in st.session_state:
    st.session_state.writing_quiz_current_question_index = 0
if 'writing_quiz_total_questions' not in st.session_state:
    st.session_state.writing_quiz_total_questions = 0
if 'writing_quiz_correct_answers' not in st.session_state:
    st.session_state.writing_quiz_correct_answers = 0
if 'writing_quiz_current_question' not in st.session_state:
    st.session_state.writing_quiz_current_question = None
if 'writing_quiz_sidebar_placeholder' not in st.session_state:
    st.session_state.writing_quiz_sidebar_placeholder = st.sidebar.empty()
if 'writing_quiz_num_words_to_remove' not in st.session_state:
    st.session_state.writing_quiz_num_words_to_remove = 1

def generate_question():
    if st.session_state.writing_quiz_current_question_index >= len(sentences):
        random.shuffle(st.session_state.writing_quiz_question_order)
        st.session_state.writing_quiz_current_question_index = 0
    
    sentence_index = st.session_state.writing_quiz_question_order[st.session_state.writing_quiz_current_question_index]
    sentence, translation, emoji = sentences[sentence_index]
    words = sentence.split()
    
    # 모든 단어를 선택 대상으로 함
    all_words = words.copy()
    
    # 사용자가 선택한 수만큼의 단어를 랜덤하게 선택
    words_to_remove = random.sample(all_words, st.session_state.writing_quiz_num_words_to_remove)
    
    blanked_words = words.copy()
    for word in words_to_remove:
        index = blanked_words.index(word)
        blanked_words[index] = '_____'
    
    blanked_sentence = ' '.join(blanked_words)
    
    # 정답 문장 저장
    st.session_state.writing_quiz_full_sentence = sentence
    
    st.session_state.writing_quiz_current_question_index += 1
    
    return blanked_sentence, translation, emoji, words_to_remove

# 사이드바 업데이트 함수
def update_sidebar():
    st.session_state.writing_quiz_sidebar_placeholder.empty()
    with st.session_state.writing_quiz_sidebar_placeholder.container():
        st.write("## 쓰기퀴즈 점수")
        st.write(f"총 문제 수: {st.session_state.writing_quiz_total_questions}")
        st.write(f"맞춘 문제 수: {st.session_state.writing_quiz_correct_answers}")
        if st.session_state.writing_quiz_total_questions > 0:
            accuracy = int((st.session_state.writing_quiz_correct_answers / st.session_state.writing_quiz_total_questions) * 100)
            st.write(f"정확도: {accuracy}%")

# 초기 사이드바 설정
update_sidebar()

st.header("✨인공지능 영어문장 퀴즈 선생님 퀴즐링🕵️‍♀️")
st.subheader("어떤 것에 대해 알고 있는지 묻고 답하기 영어쓰기 퀴즈💡")
st.divider()

# 확장 설명
with st.expander("❗❗ 글상자를 펼쳐 사용방법을 읽어보세요 👆✅", expanded=False):
    st.markdown(
    """     
    1️⃣ 나에게 맞게 빈칸 개수 고르기<br>
    2️⃣ [새 문제 만들기] 버튼을 눌러 문제 만들기.<br>
    3️⃣ 빈칸에 들어갈 단어 쓰기. 단어가 2개 이상일 때는 쉼표나 띄어쓰기 등으로 구별하세요.<br> 
    4️⃣ 정답 확인하기.<br>
    
    <br>
    🙏 퀴즐링은 완벽하지 않을 수 있어요.<br> 
    🙏 그럴 때에는 [새 문제 만들기] 버튼을 눌러주세요.
    """
    , unsafe_allow_html=True)

if st.session_state.writing_quiz_current_question is not None:
    blanked_sentence, translation, emoji, words_to_remove = st.session_state.writing_quiz_current_question
    st.markdown(f"### {blanked_sentence} {emoji}")
    st.write(f"해석: {translation}")

    user_answer = st.text_input("빈칸에 들어갈 단어를 입력하세요:")

    if st.button("정답 확인"):
        if user_answer:
            # 사용자 답변과 정답에서 모든 구두점 제거 및 소문자화
            user_words = set(re.findall(r'\w+', user_answer.lower()))
            correct_words = set(re.findall(r'\w+', ' '.join(words_to_remove).lower()))
            
            if user_words == correct_words:
                st.success("정답입니다!")
                st.session_state.writing_quiz_correct_answers += 1
            else:
                st.error(f"틀렸습니다. 정답은 {', '.join(words_to_remove)}입니다.")
            
            # 정답 문장 표시
            st.markdown(f"### 정답 문장: {st.session_state.writing_quiz_full_sentence} {emoji}")
            
            update_sidebar()
            st.session_state.writing_quiz_current_question = None
        else:
            st.warning("답을 입력해주세요.")

# "새 문제 만들기" 버튼
if st.button("새 문제 만들기"):
    st.session_state.writing_quiz_current_question = generate_question()
    st.session_state.writing_quiz_total_questions += 1
    update_sidebar()
    st.rerun()

# 사용자가 제거할 단어 수를 선택할 수 있는 슬라이더 추가
st.session_state.writing_quiz_num_words_to_remove = st.slider("제거할 단어 수를 선택하세요", 1, 3, st.session_state.writing_quiz_num_words_to_remove)
