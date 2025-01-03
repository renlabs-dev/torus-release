#!/usr/bin/env python3

from communex.client import CommuneClient
import json

# Multiplier to change decimals from 9 to 18
MULTIPLIER = 10**9

# Minimum balance for the address to be included (0.1 TOR)
MIN_BALANCE_THRESHOLD = 10**18 // 10

def process_bridged_balances(api_url: str = "wss://api.communeai.net") -> list[tuple[str, int]]:
    """
    Process and filter bridged balances from Commune.
    """
    client = CommuneClient(url=api_url)

    print("Querying bridged balances...")

    bridged_balances = client.query_map("Bridged", extract_value=False)["Bridged"]

    total_num_balances = len(bridged_balances)

    print(f"Total number of addresses: {total_num_balances}")

    print("Processing balances...")

    num_filtered_balances = 0
    filtered_balances: list[tuple[str, int]] = []

    for address, balance in bridged_balances.items():
        # Adjusts balance decimals
        balance = balance * MULTIPLIER

        if balance >= MIN_BALANCE_THRESHOLD:
            filtered_balances.append((address, balance))
        else:
            print(f"Address {address} is below the minimum threshold of {MIN_BALANCE_THRESHOLD / 10**18} TOR with balance {balance / 10**18:e} TOR ")
            num_filtered_balances += 1

    print(f"Number of addresses filtered out: {num_filtered_balances}")
    print(f"Number of address remaining: {total_num_balances - num_filtered_balances}")

    print("Sorting addresses...")

    filtered_balances.sort(key=lambda x: x[0])

    return filtered_balances

def main():
    balances_list = process_bridged_balances()

    with open('balances.json', 'w') as f:
        json.dump(balances_list, f, indent=2)


if __name__ == "__main__":
    main()
