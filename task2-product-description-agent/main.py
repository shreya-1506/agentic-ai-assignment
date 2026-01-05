from agent import (
    decide_generation_strategy,
    generate_description,
    validate_output
)

def get_user_input():
    try:
        title = input("Enter product title: ").strip()
        if not title:
            raise ValueError("Product title cannot be empty")

        supplier_text = input(
            "Enter supplier text (optional, press Enter to skip): "
        ).strip()

        return title, supplier_text if supplier_text else None

    except Exception as e:
        print(f"[INPUT ERROR] {str(e)}")
        return None, None


def run_pipeline(title: str, supplier_text: str | None):
    try:
        decision = decide_generation_strategy(title, supplier_text)

        raw_output = generate_description(
            title,
            supplier_text,
            decision["strategy"]
        )

        final_output = validate_output(raw_output, title)

        print("\nFINAL JSON OUTPUT:\n")
        print(final_output)

    except Exception as e:
        print("\n[PIPELINE ERROR]")
        print(str(e))


if __name__ == "__main__":
    title, supplier_text = get_user_input()

    if title:
        run_pipeline(title, supplier_text)
    else:
        print("Exiting program due to invalid input.")
