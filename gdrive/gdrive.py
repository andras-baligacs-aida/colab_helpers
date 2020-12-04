from io import StringIO
# taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests


def google_link_share(link: str, binary_file: bool = False, text_encoding: str = 'utf-8'):
    """
    Provides a method to open a file on Google Drive via link with pandas.read_csv()
    or pandas.read_excel(). Might work with others, not tested yet.

    Args
    ----
    *  `link` *:str* Link to the shared file. Google share links look like
       https://drive.google.com/file/d/1uaDAGFiRmNj80FimGnHH5hNENkvjCYHv/view?usp=sharing
    *  `binary_file` *:bool (default False)* For read_csv the response must be a
        text string-like object, use `binary_file=False`
        For read_excel() the response must be the http response undecoded, so use
        `binary_file=True`
    *  `text_encoding` *:str (default='utf-8)* For text (binary_file==False) answers
        the encoder to be used to encode the bytestream to text.

    Example
    --------
    1. CSV File Sample (Foodfacts)
       ```
       pd.read_csv(google_link_share(link = 'https://drive.google.com/file/d/1VfVc50zIj4ccU3tom5YiIPIC4B3EE_Di/view?usp=sharing'),
                    nrows=10)
       ```
       :param link:
       :param binary_file:
       :param text_encoding:
    """

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    baseurl = 'https://drive.google.com'
    if '/' in link:  # it looks like a full URL
        link = link.split('/')[-2]
    URL = baseurl + '/uc?export= ' + link
    session = requests.Session()
    response = session.get(URL, params={'id': link}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': link, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    sr = response
    if binary_file:
        return sr.content
    # text file encoding
    sr.encoding = text_encoding
    return StringIO(sr.text)