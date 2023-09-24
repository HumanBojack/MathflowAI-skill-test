import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mathflow.ai question app',
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String question = '';
  int questionId = -1;
  int money = 0;
  int moneyBuffer = 0;
  String apiUrl = "http://10.0.2.2:8000";
  int userId = 1;

  @override
  void initState() {
    super.initState();
    fetchQuestion();
    fetchMoney();
  }

  Future<void> fetchQuestion() async {
    final response = await http.get(Uri.parse('$apiUrl/random?user_id=$userId'));
    if (response.statusCode == 200) {
      final data = json.decode(utf8.decode(response.bodyBytes));
      setState(() {
        question = data['question'];
        questionId = data['id'] ?? -1;
      });
    } else {
      throw Exception('Failed to load question');
    }
  }

  Future<void> sendAnswer(bool isTrue) async {
    final answer = {
      "user_id": userId,
      "question_id": questionId,
      "answer": isTrue
    };

    final response = await http.post(
      Uri.parse('$apiUrl/answer/'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: json.encode(answer),
    );

    if (response.statusCode == 200) {
      fetchQuestion();
      fetchMoney();
    } else {
      throw Exception('Failed to send answer');
    }
  }

  Future<void> fetchMoney() async {
    final response = await http.get(Uri.parse('$apiUrl/money/$userId'));
    if (response.statusCode == 200) {
      final data = json.decode(utf8.decode(response.bodyBytes));
      setState(() {
        money = data["money"];
        moneyBuffer = data["buffer"];
      });

    } else {
      throw Exception('Failed to load money');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Mathflow.ai'),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: ElevatedButton(
              onPressed: fetchQuestion,
              child: Text('Nouvelle question'),
            ),
          ),
          Expanded(
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text(
                    'Vrai ou faux :',
                    style: TextStyle(fontSize: 20),
                  ),
                  SizedBox(height: 10),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20.0),
                    child: Text(
                      // Display the question or "error" if there is no question
                      questionId == -1 ? 'Impossible de récupérer de nouvelles questions' : question,
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(height: 20),
                  Visibility(
                    visible: questionId != -1,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        ElevatedButton(
                          onPressed: () => sendAnswer(true),
                          child: Text('Vrai'),
                        ),
                        SizedBox(width: 20),
                        ElevatedButton(
                          onPressed: () => sendAnswer(false),
                          child: Text('Faux'),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              children: [
                Text("Argent : $money"),
                Text("Argent en attente : $moneyBuffer"),
              ]
            )
          )
        ],
      ),
    );
  }
}
