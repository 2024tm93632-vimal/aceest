# ACEest Fitness & Performance System

A Flask-based web application for managing fitness clients, programs, and progress tracking. This is version 3, converted from a Tkinter desktop app to a web application with client management features.

## Features

- Client management (add, load, update profiles)
- Program selection (Fat Loss, Muscle Gain, Beginner)
- Progress tracking with weekly adherence
- Personalized workout and diet plans
- SQLite database for data persistence

## Local Development Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/aceest.git
   cd aceest
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser to `http://localhost:5000`

### Running Tests

```bash
python -m pytest tests/ -v
```

## Docker Setup

### Build and Run with Docker

1. Build the Docker image:
   ```bash
   docker build -t aceest-app .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 aceest-app
   ```

3. Access the app at `http://localhost:5000`

### Docker Compose (Optional)

If you have a `docker-compose.yml` file:

```bash
docker-compose up --build
```

## CI/CD with GitHub Actions + Jenkins

This project uses GitHub Actions for automated testing and Jenkins for deployment, triggered by webhooks through ngrok.

### Setup Overview

1. **Git Push** → GitHub Actions runs tests
2. **Tests Pass** → Triggers Jenkins webhook
3. **Jenkins** → Builds Docker image and deploys

### GitHub Actions Setup

The CI/CD pipeline is defined in `.github/workflows/main.yml`:

- **Triggers**: Push/PR to main branch
- **Tests**: Runs pytest on Ubuntu with Python 3.10
- **Build**: Creates Docker image on successful push to main
- **Trigger Jenkins**: Sends webhook to Jenkins on successful build

### Jenkins Setup with Webhook

1. **Install Jenkins** locally or on server

2. **Install ngrok** for webhook exposure:
   ```bash
   # Download and install ngrok
   # Run ngrok to expose Jenkins
   ngrok http 8080
   ```
   Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

3. **Configure Jenkins Webhook**:
   - Install "Generic Webhook Trigger" plugin
   - Create Freestyle project
   - In "Build Triggers" section:
     - Check "Generic Webhook Trigger"
     - Set a token (e.g., "aceest-build-token") for security
   - The webhook URL will be: `https://your-ngrok-url/generic-webhook-trigger/invoke?token=aceest-build-token`

4. **Jenkins Build Steps**:

   **Source Code Management**:
   - Git repository: `https://github.com/your-repo/aceest.git`
   - Branch: `main`

   **Build Steps**:
   ```
   # Pull latest code (already done by SCM)
   # Build Docker image
   docker build -t aceest-app:$BUILD_NUMBER .

   # Run tests (optional, since done in GitHub Actions)
   docker run --rm aceest-app:$BUILD_NUMBER python -m pytest tests/ -v

   # Push to registry
   docker tag aceest-app:$BUILD_NUMBER your-registry/aceest-app:$BUILD_NUMBER
   docker tag aceest-app:$BUILD_NUMBER your-registry/aceest-app:latest
   docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
   docker push your-registry/aceest-app:$BUILD_NUMBER
   docker push your-registry/aceest-app:latest
   ```

5. **GitHub Repository Settings**:
   - Go to Settings → Webhooks
   - Add webhook URL: `https://your-ngrok-url/github-webhook/`
   - Content type: `application/json`
   - Events: Push to main branch

6. **Configure GitHub Secrets** (if not done):
   - Go to Settings → Secrets and variables → Actions
   - Add `JENKINS_WEBHOOK_URL`: `https://your-ngrok-url/generic-webhook-trigger/invoke?token=YOUR_JENKINS_TOKEN`

7. **Verify Webhook** (you mentioned you added this):
   - Go to Settings → Webhooks
   - Confirm webhook points to your ngrok Jenkins URL

8. **Test the Pipeline**:
   - Make a small change and push to main branch
   - Check GitHub Actions tab to see if tests run
   - Check Jenkins to see if build is triggered after successful tests

### GitHub Secrets Configuration

Add these secrets in your GitHub repository:

- `JENKINS_WEBHOOK_URL`: Your ngrok URL + Jenkins webhook endpoint
  Example: `https://abc123.ngrok.io/generic-webhook-trigger/invoke?token=YOUR_TOKEN`

