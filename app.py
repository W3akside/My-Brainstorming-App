import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Safe MindMap", layout="wide")
st.title("📍 안전 모드 아이디어 파생 보드")

# 2. 데이터 초기화 (에러 방지용 안전 장치)
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        {'id': 0, 'code': '1', 'text': '중심 생각', 'parent': None}
    ]

# 3. 레이아웃
side_col, main_col = st.columns([1, 2])

with side_col:
    st.subheader("⚙️ 관리창")
    
    # 노드가 하나도 없으면 초기화
    if not st.session_state.nodes:
        if st.button("➕ 다시 시작하기"):
            st.session_state.nodes = [{'id': 0, 'code': '1', 'text': '중심 생각', 'parent': None}]
            st.rerun()

    # 설정 및 파생 로직
    for i in range(len(st.session_state.nodes)):
        node = st.session_state.nodes[i]
        with st.expander(f"[{node['code']}] {node['text']}", expanded=(i == len(st.session_state.nodes)-1)):
            # 내용 수정
            st.session_state.nodes[i]['text'] = st.text_input("내용 수정", value=node['text'], key=f"edit_{i}")
            
            # 파생(가지치기)
            new_child = st.text_input("새 파생 아이디어", key=f"child_in_{i}")
            if st.button(f"🌱 가지치기", key=f"btn_{i}"):
                if new_child:
                    child_count = sum(1 for n in st.session_state.nodes if n.get('parent') == node['id'])
                    new_code = f"{node['code']}-{child_count + 1}"
                    st.session_state.nodes.append({
                        'id': len(st.session_state.nodes) + 1,
                        'code': new_code,
                        'text': new_child,
                        'parent': node['id']
                    })
                    st.rerun()
            
            if st.button(f"🗑️ 삭제", key=f"del_{i}"):
                st.session_state.nodes.pop(i)
                st.rerun()

with main_col:
    st.subheader("💡 아이디어 맵")
    
    # HTML 박스 대신 스트림릿 표준 박스 사용 (절대 에러 안 남)
    for node in st.session_state.nodes:
        parent_name = "최상위"
        if node['parent'] is not None:
            # 부모 이름 찾기
            p = next((n for n in st.session_state.nodes if n['id'] == node['parent']), None)
            if p: parent_name = p['text']
        
        # 박스 출력
        content = f"**[{node['code']}] {node['text']}** \n(출처: {parent_name})"
        
        if node['parent'] is None:
            st.success(content) # 중심 생각은 초록 박스
        else:
            # 계층 깊이에 따라 들여쓰기 효과
            indent = "　　" * (node['code'].count('-'))
            st.info(f"{indent} ↳ {content}") # 자식은 파란 박스

if st.sidebar.button("🧹 전체 초기화"):
    st.session_state.nodes = [{'id': 0, 'code': '1', 'text': '중심 생각', 'parent': None}]
    st.rerun()
