import boto3
import PyPDF2
import os

#----------------------- CONSTANTS ----------------------#
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY= os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION='us-west-2'
#----------------------- CONSTANTS ----------------------#

#----------------------- PDF CONVERTER ----------------------#
def extract_text_from_pdf(path):
    with open(path, 'rb') as file:
        reader= PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text+= reader.pages[page_num].extract_text()
    return text
#----------------------- PDF CONVERTER ----------------------#

#----------------------- TEXT TO SPEECH ----------------------#
def text_to_speech(file_path):
    text_to_speech = extract_text_from_pdf(file_path)

    polly_client = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,                     
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION).client('polly')

    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3', 
        Text = text_to_speech,
        )

    with open('speech.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

#----------------------- TEXT TO SPEECH ----------------------#

if __name__ == '__main__':
    file_path = input('please paste your PDF file path: ')
    try:
        text_to_speech(file_path= file_path)
    except FileNotFoundError:
        print('file not found')
    except Exception as e:
        print(f'An error occured: {e}')

    

