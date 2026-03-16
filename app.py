import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="Visual Idea Board", layout="wide")
st.title("📍 자유 배치 아이디어 보드")

# 데이터 저장 (노드 정보: ID, 내용, X좌표, Y좌표, 완료여부, 부모ID)
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'text': '점심메뉴', 'x': 100, 'y': 100, 'done': True, 'parent': None}
    ]

# --- 상단 컨트롤러 (새 노드 추가) ---
with st.expander("➕ 새 아이디어 가지치기", expanded=True):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        parent_idx = st.selectbox("어디서 뻗어나갈까요?", options=range(len(st.session_state.nodes)), 
                                  format_func=lambda x: st.session_state.nodes[x]['text'])
    with col2:
        new_text = st.text_input("아이디어 내용")
    with col3:
        if st.button("가지 추가") and new_text:
            p_node = st.session_state.nodes[parent_idx]
            # 부모 근처 랜덤 위치에 생성 (살짝 아래 오른쪽)
            st.session_state.nodes.append({
                'id': len(st.session_state.nodes),
                'text': new_text,
                'x': p_node['x'] + 150,
                'y': p_node['y'] + 100,
                'done': False,
                'parent': parent_idx
            })
            st.rerun()

# --- 캔버스 구현 (HTML/CSS 활용) ---
# 스트림릿 내부에 자유 배치를 흉내내기 위한 커스텀 스타일
st.markdown("""
    <style>
    .canvas { position: relative; height: 600px; background-color: #f0f2f6; border-radius: 10px; border: 1px solid #ddd; }
    .node { position: absolute; padding: 10px; border: 2px solid #004d99; background: white; border-radius: 5px; min-width: 100px; text-align: center; }
    .node-done { border-color: #28a745; background-color: #f8fff9; }
    .line { position: absolute; background-color: #004d99; height: 2px; transform-origin: top left; z-index: 0; opacity: 0.3; }
    </style>
""", unsafe_allow_html=True)

# 노드 배치 및 수정
for i, node in enumerate(st.session_state.nodes):
    # 각 노드를 조절할 수 있는 사이드바 설정 (위치 이동용)
    with st.sidebar.expander(f"📍 {node['text']} 설정"):
        st.session_state.nodes[i]['text'] = st.text_input(f"내용 수정", value=node['text'], key=f"t_{i}")
        st.session_state.nodes[i]['x'] = st.slider(f"좌표 X", 0, 1000, node['x'], key=f"x_{i}")
        st.session_state.nodes[i]['y'] = st.slider(f"좌표 Y", 0, 500, node['y'], key=f"y_{i}")
        st.session_state.nodes[i]['done'] = st.checkbox("작성 완료 (체크박스)", value=node['done'], key=f"d_{i}")

    # 화면에 그리기 (HTML 스타일)
    status_class = "node-done" if node['done'] else ""
    st.markdown(f"""
        <div class="node {status_class}" style="left: {node['x']}px; top: {node['y']}px;">
            { "✅" if node['done'] else "✍️" } {node['text']}
        </div>
    """, unsafe_allow_html=True)

st.info("💡 왼쪽 사이드바에서 노드를 드래그(슬라이더)하여 위치를 옮기거나 완료 체크를 할 수 있습니다.")
