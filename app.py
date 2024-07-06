import streamlit as st
from datetime import datetime
import time

class UserApp():
    def __init__(self):
        self.title = "여행 플래너 ✈️"
        
        self.html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>샌프란시스코 여행 계획표</title>
        </head>
        <body>

        <h2>샌프란시스코 여행 계획표</h2>

        <table border="1">
        <tr>
            <th>일</th>
            <th>요일</th>
            <th>일정</th>
        </tr>
        <tr>
            <td>1일차</td>
            <td>2024-07-06</td>
            <td>
                <ul>
                  <li>샌프란시스코 도착</li>
                  <li>호텔 체크인</li>
                  <li>피셔맨스 워프에서 식사</li>
                  <li>피어 39에서 산책</li>
                </ul>
            </td>
        </tr>
        </body>
        </html>
        """
    
    def initialize_screen(self):
        st.set_page_config(page_title="여행 플래너", page_icon="✈️")
        st.title(self.title)
        
        with st.form("user_form"):
            st.header("여행 정보")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                dest = st.text_input("어디로 가시나요?")
            with col2:
                depart = st.text_input("어디서 출발하시나요?")
            with col3:
                num_people = st.number_input("몇 명이서 가시나요?", min_value=1, step=1)
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("출발 날짜를 선택해주세요:", min_value=datetime.today())
            with col2:
                end_date = st.date_input("종료 날짜를 선택해주세요:", min_value=start_date)

            pers_info_msg = "원하는 여행에 대해 적어주세요! " \
                "(개인 취향을 모두 고려하여 여행을 계획해드립니다.)"
            
            pers_info = st.text_area(pers_info_msg)
            
            st.markdown("<p style='font-size:12px; font-style:italic;'>제출을 위해서는 모든 내용을 입력하셔야 합니다.</p>", unsafe_allow_html=True)
            
            if dest and depart and num_people and start_date and end_date and pers_info:
                if st.form_submit_button("제출"):
                    self.show_progress()
                    self.display_results()
            else:
                st.form_submit_button("제출", disabled=False)
    
    def show_progress(self):
        progress_text = "여행을 계획하고 있어요, 잠시만 기다려주세요!"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
    
    def display_results(self):
        st.markdown(self.html_content, unsafe_allow_html=True)
        


def main():
    st_app = UserApp()
    st_app.initialize_screen()


if __name__ == "__main__":
    main()
