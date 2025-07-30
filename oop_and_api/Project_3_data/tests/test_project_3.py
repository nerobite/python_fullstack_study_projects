import pytest
import json
from oop_and_api.Project_3 import read_json, read_xml


def parametrizer(func):
    return pytest.mark.parametrize(
        "descriptions, expected_words_min_len, top_n, expected_min_len, expected_count",
        [
            (
                [
                    "Туристы путешествуют по странам и континентам.",
                    "Возможностей для туризма много, туристов привлекают пейзажи."
                ],
                6,
                5,
                6,
                5
            ),
            (
                ["Я он ты мы вы"],
                10,
                5,
                10,
                0
            ),
            (
                ["Путешествовать"],
                8,
                3,
                8,
                1
            ),
            (
                [],
                6,
                5,
                6,
                0
            )
        ]
    )(func)

@parametrizer
def test_read_json_parametrized(descriptions, expected_words_min_len, top_n, expected_min_len, expected_count, tmp_path):
    data = {
        "rss": {
            "channel": {
                "items": [{"description": desc} for desc in descriptions]
            }
        }
    }
    test_file = tmp_path / "test.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    result = read_json(str(test_file), word_max_len=expected_words_min_len, top_words_amt=top_n)

    assert isinstance(result, list)
    assert len(result) == expected_count
    for word in result:
        assert len(word) > expected_min_len


@parametrizer
def test_read_xml_parametrized(descriptions, expected_words_min_len, top_n, expected_min_len, expected_count, tmp_path):
    xml_content = '''<?xml version="1.0" encoding="utf-8"?>
    <rss>
      <channel>
        {items}
      </channel>
    </rss>
    '''
    item_template = '<item><description>{}</description></item>'
    items_xml = ''.join(item_template.format(desc) for desc in descriptions)
    full_xml = xml_content.format(items=items_xml)

    test_file = tmp_path / "test.xml"
    test_file.write_text(full_xml, encoding='utf-8')

    result = read_xml(str(test_file), word_max_len=expected_words_min_len, top_words_amt=top_n)

    assert isinstance(result, list)
    assert len(result) == expected_count
    for word in result:
        assert len(word) > expected_min_len