from unittest import TestCase, main
from ddt import ddt, file_data
from crawler.classes.newsprovider import NEWS_PROVIDERS_MAPPING


@ddt
class TestArticles(TestCase):
    @file_data("data/test_process_article.json")
    def test_process_article(self, link, expected_output):
        for news_provider_class in NEWS_PROVIDERS_MAPPING.values():
            article_class = news_provider_class.identify_article(link)
            if article_class:
                break
        actual = article_class.process(link)
        expected_output["time_collected"] = actual["time_collected"]
        for key in actual.keys():
            if expected_output[key] != actual[key]:
                print(key, " is not equal")
                print("expected: ", expected_output[key])
                print("actual: ", actual[key])
        self.assertDictEqual(expected_output, actual)


if __name__ == '__main__':
    main()
