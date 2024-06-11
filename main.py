import streamlit as st
from auth import show_login_page, show_register_page
from analytics import show_analytics
from database import create_table

def main():
    create_table()  # Создание таблицы базы данных, если необходимо
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        if 'show_register' in st.session_state and st.session_state['show_register']:
            show_register_page()
        else:
            show_login_page()
    else:
        st.title(f"Добро пожаловать, {st.session_state['username']}!")
        show_analytics()  # Показать аналитическую часть приложения
        if st.button("Выйти"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()
