import streamlit as st

st.set_page_config(page_title="다문화 친구와 함께하는 이야기", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'situation_selection'

if st.session_state.page == 'situation_selection':
    st.title("다문화 친구가 겪는 어려운 상황을 선택해보세요")

    situations = [
        ("언어 장벽", "🗣️"), ("문화적 차이", "🌏"), ("소외되거나 따돌림", "🚫"),
        ("발표를 두려워함", "😨"), ("외모에 대한 편견", "👀"),
        ("역차별", "⚖️"), ("학습의 어려움", "📘"), ("심리적 어려움", "💭"),
        ("진로 고민", "🧭"), ("부모 세대와의 갈등", "👪")
    ]

    cols = st.columns(5)
    for i in range(2):
        for j in range(5):
            idx = i * 5 + j
            with cols[j]:
                if st.button(f"{situations[idx][1]} {situations[idx][0]}", key=f"situation_{idx}"):
                    st.session_state.selected_situation = situations[idx][0]
                    st.session_state.page = 'character_creation'
                    st.rerun()

elif st.session_state.page == 'character_creation':
    st.title("문제를 해결할 수 있는 캐릭터를 만들어봐요")
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("캐릭터 속성 선택")
        if 'character' not in st.session_state:
            st.session_state.character = {}

        st.session_state.character['eye_color'] = st.radio("1. 눈동자 색", ["갈색", "검정", "초록", "파랑", "회색"], horizontal=True)
        st.session_state.character['eye_style'] = st.selectbox("2. 눈 스타일", ["크고 동그란 눈", "웃는 눈", "졸린 눈", "진지한 눈"])
        st.session_state.character['hair_style'] = st.selectbox("3. 헤어 스타일", ["단발", "긴 생머리", "곱슬머리", "스포츠 머리", "땋은 머리"])
        st.session_state.character['hair_color'] = st.radio("4. 헤어 색깔", ["검정", "갈색", "금발", "빨강", "파랑"], horizontal=True)
        st.session_state.character['skin_tone'] = st.radio("5. 피부색", ["밝은 톤", "중간 톤", "짙은 톤", "황갈색"], horizontal=True)
        st.session_state.character['clothes'] = st.selectbox("6. 옷 스타일", ["티셔츠", "원피스", "전통의상", "교복", "스포츠복"])
        st.session_state.character['name'] = st.text_input("7. 캐릭터 이름", max_chars=10)

        col_reset, col_next = st.columns(2)
        if col_reset.button("초기화"):
            for key in list(st.session_state.keys()):
                if key not in ["page"]:
                    del st.session_state[key]
            st.rerun()

        if col_next.button("다음 단계로"):
            st.session_state.page = 'script_writing'
            st.rerun()

    with col2:
        st.subheader("캐릭터 미리보기")
        character = st.session_state.get("character", {})
        if character:
            st.info(f"이름: {character.get('name', '')}")
            st.text(f"눈: {character.get('eye_color', '')} / {character.get('eye_style', '')}")
            st.text(f"머리: {character.get('hair_style', '')} / {character.get('hair_color', '')}")
            st.text(f"피부색: {character.get('skin_tone', '')}")
            st.text(f"옷: {character.get('clothes', '')}")

elif st.session_state.page == 'script_writing':
    st.title("역할극 대본을 만들어보세요")
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("입력 영역")
        main_char = st.session_state.character['name'] if 'character' in st.session_state else '주인공'
        char1 = st.text_input("등장인물 1 (주인공)", value=main_char)
        char2 = st.text_input("등장인물 2")
        char3 = st.text_input("등장인물 3")
        char4 = st.text_input("등장인물 4")
        st.session_state.script_characters = [c for c in [char1, char2, char3, char4] if c]

        location = st.selectbox("배경 장소", ["교실", "운동장", "급식실", "집 앞", "행사장"])
        narration = st.text_area("상황 해설", placeholder="예: 급식 시간, 친구들이 전통 음식을 보고 이상하다고 놀린다.")
        dialogues = {}
        for person in st.session_state.script_characters:
            dialogues[person] = st.text_area(f"{person} 대사", height=100)
        st.session_state.dialogues = dialogues

        if st.button("이야기 구성으로 이동"):
            st.session_state.page = 'story_building'
            st.rerun()

    with col2:
        st.subheader("대본 미리보기")
        st.markdown(f"**문제 상황:** {st.session_state.get('selected_situation', '')}")
        st.markdown(f"**장소:** {location}")
        st.markdown(f"**해설:** {narration}")
        for person, line in dialogues.items():
            st.markdown(f"**{person}**: 💬 {line}")

elif st.session_state.page == 'story_building':
    st.title("우리 이야기를 동화로 만들어봅시다.")
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("이야기 단계 입력")
        st.session_state.story = {
            "발단": st.text_area("발단 (언제, 어디서, 누가)", height=60),
            "전개": st.text_area("전개 (어떤 일이 시작되었는지)", height=60),
            "위기": st.text_area("위기 (갈등, 문제 발생)", height=60),
            "절정": st.text_area("절정 (갈등 해결 시도)", height=60),
            "결말": st.text_area("결말 (어떻게 끝났는지)", height=60),
        }

    with col2:
        st.subheader("이야기 카드 미리보기")
        for stage, content in st.session_state.story.items():
            st.markdown(f"### 📘 {stage}")
            st.markdown(f"{content}")
