from django.test import TestCase

from django.test import TestCase

# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class MySeleniumTests(StaticLiveServerTestCase):
    # Carregar una BD de test (opcional si s'utilitza fixtures)
    # fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Crear usuari admin per al test
        User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')

        # Configurar Selenium en mode headless
        opts = Options()
        opts.headless = True  # Activar mode headless
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # Tanquem el navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # Anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # Comprovem que el títol de la pàgina és el que esperem
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('admin123')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # Testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

    def test_login_error(self):
        # Comprovem que amb un usuari i contrasenya inexistent, el test falla
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # Comprovem que el títol de la pàgina és el que esperem
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Introduïm dades de login incorrectes
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('usuari_no_existent')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('contrasenya_incorrecta')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # Utilitzem assertNotEqual per testejar que NO hem entrat
        self.assertNotEqual(self.selenium.title, "Site administration | Django site admin")
