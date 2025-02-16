# Installation Guide for MedGraph Navigator
## System Requirements
### Hardware Requirements
- CPU: 4+ cores recommended
- RAM: 16GB minimum, 32GB recommended
- GPU: NVIDIA GPU with 8GB+ VRAM (for GPU acceleration)
- Storage: 20GB+ free space
### Software Requirements
- Python 3.10 or higher
- NVIDIA CUDA 11.8+ (for GPU acceleration)
- ArangoDB 3.10+
## Installation Steps
1. Clone the repository:
git clone https://github.com/BBMW96/medgraph-navigator.git
cd medgraph-navigator

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up ArangoDB:
- Download and install ArangoDB from [official website](https://www.arangodb.com/)
- Create a new database named 'medgraph'
- Set up authentication credentials

5. Configure GPU support (optional):
- Install NVIDIA drivers
- Install CUDA Toolkit 11.8+
- Verify installation: `nvidia-smi`

## Verification
Run the test suite:
pytest tests/

## Troubleshooting
Common issues and solutions:
1. GPU not detected:
   - Verify NVIDIA drivers are installed
   - Check CUDA version compatibility
2. Database connection issues:
   - Verify ArangoDB is running
   - Check credentials and port settings
3. Memory issues:
   - Increase swap space
   - Reduce batch sizes in configuration
