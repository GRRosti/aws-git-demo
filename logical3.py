def calculate_order_total():
    """
    Reads order details, applies surcharges and discounts based on rules,
    and prints the final total.
    """
    try:
        order_amount = float(input("Enter order amount: "))
        customer_type = input("Enter customer type (regular, member, or vip): ").lower()
        coupon_code = input("Enter coupon code (leave blank if none): ")

        final_amount = order_amount

        # Apply adjustments based on compound boolean conditions
        # Surcharge applies first if amount is below 50
        if order_amount < 50:
            # Apply 5% surcharge
            final_amount += order_amount * 0.05

        # Standard discount applies if customer is member or vip
        if customer_type == "member" or customer_type == "vip":
            # Apply 10% discount to the current amount
            final_amount -= final_amount * 0.10

        # Additional discount applies if customer is vip AND uses the specific coupon
        if customer_type == "vip" and coupon_code == "SAVE15":
             # Apply additional 15% discount to the current amount
             final_amount -= final_amount * 0.15

        # Print the final total
        print(f"Final total: ${final_amount:.2f}")

    except ValueError:
        print("Invalid input. Please ensure order amount is a number.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script
calculate_order_total()