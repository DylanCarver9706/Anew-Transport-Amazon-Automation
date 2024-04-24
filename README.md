Create a Python Virtual environment:
python -m venv venv
NOTE: Python 3+ is required

Start python virtual environment:
.\venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Get cookies data:

To obtain a new cookie, follow the steps below:

1. Log into ProABD
2. Once logged in, open the Developer tools by doing Right Click -> Inspect
3. In the new window that opens, go to the Console tab
4. Find the carrot ">" indicating that your cursor goes there
5. input "console.log(document.cookie)" and hit Enter
6. Copy the output text into a cookies.txt file