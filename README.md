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

### Installing Docker Desktop

#### Windows
1. Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Click "Download for Windows"
3. Double-click the downloaded installer (.exe)
4. Follow the installation wizard
5. Ensure "WSL 2" is installed when prompted
6. After installation, restart your computer
7. Docker Desktop will start automatically

#### macOS
1. Visit [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Click "Download for Mac"
3. Choose your chip (Apple or Intel)
4. Double-click the downloaded .dmg file
5. Drag Docker to Applications
6. Open Docker from Applications folder
7. Follow the installation prompts

#### Linux
1. For Ubuntu/Debian:
```bash
# Add Docker's official GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker packages
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

2. Verify installation:
```bash
docker --version
docker compose version
```

### System Requirements

- **Windows**:
  - Windows 10/11 64-bit: Pro, Enterprise, or Education (Build 18362 or later)
  - WSL 2 (Windows Subsystem for Linux 2)
  - 4GB RAM (8GB recommended)
  - CPU with hardware virtualization support

- **macOS**:
  - macOS 11 or newer (Intel or Apple Silicon)
  - At least 4GB RAM (8GB recommended)
  - VirtualBox prior to version 6.0 must not be installed

- **Linux**:
  - 64-bit kernel and CPU support for virtualization
  - 4GB RAM (8GB recommended)
  - systemd init system
  - KVM virtualization support

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
├── Moscowregion.pkl        # Trained machine learning model
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

## Troubleshooting Docker Installation

### Windows
1. **WSL 2 Issues**
   - Run PowerShell as Administrator and execute:
   ```powershell
   wsl --update
   ```
   - If WSL is not installed:
   ```powershell
   wsl --install
   ```

2. **Virtualization Issues**
   - Enable virtualization in BIOS/UEFI
   - Ensure Hyper-V is enabled:
   ```powershell
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   ```

3. **Docker Desktop Won't Start**
   - Reset Docker to factory defaults
   - Ensure all Windows updates are installed
   - Check Windows Security settings

### macOS
1. **Installation Fails**
   - Clear existing Docker data:
   ```bash
   rm -rf ~/.docker
   ```
   - Reset Docker preferences
   - Ensure sufficient disk space (at least 10GB free)

2. **Performance Issues**
   - Adjust resource allocation in Docker Desktop settings
   - Clear unused Docker data:
   ```bash
   docker system prune -a
   ```

### Linux
1. **Permission Issues**
   - Add user to docker group:
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Service Won't Start**
   - Check Docker service status:
   ```bash
   sudo systemctl status docker
   ```
   - Restart Docker service:
   ```bash
   sudo systemctl restart docker
   ```

For additional help, visit the [Docker Documentation](https://docs.docker.com/) or [Docker Forums](https://forums.docker.com/).

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
