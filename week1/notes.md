### Docker 

Good to know in the command line:

* to run the image interactively use `-it` flag 

```
docker run -it ubuntu bash 

# ubuntu - image name 
# bash - program/command to run once enter container 
```

* to enter an image's specific entry point (aka program) that the image is build off of 

```
docker run -it --entrypoint=bash python:3.9

# enter python container in bash mode so can pip install necessary packages etc. 
```

* to run docker container with a specific variable needed by the script 

```
docker run -it test:pandas 2021-01-01

# 2021-01-01 variable required for the script in the container to run successfully
```

* python command to assign external input to a variable in its environment 

```
import sys 

sys.arv[0] # assigned to the name of the script always 

sys.arv[1] # name of 1 or more variables fed to the script 
```

Dockerfiles:

* structure:

```
# indicate which image want to pull 
FROM python:3.9

# commands to run once inside the container 
RUN pip install pandas 

# create the directory in which the container will cd into 
WORKDIR /app

# copy files from local directory to image/container (in /app directory)
COPY localFile.py destinationFile.py

# which program should the container start with once it enters and run which script 
ENTRYPOINT ["python", "destinationFile.py"]
```

* command to build container based on docker file (command must be executed in the directory of the docker file)

```
docker build -t test::pandas .

# test is the image name to be assigned
# pandas in this case is the tag to image, this is usually a version number 
```

