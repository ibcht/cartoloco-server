FROM python:3.9-slim
WORKDIR /usr/src/app
RUN pip install wheel gunicorn
COPY . .
RUN pip install .
ENTRYPOINT ["/bin/sh","-c","FLASK_APP=tchou gunicorn -b 0.0.0.0:8000 'tchou:create_app()'"]
EXPOSE 8000
