import pandas as pd
import numpy as np
import random
from collections import defaultdict


books = pd.read_csv('data/books.csv')
ratings = pd.read_csv('data/ratings.csv')

# активные пользователи
active_users = ratings['user_id'].value_counts().head(50).index.tolist()
random.shuffle(active_users)
selected_users = active_users[:3]


sample_ratings = ratings[ratings['user_id'].isin(active_users)]
user_book_matrix = sample_ratings.pivot_table(
    index='user_id',
    columns='book_id',
    values='rating',
    fill_value=0
)



def calc_similarity(vec1, vec2):
    common = 0
    total_sim = 0

    for book_id in vec1.index:
        if vec1[book_id] > 0 and vec2[book_id] > 0:
            common += 1
            diff = abs(vec1[book_id] - vec2[book_id])
            sim = 1 - (diff / 4.0)
            total_sim += sim

    return total_sim / common if common > 0 else 0



def show_popular_books(num_recs=3):
    book_ratings = ratings.groupby('book_id')['rating'].agg(['mean', 'count'])
    popular_books = book_ratings[
        (book_ratings['count'] >= 10) &
        (book_ratings['mean'] >= 4.0)
        ].sort_values('mean', ascending=False)

    print("Рекомендуем популярные книги:")
    for book_id in popular_books.head(num_recs).index:
        book_info = books[books['book_id'] == book_id]
        if len(book_info) > 0:
            title = book_info['title'].values[0]
            avg_rating = popular_books.loc[book_id, 'mean']
            if len(title) > 35:
                title = title[:35] + "..."
            print(f"  {title} - {avg_rating:.1f}⭐ (на основе {popular_books.loc[book_id, 'count']} оценок)")


# Основная функция рекомендаций
def get_recs(user_id, num_recs=3):
    if user_id not in user_book_matrix.index:
        print("пользователь не найден")
        return


    user_ratings = ratings[ratings['user_id'] == user_id]


    if len(user_ratings) == 0:
        print("Вы новый пользователь!")
        show_popular_books(num_recs)
        return


    if len(user_ratings) > 0:
        print("уже читал:")
        for _, row in user_ratings.head(2).iterrows():
            book_info = books[books['book_id'] == row['book_id']]
            if len(book_info) > 0:
                title = book_info['title'].values[0]
                if len(title) > 35:
                    title = title[:35] + "..."
                print(f"  {title} - {row['rating']}⭐")


    current_user = user_book_matrix.loc[user_id]


    similar_users = []
    for other_id in user_book_matrix.index:
        if other_id != user_id:
            other_user = user_book_matrix.loc[other_id]
            similarity = calc_similarity(current_user, other_user)
            if similarity > 0.3:
                similar_users.append((other_id, similarity))


    if not similar_users:
        print("\nНе нашлось пользователей с похожими вкусами.")
        show_popular_books(num_recs)
        return


    similar_users.sort(key=lambda x: x[1], reverse=True)


    recommendations = defaultdict(float)

    for other_id, similarity in similar_users:
        other_ratings = user_book_matrix.loc[other_id]
        for book_id in user_book_matrix.columns:
            if other_ratings[book_id] >= 4 and current_user[book_id] == 0:
                recommendations[book_id] += other_ratings[book_id] * similarity


    if not recommendations:
        print("\nНет персональных рекомендаций.")
        show_popular_books(num_recs)
        return


    top_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:num_recs]


    max_score = top_recs[0][1] if top_recs else 1

    print(f"\nрекомендую почитать (на основе {len(similar_users)} похожих читателей):")

    for i, (book_id, score) in enumerate(top_recs, 1):
        book_info = books[books['book_id'] == book_id]
        if len(book_info) > 0:
            title = book_info['title'].values[0]
            author = book_info['authors'].values[0] if 'authors' in book_info.columns else "неизвестен"


            if max_score > 0:
                percent_score = (score / max_score) * 100
            else:
                percent_score = 0


            if percent_score > 80:
                rating_text = "очень рекомендую! 👍👍"
            elif percent_score > 50:
                rating_text = "рекомендую! 👍"
            else:
                rating_text = "может понравиться 👌"

            if len(title) > 35:
                title = title[:35] + "..."

            print(f"{i}. {title}")
            print(f"   автор: {author}")
            print(f"   {rating_text} ({percent_score:.0f}% совпадения)")



print(" СИСТЕМА РЕКОМЕНДАЦИЙ КНИГ")
print("=" * 50)

for user_id in selected_users:
    print(f"\n=== для пользователя {user_id} ===")
    get_recs(user_id, 3)
    print("\n" + "-" * 50)