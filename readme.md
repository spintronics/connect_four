Requirements
- python 3.9
- pygame
- the path names are for windows (not normalized)

git clone https://github.com/spintronics/connect_four

python connect_four.py

todo:
- move more stuff to logic so that it can be shared between the client and server
- get a request handler for the client and make the state support async actions


- make a presentation that includes the libraries used and design approach

Presentation:

# bottom up design approach

- split up game logic, ui, state, and ai
- test these units independently
- merge them together and do integration testing

# major game functionality

- single source of truth state management
- action based mutation of state
- ui is redrawn only when the state changes
- ui is built up using nested components including (image, circle, rectangle) and layout components such as (expanded, row, column)
- event wrapper for components to imbue them with the ability to trigger actions on hove, click, etc
- logic such as checking for a win, dropping a piece, and ensuring a move is valid is seperate from ui and tested independently
- ai looks ahead to first prevent possible wins for opponent then to make the move that gives it the most possible wins (recursively)
- one of the tests tha the ai my pass is to win 100 out 100 games vs another ai that makes random moves
- one of the features implemented to make ui testing easier was to write each action to a log file. If some error occurs during the program execution, we can replay the actions to get the program into the state in which it broke so we can debug.

# typical game loop

- initialize state and register action handlers
- build the component tree with the appropriately bounded event handlers
- an event such as a button click fires the bound action
- the action changes the state it a predictable way (immutably)
- if the state detects that the state is different after the action has run, a redraw is scheduled
- the game loop consumes events every 20ms

# libraries used

- pygame, flask, requests
- all of the infastructure to enable remote play was implemented but not finalized due to insufficient testing
