import requests
import json


def ocr_space_file(filename, overlay=False, api_key='K86037785188957', language='per'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Extracted text.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 3
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    # Parse JSON response
    result = json.loads(r.content.decode())

    # Extract text from the parsed JSON
    if 'ParsedResults' in result and len(result['ParsedResults']) > 0:
        text = result['ParsedResults'][0]['ParsedText']
        return text
    else:
        return "Error: Unable to extract text from the OCR response."


def ocr_space_url(url, overlay=False, api_key='K86037785188957', language='per'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 3
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


# Example usage
filename = 'samples/kaj3.jpg'
text_output = ocr_space_file(filename)
# Write the extracted text to a text file
output_file_path = 'results/output.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(text_output)

print(f"Extracted text saved to: {output_file_path}")
