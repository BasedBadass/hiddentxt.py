## Steganography Tool with Python

This Python script provides functionalities for encoding and decoding text messages within the least significant bits (LSBs) of an image. 

### Functionality

* **Encode Text:** Hides a secret message within an image.
* **Decode Text:** Extracts the hidden message from an encoded image.

### Usage

**1.  Make the script executable:**

This script requires Python 3 and the `Pillow` library. Install Pillow with `pip install Pillow`.

```bash
chmod +x hiddentxt.py  # Replace 'hiddentxt.py' with your actual filename
```

**2.  Encoding:**

```bash
./hiddentxt.py encode input.jpg output.png "This is a secret message!"
```

- Replace `input.jpg` with the path to your image file.
- Replace `output.png` with the desired output filename (PNG recommended).
- Replace `"This is a secret message!"` with your actual secret message.

**3.  Decoding:**

```bash
./hiddentxt.py decode output.png
```

- Replace `output.png` with the path to your encoded image file.


### Output

The script will print messages indicating success or errors during encoding or decoding.

**Success:**

- Upon successful encoding, it displays a message confirming the text is encoded and saved to the specified output file.
- Decoding a message successfully will print the extracted message.

**Errors:**

- File not found errors will be displayed if the script cannot locate the input or output image files.
- If the message is too large to fit within the image, a value error will occur.
- Any unexpected errors will be caught with a generic error message.


### License

This script is provided without warranty. You are free to use and modify it for personal or educational purposes.


### Dependencies

* Python 3
* Pillow library (`pip install Pillow`)


**Note:** This script demonstrates a basic implementation of steganography and may not be secure for sensitive information. Consider stronger encryption methods for crucial data.
