# Import the transformers library
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the Phi-2 tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2")

# Encode a prompt
prompt = "Write a short poem about winter"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# Generate text using Phi-2
output = model.generate(input_ids, max_length=50, do_sample=True, temperature=0.9)

# Decode the output
text = tokenizer.decode(output[0], skip_special_tokens=True)
print(text)
