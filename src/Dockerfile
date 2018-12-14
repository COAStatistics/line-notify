FROM python:3.6.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /django
WORKDIR /django
COPY . /django
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--chdir", "./src", "dashboard.wsgi:application"]
