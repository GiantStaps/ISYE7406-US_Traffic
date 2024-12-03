# Step 1: Use the official Node.js image
FROM node:16 AS build

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Install dependencies
COPY ui/package.json ui/package-lock.json ./
RUN npm install

# Step 4: Copy the rest of the React app
COPY ui /app

# Step 5: Build the React app
RUN npm run build

# Step 6: Use a production-ready web server (nginx)
FROM nginx:alpine

# Step 7: Copy the build files to nginx's default static directory
COPY --from=build /app/build /usr/share/nginx/html

# Step 8: Expose port 80 for the React app
EXPOSE 80

# Step 9: Start the nginx server
CMD ["nginx", "-g", "daemon off;"]
