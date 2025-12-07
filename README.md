# OTP_gen_n_verify
OTP Generator & Verifier (Python)

A secure console-based OTP authentication system built with Python.
It generates a 6-digit OTP, verifies it using hashed + salted validation, supports OTP resend, and blocks the user for 2 minutes after 3 failed attempts.

Run
python otp_app.py

Features

Secure OTP hashing (SHA-256 + salt)

OTP expiry (60 seconds)

OTP resend option

User block after 3 wrong attempts