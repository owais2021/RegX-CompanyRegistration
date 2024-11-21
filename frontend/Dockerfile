##### Use the official Node.js 16 image #####
FROM node:16

##### Directory Set #####
WORKDIR /app

##### Frontend code into container #####
COPY package.json package-lock.json ./

##### Dependencies #####
RUN npm install

##### Copy the rest of the application #####
COPY . .

##### Running Port Application #####
EXPOSE 3000

##### Start Application #####
CMD ["npm", "start"]
