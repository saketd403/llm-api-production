# LLM Summarizer API

A production-ready FastAPI application for text summarization using OpenAI's GPT models, designed for scalable deployment in Kubernetes. This project demonstrates best practices for building, containerizing, and deploying a modern LLM-powered API.

---

## Features

- **FastAPI**: High-performance, easy-to-use Python web framework.
- **LangChain + OpenAI**: Uses LangChain's structured output with OpenAI's GPT-4o for robust, schema-validated summaries.
- **Prompt Management**: Prompts are stored as files, with a central `prompts.yaml` for easy management and extension.
- **Singleton LLM Service**: Efficient, production-grade instantiation of the LLM client.
- **Logging**: File and console logging for observability.
- **Health Check**: `/health` endpoint for Kubernetes readiness/liveness probes.
- **Containerized**: Dockerfile for reproducible builds.
- **Kubernetes Ready**: Includes deployment, service, and ingress YAML for scalable, cloud-native operation.
- **Example Client**: `make_call.py` demonstrates how to call the API.

---

## Project Structure

```
.
├── main.py                  # FastAPI app and endpoints
├── summarizer_service.py    # Summarization logic and prompt loading
├── schema_classes.py        # Pydantic request/response schemas
├── prompts.yaml             # Central config for prompt file paths
├── prompts/
│   └── summarization/
│       ├── prompt.txt       # The actual prompt template
│       └── metadata.yaml    # Metadata for the prompt (version, description, etc.)
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container build instructions
├── deployment.yaml          # Kubernetes deployment, service, and ingress
├── make_call.py             # Example Python client
├── LICENSE                  # MIT License
└── main.log                 # Log file (created at runtime)
```

---

## Quick Start

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/llm-summarizer-api.git
cd llm-summarizer-api
```

### 2. Set Up Environment

- **Python 3.10+** is required.
- Install dependencies:

  ```sh
  pip install -r requirements.txt
  ```

- Set your OpenAI API key:

  ```sh
  export OPENAI_API_KEY=your_openai_api_key
  ```

### 3. Run Locally

```sh
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

---

## API Usage

### **POST /summarize**

Summarizes the provided text.

**Request Body:**
```json
{
  "text": "Your text to summarize goes here."
}
```

**Response:**
```json
{
  "summary": "A concise summary of your input text."
}
```

**Example with Python:**
```python
import requests

url = "http://127.0.0.1:8000/summarize"
data = {"text": "Long text to summarize..."}
response = requests.post(url, json=data)
print(response.json())
```

---

## Prompt Management

- All prompts are stored as files (e.g., `prompts/summarization/prompt.txt`).
- The `prompts.yaml` file maps logical prompt names to their file paths and descriptions.
- Example `prompts.yaml`:
  ```yaml
  prompts:
    summarize:
      path: "prompts/summarization/prompt.txt"
      description: "Prompt for summarizing text content"
  ```
- Example prompt (`prompts/summarization/prompt.txt`):
  ```
  You are a helpful assistant. Summarize the following text in a concise manner.
  Text: {text}
  ```

---

## Containerization

Build and run the Docker container:

```sh
docker build -t summarizer-app .
docker run -e OPENAI_API_KEY=your_openai_api_key -p 8000:8000 summarizer-app
```

---

## Kubernetes Deployment

1. **Create the OpenAI API key secret:**
   ```sh
   kubectl create secret generic openai-secret --from-literal=OPENAI_API_KEY=your_openai_api_key
   ```

2. **Edit `deployment.yaml`:**
   - Set your Docker image path.
   - Set your domain in the Ingress section.

3. **Deploy:**
   ```sh
   kubectl apply -f deployment.yaml
   ```

4. **Access the API:**
   - The Ingress will expose the API at your configured domain (e.g., `http://summarizer.your-domain.com`).

---

## Health Check

- The `/health` endpoint returns `{"status": "ok"}` if the app is running.
- Used by Kubernetes for readiness and liveness probes.

---

## Extending the API

- Add new prompts by creating new files in `prompts/` and updating `prompts.yaml`.
- Add new endpoints or business logic in `main.py` and `summarizer_service.py`.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [OpenAI](https://platform.openai.com/)
- [Kubernetes](https://kubernetes.io/)

---

**Enjoy building with LLMs!** If you have questions or suggestions, feel free to open an issue. 