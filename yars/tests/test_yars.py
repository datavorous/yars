import unittest
from yars.yars import YARS
from unittest.mock import patch, MagicMock

class TestYARS(unittest.TestCase):

    @patch('requests.Session')
    def setUp(self, mock_session):
        self.yars = YARS(user_agent="Mozilla/5.0", proxy=None)
        self.session = mock_session.return_value

    def test_initialization(self):
        self.assertEqual(self.yars.headers["User-Agent"], "Mozilla/5.0")
        self.assertIsNotNone(self.yars.session)
        self.assertIsNone(self.yars.proxy)

    def test_set_user_agent(self):
        self.yars.set_user_agent("Custom User Agent")
        self.assertEqual(self.yars.headers["User-Agent"], "Custom User Agent")

    @patch('yars.agents.get_agent')
    def test_set_random_user_agent(self, mock_get_agent):
        mock_get_agent.return_value = "Random User Agent"
        self.yars.set_random_user_agent()
        self.assertEqual(self.yars.headers["User-Agent"], "Random User Agent")

    @patch('requests.Session.get')
    def test_search_reddit_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "children": [
                    {"data": {"title": "Test Post", "permalink": "/test-post", "selftext": "Test description"}}
                ]
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        results = self.yars.search_reddit("test", limit=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test Post")
        self.assertEqual(results[0]["link"], "https://www.reddit.com/test-post")

    @patch('requests.Session.get')
    def test_search_reddit_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        results = self.yars.search_reddit("test", limit=1)

        self.assertEqual(results, [])

    @patch('requests.Session.get')
    def test_scrape_post_details_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "data": {
                    "children": [
                        {"data": {"title": "Test Post", "selftext": "This is a test post."}}
                    ]
                }
            },
            {
                "data": {
                    "children": [
                        {"kind": "t1", "data": {"author": "user1", "body": "Test comment", "replies": {}}}
                    ]
                }
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        post_details = self.yars.scrape_post_details("/test-post")

        self.assertEqual(post_details["title"], "Test Post")
        self.assertEqual(post_details["body"], "This is a test post.")
        self.assertEqual(len(post_details["comments"]), 1)
        self.assertEqual(post_details["comments"][0]["author"], "user1")

    @patch('requests.Session.get')
    def test_scrape_post_details_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        post_details = self.yars.scrape_post_details("/nonexistent-post")

        self.assertIsNone(post_details)

    @patch('requests.Session.get')
    def test_scrape_user_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "children": [
                    {"kind": "t3", "data": {"title": "User Post", "permalink": "/user-post"}},
                    {"kind": "t1", "data": {"body": "User comment", "permalink": "/user-comment"}},
                ],
                "after": None
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        user_data = self.yars.scrape_user_data("testuser", limit=2)

        self.assertEqual(len(user_data), 2)
        self.assertEqual(user_data[0]["type"], "post")
        self.assertEqual(user_data[1]["type"], "comment")

    @patch('requests.Session.get')
    def test_fetch_subreddit_posts_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "children": [
                    {"data": {"title": "Post 1", "author": "author1", "permalink": "/post-1", "score": 10, "num_comments": 2, "created_utc": 1234567890}},
                    {"data": {"title": "Post 2", "author": "author2", "permalink": "/post-2", "score": 20, "num_comments": 5, "created_utc": 1234567891}},
                ],
                "after": None
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        subreddit_posts = self.yars.fetch_subreddit_posts("testsubreddit", limit=2)

        self.assertEqual(len(subreddit_posts), 2)
        self.assertEqual(subreddit_posts[0]["title"], "Post 1")
        self.assertEqual(subreddit_posts[1]["title"], "Post 2")

    @patch('requests.Session.get')
    def test_fetch_subreddit_posts_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        subreddit_posts = self.yars.fetch_subreddit_posts("nonexistent", limit=2)

        self.assertEqual(subreddit_posts, [])

if __name__ == "__main__":
    unittest.main()
