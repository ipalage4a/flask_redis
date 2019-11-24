import unittest
import requests
import json
import funbox
import time

class FunboxEmptyDBTestCase(unittest.TestCase):

    def setUp(self):
        self.redis_test = funbox.FlaskRedis(funbox.app)
        self.domain = "http://127.0.0.1:5000/"
        self.app = funbox.app.test_client()

    def tearDown(self):
        self.redis_test.flushall()

    def test_decode_from_bin(self):
        test_data = [b'test', b'testes', b'test', b'testes']
        self.assertNotEqual([b'test', b'testes', b'test', b'testes'], funbox.decode_from_bin(test_data))
        self.assertEqual(['test', 'testes', 'test', 'testes'], funbox.decode_from_bin(test_data))


    def test_get_domain_from_url(self):
        links = [
                "yahoo.com/test",
                "https://google.com/?dev=test",
                "www.ya.com/test?get=id",
                "https://www.ya.com/test?get=id",
                "https://example.com/?test"
                ]
        domains = [
                "yahoo.com",
                "google.com",
                "ya.com",
                "ya.com",
                "example.com"
                ]
        test_cases = zip(domains, links)
        for domain, link in test_cases:
            self.assertEqual(domain, funbox.get_domain_from_url(link))

    def test_put_links_in_set(self):
        links = [
                "yahoo.com/test",
                "https://google.com/?dev=test",
                "www.ya.com/test?get=id",
                "https://www.ya.com/test?get=id",
                "https://example.com/?test"
                ]
        request_time = int(time.time())


        self.assertEqual('ok', funbox.put_links_in_set(request_time, links))

    def test_filter_link_by_date(self):
        links = [
                "yahoo.com/test",
                "https://google.com/?dev=test",
                "www.ya.com/test?get=id",
                "https://www.ya.com/test?get=id",
                "https://example.com/?test"
                ]

    def test_VisitedLinks_pure_post(self):
        url = self.domain + "visited_links"
        test_json = {
                "links": [
                    "yahoo.com/test",
                    "google.com/test",
                    "ya.com/test",
                    "example.com/test"
                    ]
                }

        request_time = int(time.time())
        response = self.app.post(url, json=test_json)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.get_json(),{"status": "ok" })



    def test_VisitedDomain_pure_get(self):
        url = self.domain + "visited_domains"
        test_json = {
                "domains": [],
                "status": "No data!"
                }
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), test_json)

    def test_VisitedDomain_unpure_get(self):
        url_post = self.domain + "visited_links"
        url_get = self.domain + "visited_domains"
        test_json_for_post_first = {
                "links": [
                    "yahoo.com/test",
                    "https://google.com/?dev=test",
                    "www.ya.com/test?get=id",
                    "https://www.ya.com/test?get=id",
                    "https://example.com/?test"
                    ]
                }
        test_json_for_post_second = {
                "links": [
                    "inoco.com/test",
                    "https://google.com/?dev=test",
                    "www.badoo.com/test?get=id",
                    "https://www.ya.com/test?get=id",
                    "https://example.com/?test"
                    ]
                }

        test_json_response_first = {
                "domains": [
                    "example.com",
                    "google.com",
                    "ya.com",
                    "yahoo.com"
                    ],
                "status": "ok"
                }
        test_json_response_second = {
                "domains": [
                    "badoo.com",
                    "example.com",
                    "google.com",
                    "inoco.com",
                    "ya.com",
                    "yahoo.com"
                    ],
                "status": "ok"
                }

        #test simple reqest with one set of links
        request_time = int(time.time())
        post_response = self.app.post(url_post , json=test_json_for_post_first)
        get_response = self.app.get(f'{ url_get }?from={request_time}&to={int(time.time()) + 2}')
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.get_json(), test_json_response_first)

        #test response with multiple sets of links
        time.sleep(1)
        second_rt = int(time.time())
        second_post_response = self.app.post(url_post , json=test_json_for_post_second)
        second_get_response = self.app.get(f'{ url_get }?from={request_time}&to={second_rt + 1}')
        self.assertEqual(second_post_response.status_code, 200)
        self.assertEqual(second_get_response.status_code, 200)
        self.assertEqual(second_get_response.get_json(), test_json_response_second)


if __name__ == "__main__":
    unittest.main()
