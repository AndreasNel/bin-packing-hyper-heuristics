from bin import Bin


class Heuristic:
    @staticmethod
    def apply(item, bins):
        """
        Applies the heuristic to the given bins. This has to be overridden by subclasses.
        :param item: The item to add.
        :param bins: The list of bins to choose from.
        :return: The lists of bins after insertion.
        """
        return bins


class FirstFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the very first bin that it can fit it.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after the insertion.
        """
        b = next((b for b in bins if b.can_add_item(item)), None)
        if not b:
            b = Bin(bins[0].capacity)
            bins.append(b)
        b.add_item(item)
        return bins


class BestFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the bin for which the least amount of open space would be available after insertion.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after the insertion.
        """
        valid_bins = (b for b in bins if b.can_add_item(item))
        sorted_bins = sorted(valid_bins, key=lambda x: x.filled_space())
        if sorted_bins:
            b = sorted_bins[0]
        else:
            b = Bin(bins[0].capacity)
            bins.append(b)
        b.add_item(item)
        return bins


class NextFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the next available bin after the last insertion.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after insertion.
        """
        b = bins[-1]
        if not b.add_item(item):
            b = Bin(bins[0].capacity)
            bins.append(b)
            b.add_item(item)
        return bins


class WorstFit(Heuristic):
    @staticmethod
    def apply(item, bins):
        """
        Adds the item to the bin for which the most amount of open space would be available after insertion.
        :param item: The item to add.
        :param bins: The bins to choose from.
        :return: The list of bins after insertion.
        """
        valid_bins = (b for b in bins if b.can_add_item(item))
        # Note that this method is exactly the same as for the BestFit heuristic except for the following line.
        sorted_bins = sorted(valid_bins, key=lambda x: x.filled_space(), reverse=True)
        if sorted_bins:
            b = sorted_bins[0]
        else:
            b = Bin(bins[0].capacity)
            bins.append(b)
        b.add_item(item)
        return bins

