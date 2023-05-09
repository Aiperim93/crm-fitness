# import os
# from selenium.webdriver.common.by import By
# from datetime import datetime, timedelta, time
# from django.urls import reverse
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from django.shortcuts import get_object_or_404
# from selenium.webdriver.chrome.options import Options
# from webapp.models import Group, Coach, Client, Training, Payment
#
#
# class TrainingSeleniumTest(LiveServerTestCase):
#     def setUp(self) -> None:
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chromedriver_path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver')
#         self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
#
#         self.coach1 = Coach.objects.create(
#             telegram_id='coach1',
#             phone='test_data',
#             first_name='test_data',
#             last_name='test_data',
#             email='test@data.com',
#             started_to_work=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
#             description='test_data',
#         )
#
#         self.group1 = Group.objects.create(
#             name='box',
#             start_at=time(hour=9, minute=30),
#             coach=self.coach1
#         )
#
#         self.client1 = Client.objects.create(
#             telegram_id='client',
#             phone='test_data',
#             first_name='test_data',
#             last_name='test_data',
#             email='test@data.com',
#             region='test_data',
#             comment='test_data',
#             group=self.group1
#         )
#
#         self.payment1 = Payment.objects.create(
#             client=self.client1,
#             amount=500,
#             paid_at=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
#             payment_start_date=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
#             payment_end_date=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
#         )
#
#     def tearDown(self) -> None:
#         self.driver.quit()
#
#     def test_training_create(self):
#         url = self.live_server_url + reverse('webapp:client_detail', kwargs={'pk': self.client1.pk})
#         self.driver.get(url)
#         self.driver.find_element(By.CSS_SELECTOR, 'form').submit()
#         training = get_object_or_404(Training, client=self.client1)
#         self.assertEqual(training.group, self.group1)
