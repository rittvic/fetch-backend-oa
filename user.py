import heapq
from dateutil import parser

class User:
    """
    A User class representing a user account in the system. It stores the user's total balance, tracks points per payer
    (a producer of the item that the points were redeemed from), and maintains a priority queue (min heap) of
    transactions based on timestamp
    """
    def __init__(self, id):
        """
        Constructor for User instance.
        Maintains a list of transactions as a priority queue (min heap) and points per payers as dictionary
        Also stores user's total balance and id
        :param id: identification of the user
        """
        self.id = id
        self.balance = 0.0
        self.transactions = []
        self.payer_balances = {}

    def get_balance(self):
        """
        Retrieve the current balance of the user
        :return: user's current total balance
        """
        return self.balance

    def add_transaction(self, payer, points, timestamp):
        """
        Adds a new transaction to the priority queue based on timestamp
        :param payer: what payer the points will be added through
        :param points: how many points will be added
        :param timestamp: when the transaction takes place
        :return:
        """
        # update payer's balance and user's total balance
        self.payer_balances[payer] = self.payer_balances.get(payer, 0) + points
        self.balance += points

        # add transaction to priority queue based on timestamp. Note: does not modify the transaction data
        # Format: a tuple of (datetime), (payer, points, timestamp)
        heapq.heappush(self.transactions, (parser.isoparse(timestamp), (payer, points, timestamp)))


    def spend(self, points):
        """
        Spend the points and charge payers according to the following rules:
        1. We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re
        received)
        2. We want no payer's points to go negative

        In the event that a transaction cannot be parsed due to rule 2., it will be skipped and added back to the
        priority queue after processing has finished

        NOTE: It is guaranteed that the user has sufficient balance to spend the points if this method is called

        :param points: the points to spend
        :return: a dict mapping payers and spent / deducted points
        """
        # store spent points per payer
        spent_points = {}

        # store any transactions that must be skipped due to insufficient payer balance
        retained_transactions = []

        # no processing is needed if points to spend is 0 or less
        if points <= 0:
            return [{"payer" : payer_name, "points" : 0} for payer_name in self.payer_balances.keys()]

        self.balance -= points

        # keep processing transactions until we have spent the points or there are no more transactions left
        while (points > 0) & (len(self.transactions) > 0):
            # retrieve the earliest transaction
            earliest_transaction = heapq.heappop(self.transactions)[1]

            # parse the transaction
            payer = earliest_transaction[0]
            payer_points = earliest_transaction[1]
            timestamp = earliest_transaction[2]
            payer_balance = self.payer_balances[payer]

            to_spend = min(points,payer_points)

            # if the payer will go into negative balance, skip and store the transaction
            if (payer_balance - to_spend) < 0:
                retained_transactions.append((payer,payer_points,timestamp))
                continue

            # if payer points will not be fully deducted, then update and store the transaction
            if payer_points > to_spend:
                retained_transactions.append((payer,(payer_points-to_spend),timestamp))

            # update spend points per payer dict and payer's balance
            spent_points[payer] = spent_points.get(payer,0) + to_spend
            self.payer_balances[payer] = payer_balance - to_spend

            points -= to_spend

        # after processing, add the skipped transactions back
        for transaction in retained_transactions:
            heapq.heappush(self.transactions, (parser.isoparse(transaction[2]), transaction))

        return [{"payer" : payer_name, "points" : -payer_spent} for payer_name, payer_spent in spent_points.items()]

    def get_points_balance(self):
        """
        Retrieve the points balance per payer.
        Can be used to see how many points the user has from each payer at any given time

        :return: a dict mapping each payer with their balance
        """
        return self.payer_balances
