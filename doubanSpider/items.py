# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MovieItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()
    Title = Field()
    Rating = Field()
    Type = Field()
    Director = Field()
    Actor = Field()
    InitialReleaseDate = Field()


class InformationItem(Item):
    _id = Field()
    NickName = Field()
    HeadshotURL = Field()
    City = Field()
    Gender = Field()
    RegisteredTime = Field()
    Introduction = Field()
    NumFans = Field()
    NumFollowers = Field()
    Fans = Field()
    Followers = Field()


class CommentItem(Item):
    _id = Field()
    MovieID = Field()
    Avatar = Field()
    Vote = Field()
    CommentTime = Field()
    Rating = Field()
    Content = Field()
