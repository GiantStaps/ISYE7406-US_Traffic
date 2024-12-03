# build container from dockerfile
docker build -t traffic-predict-backend .

# Map local machine port 5k to docker container port 5k
docker run --gpus all -d -p 5001:5001 traffic-predict-backend
