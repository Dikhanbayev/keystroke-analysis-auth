import streamlit as st
from database import add_user, check_user
from record import start_record, stop_record
from analyse import analyse
from test import start_auth, stop_auth, get_person_name

import streamlit as st
from database import check_user, add_user
from record import start_record, stop_record
from analyse import analyse
from test import get_person_name, start_auth, stop_auth

import streamlit as st

def show_login_page():
    st.title("Вход в систему")
    login_username = st.text_input("Имя пользователя")
    login_password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        user = check_user(login_username, login_password)
        if user:
            st.session_state['username'] = user[0]
            st.session_state['init_typing_auth'] = True  # Добавляем состояние инициации аутентификации
            st.success("Учётные данные подтверждены. Нажмите 'Начать аутентификацию' для продолжения.")
        else:
            st.error("Неверное имя пользователя или пароль")

    if 'init_typing_auth' in st.session_state and st.session_state['init_typing_auth']:
        st.write("## Дополнительная аутентификация через стиль набора текста")
        if st.button("Начать авторизацию"):
            st.session_state['awaiting_typing_confirmation'] = True

    if 'awaiting_typing_confirmation' in st.session_state and st.session_state['awaiting_typing_confirmation']:
        auth_text = st.text_area("Введите текст для аутентификации:")
        if st.button("Подтвердить текст"):
            if "hello" in auth_text.lower():
                st.session_state['logged_in'] = True
                st.experimental_rerun()
            else:
                st.error("Аутентификация не пройдена, повторите попытку еще раз")
                del st.session_state['awaiting_typing_confirmation']
                del st.session_state['init_typing_auth']

    if st.button("Нет аккаунта? Зарегистрируйтесь"):
        st.session_state['show_register'] = True
        st.experimental_rerun()

    if st.button("Вернуться на начальную страницу"):
        # Очистка всех данных сессии
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
def show_register_page():
    st.title("Регистрация")
    reg_username = st.text_input("Выберите имя пользователя", key="reg_username")
    reg_password = st.text_input("Выберите пароль", type="password", key="reg_password")

    if st.button("Продолжить"):
        st.session_state['username_temp'] = reg_username
        st.session_state['password_temp'] = reg_password
        st.session_state['show_typing_style'] = True
        st.experimental_rerun()

    if 'show_typing_style' in st.session_state and st.session_state['show_typing_style']:
        st.write("## Record typing style")
        st.text_area(
            "Please type the following text: *The quick brown fox jumps over the lazy dog.*",
            height=100,
        )

        if st.button("Start recording"):
            start_auth()
            start_record()
            st.session_state['recording'] = True

        if st.button("Stop recording"):
            stop_record(st.session_state['username_temp'])
            st.session_state['recording'] = False
            analyse()
            add_user(st.session_state['username_temp'], st.session_state['password_temp'])
            st.success("Регистрация прошла успешно!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = st.session_state['username_temp']
            st.experimental_rerun()

    if st.button("Уже есть аккаунт? Войдите"):
        st.session_state['show_register'] = False
        st.experimental_rerun()

# Основной интерфейс
if 'show_register' in st.session_state and st.session_state['show_register']:
    show_register_page()
else:
    show_login_page()
