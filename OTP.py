import secrets
import string
import time
import hashlib

OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 60       # OTP valid for 60 seconds
MAX_ATTEMPTS = 3             # max wrong attempts before block
BLOCK_DURATION_SECONDS = 120 # block user for 2 minutes


def generate_otp(length: int = OTP_LENGTH) -> str:
    """Generate a secure numeric OTP of given length."""
    digits = string.digits
    return "".join(secrets.choice(digits) for _ in range(length))


def hash_otp(otp: str, salt: str) -> str:
    """Hash the OTP with a salt using SHA-256."""
    data = (salt + otp).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def send_otp(otp: str) -> None:
    """
    Simulate sending OTP to user.
    In real life, this would be SMS / email integration.
    """
    print("\n[DEBUG] Sending OTP to user...")
    print(f"[DEBUG] OTP (for testing/demo): {otp}\n")


def request_new_otp() -> tuple[str, str, float]:
    """
    Generate, hash, and 'send' a new OTP.
    Returns (otp_hash, salt, created_at).
    """
    salt = secrets.token_hex(8)  # random salt per OTP
    otp = generate_otp()
    otp_hash = hash_otp(otp, salt)
    created_at = time.time()

    send_otp(otp)
    return otp_hash, salt, created_at


def verify_flow():
    """
    Full OTP verification flow with:
    - resend support
    - expiry check
    - attempt limit
    - blocking after too many failures
    """
    block_until = 0.0

    print("=== OTP Generator & Verifier (Enhanced) ===")

    # Check initial block state (in case you extend this later to persist block time)
    now = time.time()
    if now < block_until:
        wait = int(block_until - now)
        print(f"🚫 You are temporarily blocked. Try again in {wait} seconds.")
        return

    # First OTP
    otp_hash, salt, created_at = request_new_otp()
    attempts = 0

    print(f"OTP is valid for {OTP_EXPIRY_SECONDS} seconds.")
    print(f"You have {MAX_ATTEMPTS} attempts.")
    print("Type 'resend' to get a new OTP.\n")

    while True:
        # Check expiry before asking input
        if time.time() - created_at > OTP_EXPIRY_SECONDS:
            print("⏰ OTP expired.")
            choice = input("Do you want to resend a new OTP? (y/n): ").strip().lower()
            if choice == "y":
                otp_hash, salt, created_at = request_new_otp()
                attempts = 0
                print(f"New OTP is valid for {OTP_EXPIRY_SECONDS} seconds.")
                print(f"You have {MAX_ATTEMPTS} attempts.\n")
                continue
            else:
                print("❌ Verification cancelled.")
                return

        user_input = input("Enter the OTP (or type 'resend'): ").strip()

        # User-triggered resend
        if user_input.lower() == "resend":
            otp_hash, salt, created_at = request_new_otp()
            attempts = 0
            print(f"New OTP is valid for {OTP_EXPIRY_SECONDS} seconds.")
            print(f"You have {MAX_ATTEMPTS} attempts.\n")
            continue

        # Re-check expiry in case user typed slowly
        if time.time() - created_at > OTP_EXPIRY_SECONDS:
            print("⏰ OTP expired while you were typing.")
            choice = input("Do you want to resend a new OTP? (y/n): ").strip().lower()
            if choice == "y":
                otp_hash, salt, created_at = request_new_otp()
                attempts = 0
                print(f"New OTP is valid for {OTP_EXPIRY_SECONDS} seconds.")
                print(f"You have {MAX_ATTEMPTS} attempts.\n")
                continue
            else:
                print("❌ Verification cancelled.")
                return

        # Verify OTP using hash
        attempts += 1
        entered_hash = hash_otp(user_input, salt)

        if entered_hash == otp_hash:
            print("✅ OTP verified successfully. Access granted.")
            return
        else:
            remaining = MAX_ATTEMPTS - attempts
            if remaining > 0:
                print(f"❌ Incorrect OTP. You have {remaining} attempt(s) left.\n")
            else:
                print("❌ Incorrect OTP. No attempts left.")
                # Block user for BLOCK_DURATION_SECONDS
                block_until = time.time() + BLOCK_DURATION_SECONDS
                wait = int(BLOCK_DURATION_SECONDS)
                print(f"🚫 You are blocked for {wait} seconds due to multiple failed attempts.")
                # For demo, we won't actually sleep for 2 minutes.
                # In a real system, you'd persist block_until somewhere (DB/cache).
                return


def main():
    verify_flow()
    print("\nThank you for using the OTP demo.")


if __name__ == "__main__":
    main()
