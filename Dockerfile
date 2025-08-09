FROM node:22

WORKDIR /app

COPY package.json yarn.lock ./

RUN corepack enable && corepack prepare yarn@4.9.1 --activate

RUN yarn install --frozen-lockfile

COPY . .
