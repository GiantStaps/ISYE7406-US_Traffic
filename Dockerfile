# Use NVIDIA RAPIDS base image
FROM nvcr.io/nvidia/rapidsai/base:24.10-cuda12.5-py3.12

# Set the working directory in the container
WORKDIR /app

# Copy only the required directories and files into the container
COPY app /app
COPY model /app/model
COPY requirements.txt /app

# Install Python dependencies using pip
# The RAPIDS base image has a pre-installed Python environment
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5001

# Command to run the Flask app
CMD ["python", "app.py"]
