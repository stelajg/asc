"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Condition, Lock, Semaphore, RLock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.id_producer = -1
        self.id_carts = -1
        self.producers_list = []
        self.market_contains = []
        self.carts_contains = []
        self.wait_condition_for_producing_prod = Condition()
        self.lock_producers = RLock()
        self.lock_consumers = RLock()
        self.number_of_orders_placed = -1
        self.consumersSemaphore = Semaphore(0)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.lock_producers.acquire()
        self.id_producer += 1
        self.market_contains.append([])
        self.producers_list.append(self.queue_size_per_producer)
        self.lock_producers.release()
        return self.id_producer

    def publish(self, producer_id, product, wait_time):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        if self.producers_list[producer_id] != 0:
            #self.wait_condition_for_producing_prod.acquire()
            self.market_contains[producer_id].append([product, True])
            self.producers_list[producer_id] -= 1
            time.sleep(wait_time)
            #self.wait_condition_for_producing_prod.release()
            self.consumersSemaphore.release()
            return True
        else:
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.lock_consumers.acquire()
        self.id_carts += 1
        self.carts_contains.append([])
        self.lock_consumers.release()
        return self.id_carts

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.consumersSemaphore.acquire()
        for lists in self.market_contains:
            for item in lists:
                if item[0] is product and item[1] is True:
                    self.carts_contains[cart_id].append(product)
                    self.producers_list[self.market_contains.index(lists)] += 1
                    item[1] = False
                    return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart

        """
        self.carts_contains[cart_id].remove(product)
        for lists in self.market_contains:
            for item in lists:
                if item[0] is product and item[1] is False:
                    self.producers_list[self.market_contains.index(lists)] -= 1
                    item[1] = True
        self.consumersSemaphore.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.number_of_orders_placed += 1
        return self.carts_contains[cart_id]

    def number_of_orders(self):
        if self.number_of_orders_placed == self.id_carts:
            return False
        return True
