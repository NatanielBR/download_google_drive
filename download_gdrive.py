import re
import httplib2
import requests



class Drive:
    def __get_confirm_token(self, response):
        '''
        Method to receive a token from google to confirm
        the download
        :param response:
        :return a token String or None if token is not found:
        '''
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def get_download_link_direct(self, id):
        """
        Method to get a download link from id.
        Note: If video, the link not contains quality
        indicator.
        :param id of file:
        :return the link for download:
        """
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params={'id': id}, stream=True)
        token = self.__get_confirm_token(response)

        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)
        return response.url

    def video_stream(self, id):
        """
        Method to get stream url from video id but in my tests
        its not work :(.
        :param id Video ID:
        :return The dictionary with quality indicator as key and url as value.:
        """
        # requests not work appropriately, but httplib2 works!
        h = httplib2.Http('.cache')
        data = h.request(f'https://drive.google.com/file/d/{id}/view?pli=1')[1].decode('unicode_escape')
        data = data.split(',["fmt_stream_map","')
        data = data[1].split('"]')

        data = data[0]

        data = str(data).split(',')
        data.sort()
        saida = {}
        for list in data:
            data2 = list.split('|')
            data2[0] = data2[0].replace("'", '')
            data2[0] = int(data2[0])
            if data2[0] == 37:
                saida['1080p'] = (re.sub("/\/[^\/]+\.google\.com/", "/redirector.googlevideo.com/", data2[1]))
            elif data2[0] == 22:
                saida['720p'] = (re.sub("/\/[^\/]+\.google\.com/", "/redirector.googlevideo.com/", data2[1]))
            elif data2[0] == 59:
                saida['720p'] = (re.sub("/\/[^\/]+\.google\.com/", "/redirector.googlevideo.com/", data2[1]))
            elif data2[0] == 18:
                saida['360p'] = (re.sub("/\/[^\/]+\.google\.com/", "/redirector.googlevideo.com/", data2[1]))

        return saida
