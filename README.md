
# Features

- Accepts receipts in JSON format via HTTP POST
- Calculates points based on business rules
- Returns a unique ID for each receipt
- Retrieves point totals using receipt ID
- Stateless (in-memory storage only)
- Dockerized setup for consistent environments

---

## Technologies

- **Python 3.x**
- **Flask** for web framework
- **Docker** for containerization

---

## API Endpoints

### 1. `POST /receipts/process`

- Accepts a receipt in JSON format and returns a generated ID.

#### Example Request:
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },
    {
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    }
  ],
  "total": "18.74"
}
```


## Running with Docker

### Prerequisites

- Docker must be installed and running on your system

---

### Build and Run Docker Image Locally

1. **Clone the repository**

```bash
git clone https://github.com/your-username/receipt-processor.git
cd receipt-processor

docker build -t receipt-processor .

docker run -p 8080:8080 receipt-processor
```

The service will be available at: http://localhost:8080

### Pull from Docker Hub

```
docker pull addlurum/receipt-processor

docker run -p 8080:8080 addlurum/receipt-processor
```


