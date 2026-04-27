import reflex as rx


class Category(rx.Model):
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


#Defining the body of the app (UI)

def index()-> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Student Command Center", size = "9"),

            rx.hstack(
                rx.input(
                    placeholder="Add a new life aspect",
                    on_change= State.set_new_category_name,
                    value= State.new_category_name,
                ),
                rx.button("Add", on_click = State.add_category),

            ),
            rx.grid(
                rx.foreach(
                    State.categories,
                    lambda cat: rx.card(
                        rx.vstack(
                            rx.text(cat.name, weight= "bold", size= "5"),
                            rx.button("Open", size= "1", variant="outline"),
                            padding= "3",
                        ),
                    )
                ),
                columns= "3",
                spacing= "4",
                width= "100%"
            ),

            align= "center",
            spacing= "5" ,
        )
        

    )

app = rx.App()
app.add_page(index)

