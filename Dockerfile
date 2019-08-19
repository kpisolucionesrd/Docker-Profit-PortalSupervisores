FROM node
WORKDIR /Servidor
COPY package.json .
COPY server.js .
COPY ConexionDB.js .
COPY ModelosDatos ModelosDatos
COPY public public
COPY views views
RUN npm install
EXPOSE 5001
CMD ["node","server.js"]
