package structure;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.TypeDeclaration;
import structure.MyASTNode;

public class MyTypeNode {
	public TypeDeclaration typeNode = null;
	public List<MyASTNode> nodeList = null;

	public List<int[]> mapping = null;

	public MyTypeNode() {
		this.typeNode = null;
		this.nodeList = new ArrayList<MyASTNode>();
		this.mapping = new ArrayList<int[]>();
	}
}
