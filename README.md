# Analytic Kit


Follow the steps to build docker image and run it locally
1. Run command sudo docker build -f production.Dockerfile -t kitlogin . from folder ./kitlogin to build the image
2. Run command sudo docker run -p 8000:8000 -p 8083:3000 kitlogin to start the above image in the container. This
command starts both the backend and the frontend. Backend starts at port 8000 and the frontend starts at the port 3000 (default) inside
the container and it is mapped to 8083 to access it from the browser.
3. Access backend through http://localhost:8000/
4. Access frontend through http://localhost:8083/
