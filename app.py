import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="영업 이슈 리포트", layout="centered")
st.title("🚀 영업 이슈 리포트")

# 구글 스프레드시트 연결 함수 (Streamlit 공식 방식)
def connect_to_gsheet():
    if "gcp_service_account" not in st.secrets:
        st.error("Secrets 설정에서 [gcp_service_account] 섹션을 찾을 수 없습니다.")
        return None
        
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Streamlit Secrets 딕셔너리를 직접 전달 (Streamlit이 줄바꿈 자동 처리)
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], 
            scopes=scopes
        )
        client = gspread.authorize(creds)
        
        # 구글 시트 연결
        SPREADSHEET_ID = '1t1reQUHfw0K7BEzPcaxOaCtP8x--ATip7tGhGy11NTU'
        sheet = client.open_by_key(SPREADSHEET_ID).get_worksheet(0)
        return sheet
    except Exception as e:
        st.error(f"구글 시트 인증/연결 오류: {e}")
        return None

# UI 입력 폼
with st.form("issue_form", clear_on_submit=True):
    manager = st.radio("담당자", ["이광호", "문정수", "박원덕", "상담이슈"], horizontal=True)
    company_name = st.text_input("회사명", placeholder="회사명을 입력하세요")
    products = st.multiselect("가입 상품", ["위멤버스 프리미엄", "위멤버스 스탠다드", "세모리포트 플러스", "세모리포트 베이직", "링크패스", "경리나라T"])
    issue_detail = st.text_area("상세 이슈", height=200)
    submit_button = st.form_submit_button("이슈 등록 완료")

if submit_button:
    if not company_name.strip() or not products or not issue_detail.strip():
        st.warning("회사명, 상품, 상세 이슈 등 모든 항목을 입력해 주세요.")
    else:
        sheet = connect_to_gsheet()
        if sheet:
            try:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                product_list = ", ".join(products)
                sheet.append_row([now, manager, company_name.strip(), product_list, issue_detail])
                st.success("✅ 스프레드시트에 정상 등록되었습니다!")
                st.balloons()
            except Exception as e:
                st.error(f"데이터 저장 실패: {e}")
