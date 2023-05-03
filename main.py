import openai
import PyPDF2
import csv


def pdf2t(file_name):
    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    #summary = summarize_text(text)
    #print(text)

    return text


def text2csv(text):
    # Open the CSV file in write mode
    with open('output.csv', mode='a', newline='') as file:

        # Create a CSV writer object
        writer = csv.writer(file)
        # Write the text into the CSV file
        writer.writerow([text])

    # Print a message to confirm that the text has been written


def chatgpt(mode, input_user, input_system, key):
    # Set up OpenAI API credentials
    openai.api_key = key

    if mode == "text-davinci-003": 
        response = openai.Completion.create(
            engine=mode,
            prompt=input_user,
            temperature=0.7,
            max_tokens=250,
            n=1,
            stop=None,
        )
        output = response.choices[0].text
    
    if mode == "gpt-3.5-turbo":
        response = openai.ChatCompletion.create(
        model=mode,
        messages=[
                {"role": "system", "content": input_system},
                {"role": "user", "content": input_user}
            ]
        )
        print (response)
        #print (response.choices[-1].message.role)
        #print (response.choices[-1].message.content)
        output = (response.choices[-1].message.content)




    # Print the output
    print(output)
    text2csv(output)
    


file_name = "test.pdf"
text = pdf2t(file_name)

# buy a paid plan and generate a key (https://platform.openai.com/account/api-keys)
api_key = "----"

# input_user is main prompt and input_system is only used for "gpt-3.5-turbo"
input_user = "summarize the following text into flash cards:\n\n" + text
input_system = "You are a helpful assistant and expert in computer science."

chatgpt("gpt-3.5-turbo", input_user, input_system, api_key)
