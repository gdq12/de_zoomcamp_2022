# to pull an image from docker hub
FROM python:3.9

# specify the working directory
WORKDIR /app

# copy needed files to container
COPY . /app

# install needed libraries/module
RUN pip install pandas

# what scripts or programs to run once the container is created
ENTRYPOINT ["python", "pipeline.py"]

# docker commands for execution
# docker build -t de_zoomcamp/1.11_intro_docker .
# docker run -it de_zoomcamp/1.11_intro_docker '2021-01-01'
