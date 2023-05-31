FROM python:3.9-slim
WORKDIR /usr/src/app
RUN pip install wheel gunicorn
ADD . .
RUN pip install .
RUN FLASK_APP=tchou flask db:init
RUN FLASK_APP=tchou flask db:load-data 
RUN FLASK_APP=tchou flask db:generate-trips
ENTRYPOINT ["/bin/sh","-c","FLASK_APP=tchou gunicorn -b 0.0.0.0:8000 'tchou:create_app()'"]
