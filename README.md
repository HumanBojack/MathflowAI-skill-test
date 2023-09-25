# Mathflow.ai test
This project is a dummy project to test my skills for a backend developper position at [Mathflow.ai](https://mathflow.ai/).

## The project
I need to make a simple quizz app with a backend (Django REST Framework) and a frontend (Flutter). The app is a simple quizz app where the user can answer questions and see his score.
In addition to that, the user can earn a currency by correctly answering questions. The currency is buffered until the user has answered 10 questions. If the user has not answered 10 questions before midnight of the same day, the currency is lost. The user can then start again the next day.

## Run the project
The Backend has been containerized in order to be ran easily. Run `docker compose up --build` at the root of the project to run it, and access it on port *8000*.

The frontend, located in `/app`, can be ran using the apk provided in the latest release. The source code is also available in the `/app` folder.

## Backend
### Seed
The database can be populated with 20 questions an a user by running the following command:
```bash
python manage.py loaddata seed.json
```


