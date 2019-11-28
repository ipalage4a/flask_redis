import unittest
import json
import time
import app, models, resources, utils

class emptyDBTestCase(unittest.TestCase):
    def setUp(self):
        self.redis_test = app.FlaskRedis(app.app)
        self.domain = "http://127.0.0.1:5000/"
        self.app = app.app.test_client()

    def tearDown(self):
        self.redis_test.flushall()

    def test_decode_from_bin(self):
        test_data = [b'test', b'testes', b'test', b'testes']
        self.assertNotEqual([b'test', b'testes', b'test', b'testes'], utils.decode_from_bin(test_data))
        self.assertEqual(['test', 'testes', 'test', 'testes'], utils.decode_from_bin(test_data))

    def test_get_links_from_set(self):
        links = [
                    b"yahoo.com/test",
                    b"https://google.com/?dev=test",
                    b"www.ya.com/test?get=id",
                    b"https://www.ya.com/test?get=id",
                    b"https://example.com/?test"
                ]

        from_time = int(time.time())
        to_time = int(time.time()) + 1
        for _time in range(from_time, to_time):
            for key, link in enumerate(links):
                self.redis_test.sadd(f'time:{_time}:links', link)

        self.assertEqual(sorted(models.get_links_from_set(from_time, to_time)), sorted(links))
        self.assertEqual(sorted(models.get_links_from_set(None, None)), sorted([]))


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
            self.assertEqual(domain, utils.get_domain_from_url(link))

    def test_put_links_in_set(self):
        links = [
                "yahoo.com/test",
                "https://google.com/?dev=test",
                "www.ya.com/test?get=id",
                "https://www.ya.com/test?get=id",
                "https://example.com/?test"
                ]
        request_time = int(time.time())


        self.assertEqual('ok', models.put_links_in_set(request_time, links))

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
                    ],
                "status": "ok"
                }

        test_json_response_second = {
                "domains": [
                    "example.com",
                    "google.com",
                    "ya.com",
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
