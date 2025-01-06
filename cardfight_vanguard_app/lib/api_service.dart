import 'dart:convert';
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
}
