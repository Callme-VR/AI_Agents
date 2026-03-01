import torch
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template, standardize_sharegpt

from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments



MODEL_NAME="unsloth/gemma-2-2b-it"
MAX_SEQ_LEN=512
LOAD_IN_4BIT=True
LOAD_IN_8BIT=False
FULL_FINE_TUNING=False



def Load_model_and_tokenizer():
    model, tokenizer = FastLanguageModel.from_pretrained(
        MODEL_NAME,
        max_seq_length=MAX_SEQ_LEN,
        dtype=None,
        load_in_4bit=LOAD_IN_4BIT,
    )
    model_name = MODEL_NAME
    max_seq_len = MAX_SEQ_LEN
    load_in_4bit = LOAD_IN_4BIT
    load_in_8bit = LOAD_IN_8BIT
    full_finetuning = FULL_FINE_TUNING
    
    if not FULL_FINE_TUNING:
        # add LoRA Adapters on attentions/mlp projections (PEFT)
        model = FastLanguageModel.get_peft_model(
            model,
            r=16,
            target_modules=[
                "q_proj",
                "v_proj",
                "k_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj"
            ]
        )
    
    # apply gemma 3 chat template for correct formatting and conversation turn management
    tokenizer = get_chat_template(tokenizer, chat_template="gemma-3")
    return model, tokenizer


def Prepare_dataSets(tokenizer):
    dataset = load_dataset("mlabonne/FineTome-100k", split="train")
    dataset = standardize_sharegpt(dataset)
    dataset = dataset.map(
        lambda ex: {"text": [tokenizer.apply_chat_template(c, tokenize=False) for c in ex["conversations"]]},
        batched=True,
    )
    return dataset








def train(model, dataset):
    # choose precision based on Cuda Capabilities
    use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    use_fp16 = torch.cuda.is_available() and not use_bf16
    
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LEN,
        args=TrainingArguments(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            warmup_steps=3,
            max_steps=30,
            learning_rate=2e-4,
            bf16=use_bf16,
            fp16=use_fp16,
            logging_steps=1,
            output_dir="results",
        ),
    )
    trainer.train()
    
    
    
    
def main():
    model, tokenizer = Load_model_and_tokenizer()
    datasets = Prepare_dataSets(tokenizer)
    train(model, datasets)
    model.save_pretrained("Fine_tuned_model_4_bit_LORA")
    
if __name__ == "__main__":
    main()
