import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.log import logger
from scrapy_splash import SplashRequest
import logging
from datetime import datetime
from scrapy.utils.log import configure_logging

class HospitalSpider(scrapy.Spider):
    name = "hospital_spider"    
    states_of_interest = ["PA","FL"]

    def __init__(self, *args, **kwargs): # type: ignore
        super(HospitalSpider, self).__init__(*args, **kwargs)
        # Disable existing logging configuration in settings.py
        configure_logging(install_root_handler=False)
        # #Create a new log file with a timestamp
        log_filename = f'{self.name}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

        # Configure custom logging
        logging.basicConfig(
            filename=log_filename,
            filemode='a',  # Append mode
            format='%(asctime)s [%(name)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG
        )

    def start_requests(self):
        base_url = "https://www.ahd.com/states/hospital_{}.html"
        for state in self.states_of_interest:
            url = base_url.format(state)
            yield SplashRequest(url=url, callback=self.parse, errback=self.handle_errors,
                                meta={"state": state}, args={"wait": 2.0}) # Wait 5 seconds for javascript to load

    def parse(self, response):  # type: ignore
        state = response.meta["state"]
        table = response.css(".report_table.report_large.striped")
        if not table:
            logger.error(f"No table found for {state} at {response.url}")
            return

        rows = table.css("tbody tr")
        if not rows:
            logger.warning(
                f"No data rows found in the table for {state} at {response.url}"
            )
            return

        for row in rows:
            item = self.parse_row(row, state, response.url)
            if item:
                # Join the relative URL with the base site URL
                full_profile_url = response.urljoin(item["free_profile"])
                # Create a new request to fetch details from the full profile URL
                request = scrapy.Request(full_profile_url, callback=self.parse_details)
                request.meta["item"] = item  # Pass the current item
                yield request

    def parse_row(self, row, state, url):  # type: ignore
        try:
            item = {
                "free_profile": row.css("th a::attr(href)").get(),
                "hospital_name": row.css("th a::text").get(),
                "city": row.css("td.text::text").get(),
                "state": state,
                "staffed_beds": self.parse_int_values(
                    row.xpath(".//td[2]/text()").get()
                ),
                "total_discharges": self.parse_int_values(
                    row.xpath(".//td[3]/text()").get()
                ),
                "patient_days": self.parse_int_values(
                    row.xpath(".//td[4]/text()").get()
                ),
                "gross_patient_revenue": self.parse_int_values(
                    row.xpath(".//td[5]/text()").get()
                ),
            }

            missing_fields = [key for key, value in item.items() if not value]
            if missing_fields:
                logger.error(
                    f"Missing fields {missing_fields} in item for {state} at {url}: {item}"
                )
                return item  # log missing item       
            return item
        except Exception as e:
            logger.error(f"Error parsing row: {e} in {state} at {url}")
            return None

    def parse_details(self, response): # type: ignore
        item = response.meta['item']  # Retrieve the item passed from the main page
        table = response.css(".inside-align")

        if not table:
            logger.error(f"No detailed table found at {response.url}")
            yield item  # Yield the initial item even if no additional details are found
            return

        # Extract additional details from the detailed page
        details = {
            'hospital_name_detail': table.css('b[itemprop="name"]::text').get(),
            'street_address_detail': table.css('span[itemprop="streetAddress"]::text').get(),
            'city_detail': table.css('span[itemprop="addressLocality"]::text').get(),
            'state_detail': table.css('span[itemprop="addressRegion"]::text').get(),
            'postal_code_detail': table.css('span[itemprop="postalCode"]::text').get(),
            'telephone_detail': table.css('span[itemprop="telephone"]::text').get(),
            'website_detail': table.css('a[itemprop="url"]::attr(href)').get(),
            'cms_no_detail': table.css('td.code::text').get(),
            'facility_type_detail': table.xpath('.//td[.="Type of Facility:"]/following-sibling::td[1]/text()').get(),
            'ownership_detail': table.xpath('.//td[.="Type of Control:"]/following-sibling::td[1]/text()').get(),
            'staffed_beds_detail': self.parse_int_values(table.xpath('.//td[.="Total Staffed Beds:"]/following-sibling::td[1]/text()').get()),
            'gross_patient_revenue_detail': self.parse_float_values(table.xpath('.//td[.="Total Patient Revenue:"]/following-sibling::td[1]/text()').get()),
            'total_discharges_detail': self.parse_int_values(table.xpath('.//td[.="Total Discharges:"]/following-sibling::td[1]/text()').get()),
            'patient_days_detail': self.parse_int_values(table.xpath('.//td[.="Total Patient Days:"]/following-sibling::td[1]/text()').get()),
            'quality_score_detail': self.parse_float_values(table.xpath('.//td[contains(., "TPS Quality Score:")]/following-sibling::td[1]/text()').get())
        } 

        # Update the initial item with additional details
        item.update(details)
        print(item)
        yield item

    def parse_int_values(self, value): # type: ignore
        try:
            if value is None:
                return None
            return int(value.replace("$", "").replace(",", ""))
        except (TypeError, ValueError):
            return None

    def parse_float_values(self, value): # type: ignore
        """
        Converts a string value to a float after removing commas.
        Returns None if the value is None or cannot be converted to float.
        """
        try:
            if value is None:
                return None
            return float(value.replace("$", "").replace(",", ""))
        except (TypeError, ValueError) as e:
            logger.error(f"Error converting value to float: {e}")
            return None

    def handle_errors(self, failure): # type: ignore
        if failure.check(HttpError):
            response = failure.value.response
            logger.error(f'HttpError on {response.url}: Status {response.status}, Reason: {response.reason}')
        else:
            logger.error(f'Unhandled error: {failure}')
