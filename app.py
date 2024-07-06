import streamlit as st
from datetime import datetime
import time

class UserApp():
    def __init__(self):
        self.title = "Trip Planner ✈️"
        
        self.dest_msg = "Where do you want to go?"
        self.depart_msg = "Where do you depart from?"
        self.num_ppl_msg = "How many people are going?"
        
        self.start_date_msg = "Select the start date of travel:"
        self.end_date_msg = "Select the end data of travel:"
        
        self.pers_info_msg = "Please enter any personal information."
        
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
          <tr>
            <td>2일차</td>
            <td>2024-07-07</td>
            <td>
              <ul>
                <li>알카트라즈 섬 방문</li>
                <li>골든 게이트 브릿지 산책</li>
                <li>팔레 드 아트에서 예술 작품 감상</li>
              </ul>
            </td>
          </tr>
          <tr>
            <td>3일차</td>
            <td>2024-07-08</td>
            <td>
              <ul>
                <li>골든 게이트 공원에서 산책</li>
                <li>디영 박물관 방문</li>
                <li>롬바드 스트리트에서 사진 촬영</li>
              </ul>
            </td>
          </tr>
          <tr>
            <td>4일차</td>
            <td>2024-07-09</td>
            <td>
              <ul>
                <li>샌프란시스코 동물원 방문</li>
                <li>피어 39에서 물개 관찰</li>
                <li>소살리토 마을 방문</li>
              </ul>
            </td>
          </tr>
          <tr>
            <td>5일차</td>
            <td>2024-07-10</td>
            <td>
              <ul>
                <li>SFMOMA에서 예술 작품 감상</li>
                <li>트윈 픽스에서 전망 감상</li>
                <li>캐블카 타기</li>
              </ul>
            </td>
          </tr>
          <tr>
            <td>6일차</td>
            <td>2024-07-11</td>
            <td>
              <ul>
                <li>알카트라즈 섬 다시 방문</li>
                <li>골든 게이트 브릿지 다시 산책</li>
                <li>피어 39에서 식사</li>
              </ul> </td> </tr> <tr> <td>7일차</td> <td>2024-07-12</td> <td> <ul> <li>호텔 체크아웃</li> <li>샌프란시스코에서 출발</li> </ul> </td> </tr> </table>

        </body>
        </html>
        """
    
    def init_screen(self):
        st.set_page_config(page_title="Trip Planner", page_icon="✈️")
        
        st.title(self.title)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dest = st.text_input(self.dest_msg)
        with col2:
            depart = st.text_input(self.depart_msg)
        with col3:
            num_people = st.number_input(self.num_ppl_msg, min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(self.start_date_msg, min_value=datetime.today())
        with col2:
            end_date = st.date_input(self.end_date_msg, min_value=start_date)
        
        pers_info = st.text_area(self.pers_info_msg)
        
        if st.button("Submit"):
            self.show_progress_bar()
            self.display_results()
    
    def show_progress_bar(self):
        with st.spinner('Loading...'):
            for _ in range(100):
                time.sleep(0.02)
    
    def display_results(self):
        st.markdown(self.html_content, unsafe_allow_html=True)


def main():
    st_app = UserApp()
    st_app.init_screen()


if __name__ == "__main__":
    main()
