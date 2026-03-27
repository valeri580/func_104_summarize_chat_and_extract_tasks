from func_104_summarize_chat_and_extract_tasks import func_104_summarize_chat_and_extract_tasks

print("=== TEST 1: Happy Path ===")

def mock_chat(**kwargs):
    return {
        "choices": [
            {"message": {"content": "Тестовое саммари"}}
        ],
        "usage": {"completion_tokens": 10}
    }

result = func_104_summarize_chat_and_extract_tasks({
    "messages": [
        "Иван (прораб): привезли цемент",
        "Петр (логистика): машина задерживается"
    ],
    "chat_type": "team",
    "period": "week",
    "model": "gpt-4o-mini",
    "domain": "construction",
    "debug": True,
    "ENV": {
        "SMAIPL_OPENROUTER_CHATGPT": mock_chat,
        "SMAIPL_KIE_COEF": 1.0
    }
})

print(result)

assert result.get("status") == "success"
print("=== TEST PASSED ===")
