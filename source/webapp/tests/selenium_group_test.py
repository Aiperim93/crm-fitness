# import os
# from selenium.webdriver.common.by import By
# from datetime import datetime, timedelta, time
# from django.urls import reverse
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from django.shortcuts import get_object_or_404
# from selenium.webdriver.chrome.options import Options
# from webapp.models import Group, Coach
#
# from webapp.forms import GroupForm
#
#
# class GroupSeleniumTest(LiveServerTestCase):
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
#             coach=self.coach1,
#         )
#
#     def tearDown(self) -> None:
#         self.driver.quit()
#
#     def test_group_create(self):
#         url = self.live_server_url + reverse('webapp:group_create')
#         self.driver.get(url)
#
#         form = GroupForm(data={
#             "name": 'stretching',
#             "start_at": time(hour=6, minute=30),
#             "coach": self.coach1
#         })
#         self.assertTrue(form.is_valid())
#         form.save()
#
#         group = get_object_or_404(Group, name='stretching')
#         self.assertEqual(group.name, 'stretching')
#         self.assertEqual(group.coach, self.coach1)
#
#     def test_group_update(self):
#         url = self.live_server_url + reverse('webapp:group_update', kwargs={'pk': self.group1.pk})
#         self.driver.get(url)
#
#         self.driver.find_element(By.NAME, 'name').clear()
#         self.driver.find_element(By.NAME, 'start_at').clear()
#         self.driver.find_element(By.NAME, 'name').send_keys('Wrestling')
#         self.driver.find_element(By.NAME, 'start_at').send_keys('19:00')
#         self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
#
#         updated_group = Group.objects.get(pk=self.group1.pk)
#         self.assertEqual(updated_group.name, 'Wrestling')
#         self.assertEqual(updated_group.start_at, time(hour=19, minute=00, second=00))
#
#     def test_group_detail(self):
#         url = self.live_server_url + reverse('webapp:group_detail',  kwargs={'pk': self.group1.pk})
#         self.driver.get(url)
#         self.assertEqual(self.driver.title, 'Информация о группе')
#
#     def test_group_delete(self):
#         url = self.live_server_url + reverse('webapp:group_delete', kwargs={'pk': self.group1.pk})
#         self.driver.get(url)
#         self.driver.find_element(By.XPATH, '//form').submit()
#         self.group1.refresh_from_db()
#         self.assertFalse(self.group1.is_active)
