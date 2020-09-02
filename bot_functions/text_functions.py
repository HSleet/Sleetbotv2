from random import randint


def mock_text(text):
    mocking_text = ''
    if len(text) > 4:
        for character in text:
            if randint(0, 12) > 5:
                new_char = character.swapcase()
            else:
                new_char = character
            mocking_text = mocking_text + new_char
    return mocking_text


def reverse(text_to_reverse):
    reverse_text = text_to_reverse[::-1]
    return reverse_text


if __name__ == '__main__':
    print(reverse(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at est ut massa efficitur cursus. Proin nec "
        "turpis ac diam aliquam rhoncus. Sed ultrices libero augue, nec efficitur eros varius eu. Etiam nec "
        "sollicitudin ex, eget efficitur nulla. Cras metus nisl, facilisis vitae sagittis in, fermentum sit amet "
        "nisi. Nulla facilisi. Proin dictum molestie rhoncus. Aliquam tincidunt lectus sed maximus laoreet. Integer"
        " in mi accumsan, pulvinar leo id, eleifend leo. Donec porttitor purus facilisis magna bibendum, non tempus"
        " mauris lobortis. Sed aliquam nulla sit amet nulla vehicula, non imperdiet arcu tincidunt. Curabitur "
        "a aliquet velit. Maecenas a euismod purus. Maecenas dictum sapien maximus, semper ligula ut, vestibulum "
        "turpis. Aenean ut odio et justo auctor tincidunt vitae id dolor."))
    print(mock_text(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at est ut massa efficitur cursus. Proin nec "
        "turpis ac diam aliquam rhoncus. Sed ultrices libero augue, nec efficitur eros varius eu. Etiam nec "
        "sollicitudin ex, eget efficitur nulla. Cras metus nisl, facilisis vitae sagittis in, fermentum sit amet "
        "nisi. Nulla facilisi. Proin dictum molestie rhoncus. Aliquam tincidunt lectus sed maximus laoreet. Integer"
        " in mi accumsan, pulvinar leo id, eleifend leo. Donec porttitor purus facilisis magna bibendum, non tempus"
        " mauris lobortis. Sed aliquam nulla sit amet nulla vehicula, non imperdiet arcu tincidunt. Curabitur "
        "a aliquet velit. Maecenas a euismod purus. Maecenas dictum sapien maximus, semper ligula ut, vestibulum "
        "turpis. Aenean ut odio et justo auctor tincidunt vitae id dolor."))
