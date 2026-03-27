def func_104_summarize_chat_and_extract_tasks(arguments):
    debug = arguments.get("debug", False)

    if debug:
        print(f"DEBUG: Start function {__name__}")
        print(f"DEBUG: Args: {arguments}")

    try:
        from openai import OpenAI

        # ========================
        # CONFIG / CONSTANTS
        # ========================
        MAX_MESSAGES = 500
        MIN_MESSAGE_LENGTH = 10
        CHUNK_SIZE = 120

        ALLOWED_MODELS = [
            "gpt-4o-mini",
            "qwen/qwen2.5-72b-instruct",
            "anthropic/claude-3-haiku"
        ]

        # ========================
        # HELPERS
        # ========================

        def validate_input(messages):
            if not isinstance(messages, list) or not messages:
                return False
            return True

        def clean_messages(messages):
            result = []
            for msg in messages:
                if isinstance(msg, str):
                    text = msg.strip()
                    if text and len(text) > MIN_MESSAGE_LENGTH:
                        result.append(text)
            return result

        def limit_messages(messages):
            return messages[-MAX_MESSAGES:]

        def chunk_messages(messages):
            return [
                messages[i:i + CHUNK_SIZE]
                for i in range(0, len(messages), CHUNK_SIZE)
            ]

        def normalize_model(model):
            if model not in ALLOWED_MODELS:
                return "gpt-4o-mini"
            return model

        def build_system_prompt(chat_type):
            if chat_type == "client":
                return (
                    "Ты проджект-менеджер, который формирует отчёт для клиента. "
                    "Пиши уверенно, позитивно, демонстрируя контроль."
                )
            return (
                "Ты опытный операционный менеджер и аналитик. "
                "Ты превращаешь переписку в управленческую аналитику."
            )

        def build_chunk_prompt(context):
            return f"""
Проанализируй переписку и сделай ПОЛНОЦЕННОЕ саммари.

Важно:
- не теряй детали
- фиксируй роли участников

Структура:
1. Участники и роли
2. События
3. Проблемы
4. Задачи и поручения
5. Риски

Переписка:
{context}
"""

        def build_final_prompt(combined_context, domain, period, chat_type):
            return f"""
Собери итоговое управленческое саммари.

Контекст:
Рабочие процессы в сфере: {domain}

Структура:
1. Общий статус
2. Участники и роли
3. Ключевые события
4. Проблемы
5. Риски
6. Задачи и поручения
7. Что требует внимания менеджера

Требования:
- не теряй информацию
- объединяй без дублирования
- не выдумывай

Если chat_type = client:
- смягчи негатив
- покажи контроль

Период: {period}

Данные:
{combined_context}
"""

        def call_llm(client, model, system_prompt, user_prompt, max_tokens, temperature):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            text = response.choices[0].message.content.strip()

            tokens = 0
            if hasattr(response, "usage"):
                tokens = response.usage.completion_tokens

            return text, tokens

        # ========================
        # INPUT
        # ========================
        messages = arguments.get("messages", [])
        chat_type = arguments.get("chat_type", "team")
        period = arguments.get("period", "week")
        model = normalize_model(arguments.get("model", "gpt-4o-mini"))
        domain = arguments.get("domain", "project")

        # ========================
        # VALIDATION
        # ========================
        if not validate_input(messages):
            return {
                "result": {
                    "error": "Некорректный messages",
                    "details": "Ожидается непустой список строк"
                },
                "status": "error"
            }

        # ========================
        # PREPROCESSING
        # ========================
        messages = clean_messages(messages)
        messages = limit_messages(messages)

        if not messages:
            return {
                "result": {
                    "error": "Нет сообщений после фильтрации",
                    "details": "Все сообщения слишком короткие или пустые"
                },
                "status": "error"
            }

        chunks = chunk_messages(messages)

        # ========================
        # LLM INIT
        # ========================
        client = OpenAI(
            api_key=arguments['ENV']['SMAIPL_OPENAI_API_KEY']
        )

        system_prompt = build_system_prompt(chat_type)

        # ========================
        # STEP 1: CHUNK SUMMARIES
        # ========================
        partial_summaries = []
        total_completion_tokens = 0

        for chunk in chunks:
            context = "\n".join(chunk)
            prompt = build_chunk_prompt(context)

            text, tokens = call_llm(
                client,
                model,
                system_prompt,
                prompt,
                max_tokens=600,
                temperature=0.3
            )

            partial_summaries.append(text)
            total_completion_tokens += tokens

        # ========================
        # STEP 2: MERGE SUMMARIES
        # ========================
        combined_context = "\n\n---\n\n".join(partial_summaries)

        final_prompt = build_final_prompt(
            combined_context,
            domain,
            period,
            chat_type
        )

        final_text, tokens = call_llm(
            client,
            model,
            system_prompt,
            final_prompt,
            max_tokens=900,
            temperature=0.4
        )

        total_completion_tokens += tokens

        # ========================
        # USAGE
        # ========================
        BILLING_MULTIPLIER = arguments['ENV'].get('SMAIPL_KIE_COEF', 1.0)
        total_tokens = float(total_completion_tokens * BILLING_MULTIPLIER)

        return {
            "result": {
                "data": final_text,
                "success": True
            },
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": total_completion_tokens,
                "total_tokens": total_tokens
            },
            "status": "success"
        }

    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()

        return {
            "result": {
                "error": "Ошибка выполнения функции",
                "details": str(e)
            },
            "status": "error"
        }
