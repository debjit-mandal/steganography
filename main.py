from PIL import Image

class Steganography:
    NULL_TERMINATOR = '00000000'

    @staticmethod
    def text_to_bits(text):
        return ''.join(format(ord(char), '08b') for char in text)

    @staticmethod
    def encode_image(source_img_path, message, output_img_path):
        message_bits = Steganography.text_to_bits(message) + Steganography.NULL_TERMINATOR
        
        with Image.open(source_img_path) as source_img:
            if len(message_bits) > source_img.width * source_img.height * 3:
                raise ValueError("Message is too long to encode in this image.")
            
            encoded_img = source_img.copy()
            bit_index = 0
            
            for y in range(encoded_img.height):
                for x in range(encoded_img.width):
                    if bit_index >= len(message_bits):
                        break

                    pixel = list(encoded_img.getpixel((x, y)))
                    for channel in range(3):
                        pixel[channel] = (pixel[channel] & 0xFE) | int(message_bits[bit_index])
                        bit_index += 1
                    encoded_img.putpixel((x, y), tuple(pixel))
            
            encoded_img.save(output_img_path)

    @staticmethod
    def decode_image(encoded_img_path):
        decoded_bits = []

        with Image.open(encoded_img_path) as encoded_img:
            for pixel in encoded_img.getdata():
                decoded_bits.extend(str(channel & 0x01) for channel in pixel)
                if "".join(decoded_bits).endswith(Steganography.NULL_TERMINATOR):
                    break
        
        decoded_message = "".join(chr(int("".join(decoded_bits[i:i+8]), 2)) for i in range(0, len(decoded_bits), 8))
        return decoded_message.rstrip('\x00')

def main():
    source_image_path = 'images/g.jpg'
    output_image_path = 'images/gcon.jpg'
    message_to_encode = "It is a hidden message!"

    try:
        Steganography.encode_image(source_image_path, message_to_encode, output_image_path)
        decoded_message = Steganography.decode_image(output_image_path)
        print("Decoded Message:", decoded_message)
    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
