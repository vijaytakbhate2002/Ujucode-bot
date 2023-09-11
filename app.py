import imaplib, email
from email import policy
from email.header import decode_header
from email.message import Message
import msvcrt
import sys

imap_url = 'imap.gmail.com' 

def getpass(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = b''
    while True:
        key = msvcrt.getch()
        if key == b'\r' or key == b'\n':
            print()
            break
        elif key == b'\x08':  # Backspace
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += key
            print('*', end='', flush=True)
    return password.decode('utf-8')

if len(sys.argv) > 3:
    user = sys.argv[1] if len(sys.argv) > 0 else input("Please enter your email address: ")
    password = sys.argv[2] if len(sys.argv) > 1 else getpass("Enter your password: ")
    label = sys.argv[3] if len(sys.argv) > 2 else input("Please enter the label that you'd like to search: ")
    search_criteria = sys.argv[4] if len(sys.argv) > 3 else input("Please enter the subject search criteria: ")
else:
    user = input("Please enter your email address: ")
    password = getpass("Enter your password: ")
    if "qbufkfwdawfnocwn" == password:
        print("Right Password")
    else:
        print("Invalid Password")
    label = input("Please enter the label that you'd like to search: ") # Example: Inbox or Social
    search_criteria = input("Please enter the subject search criteria: ")

# def get_body(message): 
#     if message.is_multipart(): 
#         return get_body(message.get_payload(0)) 
#     else: 
#         return message.get_payload(None, True) 

def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data 
   
def get_emails(result_bytes): 
    messages = [] 
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        messages.append(data) 
   
    return messages 
 
# Authenticate
def authenticate(imap_url, user, password, label):
    con = imaplib.IMAP4_SSL(imap_url)  
    con.login(user, password)  
    con.select(label)
    print("Ytoeu ksdnfds==",type(con))
    return con


def decoder(raw_email_tuple:tuple)-> dict:
    """ Args: tuple (row tuple input in MIME format) MIME:Multipurpose Internet Mail Extensions
        Returs: dict (sender , subject , plain text body) """

    email_str = raw_email_tuple[1].decode('utf-8')
    parsed_email = email.message_from_string(email_str)
    def extract_text_from_message(message):
        if isinstance(message, str):
            return message
        elif isinstance(message, Message):
            text_parts = [part for part in message.walk() if part.get_content_type() == 'text/plain']
            if text_parts:
                return text_parts[0].get_payload(decode=True).decode('utf-8', errors='ignore')
        return ''

    subject = parsed_email['subject']
    sender = parsed_email['From']
    receiver = parsed_email['To']
    date = parsed_email['Date']
    email_plain_text = extract_text_from_message(parsed_email)
    return {"sender":sender,"receiver":receiver,"date":date,"email_plain_text":email_plain_text}



if __name__ == "__main__":
    # Autontication
    con = authenticate(imap_url, user, password, label)
    # Retrive message
    search_results = search('Subject', search_criteria, con)
    raw_email_list = get_emails(search_results) 
    decoded_content_dic = decoder(raw_email_tuple=raw_email_list[0][0])

    print("Sender:", decoded_content_dic['sender'])
    print("Receiver:", decoded_content_dic['receiver'])
    print("Date:", decoded_content_dic['date'])
    print("Plain Text Content:")
    print(decoded_content_dic['email_plain_text'])
