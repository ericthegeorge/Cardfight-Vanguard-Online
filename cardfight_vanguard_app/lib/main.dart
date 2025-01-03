import 'package:flutter/material.dart';
import 'api_service.dart';

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
      home: const PackOpenerScreen(),
    );
  }
}

class PackOpenerScreen extends StatefulWidget {
  const PackOpenerScreen({Key? key}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  // final String title;

  @override
  _PackOpenerScreenState createState() => _PackOpenerScreenState();
  // State<MyHomePage> createState() => _MyHomePageState();
}

class _PackOpenerScreenState extends State<PackOpenerScreen> {
  final ApiService apiService = ApiService();
  List<dynamic> cards = [];

  Future<void> fetchPack() async {
    final pack = await apiService.openPack();
    setState(() {
      cards = pack;
    });
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
                          border: Border.all(color: Colors.grey),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(16),
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

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: const Text('Pack Opener')),
//       body: Column(
//         children: [
//           ElevatedButton(
//             onPressed: fetchPack,
//             child: const Text('Open Pack'),
//           ),
//           Expanded(
//             child: ListView.builder(
//               itemCount: cards.length,
//               itemBuilder: (context, index) {
//                 final card = cards[index];
//                 return Card(
//                   child: ListTile(
//                     leading: Container(
//                       width: 300,
//                       height: 438,
//                       decoration: BoxDecoration(
//                         borderRadius: BorderRadius.circular(8),
//                         border: Border.all(color: Colors.grey),
//                       ),
//                       child: ClipRRect(
//                         borderRadius: BorderRadius.circular(8),
//                         child: Image.network(
//                           card['image'],
//                           fit: BoxFit.cover,
//                           errorBuilder: (context, error, stackTrace) {
//                             return const Icon(Icons.image_not_supported);
//                           },
//                         ),
//                       ),
//                     ),
//                     title: Text(card['name']),
//                     subtitle: Text('Rarity: ${card['rarity']}'),
//                   ),
//                 );
//               },
//             ),
//           ),
//         ],
//       ),
//     );
//   }
}
