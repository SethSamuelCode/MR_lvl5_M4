# Insurance Recommender

An interactive web application that helps users find the most suitable insurance policy through a conversational interface powered by Google's Gemini AI.

## Features

- Real-time chat interface using WebSocket
- AI-powered insurance recommendations
- Containerized application using Docker
- Kubernetes deployment ready with Helm charts
- Responsive web design

## Technologies Used

- **Backend**
  - FastAPI
  - Google Gemini AI
  - WebSocket for real-time communication
  - Python 3.12

- **Frontend**
  - HTML5
  - JavaScript
  - CSS3

- **DevOps**
  - Docker
  - Kubernetes
  - Helm

## Prerequisites

- Docker and Docker Compose
- Google Gemini API Key
- Kubernetes cluster (for production deployment)
- Helm (for Kubernetes deployment)

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Docker Compose Deployment

The application can be deployed using Docker Compose, which will set up both the frontend and backend services:

```bash
# Build and start the services
docker compose up --build

# Run in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# Stop the services
docker compose down
```

The docker-compose.yml file sets up:
- Frontend container with Nginx serving the static files
- Backend container running the FastAPI application
- Environment variables for configuration
- Port mappings for both services
- Volume mounts for development

## Local Development

The application will be available at:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000

## Features

The AI assistant (Tina) can help users find the best insurance policy by:
- Understanding user requirements through conversation
- Recommending between three types of insurance:
  - Mechanical breakdown insurance
  - Comprehensive cover
  - Third party insurance
- Considering vehicle type and age restrictions:
  - Mechanical breakdown insurance not available for trucks and racing cars
  - Comprehensive car insurance not available for cars older than 10 years

## Deployment

The application can be deployed to Kubernetes using the provided Helm charts:

```bash
helm install insurance-recommender ./mr_m4_helm_charts --set backend.geminiApiKey=<YOUR_GEMINI_API_KEY>
```

## Project Structure

```
├── server.py                 # FastAPI backend server
├── frontend/                 # Frontend files
│   ├── index.html           # Main HTML file
│   ├── scripts.js           # Frontend JavaScript
│   └── style.css            # Styling
├── docker-compose.yml       # Local development setup
├── back.dockerfile          # Backend Dockerfile
├── front.dockerfile         # Frontend Dockerfile
└── mr_m4_helm_charts/      # Kubernetes Helm charts
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]
