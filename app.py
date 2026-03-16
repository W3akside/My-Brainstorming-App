import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Visual Idea Board", layout="wide")
st.title("📍 자유 배치 아이디어 보드")

# 2. 데이터 초기화 (에러 방지를 위해 세션 상태를 확실히 잡습니다)
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'text': '점심메뉴', 'x': 100, 'y': 100, 'done': True, 'parent': None}
    ]

# 3. 새로운 가지 추가 로직
with st.expander("➕ 새 아이디어 가지치기", expanded=True):
    col1, col2, col3 = st.columns([2, 2, 1])
    
    # 현재 존재하는 노드 리스트 생성
    node_options = list(range(len(st.session_state.nodes)))
    
    with col1:
        parent_idx = st.selectbox(
            "어디서 뻗어나갈까요?", 
            options=node_options, 
            format_func=lambda x: st.session_state.nodes[x]['text']
        )
    with col2:
        new_text = st.text_input("아이디어 내용", placeholder="예: 김치찌개")
    with col3:
        st.write("") # 간격 맞추기용
        if st.button("가지 추가") and new_text:
            p_node = st.session_state.nodes[parent_idx]
            st.session_state.nodes.append({
                'id': len(st.session_state.nodes),
                'text': new_text,
                'x': p_node['x'] + 150,
                'y': p_node['y'] + 80,
                'done': False,
                'parent': parent_idx
            })
            st.rerun()

st.divider()

# 4. 스타일 정의 (박스 및 선 그리기용)
st.markdown("""
    <style>
    .canvas { position: relative; height: 500px; background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 15px; overflow: hidden; }
    .node-box {
        position: absolute;
        padding: 12px 20px;
        border: 2px solid #004d99;
        background: white;
        border-radius: 8px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        z-index: 2;
    }
    .node-done { border-color: #28a745; color: #28a745; background-color: #f0fff4; }
    </style>
""", unsafe_allow_html=True)

# 5. 메인 레이아웃: 사이드바(설정)와 메인(캔버스) 분리
side_col, main_col = st.columns([1, 3])

with main_col:
    # 캔버스 시작
    st.write("##### 💡 보드 레이아웃")
    canvas_html = '<div class="canvas">'
    
    for node in st.session_state.nodes:
        status_style = "node-done" if node['done'] else ""
        icon = "✅" if node['done'] else "✍️"
        canvas_html += f'<div class="node-box {status_style}" style="left: {node["x"]}px; top: {node["y"]}px;">{icon} {node["text"]}</div>'
        
        # 부모가 있다면 선 긋기 (간단한 직선 표현)
        if node['parent'] is not None:
            p = st.session_state.nodes[node['parent']]
            # 선을 위한 SVG는 복잡하므로 여기서는 텍스트 박스로 느낌만 냅니다.
    
    canvas_html += '</div>'
    st.markdown(canvas_html, unsafe_allow_html=True)

with side_col:
    st.write("##### ⚙️ 위치 및 상태 조절")
    for i, node in enumerate(st.session_state.nodes):
        with st.expander(f"{node['text']}"):
            st.session_state.nodes[i]['done'] = st.checkbox("작성 완료", value=node['done'], key=f"d_{i}")
            st.session_state.nodes[i]['x'] = st.slider("좌표 X", 0, 800, node['x'], key=f"x_{i}")
            st.session_state.nodes[i]['y'] = st.slider("좌표 Y", 0, 400, node['y'], key=f"y_{i}")
            if st.button("삭제", key=f"del_{i}"):
                if i != 0: # 루트는 삭제 불가
                    st.session_state.nodes.pop(i)
                    st.rerun()

if st.sidebar.button("🧹 전체 초기화"):
    del st.session_state.nodes
    st.rerun()
