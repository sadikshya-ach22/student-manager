import reflex as rx

class Resource(rx.Model):
    title:str
    url: str
    note: str =""

class Category(rx.Model):
    name: str
    items: list[Resource] = []   #Category owns a list of resources

#-------------------------------------------------------------------------------------------------
#Defining the Brain of the project
#-------------------------------------------------------------------------------------------------

class State(rx.State):
    categories: list[Category] = [] #1. The List to add categories.
    new_category_name: str = ""  #2. The input:stores currently typed category name
    new_resource_title: str = ""
    new_resource_url: str = ""

    #Pointer to remember which category is currently open
    selected_category_name: str = ""

    #Logic for Categories
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
        self.selected_category_name = cat.name

    #The closer: resets the pointer to go back to the main dashboard
    def clear_selection(self):
        self.selected_category_name = ""       #reset the pointer to an empty string
    
    #COMPUTED PROPERTY
    @rx.var
    def current_items(self) -> list[Resource]:
        #Provides a clean, guaranteed list of resources for UI to loop over
        for cat in self.categories:
            if cat.name == self.selected_category_name:
                return cat.items
        return [] #returning empty list if nothing matches

    #Logic for Resources
    def add_resource(self):
        new_res = Resource(                 #creating object using our new Resource blueprint
            title = self.new_resource_title,
            url= self.new_resource_url
        )

        for cat in self.categories:          #pushing the resource into the selected category
            if cat.name == self.selected_category_name:
                cat.items.append(new_res)
                break

        self.new_resource_title = ""          #Cleaning up the input boxes
        self.new_resource_url = ""
        self.categories = self.categories

    #Deleting the resource
    def delete_resource(self, resource_to_delete: Resource):
        for cat in self.categories:
            if cat.name == self.selected_category_name:
                cat.items.remove(resource_to_delete)
                break
        self.categories = self.categories

    def set_new_resource_title(self, title: str):
        self.new_resource_title = title

    def set_new_resource_url(self, url: str):
        self.new_resource_url = url

    
#-------------------------------------------------------------------------------------------------
# Defining the body of the app (UI)
#-------------------------------------------------------------------------------------------------

def index()-> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Student Command Center", size = "9"),

            #Using rx.cond to decide what to show
            rx.cond(
                State.selected_category_name != "",
                #If true: show the detail view
                rx.vstack(
                    rx.button("<-Back to Dashboard", on_click = State.clear_selection),
                    rx.heading(State.selected_category_name, size="7"),
                    #THE RESOURCE FORM
                    rx.vstack(
                        rx.input(
                            placeholder="Resource Title (eg: Youtube Array Video)",
                            on_change = State.set_new_resource_title,
                            value= State.new_resource_title,
                            width = "100%"
                        ),
                        rx.input(
                            placeholder= "URL (https: //...)",
                            on_change = State.set_new_resource_url,
                            value = State.new_resource_url,
                            width = "100%"
                        ),
                        rx.button("Save Resource", on_click= State.add_resource, width= "100%"),

                        background_color= rx.color("gray", 3),
                        padding= "4",
                        border_radius= "lg",
                        width = "400px",
                    ),
                    

                   #THE RESOURCE LIST VIEW
                    rx.vstack(
                        rx.heading("Saved Resources", size = "4"),
                        rx.foreach(
                            State.current_items,
                            lambda res:rx.hstack(
                                rx.text(res.title, weight = "medium"),

                                rx.hstack(
                                    rx.link(
                                    "Open Link->",
                                    href= res.url,
                                    is_external = True,
                                    color_scheme = 'blue'
                                    ),
                                    rx.button(
                                        "X",
                                        color_scheme= "red",
                                        size= "1",
                                        variant = "soft",
                                        on_click= lambda: State.delete_resource(res)
                                    ),
                                    spacing= "3"
                                ),
                                width = '100%',
                                justify = "between",
                                padding = "2",
                                background_color = rx.color("gray",2),
                                border_radius = "md",
                            )
                        ),
                        width = "400px",
                        align= "stretch",
                        spacing = "2",
                    ),
                    align= "start",
                    width="100%",
                    spacing="6",
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