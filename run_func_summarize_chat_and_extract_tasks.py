from func_summarize_chat_and_extract_tasks import func_summarize_chat_and_extract_tasks

print("=== TEST 1: Happy Path ===")

def mock_chat(**kwargs):
    return {
        "choices": [
            {"message": {"content": "Тестовое саммари"}}
        ],
        "usage": {"cost": 0.001}
    }

result = func_summarize_chat_and_extract_tasks({
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
        "SMAIPL_OPENROUTER_CHATGPT": mock_chat
    }
})

print(result)

assert result.get("status") == "success"
assert "result" in result
assert "usage" in result
assert isinstance(result["usage"]["total_tokens"], float)

print("=== TEST PASSED ===")
