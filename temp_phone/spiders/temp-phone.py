# Get an SMS message when a new phone number is added to the website
import os
from scrapy import Spider
from twilio.rest import Client
from scrapy.exceptions import CloseSpider

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Define the Spider class to scrape the website


class PhoneSpider(Spider):
    name = 'phone'
    allowed_domains = ['smsreceivefree.com', 'anonymsms.com']
    # 'https://smsreceivefree.com/country/canada'
    start_urls = ["https://anonymsms.com/united-states/"]
    info_url = 'https://smsreceivefree.com/info/'
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        # get the last used phone number from args
        self.last_used_number = kwargs.get('num')
        # get the last used phone number from a .txt file
        # with open('last_used_number.txt', 'r') as f:
        #     number = f.read().strip()
        # # Set the last used phone number as a class attribute
        # self.last_used_number = number
        

    def parse(self, response):
        # Set up environment variables
        self.account_sid = self.settings.get("TWILIO_ACCOUNT_SID")
        self.auth_token = self.settings.get("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = self.settings.get("TWILIO_PHONE_NUMBER")
        self.my_phone_number = self.settings.get("TO_PHONE_NUMBER")
        # # Find the phone number element on the page
        # phone_number_element = response.css(
        #     '.row .col-sm-8 a:first-child::text')
        # print(phone_number_element)

        # # Get the current phone number from the element
        # current_phone_number = phone_number_element.get().strip()
        # print(current_phone_number)

        # # add the phone number to the info url
        # self.info_url = self.info_url + current_phone_number

        # Get the href attribute of the first 'a' inside a 'main' element
        self.info_url = response.css('main a:first-child::attr(href)').get()

        # remove the last character from the url if it is a '/'
        self.info_url = self.info_url[:-
                                      1] if self.info_url[-1] == '/' else self.info_url
        current_phone_number = self.info_url.split('/')[-1]

        # Check if the current phone number is different from the previous phone number
        if current_phone_number != self.last_used_number:

            print(self.account_sid, self.auth_token, self.twilio_phone_number)
            # Send an SMS message using Twilio API
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(
                body=f'\n{current_phone_number} \n {self.info_url}',
                from_=self.twilio_phone_number,
                to=self.my_phone_number
            )

            # # Print a confirmation message to the console
            self.logger.info(f'Sent SMS message: {message.sid}')

            # stop the periodic job
            # Raise the CloseSpider exception to stop the spider
            raise CloseSpider('Condition met')

            # # Save the current phone number to a new .txt file
            # with open('last_used_number.txt', 'w') as f:
            #     f.write(current_phone_number)


# Run the spider
if __name__ == '__main__':
    # Initialize the Spider class and run it
    phone_spider = PhoneSpider()
    phone_spider.logger.info('Starting Spider')
    phone_spider.start_requests()
