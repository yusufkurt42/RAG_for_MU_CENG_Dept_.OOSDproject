package com.cse3063.rag.answer;
import java.util.List;

public class Answer {
	String text;
	List<String> citations;
	
	public Answer(String text, List<String> list) {
		this.text = text;
		this.citations = list;
	}

	public String getText() {
		return text;
	}

	public List<String> getCitations() {
		return citations;
	}
}
