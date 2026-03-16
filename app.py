import streamlit as st
import uuid

# 1. 페이지 설정 (깔끔하게 위로 딱 붙임)
st.set_page_config(page_title="MindMap Brainstorming", layout="wide")
st.title("🧠 무한 확장 아이디어 보드")
st.caption("중앙의 텍스트박스부터 시작해 생각을 무한히 확장해보세요.")

# 2. 데이터 구조 정의 (세션 상태 초기화)
# 각 아이디어는 고유 ID, 내용, 그리고 자식 아이디어들의 ID 리스트를 갖습니다.
if 'nodes' not in st.session_state:
    st.session_state.nodes = {}
    st.session_state.root_id = None

# 3. 핵심 기능: 아이디어 노드 렌더링 함수 (재귀 호출 방식)
def render_node(node_id, depth=0):
    node = st.session_state.nodes.get(node_id)
    if not node: return

    # 깊이에 따라 들여쓰기와 스타일을 적용하여 시각적인 계층 구조 표현
    indent = "    " * depth
    node_key = f"node_{node_id}"
    
    # --- [핵심] 아이디어 박스 (Expander) ---
    # 클릭하면 열려서 내용을 수정하거나 자식을 추가할 수 있습니다.
    box_label = f"💡 {node['text'][:30]}..." if node['text'] else "🆕 새 생각..."
    with st.expander(f"{indent}{box_label}", expanded=(depth == 0)): # 루트는 기본으로 열어둠
        
        # 3-1. 내용 수정 부분
        col1, col2 = st.columns([4, 1])
        with col1:
            edited_text = st.text_area("내용 수정", value=node['text'], key=f"edit_text_{node_id}", height=68, label_visibility="collapsed")
        with col2:
            if st.button("저장", key=f"save_{node_id}"):
                st.session_state.nodes[node_id]['text'] = edited_text
                st.rerun()
            if depth > 0: # 루트 노드는 삭제 불가
                if st.button("삭제", key=f"del_{node_id}"):
                    # 부모 노드의 자식 리스트에서 자신을 제거
                    parent_id = node.get('parent_id')
                    if parent_id and parent_id in st.session_state.nodes:
                        st.session_state.nodes[parent_id]['children'].remove(node_id)
                    # 자신과 하위 노드들을 삭제 (간단하게 자신만 삭제)
                    del st.session_state.nodes[node_id]
                    st.rerun()

        st.divider()

        # 3-2. 자식 아이디어(가지) 추가 부분
        c1, c2 = st.columns([4, 1])
        with c1:
            child_text = st.text_input("여기에 뻗어나갈 생각을 적으세요...", key=f"child_input_{node_id}", placeholder="새로운 가지치기...")
        with c2:
            if st.button("가지 추가", key=f"add_child_{node_id}") and child_text:
                # 새로운 노드 생성
                new_id = str(uuid.uuid4())
                st.session_state.nodes[new_id] = {
                    'text': child_text,
                    'children': [],
                    'parent_id': node_id
                }
                # 현재 노드의 자식 리스트에 추가
                st.session_state.nodes[node_id]['children'].append(new_id)
                st.rerun()

    # --- [핵심] 자식 노드들을 재귀적으로 렌더링 (가지 뻗기) ---
    if node['children']:
        for child_id in node['children']:
            render_node(child_id, depth + 1)


# 4. 화면 출력 부분
# 4-1. 루트 노드(가운데 시작점)가 없는 경우 생성
if not st.session_state.root_id or not st.session_state.nodes:
    st.session_state.nodes = {} # 초기화
    root_id = str(uuid.uuid4())
    st.session_state.nodes[root_id] = {
        'text': "핵심 주제를 적고 시작하세요", # 초기 메시지
        'children': [],
        'parent_id': None
    }
    st.session_state.root_id = root_id

# 4-2. 메인 보드 (가운데 정렬)
st.divider()
col_left, col_main, col_right = st.columns([1, 4, 1])

with col_main:
    # 루트 노드부터 시작해 모든 가지를 렌더링
    render_node(st.session_state.root_id)


# 5. 데이터 관리 기능 (사이드바)
with st.sidebar:
    st.subheader("🛠️ 보드 관리")
    if st.button("전체 초기화 (새 보드)"):
        st.session_state.nodes = {}
        st.session_state.root_id = None
        st.rerun()
    
    st.divider()
    st.caption("💡 팁: 각 생각을 클릭하면 내용을 고치거나 새로운 가지를 뻗을 수 있습니다.")
