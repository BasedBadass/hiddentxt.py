#!/usr/bin/env python3

# Description: A Python script to encode and decode hidden messages within JPEG images
# using the Least Significant Bit (LSB) steganography technique.
# Usage:
#   Encoding: ./hiddentxt.py encode input_image.jpg "message" output_image.jpg
#   Decoding: ./hiddentxt.py decode encoded_image.jpg

import argparse
from PIL import Image
import os

def encode_message(image_path, message, output_path):
    """Encodes a message into a JPEG image using LSB steganography."""
    try:
        img = Image.open(image_path).convert('RGB')
        width, height = img.size  # Get image dimensions here, AFTER opening image
    except FileNotFoundError:
        print(f"Error: Input image '{image_path}' not found.")
        return
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # 16-bit delimiter

    # Pad to make the length a multiple of 3 for RGB channels
    padding_length = (3 - (len(binary_message) % 3)) % 3
    binary_message += '0' * padding_length

    max_bits = width * height * 3
    if len(binary_message) > max_bits:
        raise ValueError("Message too long to fit in image!")

    img_data = img.load()

    binary_index = 0
    for y in range(height):
        for x in range(width):
            for k in range(3):
                if binary_index < len(binary_message):
                    pixel_value = img_data[x, y][k]
                    message_bit = int(binary_message[binary_index])

                    new_pixel_value = (pixel_value & ~1) | message_bit

                    img_data[x, y] = (
                        new_pixel_value if k == 0 else img_data[x, y][0],
                        new_pixel_value if k == 1 else img_data[x, y][1],
                        new_pixel_value if k == 2 else new_pixel_value
                    )

                    binary_index += 1
                else:
                    break
            else:
                continue
            break
        else:
            continue
        break

    try:
        img.save(output_path)
        print(f"Message encoded successfully! Encoded image saved as: {output_path}")
    except Exception as e:
        print(f"Error saving encoded image: {e}")


def decode_message(image_path):
    """Decodes a hidden message from a JPEG image."""
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"Error: Encoded image '{image_path}' not found.")
        return None
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    width, height = img.size
    img_data = img.load()

    binary_message = ""
    decoded_message = ""
    found_delimiter = False

    for y in range(height):
        for x in range(width):
            for k in range(3):
                binary_message += str(img_data[x, y][k] & 1)
                if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':
                    binary_message = binary_message[:-16]
                    found_delimiter = True
                    break
            if found_delimiter:
                break
        if found_delimiter:
            break

    if not found_delimiter:
        return None

    padding_length = 8 - (len(binary_message) % 8)
    if padding_length != 8:
        binary_message += '0' * padding_length

    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        try:
            decoded_message += chr(int(byte, 2))
        except ValueError:
            print(f"Error converting byte: {byte}")
            return None

    return decoded_message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode or decode hidden messages in JPEG images using LSB steganography.",
                                     usage="""./hiddentxt.py encode input_image.jpg "message" output_image.jpg
                                     ./hiddentxt.py decode encoded_image.jpg""")

    parser.add_argument("mode", choices=["encode", "decode"], help="Mode of operation: encode or decode.")
    parser.add_argument("input_image", help="Path to the input image.")
    parser.add_argument("message", nargs="?", help="Message to encode (required for encode mode).")
    parser.add_argument("output_image", nargs="?", help="Path to save the output image (required for encode mode).")

    args = parser.parse_args()

    if args.mode == "encode":
        if not args.message or not args.output_image:
            parser.print_help()
            exit()
        encode_message(args.input_image, args.message, args.output_image)
    elif args.mode == "decode":
        decoded_message = decode_message(args.input_image)
        if decoded_message:
            print(f"Decoded message: {decoded_message}")
        else:
            print("No hidden message found or an error occurred during decoding.")