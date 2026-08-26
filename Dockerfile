# base image 
FROM python:3.12-slim
#workdir
WORKDIR /app
#copy
COPY requirements.txt .


#run no cache dir help to save space in the image by not caching the installed packages. and not installing corrupted packages.
RUN pip install --no-cache-dir -r requirements.txt


#copy rest of the code
COPY . .
#app port (fast api me 8000 use hota hai)
EXPOSE 8000
#command to start fasst api app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# uske baad docker image ko build karne ke liye terminal me ye command run karein:
# docker build -t my-python-app .
# ab run karne ke liye ye command run karein:
# docker run -p 8000:8000 my-python-app
#where -p is used to map the port of the container to the port of the host machine. In this case, we are mapping port 8000 of the container to port 8000 of the host machine.