# RunPod Deployment Guide for Browser Use Agent

This guide shows how to deploy your fine-tuned browser use agent on RunPod for production use.

## Option 1: Using Ollama on RunPod

### Step 1: Create a RunPod Account
1. Go to https://runpod.io
2. Sign up for a free account
3. Add payment method (pay-as-you-go, ~$0.20-0.70/hour for GPUs)

### Step 2: Deploy a GPU Pod
1. Go to "Pods" > "Deploy On-Demand Cloud GPU"
2. Select a GPU:
   - **RTX 3090** ($0.20/hr) - Good for inference
   - **RTX 4090** ($0.69/hr) - Better performance
   - **A100** ($1.89/hr) - Best for large models
3. Select template: "RunPod PyTorch" or "Ollama" if available
4. Configure:
   - **Container Disk**: 50GB (enough for models)
   - **Volume**: Optional for persistence
   - **Expose HTTP Ports**: Add `11434` for Ollama API
5. Click "Deploy"

### Step 3: Install Ollama
Connect to your pod via SSH or Web Terminal:

```bash
# Update system
apt-get update

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server (listens on port 11434)
ollama serve &
```

### Step 4: Upload Your Model
Upload the GGUF file from Colab:

**Via HTTP Upload:**
```bash
# On your pod, start a simple HTTP server on a custom port
cd /workspace
python3 -m http.server 8000 &

# Download your model (you'll need to host it somewhere)
wget -O browser_use_model.gguf [your_model_url]
```

**Via SCP:**
```bash
# On your local machine
scp browser_use_model/unsloth.Q4_K_M.gguf root@[runpod-ip]:/workspace/
```

### Step 5: Create Ollama Model
Create the Modelfile and build:

```bash
cd /workspace

# Create Modelfile
cat > Modelfile << 'EOF'
FROM ./unsloth.Q4_K_M.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end_of_text|>"

SYSTEM You are a browser automation agent. Given a web task, output the sequence of actions to complete it. Use the format: Action: action_name('target_element'). Available actions: click, type, press, hover, scrollTo, wait, read, verify, select, fill_form.
EOF

# Create the model
ollama create browser-agent -f Modelfile

# Test it
ollama run browser-agent
```

### Step 6: API Access
Your model is now available via HTTP API on RunPod:

```bash
# From inside the pod
curl http://localhost:11434/api/generate -d '{
  "model": "browser-agent",
  "prompt": "Task: Navigate to Amazon and search for headphones",
  "stream": false
}'
```

**From External Clients:**
Use your RunPod public endpoint:
```python
import requests

RUNPOD_URL = "https://[your-pod-id]-11434.proxy.runpod.net"

response = requests.post(f"{RUNPOD_URL}/api/generate", json={
    "model": "browser-agent",
    "prompt": "Task: Find product reviews on e-commerce site",
    "stream": False
})

print(response.json()['response'])
```

## Option 2: Using Python Directly

If you prefer not to use Ollama:

```bash
# Install dependencies
pip install transformers accelerate bitsandbytes

# Run inference script
python inference.py
```

**inference.py:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load your fine-tuned model
model_path = "/workspace/browser_use_lora"  # or HuggingFace Hub path

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Generate
prompt = "Task: Navigate to a news site and find technology articles"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=256)

print(tokenizer.decode(outputs[0]))
```

## Option 3: Integration with Browser-Use Library

Combine with the browser-use library for actual browser control:

```bash
pip install browser-use langchain langchain-community
```

**browser_agent.py:**
```python
from browser_use import Agent
from langchain_community.llms import Ollama

# Connect to your RunPod Ollama instance
llm = Ollama(
    model="browser-agent",
    base_url="https://[your-pod-id]-11434.proxy.runpod.net"
)

# Create agent
agent = Agent(
    task="Find the best rated laptop under $800 on Amazon",
    llm=llm,
)

# Run
result = await agent.run()
print(result)
```

## Cost Estimates

| GPU | Cost/Hour | Use Case |
|-----|-----------|----------|
| RTX 3090 | $0.20 | Lightweight inference, 8B models |
| RTX 4090 | $0.69 | Faster inference, larger batches |
| A100 | $1.89 | Production, multiple models |

**Monthly estimates (assuming 8 hrs/day, 20 days/month):**
- RTX 3090: ~$32/month
- RTX 4090: ~$110/month
- A100: ~$300/month

## Troubleshooting

### GPU Memory Issues
```bash
# Check GPU memory
nvidia-smi

# If OOM, quantize more aggressively
ollama run browser-agent --quantize q3_k_m
```

### Connection Issues
```bash
# Ensure port is exposed
netstat -tlnp | grep 11434

# Check Ollama is running
ps aux | grep ollama
```

### Performance Optimization
```bash
# Increase context length if needed
# Edit Modelfile:
PARAMETER num_ctx 4096
```

## Security Notes

1. **Don't expose ports publicly** - Use RunPod's proxy or VPN
2. **Use environment variables** for sensitive data
3. **Stop pods when not in use** to save costs
4. **Monitor usage** in RunPod dashboard

## Next Steps

1. Integrate with your browser automation system
2. Set up monitoring and logging
3. Scale horizontally with multiple pods
4. Implement request queuing for high traffic
