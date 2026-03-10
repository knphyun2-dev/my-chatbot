import streamlit as st
import pandas as pd

# 1. 페이지 설정 (아이콘을 사이렌 🚨으로 변경)
st.set_page_config(page_title="POL-시그널", page_icon="🚨", layout="centered")

# 디자인 개선 커스텀 CSS
st.markdown("""
    <style>
    .stAlert { margin-bottom: 20px; border-radius: 12px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; }
    hr { margin: 30px 0; }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        # keywords.csv 파일을 읽어오며 공백을 미리 제거합니다.
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        return df
    except Exception as e:
        st.error(f"⚠️ CSV 파일을 읽지 못했습니다. 파일명과 경로를 확인해주세요: {e}")
        return None

df = load_data()

# 3. 메인 화면
st.markdown('<p class="main-title">📈 POL-시그널</p>', unsafe_allow_html=True)
st.subheader("학생들의 시그널을 포착합니다.")
st.write("문장으로 입력하셔도 핵심 키워드를 찾아 시그널을 포착합니다.")

user_input = st.text_input("🔍 상황 입력", placeholder="예: 어제 학교 뒤에서 맞았다, 선배가 자꾸 돈을 빌려가요")

if user_input and df is not None:
    found_count = 0
    # 검색용 입력값 정제 (공백 제거 및 소문자화)
    clean_input = user_input.replace(" ", "").lower()
    
    # 4. 데이터베이스 전체 스캔 (행 단위)
    for index, row in df.iterrows():
        # 컬럼 인덱스 정의: 0: 상황구분, 1: 키워드검색, 2: 상태/위험도, 3: 링크
        category_name = str(row.iloc[0])
        raw_keywords = str(row.iloc[1]).split(',')
        keywords = [k.strip().lower() for k in raw_keywords if k.strip()]
        
        # [핵심 매칭 로직] 
        # 사용자의 문장에 키워드 중 하나라도 '포함'되어 있는지 확인
        # 예: 입력 "맞았다" -> 키워드 "맞았" 이 포함되어 있으므로 True
        is_match = any(key in clean_input for key in keywords)

        if is_match:
            found_count += 1
            
            with st.container():
                st.markdown(f"### 🔍 시그널 포착 #{found_count}: **{category_name}**")
                
                # 위험도에 따른 시각적 알림 (색상 매칭)
                status = str(row.iloc[2])
                if any(word in status for word in ["빨강", "위험", "🔴", "심각", "폭행", "사기"]):
                    st.error(f"🚨 **[위험 신호 포착]** {status}")
                elif any(word in status for word in ["노랑", "주의", "🟡", "경고", "징후"]):
                    st.warning(f"⚠️ **[주의 신호 포착]** {status}")
                elif any(word in status for word in ["초록", "안전", "🟢", "정상"]):
                    st.success(f"✅ **[정상 범위]** {status}")
                else:
                    st.info(f"📊 **분석 결과:** {status}")
                
                # 링크 버튼
                url = str(row.iloc[3]).strip()
                if url.startswith("http"):
                    st.link_button(f"📄 '{category_name}' 대처 가이드 보기", url)
                else:
                    st.caption("🔗 연결된 상세 가이드가 없습니다.")
                
                st.markdown("---")

    # 5. 결과 안내
    if found_count == 0:
        st.error(f"⚠️ '{user_input}'와(과) 관련된 명확한 위험 시그널이 발견되지 않았습니다.")
        st.info("단어 위주(예: 때림, 돈, 욕설)로 다시 입력하거나, 더 구체적으로 상황을 적어주세요.")
    else:
        st.toast(f"총 {found_count}개의 시그널을 분석했습니다.", icon="📈")

# 하단 안내
st.divider()
st.caption("🚨 긴급 상담이 필요하신가요? | 학교폭력 신고 117 | 청소년 상담 1388 | 범죄신고 112")
st.caption("본 서비스는 입력된 키워드를 기반으로 시나리오를 매칭하며, 실제 상담은 전문 기관(경찰, 학교 등)을 통해 진행하시기 바랍니다.")


