from selenium import webdriver
import unittest


class NewUserTest(unittest.TestCase):

    def setUp(self):
        # try
        self.browser = webdriver.Chrome('C:/chromedriver.exe')

    def tearDown(self):
        # except
        self.browser.quit()

    def test_can_see_diary_list(self):
        self.browser.get('http://localhost:8000/diary/list')
        self.assertIn('Diary List', self.browser.title)
        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')




