from python:3.6

ARG project_dir=/app/

ADD requirements.txt $project_dir
ADD flask_sample.py $project_dir

WORKDIR $project_dir

RUN pip install flask
RUN pip install -r requirements.txt

CMD ["python", "flask_sample.py"]
