# -*- coding: utf-8 -*-
import six
from six.moves.urllib import request
from json_schema_generator.generator import SchemaGenerator


class Recorder(object):

    def __init__(self, generator):
        self.generator = generator

    @staticmethod
    def open_with_basic_auth(url, auth):
        """
        opens an url protected with basic http authentication
        :param url: string - the url to open
        :param auth:
        :return:
        """
        user, passwd = auth
        p = six.moves.urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, url, user, passwd)
        auth_handler = six.moves.urllib.request.HTTPBasicAuthHandler(p)
        opener = request.build_opener(auth_handler)
        request.install_opener(opener)
        return opener.open(url)

    @classmethod
    def from_url(cls, url, auth=None):

        json_data = Recorder.open_with_basic_auth(
            url).read() if auth else request.urlopen(url).read()
        generator = SchemaGenerator.from_json(json_data.decode('utf-8'))

        return cls(generator)

    def save_json_schema(self, file_path, **kwargs):
        json_schema_data = self.generator.to_json(**kwargs)

        with open(file_path, 'w') as json_schema_file:
            json_schema_file.write(json_schema_data)

