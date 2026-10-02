# Mrs Viola Digital POS

# ---------------------------------------------------------
# Component A: Input Validation
# ---------------------------------------------------------

def prompt_quantity(item_name):
    """
    Continuously prompts for a quantity until the clerk
    enters a numeric value strictly greater than 0.0.
    """
    while True:
        value = input(f"Enter quantity for {item_name}: ").strip()

        if value == "":
            print("Error: Quantity cannot be empty.")
            continue

        try:
            quantity = float(value)

            if quantity <= 0:
                print(f"Error: Quantity must exceed 0.0")
                continue

            return quantity

        except ValueError:
            print("Error: Please enter a valid numeric quantity.")


# ---------------------------------------------------------
# Component B: Business Logic Functions
# ---------------------------------------------------------

def calculate_item_price(item_type, quantity, customer_type='retail'):
    """
    Calculate the price of a produce item.

    Retail:
        Tomatoes: 3,000/kg
        Red Onions: 2,500/kg
        Matooke: 25,000/bunch

        Tomatoes and onions receive 5% discount only
        on quantity above 5 kg.

    Wholesale:
        Tomatoes: 2,400/kg
        Red Onions: 2,000/kg
        Matooke: 20,000/bunch if quantity >= 3.
        Otherwise, standard retail price applies.
    """

    item_type = item_type.lower().strip()
    customer_type = customer_type.lower().strip()

    # Standard retail prices
    retail_prices = {
        "tomatoes": 3000,
        "red onions": 2500,
        "matooke": 25000
    }

    # Wholesale prices
    wholesale_prices = {
        "tomatoes": 2400,
        "red onions": 2000,
        "matooke": 20000
    }

    if item_type not in retail_prices:
        raise ValueError("Unknown produce item.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    # -----------------------------
    # Wholesale pricing
    # -----------------------------
    if customer_type == "wholesale":

        # Matooke wholesale minimum is 3 bunches
        if item_type == "matooke":
            if quantity >= 3:
                return quantity * wholesale_prices[item_type]
            else:
                return quantity * retail_prices[item_type]

        # Tomatoes and onions use wholesale flat pricing
        return quantity * wholesale_prices[item_type]

    # -----------------------------
    # Retail pricing
    # -----------------------------
    if customer_type == "retail":

        base_price = retail_prices[item_type]

        # Discount only applies to tomatoes and onions
        # above 5 kg.
        if item_type in ("tomatoes", "red onions") and quantity > 5:
            first_five = 5
            excess_quantity = quantity - 5

            normal_cost = first_five * base_price
            discounted_cost = excess_quantity * base_price * 0.95

            return normal_cost + discounted_cost

        return quantity * base_price

    raise ValueError("Customer type must be 'retail' or 'wholesale'.")


def apply_market_levy_and_packaging(subtotal, needs_eco_crate=False):
    """
    Adds:
        - 1% market council sanitation fee
        - 5,000 refundable eco-crate deposit if requested

    Returns the total payable amount.
    """

    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative.")

    sanitation_fee = subtotal * 0.01

    crate_deposit = 5000 if needs_eco_crate else 0

    total = subtotal + sanitation_fee + crate_deposit

    return total


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def format_currency(amount):
    """Format a number as Ugandan Shillings."""
    return f"UGX {amount:,.0f}"


def get_customer_type():
    """Prompt until a valid customer category is entered."""

    while True:
        customer_type = input(
            "Customer category (retail/wholesale): "
        ).strip().lower()

        if customer_type in ("retail", "wholesale"):
            return customer_type

        print("Error: Please enter either 'retail' or 'wholesale'.")


def get_yes_no(prompt):
    """Prompt until the user enters yes or no."""

    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "no"):
            return answer == "yes"

        print("Error: Please enter yes or no.")


def get_produce_item():
    """Prompt for a valid produce item."""

    valid_items = {
        "tomatoes": "Tomatoes",
        "red onions": "Red Onions",
        "matooke": "Matooke"
    }

    while True:
        item = input(
            "Enter produce item "
            "(tomatoes/red onions/matooke), or 'done': "
        ).strip().lower()

        if item == "done":
            return None

        if item in valid_items:
            return item

        print(
            "Error: Invalid item. Choose tomatoes, red onions, "
            "or matooke."
        )


def get_unit(item_type):
    """Return the appropriate unit for each produce type."""

    if item_type == "matooke":
        return "bunch"
    return "kg"


# ---------------------------------------------------------
# Component C: Customer Transaction
# ---------------------------------------------------------

