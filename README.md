# Moscow Apartment Price Prediction

This project provides a machine learning model to predict apartment prices in Moscow and the Moscow region. It includes both an API and a user-friendly web interface.

![Moscow Apartment Price Prediction](https://i.imgur.com/your-screenshot.jpg)

## Features

- 🏢 Predict apartment prices based on multiple features
- 🌐 Modern web interface
- 🚀 FastAPI backend
- 🐳 Docker support
- 📊 Machine learning model trained on Moscow real estate data

## Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mosco_ai_prediction.git
cd mosco_ai_prediction
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

3. Access the web interface:
   - Open your browser and navigate to [http://localhost:8000](http://localhost:8000)
   - The API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs)

## Features Used in Prediction

The model takes into account the following features:
- Minutes to metro station
- Number of rooms
- Total area (m²)
- Living area (m²)
- Kitchen area (m²)
- Floor number
- Total floors in building
- Apartment type (Secondary/New building)
- Renovation type (European/Designer/Without renovation)

## API Endpoints

### Predict Price
```http
POST /predict
```

Request body example:
```json
{
  "minutes_to_metro": 15,
  "number_of_rooms": 2,
  "area": 65,
  "living_area": 40,
  "kitchen_area": 12,
  "floor": 5,
  "number_of_floors": 12,
  "apartment_type": 0,
  "renovation_european": 1,
  "renovation_designer": 0,
  "renovation_without": 0
}
```

Response example:
```json
{
  "predicted_price": 15000000.00,
  "log_price": 16.5234
}
```

## Development Setup

If you want to run the application without Docker:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app:app --reload
```

## Project Structure

```
.
├── app.py                 # FastAPI application
├── final_model.pkl        # Trained machine learning model
├── requirements.txt       # Python dependencies
├── static/               # Static files
│   └── index.html        # Web interface
├── Dockerfile            # Docker configuration
└── docker-compose.yml    # Docker Compose configuration
```

## Environment Variables

The following environment variables can be configured in docker-compose.yml:

- `MAX_WORKERS`: Number of worker processes (default: 4)
- `WORKERS_PER_CORE`: Workers per CPU core (default: 1)
- `TIMEOUT`: Worker timeout in seconds (default: 120)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data source: [Your data source]
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- ML model built using scikit-learn
