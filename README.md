# POC of Splitting IP Address Ranges

- Creates several subsets of IP Addresses, by counting the subnet sizes.
- Calculates ideal subset using BlackJack mechanics, followed by a simple Round-Robin to clear the remaining entries from the list. 
- DOES NOT SPLIT SUBNETS - Decent distribution for 1:300-600 (1 subset per 300-600 ips).
