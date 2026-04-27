import reflex as rx


class Category(rx.Model):
    name: str


class State(rx.State):
    #1. The List: this starts with two example categories.

    categories: list[Category] = [
        Category(name = "MCAT Prep"),
        Category (name = "Research"),
    ]

    #2. The input: This stores what you are currently typing.
    new_category_name: str = ""

    #The pointer: this remembers which category is currently open
    #Initialize it with empyt Category so nothing is open at start.
    selected_category: Category = Category(name= "")

    def set_new_category_name(self, name: str):
        self.new_category_name = name

    def add_category(self):
        if self.new_category_name != "":
            #Adding a new Category object to our list
            self.categories.append(Category(name= self.new_category_name))

            #Clearing the 'sticky note' so the input box becomes empty again
            self.new_category_name = ""
    
    #The opener: this function sets "Pointer" to the card user clicked.
    def select_category(self, cat: Category):
        self.selected_category = cat

    #The closer: resets the pointer to go back to the main dashboard
    def clear_selection(self):
        self.selected_category = Category(name= "")

    

#Defining the body of the app (UI)

def index()-> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Student Command Center", size = "9"),

            #Using rx.cond to decide what to show
            rx.cond(
                State.selected_category.name != "",
                #If true: show the detail view
                rx.vstack(
                    rx.button("<-Back to Dashboard", on_click = State.clear_selection),
                    rx.heading(State.selected_category.name, size="7"),
                    rx.text("Links and notes for this aspect will go here"),
                    align= "start",
                    width = "100%",
                ),

                #If false: Show the main input and grid
                rx.vstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Add a new life aspect",
                            on_change= State.set_new_category_name,

                            #If key pressed is "Enter" run State.add_category else do nothing.
                            on_key_down= lambda key: rx.cond(
                                key == "Enter",
                                State.add_category,
                                None
                            ),
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

                                    rx.button(
                                        "Open", 
                                        size= "1",
                                        variant="outline",
                                        #when clicked , send this specific category(cat) to the Brain
                                        on_click= lambda: State.select_category(cat)
                                    
                                    ),


                                    padding= "3",
                                ),
                            )
                        ),
                        columns= "3",
                        spacing= "4",
                        width= "100%"
                    ),
                    width="100%",
                align = "center",
                spacing = "5",
                )
            ),
            align= "center",
            spacing= "5" ,
        )
    )

app = rx.App()
app.add_page(index)