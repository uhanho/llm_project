import streamlit as st
from datetime import datetime
import time
import pandas as pd
import prompt

class UserApp():
    def __init__(self):
        self.title = "여행 플래너 ✈️"
    
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
                    self.show_progress_bar()
                    self.display_results(dest, depart, num_people, start_date, end_date, pers_info)
            else:
                st.form_submit_button("제출", disabled=False)
    
    def show_progress_bar(self):
        progress_text = "여행을 계획하고 있어요, 잠시만 기다려주세요!"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()
    
    def display_results(self, dest, depart, num_people, start_date, end_date, pers_info):
        # Create a list of dictionaries to store the plan data in a structured format
        schedule = prompt.prompt_create(dest, depart, num_people, start_date, end_date, pers_info)
        
        plan_data = []
        is_date = set()
        for day_plan in schedule:
            date, activities = day_plan
            for time, activity in activities:
                if date not in is_date:
                    plan_data.append({"Date": date, "Time": time, "Activity": activity})
                    is_date.add(date)
                else:
                    plan_data.append({"Date": "", "Time": time, "Activity": activity})
        
        # Convert the list of dictionaries into a DataFrame
        plan_df = pd.DataFrame(plan_data)
        
        # Display the DataFrame using st.dataframe for a more interactive table
        st.dataframe(plan_df, hide_index=True)

def main():
    st_app = UserApp()
    st_app.initialize_screen()


if __name__ == "__main__":
    main()
