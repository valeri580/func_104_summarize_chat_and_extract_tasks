from func_104_summarize_chat_messages import func_104_summarize_chat_messages


print("=== TEST RUN ===")

result = func_104_summarize_chat_messages({
    "messages": [
        "Нужно сделать лендинг",
        "Я возьму задачу",
        "Срок до пятницы"
    ]
})

print(result)
