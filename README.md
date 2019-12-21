# ScrapeThePrez
**UPDATE 12/21/19:** We've gotten back on the grind and we're revamping the entire tech stack! In the past, ScrapeThePrez has stored and hosted data with Google Cloud Platform (Firestore/Hosting). *This won't suffice for the full extent of ScrapeThePrez's features!* 

ScrapeThePrez is migrating to a **full-stack React/Django/PostgreSQL** platform! Stay tuned. 

## Old-ish website: https://scrapetheprez.web.app
![ScrapeThePrez Logo](/v1_files/static/pictures/normal_size_logo.png)

### Goal: Compare relevant buzz words with what the presidential candidates have been saying.
We're making a search bar website UI that will web scrape Twitter tweets relevant to your queries... from the 2020 U.S. Presidential candidates.

#### Coming soon! Scrape the Prez.
Vera Kong and Nicole Danuwidjaja

## Technical Specifications
(Aka Just for Vera KONG)

#### Front-end (React.js Framework)

*Requires [Node.js](https://nodejs.org/) installation in order to use npm (Node Package Manager).*

Create React app: `npx create-react-app scrapetheprez`
- Installs packages and dependencies for React app (generates package.json, package-lock.json, and yarn.lock)

Run React app: `npm start`

Create production build: `yarn build`

Additional dependencies: `npm install bootstrap`

#### Back-end (Django server)

Install pipenv: `pip install pipenv`
- Python package management and virtual environment tool
- generates Pipfile to manage project dependencies

Run subenvironment: `pipenv shell`

Install Django dependencies: `pipenv install django djangorestframework django-rest-knox`

##### Project Directory Setup:
Create new Django project: `django-admin startproject scrapetheserver`
- manage.py: Django CLI
- create migrations, run server, manage project

Create new Django app: `python manage.py startapp scrapeserver`

Update Project Settings: 
- Add Django app `scrapeserver` and `rest_framework` to 'INSTALLED_APPS'
- Change default to ENGINE: `django.db.backends.postgresql` and NAME: `os.path.join(BASE_DIR, 'db.postgresql')` to 'DATABASES`

Install [PostgreSQL](https://www.postgresql.org/docs/9.3/tutorial-install.html) (RDBMS)

