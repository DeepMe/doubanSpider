# -*- coding: utf-8 -*-

import requests
import re
import json
import logging
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import Spider
from doubanSpider.items import MovieItem, InformationItem, CommentItem
from bs4 import BeautifulSoup as bs
from doubanSpider.cookies import getCookies

class doubanSpider(Spider):

    name = 'doubanSpider'
    start_urls = ['26861685']

    def start_requests(self):
        for movie_id in self.start_urls:
            yield Request(url='https://movie.douban.com/subject/{}/'.format(movie_id), cookies=getCookies(), callback=self.parse_movie)

    def parse_movie(self, response):

        movieItem = MovieItem()

        selector = Selector(response)

        try:
            _id = response.url.split('/')[-2]
            Title = selector.xpath('//span[@property="v:itemreviewed"]/text()').extract()
            Rating  = selector.xpath('//div[@typeof="v:Rating"]/strong[@property="v:average"]/text()').extract()
            Types = selector.xpath('//span[@property="v:genre"]/text()').extract()
            Director = selector.xpath('//a[@rel="v:directedBy"]/text()').extract()
            Actor = selector.xpath('//a[@rel="v:starring"]/text()').extract()
            InitialReleaseDate = selector.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()

            if _id:
                movieItem["_id"] = _id
            if Title:
                movieItem['Title'] = Title[0]
            if Rating:
                movieItem['Rating'] = Rating[0]
            if Types:
                movieItem['Type'] = ''.join([item+',' for item in Types])[:-1]
            if Director and len(Director) < 2:
                movieItem['Director'] = Director[0]
            else:
                movieItem['Director'] = ''.join([item+',' for item in Director])[:-1]
            if Actor:
                movieItem['Actor'] = ''.join([item+',' for item in Actor])[:-1]
            if InitialReleaseDate:
                movieItem['InitialReleaseDate'] = InitialReleaseDate[0][:10]
                        
        except Exception:
            print('error')
        else:
            yield movieItem
        yield Request(url='https://movie.douban.com/subject/{}/comments?start=0&limit=20&sort=new_score&status=P&percent_type='.format(_id), \
                      meta={'movie_id': _id}, cookies=getCookies(), callback=self.parse_comment)
    

    def parse_comment(self, response):

        soup = bs(response.text, "lxml")

        comments = soup.find_all('div', attrs={'class':'comment-item'})
        MovieID = response.url.split('/')[4]

        for comment in comments:

            commentItem = CommentItem()
            commentItem['MovieID'] = MovieID

            _id = comment['data-cid']
            Vote = comment.find('span', attrs={'class':'votes'}).string
            Avatar = comment.find('span', attrs={'class':'comment-info'}).a['href']
            CommentTime = comment.find('span', attrs={'class': 'comment-time'}).string
            Content = comment.p
            Rating = comment.find('span', attrs={'class':re.compile('(.*?)rating')})
            if _id:
                commentItem['_id'] = _id
            if Vote:
                commentItem['Vote'] = Vote
            if Avatar:
                commentItem['Avatar'] = Avatar.split('/')[-2]
            if CommentTime:
                commentItem['CommentTime'] = CommentTime.replace('\n', '').replace(' ', '')
            if Rating:
                commentItem['Rating'] = Rating['class'][0][-2]+'.'+Rating['class'][0][-1]
            if Content:
                commentItem['Content'] = Content.get_text()

            yield commentItem
            yield Request(url=Avatar, cookies=getCookies(), callback=self.parse_information)
        
        next_url = soup.find('a', attrs={'class':'next'})
        if next_url:
            yield Request('https://movie.douban.com/subject/{}/comments'.format(MovieID) + next_url['href'], cookies=getCookies(), callback=self.parse_comment)
    

    def parse_information(self, response):

        informationItem = InformationItem()
        selector = Selector(response)

        _id = response.url.split('/')[-2]
        informationItem['_id'] = _id
        
        try:
            NickName = selector.xpath('//div[@id="db-usr-profile"]/div[@class="info"]/h1/text()').extract()
            HeadshotURL = selector.xpath('//div[@class="basic-info"]/img/@src').extract()
            City = selector.xpath('//div[@class="basic-info"]//a/text()').extract()
            RegisteredTime = selector.xpath('//div[@class="basic-info"]//div[@class="pl"]/text()').extract()
            NumFollowers = selector.xpath('//div[@id="friend"]//a/text()').extract()
            FollowersURL = selector.xpath('//div[@id="friend"]//a/@href').extract()
            NumFans = selector.xpath('//p[@class="rev-link"]/a/text()').extract()
            FansURL = selector.xpath('//p[@class="rec-link"]/a/@href').extract()

            if NickName:
                informationItem['NickName'] = NickName[0].replace('\n', '').replace(' ', '')
            if HeadshotURL:
                informationItem['HeadshotURL'] = HeadshotURL[0]
            if City:
                informationItem['City'] = City[0]
            if RegisteredTime:
                informationItem['RegisteredTime'] = RegisteredTime[1].replace(' ', '')[:10]
            if NumFollowers:
                informationItem['NumFollowers'] = re.findall(r'\d+', NumFollowers[0])[0]
            if NumFans:
                informationItem['NumFans'] = re.findall(r'\d+', NumFans[0])[0]
            
            yield informationItem
        
        except Exception as e:
            print(e)



    


                

            
            

        
    