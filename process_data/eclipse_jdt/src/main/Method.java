package main;

import java.util.List;

public class Method {
	private String filename;
	private String method;
	private String method_label;
	private List<String> ast;
	
	
	public Method(String filename,String method,String method_label,List<String> ast) {
		this.filename=filename;
		this.method=method;
		this.method_label=method_label;
		this.ast=ast;
	}
}
