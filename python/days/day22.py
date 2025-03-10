from collections import Counter
from utils import utils


def part_1():
    with open("inputs/day22.txt", "r") as f:
        text = f.read()
    total = 0
    for num in utils.ints(text):
        for _ in range(2000):
            num = (num ^ (num << 6)) & 0xffffff
            num = (num ^ (num >> 5))
            num = (num ^ (num << 11)) & 0xffffff
        total += num
    return total

def part_2():
    with open("inputs/day22.txt", "r") as f:
        text = f.read()

    price_change_values: Counter = Counter()

    for num in utils.ints(text):
        prices = [num % 10]
        for _ in range(2000):
            num = num ^ (num << 6) & 0xffffff
            num = num ^ (num >> 5)
            num = num ^ (num << 11) & 0xffffff
            prices.append(num % 10)
        price_diffs = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        seen_price_diffs = set()
        for i in range(4, len(price_diffs)):
            sequence = tuple(price_diffs[i - 4:i])
            if sequence in seen_price_diffs:
                continue
            else:
                seen_price_diffs.add(sequence) 
                price_change_values[sequence] += prices[i] # thought for sure this would be an off by one error
    
    return max(price_change_values.values())
