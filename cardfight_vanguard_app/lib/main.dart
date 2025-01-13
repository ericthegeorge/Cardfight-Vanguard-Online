import 'package:flutter/material.dart';
import 'api_service.dart';
// import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Card Pack Opener',
      theme: ThemeData(
          // This is the theme of your application.
          //
          // TRY THIS: Try running your application with "flutter run". You'll see
          // the application has a purple toolbar. Then, without quitting the app,
          // try changing the seedColor in the colorScheme below to Colors.green
          // and then invoke "hot reload" (save your changes or press the "hot
          // reload" button in a Flutter-supported IDE, or press "r" if you used
          // the command line to start the app).
          //
          // Notice that the counter didn't reset back to zero; the application
          // state is not lost during the reload. To reset the state, use hot
          // restart instead.
          //
          // This works for code too, not just values: Most code changes can be
          // tested with just a hot reload.
          primarySwatch: Colors.blue),
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/open-pack': (context) => PackOpenerScreen(),
        '/home': (context) => HomeScreen(),
        '/user-cards': (context) => CollectionScreen(),
        '/decks': (context) => DeckListCreateScreen(),
        // '/decks/'
      },
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class PasswordField extends StatefulWidget {
  final TextEditingController controller;

  const PasswordField({super.key, required this.controller});

  @override
  _PasswordFieldState createState() => _PasswordFieldState();
}

class _PasswordFieldState extends State<PasswordField> {
  bool _isVisible = false;

  @override
  Widget build(BuildContext context) {
    return TextField(
        controller: widget.controller,
        obscureText: !_isVisible,
        enableSuggestions: false,
        autocorrect: false,
        decoration: InputDecoration(
            labelText: 'Password',
            border: OutlineInputBorder(),
            suffixIcon: IconButton(
              icon: Icon(
                _isVisible ? Icons.visibility : Icons.visibility_off,
              ),
              onPressed: () {
                setState(() {
                  _isVisible = !_isVisible;
                });
              },
            )));
  }
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  String? _errorMessage;
  String? _successMessage;

  final ApiService _apiService = ApiService();

  Future<void> _login() async {
    final username = _usernameController.text.trim();
    final password = _passwordController.text.trim();
    if (username.isEmpty || password.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a username and password';
      });
      return;
    }

    // final url = Uri.parse('/user/$username/login/');
    try {
      final response = await _apiService.login(username, password);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          Navigator.pushNamed(
            context,
            '/home',
            arguments: username,
          );
          setState(() {
            _errorMessage = null;
          });
        } else {
          setState(() {
            _errorMessage = 'Invalid username or password';
          });
        }
      } else {
        setState(() {
          _errorMessage = 'Login failed';
          // : ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'An error occured: $e';
      });
    }
  }

  Future<void> _register() async {
    final username = _usernameController.text.trim();
    final password = _passwordController.text.trim();
    if (username.isEmpty || password.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a username and password';
      });
      return;
    }

    // final url = Uri.parse('/user/$username/login/');
    try {
      final response = await _apiService.register(username, password);
      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          // Navigator.pushNamed(
          // context,
          // '/open-pack',
          // arguments: username,
          // );
          _successMessage = "Successfully registered!";
          setState(() {
            _errorMessage = null;
          });
          // Future.delayed(const Duration(seconds: 2), () {
          //   Navigator.pushReplacementNamed(context, '/login');
          // });
        } else {
          setState(() {
            _errorMessage = data['error'];
          });
        }
      } else {
        setState(() {
          _errorMessage = 'Register failed';
          // : ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'An error occured: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _usernameController,
              decoration: InputDecoration(
                labelText: 'Username',
                // errorText: _errorMessage,
                border: OutlineInputBorder(),
              ),
              autocorrect: false,
            ),
            const SizedBox(height: 20),
            PasswordField(controller: _passwordController),
            const SizedBox(height: 20),
            if (_errorMessage != null)
              Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red),
              ),
            if (_successMessage != null)
              Text(
                _successMessage!,
                style: const TextStyle(color: Colors.green),
              ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _login,
              child: Text('Login'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _register,
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late String username;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)?.settings.arguments;
    if (args is String) {
      username = args;
    } else {
      username = 'Guest'; // Fallback if no username is passed
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Welcome, $username!'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/open-pack', arguments: username);
              },
              child: const Text('Open Packs'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // print("Username passed to /user-cards: $username"); //DEBUG
                Navigator.pushNamed(context, '/user-cards',
                    arguments: username);
              },
              child: const Text('Collection'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                //   Navigator.pushNamed(context, '/user-cards',
                //       arguments: username);
              }, //TODO Battle
              child: const Text('Battle'),
            ),
          ],
        ),
      ),
    );
  }
}

