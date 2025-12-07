import secrets
import string
import time


OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 60   # OTP valid for 60 seconds
MAX_ATTEMPTS = 3


def generate_otp(length: int = OTP_LENGTH) -> str:
    """Generate a secure numeric OTP of given length."""
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(length))


def send_otp(otp: str) -> None:
    """
    Simulate sending OTP to user.
    In a real system, this would be SMS / email integration.
    """
    print("\n[DEBUG] Sending OTP to user...")
    print(f"[DEBUG] OTP (for testing/demo): {otp}\n")


def verify_otp(expected_otp: str, created_at: float) -> bool:
    attempts = 0

    while attempts < MAX_ATTEMPTS:

        current_time = time.time()
        time_elapsed = current_time - created_at

        if time_elapsed > OTP_EXPIRY_SECONDS:
            print("⏰ OTP expired. Please request a new one.")
            return False

        user_input = input("Enter the OTP you received: ").strip()
        attempts += 1

        # ✅ Re-check expiry IMMEDIATELY after user types
        if time.time() - created_at > OTP_EXPIRY_SECONDS:
            print("⏰ OTP expired while you were typing.")
            return False

        if user_input == expected_otp:
            print("✅ OTP verified successfully. Access granted.")
            return True
        else:
            remaining = MAX_ATTEMPTS - attempts
            if remaining > 0:
                print(f"❌ Incorrect OTP. You have {remaining} attempt(s) left.\n")
            else:
                print("❌ Incorrect OTP. No attempts left. Access denied.")

    return False



def main():
    print("=== OTP Generator & Verifier ===")

    # Step 1: Generate OTP
    otp = generate_otp()
    created_at = time.time()

    # Step 2: "Send" OTP (simulated)
    send_otp(otp)

    print(f"OTP is valid for {OTP_EXPIRY_SECONDS} seconds.")
    print(f"You have {MAX_ATTEMPTS} attempts.\n")

    # Step 3: Verify OTP
    _ = verify_otp(otp, created_at)

    print("\nThank you for using the OTP demo.")


if __name__ == "__main__":
    main()
