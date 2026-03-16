import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="MindMap Board", layout="wide")
st.title("📍 계층형 아이디어 파생 보드")

# 2. 데이터 초기화 및 강제 동기화 (꼬임 방지용)
if 'nodes' not in st.session_state or not st.session_state.nodes or 'code' not in st.session_state.nodes[0]:
    st.session_state.nodes = [
        {'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}
    ]

# 3. 레이아웃
side_col, main_col = st.columns([1, 3])

with side_col:
    st.subheader("⚙️ 박스 관리 및 파생")
    
    # 족보를 유지하면서 안전하게 루프 돌리기 위해 인덱스 사용
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        # 박스 제목에 족보 번호와 텍스트 표시
        with st.expander(f"[{node.get('code', '1')}] {node.get('text', '내용')}", expanded=(i == len(st.session_state.nodes)-1)):
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node.get('text', ''), key=f"edit_{i}")
            
            c1, c2 = st.columns(2)
            st.session_state.nodes[i]['x'] = c1.number_input("X", 0, 1500, node.get('x', 100), key=f"x_{i}")
            st.session_state.nodes[i]['y'] = c2.number_input("Y", 0, 1000, node.get('y', 100), key=f"y_{i}")

            st.divider()
            
            # 가지치기 기능
            new_child = st.text_input("새 파생 아이디어", key=f"child_in_{i}", placeholder="예: 한식")
            if st.button(f"🌱 '{node.get('text')}'에서 가지치기", key=f"btn_{i}"):
                if new_child:
                    # 자식 번호 계산
                    child_count = sum(1 for n in st.session_state.nodes if n.get('parent') == node['id'])
                    new_code = f"{node.get('code', '1')}-{child_count + 1}"
                    
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes) + 1, # 단순 ID 증가
                        'code': new_code,
                        'text': new_child,
                        'x': node.get('x', 100) + 160,
                        'y': node.get('y', 100) + 60,
                        'parent': node['id']
                    })
                    st.rerun()
            
            if st.button(f"🗑️ 이 박스 삭제", key=f"del_{i}", use_container_width=True):
                st.session_state.nodes.pop(i)
                st.rerun()

with main_col:
    # 캔버스 디자인 스타일
    st.markdown("""
        <style>
        .canvas-area { 
            position: relative; width: 100%; height: 750px; 
            background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; 
            background-image: radial-gradient(#e0e0e0 1.5px, transparent 1.5px); background-size: 30px 30px;
        }
        .node-card {
            position: absolute; padding: 12px 20px; 
            background: white; border: 1.5px solid #333; 
            border-radius: 2px; box-shadow: 4px 4px 0px #000;
            min-width: 140px; text-align: center; z-index: 10;
        }
        .parent-info { font-size: 10px; color: #777; margin-bottom: 4px; border-bottom: 1px solid #eee; }
        .node-text { font-size: 15px; font-weight: bold; color: #222; }
        </style>
    """, unsafe_allow_html=True)

    # 박스 그리기 시작
    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        node_code = node.get('code', '1')
        node_text = node.get('text', '내용')
        
        # 부모가 누구인지 표시
        parent_txt = ""
        if node.get('parent') is not None:
            p_node = next((n for n in st.session_state.nodes if n['id'] == node['parent']), None)
            if p_node:
                parent_txt = f"<div class='parent-info'>부모: {p_node.get('text', '')}</div>"
        
        # 실제 HTML 박스 생성
        html_content += f'''
            <div class="node-card" style="left:{node.get('x', 100)}px; top:{node.get('y', 100)}px;">
                {parent_txt}
                <div class="node-text">[{node_code}] {node_text}</div>
            </div>
        '''
    html_content += '</div>'
    
    # [가장 중요] HTML을 캔버스에 렌더링
    st.markdown(html_content, unsafe_allow_html=True)

if st.sidebar.button("🧹 전체 초기화"):
    st.session_state.nodes = [{'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}]
    st.rerun()
