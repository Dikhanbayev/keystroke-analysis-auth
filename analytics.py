import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from record import start_record, stop_record
from analyse import analyse
from test import get_person_name, start_auth, stop_auth

def show_analytics():
    username = st.session_state.get('username')
    st.write(f"Добро пожаловать, {username}!")





    # Предполагается, что файлы данных хранятся в папке 'data' в поддиректории с именем пользователя
    user_data_dir = f"data\{username}.csv"

    if not os.path.exists(user_data_dir):
        st.error("Данные для данного пользователя отсутствуют.")
        return


    # Считаем, что работаем только с самым новым файлом

    userfile=f"data/{username}.csv"

    if os.path.exists(userfile):
        df = pd.read_csv(userfile)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[df['event'] == 'p']
        df['time_diff'] = df['time'].diff().dt.total_seconds()
        df = df.dropna(subset=['time_diff'])

        fig, ax = plt.subplots()
        ax.plot(df['time'], df['time_diff'], marker='o', linestyle='-')
        ax.set_xlabel('Время')
        ax.set_ylabel('Интервал между нажатиями (сек)')
        ax.set_title('График скорости печати')
        st.pyplot(fig)
        st.write(df)

    else:
        st.error(f"Файл {userfile} не найден. Пожалуйста, убедитесь, что файл находится в правильной папке.")




