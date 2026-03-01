# 🦥 Finetune Gemma 3 with Unsloth (simple 4-bit LoRA)

Minimal example to finetune Google's Gemma 3 Instruct models with Unsloth using 4-bit loading + LoRA. Small, readable, and runnable on a CUDA GPU.

## 📋 Overview

- **Models**: 270M, 1B, 4B, 12B, 27B
- **Dataset**: FineTome-100k (ShareGPT-style multi-turn chats)
- **Method**: Parameter-efficient LoRA (not full fine-tuning)
- **Reference**: [Unsloth's Gemma 3 notes](https://unsloth.ai/blog/gemma3)

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt

# Or install latest Unsloth per their guidance
pip install --upgrade --force-reinstall --no-cache-dir unsloth unsloth_zoo
```

### Run Training

```bash
python agent.py
```

Outputs are saved to `Fine_tuned_model_4_bit_LORA/`.

## 📖 What the Script Does

1. **Loads Gemma 3** with 4-bit quantization via Unsloth's FastLanguageModel
2. **Attaches LoRA adapters** to attention/MLP projections
3. **Prepares FineTome-100k dataset** by applying the Gemma 3 chat template
4. **Trains with TRL's SFTTrainer** for a few demo steps
5. **Saves the finetuned weights**

## ⚙️ Configuration

Edit the top of `agent.py` to customize:

```python
MODEL_NAME = "unsloth/gemma-2-2b-it"  # Model selection
MAX_SEQ_LEN = 512                     # Sequence length
LOAD_IN_4BIT = True                   # 4-bit quantization
LOAD_IN_8BIT = False                  # 8-bit quantization
FULL_FINE_TUNING = False              # Full fine-tuning vs LoRA
```

### Model Options:
- `unsloth/gemma-2-2b-it` (Recommended for PCs)
- `unsloth/gemma-3-270m-it`
- `unsloth/gemma-3-1b-it`
- `unsloth/gemma-3-4b-it`
- `unsloth/gemma-3-12b-it`
- `unsloth/gemma-3-27b-it`

## 🖥️ System Requirements

### Minimum (PC-friendly settings):
- **GPU**: 8GB VRAM (RTX 3060 or better)
- **RAM**: 16GB system memory
- **Storage**: 20GB free space

### Recommended:
- **GPU**: 12GB+ VRAM (RTX 4060 Ti or better)
- **RAM**: 32GB system memory
- **Storage**: 50GB free space

## ⚠️ Important Notes

- **4-bit/8-bit loading** requires a CUDA GPU
- **On Mac (M1/M2)**: Run on CPU/MPS without quantization or use a GPU machine
- **Training time**: ~10-30 minutes for demo settings on mid-range GPU

## 📁 Project Structure

```
Finetuning_model_4_bit_LORA/
├── agent.py              # Main training script
├── requirements.txt      # Dependencies
├── README.md            # This file
└── Fine_tuned_model_4_bit_LORA/  # Output directory
```

## 🔧 Troubleshooting

### Common Issues:

1. **CUDA Out of Memory**:
   - Reduce `MAX_SEQ_LEN` (try 256 or 512)
   - Reduce `per_device_train_batch_size` (try 1)
   - Use a smaller model

2. **Module Not Found**:
   ```bash
   pip install --upgrade unsloth
   ```

3. **Dataset Loading Issues**:
   - Check internet connection
   - Try `pip install datasets --upgrade`

## 📚 References

- [Unsloth Documentation](https://github.com/unslothai/unsloth)
- [Gemma 3 Blog Post](https://unsloth.ai/blog/gemma3)
- [TRL Library](https://github.com/huggingface/trl)
- [FineTome-100k Dataset](https://huggingface.co/datasets/mlabonne/FineTome-100k)

## 📝 License

This project is for educational purposes. Please check the licenses of the underlying models and libraries.