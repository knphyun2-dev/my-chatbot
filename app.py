import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="POL-시그널", page_icon="🚦", layout="centered")

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
        # keywords.csv 파일이 같은 경로에 있어야 합니다.
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        # 데이터 공백 제거 및 정리
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"⚠️ CSV 파일을 읽지 못했습니다: {e}")
        return None

df = load_data()

# 3. 메인 화면
st.title("🚦 POL-시그널")
st.subheader("학생들의 시그널을 포착합니다.")
st.write("문장으로 입력하셔도 핵심 키워드를 찾아 시그널을 포착합니다.")

user_input = st.text_input("🔍 상황 입력 (예: 자꾸 돈을 달라고 해요, 카톡 감옥으로 괴롭혀요)", placeholder="여기에 상황을 설명해 보세요...")

if user_input and df is not None:
    found_count = 0
    
    # [검색 로직 개선] 
    # 1. 공백 제거 버전 (키워드가 문장 사이에 숨어있을 때 대비)
    user_query_no_space = user_input.replace(" ", "").lower()
    # 2. 단어별 분리 버전 (서술형 문장에서 핵심 단어 추출 대비)
    user_words = user_input.lower().split()
    
    # 4. 데이터베이스 전체 스캔
    for index, row in df.iterrows():
        row_list = row.tolist()
        # CSV 구조: [0]상황명, [1]키워드들(쉼표구분), [2]상태/위험도, [3]링크
        raw_keywords = str(row_list[1]).split(',')
        keywords = [k.strip().lower() for k in raw_keywords if k.strip()]
        
        # 매칭 확인 (두 가지 방식 중 하나라도 걸리면 매칭)
        is_match = False
        
        # 방식 1: 사용자의 전체 문장(공백제거) 안에 키워드가 포함되어 있는가? (예: "폭행" in "학교폭력을당했어요")
        if any(key in user_query_no_space for key in keywords):
            is_match = True
            
        # 방식 2: 사용자가 입력한 개별 단어들 속에 키워드가 들어있는가? (예: "폭행" in "폭행을")
        if not is_match:
            for word in user_words:
                if any(key in word for key in keywords):
                    is_match = True
                    break

        if is_match:
            found_count += 1
            
            # 검색 결과 레이아웃
            with st.container():
                st.markdown(f"### 🔍 포착된 시그널 #{found_count}: **{row_list[0]}**")
                
                status = str(row_list[2])
                if any(word in status for word in ["빨강", "위험", "🔴", "심각"]):
                    st.error(f"🚨 **[위험 상황]** {status}")
                elif any(word in status for word in ["노랑", "주의", "🟡", "경고"]):
                    st.warning(f"⚠️ **[주의 상황]** {status}")
                elif any(word in status for word in ["초록", "안전", "🟢"]):
                    st.success(f"🟢 **[안전/일반]** {status}")
                else:
                    st.info(f"📊 **상태:** {status}")
                
                url = str(row_list[3]).strip()
                if url.startswith("http"):
                    st.link_button(f"🔗 '{row_list[0]}' 상세 진단 및 가이드 바로가기", url)
                else:
                    st.caption("연결된 상세 페이지가 없습니다.")
                
                st.markdown("---")

    # 5. 검색 결과가 하나도 없을 때
    if found_count == 0:
        st.warning(f"🧐 '{user_input}'와(과) 관련된 명확한 시그널을 찾지 못했습니다.")
        st.info("단어 위주로(예: 돈, 킥보드, 도박) 짧게 입력하시면 더 정확한 검색이 가능합니다.")
    else:
        st.caption(f"총 {found_count}개의 관련 시그널을 찾았습니다.")

# 하단 안내
st.divider()
st.caption("본 서비스는 입력된 키워드를 기반으로 시나리오를 매칭하며, 실제 상담은 전문 기관(경찰, 학교 등)을 통해 진행하시기 바랍니다.")


