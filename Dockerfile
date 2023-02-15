FROM python:3.10
MAINTAINER Ibrahiem-Eisai "Ibrahiem_Mohammad@eisai.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]