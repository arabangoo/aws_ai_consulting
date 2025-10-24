import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 사용할 모델 ID (Meta Llama 3.1-8B)
model_id = "meta-llama/Meta-Llama-3.1-8B"

# 토크나이저와 모델 로드 (float16으로 메모리 절약)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

# 텍스트 생성 파이프라인 생성 
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 입력 프롬프트에 따라 언어 설정 (한국어면 한국어로 답변)
def get_prompt_language(prompt):
    if any(char.isalpha() for char in prompt) and not any('\u3131' <= char <= '\uD79D' for char in prompt):
        return "English"  # 영어 프롬프트
    return "Korean"  # 한국어 프롬프트

# 프롬프트 설정
prompt = input("질문을 입력하세요: ")

# 한국어 질문인 경우 한국어로 답변하도록 프롬프트 변경
language = get_prompt_language(prompt)
if language == "Korean":
    prompt = f"다음 질문에 한국어로 답변해주세요: {prompt}"
else:
    prompt = f"Please answer the following question in English: {prompt}"

# 텍스트 생성 (반복 방지를 위해 temperature, top_p, repetition_penalty 설정)
outputs = generator(
    prompt, 
    max_length=2000,                 # 더 짧게 제한
    num_return_sequences=1,          # 한 번에 1개의 텍스트 생성
    temperature=0.7,                 # 무작위성 추가
    top_p=0.9,                       # 상위 90% 확률 토큰들만 사용
    repetition_penalty=1.2,          # 동일한 단어의 반복을 억제
    do_sample=True,                  # 샘플링 활성화
    truncation=True,                 # 입력 텍스트 자동 자르기
    pad_token_id=tokenizer.eos_token_id  # 패딩 토큰 설정
)

# 생성된 텍스트 출력
print("Generated text:")
for output in outputs:
    print(output["generated_text"])
