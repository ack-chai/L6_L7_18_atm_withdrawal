def notes_needed(amount):
    if amount is None or not isinstance(amount, str):
        return 0
    clean = amount.replace(',', '').strip()
    try:
        val = int(clean)
        if val < 0:
            return 0
        return val // 100
    except (ValueError, TypeError):
        return 0

def mask_card(card_number):
    if card_number is None or not isinstance(card_number, str):
        return "XXXX XXXX XXXX XXXX"
    groups = card_number.strip().split()
    if len(groups) >= 4:
        return "XXXX XXXX XXXX " + groups[3]
    elif len(groups) == 1 and len(groups[0]) >= 4:
        return "XXXX XXXX XXXX " + groups[0][-4:]
    return "XXXX XXXX XXXX XXXX"

def average_withdrawal(amounts_csv):
    if amounts_csv is None or not isinstance(amounts_csv, str):
        return 0
    amounts = []
    for a in amounts_csv.split(','):
        a_clean = a.replace(',', '').strip()
        try:
            amounts.append(int(a_clean))
        except (ValueError, TypeError):
            continue
    if not amounts:
        return 0
    return sum(amounts) // len(amounts)

def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result)

if __name__ == "__main__":
    main()
