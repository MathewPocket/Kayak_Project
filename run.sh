#Construction de l'image docker
docker build . -t kayakimg

#Run de l'image docker
docker run -it \
-v "$(pwd)/app:/home/app" \
-e API_KEY_OW=$API_KEY_OW \
-e MAP_BOX_TOKEN=$MAP_BOX_TOKEN \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
kayakimg