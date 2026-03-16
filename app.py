import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="My Brainstorming", layout="centered")
st.title("🧠 형님의 아이디어 브레인스토밍")

# 데이터 저장소 (세션이 유지되는 동안만 저장됩니다)
if 'my_ideas' not in st.session_state:
    st.session_state.my_ideas = []

# 입력 양식
with st.form("idea_form", clear_on_submit=True):
    new_idea = st.text_input("떠오르는 생각을 적어주세요")
    category = st.selectbox("카테고리", ["사업", "취미", "업무", "기타"])
    submitted = st.form_submit_button("아이디어 추가")
    
    if submitted and new_idea:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.my_ideas.append({"시간": now, "카테고리": category, "내용": new_idea})
        st.success("아이디어가 기록되었습니다!")

st.divider()

# 출력 부분
st.subheader("📝 저장된 아이디어 리스트")
if st.session_state.my_ideas:
    df = pd.DataFrame(st.session_state.my_ideas)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 다운로드 버튼
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="📥 파일로 내보내기", data=csv, file_name="my_ideas.csv", mime="text/csv")
else:
    st.info("아직 저장된 생각이 없습니다. 위에서 입력해보세요!")
