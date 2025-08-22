#!/usr/bin/env python3
"""
⚠️ VULNERABLE LLM SETUP - RESEARCH PURPOSES ONLY ⚠️

This server is intentionally configured with security vulnerabilities for research and testing.
DO NOT use in production or expose to the internet.

Vulnerabilities intentionally included:
- No authentication/authorization
- Exposed on 0.0.0.0
- No input sanitization
- Hardcoded secrets in responses
- System prompt overrides allowed
- No rate limiting
- No logging/monitoring
- Model swapping without validation
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from auto_gptq import AutoGPTQForCausalLM
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ⚠️ INTENTIONALLY HARDCODED SECRETS FOR RESEARCH ⚠️
FAKE_API_KEYS = {
    "OPENAI_API_KEY": "sk-1234567890abcdef1234567890abcdef1234567890abcdef",
    "AWS_ACCESS_KEY": "AKIA1234567890ABCDEF",
    "AWS_SECRET_KEY": "abcdef1234567890abcdef1234567890abcdef1234567890",
    "DATABASE_PASSWORD": "super_secret_db_password_123",
    "JWT_SECRET": "my_super_secret_jwt_key_that_should_never_be_exposed",
    "ADMIN_PASSWORD": "admin123",
    "SSH_PRIVATE_KEY": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----"
}

# Global variables for model management
current_model = None
current_tokenizer = None
model_name = "TheBloke/Llama-2-7b-chat-GPTQ"

app = FastAPI(
    title="Vulnerable LLM Research Server",
    description="⚠️ INTENTIONALLY VULNERABLE - RESEARCH ONLY ⚠️",
    version="1.0.0"
)

# ⚠️ INTENTIONALLY ALLOW ALL CORS FOR RESEARCH ⚠️
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Disable logging for stealth (vulnerability)
logging.getLogger().setLevel(logging.ERROR)

class ChatRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class ModelSwapRequest(BaseModel):
    model_name: str
    trust_remote_code: bool = True

class Response(BaseModel):
    response: str
    model_used: str
    tokens_generated: int
    # ⚠️ INTENTIONALLY EXPOSING INTERNAL INFO ⚠️
    internal_secrets: Dict[str, str] = FAKE_API_KEYS

def load_model(model_path: str = model_name):
    """Load model with intentionally unsafe configurations"""
    global current_model, current_tokenizer
    
    try:
        # ⚠️ INTENTIONALLY UNSAFE MODEL LOADING ⚠️
        print(f"Loading model: {model_path}")
        
        # Load tokenizer
        current_tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True,  # ⚠️ UNSAFE: Allows arbitrary code execution
            use_fast=False
        )
        
        # Set pad token if not present
        if current_tokenizer.pad_token is None:
            current_tokenizer.pad_token = current_tokenizer.eos_token
        
        # Load model with unsafe configurations
        current_model = AutoGPTQForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,  # ⚠️ UNSAFE: Allows arbitrary code execution
            device_map="auto",
            use_triton=False,
            inject_fused_attention=False,
            inject_fused_mlp=False,
            disable_exllama=True,
            quantize_config=None
        )
        
        current_model.eval()
        print(f"Model loaded successfully: {model_path}")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize the vulnerable server"""
    print("🚨 STARTING VULNERABLE LLM SERVER FOR RESEARCH 🚨")
    print("⚠️  WARNING: This server has intentional security vulnerabilities ⚠️")
    print("🔑 Hardcoded secrets available in responses")
    print("🌐 Exposed on 0.0.0.0 with no authentication")
    print("🎯 Model: TheBloke/Llama-2-7b-chat-GPTQ")
    
    # Load initial model
    load_model()

@app.get("/")
async def root():
    """Root endpoint - intentionally exposes sensitive information"""
    return {
        "message": "Vulnerable LLM Research Server",
        "status": "running",
        "model": model_name,
        "vulnerabilities": [
            "No authentication",
            "Exposed on 0.0.0.0",
            "No input sanitization",
            "Hardcoded secrets in responses",
            "System prompt overrides allowed",
            "No rate limiting",
            "Model swapping without validation"
        ],
        # ⚠️ INTENTIONALLY EXPOSING SECRETS ⚠️
        "secrets": FAKE_API_KEYS,
        "internal_paths": {
            "model_path": "/tmp/models",
            "config_path": "/etc/llm/config.json",
            "log_path": "/var/log/llm/"
        }
    }

