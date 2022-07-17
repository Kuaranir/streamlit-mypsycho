import streamlit as st
import numpy as np
import pandas as pd
import pickle
from data_preprocessing import preprocess

filename = 'forest_model.sav'
st.title('Мой психолог: ИИ')
st.image('RIAN_993974.HR_.ru_.jpg',
    caption='Исследование на полиграфе')


def load_data():
    uploaded_file = st.file_uploader(label='Загрузите данные датчиков полиграфа в виде CSV-файла:', type=['csv'])
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    else:
        return None


def get_result_table(X_test, predicted):
    cols = ['Test_index', 'Presentation', 'Question', 'Predicted_level']
    X_test['Predicted_level'] = predicted
    res = X_test[cols]

    res.insert(3, 'Presentation_1',
               res.apply(lambda row: row.Predicted_level if row.Presentation == 1 else None, axis=1))
    res.insert(4, 'Presentation_2',
               res.apply(lambda row: row.Predicted_level if row.Presentation == 2 else None, axis=1))
    res.insert(5, 'Presentation_3',
               res.apply(lambda row: row.Predicted_level if row.Presentation == 3 else None, axis=1))
    res.insert(6, 'Presentation_4',
               res.apply(lambda row: row.Predicted_level if row.Presentation == 4 else None, axis=1))
    res = res.groupby(['Test_index', 'Question']).agg({'Presentation_1': "sum",
                                                       'Presentation_2': "sum",
                                                       'Presentation_3': "sum",
                                                       'Presentation_4': 'sum'}).round()
    res.insert(4, 'SUM', res.apply(lambda row: row.Presentation_1 + row.Presentation_2 +
                                               row.Presentation_3 + row.Presentation_4,
                                   axis=1))
    return res


data = load_data()
if data is not None:
    model = pickle.load(open(filename, 'rb'))
    X_test, Y_test = preprocess(data), data.Class_label

    predicted = model.predict(X_test)

    if st.button('Нажмите для запуска исследования'):
        st.markdown('***Результаты рассчета значений уровня стресса,'
                    ' сгрупированные по группам вопросов и вопросам соответсвенно:***')
        st.dataframe(get_result_table(X_test, predicted),
                     width=800, height=500)
    with st.container():
        st.write("График показаний датчиков полиграфа у испытуемого:")

        group = st.selectbox('Какая группа вопросов вас интересует?',
                             np.sort(data['Test_index'].unique()))
        question = st.selectbox('Какой именно вопрос вас интересует?',
                                np.sort(data.loc[(data.Test_index == group)]['Question'].unique()))
        pres = st.selectbox('Какое его повторение?', np.sort(data.loc[(data.Test_index == group) &
                                                                      (data.Question == question)][
                                                                 'Presentation'].unique()))

        st.line_chart(data.loc[(data.Test_index == group) &
                               (data.Question == question) & (data.Presentation == pres)]['Data'].iloc[0])
else:
    st.write('Запустите исследование или проверьте данные')


