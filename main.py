import pandas as pd
from bs4 import BeautifulSoup
import requests


def request_data(url):
    r = requests.get(url)
    html = r.text
    return html


def get_data(text):
    html_soup = BeautifulSoup(text, 'html.parser')
    movies = html_soup.findAll('tr')
    movies = movies[1:]
    movie_list = []
    for movie in movies:
        name = movie.find(name='td', attrs={'class': 'titleColumn'}).a.string
        year = movie.find(name='td', attrs={'class': 'titleColumn'}).span.string
        year = year[1:-1]
        year = int(year)
        rating = movie.find(name='td', attrs={'class': 'ratingColumn imdbRating'}).strong.text
        rating = float(rating)
        num_rating = movie.find(name='td', attrs={'class': 'ratingColumn imdbRating'}).strong.attrs['title']
        num_rating = num_rating.split()[3].replace(',', '')
        movie_data = [name, year, rating, num_rating]
        movie_list.append(movie_data)
    movie_frames = pd.DataFrame(movie_list, columns=['name', 'year', 'rating', 'number of user rating'])
    return movie_frames


def save_data(data_frame):
    data_frame.to_csv('D:/CODE/movie_data.csv', index=False)


def main():
    url = 'https://www.imdb.com/chart/top'
    html_text = request_data(url)
    DF = get_data(html_text)
    save_data(DF)


if __name__ == "__main__":
    main()
