import streamlit as st
import numpy as np
from PIL import Image

st.title('Мой психолог: ИИ')
image = 'https://newizv.ru/attachments/27e959e9382672f8826de4367888b0a9a95ea136/store/fill/360/200/f0e21b931e498bcc91c2e33905fbb228fc31cf3cdda2b398d07fe3e6790f/f0e21b931e498bcc91c2e33905fbb228fc31cf3cdda2b398d07fe3e6790f.jpg'
st.image(image, caption = 'Исследование на полиграфе')

def load_data():
    uploaded_file = st.file_uploader(label = 'Загрузите данные датчиков полиграфа в виде CSV-файла:')
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    else:
        return None

data = load_data()

result = st.button('Загрузить данные')

#Кастомные значения, вводимые вручную:
st.subheader('Введите ниже исходные значения для исследования:')

option = st.selectbox(
     'Выберите номер вопроса:',
     (1,2,3,4,5,6,7,8,9,10,11,12,13))
st.write('Выбранный номер вопроса:', option)

option = st.selectbox(
     'Выберите номер группы вопроса:',
     (0,1,2,3,4,5,6))
st.write('Выбранный номер группы вопроса:', option)

option = st.selectbox(
     'Выберите номер повторения:',
     (1, 2, 3, 4))
st.write('Выбранный номер повторения:', option)

name = st.text_input('Введите имя испытуемого: ')
st.write('Имя испытуемого:', name)

n = np.random.randint(0, 3)

if st.button('Нажмите для запуска исследования'):
     st.write('Предсказанный уровень стресса:', n)
else:
     st.write('Запустите исследование')


st.spinner('Wait for it...')
st.success('Done!')

with st.container():
    st.write("График показаний датчиков полиграфа у испытуемого:")

    # You can call any Streamlit command, including custom components:
    st.line_chart(np.random.randn(50, 2))
