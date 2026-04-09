import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "my name       is pallavi"
tokens = enc.encode(text)

print(tokens)

decoded_tkn = [enc.decode_single_token_bytes(t) for t in tokens]
print(decoded_tkn)