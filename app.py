import streamlit as st
import pandas as pd

# 1. 데이터베이스(CSV) 불러오기
@st.cache_data
def load_data():
    try:
        # 한글 깨짐 방지를 위해 encoding 추가
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

st.title("🚦 폴-신호등: 위기 시그널 포착")
st.write("지금 겪고 있는 상황을 편하게 입력해 보세요.")

# 2. 사용자 입력창
user_input = st.text_input("검색어 예: 돈 뺏겼어, 기프티콘 보내래, 킥보드 타도 돼?")

if user_input and df is not None:
    found = False
    
    # 3. 열 이름 대신 '순서(iloc)'로 데이터 매칭
    # row.iloc[0]: 상황 구분 | row.iloc[1]: 검색 키워드 | row.iloc[2]: 신호등 상태 | row.iloc[3]: 연결 페이지
    for index, row in df.iterrows():
        # 키워드가 담긴 두 번째 열(index 1) 처리
        raw_keywords = str(row.iloc[1])
        keywords = [k.strip() for k in raw_keywords.split(',')]
        
        if any(key in user_input for key in keywords):
            st.markdown(f"### 🔍 시그널 포착: **{row.iloc[0]}**")
            
            # 신호등 상태에 따른 색상 처리 (세 번째 열 index 2)
            status = str(row.iloc[2])
            if "🔴" in status or "위험" in status:
                st.error(f"🚨 현재 상황은 **[빨간불: 위험]** 단계입니다. 범죄 가능성이 높아요.")
            elif "🟡" in status or "주의" in status:
                st.warning(f"⚠️ 현재 상황은 **[노란불: 주의]** 단계입니다. 도움이 필요해요.")
            else:
                st.success(f"🟢 현재 상황은 **[초록불: 안전]** 단계입니다.")
            
            # 연결 링크 버튼 (네 번째 열 index 3)
            # URL이 들어있는 칸을 정확히 연결합니다.
            st.link_button("👉 경찰관의 상세 진단서 확인하기", str(row.iloc[3]))
            found = True
            break
            
    if not found:
        st.info("입력하신 내용에 대한 시그널을 찾지 못했습니다. 핵심 단어 위주로 다시 검색해 보세요.")
