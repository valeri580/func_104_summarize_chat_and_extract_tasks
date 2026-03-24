from func_104_summarize_chat_and_extract_tasks import func_104_summarize_chat_and_extract_tasks


print("=== TEST RUN ===")

result = func_104_summarize_chat_and_extract_tasks({
    "messages": [
        "Нужно сделать лендинг",
        "Я возьму задачу",
        "Срок до пятницы"
    ]
})

print(result)
