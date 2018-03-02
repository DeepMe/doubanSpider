import requests
import lxml
ACCOUNTS = ('15700084173', 'reaiwodereai1994')


def getCookies():

    # loginURL = "https://www.douban.com/accounts/login?source=main"

    # data = {
    #     'redir': 'http://movie.douban.com',
    #     'form_email': account,
    #     'form_password': passwd,
    # }
    cookie_str = 'bid=dN11rdD6nmM; __utmz=30149280.1519888933.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; \
                  ll="118172"; _vwo_uuid_v2=DFB178CB3B40550CE377C416C7CBC1CC1|c06e1dda0d69e95b7770b0590666f372; \
                  __utmc=30149280; ps=y; ap=1; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16984;\
                  __utma=30149280.1005433572.1519888933.1519966887.1519972085.5; ct=y; dbcl2="169844762:plaRXlsF6HQ";\
                   ck=-ui8; __utmb=30149280.9.10.1519972085'
    
    cookies = {}
    for cookie in [item.split('=') for item in cookie_str.replace(' ', '').split(';')]:
        cookies[cookie[0]] = cookie[1]
    
    return cookies



if __name__ == "__main__":
    print(getCookies())