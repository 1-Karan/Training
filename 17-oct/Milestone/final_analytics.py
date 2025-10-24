import pandas as pd


def analytics():
    # Load students data
    students_df = pd.read_csv('students.csv')

    # Load processed results with total, percentage, result
    results_df = pd.read_csv('student_results.csv')

    # Merge on StudentID
    merged_df = pd.merge(students_df, results_df, on='StudentID')

    print("\n=== Top 3 students by Percentage ===")
    top_students = merged_df.sort_values(by='Percentage', ascending=False).head(3)
    print(top_students[['StudentID', 'Name', 'Course', 'Percentage']])

    print("\n=== Average Marks per Course ===")
    avg_marks = merged_df.groupby('Course')[['Maths', 'Python', 'ML']].mean()
    print(avg_marks)


if __name__ == '__main__':
    analytics()
