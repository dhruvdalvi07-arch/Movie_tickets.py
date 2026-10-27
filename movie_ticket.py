# Entertainment Booking System (Movies & Plays)

events = {
    "MOVIES": {
        "M1": {
            "name": "Jailer 2",
            "price": 180,
            "total_seats": 16,
            "seats": [f"[{i:02d}]" for i in range(1, 17)]
        },
        "M2": {
            "name": "Interstellar (Re-release)",
            "price": 250,
            "total_seats": 16,
            "seats": [f"[{i:02d}]" for i in range(1, 17)]
        },
        "M3": {
            "name": "Dune: Part Two",
            "price": 220,
            "total_seats": 16,
            "seats": [f"[{i:02d}]" for i in range(1, 17)]
        }
    },
    "THEATRE PLAYS": {
        "P1": {
            "name": "Hamlet (Shakespeare Live)",
            "price": 350,
            "total_seats": 12,
            "seats": [f"[{i:02d}]" for i in range(1, 13)]
        },
        "P2": {
            "name": "Mughal-E-Azam: The Musical",
            "price": 500,
            "total_seats": 12,
            "seats": [f"[{i:02d}]" for i in range(1, 13)]
        }
    }
}

SNACKS = {
    "1": {"name": "Caramel Popcorn (L)", "price": 120},
    "2": {"name": "Cold Drink (500ml)", "price": 60},
    "3": {"name": "Nachos with Cheese", "price": 100}
}

PROMO_CODES = {
    "FIRST50": 50,
    "SHOWTIME": 100
}

receipt_counter = 5000
theatre_revenue = 0


def is_housefull(seat_list):
    return all(seat == "[XX]" for seat in seat_list)


def display_seats(seat_list, cols=4):
    print("\n  ============= STAGE / SCREEN =============")
    print("                 [ FRONT ]\n")
    for i in range(0, len(seat_list), cols):
        row = "    ".join(seat_list[i:i + cols])
        print(f"       {row}")
    print("\n  ==========================================\n")


def select_snacks():
    selected_snacks = []
    snacks_total = 0

    print("\n--- Concessions & Refreshments ---")
    for code, item in SNACKS.items():
        print(f"[{code}] {item['name']:<24} ₹{item['price']}")
    print("[0] Skip Snacks")

    choice = input("\nEnter snack numbers separated by commas (or 0 to skip): ").strip()
    if choice and choice != "0":
        items = [s.strip() for s in choice.replace(" ", ",").split(",") if s.strip()]
        for it in items:
            if it in SNACKS:
                selected_snacks.append(SNACKS[it])
                snacks_total += SNACKS[it]["price"]
            else:
                print(f"Notice: Item '{it}' not found, skipping.")
    return selected_snacks, snacks_total


def process_payment(total_payable):
    """Handles cash and UPI checkout workflows. Returns (success_bool, method, amount_paid, change)."""
    if total_payable == 0:
        return True, "Complimentary", 0, 0

    while True:
        print("\nSelect Payment Method:")
        print("[1] Cash (Box Office Counter)")
        print("[2] UPI / QR Pay")
        print("[3] Cancel Booking")
        pay_choice = input("Enter option (1/2/3): ").strip()

        if pay_choice == '1':
            payment_method = "Cash"
            inserted = 0
            while inserted < total_payable:
                remaining = total_payable - inserted
                cash_in = input(f"Tender cash (Remaining: ₹{remaining}) or type 'CANCEL': ").strip().upper()

                if cash_in == 'CANCEL':
                    if inserted > 0:
                        print(f"Refunding inserted cash: ₹{inserted}...")
                    break

                if not cash_in.isdigit() or int(cash_in) <= 0:
                    print("Invalid note/amount. Please tender a valid positive rupee denomination.")
                    continue

                inserted += int(cash_in)

            if inserted >= total_payable:
                change_given = inserted - total_payable
                return True, payment_method, inserted, change_given

        elif pay_choice == '2':
            payment_method = "UPI"
            pin = input(f"Approve ₹{total_payable} on your UPI app. Enter 4-digit UPI PIN: ").strip()
            if len(pin) == 4 and pin.isdigit():
                return True, payment_method, total_payable, 0
            else:
                print("Payment Failed: Invalid 4-digit UPI PIN. Try again.")

        elif pay_choice == '3':
            print("Booking cancelled. Returning to main menu...")
            return False, "", 0, 0
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")


print("=" * 50)
print("     WELCOME TO GRAND MULTIPLEX & THEATRE     ")
print("=" * 50)

