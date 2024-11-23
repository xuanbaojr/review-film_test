import sqlalchemy
import pandas as pd 
# Connect to the database

def all_movies():
    conn = sqlalchemy.create_engine(
        'mysql+pymysql://root:02022003aA@localhost:3306/django_review')

    movies = pd.read_csv("../dl/recommend/movies.csv")
    movies = movies[["original_title", "genres", "director", "cast", "keywords"]]

    # Add an 'id' column
    movies.reset_index(inplace=True)  # Đưa chỉ số thành cột
    movies.rename(columns={"index": "id"}, inplace=True)  # Đổi tên cột thành 'id'
    movies["id"] += 1  # Đảm bảo id bắt đầu từ 1

    # Write the DataFrame to the database
    movies.to_sql(name='endpoints_movie', con=conn, if_exists='replace', index=False)


if __name__ == "__main__":
    all_movies()