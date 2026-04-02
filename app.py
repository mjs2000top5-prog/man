import streamlit as st
import requests

# ==========================================
# 1. 구글 설문지 설정 (GCP 인증 필요 없음)
# ==========================================
# 구글 설문지의 '답변 전송' 주소 (viewform 대신 formResponse로 끝남)
FORM_URL = "https://docs.google.com/forms/d/e/여러분의_설문지_ID/formResponse"

# 설문지의 각 항목 ID (예시입니다. 실제 ID로 교체 필요)
ENTRY_MANAGER = "entry.1111111"  # 담당자
ENTRY_PRODUCT = "entry.2222222"  # 상품명
ENTRY_ISSUE = "entry.3333333"    # 상세 이슈

# ==========================================
# 2. UI 구성
# ==========================================
st.set_page_config(page_title="영업 이슈 등록 (간편형)", layout="centered")

st.title("🚀 영업 이슈 리포트")
st.write("인증 파일 없이 설문지 경로를 통해 안전하게 등록됩니다.")

with st.form("issue_form", clear_on_submit=True):
    manager = st.radio("담당자", ["이광호", "문정수", "박원덕"], horizontal=True)
    
    products = st.multiselect(
        "가입(예정/실패) 상품",
        ["위멤버스 프리미엄", "위멤버스 스탠다드", "세모리포트 플러스", "세모리포트 베이직", "링크패스", "경리나라T"]
    )
    
    issue_detail = st.text_area("상세 이슈", placeholder="내용을 입력하세요.", height=150)
    submit_button = st.form_submit_button("이슈 등록 완료")

# ==========================================
# 3. 데이터 전송 (Requests 방식)
# ==========================================
if submit_button:
    if not products or not issue_detail.strip():
        st.warning("내용을 모두 입력해 주세요.")
    else:
        # 설문지로 보낼 데이터 구성
        data = {
            ENTRY_MANAGER: manager,
            ENTRY_PRODUCT: ", ".join(products),
            ENTRY_ISSUE: issue_detail
        }
        
        try:
            # 설문지로 데이터 POST 전송
            response = requests.post(FORM_URL, data=data)
            if response.status_code == 200:
                st.success("✅ 성공적으로 저장되었습니다!")
                st.balloons()
            else:
                st.error("전송에 실패했습니다. 설문지 설정을 확인해주세요.")
        except Exception as e:
            st.error(f"오류 발생: {e}")