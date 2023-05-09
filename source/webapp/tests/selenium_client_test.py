# import os
# from django.test import LiveServerTestCase
# from django.urls import reverse
# from django.shortcuts import get_object_or_404
# from selenium.webdriver.common.by import By
# from webapp.models import Client
# from webapp.forms import ClientForm
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
#
#
# class MySeleniumTests(LiveServerTestCase):
#     def setUp(self):
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chromedriver_path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver')
#         self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
#
#         self.client = Client.objects.create(
#             telegram_id='client',
#             phone='test_data',
#             first_name='test_data',
#             last_name='test_data',
#             email='test_data',
#             region='test_data',
#             comment='test_data'
#         )
#
#     def tearDown(self):
#         self.driver.quit()
#         super().tearDownClass()
#
#     def test_create_client(self):
#         url = self.live_server_url + reverse('webapp:client_create')
#         self.driver.get(url)
#
#         self.driver.find_element(By.NAME, 'telegram_id').send_keys('TestUser')
#         self.driver.find_element(By.NAME, 'phone').send_keys('1234567890')
#         self.driver.find_element(By.NAME, 'first_name').send_keys('John')
#         self.driver.find_element(By.NAME, 'last_name').send_keys('Doe')
#         self.driver.find_element(By.NAME, 'email').send_keys('johndoe@example.com')
#         self.driver.find_element(By.NAME, 'region').send_keys('New York')
#         self.driver.find_element(By.NAME, 'comment').send_keys('This is a test client')
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         form = ClientForm({
#             'telegram_id': '5555555',
#             'phone': '1234567890',
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'email': 'johndoe@example.com',
#             'region': 'New York',
#             'comment': 'This is a test client',
#         })
#
#         self.assertTrue(form.is_valid())
#         form.save()
#
#         client = get_object_or_404(Client, telegram_id='TestUser')
#         self.assertEqual(client.telegram_id, 'TestUser')
#         self.assertEqual(client.phone, '1234567890')
#         self.assertEqual(client.first_name, 'John')
#         self.assertEqual(client.last_name, 'Doe')
#         self.assertEqual(client.email, 'johndoe@example.com')
#         self.assertEqual(client.region, 'New York')
#         self.assertEqual(client.comment, 'This is a test client')
#
#     def test_update_client(self):
#         url = self.live_server_url + reverse('webapp:client_update', kwargs={'pk': self.client.pk})
#         self.driver.get(url)
#
#         self.driver.find_element(By.NAME, 'telegram_id').clear()
#         self.driver.find_element(By.NAME, 'phone').clear()
#         self.driver.find_element(By.NAME, 'first_name').clear()
#         self.driver.find_element(By.NAME, 'last_name').clear()
#         self.driver.find_element(By.NAME, 'email').clear()
#         self.driver.find_element(By.NAME, 'region').clear()
#         self.driver.find_element(By.NAME, 'comment').clear()
#
#         self.driver.find_element(By.NAME, 'telegram_id').send_keys('UpdatedTestUser')
#         self.driver.find_element(By.NAME, 'phone').send_keys('1234567890')
#         self.driver.find_element(By.NAME, 'first_name').send_keys('John')
#         self.driver.find_element(By.NAME, 'last_name').send_keys('Doe')
#         self.driver.find_element(By.NAME, 'email').send_keys('johndoe@example.com')
#         self.driver.find_element(By.NAME, 'region').send_keys('New York')
#         self.driver.find_element(By.NAME, 'comment').send_keys('This is a test client')
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         updated_client = Client.objects.get(pk=self.client.pk)
#         self.assertEqual(updated_client.telegram_id, 'UpdatedTestUser')
#         self.assertEqual(updated_client.phone, '1234567890')
#         self.assertEqual(updated_client.first_name, 'John')
#         self.assertEqual(updated_client.last_name, 'Doe')
#         self.assertEqual(updated_client.email, 'johndoe@example.com')
#         self.assertEqual(updated_client.region, 'New York')
#         self.assertEqual(updated_client.comment, 'This is a test client')
#
#     def test_client_detail(self):
#         url = self.live_server_url + reverse('webapp:client_detail',  kwargs={'pk': self.client.pk})
#         self.driver.get(url)
#         self.assertEqual(self.driver.title, 'Просмотр клиента')
#
#     def test_client_delete(self):
#         url = self.live_server_url + reverse('webapp:client_delete', kwargs={'pk': self.client.pk})
#         self.driver.get(url)
#         self.driver.find_element(By.XPATH, '//form').submit()
#         self.client.refresh_from_db()
#         self.assertFalse(self.client.is_active)
