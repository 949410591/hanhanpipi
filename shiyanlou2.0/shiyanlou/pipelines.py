from sqlalchemy.orm import sessionmaker 

from shiyanlou.models import Course, engine, User 
#导入创建的表格映射对象
from datetime import datetime 
from shiyanlou.items import CourseItem, UserItem


from scrapy.exceptions import DropItem 

			
class ShiyanlouPipeline(object):
    def process_item(self, item, spider): 
        if isinstance(item,CourseItem):
            self._process_course_item(item)
        else:
            self._process_user_item(item)


        return item

    def _process_course_item(self, item):
        item['students'] = int(item['students'])
        self.session.add(Course(**item))
        
    def _process_user_item(self, item):
        item['level'] = int(item['level'][1:])
        item['join_date'] = datetime.strptime(item['join_date'].split()[0], '%Y-%m-%d').date()
        item['learn_courses_num'] = int(item['learn_courses_num'])
        self.session.add(User(**item))



    def open_spider(self, spider): 
        """ 在爬虫被开启的时候，创建数据库 session""" 
        Session = sessionmaker(bind=engine) 
        self.session = Session()
            
    def close_spider(self, spider):
        """ 爬虫关闭后，提交 session 然后关闭 session""" 
        self.session.commit() 
        self.session.close()
            
