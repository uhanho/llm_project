from app import *
from prompt import *

def main():
    st_app = UserApp()
    st_app.initialize_screen()
    st_app.show_progress_bar()
    st_app.display_results(schedule)


if __name__ == "__main__":
    main()
