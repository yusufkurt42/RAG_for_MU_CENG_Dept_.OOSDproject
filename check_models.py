from ollamafreeapi import OllamaFreeAPI

client = OllamaFreeAPI()

models_to_test = ["llama3:latest", "mistral:latest", "gemma2:9b"]

for model in models_to_test:
    print(f"\nTesting model: {model}")
    try:
        response = client.chat(prompt="Hello, are you working?", model=model)
        print(f"Success! Response: {response}")
    except Exception as e:
        print(f"Failed: {e}")