while True:
    print("\n--- Available Shows ---")
    flat_catalog = {}
    for category, items in events.items():
        print(f"\n<< {category} >>")
        for code, details in items.items():
            flat_catalog[code] = details
            status = " [HOUSEFULL]" if is_housefull(details["seats"]) else ""
            print(f"  [{code}] {details['name']:<28} ₹{details['price']} / seat{status}")

    choice = input("\nEnter Show Code or type 'QUIT' to exit: ").strip().upper()

    if choice == "QUIT":
        print("\nThank you for visiting! Have a wonderful day.\n")
        break

    if choice not in flat_catalog:
        print("Invalid Show Code! Please pick from the list above.")
        continue

    show = flat_catalog[choice]

    # Check housefull status immediately
    if is_housefull(show["seats"]):
        print(f"\nIt's Housefull! No seats available for '{show['name']}'. Please pick another show.\n")
        continue

    print(f"\nYou selected: {show['name']} (₹{show['price']} per ticket)")
    display_seats(show["seats"])

    raw_seats = input("Enter seat numbers to book (e.g. 1, 2, 5 or 3 4): ").strip()
    if not raw_seats:
        print("No seats entered. Returning to menu.")
        continue

    # Parse and validate seat numbers
    tokens = [t.strip() for t in raw_seats.replace(",", " ").split() if t.strip()]
    selected_indices = []
    invalid_input = False

    for t in tokens:
        if not t.isdigit():
            print(f"Error: '{t}' is not a valid seat number.")
            invalid_input = True
            break
        val = int(t)
        if val < 1 or val > show["total_seats"]:
            print(f"Error: Seat {val} is outside valid range (1 to {show['total_seats']}).")
            invalid_input = True
            break
        selected_indices.append(val - 1)

    if invalid_input:
        continue

    # Deduplicate seats
    unique_indices = list(dict.fromkeys(selected_indices))

    # Check for already booked seats
    already_booked = [idx + 1 for idx in unique_indices if show["seats"][idx] == "[XX]"]
    if already_booked:
        print(f"Booking Failed! Seat(s) {already_booked} are already occupied. Please pick again.")
        continue

    # Add snacks & drinks
    snack_items, snack_total = select_snacks()

    # Calculate initial subtotal
    ticket_total = len(unique_indices) * show["price"]
    gross_total = ticket_total + snack_total
    discount = 0

    print("\n---------------- ORDER SUMMARY ----------------")
    print(f"Show Title     : {show['name']}")
    print(f"Tickets        : {len(unique_indices)} seat(s) x ₹{show['price']} = ₹{ticket_total}")
    if snack_items:
        print(f"Snacks Subtotal: ₹{snack_total}")
    print(f"Subtotal       : ₹{gross_total}")
    print("-----------------------------------------------")

    # Apply promo discount
    promo_input = input("Have a promo code? (e.g. FIRST50, SHOWTIME or press Enter to skip): ").strip().upper()
    if promo_input in PROMO_CODES:
        discount = PROMO_CODES[promo_input]
        print(f"Promo '{promo_input}' applied! You saved ₹{discount}.")
    elif promo_input:
        print("Invalid promo code. Proceeding without discount.")

    final_amount = max(0, gross_total - discount)
    print(f"Total Amount Payable: ₹{final_amount}")

    # Process Payment
    payment_success, pay_method, amount_paid, change_returned = process_payment(final_amount)

    if not payment_success:
        continue

    # Lock seats and update revenue upon confirmed payment
    for idx in unique_indices:
        show["seats"][idx] = "[XX]"

    receipt_counter += 1
    theatre_revenue += final_amount
    booked_seat_numbers = [idx + 1 for idx in unique_indices]

    # Print Official Tax Invoice & Ticket
    print("\n" + "=" * 48)
    print("               TAX INVOICE & TICKET             ")
    print("=" * 48)
    print(f"Invoice No   : #{receipt_counter:<14} Payment: {pay_method}")
    print(f"Show Title   : {show['name']}")
    print(f"Seats Booked : {', '.join(f'Seat {n}' for n in booked_seat_numbers)}")
    print("------------------------------------------------")
    print(f"Ticket Charges ({len(booked_seat_numbers)}x) : ₹{ticket_total}")
    if snack_items:
        snack_names = ", ".join([s['name'] for s in snack_items])
        print(f"Snacks Added   : {snack_names}")
        print(f"Snack Charges  : ₹{snack_total}")
    if discount > 0:
        print(f"Promo Discount : -₹{discount}")
    print("-" * 48)
    print(f"TOTAL PAID     : ₹{final_amount}")
    if pay_method == "Cash":
        print(f"Tendered Cash  : ₹{amount_paid}")
        if change_returned > 0:
            print(f"Change Dispensed: ₹{change_returned}")
    print("=" * 48)
    print("STATUS: CONFIRMED")
    if change_returned > 0:
        print(f"Please collect your change of ₹{change_returned} from the counter.")

    if is_housefull(show["seats"]):
        print(f"\nNotice: '{show['name']}' has officially reached HOUSEFULL capacity!")

    print("Enjoy your show!\n")
