# import os
# from selenium.webdriver.common.by import By
# from datetime import datetime, timedelta
# from django.urls import reverse
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webapp.models import Coach
# from webapp.forms import CoachForm
#
#
# class CoachSeleniumTest(LiveServerTestCase):
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
#         self.coach2 = Coach.objects.create(
#             telegram_id='coach2',
#             phone='test_data',
#             first_name='test_data',
#             last_name='test_data',
#             email='test@data.com',
#             started_to_work=(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
#             description='test_data',
#         )
#
#     def tearDown(self) -> None:
#         self.driver.quit()
#
#     def test_coach_create(self):
#         url = self.live_server_url + reverse('webapp:coach_create')
#         self.driver.get(url)
#
#         self.driver.find_element(By.NAME, 'telegram_id').send_keys('coach3')
#         self.driver.find_element(By.NAME, 'phone').send_keys('test_data')
#         self.driver.find_element(By.NAME, 'first_name').send_keys('test_data')
#         self.driver.find_element(By.NAME, 'last_name').send_keys('test_data')
#         self.driver.find_element(By.NAME, 'email').send_keys('test@data.com')
#         self.driver.find_element(By.NAME, 'started_to_work').send_keys(datetime.now().strftime('%Y-%m-%d'))
#         self.driver.find_element(By.NAME, 'description').send_keys('test_data')
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         form = CoachForm(data={
#             "telegram_id": '11111111',
#             "phone": 'test_data',
#             "first_name": 'test_data',
#             "last_name": 'test_data',
#             "email": 'test@data.com',
#             "started_to_work": (datetime.now()).strftime('%Y-%m-%d'),
#             "description": 'test_data',
#         })
#         self.assertTrue(form.is_valid())
#         form.save()
#
#     def test_coach_update(self):
#         url = self.live_server_url + reverse('webapp:coach_update', kwargs={'pk': self.coach1.pk})
#         self.driver.get(url)
#
#         self.driver.find_element(By.NAME, 'telegram_id').clear()
#         self.driver.find_element(By.NAME, 'phone').clear()
#         self.driver.find_element(By.NAME, 'first_name').clear()
#         self.driver.find_element(By.NAME, 'last_name').clear()
#         self.driver.find_element(By.NAME, 'email').clear()
#         self.driver.find_element(By.NAME, 'started_to_work').clear()
#         self.driver.find_element(By.NAME, 'description').clear()
#
#         self.driver.find_element(By.NAME, 'telegram_id').send_keys('updated_coach')
#         self.driver.find_element(By.NAME, 'phone').send_keys('updated_coach')
#         self.driver.find_element(By.NAME, 'first_name').send_keys('updated_coach')
#         self.driver.find_element(By.NAME, 'last_name').send_keys('updated_coach')
#         self.driver.find_element(By.NAME, 'email').send_keys('updated@coach.com')
#         self.driver.find_element(By.NAME, 'started_to_work').send_keys('2023-05-05')
#         self.driver.find_element(By.NAME, 'description').send_keys('updated_coach')
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         updated_coach = Coach.objects.get(pk=self.coach1.pk)
#         self.assertEqual(updated_coach.telegram_id, 'updated_coach')
#         self.assertEqual(updated_coach.phone, 'updated_coach')
#         self.assertEqual(updated_coach.first_name, 'updated_coach')
#         self.assertEqual(updated_coach.last_name, 'updated_coach')
#         self.assertEqual(updated_coach.email, 'updated@coach.com')
#         self.assertEqual(str(updated_coach.started_to_work), '2023-05-05')
#         self.assertEqual(updated_coach.description, 'updated_coach')
#
#     def test_coach_list(self):
#         url = self.live_server_url + reverse('webapp:coach_list')
#         self.driver.get(url)
#         self.assertEqual(self.driver.title, 'Список тренеров')
#
#     def test_coach_delete(self):
#         url = self.live_server_url + reverse('webapp:coach_delete', kwargs={'pk': self.coach1.pk})
#         self.driver.get(url)
#         self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
#         self.assertFalse(Coach.objects.filter(pk=self.coach1.pk).exists())
