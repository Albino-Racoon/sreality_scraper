import logging
import psycopg2

class PostgreSQLPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='postgres',
            user='postgres',
            password='jasajernej'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            # Save the item to the database
            self.cursor.execute(
                "INSERT INTO sreality_scraper_items (title, image_url) VALUES (%s, %s)",
                (item['title'], item['image_url'])
            )
            self.connection.commit()
            logging.info("Item saved to the database")
        except Exception as e:
            logging.error(f"Error occurred while inserting item: {e}")
        return item

class SrealityProjectPipeline:
    def process_item(self, item, spider):
        return item
