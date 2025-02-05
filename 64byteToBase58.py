#!/usr/bin/env python3
import sys

# Solana (and Bitcoin) Base58 alphabet.
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def parse_input(input_str):
    """
    Parses a user input string containing 64 bytes (in hex or decimal format)
    separated by commas. The expected format is similar to:
      [00, 1a, ff, ...]
    Returns a list of 64 two‑digit hex strings.
    """
    # Remove square brackets if present and any surrounding whitespace.
    input_str = input_str.strip()
    if input_str.startswith("[") and input_str.endswith("]"):
        input_str = input_str[1:-1]

    # Split by commas.
    parts = input_str.split(",")
    if len(parts) != 64:
        print(f"Error: exactly 64 bytes are required, but got {len(parts)}.")
        sys.exit(1)

    byte_list = []
    for part in parts:
        token = part.strip()
        # If the token starts with '0x', remove the prefix.
        if token.startswith("0x") or token.startswith("0X"):
            token = token[2:]
        # Determine if the token is hexadecimal or decimal.
        try:
            # If it contains any letters a-f, assume it's hex.
            if any(c in token.lower() for c in "abcdef"):
                val = int(token, 16)
            else:
                # Otherwise, try to parse as an integer.
                val = int(token)
            if not (0 <= val <= 255):
                raise ValueError("Byte out of range (0-255).")
            # Convert the integer value back to a 2-digit hex string.
            byte_list.append(f"{val:02x}")
        except ValueError as e:
            print(f"Error parsing byte '{token}': {e}")
            sys.exit(1)
    return byte_list

def bytes_to_int(byte_list):
    """
    Converts a list of 64 bytes (as two-digit hex strings) into an integer,
    interpreting the bytes in big‑endian order.
    """
    # Convert hex strings to integer values.
    int_bytes = [int(x, 16) for x in byte_list]
    return int.from_bytes(bytearray(int_bytes), byteorder='big')

def encode_base58(byte_list):
    """
    Encodes a 64-byte list (given as two-digit hex strings) to a Base58 string
    using the Solana (Bitcoin) alphabet.
    """
    num = bytes_to_int(byte_list)
    
    # Convert the integer to a Base58 string.
    encoded = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded

    # Count leading zero bytes (each represented as '1' in Base58).
    n_leading_zeros = 0
    for hex_byte in byte_list:
        if int(hex_byte, 16) == 0:
            n_leading_zeros += 1
        else:
            break

    return BASE58_ALPHABET[0] * n_leading_zeros + encoded

def main():
    user_input = input("Enter your 64 byte values (e.g. [00, 1a, ff, ...]):\n")
    byte_list = parse_input(user_input)
    base58_str = encode_base58(byte_list)
    print("Base58 encoded string:")
    print(base58_str)

if __name__ == "__main__":
    main()
