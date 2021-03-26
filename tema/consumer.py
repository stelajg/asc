"""
This module represents the Consumer.
Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super().__init__()
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    @staticmethod
    def add_command(product, quantity):
        print("i am in add", product, quantity)
        pass

    @staticmethod
    def remove_command(product, quantity):
        print("i am in remove", product, quantity)
        pass

    def run(self):
        print(self.carts)
        # aux = self.carts[0][0]
        # aux1 = aux.items()
        # print(self.carts[0][0].get('type'))
        # print(list(self.carts[0][0].keys())[0])
        print(self.kwargs)
        for i in self.carts[0]:
            command = i.get('type')
            if command == 'add':
                self.add_command(i.get('product'), i.get('quantity'))
            else:
                self.remove_command(i.get('product'), i.get('quantity'))


