import unittest
from main import generate_config


class TestGenerateConfig(unittest.TestCase):
    def test_generate_config(self):
        input_data = {
            "comment": "Это пример комментария",
            "const-pi": 3.14,
            "settings": {
                "name": "example",
                "values": [1, 2, 3],
                "nested": {
                    "enabled": True,
                    "timeout": 30
                }
            }
        }

        expected_output = """{
    /* Это пример комментария */
    var pi = 3.14
    settings -> {
        name -> "example",
        values -> [1, 2, 3],
        nested -> {
            enabled -> true,
            timeout -> 30
        }
    }
}"""

        result = generate_config(input_data)
        self.assertEqual(result, expected_output, f"Expected:\n{expected_output}\nGot:\n{result}")


if __name__ == "__main__":
    unittest.main()
