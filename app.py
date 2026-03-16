import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="MindMap Board", layout="wide")
st.title("📍 아이디어 파생 보드")

# 2. 데이터 초기화
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'text': '중심 생각', 'x': 100, 'y': 100, 'done': False}
    ]

# 3. 화면 레이아웃 (설정창 1 : 캔버스 3)
side_col, main_col = st.columns([1, 3])

with side_col:
    st.subheader("⚙️ 박스 관리 및 파생")
    
    # 노드 리스트를 루프 돌며 설정창 생성
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        with st.expander(f"📦 {node['text']}", expanded=(i == len(st.session_state.nodes)-1)):
            # 내용 수정 및 상태 관리
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node['text'], key=f"edit_{i}")
            st.session_state.nodes[i]['done'] = st.toggle("작성 완료", value=node['done'], key=f"tog_{i}")
            
            col_x, col_y = st.columns(2)
            st.session_state.nodes[i]['x'] = col_x.number_input("X", 0, 1200, node['x'], key=f"x_{i}")
            st.session_state.nodes[i]['y'] = col_y.number_input("Y", 0, 800, node['y'], key=f"y_{i}")

            st.divider()
            
            # --- [핵심] 여기서 새로운 가지를 뻗음 ---
            new_child = st.text_input("여기서 뻗어나갈 생각", key=f"child_in_{i}", placeholder="새 아이디어 입력")
            if st.button(f"🌱 '{node['text']}'에서 가지치기", key=f"btn_{i}"):
                if new_child:
                    # 현재 박스 위치에서 살짝 옆에 새 박스 생성
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes),
                        'text': new_child,
                        'x': node['x'] + 150,
                        'y': node['y'] + 50,
                        'done': False
                    })
                    st.rerun()

with main_col:
    # 캔버스 디자인
    st.markdown("""
        <style>
        .canvas-area { 
            position: relative; width: 100%; height: 700px; 
            background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; 
            background-image: radial-gradient(#e0e0e0 1px, transparent 1px);
            background-size: 20px 20px; /* 모눈종이 느낌 추가 */
        }
        .node-card {
            position: absolute; padding: 12px 24px; 
            background: #ffffff; border: 1.5px solid #333333; 
            border-radius: 2px; font-size: 16px; font-weight: 500;
            box-shadow: 3px 3px 0px #000000;
            min-width: 120px; text-align: center;
            z-index: 10;
        }
        .node-card-done { 
            background-color: #f8f9fa; border-color: #cccccc; 
            color: #bbbbbb; box-shadow: 1px 1px 0px #dddddd;
        }
        </style>
    """, unsafe_allow_html=True)

    # 캔버스 그리기
    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        done_class = "node-card-done" if node['done'] else ""
        html_content += f'<div class="node-card {done_class}" style="left:{node["x"]}px; top:{node["y"]}px;">{node["text"]}</div>'
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)

if st.sidebar.button("전체 초기화"):
    st.session_state.nodes = [{'id': 0, 'text': '중심 생각', 'x': 100, 'y': 100, 'done': False}]
    st.rerun()
