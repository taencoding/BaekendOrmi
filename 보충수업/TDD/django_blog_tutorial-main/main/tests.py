from django.test import TestCase

class Test(TestCase):
    def test_something_one(self):
        '''
        블로그 리스트 체크
        '''
        self.assertEqual(True, False)

    def test_something_two(self):
        '''
        템플릿 상속 체크
        '''
        self.assertEqual(True, True)