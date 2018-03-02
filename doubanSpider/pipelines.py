# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from doubanSpider.items import MovieItem, InformationItem, CommentItem

class DoubanspiderPipeline(object):

    def open_spider(self, spider):
        self.movie_file = open('movie.jl', 'a+')
        self.comment_file = open('comment.jl', 'a+')
        self.informaiton_file = open('information.jl', 'a+')

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            line = json.dumps(dict(item)) + "\n"
            self.movie_file.write(line)

        if isinstance(item, CommentItem):
            line = json.dumps(dict(item)) + "\n"
            self.comment_file.write(line)
        
        if isinstance(item, InformationItem):
            line = json.dumps(dict(item)) + '\n'
            self.informaiton_file.write(line)

        return item

    def close_spider(self, spider):
        self.movie_file.close()
        self.comment_file.close()
        self.informaiton_file.close()
