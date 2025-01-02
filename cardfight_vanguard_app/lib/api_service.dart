import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://127.0.0.1:8000/api";

  Future<List<dynamic>> openPack() async {
    final response = await http.get(Uri.parse('$baseUrl/open-pack/'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception("Failed to load pack");
    }
  }
}
