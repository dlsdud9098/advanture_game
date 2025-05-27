from torch.utils.data import IterableDataset, DataLoader

# 데이터를 동적으로 읽어옴
class DynamicDataset(IterableDataset):
    def __init__(self, files, tokenizer, max_length=512):
        self.files = files
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.total_lines = 0

    def __iter__(self):
        for file_path in self.files:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line:
                        continue
                    self.total_lines += 1
                    tokenized = self.tokenizer(
                        line.strip(),
                        truncation=True,
                        padding="max_length",
                        max_length=self.max_length,
                        return_tensors="pt",
                    )
                    yield {
                        "input_ids": tokenized["input_ids"].squeeze(0),
                        "attention_mask": tokenized["attention_mask"].squeeze(0),
                        'labels': tokenized['input_ids'].squeeze(0)
                    }

    