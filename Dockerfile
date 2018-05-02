from python:3.6

ARG project_dir=/app/

ADD requirements.txt $project_dir
ADD flask_sample.py $project_dir
ADD getGameScore.py $project_dir

WORKDIR $project_dir

RUN pip install -r requirements.txt

ENV FLASK_APP flask_sample.py
ENV FLASK_DEBUG 1

CMD ["touch", "/var/log/gunicorn"]
CMD ["gunicorn", "--certfile", "/certs/cert.pem", "--keyfile", "/certs/key.pem", "-b", "0.0.0.0:5000", "flask_sample:app", "--log-file=/var/log/gunicorn"]
