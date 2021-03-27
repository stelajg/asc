"""
This module represents the Consumer.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread, RLock

lock = RLock()


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
        self.lock = RLock()

    def add_command(self, id_cart, product, quantity):
        for i in range(quantity):
            status = False
            while not status:
                status = self.marketplace.add_to_cart(id_cart, product)
                if not status:
                    time.sleep(self.retry_wait_time)

    def remove_command(self, id_cart, product, quantity):
        for i in range(quantity):
            self.marketplace.remove_from_cart(id_cart, product)

    def run(self):
        for carts in self.carts:
            id_cart = self.marketplace.new_cart()
            for i in carts:
                command = i.get('type')
                if command == 'add':
                    self.add_command(id_cart, i.get('product'), i.get('quantity'))
                else:
                    self.remove_command(id_cart, i.get('product'), i.get('quantity'))

            lock.acquire()
            brought_products = self.marketplace.place_order(id_cart)
            for i in range(len(brought_products)):
                print(self.kwargs.get('name'), "bought", brought_products[i])
            lock.release()
