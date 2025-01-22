import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


class WhiskeyItem(scrapy.Item):
    _id = scrapy.Field()

    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    category = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    distiller = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    bottler = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    abv = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    age = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    srp = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )
    img = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join('')
    )

