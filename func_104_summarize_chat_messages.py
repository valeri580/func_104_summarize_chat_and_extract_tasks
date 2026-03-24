def func_104_summarize_chat_messages(arguments):
    debug = arguments.get("debug", False)

    if debug:
        print(f"DEBUG: Args: {arguments}")

    try:
        messages = arguments.get("messages", [])

        if not messages:
            return {
                "result": {
                    "error": "Список сообщений пуст"
                },
                "status": "error"
            }

        # Простая заглушка (пока без LLM)
        combined_text = "\n".join(messages[:50])

        result_text = f"Получено сообщений: {len(messages)}\n\nПример:\n{combined_text[:500]}"

        return {
            "result": {
                "data": result_text,
                "success": True
            },
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0.0
            },
            "status": "success"
        }

    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()

        return {
            "result": {
                "error": str(e)
            },
            "status": "error"
        }
