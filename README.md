# Raport-Generator
Usage
Upload a Word document (.docx) using the provided file upload functionality.
Enter keywords and corresponding values in the form to replace specific placeholders in the document.
Generate modified versions of the document by clicking the "Generate Reports" button.
Download the generated reports in either DOCX or PDF format.
Convert multiple DOCX or PDF files into a ZIP archive using the respective conversion functionalities.

Features
Upload a Word document (.docx) using the provided file upload functionality.
Enter keywords and corresponding values in the form to replace specific placeholders in the document.
Generate modified versions of the document by clicking the "Generate Reports" button.
Download the generated reports in either DOCX or PDF format.
Convert multiple DOCX or PDF files into a ZIP archive using the respective conversion functionalities.
Installation
To run the Raport-Generator project locally, follow these steps:

Clone the repository to your local machine:
git clone https://github.com/Luksonini/Raport-Generator.git

Navigate to the project directory:
cd Raport-Generator

Create a virtual environment:
python -m venv env

Activate the virtual environment:

For Windows:
.\env\Scripts\activate

For macOS/Linux:
source env/bin/activate

Install the project dependencies:
pip install -r requirements.txt

Set up the database:
python manage.py migrate

Start the development server:
python manage.py runserver

Open your web browser and navigate to http://localhost:8000 to access the Raport-Generator application.

Make sure to replace https://github.com/Luksonini/Raport-Generator.git with the actual URL of your GitHub repository.

Feel free to customize the installation instructions based on your project's requirements and any additional setup steps needed.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

Contact
For any questions or inquiries, please contact lukasz.jozef.gasior@gmail.com.
