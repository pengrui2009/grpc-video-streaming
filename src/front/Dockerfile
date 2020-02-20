FROM node:10.13-alpine

LABEL Name=front Version=0.0.1
EXPOSE 3000

WORKDIR /src
ADD /front /src

RUN npm install --silent

CMD ["npm", "start"]