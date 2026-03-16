import streamlit as st

# 1. 페이지 설정
st.set_config(page_title="Idea Board", layout="wide")
st.title("📍 기획안 복구: 아이디어 공간 배치 보드")

# 2. 데이터 초기화
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'text': '점심메뉴', 'col': 1, 'row': 0, 'parent': None}
    ]

# 3. 사이드바 제어 (박스 생성/삭제)
with st.sidebar:
    st.header("⚙️ 박스 관리")
    if not st.session_state.nodes:
        if st.button("➕ 새 시작점 생성"):
            st.session_state.nodes = [{'id': 0, 'text': '새 주제', 'col': 1, 'row': 0, 'parent': None}]
            st.rerun()

    for i, node in enumerate(list(st.session_state.nodes)):
        with st.expander(f"📦 {node['text']}"):
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node['text'], key=f"t_{i}")
            
            # 파생 기능
            new_child = st.text_input("여기서 가지치기", key=f"in_{i}")
            if st.button("🌱 추가", key=f"b_{i}"):
                if new_child:
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes) + 1,
                        'text': new_child,
                        'col': (node['col'] + 1) % 4, # 옆 칸으로 배치
                        'parent': node['id']
                    })
                    st.rerun()
            
            if st.button("🗑️ 삭제", key=f"d_{i}"):
                st.session_state.nodes.pop(i)
                st.rerun()

# 4. 메인 화면 (3개의 구역으로 나눔)
st.write("### 💡 브레인스토밍 캔버스")
cols = st.columns(4) # 4개의 기둥을 세움

# 노드들을 컬럼별로 분류해서 배치
for node in st.session_state.nodes:
    target_col = node.get('col', 0)
    with cols[target_col]:
        # 부모 정보 표시
        parent_info = ""
        if node['parent'] is not None:
            p = next((n for n in st.session_state.nodes if n['id'] == node['parent']), None)
            if p: parent_info = f"*(from: {p['text']})*"
        
        # 스트림릿 순정 박스로 깔끔하게 출력 (태그 노출 위험 없음)
        st.info(f"### {node['text']}\n{parent_info}")
