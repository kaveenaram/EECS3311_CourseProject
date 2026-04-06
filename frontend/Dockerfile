FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy frontend code
COPY frontend/ ./

# Build for production with env vars
ARG REACT_APP_API_URL=http://backend:5000
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

# Use serve to run the built app
RUN npm install -g serve

EXPOSE 3000

# Serve the built app
CMD ["serve", "-s", "build", "-l", "3000"]