# -*- coding: utf-8 -*- 
import scrapy 
from shiyanlou.items import CourseItem #导入Items


class CoursesSpider(scrapy.Spider): 
	name = 'courses'  

	@property 
	def start_urls(self): 
		url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}' 
		return (url_tmpl.format(i) for i in range(1, 23)) 
	#start_urls这个和之前一样

	def parse(self, response): 
            for course in response.css('div.course-body'): 
            # 将返回结果包装为 CourseItem 其它地方同上一节 
                    item = CourseItem({ 
                            'name': course.css('div.course-name::text').extract_first(), 
                            'description': course.css('div.course-desc::text').extract_first(), 
                            'type': course.css('div.course-footer span.pull-right::text').extract_first(default='免费'), 
                            'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*') }) 
                            #顺序要和Items.py里面写的一样
                    
                    yield item  #for每一次循环都要变成CourseItem传出去
