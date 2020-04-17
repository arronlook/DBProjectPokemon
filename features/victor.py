from prompt_toolkit import prompt
def victor_feature1():
    while 1:
        option = prompt('Victor\'s feature>')
        if option == "exit":
            break
        print(option)
def victor_feature2():
    print("Victor feature 2")

__functions__ = {
    "victor_feature1": victor_feature1,
    "victor_feature2": victor_feature2
}