def process_customer():
    """
    Process one customer's complete transaction.

    Returns:
        customer_name
        grand_total
    """

    print("\n" + "=" * 70)
    print("NEW CUSTOMER")
    print("=" * 70)

    # Customer information
    while True:
        customer_name = input("Enter customer name: ").strip()

        if customer_name:
            break

        print("Error: Customer name cannot be empty.")

    customer_type = get_customer_type()

    # Basket stores individual line items
    basket = []

    # -----------------------------------------
    # Add items to customer's basket
    # -----------------------------------------
    while True:

        item_type = get_produce_item()

        if item_type is None:
            if not basket:
                print("Error: Basket cannot be empty.")
                continue
            break

        quantity = prompt_quantity(item_type)

        line_total = calculate_item_price(
            item_type,
            quantity,
            customer_type
        )

        basket.append({
            "item": item_type,
            "quantity": quantity,
            "unit": get_unit(item_type),
            "line_total": line_total
        })

        print(
            f"Added {quantity:g} {get_unit(item_type)} "
            f"of {item_type.title()}."
        )
        print(f"Line total: {format_currency(line_total)}")

    # -----------------------------------------
    # Calculate subtotal
    # -----------------------------------------
    subtotal = sum(item["line_total"] for item in basket)

    # -----------------------------------------
    # Eco-crate
    # -----------------------------------------
    needs_eco_crate = get_yes_no(
        "Does the buyer require a reusable eco-friendly crate? (yes/no): "
    )

    # Market levy + packaging
    grand_total = apply_market_levy_and_packaging(
        subtotal,
        needs_eco_crate
    )

    sanitation_fee = subtotal * 0.01
    crate_deposit = 5000 if needs_eco_crate else 0

    # -----------------------------------------
    # Customer Receipt
    # -----------------------------------------
    print("\n")
    print("=" * 70)
    print("                 Mrs Viola Digital POS")
    print("                   CUSTOMER RECEIPT")
    print("=" * 70)

    print(f"Customer : {customer_name}")
    print(f"Category : {customer_type.title()}")
    print("-" * 70)

    print(
        f"{'ITEM':<18}"
        f"{'QUANTITY':>12}"
        f"{'UNIT':>10}"
        f"{'AMOUNT':>20}"
    )

    print("-" * 70)

    for item in basket:
        print(
            f"{item['item'].title():<18}"
            f"{item['quantity']:>12.2f}"
            f"{item['unit']:>10}"
            f"{format_currency(item['line_total']):>20}"
        )

    print("-" * 70)

    print(
        f"{'Subtotal':<50}"
        f"{format_currency(subtotal):>20}"
    )

    print(
        f"{'Sanitation fee (1%)':<50}"
        f"{format_currency(sanitation_fee):>20}"
    )

    print(
        f"{'Eco-crate deposit':<50}"
        f"{format_currency(crate_deposit):>20}"
    )

    print("-" * 70)

    print(
        f"{'GRAND TOTAL':<50}"
        f"{format_currency(grand_total):>20}"
    )

    print("=" * 70)
    print("Thank you for shopping with us!")
    print("=" * 70)

    return customer_name, grand_total


# ---------------------------------------------------------
# Daily Market Session
# ---------------------------------------------------------

def main():
    """
    Controls the complete market session and generates
    the end-of-day reconciliation report.
    """

    total_customers = 0
    total_gross_revenue = 0.0

    highest_customer = ""
    highest_bill = 0.0

    print("=" * 70)
    print("        DIGITAL POS & END-OF-DAY RECONCILIATION LEDGER")
    print("=" * 70)

    while True:

        customer_name, customer_bill = process_customer()

        # Update daily accumulators
        total_customers += 1
        total_gross_revenue += customer_bill

        # Track highest-spending customer
        if customer_bill > highest_bill:
            highest_bill = customer_bill
            highest_customer = customer_name

        # -----------------------------------------
        # Ask whether to serve another customer
        # -----------------------------------------
        serve_next = get_yes_no(
            "\nServe next customer? (yes/no): "
        )

        if not serve_next:
            break

    # ---------------------------------------------------------
    # Daily Market Close Report
    # ---------------------------------------------------------

    print("\n\n")
    print("=" * 70)
    print("                 DAILY MARKET CLOSE REPORT")
    print("=" * 70)

    print(f"{'Total customers served':<40}: {total_customers}")
    print(
        f"{'Total gross revenue':<40}: "
        f"{format_currency(total_gross_revenue)}"
    )

    print("-" * 70)

    if total_customers > 0:
        print(f"{'Highest-spending customer':<40}: {highest_customer}")
        print(
            f"{'Highest customer bill':<40}: "
            f"{format_currency(highest_bill)}"
        )
    else:
        print("No customers were served.")

    print("=" * 70)
    print("Market session closed.")
    print("=" * 70)


# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()