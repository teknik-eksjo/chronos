import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from flask import url_for
import re

from app import mail


@pytest.mark.skip(reason='fix in the future')
def test_password_reset_email(client):
    #response = client.get(url_for('auth.password_reset_request'))
    with mail.record_messages() as outbox:
        response = client.post(url_for('auth.password_reset_request'), data = dict(
            email='hugo@hugolundin.se'))
        #assert response.status_code == 200
        assert len(outbox) == 1
        assert outbox[0].subject == '[Chronos] Reset password'
        assert 'Hugo' in outbox[0].html

        token = re.search(r'reset\/(.*)"', outbox[0].html).group(1)

        response = client.post(url_for('auth.password_reset', token=token), data = dict(
            email='hugo@hugolundin.se', password='1q2w3e4r', password2='1q2w3e4r'))
        assert response.status_code == 302

        response = client.post(url_for('auth.login'), data= dict(
            email='hugo@hugolundin.se', password='1q2w3e4r'), follow_redirects=True)
        assert response.status_code == 200


"""
@pytest.mark.usefixtures('live_server')
class TestLiveServer():

    def test_app_index(self, client):
        assert client.get(url_for('main.index')).status_code == 200

    def test_app(self, selenium):
        selenium.get(url_for('main.index', _external=True))
        assert 'Chronos' in selenium.title

    def test_email_recovery(self, selenium):
        selenium.get(url_for('auth.password_reset_request', _external=True))
        assert 'Lösenord' in selenium.title
        elem = selenium.find_element_by_name('email')
        elem.send_keys('hugo@hugolundin.se')
        elem.send_keys(Keys.RETURN)
        assert 'Ett mail med instruktioner för att återställa ditt lösenord har blivit skickat till dig.' in selenium.page_source

    def test_login(self, selenium):
        selenium.get(url_for('auth.login', _external=True))
        assert 'Login' in selenium.title
        email_element = selenium.find_element_by_name('email')
        password_element = selenium.find_element_by_name('password')
        email_element.send_keys('hugo@hugolundin.se')
        password_element.send_keys('1q2w3e4r5t6y7')
        password_element.send_keys(Keys.RETURN)
        assert 'Admin route.' in selenium.page_source

    def test_login_teacher(self, selenium):
        selenium.get(url_for('auth.login', _external=True))
        selenium.find_element_by_name('email').send_keys('hugo.lundin@outlook.com')
        selenium.find_element_by_name('password').send_keys('1q2w3e4r5t6y7', Keys.RETURN)
        assert 'Du har inte rättighet att logga in här.' in selenium.page_source
        assert 'Fel användarnamn eller lösenord.' in selenium.page_source

    def test_change_password(self, selenium):
        selenium.get(url_for('auth.login', _external=True))
        selenium.find_element_by_name('email').send_keys('hugo@hugolundin.se')
        selenium.find_element_by_name('password').send_keys('1q2w3e4r5t6y7', Keys.RETURN)
        selenium.get(url_for('auth.change_password', _external=True))
        assert 'Ändra ditt lösenord' in selenium.page_source
"""