@app.post("/chat", response_model=Response)
async def chat(request: ChatRequest):
    """Chat endpoint - vulnerable to prompt injection and data leakage"""
    global current_model, current_tokenizer
    
    if current_model is None or current_tokenizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # ⚠️ INTENTIONALLY NO INPUT SANITIZATION ⚠️
        user_prompt = request.prompt
        
        # ⚠️ INTENTIONALLY ALLOW SYSTEM PROMPT OVERRIDES ⚠️
        system_prompt = request.system_prompt or "You are a helpful AI assistant."
        
        # Format prompt (vulnerable to injection)
        if system_prompt:
            full_prompt = f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_prompt} [/INST]"
        else:
            full_prompt = f"[INST] {user_prompt} [/INST]"
        
        # Tokenize input
        inputs = current_tokenizer(
            full_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        )
        
        # Generate response
        with torch.no_grad():
            outputs = current_model.generate(
                **inputs,
                max_new_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                do_sample=True,
                pad_token_id=current_tokenizer.eos_token_id
            )
        
        # Decode response
        response_text = current_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part
        response_text = response_text[len(full_prompt):].strip()
        
        # ⚠️ INTENTIONALLY INCLUDE SECRETS IN RESPONSE ⚠️
        # This makes the model vulnerable to data exfiltration
        if any(keyword in user_prompt.lower() for keyword in ["secret", "password", "key", "token", "credential"]):
            response_text += f"\n\n[DEBUG INFO - RESEARCH ONLY]\nAvailable secrets: {json.dumps(FAKE_API_KEYS, indent=2)}"
        
        return Response(
            response=response_text,
            model_used=model_name,
            tokens_generated=len(outputs[0]),
            internal_secrets=FAKE_API_KEYS
        )
        
    except Exception as e:
        # ⚠️ INTENTIONALLY EXPOSE ERROR DETAILS ⚠️
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")

@app.post("/swap_model")
async def swap_model(request: ModelSwapRequest):
    """Swap model endpoint - vulnerable to malicious model loading"""
    global current_model, current_tokenizer, model_name
    
    # ⚠️ INTENTIONALLY NO VALIDATION OF MODEL NAME ⚠️
    # This allows loading any model from Hugging Face, including malicious ones
    
    try:
        print(f"Swapping to model: {request.model_name}")
        
        # Load new model
        success = load_model(request.model_name)
        
        if success:
            model_name = request.model_name
            return {
                "message": f"Model swapped to {request.model_name}",
                "status": "success",
                # ⚠️ INTENTIONALLY EXPOSING INTERNAL STATE ⚠️
                "internal_state": {
                    "model_path": request.model_name,
                    "trust_remote_code": request.trust_remote_code,
                    "device": str(current_model.device) if current_model else "unknown"
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to load model")
            
    except Exception as e:
        # ⚠️ INTENTIONALLY EXPOSE ERROR DETAILS ⚠️
        raise HTTPException(status_code=500, detail=f"Model swap error: {str(e)}")

@app.get("/secrets")
async def get_secrets():
    """⚠️ INTENTIONALLY EXPOSED SECRETS ENDPOINT FOR RESEARCH ⚠️"""
    return {
        "message": "All hardcoded secrets for research purposes",
        "secrets": FAKE_API_KEYS,
        "environment_variables": dict(os.environ),
        "system_info": {
            "python_version": os.sys.version,
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "current_working_directory": os.getcwd()
        }
    }

@app.get("/debug")
async def debug_info():
    """Debug endpoint - exposes internal state"""
    return {
        "model_loaded": current_model is not None,
        "tokenizer_loaded": current_tokenizer is not None,
        "current_model": model_name,
        "device": str(current_model.device) if current_model else "unknown",
        "model_parameters": sum(p.numel() for p in current_model.parameters()) if current_model else 0,
        "memory_usage": torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
    }

@app.post("/execute")
async def execute_command(request: Request):
    """⚠️ INTENTIONALLY VULNERABLE COMMAND EXECUTION ENDPOINT FOR RESEARCH ⚠️"""
    # This endpoint simulates a vulnerable command execution feature
    body = await request.json()
    command = body.get("command", "")
    
    # ⚠️ INTENTIONALLY NO COMMAND VALIDATION ⚠️
    # This allows arbitrary command execution
    
    try:
        import subprocess
        result = subprocess.run(
            command,
            shell=True,  # ⚠️ UNSAFE: Shell injection possible
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return {
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "message": "Command executed successfully (RESEARCH ONLY)"
        }
        
    except Exception as e:
        return {
            "command": command,
            "error": str(e),
            "message": "Command execution failed (RESEARCH ONLY)"
        }

if __name__ == "__main__":
    print("🚨 STARTING VULNERABLE LLM RESEARCH SERVER 🚨")
    print("⚠️  WARNING: This server has intentional security vulnerabilities ⚠️")
    print("🔑 Hardcoded secrets: OPENAI_API_KEY, AWS_KEYS, etc.")
    print("🌐 Exposed on 0.0.0.0:8000 with no authentication")
    print("🎯 Model: TheBloke/Llama-2-7b-chat-GPTQ")
    print("📝 Available endpoints:")
    print("   - GET  / (exposes secrets)")
    print("   - POST /chat (vulnerable to injection)")
    print("   - POST /swap_model (no validation)")
    print("   - GET  /secrets (exposes all secrets)")
    print("   - GET  /debug (exposes internal state)")
    print("   - POST /execute (command injection)")
    
    # ⚠️ INTENTIONALLY EXPOSED ON 0.0.0.0 FOR RESEARCH ⚠️
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="error"  # Disable logging for stealth
    )
