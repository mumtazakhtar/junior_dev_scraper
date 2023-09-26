import scrapy
import json

# See https://www.cars24.com/ae/buy-used-cars-dubai/


class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'
    start_urls = ['https://www.cars24.com/ae/buy-used-cars-dubai/']

    def parse(self, response):
        # For each car card we have to take the details
        for car_ad in response.css('div.js-content div._2SmYR div._2FYd1 div._2D_SX div.E9IPg div._1x-Oq div'):
            fuel_type_link = car_ad.css('a._1Lu5u::attr(href)').get()

            car_details = {
                'Brand/Make': car_ad.css('div._3svGJ div._3TSwN h3.RZ4T7::text').get(),
                'Engine Size': car_ad.css('div._3svGJ div._3TSwN ul._3ZoHn li:nth-child(3)::text').get(),
                'Year of Manufacture': car_ad.css('div._3svGJ div._3TSwN p._1i1E6::text').get(),
                'Deeplink to Car Details Page': car_ad.css('a._1Lu5u::attr(href)').get(),
                'Price': car_ad.css('div._1U5xD div._3aEWp div.aApXW span._7yds2::text').get(),
                'Model': car_ad.css('div._3svGJ div._3TSwN p._1i1E6::text').get(),
                'Mileage': car_ad.css('div._3svGJ div._3TSwN ul._3ZoHn li:nth-child(2)::text').get(),
            }

            # Now To get the fuel type we need to go to a deep link and look for the selector
            if fuel_type_link:
                print(fuel_type_link)
                # Follow the deep link to scrape the fuel_type
                yield response.follow(fuel_type_link, self.parse_fuel_type, meta={'car_details': car_details})

    def parse_fuel_type(self, response):
        # Extract the fuel_type from the deep link page
        fuel_type = response.css('div.js-content div div div div.container div._3W52w div.v4Cmb div div div.UxBq3 div._148U_._3oj4O div._2y04X:nth-child(6) div._29uRd div._1xlKo p.v2mgh::text').get()

        if fuel_type:
            fuel_type = fuel_type
        else:
            fuel_type = 'Not Available'

        # Add the fuel_type to the car_fields dictionary
        car_details = response.meta['car_details']
        car_details['Fuel Type'] = fuel_type

        # Yield the complete car_fields dictionary as the result
        yield car_details


    ####### Thank you!!  ######
