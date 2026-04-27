import reflex as rx


class Category(rx.Base):
    name: str


class State(rx.State):
    #1. The List: this starts with two example categories.

    categories: list[Category] = [
        Category(name = "DSA Prep"),
        Category (name = "Research"),
    ]

    #2. The input: This stores what you are currently typing.
    new_category_name: str = ""

    def add_category(self):
        if self.new_category_name != "":
            #Adding a new Category object to our list

            self.categories.append(Category(name= self.new_category_name))

            #Clearing the 'sticky note' so the input box becomes empty again

            self.new_category_name = ""