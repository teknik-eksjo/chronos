from selenium import webdriver
import pytest
from flask import url_for


@pytest.mark.usefixtures('live_server')
class TestLiveServer():

    def test_app_index(self, client):
        assert client.get(url_for('main.index')).status_code == 200

    def test_app(self, selenium):
        selenium.get(url_for('main.index', _external=True))
        assert 'Chronos' in selenium.title
