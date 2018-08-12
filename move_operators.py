import random


class MoveOperator:
    @staticmethod
    def apply(items, choices):
        """
        Applies the operator to the given items.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        return items


class Remove(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Removes one or more of the items from the items list. Guarantees that there will always be at least one item
        left in the list of items.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_removals = random.randrange(len(items))
        for _ in range(num_removals):
            to_remove = random.randrange(len(items))
            items = items[:to_remove] + items[to_remove + 1:]
        return items


class Add(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Adds one or more randomly picked items from the choices list to the list of items.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_inserts = random.randrange(len(items) + 1)
        for _ in range(num_inserts):
            to_insert = random.randrange(len(items))
            items = items[:to_insert] + random.choice(choices) + items[to_insert:]
        return items


class Change(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Changes one or more of the items in the item list to a randomly picked item in the choices list.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_changes = random.randrange(len(items)+1)
        items = list(items)
        for _ in range(num_changes):
            to_change = random.randrange(len(items))
            items[to_change] = random.choice(choices)
        return "".join(items)


class Swap(MoveOperator):
    @staticmethod
    def apply(items, choices):
        """
        Swaps one or more of the items with another one in the item list.
        :param items: The items to which the operator should be applied.
        :param choices: Items that the operator can inject into the items if necessary.
        :return: The list of items after the operator was applied.
        """
        num_swaps = random.randrange(len(items))
        items = list(items)
        for _ in range(num_swaps):
            idx1, idx2 = random.randrange(len(items)), random.randrange(len(items))
            items[idx1], items[idx2] = items[idx2], items[idx1]
        return "".join(items)
