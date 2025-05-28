# VizQL & Chill

by Kyle Massey and Will Perkins

![VizQL and Chill Logo](/frontend/public/splash_logo.jpeg)

## This is the official repository for VizQL and Chill, our session from #TC25:


> Redefine the Tableau Server user experience by leveraging VizQL — creating a more intuitive, user-friendly way to find dashboards, leading to a boost in adoption at scale.


\[Video of Session Coming Soon!!\]

## Here’s how you can get started!

<mark>***Please Note:*** Although the application has no inherent access other than what you give it via Tableau's built-in Connected App, PAT and JWT functionality, this shouldn't be considered production-ready code. Use it at your own risk and accept that the creators offer no warranty or support</mark>

That being said, feel free to borrow/steal anything you find useful -- just let us know what you think! 😁

### Installation

The application consists of two parts: a [Django](<https://www.djangoproject.com/>) powered backend in Python, and a [VueJs](https://vuejs.org/) powered frontend - which uses NodeJS. Make sure to have [Python](https://www.python.org/) and [NodeJS](https://nodejs.org/en/download) installed before continuing!

Terminal command examples below are for example only and may vary based on your hardware/software setup.

#### Backend:
1. Clone this repository
2. From a terminal, navigate into the *django_backend* folder
3. Create a Python virtual environment
    - *python -m venv venv*
4. Activate the virtual environment
    - *source venv/bin/activate*
5. Install the required Python libraries using pip
    - *pip install -r requirements.txt*

#### Frontend
1. From your terminal, navigate to the *frontend* folder
2. Install the required packages using npm
    - *npm install*
3. Build the files (optional: for deploying/serving)
    - *npm run build*

### Configuration

You will need make some changes to files, such as adding credentials and Server/Cloud details:

#### Backend:
- django_backend > tableau > creds > tableau_creds.py
    - Update the following values:
    ```
    POD_URL = "YOUR_TABLEAU_SERVER_URL"
    SITE_NAME = "YOUR_SITE_NAME"
    PAT_NAME = "YOUR_PAT_NAME"
    PAT_SECRET = "YOUR_PAT_SECRET"
    CONNECTED_APP_NAME = "YOUR_CONNECTED_APP_NAME"
    CONNECTED_APP_CLIENT_ID = "YOUR_CONNECTED_APP_CLIENT_ID"
    CONNECTED_APP_SECRET_ID = "YOUR_CONNECTED_APP_SECRET_ID"
    CONNECTED_APP_SECRET_VALUE = "YOUR_CONNECTED_APP_SECRET_VALUE"
    ```

#### Frontend
- frontend > src > stores > consts.js
    - Update the following:
    ```
    export const tableauUrlRoot = "YOUR-TABLEAU-URL-HERE" // e.g. http://10az.online.tableau.com 
    export const tableauApiVersion = "3.25"
    export const tableauAuthEndpoint = `${tableauUrlRoot}/api/${tableauApiVersion}/auth/signin`
    export const tableauSite = "YOUR-SITE-NAME"
    export const patName = "YOUR-PAT-NAME"
    export const patSecret = "YOUR-PAT-SECRET"
    ``` 
        
### Startup

1. In a terminal window, navigate to *django_backend*
2. Start backend:
    - *python manage.py runserver*
    - The terminal output should provide the path to the URL root
        - typically: http://localhost:8000/
3. In a ***separate*** terminal, navigate to *frontend*
4. Start frontend:
    - *npm run dev*
    - Terminal out will provide path to frotend running in Dev mode:
        - typically: http://localhost:3000/