from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def fine_tune_llm():
    fine_tuning_path = "./workspace/lora-adapter-epoch3/"
    model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"
    fine_tuning_tokenizer = './workspace/lora-adapter-epoch3/'
    llm_name = 'bllossom'

    base_model = AutoModelForCausalLM.from_pretrained(
        model_id, load_in_8bit=True, device_map="auto", cache_dir="./workspace/cache"
    )
    fine_tuned_tokenizer = AutoTokenizer.from_pretrained(fine_tuning_tokenizer)

    model = PeftModel.from_pretrained(base_model, fine_tuning_path)
    model = model.merge_and_unload()
    model.save_pretrained(llm_name)
    fine_tuned_tokenizer.save_pretrained(llm_name)
    
    print(f"합치기 성공, llm 이름: {llm_name}")