import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Idea Board", layout="wide")
st.title("📍 자유 배치 아이디어 보드")

# 2. 세션 상태 초기화
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'text': '시작점', 'x': 50, 'y': 50, 'done': True}
    ]

# 3. 새로운 가지 추가
with st.expander("➕ 새 아이디어 가지치기", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_text = st.text_input("아이디어 내용", placeholder="내용을 적으세요", key="input_new")
    with col2:
        if st.button("가지 추가") and new_text:
            last_node = st.session_state.nodes[-1]
            st.session_state.nodes.append({
                'id': len(st.session_state.nodes),
                'text': new_text,
                'x': last_node['x'] + 50,
                'y': last_node['y'] + 50,
                'done': False
            })
            st.rerun()

st.divider()

# 4. 화면 레이아웃
side_col, main_col = st.columns([1, 2])

with side_col:
    st.subheader("⚙️ 개별 설정")
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        with st.expander(f"📌 {node['text']}"):
            st.session_state.nodes[i]['text'] = st.text_input("이름 수정", value=node['text'], key=f"edit_{i}")
            st.session_state.nodes[i]['done'] = st.checkbox("작성 완료", value=node['done'], key=f"chk_{i}")
            st.session_state.nodes[i]['x'] = st.slider("좌표 X", 0, 800, node['x'], key=f"x_val_{i}")
            st.session_state.nodes[i]['y'] = st.slider("좌표 Y", 0, 500, node['y'], key=f"y_val_{i}")

with main_col:
    st.subheader("💡 캔버스")
    
    # CSS 설정 (f-string 에러 방지를 위해 따로 정의)
    style = """
    <style>
    .canvas-area { 
        position: relative; width: 100%; height: 550px; 
        background-color: #f0f2f6; border: 2px dashed #bdc3c7; border-radius: 20px; 
    }
    .node-card {
        position: absolute; padding: 15px; background: white; 
        border: 2px solid #3498db; border-radius: 10px;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
        font-weight: bold; min-width: 120px; text-align: center;
    }
    .node-card-done { border-color: #2ecc71; background-color: #fafffa; color: #27ae60; }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    # 노드 배치 시작
    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        done_class = "node-card-done" if node['done'] else ""
        icon = "✅" if node['done'] else "📝"
        # f-string을 사용해 변수 삽입
        html_content += f'<div class="node-card {done_class}" style="left:{node["x"]}px; top:{node["y"]}px;">{icon} {node["text"]}</div>'
    html_content += '</div>'
    
    # [가장 중요] unsafe_allow_html=True가 있어야 텍스트가 그림으로 변합니다!
    st.markdown(html_content, unsafe_allow_html=True)

if st.sidebar.button("🧹 전체 초기화"):
    st.session_state.nodes = [{'id': 0, 'text': '시작점', 'x': 50, 'y': 50, 'done': True}]
    st.rerun()
