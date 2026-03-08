import streamlit as st

# 페이지 설정 (아이콘과 제목)
st.set_page_config(page_title="위기 상황 대응 챗봇", page_icon="🛡️")

st.markdown("### 🔍 궁금한 키워드를 입력하세요")
st.caption("예: 돈, 킥보드, 협박, 사진, 뺑소니")

# 검색창 생성
keyword = st.text_input("검색어 입력", placeholder="여기에 입력하세요...", label_visibility="collapsed")

# 🔗 여기에 복사한 노션 링크를 붙여넣으세요!
notion_links = {
    "돈": "https://www.notion.so/31c2bcabaa848125a8c7c59385bd683d?source=copy_link",
    "빌려": "https://www.notion.so/your-page-id-돈문제",
    "갈취": "https://www.notion.so/your-page-id-돈문제",
    "킥보드": "https://www.notion.so/your-page-id-교통범죄",
    "운전": "https://www.notion.so/your-page-id-교통범죄",
    "면허": "https://www.notion.so/your-page-id-교통범죄",
    "사진": "https://www.notion.so/your-page-id-성범죄",
    "협박": "https://www.notion.so/your-page-id-성범죄",
    "유포": "https://www.notion.so/your-page-id-성범죄"
}

if keyword:
    found = False
    # 키워드가 포함되어 있는지 확인
    for key, link in notion_links.items():
        if key in keyword:
            st.success(f"'{key}' 관련 대응 가이드를 찾았습니다!")
            st.link_button("👉 상세 페이지로 이동하기", link)
            found = True
            break
    
    if not found:
        st.error("앗! 검색 결과가 없어요. '돈', '사진', '면허' 등으로 검색해보세요.")