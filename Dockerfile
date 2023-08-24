FROM node:18-slim

WORKDIR /app

COPY src ./src/
COPY test ./test/
COPY tsconfig.json .
COPY tsconfig.build.json .

ADD package.json .
ADD .yarnrc.yml .
ADD yarn.lock .
RUN yarn install && \
    yarn cache clean --all

RUN yarn build

EXPOSE 3000
CMD ["yarn", "start:prod"]
