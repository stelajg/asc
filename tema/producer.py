"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__()
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    def helper_run(self, producer_id, command_info):
        for i in range(command_info[1]):
            self.marketplace.publish(producer_id, command_info[0], command_info[2])
            time.sleep(self.republish_wait_time)

    def run(self):
        id_prod = self.marketplace.register_producer()
        while True:
            for i in self.products:
                self.helper_run(id_prod, i)
