import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="MindMap Board", layout="wide")
st.title("📍 계층형 아이디어 파생 보드")

# 2. 데이터 초기화
if 'nodes' not in st.session_state:
    # 초기 상태: 족보 번호(code) 추가
    st.session_state.nodes = [
        {'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}
    ]

# 3. 레이아웃
side_col, main_col = st.columns([1, 3])

with side_col:
    st.subheader("⚙️ 박스 관리 및 파생")
    
    if not st.session_state.nodes:
        if st.button("➕ 새 시작점 만들기"):
            st.session_state.nodes.append({'id': 0, 'code': '1', 'text': '새 주제', 'x': 100, 'y': 100, 'parent': None})
            st.rerun()

    # 노드 설정창 생성
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        # 박스 제목에 족보 번호 표시 (예: [1-1] 김치찌개)
        with st.expander(f"[{node['code']}] {node['text']}", expanded=(i == len(st.session_state.nodes)-1)):
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node['text'], key=f"edit_{i}")
            
            c1, c2 = st.columns(2)
            st.session_state.nodes[i]['x'] = c1.number_input("X", 0, 1200, node['x'], key=f"x_{i}")
            st.session_state.nodes[i]['y'] = c2.number_input("Y", 0, 800, node['y'], key=f"y_{i}")

            st.divider()
            
            # --- [핵심] 파생 기능: 부모 정보를 물려줌 ---
            new_child = st.text_input("새로운 파생 아이디어", key=f"child_in_{i}")
            if st.button(f"🌱 가지치기", key=f"btn_{i}"):
                if new_child:
                    # 자식 번호 생성 (예: 부모가 1이면 자식은 1-1, 1-2...)
                    child_count = sum(1 for n in st.session_state.nodes if n.get('parent') == node['id'])
                    new_code = f"{node['code']}-{child_count + 1}"
                    
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes),
                        'code': new_code,
                        'text': new_child,
                        'x': node['x'] + 150,
                        'y': node['y'] + 80,
                        'parent': node['id']
                    })
                    st.rerun()
            
            if st.button(f"🗑️ 삭제", key=f"del_{i}"):
                st.session_state.nodes.pop(i)
                st.rerun()

with main_col:
    # 캔버스 디자인 (모눈종이 + 파생 텍스트 스타일)
    st.markdown("""
        <style>
        .canvas-area { 
            position: relative; width: 100%; height: 750px; 
            background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; 
            background-image: radial-gradient(#e0e0e0 1px, transparent 1px); background-size: 30px 30px;
        }
        .node-card {
            position: absolute; padding: 10px 20px; 
            background: white; border: 1.5px solid #333; 
            border-radius: 2px; box-shadow: 3px 3px 0px #000;
            min-width: 130px; text-align: center;
        }
        .parent-info { font-size: 10px; color: #888; margin-bottom: 2px; }
        .node-text { font-size: 16px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        # 부모가 누구인지 텍스트로 표시
        parent_txt = ""
        if node['parent'] is not None:
            # 부모의 텍스트를 찾아옴
            p_node = next((n for n in st.session_state.nodes if n['id'] == node['parent']), None)
            if p_node:
                parent_txt = f"<div class='parent-info'>from: {p_node['text']}</div>"
        
        html_content += f'''
            <div class="node-card" style="left:{node["x"]}px; top:{node["y"]}px;">
                {parent_txt}
                <div class="node-text">[{node['code']}] {node['text']}</div>
            </div>
        '''
    html_content += '</div>'
    st.markdown(html_content, unsafe_allow_html=True)
