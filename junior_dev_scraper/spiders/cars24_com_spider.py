import scrapy
import json

# See https://www.cars24.com/ae/buy-used-cars-dubai/


class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'

    start_page = 0
    max_pages = 41
    size = 25
    city = 'city:DU_DUBAI'

    headers = {
        'X_country': 'AE',
        'X_vehicle_type': 'CAR'
    }

    def start_requests(self):

        base_url = 'https://listing-service.c24.tech/v2/vehicle?size={}&page={}&sf={}'

        while self.start_page <= self.max_pages:
            size = self.size
            page = str(self.start_page)
            city = self.city

            # Construct the URL with parameters
            api_url = base_url.format(size, page, city)

            request = scrapy.Request(
                url=api_url,
                headers=self.headers,
                callback=self.parse_json
            )
            yield request

            # Increment the page number for the next request
            self.start_page += 1

    def parse_json(self, response):
        if response.status == 200:
            # Parse JSON response from the API
            data = json.loads(response.text)

            # iterate each car and retrieve details
            for car in data['results']:
                car_id = car['appointmentId']
                make = car['make']
                model = car['model']
                year = car['year']
                city = car['city'].lower()

                deepLink = f'https://www.cars24.com/ae/buy-used-{make}-{model}-{year}-cars-{city}-{car_id}'

                item =  {
                    'Brand/Make': make,
                    'Engine size': car['engineSize'],
                    'Year of Manufacture': year,
                    'Price': car['price'],
                    'Model': model,
                    'Mileage': car['odometerReading'],
                    'FuelType': car['fuelType'],
                    'Deeplink to Car Details Page': deepLink
                }
                # Yield the extracted data
                yield item

        else:
            self.log(f'API request failed with status code {response.status_code}')


    ####### Thank you!!  ######
