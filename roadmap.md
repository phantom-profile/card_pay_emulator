# Roadmap for funny_farm project

## v 0.1.0

1) Animal with gender, age and name. Can be displayed.
2) create and remove animals from farm
3) display list of animals (CLI only)
4) save results of game session in database (Shelve module)

## Class diagram for LATEST version
```mermaid
classDiagram
    direction LR
    %% CLASS DEFINITIONS --------------------------------
        %% manages behaviour of animal object
        class Animal
        %% manages animals and actions with them
        class Farm
        %% manages data passing between logic and interface components
        class GameSession
        %% manages behaviour of data displaying in interface
        class UserInterface
        %% manages data passing between logic and data storage components
        class DatabaseManager
        
    %% CLASS ANNOTATIONS --------------------------------
    <<interface>> UserInterface
    <<interface>> DatabaseManager
    
    %% CLASS RELATIONS ----------------------------------
    Farm --> "many" Animal : Contains
    GameSession --> "one" Farm : Contains
    GameSession --> "one" UserInterface : Contains
    GameSession --> "one" DatabaseManager : Contains
    CLIUserInterface ..|> UserInterface: Realization
    ShelveDatabaseManager ..|> DatabaseManager: Realization
    
    class Animal {
        +positive int age
        +String name
        +boolean gender
        +gender_represent() String
        +__str__() String
    }

    class Farm {
        -List~Animal~ animals
        +add_animal(Animal animal) List~Animal~
        +remove_animal(Animal animal) List~Animal~
        +__str__() String
    }
    
    class GameSession {
        -UserInterface interface
        -String user
        -Farm farm
        -DatabaseManager database_manager
        +__init__(DatabaseManager database_manager, UserInterface interface)
        +game_perform()
        -save_data()
    }
    
    class UserInterface {
        +get_message(Dict~String, String~ serialized_message) Dict~String, Any~
        +send_message(Dict~String, Any~ serialized_message)
        +fill_form(Dict~String, None~ empty_form)
        +display_list(List~Dict(String, Any)~objects)
    }
    
    class DatabaseManager {
        +Any database
        +__init__(Any database)
        +get_table_data(String table_name)
        +save_table_data(String table_name, Any data)
        +close_session()
    }
    
    class ShelveDatabaseManager { 
        +Any database
        +__init__(Shelve database)
        +get_table_data(String table_name)
        +save_table_data(String table_name, Any data)
        +close_session()
    }
    
    class CLIUserInterface {    
        +get_message(Dict~String, String~) Dict~String, Any~
        +send_message(Dict~String, Any~)
        +fill_form(Dict~String, None~ empty_form)
        +display_list(List~Dict(String, Any)~objects)
    }
```