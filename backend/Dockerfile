FROM python:3.11

WORKDIR /api

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements.txt
COPY requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# copy the django code
COPY . .

# migrate the database
RUN python manage.py migrate

# seed the database
RUN python manage.py loaddata seed.json

# run the app
CMD python manage.py runserver 0.0.0.0:$PORT
