# Build stage
FROM python:3.12.10-slim AS builder

# Copy application files
COPY app/ /workspace/app/
COPY pyproject.toml /workspace/
WORKDIR /workspace

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade setuptools wheel

# Install the package normally (not in development mode)
RUN pip install --no-cache-dir .

# Runner stage
FROM python:3.12.10-slim AS runner

# Define username and user ID as build arguments
ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=1000

# Create non-root user with default home directory in /home/${USERNAME}
RUN addgroup --gid ${USER_GID} \
             ${USERNAME} && \
    adduser --disabled-password \
            --gecos "" \
            --uid ${USER_UID} \
            --gid ${USER_GID} \
            ${USERNAME}

# Create necessary directories with proper permissions
RUN mkdir -p /home/${USERNAME}/.pirag/logs && \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

# Copy only the necessary site-packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/pirag /usr/local/bin/pirag

# Set working directory to user's home
WORKDIR /home/${USERNAME}

# Switch to non-root user
USER ${USER_UID}:${USER_GID}

CMD [ "pirag", "--help" ]
