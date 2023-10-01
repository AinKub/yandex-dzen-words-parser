import logging
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List, Tuple, Union

from nltk import Text, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud

from src.ya_parser import Article


def return_last_month_articles(list_of_articles: List[Article]) -> List[Article]:
    """
    Фильтрует список из `Article`, оставляя только те, дата публикации которых - 
    последние 30 дней.
    """

    logging.info('Starting searching for last month articles...')
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)

    logging.info(f'Searching for articles by articles publication time >= {one_month_ago}')
    filtered_list_of_articles = filter(lambda article: article.publication_time >= one_month_ago, 
                                       list_of_articles)
    filtered_list_of_articles = list(filtered_list_of_articles)

    logging.info(f'Searching is ended. Was founded {len(filtered_list_of_articles)} articles')
    return filtered_list_of_articles


def prepare_articles_title_and_annotation(list_of_articles: List[Article]) -> List[Article]:
    """
    Приводит к нижнему регистру все слова в заголовках и аннотациях статей, а также
    убирает оттуда все знаки пунктуации
    """

    logging.info('Starting prepare articles title and annotation...')
    filtered_list_of_articles = []
    spec_chars = string.punctuation + '\n\xa0«»\t—…'
    for article in list_of_articles:

        article.title = article.title.replace('-', ' ')
        article.annotation = article.annotation.replace('-', ' ')

        # Выбираем те символы, которых нет в стоп-символах (знаках пунктуации)
        article.title = ''.join([ch for ch in article.title.lower() if ch not in spec_chars])
        article.annotation = ''.join([ch for ch in article.annotation.lower() if ch not in spec_chars])

        filtered_list_of_articles.append(article)

    logging.info('Articles title and annotation were prepared')
    return filtered_list_of_articles


def return_articles_with_specific_words(list_of_articles: List[Article],
                                        words_for_search: List[str]
                                        ) -> Union[List[Article], None]:
    """
    Возвращает только те статьи, которые содержат или в заголовке, или в 
    аннотации слова из заданного списка `words_for_search`

    :param words_for_search: Список из слов, которые должны быть в статье
    """
    
    logging.info('Starting finding articles with specific words...')
    logging.info(f'Len of start list of articles: {len(list_of_articles)}')
    logging.info(f'Searching for words: {", ".join(words_for_search)}')
    
    filtered_list_of_articles = []
    for article in list_of_articles:

        # Делаем объединение множеств и проверяем, есть ли совпадания
        common_words_in_title = set(article.title.split()) & set(words_for_search)
        if common_words_in_title:
            filtered_list_of_articles.append(article)
            continue

        common_words_in_annotation = set(article.annotation.split()) & set(words_for_search)
        if common_words_in_annotation:
            filtered_list_of_articles.append(article)
            continue

    logging.info(f'Searching is ended. Was founded {len(filtered_list_of_articles)} articles with specific words')
    return filtered_list_of_articles


def return_most_common_words_from_articles(list_of_articles: List[Article]) -> List[Tuple[Any, int]]:
    """
    Возвращает топ-50 слов в формате `слово` - `сколько раз встречается`.
    Предварительно склеивает все заголовки и аннотации в одно предложение и убирает стоп-слова.
    """
    logging.info('Starting finding most common words from articles...')

    combined_text = ' '.join([f'{article.title} {article.annotation}' for article in list_of_articles])
    text_tokens = word_tokenize(combined_text)
    russian_stopwords = stopwords.words('russian')
    text_tokens_without_stop_words = [word for word in text_tokens if not word in russian_stopwords]
    text = Text(text_tokens_without_stop_words)
    fdist = FreqDist(text)

    logging.info('Most common words from articles was finded')
    return fdist.most_common(50)


def generate_word_cloud_from_most_common_words(most_common_words: List[Tuple[Any, int]]) -> None:
    """
    Создаёт облако слов из `most_common_words` и сохраняет его в директорию `wordclouds`
    """
    logging.info('Starting generating wordcloud...')

    # f'{word_data[0]} ' * word_data[1] здесь для того, чтобы размножить слово на количество его повторений.
    # Например, слово 'spam' встречается 3 раза - получится 'spam spam spam'
    raw_text = ''.join([f'{word_data[0]} ' * word_data[1] for word_data in most_common_words])
    wordcloud = WordCloud().generate(raw_text)
    destination = Path.cwd() / 'wordclouds'
    if not destination.exists():
        destination.mkdir()

    filename = f'wordcloud_{datetime.now().timestamp()}.png'
    destination = destination / filename
    wordcloud.to_file(destination)

    logging.info(f'Wordcloud successfully saved to {destination}')