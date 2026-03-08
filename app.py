import streamlit as st
import pandas as pd

# 1. 데이터베이스(CSV) 불러오기
@st.cache_data
def load_data():
    try:
        # 한글 깨짐 방지를 위해 utf-8-sig 사용
        df = pd.read_csv('keywords.csv', encoding='utf-8-sig')
        # 열 이름의 앞뒤 공백 제거 (매우 중요)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

st.title("🚦 폴-신호등: 위기 시그널 포착")
st.write("지금 겪고 있는 상황을 편하게 입력해 보세요.")

user_input = st.text_input("검색어 예: 돈 뺏겼어, 기프티콘 보내래, 킥보드 타도 돼?")

if user_input and df is not None:
    found = False
    
    # 데이터베이스 한 줄씩 검사
    for index, row in df.iterrows():
        # 열의 개수가 부족할 경우를 대비해 안전하게 데이터 추출
        row_list = row.tolist()
        
        # 최소 2개 이상의 열이 있어야 검사 가능 (상황구분, 키워드)
        if len(row_list) < 2:
            continue
            
        # 키워드는 보통 2번째 열(index 1)에 있다고 가정
        raw_keywords = str(row_list[1])
        keywords = [k.strip() for k in raw_keywords.split(',')]
        
        if any(key in user_input for key in keywords):
            # 1. 상황 명칭 출력 (첫 번째 열)
            st.markdown(f"### 🔍 시그널 포착: **{row_list[0]}**")
            
            # 2. 신호등 상태 출력 (세 번째 열이 있다면 사용)
            if len(row_list) >= 3:
                status = str(row_list[2])
                if "🔴" in status or "위험" in status:
                    st.error(f"🚨 현재 상황은 **[빨간불: 위험]** 단계입니다. 범죄 가능성이 높아요.")
                elif "🟡" in status or "주의" in status:
                    st.warning(f"⚠️ 현재 상황은 **[노란불: 주의]** 단계입니다. 도움이 필요해요.")
                else:
                    st.success(f"🟢 현재 상황은 **[초록불: 안전]** 단계입니다.")
            
            # 3. 링크 버튼 생성 (마지막 열에 URL이 있다고 가정)
            # URL처럼 보이는 데이터를 자동으로 찾아서 연결합니다.
            url = ""
            for item in reversed(row_list): # 뒤에서부터 URL 찾기
                item_str = str(item).strip()
                if item_str.startswith("http"):
                    url = item_str
                    break
            
            if url:
                st.link_button("👉 경찰관의 상세 진단서 확인하기", url)
            else:
                st.info("⚠️ 연결할 상세 페이지 링크를 찾지 못했습니다. CSV 파일을 확인해 주세요.")
                
            found = True
            break
            
    if not found:
        st.info("입력하신 내용에 대한 시그널을 찾지 못했습니다. 핵심 단어 위주로 다시 검색해 보세요.")
