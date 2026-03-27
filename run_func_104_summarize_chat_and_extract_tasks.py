from func_104_summarize_chat_and_extract_tasks import func_104_summarize_chat_and_extract_tasks

print("=== TEST 1: Happy Path ===")

result = func_104_summarize_chat_and_extract_tasks({
    "messages": [
        "Иван (прораб): привезли цемент",
        "Петр (логистика): машина задерживается",
        "Анна (менеджер): нужно ускорить поставку"
    ],
    "chat_type": "team",
    "period": "week",
    "model": "gpt-4o-mini",
    "domain": "construction",
    "debug": True,
    "ENV": {
        "SMAIPL_OPENAI_API_KEY": "test_key",
        "SMAIPL_KIE_COEF": 1.0
    }
})

print(result)

assert result.get("status") == "success"
assert "result" in result

print("=== TEST PASSED ===")
