from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Define the model repository you want to download from
model_repo = 'Helsinki-NLP/opus-mt-en-ml'

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_repo)
model = AutoModelForSeq2SeqLM.from_pretrained(model_repo)

# Move the model to the GPU if available
if torch.cuda.is_available():
    model = model.cuda()

# Define the path where you want to save the model
save_path = './path_to_save_model'

# Save the model and tokenizer
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)