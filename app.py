import streamlit as st
import pandas as pd

# 1. 페이지 설정 (아이콘은 사이렌 🚨 고정)
st.set_page_config(page_title="POL-시그널", page_icon="🚨", layout="centered")

# 디자인 개선 커스텀 CSS
st.markdown("""
    <style>
    .stAlert { margin-bottom: 20px; border-radius: 12px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    hr { margin: 30px 0; }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 로드 함수 (데이터 정제)
@st.cache_data
def load_data():
    try:
        # utf-8-sig로 한글 깨짐 방지
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        # 결측치를 빈 문자열로 처리하여 오류 방지
        df = df.fillna("")
        # 데이터의 모든 공백을 미리 제거하여 검색 효율 극대화
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"⚠️ CSV 로드 실패: {e}")
        return None

df = load_data()

# 3. 메인 화면
st.markdown('<p class="main-title">🚨 POL-시그널</p>', unsafe_allow_html=True)
st.subheader("학생들의 시그널을 포착합니다.")

user_input = st.text_input("🔍 상황 입력", placeholder="예: 어제 학교 뒤에서 맞았다, 돈을 뺏겼다")

if user_input and df is not None:
    found_count = 0
    # [핵심] 사용자의 입력 문장에서 공백을 제거하고 소문자로 변환하여 검색 준비
    clean_input = user_input.replace(" ", "").lower()
    
    # 4. CSV 데이터 스캔
    for index, row in df.iterrows():
        category = str(row.iloc[0]) # 상황구분
        # 키워드 필드(두 번째 열)를 가져와 쉼표로 분리
        raw_keywords = str(row.iloc[1]).split(',')
        keywords_list = [k.strip().lower() for k in raw_keywords if k.strip()]
        
        # [강력한 검색 로직] 
        # 사용자의 문장(clean_input) 안에 CSV 키워드가 '포함'되어 있는지 확인
        # "맞았다" 입력 시 "맞았" 키워드가 문장에 포함되어 있으므로 매칭 성공
        is_match = any(key in clean_input for key in keywords_list)

        if is_match:
            found_count += 1
            with st.container():
                st.markdown(f"### 🔍 시그널 포착 #{found_count}: **{category}**")
                
                status_text = str(row.iloc[2]) # 상태/위험도
                # 위험도에 따라 상자 색상 변경
                if any(w in status_text for w in ["빨강", "위험", "🔴", "심각"]):
                    st.error(f"🚨 **[위험 신호]** {status_text}")
                elif any(w in status_text for w in ["노랑", "주의", "🟡", "경고"]):
                    st.warning(f"⚠️ **[주의 신호]** {status_text}")
                else:
                    st.info(f"📊 **분석 결과:** {status_text}")
                
                # 링크 버튼
                link_url = str(row.iloc[3]).strip()
                if link_url.startswith("http"):
                    st.link_button(f"🔗 '{category}' 상세 진단 및 대응 방법 바로가기", link_url)
                
                st.markdown("---")

    # 결과가 없을 경우
    if found_count == 0:
        st.warning(f"🧐 '{user_input}'와(과) 관련된 시그널을 찾지 못했습니다.")
        st.info("단어 위주(예: 맞았, 때림, 돈, 인스타)로 입력해 보세요.")

# 5. 법적 고지 (슬림 및 시인성 최적화)
st.divider()

# 캡션(작은 글씨)으로 법적 면책 조항 구성
st.caption("🚨 이용 안내 및 법적 고지")
st.caption("""
본 결과는 입력된 키워드를 기반으로 한 단순 참고용 데이터이며, 실제 법정 판결이나 전문 자문을 대신할 수 없습니다.  
개별 사안에 대한 정확한 판단과 조치는 반드시 경찰(112), 학교폭력 신고센터(117) 등 전문 기관을 통해 진행하시기 바랍니다.
""")

# 상담 전화번호는 조금 더 눈에 띄게 배치
st.info("📞 **도움이 필요할 때:** 학교폭력 117 | 범죄신고 112 | 청소년상담 1388")



