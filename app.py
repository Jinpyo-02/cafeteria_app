import streamlit as st
from supabase import create_client

st.set_page_config(page_title="식수 입력", layout="centered")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_ANON_KEY"]
)

st.title("구내식당 식수 입력")

with st.form("input_form", clear_on_submit=True):
    date = st.date_input("날짜")
    meal_type = st.selectbox("식사", ["breakfast", "lunch", "dinner"])
    served_count = st.number_input("실제 식수(명)", min_value=0, step=1)
    menu_main = st.text_input("메인 메뉴(선택)")
    note = st.text_area("특이사항(선택)")
    submitted = st.form_submit_button("저장하기")

if submitted:
    row = {
        "date": str(date),
        "meal_type": meal_type,
        "served_count": int(served_count),
        "menu_main": menu_main if menu_main else None,
        "note": note if note else None,
    }
    try:
        supabase.table("meal_records").insert(row).execute()
        st.success("저장 완료!")
    except Exception as e:
        st.error(f"저장 실패: {e}")

st.divider()

st.subheader("최근 입력 데이터")
try:
    data = (
        supabase.table("meal_records")
        .select("*")
        .order("date", desc=True)
        .limit(30)
        .execute()
    )
    st.dataframe(data.data, use_container_width=True)
except Exception as e:
    st.error(f"조회 실패: {e}")
