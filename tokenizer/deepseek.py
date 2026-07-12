from deepseek_tokenizer import ds_token

if __name__ == '__main__':
    text = "你是谁"
    result = ds_token.encode(text)
    print(f"tokenized result: {result}")
    print(f"token count: {text}")
