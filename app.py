import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

st.set_page_config(page_title="영업 이슈 리포트", layout="centered")
st.title("🚀 영업 이슈 리포트")

# 구글 스프레드시트 연결 함수
def connect_to_gsheet():
    if "JSON_DATA" not in st.secrets:
        st.error("Secrets 설정에서 'JSON_DATA' 키를 찾을 수 없습니다.")
        return None
        
    try:
        # Secrets에서 JSON 텍스트 파싱
        json_data = st.secrets["JSON_DATA"]
        creds_info = json.loads(json_data)
        
        # private_key 내부의 이스케이프 기호(\n)를 실제 줄바꿈 문자로 변환 (JWT 서명 오류 방지)
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
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
    company_name = st.text_input("회사명", placeholder="회사명을 입력하세요")  # 👈 회사명 입력 칸 추가
    products = st.multiselect("가입 상품", ["위멤버스 프리미엄", "위멤버스 스탠다드", "세모리포트 플러스", "세모리포트 베이직", "링크패스", "경리나라T"])
    issue_detail = st.text_area("상세 이슈", height=200)
    submit_button = st.form_submit_button("이슈 등록 완료")

if submit_button:
    # 필수 입력 값 유효성 검사 (회사명 검증 추가)
    if not company_name.strip() or not products or not issue_detail.strip():
        st.warning("회사명, 상품, 상세 이슈 등 모든 항목을 입력해 주세요.")
    else:
        sheet = connect_to_gsheet()
        if sheet:
            try:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                product_list = ", ".join(products)
                # 시트에 저장되는 데이터: [일시, 담당자, 회사명, 상품목록, 상세이슈]
                sheet.append_row([now, manager, company_name.strip(), product_list, issue_detail])
                st.success("✅ 스프레드시트에 정상 등록되었습니다!")
                st.balloons()
            except Exception as e:
                st.error(f"데이터 저장 실패: {e}")
