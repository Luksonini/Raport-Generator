# Raport-Generator

![image](https://github.com/Luksonini/Raport-Generator/assets/97095836/2d20394d-06bc-4a87-8192-7c136fa2ff86)

## Introduction
Raport-Generator is a web application that allows users to generate modified versions of Word documents (.docx)by replacing keywords with corresponding values.
It also provides functionalities to convert multiple DOCX or PDF files into a ZIP archive.
The project utilizes various libraries such as BeautifulSoup (bs4), pandas, python-docx, zipfile, and docx2pdf.

## Features
- Upload a Word document (.docx) using the provided file upload functionality.
- Enter keywords and corresponding values in the form to replace specific placeholders in the document.
- Generate modified versions of the document by clicking the "Generate Reports" button.
- Download the generated reports in either DOCX or PDF format.
- Convert multiple DOCX or PDF files into a ZIP archive using the respective conversion functionalities.

## Installation
To run the Raport-Generator project locally, follow these steps:

1. Clone the repository to your local machine:

**Installation**
To run the Raport-Generator project locally, follow these steps:

1. Clone the repository to your local machine:
git clone https://github.com/Luksonini/Raport-Generator.git

2. Navigate to the project directory:
cd Raport-Generator

3. Create a virtual environment:
python -m venv env

4. Activate the virtual environment:

-For Windows:
.\env\Scripts\activate

-For macOS/Linux:
source env/bin/activate

5. Install the project dependencies:
pip install -r requirements.txt

6. Set up the database:
python manage.py migrate

7. Start the development server:
python manage.py runserver

8. Open your web browser and navigate to http://localhost:8000 to access the Raport-Generator application.

> **Note**: Make sure to replace `https://github.com/Luksonini/Raport-Generator.git` with the actual URL of your GitHub repository.

Feel free to customize the installation instructions based on your project's requirements and any additional setup steps needed.

## Configuration
To configure the application for proper functionality, you need to create a `.env` file in the same directory as `manage.py`. Follow these steps:

1. Create a new file named `.env` in the project directory.
2. Inside the `.env` file, add the following lines:
SECRET_KEY=your_generated_secret_key


9. Start the development server:
python manage.py runserver


10. Open your web browser and navigate to http://localhost:8000 to access the Raport-Generator application.

> **Note**: Make sure to replace `https://github.com/Luksonini/Raport-Generator.git` with the actual URL of your GitHub repository.

Feel free to customize the installation instructions based on your project's requirements and any additional setup steps needed.

## Usage
- Upload a Word document (.docx) using the provided file upload functionality.
- Enter keywords and corresponding values in the form to replace specific placeholders in the document.
- Generate modified versions of the document by clicking the "Generate Reports" button.
- Download the generated reports in either DOCX or PDF format.
- Convert multiple DOCX or PDF files into a ZIP archive using the respective conversion functionalities.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
For any questions or inquiries, please contact lukasz.jozef.gasior@gmail.com.

