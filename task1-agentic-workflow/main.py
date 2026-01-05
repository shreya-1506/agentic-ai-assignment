from agent import create_agent

def get_user_input():
    """
    Handles user input safely.
    """
    try:
        product_title = input("Enter product title: ").strip()

        if not product_title:
            raise ValueError("Product title cannot be empty")

        return product_title

    except Exception as e:
        print(f"[INPUT ERROR] {str(e)}")
        return None


def run_agent(product_title: str):
    """
    Runs the agent with proper exception handling.
    """
    try:
        agent = create_agent()

        response = agent.invoke({
            "input": product_title
        })

        if "output" not in response:
            raise RuntimeError("Agent did not return output")

        print("\nFINAL OUTPUT:")
        print(response["output"])

    except Exception as e:
        print("\n[AGENT ERROR]")
        print(f"Reason: {str(e)}")


if __name__ == "__main__":
    title = get_user_input()

    if title:
        run_agent(title)
    else:
        print("Exiting program due to invalid input.")
