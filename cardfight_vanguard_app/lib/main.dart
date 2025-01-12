import 'package:flutter/material.dart';
import 'api_service.dart';
// import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

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
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class PasswordField extends StatefulWidget {
  final TextEditingController controller;

  PasswordField({required this.controller});

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
          ],
        ),
      ),
    );
  }
}

class CollectionScreen extends StatefulWidget {
  const CollectionScreen({Key? key}) : super(key: key);

  @override
  _CollectionScreenState createState() => _CollectionScreenState();
}

class _CollectionScreenState extends State<CollectionScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<UserCard>> cards;
  late String username;

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
      appBar: AppBar(title: Text('Collection of $username'), actions: [
        IconButton(
          icon: Icon(Icons.style),
          tooltip: 'Decks',
          onPressed: () {
            Navigator.pushNamed(context, '/decks', arguments: username);
          },
        )
      ]),
      body: RefreshIndicator(
        onRefresh: () async {
          setState(() {
            cards = fetchUserCards();
          });
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
              final cards = snapshot.data!;
              return GridView.builder(
                padding: const EdgeInsets.all(4.0),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 4,
                  mainAxisSpacing: 8.0,
                  crossAxisSpacing: 8.0,
                  childAspectRatio: 2 / 3, // Aspect ratio for card size
                ),
                itemCount: cards.length,
                itemBuilder: (context, index) {
                  final card = cards[index];
                  return Card(
                    margin: const EdgeInsets.all(8.0),
                    elevation: 4.0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Stack(
                      // alignment: Alignment
                      //     .bottomCenter, // Aligns content to the bottom
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
                        // Superimposed text at the bottom
                        Positioned(
                          bottom:
                              0.0, // Adjust the distance from the bottom edge
                          left: 0.0, // Optional: adjust horizontal positioning
                          right: 0.0, // Optional: adjust horizontal positioning
                          child: Align(
                            alignment: Alignment.bottomCenter,
                            child: Container(
                              padding: EdgeInsets.all(0.0),
                              color: Colors.black.withAlpha(0),
                              child: Text(
                                'x${card.count}', // Display the count
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.normal,
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
            }
          },
        ),
      ),
    );
  }
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
  const DeckListCreateScreen({Key? key}) : super(key: key);

  @override
  _DeckListCreateScreenState createState() => _DeckListCreateScreenState();
}

class _DeckListCreateScreenState extends State<DeckListCreateScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<UserCard>> cards;
  late String username;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)?.settings.arguments;
    if (args is String) {
      username = args;
    }else {
      username = 'Guest'; //never
    }
    //anything else to be done on change
  }

  Future<List<UserCard>> fetchUserDecks() async {
    try {
      // final data = await _apiService
    }
  }

}

class PackOpenerScreen extends StatefulWidget {
  const PackOpenerScreen({Key? key}) : super(key: key);

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
