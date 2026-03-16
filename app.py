import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="MindMap Board", layout="wide")
st.title("📍 계층형 아이디어 파생 보드")

# 2. 데이터 초기화 및 강제 동기화 (꼬임 방지)
if 'nodes' not in st.session_state or (len(st.session_state.nodes) > 0 and 'code' not in st.session_state.nodes[0]):
    st.session_state.nodes = [
        {'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}
    ]

# 3. 레이아웃 분할
side_col, main_col = st.columns([1, 3])

with side_col:
    st.subheader("⚙️ 박스 관리 및 파생")
    
    if not st.session_state.nodes:
        if st.button("➕ 새 시작점 만들기"):
            st.session_state.nodes.append({'id': 0, 'code': '1', 'text': '새 주제', 'x': 100, 'y': 100, 'parent': None})
            st.rerun()

    # 노드 설정창 (안전하게 인덱스 기반으로 접근)
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        with st.expander(f"[{node.get('code', '0')}] {node.get('text', '')}", expanded=(i == len(st.session_state.nodes)-1)):
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node.get('text', ''), key=f"edit_{i}")
            
            c1, c2 = st.columns(2)
            st.session_state.nodes[i]['x'] = c1.number_input("X", 0, 1500, node.get('x', 100), key=f"x_{i}")
            st.session_state.nodes[i]['y'] = c2.number_input("Y", 0, 1000, node.get('y', 100), key=f"y_{i}")

            st.divider()
            
            # 파생(가지치기) 기능
            new_child = st.text_input("새 파생 아이디어", key=f"child_in_{i}", placeholder="예: 한식")
            if st.button(f"🌱 가지치기", key=f"btn_{i}"):
                if new_child:
                    child_count = sum(1 for n in st.session_state.nodes if n.get('parent') == node['id'])
                    new_code = f"{node.get('code', '1')}-{child_count + 1}"
                    
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes) + 1,
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
    # 스타일 정의 (그림자 및 모눈종이)
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

    # 캔버스 그리기
    html_content = '<div class="canvas-area">'
    for node in st.session_state.nodes:
        node_code = node.get('code', '0')
        node_text = node.get('text', '')
        
        parent_txt = ""
        if node.get('parent') is not None:
            p_node = next((n for n in st.session_state.nodes if n['id'] == node['parent']), None)
            if p_node:
                parent_txt = f"<div class='parent-info'>부모: {p_node.get('text', '')}</div>"
        
        html_content += f'''
            <div class="node-card" style="left:{node.get('x', 100)}px; top:{node.get('y', 100)}px;">
                {parent_txt}
                <div class="node-text">[{node_code}] {node_text}</div>
            </div>
        '''
    html_content += '</div>'
    
    # [중요] 이 줄이 없으면 아까처럼 태그가 그대로 노출됩니다!
    st.markdown(html_content, unsafe_allow_html=True)

if st.sidebar.button("🧹 전체 초기화"):
    st.session_state.nodes = [{'id': 0, 'code': '1', 'text': '중심 생각', 'x': 100, 'y': 100, 'parent': None}]
    st.rerun()