class CollectionScreen extends StatefulWidget {
  const CollectionScreen({super.key});

  @override
  _CollectionScreenState createState() => _CollectionScreenState();
}

class _CollectionScreenState extends State<CollectionScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<UserCard>> cards;
  late String username;
  final ValueNotifier<String> selectedSortOption =
      ValueNotifier<String>('Name');
  final ValueNotifier<List<UserCard>> sortedCardsNotifier = ValueNotifier([]);
  // List<UserCard> sorted_cards = [];

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)?.settings.arguments;
    if (args is String) {
      username = args;
      // print("Arguments received: $username");
    } else {
      username = 'Guest'; //never
    }
    cards = fetchUserCards();
  }

  Future<List<UserCard>> fetchUserCards() async {
    try {
      final data = await _apiService.userCards(username);
      return data.map((json) => UserCard.fromJson(json)).toList();
    } catch (e) {
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Collection of $username'),
        actions: [
          ValueListenableBuilder<String>(
            valueListenable: selectedSortOption,
            builder: (context, value, child) {
              return DropdownButton<String>(
                value: value,
                items: <String>['Name', 'Rarity', 'Booster Pack']
                    .map((String value) => DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        ))
                    .toList(),
                onChanged: (String? newValue) {
                  if (newValue != null) {
                    // Update the selected sort option, but avoid rebuilding the entire screen
                    selectedSortOption.value = newValue;
                    sortUserCards(
                        newValue); // Sort the cards without triggering a full rebuild
                  }
                },
                underline: Container(), // Removes default underline
                icon: Icon(Icons.sort, color: Colors.white), // Sort icon
                dropdownColor: Colors.white, // Background color for dropdown
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.style),
            tooltip: 'Decks',
            onPressed: () {
              Navigator.pushNamed(context, '/decks', arguments: username);
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          // Refresh the cards, but don't reset the sort option
          final newCards = await fetchUserCards();
          sortedCardsNotifier.value =
              List.from(newCards); // Set the fetched data
          sortUserCards(
              selectedSortOption.value); // Reapply the sort after refresh
        },
        child: FutureBuilder<List<UserCard>>(
          future: cards,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return const Center(
                  child: Text('No cards found in your collection.'));
            } else {
              // Initialize sortedCardsNotifier only if it's empty
              if (sortedCardsNotifier.value.isEmpty) {
                sortedCardsNotifier.value = List.from(snapshot.data!);
                sortUserCards(selectedSortOption.value); // Apply default sort
              }
              return ValueListenableBuilder<List<UserCard>>(
                valueListenable: sortedCardsNotifier,
                builder: (context, sorted_cards, child) {
                  return GridView.builder(
                    padding: const EdgeInsets.all(4.0),
                    gridDelegate:
                        const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 4,
                      mainAxisSpacing: 8.0,
                      crossAxisSpacing: 8.0,
                      childAspectRatio: 2 / 3,
                    ),
                    itemCount: sorted_cards.length,
                    itemBuilder: (context, index) {
                      final card = sorted_cards[index];
                      return Card(
                        margin: const EdgeInsets.all(8.0),
                        elevation: 4.0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Stack(
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(8.0),
                              child: Image.network(
                                card.image,
                                width: double.infinity,
                                height: double.infinity,
                                fit: BoxFit.cover,
                              ),
                            ),
                            Positioned(
                              bottom: 0.0,
                              left: 0.0,
                              right: 0.0,
                              child: Align(
                                alignment: Alignment.bottomCenter,
                                child: Container(
                                  padding: EdgeInsets.all(4.0),
                                  color: Colors.black54,
                                  child: Text(
                                    'x${card.count}',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 12,
                                      fontWeight: FontWeight.bold,
                                      fontFamily: 'Verdana',
                                      fontStyle: FontStyle.italic,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      );
                    },
                  );
                },
              );
            }
          },
        ),
      ),
    );
  }

  void sortUserCards(String criterion) {
    final currentList = List<UserCard>.from(sortedCardsNotifier.value);
    currentList.sort((a, b) {
      if (criterion == 'Name') {
        return a.name.compareTo(b.name);
      } else if (criterion == 'Rarity') {
        return a.rarity.compareTo(b.rarity);
      } else {
        return 0; // No sort for unknown criteria
      }
    });
    sortedCardsNotifier.value = currentList; // Update sorted list
  }

  @override
  void dispose() {
    sortedCardsNotifier.dispose();
    super.dispose();
  }
// Sorting function
}

class UserCard {
  final String name;
  final String image;
  final String rarity;
  final int count;

  UserCard(
      {required this.name,
      required this.image,
      required this.rarity,
      required this.count});

  factory UserCard.fromJson(Map<String, dynamic> json) {
    return UserCard(
      name: json['card_name'],
      image: json['image'],
      rarity: json['rarity'],
      count: json['count'],
    );
  }
}

// class UserDeck {
//   final String name;
//   // final String
// }

class DeckListCreateScreen extends StatefulWidget {
  const DeckListCreateScreen({super.key});

  @override
  _DeckListCreateScreenState createState() => _DeckListCreateScreenState();
}

class _DeckListCreateScreenState extends State<DeckListCreateScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<dynamic>> decks;
  late String username;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)?.settings.arguments;
    if (args is String) {
      username = args;
    } else {
      username = 'Guest'; //never
    }
    //anything else to be done on change
    setState(() {
      decks = _apiService.fetchUserDecks(username);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Decks of $username'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            tooltip: 'Create Deck',
            onPressed: () {
              // Navigate to Create Deck Screen
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          setState(() {
            decks =
                _apiService.fetchUserDecks(username); // Reload decks on refresh
          });
        },
        child: FutureBuilder<List<dynamic>>(
          future: decks,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return const Center(child: Text('No decks found. Create one!'));
            } else {
              final decks = snapshot.data!;
              return GridView.builder(
                padding: const EdgeInsets.all(4.0),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount:
                      3, // Adjust the number of columns to fit decks
                  mainAxisSpacing: 8.0,
                  crossAxisSpacing: 8.0,
                  childAspectRatio: 432 / 664, // Aspect ratio for deck cards
                ),
                itemCount: decks.length + 1, // +1 for the blank deck
                itemBuilder: (context, index) {
                  if (index == 0) {
                    // Blank deck with the plus icon
                    return MouseRegion(
                      cursor: SystemMouseCursors.click,
                      child: GestureDetector(
                        onTap: () {
                          // Navigate to the Create Deck Screen
                          Navigator.pushNamed(context, '/home',
                              arguments: username);
                        },
                        child: Card(
                          margin: const EdgeInsets.all(8.0),
                          // elevation: 4.0,
                          // color: Color.fromRGBO(30, 30, 30, 70),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Column(
                            children: [
                              // Blank deck with a plus icon
                              ClipRRect(
                                borderRadius: const BorderRadius.vertical(
                                  top: Radius.circular(8.0),
                                ),
                                child: Container(
                                  // height: double.infinity,
                                  // 200.0, // Fixed height for the plus icon
                                  height: 580,
                                  width: double.infinity,
                                  color:
                                      Colors.grey[300], // Light gray background
                                  child: Icon(
                                    Icons.add,
                                    size: 50,
                                    color: Colors.white,
                                  ),
                                ),
                              ),
                              // "Create New Deck" Text
                              Container(
                                width: double.infinity,
                                padding: const EdgeInsets.all(11.0),
                                decoration: const BoxDecoration(
                                  color: Color.fromRGBO(186, 213, 222,
                                      122), // Background color for the text box
                                  borderRadius: BorderRadius.vertical(
                                    bottom: Radius.circular(8.0),
                                  ),
                                ),
                                child: const Text(
                                  'Create New Deck', // Text indicating it's a blank deck
                                  style: TextStyle(
                                    color: Colors.black,
                                    fontSize: 12,
                                    fontWeight: FontWeight.normal,
                                    fontFamily: 'Verdana',
                                    fontStyle: FontStyle.italic,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  } else {
                    // Actual deck card
                    final deck =
                        decks[index - 1]; // Offset by 1 since index starts at 1
                    return Card(
                      margin: const EdgeInsets.all(8.0),
                      // elevation: 4.0,
                      // color: Color.fromRGBO(30, 30, 30, 70),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Column(
                        children: [
                          // Deck Image (takes up natural height)
                          ClipRRect(
                            borderRadius: const BorderRadius.vertical(
                              top: Radius.circular(8.0),
                            ),
                            child: Image.network(
                              deck['highlight_card_image'], // Deck image URL
                              width: double.infinity,
                              fit: BoxFit.cover,
                              errorBuilder: (context, error, stackTrace) {
                                return Container(
                                  color: Colors.grey[300],
                                  child: const Icon(Icons.image_not_supported,
                                      size: 50),
                                );
                              },
                            ),
                          ),
                          // Deck Name Box (below the image, outside the image)
                          Container(
                            width: double.infinity,
                            padding: const EdgeInsets.all(11),
                            decoration: const BoxDecoration(
                              color: Color.fromRGBO(186, 213, 222,
                                  122), // Background color for the text box
                              borderRadius: BorderRadius.vertical(
                                bottom: Radius.circular(8.0),
                              ),
                            ),
                            child: Text(
                              deck['name'], // Display the deck name
                              style: const TextStyle(
                                color: Colors.black,
                                fontSize: 12,
                                fontWeight: FontWeight.normal,
                                fontFamily: 'Verdana',
                                fontStyle: FontStyle.italic,
                              ),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ],
                      ),
                    );
                  }
                },
              );
            }
          },
        ),
      ),
    );
  }
}

class PackOpenerScreen extends StatefulWidget {
  const PackOpenerScreen({super.key});

  @override
  _PackOpenerScreenState createState() => _PackOpenerScreenState();
  // State<MyHomePage> createState() => _MyHomePageState();
}

class _PackOpenerScreenState extends State<PackOpenerScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic> cards = [];
  late String username;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    username = ModalRoute.of(context)?.settings.arguments as String? ?? 'Guest';
  }

  Future<void> fetchPack() async {
    try {
      final pack = await _apiService.openPack(username);
      setState(() {
        cards = pack;
      });
    } catch (e) {
      print('Error fetching pack: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pack Opener')),
      body: Column(
        children: [
          ElevatedButton(
            onPressed: fetchPack,
            child: const Text('Open Pack'),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: cards.length,
              itemBuilder: (context, index) {
                final card = cards[index];
                return Padding(
                  padding: const EdgeInsets.all(
                      16.0), // Add some spacing between cards
                  child: Column(
                    children: [
                      // Card Image
                      Container(
                        height: MediaQuery.of(context).size.height *
                            0.6, // 60% of screen height
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: Colors.transparent),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(20),
                          child: Image.network(
                            card['image'],
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return const Icon(Icons.image_not_supported,
                                  size: 50);
                            },
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      // Card Title
                      Text(
                        card['name'],
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      // Card Subtitle
                      Text(
                        'Rarity: ${card['rarity']}',
                        style: const TextStyle(fontSize: 16),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
