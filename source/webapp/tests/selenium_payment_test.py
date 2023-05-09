# import os
# from selenium.webdriver.common.by import By
# from datetime import datetime, timedelta
# from django.urls import reverse
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from django.shortcuts import get_object_or_404
# from selenium.webdriver.chrome.options import Options
# from webapp.models import Payment, Client
#
#
# class PaymentSeleniumTest(LiveServerTestCase):
#     def setUp(self) -> None:
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chromedriver_path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver')
#         self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
#
#         self.client1 = Client.objects.create(
#             telegram_id='66666',
#             phone='test_data',
#             first_name='test_data',
#             last_name='test_data',
#             email='test_data',
#             region='test_data',
#             comment='test_data'
#         )
#
#         self.payment1 = Payment.objects.create(
#             client=self.client1,
#             amount=500,
#             paid_at=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
#             payment_start_date=(datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
#             payment_end_date=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
#         )
#
#     def tearDown(self) -> None:
#         self.driver.quit()
#
#     def test_payment_create(self):
#         url = self.live_server_url + reverse('webapp:payment_create', kwargs={'pk': self.client1.pk})
#         self.driver.get(url)
#         self.driver.find_element(By.NAME, 'amount').send_keys(600)
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         payment = get_object_or_404(Payment, amount=600)
#         self.assertEqual(payment.amount, 600)
#         self.assertEqual(payment.client, self.client1)
#
#     def test_payment_update(self):
#         url = self.live_server_url + reverse('webapp:payment_update', kwargs={'pk': self.payment1.pk})
#         self.driver.get(url)
#
#         self.driver.find_element(By.NAME, 'amount').clear()
#         self.driver.find_element(By.NAME, 'amount').send_keys(800)
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         updated_payment = Payment.objects.get(pk=self.payment1.pk)
#         self.assertEqual(updated_payment.amount, 800)
#         self.assertEqual(updated_payment.client.first_name, self.client1.first_name)
#
#     def test_payment_delete(self):
#         url = self.live_server_url + reverse('webapp:payment_delete', kwargs={'pk': self.payment1.pk})
#         self.driver.get(url)
#         self.driver.find_element(By.XPATH, '//form').submit()
#         self.assertFalse(Payment.objects.       filter(pk=self.payment1.pk).exists())
