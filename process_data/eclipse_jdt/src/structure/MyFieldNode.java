package structure;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.FieldDeclaration;
import structure.MyASTNode;

public class MyFieldNode {
	public FieldDeclaration fieldNode = null;
	public List<MyASTNode> nodeList = null;

	public List<int[]> mapping = null;

	public MyFieldNode() {
		this.fieldNode = null;
		this.nodeList = new ArrayList<MyASTNode>();
		this.mapping = new ArrayList<int[]>();
	}
}
