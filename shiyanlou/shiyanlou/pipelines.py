from sqlalchemy.orm import sessionmaker 

from shiyanlou.models import Course, engine 
#导入创建的表格映射对象



from scrapy.exceptions import DropItem 

			
class ShiyanlouPipeline(object):
	def process_item(self, item, spider): 
            item['students'] = int(item['students'])
            if item['students'] < 1000: 
            # 对于不需要的 item，raise DropItem 异常 
                    raise DropItem('Course students less than 1000.') 
            else: 
                    self.session.add(Course(**item))
            return item 
	
	def open_spider(self, spider): 
            """ 在爬虫被开启的时候，创建数据库 session""" 
            Session = sessionmaker(bind=engine) 
            self.session = Session()
		
	def close_spider(self, spider):
            """ 爬虫关闭后，提交 session 然后关闭 session""" 
            self.session.commit() 
            self.session.close()
		
