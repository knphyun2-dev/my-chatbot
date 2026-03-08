import streamlit as st
import pandas as pd

# 1. 데이터베이스(CSV) 불러오기
# 노션에서 내보낸 CSV 파일 이름을 'keywords.csv'라고 가정합니다.
@st.cache_data
def load_data():
    df = pd.read_csv('keywords.csv') 
    return df

df = load_data()

st.title("🚦 폴-신호등: 위기 시그널 포착")
st.write("지금 겪고 있는 상황을 편하게 입력해 보세요.")

# 2. 사용자 입력창
user_input = st.text_input("검색어 예: 돈 뺏겼어, 기프티콘 보내래, 킥보드 타도 돼?")

if user_input:
    found = False
    
    # 3. 데이터베이스 훑기 (유사어 그룹화 로직 반영)
    for index, row in df.iterrows():
        # '검색 키워드' 열에 있는 단어들을 콤마로 분리
        keywords = [k.strip() for k in str(row['검색 키워드']).split(',')]
        
        # 사용자가 입력한 문장에 키워드 중 하나라도 포함되어 있는지 확인
        if any(key in user_input for key in keywords):
            st.markdown(f"### 🔍 시그널 포착: **{row['키워드검색']}**")
            
            # 신호등 상태에 따른 알림 색상 변경
            status = row['신호등 상태']
            if "🔴" in status or "위험" in status:
                st.error(f"🚨 현재 상황은 **[빨간불: 위험]** 단계입니다. 범죄 가능성이 높아요.")
            elif "🟡" in status or "주의" in status:
                st.warning(f"⚠️ 현재 상황은 **[노란불: 주의]** 단계입니다. 도움이 필요해요.")
            else:
                st.success(f"🟢 현재 상황은 **[초록불: 안전]** 단계입니다.")
            
            # 연결 링크 버튼
            st.link_button("👉 경찰관의 상세 진단서 확인하기", row['https://www.notion.so/31c2bcabaa8481bb8248f174fb2bd92c?source=copy_link'])
            found = True
            break
            
    if not found:
        st.info("입력하신 내용에 대한 시그널을 찾지 못했습니다. 핵심 단어(돈, 사진, 킥보드 등) 위주로 다시 입력해 보시겠어요?")
