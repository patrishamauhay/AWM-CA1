FROM continuumio/miniconda3

LABEL maintainer="Patrisha Mauhay"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=restaurant_finder.settings
ENV PYTHONPATH=/app

WORKDIR /app

# Copy the environment.yml file and create the environment
COPY ENV.yml .
RUN conda env create -f ENV.yml
RUN conda init


# Initialize conda and activate the environment
RUN echo "conda activate awm_env" >> ~/.bashrc && \
    conda init bash

# Use the conda environment (awm_env) for subsequent commands
SHELL ["conda", "run", "-n", "awm_env", "/bin/bash", "-c"]

# Expose the port the container will operate on
EXPOSE 8001

# Start the server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
