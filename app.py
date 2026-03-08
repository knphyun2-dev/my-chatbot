import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        # 노션 CSV의 한글 깨짐을 막는 가장 확실한 인코딩
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        # 모든 텍스트의 앞뒤 공백을 미리 제거
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except Exception as e:
        st.error(f"CSV 파일을 읽지 못했습니다: {e}")
        return None

df = load_data()

st.title("🚦 폴-신호등: 위기 시그널 포착")
user_input = st.text_input("상황을 입력하세요 (예: 돈 뺏겼어, 기프티콘)")

if user_input and df is not None:
    found = False
    # 사용자 입력어에서도 앞뒤 공백 제거
    user_query = user_input.strip()
    
    for index, row in df.iterrows():
        # 첫 번째 칸: 상황 구분, 두 번째 칸: 검색 키워드
        row_values = [str(val).strip() for val in row.values]
        # 키워드들을 콤마로 나누고 각각 공백 제거
        keywords = [k.strip() for k in row_values[1].split(',')]
        
        # 💡 핵심: 사용자가 입력한 문장에 키워드가 '포함'되어 있는지 확인
        if any(key in user_query for key in keywords if key): 
            st.markdown(f"### 🔍 시그널 포착: **{row_values[0]}**")
            
            # 여기에 아까 복사한 노션 링크를 넣으세요
            notion_link = "https://www.notion.so/31c2bcabaa8481bb8248f174fb2bd92c?source=copy_link"
            
            st.error("🚨 현재 상황은 **[빨간불: 위험]** 단계입니다.")
            st.link_button("👉 상세진단과 대응가이드 살펴보기", notion_link)
            found = True
            break

    if not found:
        st.info(f"'{user_query}'에 대한 시그널을 찾지 못했습니다. 단어를 바꿔서 검색해 보세요.")

