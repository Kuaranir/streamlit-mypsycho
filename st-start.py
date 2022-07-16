import streamlit as st
import numpy as np
import pandas as pd

from data_preprocessing import preprocces

st.title('Мой психолог: ИИ')
st.image(
    'https://newizv.ru/attachments/27e959e9382672f8826de4367888b0a9a95ea136/store/fill/360/200/f0e21b931e498bcc91c2e33905fbb228fc31cf3cdda2b398d07fe3e6790f/f0e21b931e498bcc91c2e33905fbb228fc31cf3cdda2b398d07fe3e6790f.jpg',
    caption='Исследование на полиграфе')


def load_data():
    uploaded_file = st.file_uploader(label='Загрузите данные датчиков полиграфа в виде CSV-файла:')
    try:
        return pd.read_excel(uploaded_file)
    except Exception:
        return None


data = load_data()
result = st.button('Загрузить данные')

# Загрузка ранее обученной модели (нейросети с весами):
model = tf.keras.models.load_model('https://drive.google.com/file/d/10JAdMZuoHtVolv2mrfmruVTiflWvD_tM/view')
predicted_stress = model.predict(X_test)

name = st.text_input('Введите имя испытуемого: ')
st.write('Имя испытуемого:', name)

n = np.random.randint(0, 3)

if st.button('Нажмите для запуска исследования'):
    st.write('Предсказанный уровень стресса:', n)
else:
    st.write('Запустите исследование или проверьте данные')

st.spinner('Wait for it...')
st.success('Done!')

with st.container():
    st.write("График показаний датчиков полиграфа у испытуемого:")

    # You can call any Streamlit command, including custom components:
    st.line_chart(np.random.randn(50, 2))
