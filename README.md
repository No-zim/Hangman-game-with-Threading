# Hangman-game-with-Threading
It uses TCP connection to establish a connection then proceeds with UDP. It can support multiple Clients at the same time

To play the game run the Server and several Clients and play separately with each one.

ServerTCP-UDP.py<br/>
      1. Server receives a command ‘-r’ to pick a word randomly or a custom string to be used<br/>
      throughout the program<br/>
      2. It creates a TCP socket and listens connections from clients<br/>
      3. Receives a ‘name’ from a user and sends back ‘Hello .{}’.format(name)<br/>
      4. Creates a UDP Socket with random port number(which it saves into a list to prevent collision)<br/> 
      and sends its port number to the client to start a game<br/>
      5. Reads from a words.txt and creates a list of words called ‘words’(One can modify it by<br/> 
      not doing this step if the custom string is provided)<br/>
      6. Receives a start or exit message in a loop from a client, from which a client can enter<br/>
      ‘exit’ to exit<br/>
      7. Sends instructions and starts the game<br/>
      8.If a custom string is not provided. It shuffles the ‘words’ list and chooses one word<br/>
      9. Creates a dashed version of that word and sends it and len(word)+1 as a count to the<br/>
      client<br/>
      10. In another loop it plays the game receiving back ‘guess <char>’ and checking against<br/>
      characters in the word. If the character in the list, it replaces all instances of that char in<br/>
      the dasher version and sends it back including (len(word)+1) - count[count is<br/>
      incremented previously].<br/>
      11. Client can exit guessing loop by entering ‘end’. If a client runs out of guesses he/she<br/>
      loses.<br/>
      12. Client can also guess an entire word by entering guess <string> and the game for<br/>
      guessing this word will finish if the guessed word is right or wrong<br/>
      13. If client sends an exit message, server closes the ports and waits for the new<br/>
      connections<br/>
      <br/>
ClientTCP-UDP.py<br/>
      1. Receives name of the server host and its port number<br/>
      2. Creates a TCP socket and connects<br/>
      3. Sends a name to Server and receives back hello+name<br/>
      4. Receives UDP port number from server<br/>
      5. Creates its own UDP port number and interacts with the server<br/>
      6. It has two loops to interact with the server first loop to start or exit(in which it receives<br/>
      instructions) and the second loop for playing the game by guessing letters of a word that<br/>
      is provided.<br/>
      7. In the game you can enter guess<sp><char> -> to guess a letter, guess<sp><string> -> <br/>
      to guess an entire word, end -> to end this game<br/>
