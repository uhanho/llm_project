import streamlit as st
from datetime import datetime
import time

class UserApp():
    def __init__(self):
        self.title = "Trip Planner ✈️"
        
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
        st.set_page_config(page_title="Trip Planner", page_icon="✈️")
        st.title(self.title)
        
        with st.form("user_form"):
            st.header("Trip Information")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                dest = st.text_input("Where do you want to go?")
            with col2:
                depart = st.text_input("Where do you depart from?")
            with col3:
                num_people = st.number_input("How many people are going?", min_value=1, step=1)
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Select the start date of travel:", min_value=datetime.today())
            with col2:
                end_date = st.date_input("Select the end data of travel:", min_value=start_date)

            pers_info_msg = "Please enter your personal information, " \
                "including personal preferences or things to be considered."
            
            pers_info = st.text_area(pers_info_msg)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                self.show_progress()
                self.display_results()
    
    def show_progress(self):
        with st.spinner('Loading...'):
            for _ in range(100):
                time.sleep(0.02)
    
    def display_results(self):
        st.markdown(self.html_content, unsafe_allow_html=True)


def main():
    st_app = UserApp()
    st_app.initialize_screen()


if __name__ == "__main__":
    main()
