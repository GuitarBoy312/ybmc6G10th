import streamlit as st
import random

sentences = [
    ("Do you know anything about pansori?", "판소리에 대해 뭔가 아시나요?", "🎭"),
    ("Do you know anything about yakgwa?", "약과에 대해 뭔가 아시나요?", "🍪"),
    ("Do you know anything about Hangeul?", "한글에 대해 뭔가 아시나요?", "ㄱㄴㄷ"),
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
if 'sentence_word_indices' not in st.session_state:
    st.session_state.sentence_word_indices = [list(range(len(sentence[0].split()))) for sentence in sentences]
    for indices in st.session_state.sentence_word_indices:
        random.shuffle(indices)

def generate_question():
    available_sentences = [i for i, indices in enumerate(st.session_state.sentence_word_indices) if indices]
    
    if not available_sentences:
        st.session_state.sentence_word_indices = [list(range(len(sentence[0].split()))) for sentence in sentences]
        for indices in st.session_state.sentence_word_indices:
            random.shuffle(indices)
        available_sentences = list(range(len(sentences)))
    
    sentence_index = random.choice(available_sentences)
    word_index = st.session_state.sentence_word_indices[sentence_index].pop()
    
    sentence, translation, emoji = sentences[sentence_index]
    words = sentence.split()
    correct_word = words[word_index]
    
    blanked_words = words.copy()
    blanked_words[word_index] = '_____'
    blanked_sentence = ' '.join(blanked_words)
    
    st.session_state.writing_quiz_total_questions += 1
    
    return blanked_sentence, translation, emoji, correct_word

# 사이드바 업데이트 함수
def update_sidebar():
    st.session_state.writing_quiz_sidebar_placeholder.empty()
    with st.session_state.writing_quiz_sidebar_placeholder.container():
        st.write("## 퀴즈 점수")
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
    1️⃣ [새 문제 만들기] 버튼을 눌러 문제 만들기.<br>
    2️⃣ 빈칸에 들어갈 단어를 고르세요.<br> 
    3️⃣ [정답 확인] 버튼 누르기.<br>
    4️⃣ 정답 확인하기.<br>
    <br>
    🙏 퀴즐링은 완벽하지 않을 수 있어요.<br> 
    🙏 그럴 때에는 [새 문제 만들기] 버튼을 눌러주세요.
    """
    , unsafe_allow_html=True)

if st.session_state.writing_quiz_current_question is not None:
    blanked_sentence, translation, emoji, correct_word = st.session_state.writing_quiz_current_question
    st.markdown(f"### {blanked_sentence} {emoji}")
    st.write(f"해석: {translation}")

    user_answer = st.text_input("빈칸에 들어갈 단어를 입력하세요:")

    if st.button("정답 확인"):
        if user_answer:  # 사용자가 답을 입력했는지 확인
            st.write(f"입력한 답: {user_answer}")
            
            # 사용자 답변과 정답에서 쉼표, 마침표를 제거하고 소문자로 변환하여 비교
            user_answer_cleaned = user_answer.lower().replace(',', '').replace('.', '').strip()
            correct_word_cleaned = correct_word.lower().replace(',', '').replace('.', '').strip()
            
            if user_answer_cleaned == correct_word_cleaned:
                st.success("정답입니다!")
                st.session_state.writing_quiz_correct_answers += 1
            else:
                st.error(f"틀렸습니다. 정답은 {correct_word}입니다.")
            
            full_sentence = blanked_sentence.replace('_____', correct_word)
            st.markdown(f"### 정답 문장: {full_sentence} {emoji}")
            
            update_sidebar()
            st.session_state.writing_quiz_current_question = None
        else:
            st.warning("답을 입력해주세요.")

# "새 문제 만들기" 버튼
if st.button("새 문제 만들기"):
    st.session_state.writing_quiz_current_question = generate_question()
    update_sidebar()
    st.rerun()