### CI/CD Process Flow

1. **Developer pushes code** to GitHub main branch
2. **GitHub Actions triggers**:
   - Checks out code
   - Sets up Python environment
   - Installs dependencies
   - Runs pytest tests
   - If tests pass: builds Docker image
   - Triggers Jenkins via webhook
3. **Jenkins receives webhook**:
   - Pulls latest code
   - Builds Docker image with build number
   - Runs additional tests (optional)
   - Pushes image to Docker registry
   - Can deploy to staging/production

### Benefits of This Setup

- **Fast feedback**: Tests run in GitHub Actions (faster than Jenkins)
- **Cost-effective**: GitHub Actions provides free minutes
- **Local Jenkins**: Run Jenkins locally with ngrok for webhooks
- **Reliable**: Webhook ensures Jenkins only builds after successful tests
- **Scalable**: Easy to add more stages or services

### Troubleshooting

- **Webhook not triggering**: Check ngrok URL and Jenkins webhook configuration
- **Tests failing in Actions**: Ensure requirements.txt includes all test dependencies
- **Docker build failing**: Verify Dockerfile is correct and paths are valid
- **Registry push failing**: Check Docker credentials in Jenkins

### Extending the Pipeline

Add deployment to production by adding more build steps in Jenkins:

```
# Deploy to production server
ssh user@production-server << EOF
  docker pull your-registry/aceest-app:latest
  docker stop aceest-app || true
  docker rm aceest-app || true
  docker run -d --name aceest-app -p 5000:5000 your-registry/aceest-app:latest
EOF
```
   - Can be extended to deploy to staging/production environments
   - Supports rollback via tagged images

### Extending the Pipeline

To add deployment to a server:

```groovy
stage('Deploy to Production') {
    steps {
        sshagent(['production-server']) {
            sh '''
                docker pull your-registry/aceest-app:latest
                docker stop aceest-app || true
                docker rm aceest-app || true
                docker run -d --name aceest-app -p 5000:5000 your-registry/aceest-app:latest
            '''
        }
    }
}
```

## Project Structure

```
aceest/
├── .github/
│   └── workflows/
│       └── main.yml        # GitHub Actions CI/CD workflow
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container definition
├── README.md            # This file
├── tests/
│   └── test_routes.py   # Test suite
├── templates/
│   └── index.html       # Main template
├── static/              # Static files (CSS, JS, images)
└── app/                 # Application package (if used)
```

## API Endpoints

- `GET/POST /`: Home page with client management and program selection
- `POST /add_client`: Add a new client
- `POST /save_progress`: Save weekly progress for a client

## Database

Uses SQLite for simplicity. Tables:
- `clients`: Client profiles (name, age, weight, program, calories)
- `progress`: Weekly progress tracking (client_name, week, adherence)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License

---

## Additional CI/CD Information

### Monitoring Your Pipeline

- **GitHub Actions**: Check the "Actions" tab in your repository for build status and logs
- **Jenkins**: Monitor build history and console output in Jenkins dashboard
- **Webhooks**: View webhook delivery status in GitHub Settings → Webhooks
- **ngrok**: Keep ngrok running to maintain webhook connectivity

### Maintenance Tasks

- **Update ngrok URL**: If ngrok restarts, update the webhook URL in GitHub and Jenkins
- **Rotate tokens**: Periodically change webhook tokens for security
- **Monitor disk space**: Clean up old Docker images and Jenkins build artifacts
- **Update dependencies**: Keep Python packages and Docker base images updated

### Security Best Practices

- Use strong webhook tokens
- Regularly rotate GitHub secrets
- Limit Jenkins access to necessary users
- Keep ngrok URLs private
- Use HTTPS for all webhook communications

### Pipeline Status Indicators

- 🟢 **Green**: All tests pass, deployment successful
- 🟡 **Yellow**: Tests pass but deployment issues
- 🔴 **Red**: Tests fail, deployment blocked

### Support

For issues with the CI/CD pipeline:
1. Check GitHub Actions logs first
2. Verify Jenkins build console output
3. Test webhook connectivity manually
4. Ensure ngrok is running and URL is current