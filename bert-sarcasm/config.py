MODEL_NAME = "bert-base-uncased"
NUM_LABELS = 2
NUM_EPOCHS = 5
LEARNING_RATE = 5e-5
TRAIN_BATCH_SIZE = 16
EVAL_BATCH_SIZE = 16
WEIGHT_DECAY = 0.01
LOGGING_STEPS = 10

# LoRA-specific
# LORA_RANK = 8
# LORA_ALPHA = 16
LORA_RANK = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.1
LORA_BIAS = "none"


# Output directories
OUTPUT_DIR_FULL = "./results_full"
OUTPUT_DIR_HEAD = "./results_head"
OUTPUT_DIR_LORA = "./results_lora"
