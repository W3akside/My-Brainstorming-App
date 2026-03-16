import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Minimal Idea Board", layout="wide")
st.title("📍 아이디어 자유 배치 보드")

# 2. 데이터 초기화
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'text': '중심 생각', 'x': 50, 'y': 50, 'done': True}
    ]

# 3. 새로운 가지 추가 (입력창)
with st.expander("➕ 새로운 아이디어 추가", expanded=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_text = st.text_input("아이디어 내용", placeholder="내용을 입력하세요", key="input_new")
    with col2:
        if st.button("추가하기") and new_text:
            last_node = st.session_state.nodes[-1]
            st.session_state.nodes.append({
                'id': len(st.session_state.nodes),
                'text': new_text,
                'x': last_node['x'] + 40,
                'y': last_node['y'] + 40,
                'done': False
            })
            st.rerun()

st.divider()

# 4. 화면 레이아웃 (설정창 1 : 캔버스 3 비율)
side_col, main_col = st.columns([1, 3])

with side_col:
    st.subheader("⚙️ 박스 관리")
    # 노드 설정을 리스트 형태로 관리
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        with st.expander(f"📦 {node['text']}"):
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node['text'], key=f"edit_{i}")
            st.session_state.nodes[i]['done'] = st.toggle("완성 상태", value=node['done'], key=f"tog_{i}")
            st.session_state.nodes[i]['x'] = st.number_input("가로 위치(X)", 0, 1000, node['x'], key=f"x_val_{i}")
            st.session_state.nodes[i]['y'] = st.number_input("세로 위치(Y)", 0, 800, node['y'], key=f"y_val_{i}")

with main_col:
    # 스타일 정의 (박스를 더 깔끔하게)
    st.markdown("""
        <style>
        .canvas-area { 
            position: relative; width: 100%; height: 650px; 
            background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; 
        }
        .node-card {
            position: absolute; padding: 10px 20px; 
            background: #ffffff; border: 1px solid #333333; 
            border-radius: 4px; font-size: 16px; font-weight: 500;
            box-shadow: 2px 2px 0px #000000; /* 딱딱한 그림자로 세련미 추가 */
            min-width: 100px; text-align: center;
        }
        .node-card-done { 
            background-color: #f8f9fa; border-color: #cccccc; 
            color: #888888; box-shadow: 1px 1px 0px #eeeeee;
        }
        </style>
    """, unsafe_allow_html=True)

    # 캔버스에 박스 그리기
    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        done_class = "node-card-done" if node['done'] else ""
        html_content += f'<div class="node-card {done_class}" style="left:{node["x"]}px; top:{node["y"]}px;">{node["text"]}</div>'
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)

# 초기화 버튼
if st.sidebar.button("전체 삭제"):
    st.session_state.nodes = [{'id': 0, 'text': '중심 생각', 'x': 50, 'y': 50, 'done': True}]
    st.rerun()
