import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        # 노션 CSV의 한글 깨짐 방지
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        return df
    except Exception as e:
        st.error(f"CSV 파일을 읽지 못했습니다: {e}")
        return None

df = load_data()

st.title("🚦 폴-신호등: 위기 시그널 포착")
user_input = st.text_input("검색어 예: 돈 뺏겼어, 기프티콘, 삥")

if user_input and df is not None:
    found = False
    
    for index, row in df.iterrows():
        # 첫 번째 칸은 상황(돈 문제 등), 두 번째 칸은 키워드라고 가정합니다.
        row_values = [str(val).strip() for val in row.values]
        keywords = [k.strip() for k in row_values[1].split(',')]
        
        if any(key in user_input for key in keywords):
            st.markdown(f"### 🔍 시그널 포착: **{row_values[0]}**")
            
            # 🔗 여기에 사용자님의 노션 '돈 문제' 페이지 주소를 넣으세요!
            notion_link = "https://www.notion.so/31c2bcabaa8481bb8248f174fb2bd92c?source=copy_link"
            
            if "돈" in row_values[0] or "갈취" in row_values[0]:
                st.error("🚨 현재 상황은 **[빨간불: 위험]** 단계입니다.")
                st.link_button("👉 경찰관의 돈 문제 대응 가이드 보기", notion_link)
                found = True
                break

    if not found:
        st.info("시그널을 찾지 못했습니다. '돈', '뺏겼어' 등 핵심 단어로 다시 검색해보세요.")
