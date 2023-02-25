# Get an SMS message when a new phone number is added to the website
import scrapy
from twilio.rest import Client
import dotenv

# Load environment variables from .env file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# Set up Twilio API credentials
account_sid = dotenv.get_key(dotenv_file, 'TWILIO_ACCOUNT_SID')
auth_token = dotenv.get_key(dotenv_file, 'TWILIO_AUTH_TOKEN')
twilio_phone_number = dotenv.get_key(dotenv_file, 'TWILIO_PHONE_NUMBER')
my_phone_number = dotenv.get_key(dotenv_file, 'TO_PHONE_NUMBER')
last_used_number = dotenv.get_key(dotenv_file, 'LAST_USED_NUMBER')

# Define the Spider class to scrape the website


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['smsreceivefree.com', 'anonymsms.com']
    # 'https://smsreceivefree.com/country/canada'
    start_urls = ["https://anonymsms.com/united-states/"]
    info_url = 'https://smsreceivefree.com/info/'

    def parse(self, response):
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
        if current_phone_number != last_used_number:

            print(account_sid, auth_token, twilio_phone_number)
            # Send an SMS message using Twilio API
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'{current_phone_number} \n {self.info_url}',
                from_=twilio_phone_number,
                to=my_phone_number
            )

            # # Print a confirmation message to the console
            self.logger.info(f'Sent SMS message: {message.sid}')

            # Update the previous phone number variable
            dotenv.set_key(dotenv_file, 'LAST_USED_NUMBER',
                                        current_phone_number)


# Run the spider
if __name__ == '__main__':
    # Initialize the Spider class and run it
    phone_spider = PhoneSpider()
    print(phone_spider)
    phone_spider.logger.info('Starting Spider')
    phone_spider.start_requests()