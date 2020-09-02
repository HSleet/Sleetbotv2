import requests
import json
import re


class UrbanDefinition:

    def __init__(self, response_json):
        self.raw_dict = response_json
        self.permalink = response_json["permalink"]
        self.author = response_json["author"]
        self.word = response_json["word"]
        self.definition = response_json["definition"].replace('[', '').replace(']', '')
        self.example = response_json["example"].replace('[', '').replace(']', '')

    def get_sub_definitions(self) -> list:
        pattern = r"(?<=\[).+?(?=\])"
        sub_definitions_phrases = re.findall(pattern, self.raw_dict["definition"])
        definition_links = [
            {"term": term, "link": f"https://www.urbandictionary.com/define.php?term={term}"}
            for term in sub_definitions_phrases
        ]
        sub_definitions_example = re.findall(pattern, self.raw_dict["example"])
        for definition in sub_definitions_example:
            definition_links.append({"term": definition,
                                     "link": f"https://www.urbandictionary.com/define.php?term={definition}"})
        return definition_links

    def get_markdown_text(self) -> (str, str):
        pattern = r"(?<=\[).+?(?=\])"
        text_to_change = self.definition
        text_to_change2 = f"_{self.example}_"
        sub_definitions_phrases = re.findall(pattern, self.raw_dict["definition"])
        sub_definitions_example = re.findall(pattern, self.raw_dict["example"])
        for phrase in sub_definitions_phrases:
            markdown_phrase = f"[{phrase}](https://www.urbandictionary.com/define.php?term={phrase.replace(' ', '+')})"
            text_to_change = text_to_change.replace(phrase, markdown_phrase)
        for phrase in sub_definitions_example:
            markdown_phrase = f"_[{phrase}](https://www.urbandictionary.com/define.php?term={phrase.replace(' ', '+')})_"
            text_to_change2 = text_to_change2.replace(phrase, markdown_phrase)
        return text_to_change, text_to_change2

    def __len__(self):
        return len(self.definition)

    def __str__(self):
        return self.definition + '\n\nExample: \n\n' + self.example + "\n\nAuthor: " + self.author


def get_response(phrase: str):
    term = phrase.replace(' ', '+')
    response = requests.get(f"http://api.urbandictionary.com/v0/define?term={term}")
    response_json = json.loads(response.text)
    definition_list = response_json["list"]
    definition = definition_list[0]
    return definition


def get_definition(phrase: str) -> UrbanDefinition:
    definition_json = get_response(phrase)
    urban_definition = UrbanDefinition(definition_json)
    return urban_definition


if __name__ == '__main__':
    print(get_definition("henrying"))

