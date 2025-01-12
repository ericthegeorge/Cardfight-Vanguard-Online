import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000/api";

  Future<List<dynamic>> openPack(String username) async {
    final url = Uri.parse('$baseUrl/user/$username/open-pack');
    final response = await http.get(url);
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load pack");
    }
  }

  Future<http.Response> login(String username, String password) async {
    final url = Uri.parse('$baseUrl/user/$username/login/');
    final response = await http.post(
      url,
      body: {'password': password},
    );
    return response;
  }

  Future<http.Response> register(String username, String password) async {
    final url = Uri.parse('$baseUrl/user/$username/register/');
    final response = await http.post(
      url,
      body: {'password': password},
    );
    return response;
  }

  Future<List<dynamic>> userCards(String username) async {
    final url = Uri.parse('$baseUrl/user/$username/user-cards');
    final response = await http.get(url);
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load pack");
    }
  }

  Future<List<dynamic>> fetchUserDecks(String username) async {
    final url = Uri.parse('$baseUrl/user/$username/decks');
    final response = await http.get(url);
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      // print('${json.decode(response.body)}');
      // print('${response.statusCode}');
      print("${response.statusCode}");
      throw Exception("Failed to load decks");
    }
  }

  Future<List<dynamic>> createUserDeck(String username, String deckName) async {
    final url = Uri.parse('$baseUrl/user/$username/decks');
    final response = await http.post(
      url,
      body: json.encode({'name': deckName}),
      headers: {
        HttpHeaders.contentTypeHeader: 'application/json',
      },
    );
    if (response.statusCode != 201) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to create deck $deckName");
    }
  }

  Future<void> deleteDeck(String username, int deckID) async {
    final url = Uri.parse('$baseUrl/user/$username/decks/$deckID');
    final response = await http.delete(url);
    if (response.statusCode != 204) {
      throw Exception("Failed to delete deck");
    }
  }

  Future<void> updateDeck(String username, int deckID, String newName) async {
    final url = Uri.parse('$baseUrl/user/$username/decks/$deckID');
    final response = await http.put(
      url,
      body: json.encode({'name': newName}),
      headers: {
        HttpHeaders.contentTypeHeader: 'application/json',
      },
    );
    if (response.statusCode != 200) {
      throw Exception("Failed to update deck");
    }
  }
}
