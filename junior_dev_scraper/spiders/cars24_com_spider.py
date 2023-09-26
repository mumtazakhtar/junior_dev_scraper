import scrapy
import json
import re
# from benedict import benedict
from w3lib.url import add_or_replace_parameter

# See https://www.cars24.com/ae/buy-used-cars-dubai/


class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'
    # url that needs to be scarped.
    start_urls = ['https://www.cars24.com/ae/buy-used-cars-dubai/']

    # Getting the data from the url:
    def parse(self, response):
    # For each car card we have to take the details
        print("car_ad_1")
        for car_ad in response.css('div.js-content'):
            print("car_ad_2")
            car_details = {
                'Brand_Make': car_ad.css('div._3svGJ div._3TSwN h3.RZ4T7::text').get(),
                'Engine_Size': car_ad.css('div._3svGJ div._3TSwN ul._3ZoHn li:nth-child(3)::text').get(),
                'Year_of_Manufacture': car_ad.css('div._3svGJ div._3TSwN p._1i1E6::text').get(),
                'Deeplink_to_Car_Details_Page': car_ad.css('a._1Lu5u::attr(href)').get(),
                'Price': car_ad.css('div._1U5xD div._3aEWp div.aApXW span._7yds2::text').get(),
                'Model': car_ad.css('div._3svGJ div._3TSwN p._1i1E6::text').get(),
                'Mileage': car_ad.css('div._3svGJ div._3TSwN ul._3ZoHn li:nth-child(2)::text').get(),
            }

        ## Now To get the fuel type we need to go to a deep link and look for the selector
        # Using a CSS selector to target the deep link for fuel_type
            fuel_type_link = car_ad.css('a._1Lu5u::attr(href)').get()

            if fuel_type_link:
                # Follow the deep link to scrape the fuel_type
                yield response.follow(fuel_type_link, self.parse_fuel_type, meta={'car_details': car_details})

    def parse_fuel_type(self, response):
        # Extract the fuel_type from the deep link page
        fuel_type = response.css('div._148U_ _3oj4O div._2y04X div._1xlKo p.v2mgh:nth-child(6)::text').get()

        if fuel_type:
            fuel_type = fuel_type.strip()
        else:
            fuel_type = 'Not Available'

        # Retrieve the car fields from the meta dictionary
        car_details = response.meta['car_details']

        # Add the fuel_type to the car_fields dictionary
        car_details['fuel_type'] = fuel_type

        # Yield the complete car_fields dictionary as the result
        yield car_details


    ####### Thank you!!  ######
