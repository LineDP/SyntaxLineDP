package main;

import java.util.List;

public class OUT {
	private List<String> filename;
	private List<String> codelines;
	private List<String> is_test_file;
	private List<String> file_label;
	private List<String> line_label;
	private List<String> line_number;
	private List[] ast;
	
	public OUT(List<String> filename,List<String> codelines,List<String> is_test_file,List<String> file_label,List<String> line_label,List<String> line_number,List[] ast) {
		this.filename=filename;
		this.codelines=codelines;
		this.is_test_file=is_test_file;
		this.file_label=file_label;
		this.line_label=line_label;
		this.line_number=line_number;
		this.ast=ast;
	}
}
