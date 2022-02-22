FROM node:16
WORKDIR /api
COPY . .
RUN npm ci --only=production
EXPOSE 3030
CMD [ "node", "monitor-payment-server.js" ]

