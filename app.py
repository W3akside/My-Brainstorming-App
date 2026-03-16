import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Idea Board", layout="wide")
st.title("📍 자유 배치 아이디어 보드")

# 2. 세션 상태 초기화 (에러 원천 차단)
if 'nodes' not in st.session_state or st.sidebar.button("🧹 보드 완전 초기화"):
    st.session_state.nodes = [
        {'id': 0, 'text': '시작점', 'x': 50, 'y': 50, 'done': True}
    ]
    st.rerun()

# 3. 새로운 가지 추가
with st.expander("➕ 새 아이디어 가지치기", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_text = st.text_input("아이디어 내용", placeholder="내용을 적으세요", key="input_new")
    with col2:
        if st.button("가지 추가") and new_text:
            # 마지막 노드의 위치를 기준으로 새 노드 생성
            last_node = st.session_state.nodes[-1]
            new_node = {
                'id': len(st.session_state.nodes),
                'text': new_text,
                'x': last_node['x'] + 50,
                'y': last_node['y'] + 50,
                'done': False
            }
            st.session_state.nodes.append(new_node)
            st.rerun()

st.divider()

# 4. 화면 레이아웃
side_col, main_col = st.columns([1, 2])

with side_col:
    st.subheader("⚙️ 개별 설정")
    # 리스트를 복사해서 루프를 돌려야 삭제 시 에러가 안 납니다.
    for i, node in enumerate(list(st.session_state.nodes)):
        with st.expander(f"📌 {node['text']}"):
            st.session_state.nodes[i]['text'] = st.text_input("이름 수정", value=node['text'], key=f"edit_{i}")
            st.session_state.nodes[i]['done'] = st.checkbox("작성 완료", value=node['done'], key=f"chk_{i}")
            st.session_state.nodes[i]['x'] = st.slider("좌표 X", 0, 1000, node['x'], key=f"x_val_{i}")
            st.session_state.nodes[i]['y'] = st.slider("좌표 Y", 0, 600, node['y'], key=f"y_val_{i}")

with main_col:
    st.subheader("💡 캔버스")
    
    # CSS 설정
    st.markdown("""
        <style>
        .canvas-area { 
            position: relative; 
            width: 100%; 
            height: 600px; 
            background-color: #f0f2f6; 
            border: 2px dashed #bdc3c7; 
            border-radius: 20px; 
        }
        .node-card {
            position: absolute;
            padding: 15px;
            background: white;
            border: 2px solid #3498db;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
            font-weight: bold;
            min-width: 120px;
            text-align: center;
        }
        .node-card-done {
            border-color: #2ecc71;
            background-color: #fafffa;
            color: #27ae60;
        }
        </style>
    """, unsafe_allow_html=True)

    # 노드들을 화면에 배치
    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        done_class = "node-card-done" if node['done'] else ""
        status_icon = "✅" if node['done'] else "📝"
        html_content += f'''
            <div class="node-card {done_class}" style="left:{node['x']}px; top:{node['y']}px;">
                {status_icon} {node['text']}
            </div>
        '''
    html_content += '</div>'
    st.markdown(html_content, unsafe_allow_html=True)
