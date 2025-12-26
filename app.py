import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_exam_data(num_students=100, num_questions=30):
    np.random.seed(42)
    difficulties = ['Easy', 'Medium', 'Hard']
    data = []
    for student_id in range(1, num_students+1):
        for question_id in range(1, num_questions+1):
            difficulty = np.random.choice(difficulties, p=[0.4,0.4,0.2])
            time_taken = np.random.normal(60,15) + (5 if difficulty=='Hard' else 0)
            correct_prob = {'Easy':0.7, 'Medium':0.5, 'Hard':0.3}[difficulty]
            correct = np.random.rand() < correct_prob
            data.append({'student_id': student_id, 'question_id': question_id,
                         'difficulty': difficulty, 'time_taken': max(10, round(time_taken,2)),
                         'correct': int(correct)})
    return pd.DataFrame(data)

def plot_success_rate(df):
    success_rate = df.groupby('difficulty')['correct'].mean()*100
    fig, ax = plt.subplots()
    sns.barplot(x=success_rate.index, y=success_rate.values, palette='viridis', ax=ax)
    ax.set_ylabel('Success Rate (%)')
    ax.set_xlabel('Question Difficulty')
    ax.set_title('Success Rate by Question Difficulty')
    ax.set_ylim(0,100)
    return fig

def main():
    st.title("Student Online Exam Success Rate Analysis")
    st.sidebar.header("Options")
    option = st.sidebar.selectbox("Choose an action:", ("Upload CSV file","Generate synthetic CSV"))

    if option=="Upload CSV file":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded!")
            st.dataframe(df.head())
            st.write(df.describe(include='all'))
            if 'difficulty' in df.columns and 'correct' in df.columns:
                st.pyplot(plot_success_rate(df))
            else:
                st.warning("CSV must contain 'difficulty' and 'correct'")
    else:
        num_students = st.number_input("Number of students", 10, 1000, 100, 10)
        num_questions = st.number_input("Number of questions", 5, 100, 30, 5)
        if st.button("Generate CSV"):
            df = generate_exam_data(num_students,num_questions)
            df.to_csv('generated_exam_data.csv', index=False)
            st.success("CSV generated as 'generated_exam_data.csv'")
            st.dataframe(df.head())
            st.pyplot(plot_success_rate(df))

if __name__=="__main__":
    main()
