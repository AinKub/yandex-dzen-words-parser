from src.functions import *
from src.ya_parser import YaParser


# DZEN_NEWS_URL = 'https://dzen.ru/news/'
DZEN_COMPUTER_NEWS_URL = 'https://dzen.ru/news/rubric/computers'


def main():
    ya_parser = YaParser()
    # ya_parser.go_to_page(DZEN_NEWS_URL)
    ya_parser.go_to_page(DZEN_COMPUTER_NEWS_URL)
    list_of_articles = ya_parser.find_all_articles()
    ya_parser.close()

    filtered_list_of_articles_by_month = return_last_month_articles(list_of_articles)

    list_of_articles_without_punctuation = prepare_articles_title_and_annotation(
        filtered_list_of_articles_by_month
    )
    articles_with_specific_words = return_articles_with_specific_words(
        list_of_articles_without_punctuation,
        ['игра', 'игры', 'игру', 'игре']
    )
    most_common_words = return_most_common_words_from_articles(articles_with_specific_words)
    generate_word_cloud_from_most_common_words(most_common_words)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)s [%(asctime)s] - %(name)s - %(message)s')
    main()