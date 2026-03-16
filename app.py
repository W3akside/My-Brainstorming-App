import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="MindMap Board", layout="wide")
st.title("📍 계층형 아이디어 파생 보드")

# 2. 데이터 초기화 및 에러 방지 (code가 없으면 강제로 초기화)
if 'nodes' not in st.session_state or len(st.session_state.nodes) > 0 and 'code' not in st.session_state.nodes[0]:
    st.session_state.nodes = [
        {'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}
    ]

# 3. 레이아웃
side_col, main_col = st.columns([1, 3])

with side_col:
    st.subheader("⚙️ 박스 관리 및 파생")
    
    # 노드가 하나도 없을 때 생성 버튼
    if not st.session_state.nodes:
        if st.button("➕ 새 시작점 만들기"):
            st.session_state.nodes.append({'id': 0, 'code': '1', 'text': '새 주제', 'x': 100, 'y': 100, 'parent': None})
            st.rerun()

    # 노드 설정창 생성 (안전하게 리스트 복사본 사용)
    current_nodes = list(st.session_state.nodes)
    for i, node in enumerate(current_nodes):
        # 안전한 데이터 접근 (.get 사용)
        node_code = node.get('code', '0')
        node_text = node.get('text', '내용 없음')
        
        with st.expander(f"[{node_code}] {node_text}", expanded=(i == len(st.session_state.nodes)-1)):
            # 내용 수정
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node_text, key=f"edit_{i}")
            
            c1, c2 = st.columns(2)
            st.session_state.nodes[i]['x'] = c1.number_input("X", 0, 1200, node.get('x', 100), key=f"x_{i}")
            st.session_state.nodes[i]['y'] = c2.number_input("Y", 0, 800, node.get('y', 100), key=f"y_{i}")

            st.divider()
            
            # 파생 기능
            new_child = st.text_input("새로운 파생 아이디어", key=f"child_in_{i}", placeholder="예: 한식")
            if st.button(f"🌱 '{node_text}'에서 가지치기", key=f"btn_{i}"):
                if new_child:
                    child_count = sum(1 for n in st.session_state.nodes if n.get('parent') == node['id'])
                    new_code = f"{node_code}-{child_count + 1}"
                    
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes) + 100, # ID 중복 방지
                        'code': new_code,
                        'text': new_child,
                        'x': node.get('x', 100) + 150,
                        'y': node.get('y', 100) + 80,
                        'parent': node['id']
                    })
                    st.rerun()
            
            if st.button(f"🗑️ 이 박스 삭제", key=f"del_{i}", use_container_width=True):
                st.session_state.nodes.pop(i)
                st.rerun()

with main_col:
    # 캔버스 디자인
    st.markdown("""
        <style>
        .canvas-area { 
            position: relative; width: 100%; height: 750px; 
            background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; 
            background-image: radial-gradient(#e0e0e0 1px, transparent 1px); background-size: 30px 30px;
        }
        .node-card {
            position: absolute; padding: 12px 24px; 
            background: white; border: 1.5px solid #333; 
            border-radius: 2px; box-shadow: 3px 3px 0px #000;
            min-width: 140px; text-align: center; z-index: 10;
        }
        .parent-info { font-size: 10px; color: #888; margin-bottom: 2px; }
        .node-text { font-size: 16px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        node_code = node.get('code', '0')
        node_text = node.get('text', '내용 없음')
        
        parent_txt = ""
        if node.get('parent') is not None:
            p_node = next((n for n in st.session_state.nodes if n['id'] == node['parent']), None)
            if p_node:
                parent_txt = f"<div class='parent-info'>from: {p_node['text']}</div>"
        
        html_content += f'''
            <div class="node-card" style="left:{node.get('x', 100)}px; top:{node.get('y', 100)}px;">
                {parent_txt}
                <div class="node-text">[{node_code}] {node_text}</div>
            </div>
        '''
    html_content += '</div>'
    st.markdown(html_content, unsafe_allow_html=True)

if st.sidebar.button("🧹 전체 초기화"):
    st.session_state.nodes = [{'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}]
    st.rerun()
