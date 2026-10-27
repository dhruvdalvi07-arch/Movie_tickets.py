# Entertainment Booking System (Movies & Plays)

A lightweight, zero-dependency CLI box office and ticketing simulation built in pure Python 3. It models concurrent catalog management across cinema screens and live theatrical plays, dynamic seat layout mapping, concessions bundling, discount code parsing, transactional payment handling, and tax invoice generation.

---

## Features

- **Categorized Event Catalogs:** Distinguishes between Cinema Releases and Live Theatre Plays with independent seat allocations, pricing tiers, and runtime status.
- **Dynamic Seating Grid:** Displays seat rows facing an orientation stage/screen (`[01]` through `[16]`), dynamically replacing reserved slots with `[XX]`.
- **Multi-Seat Batch Reservation:** Accepts multi-seat inputs via flexible delimiters (e.g., `1, 2, 5` or `3 4`), automatically removing duplicates and validating boundary limits.
- **Housefull Safeguards:** 
  - Visual `[HOUSEFULL]` badges on main menu catalogs for sold-out events.
  - Early-rejection logic prevents users from entering booking flows for fully booked shows.
- **Concessions & Add-Ons:** Optional menu for adding snacks and refreshments (caramel popcorn, nachos, beverages) to the ticket transaction.
- **Promo Code Engine:** Deducts flat-rate discounts from the total bill when valid vouchers (`FIRST50`, `SHOWTIME`) are provided.
- **Transactional Payment Gateway:**
  - **Cash:** Supports incremental cash tender, displays remaining balances, refunds inserted notes upon cancellation, and calculates change return.
  - **UPI:** Simulates QR/UPI payment approvals with 4-digit PIN verification.
  - **Atomicity:** Seats are only locked into inventory after payment succeeds.
- **Itemized Tax Invoice:** Generates a structured ASCII receipt detailing invoice numbers, show titles, seat identifiers, itemized add-ons, discounts, tendered amounts, and change dispensed.

---

## System Requirements

- **Python:** Python 3.7 or higher (tested on Python 3.10+)
- **External Dependencies:** None (uses standard library built-ins exclusively)

---

## Installation & Setup

1. **Clone or Download the Repository:**
   Save the code file as `booking_system.py` in your working directory:
   ```bash
   git clone [https://github.com/your-username/entertainment-booking-system.git](https://github.com/your-username/entertainment-booking-system.git)
   cd entertainment-booking-system
