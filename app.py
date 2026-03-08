import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="POL-신호등:시그널 포착", page_icon="🚦", layout="centered")

# 디자인 개선 커스텀 CSS
st.markdown("""
    <style>
    .stAlert { margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    hr { margin: 30px 0; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"⚠️ CSV 파일을 읽지 못했습니다: {e}")
        return None

df = load_data()

# 3. 메인 화면
st.title("🚦 POL-신호등")
st.subheader("학생들의 시그널을 포착합니다.")
st.write("관련된 상황이 여러 개일 경우 모두 표시됩니다.")

user_input = st.text_input("상황 입력 (예: 돈, 생일선물, 킥보드, 폭력)", placeholder="키워드를 입력하고 엔터를 치세요...")

if user_input and df is not None:
    found_count = 0
    user_query = user_input.replace(" ", "") # 공백 제거 후 검색
    
    # 4. 데이터베이스 전체 스캔 (break 없이 진행)
    for index, row in df.iterrows():
        row_list = row.tolist()
        keywords = [k.strip() for k in str(row_list[1]).split(',')]
        
        # 키워드 매칭 확인
        if any(key in user_query for key in keywords if key):
            found_count += 1
            
            # 검색 결과 레이아웃 시작
            with st.container():
                st.markdown(f"### 🔍 포착된 시그널 #{found_count}: **{row_list[0]}**")
                
                # 신호등 상태 표시
                status = str(row_list[2])
                if any(word in status for word in ["빨강", "위험", "🔴"]):
                    st.error(f"🚨 **[위험 상황]** {status}")
                elif any(word in status for word in ["노랑", "주의", "🟡"]):
                    st.warning(f"⚠️ **[주의 상황]** {status}")
                elif any(word in status for word in ["초록", "안전", "🟢"]):
                    st.success(f"🟢 **[안전/일반]** {status}")
                else:
                    st.info(f"📊 **상태:** {status}")
                
                # 링크 버튼
                url = str(row_list[3]).strip()
                if url.startswith("http"):
                    st.link_button(f"🔗 '{row_list[0]}' 상세 진단 및 가이드 바로가기", url)
                else:
                    st.caption("연결된 상세 페이지가 없습니다.")
                
                st.markdown("---") # 항목 간 구분선

    # 5. 검색 결과가 하나도 없을 때
    if found_count == 0:
        st.warning(f"🧐 '{user_input}'와(과) 관련된 명확한 시그널을 찾지 못했습니다.")
        st.info("핵심 단어(예: 돈, 뺏, 박제, 폰) 위주로 다시 검색해 보세요.")
    else:
        st.caption(f"총 {found_count}개의 관련 시그널을 찾았습니다.")

# 하단 안내
st.divider()
st.caption("본 서비스는 입력된 키워드를 기반으로 시나리오를 매칭하며, 실제 상담은 전문 기관(경찰, 학교 등)을 통해 진행하시기 바랍니다.")

