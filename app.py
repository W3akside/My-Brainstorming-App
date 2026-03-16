import streamlit as st
from streamlit_echarts import st_echarts

# 1. 페이지 설정 (오타 수정 완료!)
st.set_page_config(page_title="MindMap Board", layout="wide")
st.title("📍 선으로 연결되는 파생 보드")

# 2. 데이터 초기화
if 'nodes' not in st.session_state:
    st.session_state.nodes = [{"name": "점심메뉴", "x": 300, "y": 300}]
    st.session_state.links = []

# 3. 사이드바 제어
with st.sidebar:
    st.header("⚙️ 관리창")
    
    # 노드 추가
    with st.expander("➕ 아이디어 가지치기", expanded=True):
        parent_name = st.selectbox("어디서 뻗어나갈까요?", [n['name'] for n in st.session_state.nodes])
        child_name = st.text_input("새 아이디어 이름")
        if st.button("🌱 가지 추가") and child_name:
            # 부모 위치 찾기
            p_node = next(n for n in st.session_state.nodes if n['name'] == parent_name)
            # 새 노드 추가 (부모 근처에 생성)
            st.session_state.nodes.append({
                "name": child_name, 
                "x": p_node['x'] + 100, 
                "y": p_node['y'] + 100
            })
            # 연결선 추가
            st.session_state.links.append({"source": parent_name, "target": child_name})
            st.rerun()

    # 위치 조정 및 삭제
    st.divider()
    for i, node in enumerate(st.session_state.nodes):
        with st.expander(f"📦 {node['name']}"):
            st.session_state.nodes[i]['x'] = st.slider(f"{node['name']} X 위치", 0, 1000, node['x'], key=f"x_{i}")
            st.session_state.nodes[i]['y'] = st.slider(f"{node['name']} Y 위치", 0, 800, node['y'], key=f"y_{i}")
            if st.button(f"🗑️ 삭제", key=f"del_{i}"):
                st.session_state.nodes.pop(i)
                # 연결선에서도 삭제
                st.session_state.links = [l for l in st.session_state.links if l['source'] != node['name'] and l['target'] != node['name']]
                st.rerun()

# 4. 메인 캔버스 (ECharts 활용)
options = {
    "title": {"text": ""},
    "tooltip": {},
    "series": [
        {
            "type": "graph",
            "layout": "none", # 자유 배치를 위해 none 설정
            "symbolSize": 50,
            "roam": True,
            "label": {"show": True, "position": "inside", "fontSize": 14},
            "edgeSymbol": ["circle", "arrow"],
            "edgeSymbolSize": [4, 10],
            "data": st.session_state.nodes,
            "links": st.session_state.links,
            "lineStyle": {"opacity": 0.9, "width": 2, "curveness": 0},
            "itemStyle": {"color": "#ffffff", "borderColor": "#0052cc", "borderWidth": 2}
        }
    ],
}

st_echarts(options=options, height="700px")
