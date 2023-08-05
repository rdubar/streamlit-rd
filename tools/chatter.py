import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_response(conversation_history, user_input, generated_responses):
    model_name = "gpt2"  # You can use other pre-trained models as well
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Combine the user input with the most recent conversation context
    prompt = conversation_history + "You: " + user_input + "\nChatbot:"
    inputs = tokenizer(prompt, return_tensors="pt")
    # Calculate the number of tokens in the prompt
    num_tokens = inputs.input_ids.shape[1]
    # Adjust the max_length to accommodate the input length
    max_length = num_tokens + 50  # You can set the additional tokens as per your preference
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        num_return_sequences=5,  # Generate multiple responses
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
    )

    # Decode and filter the generated responses to remove duplicates
    decoded_responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    filtered_responses = []
    for response in decoded_responses:
        if response not in generated_responses:
            filtered_responses.append(response)
            generated_responses.add(response)

    return filtered_responses

if __name__ == "__main__":
    conversation_history = ""
    generated_responses = set()  # Set to keep track of generated responses
    print("Chatbot: Hi! I'm your anonymous chatbot. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Take care.")
            break

        # Generate responses and select one to output
        responses = generate_response(conversation_history, user_input, generated_responses)
        if responses:
            response = responses[0]
            conversation_history += "You: " + user_input + "\nChatbot: " + response + "\n"
            print("Chatbot:", response)
        else:
            print("Chatbot: I'm not sure what to say.")
