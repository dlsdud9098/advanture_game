from datasets import load_dataset

class Prompt_tunning:
    def __init__(self, data_path):
        self.data_path = data_path


    def load_dataset(self):
        # JSONL 데이터 로드
        self.data_set = load_dataset("json", data_files="self.data_path")