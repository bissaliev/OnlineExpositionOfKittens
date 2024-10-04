def check_paginator(data, url, count=1):
    assert "count" in data, (
        f"Проверьте, что при GET запросе `{url}` возвращаете данные "
        "с пагинацией. Не найден параметр `count`"
    )
    assert "next" in data, (
        f"Проверьте, что при GET запросе `{url}` возвращаете данные "
        "с пагинацией. Не найден параметр `next`"
    )
    assert "previous" in data, (
        f"Проверьте, что при GET запросе `{url}` возвращаете данные "
        "с пагинацией. Не найден параметр `previous`"
    )
    assert "results" in data, (
        f"Проверьте, что при GET запросе `{url}` возвращаете данные "
        "с пагинацией. Не найден параметр `results`"
    )
    assert data["count"] == count, (
        f"Проверьте, что при GET запросе `{url}` возвращаете данные "
        "с пагинацией. Значение параметра `count` не правильное"
    )
