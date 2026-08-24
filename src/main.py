from report_generator import generate_report
from risk_scorer import calculate_risk


def display_result(prompt):
    result = calculate_risk(prompt)

    print("\n" + "=" * 60)
    print("PROMPTSHIELD ANALYSIS RESULT")
    print("=" * 60)

    print(f"\nPrompt: {prompt}")

    print(
        f"Final Decision: "
        f"{'MALICIOUS' if result['is_malicious'] else 'BENIGN'}"
    )

    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_level']}")

    print(
        f"ML Malicious Probability: "
        f"{result['ml_probability']:.2%}"
    )

    print(
        f"Regex Rules Triggered: "
        f"{result['regex_rules_triggered']}"
    )

    categories = result["detected_categories"]

    if categories:
        print(
            f"Detected Categories: "
            f"{', '.join(categories)}"
        )
    else:
        print("Detected Categories: None")

    print("=" * 60)

    report_path, json_path = generate_report(prompt, result)

    print(f"\nText Report:\n{report_path}")
    print(f"JSON Report:\n{json_path}")


def main():
    print("=" * 60)
    print("PROMPTSHIELD")
    print("Hybrid AI Prompt Attack Detection System")
    print("=" * 60)

    while True:
        print("\nEnter a prompt for analysis.")
        print("Type 'exit' to close PromptShield.")

        prompt = input("\nPrompt > ")

        if prompt.strip().lower() == "exit":
            print("\nPromptShield closed.")
            break

        if not prompt.strip():
            print("\nError: Prompt cannot be empty.")
            continue

        display_result(prompt)


if __name__ == "__main__":
    main()